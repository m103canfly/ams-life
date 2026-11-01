# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check photo prompts and the prompts sent to the image service."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import test_selfie  # noqa: E402
import mixin_selfie as phone  # noqa: E402


class PhotoPromptTests(unittest.IsolatedAsyncioTestCase):
    def test_selfie_and_guide_describe_self_taken_photos(self):
        for phrase in ('自己拿 iPhone', '前置镜头', '对着镜子', '没有第二个拍照的人'):
            self.assertIn(phrase, phone.SELFIE_PROMPT)
        for prompt in (phone.SELFIE_PROMPT, phone.PHOTO_GUIDE):
            for phrase in ('朋友抓拍', '回头'):
                self.assertNotIn(phrase, prompt)

    def test_guide_keeps_varied_angles(self):
        for angle in ('四分之三侧', '低头', '俯拍', '对镜'):
            self.assertIn(angle, phone.PHOTO_GUIDE)

    def test_snap_starts_with_rear_camera(self):
        self.assertTrue(phone.SNAP_PROMPT.startswith('她自己用 iPhone 随手拍的照片（后置镜头）'))

    async def test_make_photo_sends_the_matching_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'her_base.png').write_bytes(b'fake reference')
            plugin = test_selfie.Phone()
            plugin._phone_account = Mock()
            plugin._phone_price = Mock(return_value=0)
            plugin._phone_path = Mock(return_value=root / 'photo.png')
            raw = b'{"data": [{"b64_json": "cG5n"}]}'
            plugin._post_selfie = AsyncMock(return_value=raw)
            plugin._post_json = AsyncMock(return_value=(raw, 'application/json'))
            with patch.object(phone, 'REF_DIR', root):
                selfie_what = '在家穿毛衣侧身看窗'
                self.assertIsNotNone(await plugin._make_photo('selfie', selfie_what))
                self.assertEqual(plugin._post_selfie.await_args.args[1], phone.SELFIE_PROMPT + selfie_what)
                snap_what = '窗边的天空'
                self.assertIsNotNone(await plugin._make_photo('snap', snap_what))
                self.assertEqual(plugin._post_json.await_args.args[1]['prompt'], phone.SNAP_PROMPT + snap_what)
