# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for the note when an image was not seen."""
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_onebot
import attention
import events
import harness
import main
import stickers
import turn
from astrbot.api.message_components import Image, Plain, Reply


def neutral(parts, quoted=None):
    frame = {'post_type': 'message', 'message_type': 'private', 'self_id': '20002',
             'user_id': '10001', 'message_id': '10003', 'message': parts}
    return turn.TurnEvent(adapter_onebot.from_onebot(frame, quoted=quoted))


def astrbot(parts, raw=None):
    event = harness.FakeEvent('hello', sender='10001', name='Example')
    event.get_messages = lambda: parts
    if raw is not None:
        event.message_obj.raw_message = {'message': raw}
    return event


class UnseenImageTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        test_basics.PLUGINS.append(self.plugin)

    async def prompt(self, event, image='', self_decide=False):
        self.plugin.self_decide = self_decide
        self.plugin._image_context = AsyncMock(return_value=image)
        request = turn.TurnRequest(prompt='hello')
        await self.plugin._prepare_turn(event, request)
        return '\n'.join(part.get('text', '') for part in request.extra_user_content_parts)

    async def test_neutral_unseen_image_even_when_recognition_disabled(self):
        self.plugin.image_recognition_enabled = False
        event = neutral([{'type': 'image', 'data': {'file': 'picture.png'}}])
        prompt = await self.prompt(event, '[BioCore Image]  ', self_decide=True)
        self.assertIn('[图] ' + attention.UNSEEN_IMAGE_NOTE, prompt)
        self.assertLess(prompt.index('[图]'), prompt.index('[她可以]'))

    async def test_astrbot_unseen_image_with_self_decide_off(self):
        prompt = await self.prompt(astrbot([Image(file='picture.png'), Plain('hello')]))
        self.assertIn(attention.UNSEEN_IMAGE_NOTE, prompt)
        self.assertNotIn('[她可以]', prompt)

    async def test_seen_image_has_caption_and_no_note(self):
        event = neutral([{'type': 'image', 'data': {'file': 'picture.png'}}])
        prompt = await self.prompt(event, '[BioCore Image] 图里是一只猫')
        self.assertIn('猫', prompt)
        self.assertNotIn(attention.UNSEEN_IMAGE_NOTE, prompt)

    async def test_no_image_has_no_note(self):
        prompt = await self.prompt(astrbot([Plain('hello')]))
        self.assertNotIn(attention.UNSEEN_IMAGE_NOTE, prompt)

    async def test_quoted_image_has_note(self):
        event = neutral([{'type': 'reply', 'data': {'id': '10003'}}],
                        quoted={'message': [{'type': 'image', 'data': {'file': 'picture.png'}}]})
        self.assertIn(attention.UNSEEN_IMAGE_NOTE, await self.prompt(event))
        event = astrbot([Reply(chain=[Image(file='picture.png')])])
        self.assertIn(attention.UNSEEN_IMAGE_NOTE, await self.prompt(event))

    async def test_neutral_sticker_has_no_note(self):
        for data in ({'file': 'sticker.png', 'sub_type': 1},
                     {'file': 'sticker.png', 'summary': stickers.STICKER_SUMMARY}):
            with self.subTest(data=data):
                event = neutral([{'type': 'image', 'data': data}])
                self.assertNotIn(attention.UNSEEN_IMAGE_NOTE, await self.prompt(event))

    async def test_astrbot_sticker_has_no_note(self):
        data = {'file': 'sticker.png', 'url': 'sticker-ref', 'sub_type': 1}
        event = astrbot([Image(file=data['file'], url=data['url'])],
                        [{'type': 'image', 'data': data}])
        self.assertNotIn(attention.UNSEEN_IMAGE_NOTE, await self.prompt(event))

    async def test_quoted_sticker_and_mixed_images(self):
        sticker = {'type': 'image', 'data': {'file': 'sticker.png', 'sub_type': 1}}
        quote = {'message': [sticker]}
        event = neutral([{'type': 'reply', 'data': {'id': '10003'}}], quoted=quote)
        self.assertNotIn(attention.UNSEEN_IMAGE_NOTE, await self.prompt(event))
        event = neutral([{'type': 'reply', 'data': {'id': '10003'}},
                         {'type': 'image', 'data': {'file': 'picture.png'}}], quoted=quote)
        self.assertIn(attention.UNSEEN_IMAGE_NOTE, await self.prompt(event))


if __name__ == '__main__':
    unittest.main()
