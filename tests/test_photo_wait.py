# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Photo preparation holds the reply on both turn routes."""
import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot_turn
import harness
import main
import mixin_selfie
import test_turn_runner
import turn_runner
from astrbot.api.provider import LLMResponse


class PhotoWait(unittest.IsolatedAsyncioTestCase):
    setUp = test_turn_runner.OneTurn.setUp
    close_cached_stores = test_turn_runner.OneTurn.close_cached_stores
    event = test_turn_runner.OneTurn.event

    def prepare(self, outcome='path', delay=0.002):
        self.order = []
        self.her.config['photo_enabled'] = True
        self.her._phone_clear = AsyncMock(return_value=True)
        self.her._phone_account = Mock()
        self.her._phone_prune = Mock()
        self.her._note_she_sent = Mock()
        async def photo(kind, what):
            self.order.append('start')
            await asyncio.sleep(delay)
            self.order.append('ready')
            if outcome == 'error':
                raise ValueError('fake failure')
            return Path('photo.png') if outcome == 'path' else None
        self.her._make_photo = AsyncMock(side_effect=photo)
        async def send(place, segments):
            self.order.append('photo' if any(s.type == 'image' for s in segments) else 'text')
        self.her._neutral_messenger.send = AsyncMock(side_effect=send)

    async def run_photo(self, reply='hello'):
        self.fake.call_tools(('take_photo', {'kind': 'snap', 'what': 'sky', 'where': 'home',
                                             'doing': 'looking', 'caption': 'look'}))
        self.fake.say(reply)
        with patch.object(mixin_selfie, 'SEND_DELAY', 0), patch.object(mixin_selfie, 'PHOTO_WAIT_SECONDS', 0.1):
            await turn_runner.run_turn(self.her, self.event())
            await asyncio.sleep(0.03)

    async def test_new_turn_waits_then_sends_photo_once(self):
        self.prepare()
        await self.run_photo()
        self.assertEqual(self.order, ['start', 'ready', 'text', 'photo'])
        self.her._make_photo.assert_awaited_once()

    async def test_timeout_never_sends_late_photo(self):
        self.prepare(delay=0.25)
        await self.run_photo()
        await asyncio.sleep(0.27)
        self.assertEqual(self.order, ['start', 'text'])
        self.her._make_photo.assert_awaited_once()

    async def test_none_and_error_send_only_text(self):
        for outcome in ('none', 'error'):
            with self.subTest(outcome=outcome):
                self.prepare(outcome)
                await self.run_photo()
                self.assertEqual(self.order, ['start', 'ready', 'text'])

    async def test_silent_and_held_replies_do_not_start_photo(self):
        self.prepare()
        await self.run_photo('【不说】')
        self.her._make_photo.assert_not_awaited()
        self.her.global_memory = True
        self.her._look_at_reply = AsyncMock(return_value='')
        await self.run_photo()
        self.her._make_photo.assert_not_awaited()

    async def test_astrbot_waits_before_first_text(self):
        self.prepare()
        event = harness.FakeEvent('hello', sender='10001', name='Alice', group='900001')
        self.her._phone_queue(event)['photo'] = ('snap', 'sky', 'look')
        reply = adapter_astrbot_turn.reply_handle(LLMResponse('hello'))
        with patch.object(mixin_selfie, 'SEND_DELAY', 0), patch.object(mixin_selfie, 'PHOTO_WAIT_SECONDS', 0.1):
            await self.her._after_reply(event, reply)
            self.order.append('text')
            await asyncio.sleep(0.03)
        self.assertEqual(self.order, ['start', 'ready', 'text', 'photo'])
        self.her._make_photo.assert_awaited_once()

    async def test_voice_only_does_not_wait_for_photo(self):
        self.prepare()
        self.her.config['say_aloud_enabled'] = True
        self.her._make_voice = AsyncMock(return_value=Path('voice.wav'))
        self.fake.call_tools(('say_aloud', {'text': 'hello'}))
        self.fake.say('hello')
        with patch.object(mixin_selfie, 'SEND_DELAY', 0):
            await turn_runner.run_turn(self.her, self.event())
            await asyncio.sleep(0.01)
        self.assertEqual(self.order[0], 'text')
        self.her._make_photo.assert_not_awaited()
