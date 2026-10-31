# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Neutral model routing, spending and retry compatibility."""
import asyncio
import inspect
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot_model
import attention
import harness
import main
import mixin_attention
import mixin_ports
import mixin_send_check
import model_client


USAGE = {'input_hit': 20, 'input_miss': 100, 'output': 30}


class FakeModel(model_client.ModelClient):
    def __init__(self, usage=None):
        self.usage = USAGE if usage is None else usage
        self.calls = []

    async def chat(self, **kwargs):
        self.calls.append(kwargs)
        return model_client.ModelReply('重说的话<bc>{}</bc>', (), self.usage, '')


class FakeProvider:
    def __init__(self):
        self.calls = []

    async def text_chat(self, **kwargs):
        self.calls.append(kwargs)
        usage = SimpleNamespace(input_cached=20, input_other=100, output=30, total=150)
        return SimpleNamespace(completion_text='重说的话<bc>{}</bc>', usage=usage)


# mixin_send_check.py 121-153 at d20f2fa.
OLD_REDO = '''async def old_redo_reply(self, event):
    note = self._check_note(event)
    req = note.get("req")
    if req is None:
        return None
    try:
        provider = self.context.get_using_provider(str(getattr(event, "unified_msg_origin", "") or ""))
    except Exception:
        provider = None
    if provider is None:
        return None
    system = getattr(req, "system_prompt", None)
    compact = note.get("compact", "")
    if compact and compact in str(system or ""):
        compact = ""
    prompt = "\\n\\n".join(x for x in (compact, str(getattr(req, "prompt", "") or ""), send_check.REDO_NOTE) if x)
    self._count_check("redo_calls")
    try:
        resp = await provider.text_chat(prompt=prompt, contexts=list(getattr(req, "contexts", None) or []),
                                        system_prompt=system,
                                        image_urls=list(getattr(req, "image_urls", None) or []))
    except Exception as exc:
        logger.warning("[ams-life] send check: asking once more failed: %s", type(exc).__name__)
        return None
    if getattr(self, "self_decide", False):
        self._note_spend("redo", resp)
    usage = getattr(resp, "usage", None)
    if usage is not None:
        self._count_check("redo_tokens", int(getattr(usage, "total", 0) or 0))
    text = interpretation.strip_state_tags(str(getattr(resp, "completion_text", "") or "")).strip()
    return text or None
'''
_old_namespace = dict(vars(mixin_send_check))
exec(OLD_REDO, _old_namespace)
old_redo_reply = _old_namespace['old_redo_reply']


class ModelPortTest(unittest.TestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.config = {}
        self.plugin.self_decide = True
        self.plugin.context = harness.FakeContext()

    def test_model_for_neutral_and_astrbot(self):
        model = FakeModel()
        self.assertIs(mixin_ports.model_for(model), model)
        self.assertIsInstance(mixin_ports.model_for(FakeProvider()), adapter_astrbot_model.AstrBotModel)

    def test_spending_wraps_once_and_respects_setting(self):
        model = FakeModel()
        wrapped = self.plugin._spending('reply', model)
        self.assertIsInstance(wrapped, mixin_attention._SpendingModel)
        self.assertIs(self.plugin._spending('reply', wrapped), wrapped)
        self.plugin.self_decide = False
        self.assertIs(self.plugin._spending('reply', model), model)

    def test_model_usage_and_spending(self):
        model = FakeModel()
        data = {}
        with patch.object(mixin_attention, '_read_json', return_value=data), patch.object(mixin_attention, '_write_json'):
            reply = asyncio.run(self.plugin._spending('reply', model).chat(prompt='hello'))
        self.assertEqual(self.plugin._usage_of(reply), USAGE)
        day = next(iter(data.values()))
        self.assertEqual(day['reply'], round(attention.cost(USAGE, mixin_attention.DEFAULT_PRICES), 6))
        self.assertEqual(day['calls'], 1)

    def test_provider_for_neutral_and_context(self):
        model = FakeModel()
        self.plugin._neutral_model = model
        self.plugin._function_cfg = Mock(side_effect=AssertionError('should not look up settings'))
        self.plugin.self_decide = False
        self.assertIs(asyncio.run(self.plugin._provider_for('reply')), model)
        self.plugin.self_decide = True
        self.assertIs(asyncio.run(self.plugin._provider_for('reply'))._model, model)
        del self.plugin._neutral_model
        self.plugin._function_cfg = Mock(return_value={'provider': 'follow_llm'})
        self.plugin.self_decide = False
        self.assertIs(asyncio.run(self.plugin._provider_for('reply')), self.plugin.context.provider)

    def run_redo(self, method, neutral=None, decide=True):
        plugin = self.plugin
        plugin.self_decide = decide
        provider = FakeProvider()
        plugin.context.provider = provider
        if neutral is not None:
            plugin._neutral_model = neutral
        req = SimpleNamespace(prompt='hello', system_prompt='system', contexts=[{'role': 'user', 'content': 'before'}], image_urls=[])
        plugin._check_note = Mock(return_value={'req': req, 'compact': 'compact'})
        counts, data = {}, {}
        def count(key, value=1):
            counts[key] = counts.get(key, 0) + value
        plugin._count_check = count
        with patch.object(mixin_attention, '_read_json', return_value=data), patch.object(mixin_attention, '_write_json'):
            text = asyncio.run(method(plugin, harness.FakeEvent('hello')))
        day = next(iter(data.values()), {})
        return text, counts, day, provider.calls

    def test_redo_neutral_counts_and_spending(self):
        model = FakeModel()
        text, counts, day, _ = self.run_redo(type(self.plugin)._redo_reply, model)
        self.assertEqual(text, '重说的话')
        self.assertEqual(counts, {'redo_calls': 1, 'redo_tokens': 150})
        self.assertEqual(day, {'redo': round(attention.cost(USAGE, mixin_attention.DEFAULT_PRICES), 6), 'calls': 1})
        self.assertEqual(model.calls[0]['messages'], [{'role': 'user', 'content': 'before'}])

    def test_redo_astrbot_matches_frozen_method(self):
        for decide in (False, True):
            with self.subTest(decide=decide):
                old = self.run_redo(old_redo_reply, decide=decide)
                new = self.run_redo(type(self.plugin)._redo_reply, decide=decide)
                self.assertEqual(new, old)

    def test_redo_zero_tokens_are_not_counted(self):
        _, counts, _, _ = self.run_redo(type(self.plugin)._redo_reply, FakeModel({}))
        self.assertEqual(counts, {'redo_calls': 1})

    def test_redo_uses_model_port(self):
        self.assertNotIn('.text_chat(', inspect.getsource(mixin_send_check.SendCheckMixin._redo_reply))
