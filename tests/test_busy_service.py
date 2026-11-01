# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for waiting when the local image service is busy (429)."""
import base64
import json
import shutil
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import test_selfie  # noqa: E402

import adapter_onebot  # noqa: E402
import attention  # noqa: E402
import harness  # noqa: E402
import main  # noqa: E402
import mixin_selfie as phone  # noqa: E402
import turn  # noqa: E402
import vision  # noqa: E402

PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==')
IMAGE_URL = 'data:image/png;base64,' + base64.b64encode(PNG).decode('ascii')


def busy():
    return urllib.error.HTTPError('https://image.invalid/v1/chat/completions', 429, 'busy', {}, None)


def always_busy(*args, **kwargs):
    raise busy()


def an_answer():
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return b'{"choices":[{"message":{"content":"seen"}}]}'
    return Response()


def photo_json():
    return json.dumps({'data': [{'b64_json': base64.b64encode(b'png').decode('ascii')}]}).encode('utf-8')


def slept(sleep):
    return [call.args[0] for call in sleep.await_args_list]


def logged(warning):
    return [call.args[0] % call.args[1:] if len(call.args) > 1 else str(call.args[0])
            for call in warning.call_args_list]


def neutral(parts):
    frame = {'post_type': 'message', 'message_type': 'private', 'self_id': '20002',
             'user_id': '10001', 'message_id': '10003', 'message': parts}
    return turn.TurnEvent(adapter_onebot.from_onebot(frame))


class BusyServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='ams-life-busy-')
        self.addCleanup(shutil.rmtree, self.tmp, True)
        root = Path(self.tmp)
        self.saved_dirs = (phone.SELFIE_DIR, phone.REF_DIR)
        phone.SELFIE_DIR = root / 'selfie'
        phone.REF_DIR = phone.SELFIE_DIR / 'refs'
        self.addCleanup(self._restore_dirs)
        self.plugin = test_selfie.Phone()
        self.plugin.config['vision_image_api_model'] = 'model'
        self.plugin._phone_account = lambda *args: None
        self.plugin._phone_price = lambda *args: 0
        self.api = vision.ImageAPI(self.plugin)

    def _restore_dirs(self):
        phone.SELFIE_DIR, phone.REF_DIR = self.saved_dirs

    async def test_vision_waits_5_then_10_seconds_and_sees_the_image(self):
        with patch('urllib.request.urlopen', side_effect=[busy(), busy(), an_answer()]) as request, \
                patch.object(vision, '_rest', new=AsyncMock()) as sleep, \
                patch.object(vision.logger, 'warning') as warning:
            reply = await self.api.text_chat(prompt='看图')
        self.assertEqual(reply.completion_text, 'seen')
        self.assertEqual(request.call_count, 3)
        self.assertEqual(slept(sleep), [5, 10])
        messages = logged(warning)
        self.assertIn('[ams-life] vision service busy (429), retry in 5s', messages)
        self.assertIn('[ams-life] vision service busy (429), retry in 10s', messages)

    async def test_vision_gives_up_after_at_most_three_minutes(self):
        with patch('urllib.request.urlopen', side_effect=always_busy) as request, \
                patch.object(vision, '_rest', new=AsyncMock()) as sleep, \
                patch.object(vision.logger, 'warning') as warning:
            with self.assertRaises(RuntimeError):
                await self.api.text_chat(prompt='看图')
        self.assertEqual(request.call_count, 6)
        self.assertEqual(slept(sleep), [5, 10, 20, 40, 60])
        self.assertLessEqual(sum(slept(sleep)), 3 * 60)
        self.assertIn('[ams-life] vision service busy (429), gave up after 135s', logged(warning))

    async def test_photo_waits_5_then_10_seconds_and_makes_the_photo(self):
        self.plugin._post_json = AsyncMock(side_effect=[busy(), busy(), (photo_json(), 'application/json')])
        with patch.object(vision, '_rest', new=AsyncMock()) as sleep, \
                patch.object(vision.logger, 'warning') as warning:
            path = await self.plugin._make_photo('snap', '窗边的天空')
        self.assertIsNotNone(path)
        self.assertEqual(path.read_bytes(), b'png')
        self.assertEqual(self.plugin._post_json.await_count, 3)
        self.assertEqual(slept(sleep), [5, 10])
        self.assertIn('[ams-life] vision service busy (429), retry in 5s', logged(warning))

    async def test_vision_request_takes_the_bridge_lock_before_sending(self):
        lock = vision.bridge_lock(self.plugin)
        held = []
        def open_request(*args, **kwargs):
            held.append(lock.locked())
            return an_answer()
        with patch('urllib.request.urlopen', side_effect=open_request):
            self.assertEqual((await self.api.text_chat(prompt='看图')).completion_text, 'seen')
        self.assertEqual(held, [True])

    async def test_photo_requests_take_the_bridge_lock_before_sending(self):
        lock = vision.bridge_lock(self.plugin)
        seen_urls = []
        async def post_json(url, payload, key, timeout=120):
            seen_urls.append((url, lock.locked()))
            return photo_json(), 'application/json'
        async def post_selfie(url, prompt, key, size, ref):
            seen_urls.append((url, lock.locked()))
            return photo_json()
        self.plugin._post_json = post_json
        self.plugin._post_selfie = post_selfie
        phone.REF_DIR.mkdir(parents=True, exist_ok=True)
        (phone.REF_DIR / 'her_base.png').write_bytes(b'fake png')
        self.assertIsNotNone(await self.plugin._make_photo('snap', '窗边的天空'))
        self.assertIsNotNone(await self.plugin._make_photo('selfie', '在家穿毛衣侧身看窗'))
        self.assertEqual([url.rsplit('/', 1)[-1] for url, _ in seen_urls], ['generations', 'edits'])
        self.assertTrue(all(held for _url, held in seen_urls))

    async def test_gave_up_vision_is_told_as_an_unseen_image(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        test_basics.PLUGINS.append(plugin)
        plugin.llm_functions['image_caption'] = {'enabled': True, 'provider': 'image_api'}
        plugin.config['vision_image_api_model'] = 'model'
        plugin.api_config = {'image': {'base_url': 'https://vision.invalid/v1'}}
        event = neutral([{'type': 'image', 'data': {'url': IMAGE_URL}}])
        with patch('urllib.request.urlopen', side_effect=always_busy) as request, \
                patch.object(vision, '_rest', new=AsyncMock()) as sleep:
            image_context = await plugin._image_context(event)
        self.assertEqual(image_context, '')
        self.assertEqual(request.call_count, 6)
        self.assertEqual(slept(sleep), [5, 10, 20, 40, 60])
        plugin._image_context = AsyncMock(return_value=image_context)
        request_parts = turn.TurnRequest(prompt='hello')
        await plugin._prepare_turn(event, request_parts)
        prompt = '\n'.join(part.get('text', '') for part in request_parts.extra_user_content_parts)
        self.assertIn('[图] ' + attention.UNSEEN_IMAGE_NOTE, prompt)


if __name__ == '__main__':
    unittest.main()
