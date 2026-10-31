# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Neutral destinations and AstrBot sessions, offline."""
import ast
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot
import attention
import discretion
import events
import harness
import main
import mixin_selfie
import turn
from adapter_astrbot_messenger import AstrBotMessenger


class SendNeutral(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin._neutral_messenger = SimpleNamespace(send=AsyncMock())

    def event(self, group=None):
        return harness.FakeEvent('hello', sender='10001', name='Alice', group=group, self_id='20002')

    def neutral(self, event):
        return turn.TurnEvent(adapter_astrbot.from_astrbot(event))

    async def test_messenger_prefers_neutral_and_falls_back(self):
        port = self.plugin._neutral_messenger
        self.assertIs(self.plugin._messenger(self.event(), as_event=True), port)
        segments = (events.Segment('text', {'text': 'hello'}),)
        await self.plugin._messenger().send('group:900001', segments)
        port.send.assert_awaited_once_with('group:900001', segments)
        del self.plugin._neutral_messenger
        self.assertIsInstance(self.plugin._messenger(self.event()), AstrBotMessenger)

    async def test_send_rest_uses_neutral_group(self):
        event = self.neutral(self.event('900001'))
        self.plugin._note_sent = Mock()
        with patch.object(attention, 'typing_seconds', return_value=0):
            self.assertTrue(await self.plugin._send_rest(event, '', ['first', 'second']))
        calls = self.plugin._neutral_messenger.send.await_args_list
        self.assertEqual([call.args[0] for call in calls], ['group:900001', 'group:900001'])
        self.assertEqual([call.args[1] for call in calls],
                         [(events.Segment('text', {'text': 'first'}),),
                          (events.Segment('text', {'text': 'second'}),)])

    async def test_media_destinations_match_old_and_neutral(self):
        self.plugin._phone_clear = AsyncMock(return_value=True)
        self.plugin._make_photo = AsyncMock(return_value=Path('photo.png'))
        self.plugin._make_voice = AsyncMock(return_value=Path('voice.wav'))
        self.plugin._phone_account = Mock()
        self.plugin._note_she_sent = Mock()
        self.plugin._phone_prune = Mock()
        event = self.event('900001')
        expected = discretion.place_of(event.unified_msg_origin)
        with patch.object(mixin_selfie.asyncio, 'sleep', new_callable=AsyncMock):
            for incoming in (event, self.neutral(event)):
                self.plugin._neutral_messenger.send.reset_mock()
                await self.plugin._media_after_reply(incoming, {'photo': ('snap', 'scene'), 'voice': 'hello'})
                calls = self.plugin._neutral_messenger.send.await_args_list
                self.assertEqual([call.args[0] for call in calls], [expected, expected])
                self.assertEqual([call.args[1][0].type for call in calls], ['image', 'record'])
        self.assertEqual(expected, 'group:900001')

    async def test_autonomy_destinations_match_old_and_neutral(self):
        self.plugin.proactive_autonomy = self.plugin.proactive_send = True
        self.plugin._user_record = Mock(return_value={})
        self.plugin._relationship_of = Mock(return_value={})
        self.plugin._autonomy_gate = Mock(return_value=('hello', {}))
        event = self.event()
        expected = discretion.place_of(event.unified_msg_origin)
        for incoming in (event, self.neutral(event)):
            self.plugin._neutral_messenger.send.reset_mock()
            core = SimpleNamespace(_proactive_autonomy={})
            self.assertTrue(await self.plugin._maybe_proactive_send(incoming, core, now=1000))
            self.assertEqual(self.plugin._neutral_messenger.send.await_args.args[0], expected)
        self.assertEqual(expected, 'private:10001')

    async def test_window_preserves_session_for_neutral_event(self):
        event = self.event('900001')
        window = {'recent': [], 'umo': 'old'}
        self.plugin._read_window = Mock(return_value=window)
        self.plugin._write_window = Mock()
        self.plugin._job_stale = Mock(return_value=False)
        self.plugin._remember_images = Mock()
        self.plugin._note_name = Mock()
        self.plugin._window_add_message(event)
        self.assertEqual(window['umo'], event.unified_msg_origin)
        self.plugin._window_add_message(self.neutral(event))
        self.assertEqual(window['umo'], event.unified_msg_origin)
        self.assertEqual(len(window['recent']), 2)
        self.assertEqual(self.plugin._write_window.call_count, 2)

    async def test_no_other_event_session_place_reads(self):
        root = Path(__file__).resolve().parent.parent
        found = []
        for name in ('ports', 'attention', 'selfie', 'autonomy', 'phone'):
            tree = ast.parse((root / ('mixin_' + name + '.py')).read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for call in ast.walk(node):
                        if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and call.func.attr == 'place_of':
                            if any(isinstance(x, ast.Constant) and x.value == 'unified_msg_origin' for x in ast.walk(call)):
                                found.append((name, node.name))
        self.assertEqual(found, [('ports', '_messenger')])


if __name__ == '__main__':
    unittest.main()
