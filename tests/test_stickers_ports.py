# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Sticker sends through the messenger, offline."""
import asyncio
import base64
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))

import harness  # noqa: E402
import main  # noqa: E402
import stickers  # noqa: E402
from astrbot.api.message_components import Image  # noqa: E402


class Bot:
    def __init__(self, fail=False):
        self.calls = []
        self.fail = fail

    async def call_action(self, action, **params):
        if self.fail:
            raise RuntimeError('send failed')
        self.calls.append((action, params))


class StickerPorts(unittest.TestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.context = harness.FakeContext()
        self.plugin.context.send_message = AsyncMock()
        self.plugin._may_speak_in = Mock(return_value=True)
        self.plugin._note_sent = Mock()
        self.lib = Mock()
        self.lib.rows = {'sticker': {'file': 'picture', 'source': 'old'}}
        self.data = b'sticker picture'
        self.b64 = base64.b64encode(self.data).decode('ascii')
        self.lib.path_of.return_value.read_bytes.return_value = self.data
        self.plugin._sticker_lib = Mock(return_value=self.lib)
        self.event = harness.FakeEvent('hello', group='900001')
        self.place = 'group:900001'
        self.port = self.plugin._messenger(self.event)
        self.port.call = AsyncMock(wraps=self.port.call)
        self.port.send = AsyncMock(wraps=self.port.send)
        self.plugin._messenger = Mock(return_value=self.port)

    def send(self):
        return asyncio.run(self.plugin._send_sticker(
            self.event, 'sticker', self.event.unified_msg_origin, self.place))

    def assert_picture(self):
        self.plugin.context.send_message.assert_awaited_once()
        umo, chain = self.plugin.context.send_message.await_args.args
        self.assertEqual(umo, self.event.unified_msg_origin)
        expected = Image.fromBase64(self.b64)
        self.assertEqual(len(chain.chain), 1)
        self.assertIsInstance(chain.chain[0], Image)
        self.assertEqual(chain.chain[0].file, expected.file)
        self.port.send.assert_awaited_once()

    def test_sticker_action_and_params(self):
        self.event.bot = Bot()
        self.assertTrue(self.send())
        self.assertEqual(self.event.bot.calls, [stickers.send_params(self.place, self.b64)])
        self.port.call.assert_awaited_once()
        self.port.send.assert_not_awaited()
        self.plugin.context.send_message.assert_not_awaited()
        self.lib.use.assert_called_once()
        self.plugin._note_sent.assert_called_once_with(self.event, 1)

    def test_failed_sticker_warns_and_sends_picture(self):
        self.event.bot = Bot(fail=True)
        with patch('mixin_stickers.logger.warning') as warning:
            self.assertTrue(self.send())
        warning.assert_called_once()
        self.port.call.assert_awaited_once()
        self.assert_picture()

    def test_no_bot_sends_picture_without_warning_or_call(self):
        with patch('mixin_stickers.logger.warning') as warning:
            self.assertTrue(self.send())
        warning.assert_not_called()
        self.port.call.assert_not_awaited()
        self.assert_picture()

    def test_cannot_speak_sends_nothing(self):
        self.event.bot = Bot()
        self.plugin._may_speak_in.return_value = False
        self.assertFalse(self.send())
        self.plugin._messenger.assert_not_called()
        self.assertEqual(self.event.bot.calls, [])
        self.plugin.context.send_message.assert_not_awaited()
        self.lib.use.assert_not_called()
        self.plugin._note_sent.assert_not_called()

