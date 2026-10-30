# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Port entry points and the remaining parts of a split reply, offline."""
import asyncio
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))

import harness  # noqa: E402
import attention  # noqa: E402
import adapter_astrbot  # noqa: E402
import main  # noqa: E402
from adapter_astrbot_messenger import AstrBotMessenger  # noqa: E402
from adapter_astrbot_model import AstrBotModel  # noqa: E402
from mixin_ports import PortsMixin  # noqa: E402


class Ports(unittest.TestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.context = harness.FakeContext()
        self.event = harness.FakeEvent('hello', group='900001')
        self.plugin._read_window = Mock(return_value={'umo': 'default:GroupMessage:900002'})

    def test_umo_of_event_window_and_missing(self):
        self.assertEqual(self.plugin._umo_of('group:900001', self.event), self.event.unified_msg_origin)
        self.assertEqual(self.plugin._umo_of('group:900002', self.event), 'default:GroupMessage:900002')
        self.plugin._read_window.return_value = {}
        self.assertEqual(self.plugin._umo_of('group:900003', self.event), '')
        self.assertEqual(self.plugin._umo_of('', self.event), '')
        self.plugin._read_window.side_effect = OSError('unreadable')
        self.assertEqual(self.plugin._umo_of('group:900003'), '')

    def test_messenger_resolves_session_and_bot(self):
        self.event.bot = object()
        port = self.plugin._messenger(self.event)
        self.assertIsInstance(port, AstrBotMessenger)
        for place in ('group:900001', 'group:900002'):
            self.assertEqual(port.umo_of(place), self.plugin._umo_of(place, self.event))
        self.assertIs(port.bot_of(), self.event.bot)
        self.assertIsNone(self.plugin._messenger().bot_of())
        self.assertIsNot(port, self.plugin._messenger(self.event))

    def test_model_wraps_provider(self):
        provider = object()
        port = self.plugin._model(provider)
        self.assertIsInstance(port, AstrBotModel)
        self.assertIs(port.provider, provider)
        self.assertIsNot(port, self.plugin._model(provider))

    def test_incoming_matches_adapter_except_time(self):
        actual = self.plugin._incoming(self.event)
        expected = adapter_astrbot.from_astrbot(self.event)
        self.assertEqual(replace(actual, ts=expected.ts), expected)

    def test_split_reply_sends_same_components(self):
        parts = attention.split('first\n【下一条】\nsecond[表情:微笑]end\n【下一条】\nthird')
        self.assertEqual(len(parts), 3)
        sent = []

        async def record(umo, chain):
            sent.append((umo, chain.chain))

        self.plugin.context.send_message = record
        self.plugin._note_sent = Mock()
        with patch('mixin_attention.asyncio.sleep', new_callable=AsyncMock):
            result = asyncio.run(self.plugin._send_rest(self.event, self.event.unified_msg_origin, parts[1:]))
        self.assertTrue(result)
        self.assertEqual(len(sent), 2)
        for (umo, chain), part in zip(sent, parts[1:]):
            self.assertEqual(umo, self.event.unified_msg_origin)
            shape = lambda items: [(type(c).__name__, getattr(c, 'text', None), getattr(c, 'id', None))
                                   for c in items]
            self.assertEqual(shape(chain), shape(self.plugin._chain_of(part).chain))
        self.assertIn('Face', [type(c).__name__ for c in sent[0][1]])

    def test_send_error_warns_and_stops(self):
        self.plugin.context.send_message = AsyncMock(side_effect=OSError('failed'))
        self.plugin._note_sent = Mock()
        with patch('mixin_attention.asyncio.sleep', new_callable=AsyncMock), \
                patch('mixin_attention.logger.warning') as warning:
            result = asyncio.run(self.plugin._send_rest(self.event, self.event.unified_msg_origin,
                                                        ['second', 'third']))
        self.assertFalse(result)
        self.plugin.context.send_message.assert_awaited_once()
        self.plugin._note_sent.assert_not_called()
        warning.assert_called_once()

    def test_ports_mixin_is_the_only_owner_of_names(self):
        self.assertIn(PortsMixin, main.BioCorePlugin.__mro__)
        for name in ('_umo_of', '_messenger', '_model', '_incoming'):
            owners = [cls for cls in main.BioCorePlugin.__mro__ if name in vars(cls)]
            self.assertEqual(owners, [PortsMixin], name)
