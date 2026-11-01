# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for recent pictures from other people."""
import asyncio
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import events
import mixin_media
import turn


def event(sender='10001', name='Alice', ref='', sticker=False, message='20002'):
    segments = (events.Segment('image', {'file': ref, 'sub_type': '1' if sticker else '0'}),) if ref else ()
    return turn.TurnEvent(events.Incoming(
        place='group:900001', sender_id=sender, sender_name=name, self_id='10003',
        message_id=message, segments=segments, at_me=True, reply_to='', image_refs=(),
        is_private=False, is_self=False, ts=0))


class RecentImagesTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = mixin_media.MediaMixin()
        self.plugin._here = lambda e: e.incoming.place
        self.plugin._speaker = lambda e: (e.incoming.sender_id, e.incoming.sender_name)
        self.plugin._source_ids = lambda e: [e.incoming.message_id]
        self.plugin._job_stale = lambda: False
        self.plugin._may_keep = Mock(return_value=True)
        self.plugin._addresses_her = lambda e: e.incoming.at_me
        self.plugin._sticker_refs = lambda e: [s['file'] for s in mixin_media.stickers.stickers_in_segments(e.incoming.segments)]
        self.plugin._stickers_on = lambda: False
        self.plugin._llm_allowed = lambda _: True
        self.plugin._for_model = lambda name, e: name.replace('10001', 'someone')
        self.plugin._quoted_image_refs = self.no_quotes
        self.plugin._group_image_lock = lambda: self.lock
        self.plugin._group_state = lambda: {}
        self.plugin._load_image_cache = lambda: dict(self.cache)
        self.plugin._image_context_locked = self.look
        self.lock = asyncio.Lock()
        self.cache = {}
        self.calls = []
        self.clock = patch('mixin_media.time.time', return_value=1000)
        self.time = self.clock.start()
        self.addCleanup(self.clock.stop)

    async def no_quotes(self, event):
        return []

    async def look(self, event):
        self.calls.extend(event._ams_image_refs)
        for ref in event._ams_image_refs:
            self.cache[mixin_media._sha256(ref)] = {'caption': 'description ' + ref,
                'where': event.incoming.place, 'from_qq': event._ams_image_owners.get(ref, event.incoming.sender_id), 'ts': self.time.return_value}
        return 'description'

    async def test_other_sender_and_seen(self):
        self.plugin._remember_images(event(ref='one'))
        self.time.return_value = 1030
        reply = event('10005', 'Bob')
        self.assertEqual(await self.plugin._image_context(reply), 'Alice30秒前发的图：description one')
        self.assertEqual(self.cache[mixin_media._sha256('one')]['from_qq'], '10001')
        self.assertEqual(await self.plugin._image_context(reply), '')
        self.assertEqual(self.calls, ['one'])

    async def test_sticker_is_not_remembered(self):
        self.plugin._remember_images(event(ref='sticker', sticker=True))
        self.plugin._remember_images(event(ref='another-sticker', sticker=True))
        self.assertEqual(self.plugin._recent_images, {})
        self.assertEqual(await self.plugin._image_context(event('10005', 'Bob')), '')
        self.assertEqual(self.calls, [])

    async def test_existing_sender_cache_is_reused(self):
        self.plugin._remember_images(event(ref='one'))
        self.cache[mixin_media._sha256('one')] = {'caption': 'cached', 'where': 'group:900001',
                                                  'from_qq': '10001', 'ts': 1000}
        self.assertEqual(await self.plugin._image_context(event('10005', 'Bob')), 'Alice0秒前发的图：cached')
        self.assertEqual(self.calls, [])
        self.assertTrue(self.plugin._recent_images['group:900001'][0]['seen'])

    async def test_expiry_limit_and_sender_priority(self):
        self.plugin._remember_images(event(ref='old'))
        self.time.return_value = 1180
        self.plugin._remember_images(event(ref='first', message='one'))
        self.time.return_value = 1181
        self.plugin._remember_images(event('10005', 'Bob', 'own', message='two'))
        self.time.return_value = 1182
        self.plugin._remember_images(event(ref='latest', message='three'))
        result = await self.plugin._image_context(event('10005', 'Bob'))
        self.assertEqual(self.calls, ['own', 'latest'])
        self.assertEqual(result, 'Bob1秒前发的图：description own\nAlice0秒前发的图：description latest')

    async def test_keep_denied_for_person_or_place(self):
        for denied in ('person', 'place'):
            with self.subTest(denied=denied):
                self.plugin._may_keep.return_value = False
                self.plugin._remember_images(event(ref=denied))
                self.assertEqual(await self.plugin._image_context(event('10005', 'Bob')), '')
        self.assertEqual(self.plugin._recent_images, {})
        self.assertEqual(self.calls, [])

    async def test_recognition_disabled(self):
        self.plugin._remember_images(event(ref='one'))
        self.plugin.image_recognition_enabled = False
        self.assertEqual(await self.plugin._image_context(event('10005', 'Bob')), '')
        self.assertEqual(self.calls, [])

    async def test_name_for_model_and_forget(self):
        self.plugin._remember_images(event(name='10001', ref='one'))
        self.assertIn('someone0秒前发的图', await self.plugin._image_context(event('10005', 'Bob')))
        self.plugin._forget_recent_images(person='10001')
        self.assertEqual(self.plugin._recent_images, {})
