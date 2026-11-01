# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Sticker sending through neutral and AstrBot messengers, offline."""
import base64
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import events
import main
import stickers


PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+'
    'l0ZkAAAAASUVORK5CYII='
)


class StickerSendNeutral(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ['TEMP'])
        self.addCleanup(self.tmp.cleanup)
        self.lib = stickers.Library(self.tmp.name)
        self.lib.img.mkdir()
        (self.lib.img / 'one.png').write_bytes(PNG)
        self.lib.rows['one'] = {'file': 'one.png', 'uses': 0}
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin._sticker_lib = Mock(return_value=self.lib)
        self.plugin._may_speak_in = Mock(return_value=True)
        self.plugin._note_sent = Mock()
        self.plugin._read_window = Mock(return_value={'umo': 'test'})
        self.plugin.context = SimpleNamespace(send_message=AsyncMock())
        self.port = SimpleNamespace(call=AsyncMock(), send=AsyncMock())
        self.plugin._neutral_messenger = self.port
        self.event = SimpleNamespace()

    async def send(self, place):
        return await self.plugin._send_sticker(self.event, 'one', '', place)

    def assert_sticker(self, call, action, target, number):
        self.assertEqual(call.args, (action,))
        self.assertEqual(set(call.kwargs), {target, 'message'})
        self.assertEqual(call.kwargs[target], number)
        message = call.kwargs['message']
        self.assertEqual(len(message), 1)
        self.assertEqual(message[0]['type'], 'image')
        data = message[0]['data']
        self.assertEqual(data['file'], 'base64://' + base64.b64encode(PNG).decode('ascii'))
        self.assertEqual(data['sub_type'], 1)
        self.assertEqual(data['summary'], stickers.STICKER_SUMMARY)

    async def test_neutral_private_sends_sticker(self):
        self.assertTrue(await self.send('private:10001'))
        self.port.call.assert_awaited_once()
        self.assert_sticker(self.port.call.await_args, 'send_private_msg', 'user_id', 10001)
        self.port.send.assert_not_awaited()

    async def test_neutral_group_sends_sticker(self):
        self.assertTrue(await self.send('group:900001'))
        self.port.call.assert_awaited_once()
        self.assert_sticker(self.port.call.await_args, 'send_group_msg', 'group_id', 900001)
        self.port.send.assert_not_awaited()

    async def test_call_failure_sends_picture_and_records_use_once(self):
        self.port.call.side_effect = RuntimeError('failed')
        self.assertTrue(await self.send('private:10001'))
        self.port.call.assert_awaited_once()
        self.port.send.assert_awaited_once_with(
            'private:10001', (events.Segment('image', {'base64': base64.b64encode(PNG).decode('ascii')}),))
        self.assertEqual(self.lib.rows['one']['uses'], 1)

    async def test_astrbot_with_bot_sends_sticker(self):
        del self.plugin._neutral_messenger
        self.event.bot = SimpleNamespace(call_action=AsyncMock())
        self.assertTrue(await self.send('group:900001'))
        self.event.bot.call_action.assert_awaited_once()
        self.assert_sticker(self.event.bot.call_action.await_args, 'send_group_msg', 'group_id', 900001)
        self.plugin.context.send_message.assert_not_awaited()

    async def test_astrbot_without_bot_sends_picture(self):
        del self.plugin._neutral_messenger
        self.assertTrue(await self.send('private:10001'))
        self.plugin.context.send_message.assert_awaited_once()
        chain = self.plugin.context.send_message.await_args.args[1]
        self.assertEqual(len(chain.chain), 1)
        self.assertEqual(type(chain.chain[0]).__name__, 'Image')
        self.assertEqual(self.lib.rows['one']['uses'], 1)

    async def test_disallowed_place_sends_nothing(self):
        self.plugin._may_speak_in.return_value = False
        self.assertFalse(await self.send('private:10001'))
        self.port.call.assert_not_awaited()
        self.port.send.assert_not_awaited()
        self.assertEqual(self.lib.rows['one']['uses'], 0)


if __name__ == '__main__':
    unittest.main()
