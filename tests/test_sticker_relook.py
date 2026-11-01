# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for looking again at older stickers."""
import asyncio
import base64
import hashlib
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import main
import mixin_attention
import mixin_stickers
import stickers
import vision

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+l0ZkAAAAASUVORK5CYII=')
LOOK = {'caption': 'cat', 'meaning': 'agree', 'kind': 'sticker', 'personal': False,
        'group_meme': False, 'keep': True, 'tags': ['yes']}


class StickerRelook(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ['TEMP'])
        self.addCleanup(self.tmp.cleanup)
        self.lib = stickers.Library(self.tmp.name)
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.enabled = self.plugin.stickers_enabled = True
        self.plugin._sticker_lib = lambda: self.lib
        self.plugin._llm_allowed = lambda name: True
        self.plugin._embedding_runtime_config = lambda: {'model': 'model'}
        self.plugin._embed_text = AsyncMock(return_value=[1.0])
        self.plugin._job_stale = lambda: False
        self.cache = {}
        self.plugin._load_image_cache = lambda: dict(self.cache)
        self.plugin._save_image_cache = lambda cache: setattr(self, 'cache', dict(cache))
        self.provider = SimpleNamespace(text_chat=AsyncMock(return_value=SimpleNamespace(completion_text=json.dumps(LOOK))))
        self.plugin._vision_provider_for = self.gate
        self.patches = [patch.object(mixin_stickers, 'STICKERS_DIR', Path(self.tmp.name)),
                        patch.object(vision, 'DATA_DIR', Path(self.tmp.name)),
                        patch.object(mixin_attention, 'SPEND_PATH', Path(self.tmp.name) / 'spend.json')]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def gate(self, event, source, fresh=False):
        self.assertIsNone(event)
        self.assertEqual(source, 'owner_add')
        self.assertTrue(fresh)
        return vision.VisionGate(self.plugin, self.provider, event, source, fresh=fresh)

    def add(self, suffix, source='old'):
        return self.lib.add(PNG + suffix, 1, source=source, from_qq='10001',
                            look={'caption': 'old'})[0]

    async def run_worker(self):
        with patch.object(mixin_stickers.asyncio, 'sleep', new=AsyncMock()) as sleep:
            await mixin_stickers._relook_stickers(self.plugin)
            task = getattr(self.plugin, '_sticker_vector_task', None)
            if task:
                await task
            return sleep

    async def test_three_old_stickers_get_looks_and_vectors(self):
        ids = [self.add(bytes([i])) for i in range(3)]
        before = {sid: dict(self.lib.rows[sid]) for sid in ids}
        await self.run_worker()
        for sid in ids:
            row = self.lib.rows[sid]
            self.assertEqual((row['meaning'], row['look_version'], self.lib.vector_of(sid, 'model')),
                             ('agree', 2, [1.0]))
            for key in ('saved_at', 'last_used', 'uses', 'source', 'from_qq', 'from_where'):
                self.assertEqual(row[key], before[sid][key])
        self.assertEqual(self.provider.text_chat.await_count, 3)

    async def test_owner_is_skipped_and_old_precedes_self(self):
        owner = self.add(b'o', 'owner')
        own = self.add(b's', 'self')
        old = self.add(b'a')
        await self.run_worker()
        self.assertNotIn('look_version', self.lib.rows[owner])
        self.assertEqual(self.provider.text_chat.await_count, 2)
        calls = self.provider.text_chat.await_args_list
        self.assertEqual(base64.b64decode(calls[0].kwargs['image_urls'][0].split(',', 1)[1]), PNG + b'a')
        self.assertEqual(base64.b64decode(calls[1].kwargs['image_urls'][0].split(',', 1)[1]), PNG + b's')

    async def test_keep_false_and_personal_are_preserved_but_not_offered(self):
        sid = self.add(b'p')
        look = dict(LOOK, keep=False, personal=True, group_meme=True)
        self.provider.text_chat.return_value.completion_text = json.dumps(look)
        await self.run_worker()
        row = stickers.Library(self.tmp.name).rows[sid]
        self.assertTrue(row['personal'])
        self.assertTrue(row['group_meme'])
        self.assertEqual(row['look_version'], 2)
        self.assertNotIn(sid, stickers.pick_candidates({sid: row}, time.time()))

    async def test_gate_waits_for_vision_lock_without_deadlock(self):
        self.add(b'l')
        self.plugin._vision_lock = asyncio.Lock()
        await self.plugin._vision_lock.acquire()
        task = asyncio.create_task(self.run_worker())
        try:
            await asyncio.sleep(0.1)
            self.provider.text_chat.assert_not_awaited()
            self.plugin._vision_lock.release()
            await asyncio.wait_for(task, 5)
            self.provider.text_chat.assert_awaited_once()
        finally:
            if self.plugin._vision_lock.locked():
                self.plugin._vision_lock.release()
            if not task.done():
                task.cancel()

    async def test_three_consecutive_failures_stop_and_skip_failed(self):
        ids = [self.add(bytes([i])) for i in range(4)]
        good = SimpleNamespace(completion_text=json.dumps(LOOK))
        self.provider.text_chat.side_effect = [RuntimeError(), good, RuntimeError(), RuntimeError(), RuntimeError()]
        with patch.object(mixin_stickers.logger, 'warning') as warning:
            sleep = await self.run_worker()
        self.assertEqual(self.lib.rows[ids[1]]['look_version'], 2)
        self.assertNotIn('look_version', self.lib.rows[ids[0]])
        self.assertTrue(self.plugin._sticker_relook_stopped)
        self.assertEqual(warning.call_count, 1)
        self.assertEqual([c.args[0] for c in sleep.await_args_list].count(300), 3)
        mixin_stickers._start_relook_worker(self.plugin)
        self.assertFalse(hasattr(self.plugin, '_sticker_relook_task'))

    async def test_disabled_does_not_look(self):
        self.add(b'd')
        self.plugin.stickers_enabled = False
        await self.run_worker()
        self.provider.text_chat.assert_not_awaited()

    async def test_fresh_bypasses_cached_caption(self):
        sid = self.add(b'c')
        digest = hashlib.sha256(self.lib.path_of(sid).read_bytes()).hexdigest()
        scope = hashlib.sha256(b'owner').hexdigest()
        self.cache['content:' + scope + ':' + digest] = {'caption': 'cached', 'ts': time.time()}
        await self.run_worker()
        self.provider.text_chat.assert_awaited_once()
        self.assertEqual(self.lib.rows[sid]['meaning'], 'agree')
        self.assertEqual(self.lib.rows[sid]['look_version'], 2)

    async def test_missing_meaning_or_caption_does_not_change_row(self):
        for suffix, answer in ((b'm', {'caption': 'cat'}), (b'e', {'caption': '', 'meaning': 'yes'})):
            sid = self.add(suffix)
            before = dict(self.lib.rows[sid])
            self.provider.text_chat.return_value.completion_text = json.dumps(answer)
            with patch.object(mixin_stickers.logger, 'warning'), patch.object(mixin_stickers.asyncio, 'sleep', new=AsyncMock()) as sleep:
                await mixin_stickers._relook_stickers(self.plugin)
            self.assertEqual(self.lib.rows[sid], before)
            self.assertTrue(any(c.args[0] == 300 for c in sleep.await_args_list))
            self.lib.remove(sid)
