# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Event-backed Messenger and phone media, offline."""
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test_selfie  # noqa: E402
import events  # noqa: E402
import messenger  # noqa: E402
from adapter_astrbot_messenger import AstrBotMessenger  # noqa: E402
from mixin_ports import PortsMixin  # noqa: E402


def shape(chain):
    return [(type(c).__name__, getattr(c, 'text', None), getattr(c, 'file', None)) for c in chain.chain]


class EventMessengerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.context = Mock()
        self.context.send_message = AsyncMock(return_value=True)
        self.send = AsyncMock()
        self.umo = Mock(return_value='default:GroupMessage:900002')
        self.port = AstrBotMessenger(self.context, self.umo, lambda: None,
                                    event_send=self.send, event_place='group:900001')
        self.segments = (events.Segment('text', {'text': 'hello'}),
                         events.Segment('image', {'path': 'photo.png'}))

    async def test_event_place_uses_event_send(self):
        result = await self.port.send('group:900001', self.segments)
        self.assertEqual(result, messenger.Sent(True, ''))
        self.assertEqual(shape(self.send.await_args.args[0]),
                         [('Plain', 'hello', None), ('Image', None, 'photo.png')])
        self.umo.assert_not_called()
        self.context.send_message.assert_not_awaited()

    async def test_other_place_uses_context(self):
        self.assertEqual(await self.port.send('group:900002', self.segments), messenger.Sent(True, ''))
        self.send.assert_not_awaited()
        self.assertEqual(self.context.send_message.await_args.args[0], 'default:GroupMessage:900002')
        self.assertEqual(shape(self.context.send_message.await_args.args[1]),
                         [('Plain', 'hello', None), ('Image', None, 'photo.png')])

    async def test_empty_event_place_uses_event_send(self):
        self.port.event_place = ''
        self.assertEqual(await self.port.send('', self.segments), messenger.Sent(True, ''))
        self.send.assert_awaited_once()
        self.umo.assert_not_called()
        self.context.send_message.assert_not_awaited()

    async def test_empty_destination_does_not_match_event_place(self):
        await self.port.send('', self.segments)
        self.send.assert_not_awaited()
        self.umo.assert_called_once_with('')
        self.context.send_message.assert_awaited_once()

    async def test_event_error_propagates(self):
        error = OSError('send failed')
        self.send.side_effect = error
        with self.assertRaises(OSError) as caught:
            await self.port.send('group:900001', self.segments)
        self.assertIs(caught.exception, error)

    async def test_ports_event_is_opt_in(self):
        plugin = PortsMixin()
        plugin.context = self.context
        event = test_selfie.Event()
        event.send = AsyncMock()
        place = 'private:10005'
        await plugin._messenger(event, as_event=True).send(place, self.segments)
        event.send.assert_awaited_once()
        await plugin._messenger(event).send(place, self.segments)
        event.send.assert_awaited_once()
        self.context.send_message.assert_awaited_once()


class MediaPortTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.plugin = test_selfie.Phone()
        self.plugin.browser_enabled = True
        self.event = test_selfie.Event()
        self.plugin._make_photo = AsyncMock(return_value=Path('photo.png'))
        self.plugin._make_voice = AsyncMock(return_value=Path('voice.wav'))
        self.plugin._phone_account = Mock()
        self.plugin._phone_prune = Mock()

    async def send_media(self, queue, shot=None):
        self.event.sent.clear()
        with patch('mixin_selfie.asyncio.sleep', new_callable=AsyncMock), \
                patch('mixin_selfie._browser_screenshot', new_callable=AsyncMock, return_value=shot) as capture:
            await self.plugin._media_after_reply(self.event, queue)
        if shot:
            capture.assert_awaited_once()
        self.assertEqual(len(self.event.sent), 1)
        return shape(self.event.sent[0])

    async def test_photo_captions_remain_plain(self):
        for caption, expected in [('hello [表情:微笑]', [('Plain', 'hello [表情:微笑]', None)]),
                                  ('', []), ('  ', [])]:
            with self.subTest(caption=caption):
                actual = await self.send_media({'photo': ('snap', 'scene', caption)})
                self.assertEqual(actual, expected + [('Image', None, 'photo.png')])

    async def test_voice_component(self):
        self.assertEqual(await self.send_media({'voice': 'hello'}), [('Record', None, 'voice.wav')])

    async def test_screenshot_with_image(self):
        queue = {'screenshot': ('https://example.invalid/page', 'title', 'caption')}
        self.assertEqual(await self.send_media(queue, (Path('shot.jpg'), 'description')),
                         [('Plain', 'caption', None), ('Image', None, 'shot.jpg')])
        queue['screenshot'] = ('https://example.invalid/page', 'title', '  ')
        self.assertEqual(await self.send_media(queue, (Path('shot.jpg'), 'description')),
                         [('Image', None, 'shot.jpg')])

    async def test_screenshot_without_image(self):
        queue = {'screenshot': ('https://example.invalid/page', 'title', 'caption')}
        self.assertEqual(await self.send_media(queue),
                         [('Plain', 'title\nhttps://example.invalid/page\ncaption', None)])
