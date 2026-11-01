# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline coverage for shared image request serialization."""
import asyncio
import sys
import tempfile
import types
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import test_selfie  # noqa: E402
import test_vision_channel  # noqa: E402
import vision  # noqa: E402


class Response:
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return b'{"choices":[{"message":{"content":"seen"}}]}'


class BridgeLockTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.plugin = test_selfie.Phone()
        self.plugin.config['vision_image_api_model'] = 'model'
        self.plugin._phone_path = lambda *args: Path(self.tmp.name) / 'photo.png'
        self.plugin._phone_account = lambda *args: None
        self.plugin._phone_price = lambda *args: 0
        self.api = vision.ImageAPI(self.plugin)

    async def test_photo_finishes_before_vision_request(self):
        started, finish = asyncio.Event(), asyncio.Event()
        order = []
        async def photo(*args, **kwargs):
            order.append('photo start')
            started.set()
            await finish.wait()
            order.append('photo end')
            return b'{"data":[{"b64_json":"cG5n"}]}', 'application/json'
        self.plugin._post_json = photo
        def open_request(*args, **kwargs):
            order.append('vision')
            return Response()
        with patch('urllib.request.urlopen', side_effect=open_request):
            photo_task = asyncio.create_task(self.plugin._make_photo('snap', 'sky'))
            await started.wait()
            vision_task = asyncio.create_task(self.api.text_chat())
            await asyncio.sleep(0)
            self.assertEqual(order, ['photo start'])
            finish.set()
            self.assertIsNotNone(await photo_task)
            self.assertEqual((await vision_task).completion_text, 'seen')
        self.assertEqual(order, ['photo start', 'photo end', 'vision'])

    async def test_vision_gives_up_after_150_seconds(self):
        lock = vision.bridge_lock(self.plugin)
        await lock.acquire()
        async def timeout(awaitable, timeout):
            self.assertEqual(timeout, 150)
            awaitable.close()
            raise asyncio.TimeoutError
        with patch.object(vision.asyncio, 'wait_for', side_effect=timeout), \
                patch.object(vision.logger, 'warning') as warning, \
                patch('urllib.request.urlopen') as request:
            with self.assertRaisesRegex(RuntimeError, 'vision request failed'):
                await self.api.text_chat()
        self.assertIn('waiting for bridge', warning.call_args.args[0])
        request.assert_not_called()
        lock.release()

    async def test_vision_429_retries_and_releases_lock_during_sleep(self):
        error = urllib.error.HTTPError('https://image.invalid/', 429, 'busy', {}, None)
        busy = [5, 10, 20, 40, 60]
        for failures in (1, len(busy) + 1):
            got = []
            async def sleep(delay):
                got.append(delay)
                self.assertFalse(vision.bridge_lock(self.plugin).locked())
            with self.subTest(failures=failures), \
                    patch('urllib.request.urlopen', side_effect=[error] * failures + [Response()]) as request, \
                    patch.object(vision.asyncio, 'sleep', new=AsyncMock(side_effect=sleep)):
                if failures == 1:
                    self.assertEqual((await self.api.text_chat()).completion_text, 'seen')
                else:
                    with self.assertRaises(RuntimeError):
                        await self.api.text_chat()
                self.assertEqual(request.call_count, min(failures + 1, len(busy) + 1))
                self.assertEqual(got, busy[:min(failures, len(busy))])

    async def test_cancelled_photo_keeps_lock_until_request_finishes(self):
        started, finish = asyncio.Event(), asyncio.Event()
        async def photo(*args, **kwargs):
            started.set()
            await finish.wait()
            return b'', 'application/json'
        self.plugin._post_json = photo
        task = asyncio.create_task(self.plugin._make_photo('snap', 'sky'))
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(vision.bridge_lock(self.plugin).locked())
        finish.set()
        await asyncio.sleep(0)
        self.assertFalse(vision.bridge_lock(self.plugin).locked())

    async def test_vision_gate_still_serializes_vision_calls(self):
        plugin = test_vision_channel.Plugin()
        started, finish = asyncio.Event(), asyncio.Event()
        order = []
        class Provider:
            async def text_chat(self, **kwargs):
                order.append('start')
                started.set()
                await finish.wait()
                order.append('end')
                return types.SimpleNamespace(completion_text='seen')
        gate = vision.VisionGate(plugin, Provider(), object(), fresh=True)
        with patch.object(vision.mixin_attention, 'SPEND_PATH', Path(self.tmp.name) / 'spend.json'):
            first = asyncio.create_task(gate.text_chat())
            await started.wait()
            second = asyncio.create_task(gate.text_chat())
            await asyncio.sleep(0)
            self.assertEqual(order, ['start'])
            finish.set()
            await asyncio.gather(first, second)
        self.assertEqual(order, ['start', 'end', 'start', 'end'])
