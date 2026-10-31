# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for vision image preparation."""
import asyncio
import base64
import io
import json
import random
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import vision

try:
    from PIL import Image
except ImportError:
    Image = None


def encoded(image, format, **kwargs):
    output = io.BytesIO()
    image.save(output, format, **kwargs)
    return output.getvalue()


@unittest.skipUnless(Image is not None, 'Pillow is required for image preparation')
class VisionPrepareTests(unittest.TestCase):
    def test_unreadable_image_returns_original(self):
        data = b'not an image'
        with patch.object(vision.logger, 'warning') as warning:
            self.assertEqual(vision._prepared(data), data)
        warning.assert_called_once_with('[ams-life] image preparation failed: %s', 'UnidentifiedImageError')

    def test_large_image_is_bounded_jpeg(self):
        pixels = random.Random(1).randbytes(4000 * 3000 * 3)
        with Image.frombytes('RGB', (4000, 3000), pixels) as image:
            data = encoded(image, 'PNG')
        result = vision._prepared(data)
        with Image.open(io.BytesIO(result)) as image:
            self.assertEqual(image.format, 'JPEG')
            self.assertLessEqual(max(image.size), vision.VISION_MAX_SIDE)
        self.assertLessEqual(len(result), vision.VISION_MAX_BYTES)

    def test_gif_uses_first_frame(self):
        frames = [Image.new('RGB', (40, 40), color) for color in ('red', 'green', 'blue')]
        try:
            data = encoded(frames[0], 'GIF', save_all=True, append_images=frames[1:])
        finally:
            for frame in frames:
                frame.close()
        with Image.open(io.BytesIO(vision._prepared(data))) as image:
            self.assertEqual(image.format, 'JPEG')
            self.assertEqual(getattr(image, 'n_frames', 1), 1)
            self.assertGreater(image.getpixel((0, 0))[0], 200)

    def test_transparent_png_is_bounded(self):
        pixels = random.Random(2).randbytes(1280 * 1280 * 4)
        with Image.frombytes('RGBA', (1280, 1280), pixels) as image:
            result = vision._prepared(encoded(image, 'PNG'))
        self.assertLessEqual(len(result), vision.VISION_MAX_BYTES)
        with Image.open(io.BytesIO(result)) as image:
            self.assertEqual(image.format, 'PNG')
            self.assertEqual(image.mode, 'RGBA')

    def test_small_jpeg_remains_usable(self):
        with Image.new('RGB', (200, 200), 'blue') as image:
            result = vision._prepared(encoded(image, 'JPEG'))
        with Image.open(io.BytesIO(result)) as image:
            image.load()
            self.assertEqual(image.size, (200, 200))
            self.assertEqual(image.format, 'JPEG')

    def test_request_contains_prepared_jpeg(self):
        with Image.new('RGB', (2000, 1500), 'red') as image:
            data = encoded(image, 'PNG')
        ref = 'data:image/png;base64,' + base64.b64encode(data).decode('ascii')
        plugin = types.SimpleNamespace(api_config={'image': {'base_url': 'https://vision.invalid'}},
                                       config={'vision_image_api_model': 'example'})
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b'{"choices":[{"message":{"content":"ok"}}]}'

        def send(request, timeout):
            self.assertLess(len(request.data), 1500000)
            content = json.loads(request.data)['messages'][0]['content']
            self.assertTrue(content[1]['image_url']['url'].startswith('data:image/jpeg;base64,'))
            return Response()

        with patch('urllib.request.urlopen', send):
            asyncio.run(vision.ImageAPI(plugin).text_chat(image_urls=[ref]))


class MissingPillowTests(unittest.TestCase):
    def test_original_is_returned_and_warning_once(self):
        original = b'\x89PNG\r\n\x1a\noriginal image bytes'
        ref = 'data:image/png;base64,' + base64.b64encode(original).decode('ascii')
        plugin = types.SimpleNamespace(api_config={'image': {'base_url': 'https://vision.invalid'}},
                                       config={'vision_image_api_model': 'example'})
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b'{"choices":[{"message":{"content":"ok"}}]}'

        def send(request, timeout):
            content = json.loads(request.data)['messages'][0]['content']
            self.assertEqual(content[1]['image_url']['url'], ref)
            return Response()

        with patch.dict(sys.modules, {'PIL': None}), patch.object(vision, '_pillow_warned', False), \
                patch.object(vision.logger, 'warning') as warning, patch('urllib.request.urlopen', send):
            asyncio.run(vision.ImageAPI(plugin).text_chat(image_urls=[ref, ref]))
        warning.assert_called_once()
