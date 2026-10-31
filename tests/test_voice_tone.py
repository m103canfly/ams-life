# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline coverage for voice tone selection and dispatch."""
import sys
import types
import unittest
from unittest.mock import AsyncMock, Mock, patch

from tests import test_selfie
import tts
import mixin_selfie as phone
from astrbot.api.provider import ProviderRequest


class ToneFor(unittest.TestCase):
    def test_thresholds_and_priority(self):
        cases = [
            ((-0.30, 0.9, 0.8), '难过'),
            ((0.8, 0.9, 0.60), '认真'),
            ((0.35, 0.55, 0.1), '开心'),
            ((0.10, 0.1, 0.1), '温柔'),
            ((0.0, 0.0, 0.1), '平静'),
            ((0.35, 0.54, 0.1), '温柔'),
        ]
        for values, expected in cases:
            with self.subTest(values=values):
                self.assertEqual(tts.tone_for(*values), expected)

    def test_invalid_values_are_calm(self):
        for values in [(None, 0.8, 0.1), (0.8, 'bad', 0.1), (0.8, 0.8, object()),
                       (float('nan'), 0.8, 0.1), (0.8, float('inf'), 0.1)]:
            with self.subTest(values=values):
                self.assertEqual(tts.tone_for(*values), '平静')


class VoiceTone(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.p = test_selfie.Phone()
        self.event = test_selfie.Event()

    async def test_tool_schema(self):
        module = types.ModuleType('astrbot.core.agent.tool')
        module.FunctionTool, module.ToolSet = test_selfie.FunctionTool, test_selfie.ToolSet
        with patch.dict(sys.modules, {'astrbot.core.agent.tool': module}):
            req = ProviderRequest()
            self.p._give_phone_tools(req, self.event)
        tool = next(tool for tool in req.func_tool.tools if tool.name == 'say_aloud')
        self.assertEqual(tool.parameters['required'], ['text'])
        self.assertEqual(tool.parameters['properties']['tone'], {
            'type': 'string', 'enum': ['开心', '平静', '温柔', '认真', '难过'],
            'description': '语气，可以不填：不填就按你现在的心情'})

    async def test_queue_accepts_only_known_tone(self):
        await self.p._tool_say_aloud(self.event, '你好', tone='温柔')
        self.assertEqual(self.p._phone_queue(self.event)['voice_tone'], '温柔')
        event = test_selfie.Event()
        await self.p._tool_say_aloud(event, '你好', tone='生气')
        self.assertNotIn('voice_tone', self.p._phone_queue(event))

    async def test_make_voice_uses_explicit_mood_and_fallback(self):
        core = types.SimpleNamespace(v=0.5, energy=0.8, stress=0.1, _decay_to_now=Mock())
        self.p._core = Mock(return_value=core)
        self.p._post_json = AsyncMock(return_value=(b'audio', 'audio/wav'))
        self.p._phone_path = Mock(return_value=Mock())
        self.p._phone_account = Mock()
        await self.p._make_voice('你好', tone='认真')
        self.assertEqual(self.p._post_json.await_args.args[1]['voice'], '认真')
        self.p._core.assert_not_called()
        await self.p._make_voice('你好')
        self.assertEqual(self.p._post_json.await_args.args[1]['voice'], '开心')
        self.p._core.assert_called_once_with(None)
        core._decay_to_now.assert_called_once_with()
        self.p._core.side_effect = RuntimeError('unavailable')
        await self.p._make_voice('你好')
        self.assertEqual(self.p._post_json.await_args.args[1]['voice'], '平静')

    async def test_dispatch_preserves_single_argument_without_tone(self):
        self.p._make_voice = AsyncMock(return_value=None)
        with patch.object(phone, 'SEND_DELAY', 0):
            await self.p._media_after_reply(self.event, {'voice': '你好', 'voice_tone': '温柔'})
            self.p._make_voice.assert_awaited_once_with('你好', tone='温柔')
            self.p._make_voice.reset_mock()
            await self.p._media_after_reply(self.event, {'voice': '你好'})
            self.p._make_voice.assert_awaited_once_with('你好')
