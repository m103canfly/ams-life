# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Compare reply handles with the existing AstrBot behavior."""
import ast
import copy
import sys
import types
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test_basics  # noqa: E402,F401

import adapter_astrbot_turn as adapter  # noqa: E402
import browse  # noqa: E402
import attention  # noqa: E402
import events  # noqa: E402
import interpretation  # noqa: E402
import main  # noqa: E402
import messenger  # noqa: E402
import turn  # noqa: E402
from astrbot.api.event import MessageChain  # noqa: E402
from astrbot.api.message_components import At, Face, Plain, Reply  # noqa: E402
from astrbot.api.provider import LLMResponse  # noqa: E402
from mixin_attention import AttentionMixin  # noqa: E402
from mixin_send_check import SendCheckMixin  # noqa: E402


def components(chain):
    return [(type(c), getattr(c, 'text', None), getattr(c, 'id', None))
            for c in (chain.chain if chain is not None else [])]


def old_map_words(response):
    # main.py 751-765 at c209cf5.
    _reply = str(getattr(response, "completion_text", "") or "")
    _clean = interpretation.strip_state_tags(_reply)
    if _clean != _reply:
        try:
            response.completion_text = _clean
            chain = getattr(response, "result_chain", None)
            if chain is not None and getattr(chain, "chain", None):
                for comp in chain.chain:
                    if hasattr(comp, "text"):
                        comp.text = interpretation.strip_state_tags(str(comp.text or ""))
        except Exception:
            pass
    _reply = _clean
    return _reply


def old_set_reply(response, text):
    # mixin_send_check.py 199-212 at 92febba.
    response.completion_text = text
    chain = getattr(response, "result_chain", None)
    if chain is not None and getattr(chain, "chain", None):
        first = True
        kept = []
        for comp in chain.chain:
            if hasattr(comp, "text"):
                if first:
                    comp.text = text
                    kept.append(comp)
                    first = False
                continue   # the other text parts were the old words
            kept.append(comp)
        chain.chain = kept


def old_chain_of(text):
    # mixin_attention.py 379-385 at 92febba.
    chain = []
    for kind, value in attention.pieces(text):
        chain.append(Face(id=value) if kind == "face" else Plain(value))
    return MessageChain(chain)


def old_shape_first(response, first):
    # mixin_attention.py 429-434 at 92febba.
    previous = getattr(getattr(response, "result_chain", None), "chain", None) or []
    prefix = [component for component in previous if isinstance(component, (Reply, At))]
    shaped = old_chain_of(first)
    shaped.chain = prefix + shaped.chain
    response.result_chain = shaped


