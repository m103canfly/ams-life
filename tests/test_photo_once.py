# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Photo reservations, captions and outcome logs."""
import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import harness
import mixin_selfie
import test_turn_runner


class PhotoOnce(unittest.IsolatedAsyncioTestCase):
    setUp = test_turn_runner.OneTurn.setUp
    close_cached_stores = test_turn_runner.OneTurn.close_cached_stores
    event = test_turn_runner.OneTurn.event

    def ready(self):
        self.her.config['photo_enabled'] = True
        self.her._phone_clear = AsyncMock(return_value=True)
        self.her._phone_account = Mock()
        self.her._phone_prune = Mock()
        self.her._note_she_sent = Mock()
        self.her._neutral_messenger.send = AsyncMock()

    async def queue(self, event, caption='look'):
        return await self.her._tool_take_photo(event, 'snap', 'sky', 'home', 'looking', caption)

    async def test_concurrent_same_place_and_retry_after_completion(self):
        self.ready()
        first, second = self.event(), self.event()
        gate = asyncio.Event()
        async def photo(*args):
            await gate.wait()
            return Path('photo.png')
        self.her._make_photo = AsyncMock(side_effect=photo)
        self.assertEqual(await self.queue(first), mixin_selfie.PHOTO_QUEUED)
        task = asyncio.create_task(mixin_selfie._prepare_photo(self.her, first, first._ams_phone_queue))
        await asyncio.sleep(0)
        self.assertEqual(await self.queue(second), '刚才那张还在拍，拍好了会一起发；这次别再拍。')
        gate.set()
        await task
        with patch.object(mixin_selfie, 'SEND_DELAY', 0):
            await self.her._media_after_reply(first, first._ams_phone_queue)
        self.her._make_photo.assert_awaited_once()
        self.her._neutral_messenger.send.assert_awaited_once()
        self.assertEqual(await self.queue(self.event()), mixin_selfie.PHOTO_QUEUED)

    async def test_different_places_and_expired_reservation(self):
        self.ready()
        private = harness.FakeEvent('hello', sender='10001', name='Alice')
        group = harness.FakeEvent('hello', sender='10001', name='Alice', group='900001')
        with patch.object(mixin_selfie.time, 'monotonic', side_effect=[1, 2, 1000]):
            self.assertEqual(await self.queue(private), mixin_selfie.PHOTO_QUEUED)
            self.assertEqual(await self.queue(group), mixin_selfie.PHOTO_QUEUED)
            self.assertEqual(await self.queue(harness.FakeEvent('hello', sender='10001', name='Alice')), mixin_selfie.PHOTO_QUEUED)
        mixin_selfie._photo_release(self.her, private._ams_phone_queue)
        self.assertEqual(len(self.her._photo_pending), 2)

    async def test_caption_matches_sent_text_or_differs(self):
        self.ready()
        for caption, expected in [('hello, world!', ['image']), ('other', ['text', 'image'])]:
            event = self.event()
            self.her._check_note(event)['sent'] = 'Well, hello world.'
            with patch.object(mixin_selfie, 'SEND_DELAY', 0):
                await self.her._media_after_reply(event, {'photo': ('snap', 'sky', caption), 'photo_path': Path('photo.png')})
            segments = self.her._neutral_messenger.send.await_args.args[1]
            self.assertEqual([segment.type for segment in segments], expected)

    async def test_outcomes_and_retry_after_timeout(self):
        self.ready()
        for outcome in ('sent', 'timeout', 'failed', 'held', 'stopped'):
            with self.subTest(outcome=outcome):
                event = self.event()
                self.her._phone_clear.return_value = outcome != 'held'
                async def photo(*args):
                    if outcome == 'timeout':
                        await asyncio.sleep(1)
                    if outcome == 'failed':
                        raise ValueError('private caption')
                    return Path('photo.png')
                self.her._make_photo = AsyncMock(side_effect=photo)
                self.assertEqual(await self.queue(event, 'private caption'), mixin_selfie.PHOTO_QUEUED)
                with patch.object(mixin_selfie, 'SEND_DELAY', 0), patch.object(mixin_selfie, 'PHOTO_WAIT_SECONDS', 0.01), patch.object(mixin_selfie.logger, 'info') as log:
                    await mixin_selfie._prepare_photo(self.her, event, event._ams_phone_queue)
                    if outcome == 'stopped':
                        event.is_stopped = lambda: True
                    await self.her._media_after_reply(event, event._ams_phone_queue)
                lines = [call.args[0] % call.args[1:] for call in log.call_args_list]
                expected = '[ams-life] phone photo sent' if outcome == 'sent' else '[ams-life] phone photo not sent (%s)' % outcome
                self.assertEqual(lines.count(expected), 1)
                self.assertTrue(all('private caption' not in line for line in lines))
                self.assertEqual(await self.queue(self.event()), mixin_selfie.PHOTO_QUEUED)
                self.her._photo_pending.clear()
