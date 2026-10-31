# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check API configuration key handling in both runtimes."""
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import mixin_pages
import mixin_settings


class ConfigPage(mixin_pages.PagesMixin, mixin_settings.SettingsMixin):
    def _public_api_config(self):
        return {}


class ApiConfigKeys(unittest.IsolatedAsyncioTestCase):
    async def save_config(self, old, incoming, standalone):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'api_config.json'
            page = ConfigPage()
            page.api_config = {'embedding': old}
            page.llm_functions = {}
            if standalone:
                page._key_store = object()

            async def get_json(silent=True):
                return {'embedding': incoming}

            quart = types.SimpleNamespace(request=types.SimpleNamespace(get_json=get_json))
            with patch.dict(sys.modules, {'quart': quart}), \
                    patch.object(mixin_settings, 'API_CONFIG_PATH', path), \
                    patch.object(mixin_pages.logger, 'info') as log:
                result = await page.page_api_config()
            self.assertEqual(result['status'], 'ok')
            return json.loads(path.read_text(encoding='utf-8'))['embedding'], log.call_args_list

    async def test_standalone_keeps_old_key_and_updates_base_url(self):
        entry, log = await self.save_config(
            {'api_key': 'old-made-up'},
            {'api_key': 'new-made-up', 'base_url': 'https://example.invalid'}, True)
        self.assertEqual(entry['api_key'], 'old-made-up')
        self.assertEqual(entry['base_url'], 'https://example.invalid')
        self.assertNotIn('new-made-up', str(log))
        self.assertTrue(any('embedding' in str(call) for call in log))

    async def test_standalone_discards_key_when_none_saved(self):
        entry, _ = await self.save_config({}, {'api_key': 'new-made-up'}, True)
        self.assertEqual(entry['api_key'], '')

    async def test_astrbot_saves_new_key(self):
        entry, _ = await self.save_config({}, {'api_key': 'new-made-up'}, False)
        self.assertEqual(entry['api_key'], 'new-made-up')

    async def test_standalone_empty_key_keeps_old_key(self):
        entry, _ = await self.save_config({'api_key': 'old-made-up'}, {'api_key': ''}, True)
        self.assertEqual(entry['api_key'], 'old-made-up')