class ReplyHandleTests(unittest.TestCase):
    def assert_response_equal(self, old, new):
        self.assertEqual(old.completion_text, new.completion_text)
        self.assertEqual(components(old.result_chain), components(new.result_chain))

    def test_set_text_matches_send_check(self):
        cases = [(None, 'new'),
                 ([Reply(id='900001'), Plain('old'), At(id='10001', text='old')], 'new'),
                 ([Plain('one'), Plain('two'), Face(id=14)], 'new'),
                 ([Reply(id='900001'), Plain('old'), At(id='10001')], '')]
        for chain, text in cases:
            with self.subTest(chain=chain, text=text):
                response = LLMResponse('old', MessageChain(chain) if chain is not None else None)
                old, new, plugin = (copy.deepcopy(response) for _ in range(3))
                old_set_reply(old, text)
                adapter.AstrBotReply(new).set_text(text)
                SendCheckMixin._set_reply(plugin, text)
                self.assert_response_equal(old, new)
                self.assert_response_equal(old, plugin)

    def test_map_words_matches_main(self):
        tagged = 'hello<bc>{}</bc>'
        cases = [LLMResponse(tagged), LLMResponse('', MessageChain([Reply(id='900001'), Plain(tagged)])),
                 LLMResponse('', MessageChain([Reply(id='900001'), Plain('hello')]))]
        for response in cases:
            with self.subTest(text=response.completion_text):
                old, new = copy.deepcopy(response), copy.deepcopy(response)
                self.assertEqual(old_map_words(old), adapter.AstrBotReply(new).map_words(interpretation.strip_state_tags))
                self.assert_response_equal(old, new)

    def test_spend_usage_matches_attention(self):
        raw = types.SimpleNamespace(prompt_cache_hit_tokens=3, prompt_cache_miss_tokens=5, completion_tokens=2)
        usage = types.SimpleNamespace(input_cached=7, input_other=11, output=4)
        for raw_usage, reported in [(raw, usage), (None, usage), (None, None)]:
            response = LLMResponse('hello')
            response.raw_completion = types.SimpleNamespace(usage=raw_usage)
            response.usage = reported
            old, new = copy.deepcopy(response), copy.deepcopy(response)
            self.assertEqual(AttentionMixin._usage_of(old), adapter.AstrBotReply(new).spend_usage())

    def test_reported_usage_and_estimate(self):
        for usage in (types.SimpleNamespace(input_other=5, input_cached=3, output=2), None):
            response = LLMResponse('hello')
            response.usage = usage
            old, new = copy.deepcopy(response), copy.deepcopy(response)
            reported = adapter.AstrBotReply(new).reported_usage()
            self.assertEqual(reported, browse.usage_of(old.usage))
            self.assertEqual(browse.reply_estimate(3, reported), browse.reply_estimate(3, old.usage))

    def test_shape_first_matches_plugin(self):
        plugin = object.__new__(main.BioCorePlugin)
        plugin._note_sent = lambda *args: None
        plugin._send_rest = lambda *args: None
        for chain, text in [([Reply(id='900001'), Plain('old'), At(id='10001')], 'hello'),
                            ([Plain('old'), Reply(id='900001'), At(id='10001')], 'hello[表情:微笑]')]:
            response = LLMResponse('', MessageChain(chain))
            old, new, shaped = (copy.deepcopy(response) for _ in range(3))
            first = attention.split(text)[0]
            old_shape_first(old, first)
            plugin._shape_reply(types.SimpleNamespace(), shaped, text, then=None)
            adapter.AstrBotReply(new).shape_first(first)
            self.assert_response_equal(old, new)
            self.assert_response_equal(old, shaped)

    def test_chain_of_matches_attention(self):
        for text in ('hello', 'hello[表情:微笑]', '[表情:不存在]'):
            self.assertEqual(components(old_chain_of(text)), components(AttentionMixin._chain_of(text)))
            self.assertEqual(components(old_chain_of(text)), components(adapter.chain_of(text)))

    def test_neutral_reply(self):
        prefix = [events.Segment('reply', {'id': '900001'})]
        reply = turn.TurnReply(text='old', chain_prefix=prefix, usage={'input_hit': 3, 'input_miss': 5, 'output': 2})
        self.assertIsNone(reply.first_message)
        reply.set_text('hello<bc>{}</bc>')
        self.assertEqual(reply.map_words(interpretation.strip_state_tags), 'hello')
        self.assertEqual(reply.text, 'hello')
        reply.shape_first('hello[表情:微笑]')
        self.assertEqual(reply.first_message, prefix + list(messenger.text_segments('hello[表情:微笑]')))
        for result in (reply.spend_usage(), reply.reported_usage()):
            self.assertEqual(result, reply.usage)
            result['output'] = 99
            self.assertEqual(reply.usage['output'], 2)
        reply.set_text(None)
        self.assertEqual(reply.text, '')

    def test_reply_handle_idempotent(self):
        neutral = turn.TurnReply()
        response = LLMResponse('hello')
        handle = adapter.reply_handle(response)
        self.assertIs(adapter.reply_handle(neutral), neutral)
        self.assertIsInstance(handle, adapter.AstrBotReply)
        self.assertIs(handle.response, response)
        self.assertIs(adapter.reply_handle(handle), handle)

    def test_usage_of_formats(self):
        own = {'input_miss': '5', 'input_hit': -3, 'output': 2}
        self.assertEqual(browse.usage_of(own), {'input_miss': 5, 'input_hit': 0, 'output': 2})
        self.assertEqual(browse.usage_of({'input_miss': 5, 'input_hit': 3, 'output': 2}),
                         {'input_miss': 5, 'input_hit': 3, 'output': 2})
        self.assertEqual(browse.usage_of({'input_miss': 5, 'input_hit': 3, 'output': 2, 'prompt_tokens': 10}),
                         {'input_miss': 10, 'input_hit': 0, 'output': 2})
        self.assertEqual(browse.usage_of(types.SimpleNamespace(input_other=5, input_cached=3, output=2)),
                         {'input_miss': 5, 'input_hit': 3, 'output': 2})
        self.assertEqual(browse.usage_of({'prompt_tokens': 8, 'cached_tokens': 3, 'completion_tokens': 2}),
                         {'input_miss': 5, 'input_hit': 3, 'output': 2})
        self.assertEqual(browse.usage_of(None), {'input_miss': 0, 'input_hit': 0, 'output': 0})

    def test_turn_has_no_astrbot_import(self):
        tree = ast.parse((HERE.parent / 'turn.py').read_text('utf-8'))
        imports = [alias.name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
                   for alias in node.names]
        modules = [node.module or '' for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        self.assertFalse(any(name.startswith('astrbot') for name in imports + modules))
