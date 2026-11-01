# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Persistent sticker embeddings and the offline worker."""
import asyncio
import base64
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import main
import mixin_stickers
import stickers

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+l0ZkAAAAASUVORK5CYII=')


class StickerVectors(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ['TEMP'])
        self.addCleanup(self.tmp.cleanup)
        self.lib = stickers.Library(self.tmp.name)

    def add(self, suffix=b'', **kwargs):
        sid, why = self.lib.add(PNG + suffix, 1, look={'caption': 'cat'}, **kwargs)
        self.assertFalse(why)
        return sid

    def test_semantic_text(self):
        row = dict(meaning='meaning', tags=['one', 'two'], text='words', emotion='happy',
                   scene='home', reply_to='yes', caption='cat')
        self.assertEqual(stickers.semantic_text(row), 'meaning one two words happy home yes cat')
        self.assertEqual(stickers.semantic_text({'tags': [], 'text': '', 'caption': 'cat'}), 'cat')
        self.assertEqual(len(stickers.semantic_text({'meaning': 'x' * 400})), 300)

    def test_persistence_and_invalidation(self):
        sid = self.add()
        self.lib.set_vector(sid, 'model', [0.123456, 1])
        lib = stickers.Library(self.tmp.name)
        self.assertEqual(lib.vector_of(sid, 'model'), [0.12346, 1.0])
        self.assertIsNone(lib.vector_of(sid, 'other'))
        self.assertIn(sid, lib.missing_vectors('other'))
        lib.rows[sid]['meaning'] = 'changed'
        self.assertIsNone(lib.vector_of(sid, 'model'))
        self.assertIn(sid, lib.missing_vectors('model'))

    def test_deletions_remove_vectors(self):
        a = self.add(b'a')
        b = self.add(b'b', from_qq='10001')
        c = self.add(b'c')
        for sid in (a, b, c):
            self.lib.set_vector(sid, 'model', [1])
        self.lib.remove(a)
        self.lib.forget_person('10001')
        self.lib.sweep(10000000)
        self.assertEqual(json.loads(self.lib.vectors_path.read_text('utf-8')), {})


class StickerVectorWorker(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ['TEMP'])
        self.addCleanup(self.tmp.cleanup)
        self.lib = stickers.Library(self.tmp.name)
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.enabled = self.plugin.stickers_enabled = True
        self.plugin._sticker_lib = lambda: self.lib
        self.plugin._embedding_runtime_config = lambda: {'model': 'model'}
        self.plugin._embed_text = AsyncMock(return_value=[1.0, 0.0])
        self.plugin._here = lambda event: 'group:900001'
        self.plugin._speaker = lambda event: ('10001', '')
        self.plugin._job_stale = lambda: False

    def add(self, suffix, caption):
        return self.lib.add(PNG + suffix, 1, source='old', look={'caption': caption})[0]

    async def test_offer_uses_only_saved_vectors(self):
        a, b = self.add(b'a', 'a'), self.add(b'b', 'b')
        self.lib.set_vector(a, 'model', [0, 1])
        self.lib.set_vector(b, 'model', [1, 0])
        event = SimpleNamespace()
        await self.plugin._sticker_offer(event, SimpleNamespace(v=0), [1, 0])
        self.assertEqual(event._ams_stickers_offered[0], b)
        self.plugin._embed_text.assert_not_awaited()

    async def test_maybe_keep_schedules_vector_and_failure_keeps_picture(self):
        for suffix, fail in ((b'a', False), (b'b', True)):
            data = PNG + suffix
            look = {'keep': True, 'kind': 'sticker', 'personal': False, 'group_meme': False,
                    'caption': 'cat', '_picture': data, '_picture_sha256': hashlib.sha256(data).hexdigest()}
            self.plugin._embed_text = AsyncMock(side_effect=RuntimeError('offline') if fail else None,
                                                return_value=[1, 0])
            sid = await self.plugin._maybe_keep(SimpleNamespace(), '', look)
            self.assertIn(sid, self.lib.rows)
            task = self.plugin._sticker_vector_task
            await asyncio.sleep(0)
            self.plugin._embed_text.assert_awaited()
            self.assertEqual(self.lib.vector_of(sid, 'model'), None if fail else [1.0, 0.0])
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task

    async def test_worker_fills_three_and_retries_failure(self):
        ids = [self.add(bytes([i]), str(i)) for i in range(3)]
        sleeps = []
        async def sleep(seconds):
            sleeps.append(seconds)
        self.plugin._embed_text.side_effect = [RuntimeError('offline'), [1], [1], [1]]
        with patch.object(mixin_stickers.asyncio, 'sleep', side_effect=sleep):
            await mixin_stickers._fill_vectors(self.plugin)
        self.assertEqual(sleeps, [300, 2, 2, 2])
        self.assertTrue(all(self.lib.vector_of(sid, 'model') == [1.0] for sid in ids))

    async def test_worker_skips_empty_text(self):
        empty = self.add(b'a', '')
        first = self.add(b'b', 'first')
        second = self.add(b'c', 'second')
        self.assertEqual(self.lib.missing_vectors('model'), [first, second])
        with patch.object(mixin_stickers.asyncio, 'sleep', new=AsyncMock()):
            await mixin_stickers._fill_vectors(self.plugin)
        self.assertIsNone(self.lib.vector_of(empty, 'model'))
        self.assertEqual(self.lib.vector_of(first, 'model'), [1.0, 0.0])
        self.assertEqual(self.lib.vector_of(second, 'model'), [1.0, 0.0])
        self.assertEqual([call.args[0] for call in self.plugin._embed_text.await_args_list], ['first', 'second'])

    async def test_worker_advances_after_empty_and_failed_embeddings(self):
        ids = [self.add(bytes([i]), str(i)) for i in range(3)]
        self.plugin._embed_text.side_effect = [None, RuntimeError('offline'), [1], [1], [1]]
        sleep = AsyncMock()
        with patch.object(mixin_stickers.asyncio, 'sleep', new=sleep):
            await mixin_stickers._fill_vectors(self.plugin)
        self.assertEqual([call.args[0] for call in self.plugin._embed_text.await_args_list],
                         ['0', '1', '2', '0', '1'])
        self.assertEqual([call.args[0] for call in sleep.await_args_list], [300, 300, 2, 2, 2])
        self.assertTrue(all(self.lib.vector_of(sid, 'model') == [1.0] for sid in ids))
