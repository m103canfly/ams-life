# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check photo credentials without making requests."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import key_store  # noqa: E402
import mixin_selfie as phone  # noqa: E402
from test_selfie import Phone  # noqa: E402


class PhotoKeyTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        refs = root / 'refs'
        refs.mkdir()
        (refs / 'her_base.png').write_bytes(b'fake png')
        ref_patch = patch.object(phone, 'REF_DIR', refs)
        ref_patch.start()
        self.addCleanup(ref_patch.stop)
        self.p = Phone()
        self.p.api_config['image']['api_key'] = 'made-up-old'
        self.p._phone_path = Mock(return_value=root / 'photo.png')
        self.p._phone_account = Mock()
        raw = b'{"data":[{"b64_json":"cG5n"}]}'
        self.p._post_selfie = AsyncMock(return_value=raw)
        self.p._post_json = AsyncMock(return_value=(raw, 'application/json'))

    async def test_selfie_uses_vision_store(self):
        self.p._key_store = Mock()
        self.p._key_store.get.return_value = 'made-up-vision'
        self.assertIsNotNone(await self.p._make_photo('selfie', 'a scene'))
        self.p._key_store.get.assert_called_once_with('vision')
        self.assertEqual(self.p._post_selfie.await_args.args[2], 'made-up-vision')

    async def test_selfie_missing_vision_uses_empty_key(self):
        self.p._key_store = Mock()
        self.p._key_store.get.side_effect = key_store.KeyStoreError()
        self.assertIsNotNone(await self.p._make_photo('selfie', 'a scene'))
        self.assertEqual(self.p._post_selfie.await_args.args[2], '')

    async def test_selfie_astrbot_uses_config_key(self):
        self.assertIsNotNone(await self.p._make_photo('selfie', 'a scene'))
        self.assertEqual(self.p._post_selfie.await_args.args[2], 'made-up-old')

    async def test_snap_uses_vision_store(self):
        self.p._key_store = Mock()
        self.p._key_store.get.return_value = 'made-up-vision'
        self.assertIsNotNone(await self.p._make_photo('snap', 'a scene'))
        self.p._key_store.get.assert_called_once_with('vision')
        self.assertEqual(self.p._post_json.await_args.args[2], 'made-up-vision')
