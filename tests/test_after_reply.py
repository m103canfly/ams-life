# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for the reply handle integration."""
import ast
import asyncio
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test_basics  # noqa: E402,F401

import adapter_astrbot_turn as adapter  # noqa: E402
import attention  # noqa: E402
import browse  # noqa: E402
import main  # noqa: E402
import messenger  # noqa: E402
import mixin_browse  # noqa: E402
import turn  # noqa: E402
from astrbot.api.provider import LLMResponse  # noqa: E402
from mixin_attention import AttentionMixin  # noqa: E402
from mixin_send_check import SendCheckMixin  # noqa: E402


def run_case(mode):
    with tempfile.TemporaryDirectory() as tmp:
        data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
        data.mkdir()
        env = dict(os.environ, PYTHONHASHSEED='0')
        env.pop('AMS_LIFE_DATA_DIR', None)
        proc = subprocess.run([sys.executable, str(HERE / 'after_reply_cases.py'), str(data), str(out), mode],
                              env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
        if proc.returncode:
            raise AssertionError(proc.stdout + '\n' + proc.stderr)
        return json.loads(out.read_text('utf-8'))


class AfterReplyTests(unittest.TestCase):
    def test_paths_and_rounds(self):
        astrbot, neutral = run_case('astrbot'), run_case('neutral')
        self.assertEqual(astrbot, neutral)
        rows = astrbot['rounds']
        self.assertEqual(rows[0]['first'], [['text', 'hello'], ['face', 14]])
        self.assertEqual(rows[1]['rest'], ['second'])
        self.assertNotIn('<bc>', rows[2]['kept'])
        self.assertEqual(rows[3]['first'][0], ['reply', '900001'])
        self.assertEqual(rows[4]['outcome'], 'silent')
        self.assertTrue(rows[4]['stopped'])
        self.assertEqual(rows[5]['outcome'], 'failed')
        self.assertTrue(rows[5]['cleared'] and rows[5]['stopped'])
        self.assertGreater(rows[6]['spend'], 0)
        self.assertEqual(rows[6]['spend'], round(rows[5]['spend'] + attention.cost(
            {'input_hit': 300, 'input_miss': 500, 'output': 200}, astrbot['price']), 6))
        self.assertTrue(all(row['spend'] == 0 for row in rows[:6]))

    def test_usage_handles(self):
        raw = types.SimpleNamespace(prompt_cache_hit_tokens=3, prompt_cache_miss_tokens=5, completion_tokens=2)
        usage = types.SimpleNamespace(input_cached=7, input_other=11, output=4)
        for raw_usage, reported in [(raw, usage), (None, usage), (None, None)]:
            response = LLMResponse('hello')
            response.raw_completion = types.SimpleNamespace(usage=raw_usage)
            response.usage = reported
            self.assertEqual(AttentionMixin._usage_of(response), AttentionMixin._usage_of(adapter.AstrBotReply(response)))
        u = {'input_hit': 3, 'input_miss': 5, 'output': 2}
        reply = turn.TurnReply(usage=u)
        result = AttentionMixin._usage_of(reply)
        self.assertEqual(result, u)
        self.assertIsNot(result, reply.usage)

    def test_browse_handles(self):
        plugin = object.__new__(main.BioCorePlugin)
        for usage in (types.SimpleNamespace(input_other=5, input_cached=3, output=2), None):
            response = LLMResponse('hello')
            response.usage = usage
            records = []
            plugin._browse_ledger = lambda: types.SimpleNamespace(add=lambda **kw: records.append(kw))
            event = types.SimpleNamespace()
            setattr(event, mixin_browse.QUOTA_ATTR, types.SimpleNamespace(calls=lambda: 2))
            for value in (response, adapter.AstrBotReply(response), turn.TurnReply(usage=browse.usage_of(usage))):
                plugin._browse_after_reply(event, value)
            self.assertEqual(records[0], records[1])
            self.assertEqual(records[0], records[2])

    def test_handle_types_and_set(self):
        mock = MagicMock()
        wrapped = adapter.reply_handle(mock)
        self.assertIsInstance(wrapped, adapter.AstrBotReply)
        self.assertIs(wrapped.response, mock)
        neutral = turn.TurnReply(text='a')
        self.assertIs(adapter.reply_handle(neutral), neutral)
        self.assertIs(adapter.reply_handle(wrapped), wrapped)
        SendCheckMixin._set_reply(neutral, 'b')
        self.assertEqual(neutral.text, 'b')

    def test_shape_neutral(self):
        async def run():
            plugin = object.__new__(main.BioCorePlugin)
            async def send_rest(*args):
                pass
            plugin._send_rest = send_rest
            plugin._note_sent = lambda *args: None
            reply = turn.TurnReply(text='x【下一条】y')
            self.assertEqual(plugin._shape_reply(types.SimpleNamespace(), reply, reply.text, then=None), 'x\ny')
            self.assertEqual(reply.first_message, list(messenger.text_segments('x')))
            await asyncio.sleep(0)
        asyncio.run(run())

    def test_source_boundary(self):
        main_source = (HERE.parent / 'main.py').read_text('utf-8')
        self.assertNotIn('_reply_response', main_source)
        for path, name, expected, absent in [('main.py', 'on_llm_response', ('_after_reply', 'reply_handle'), ()),
                                              ('mixin_turn.py', '_after_reply', (),
                                               ('completion_text', 'result_chain', 'LLMResponse'))]:
            source = (HERE.parent / path).read_text('utf-8')
            node = next(n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.AsyncFunctionDef) and n.name == name)
            body = ast.get_source_segment(source, node)
            for item in expected:
                self.assertIn(item, body)
            for item in absent:
                self.assertNotIn(item, body)
