# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for standalone panel LLM settings."""
import sys
import types
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import app
import deepseek_client
import key_store
import mixin_pages


class StartupTests(unittest.IsolatedAsyncioTestCase):
    async def start_with(self, llm, reject_panel=False):
        captured = []
        class FakeHer:
            def __init__(self, collector, config):
                self.api_config = {'llm': llm}
                self._history_gate = Mock()

        class FakeModel(deepseek_client.DeepSeekModel):
            def __init__(self, **kwargs):
                captured.append(kwargs.copy())
                if reject_panel and 'base_url' in kwargs:
                    raise ValueError('rejected')
                super().__init__(client=object(), **kwargs)
                self.test_key = kwargs['api_key']

        keys = Mock()
        keys.has.side_effect = lambda name: name == 'deepseek'
        keys.get.return_value = 'made-up-key'
        history = Mock()
        panel = types.SimpleNamespace(start=AsyncMock(return_value=1), stop=AsyncMock())
        collector = types.SimpleNamespace(routes=[], register_web_api=Mock())
        modules = {
            'app_config': types.SimpleNamespace(load_schema=lambda: {}, load=lambda path, schema: ({}, [])),
            'persona_file': types.SimpleNamespace(NAME='persona.md', load=lambda path: types.SimpleNamespace(text='')),
            'panel_api': types.SimpleNamespace(RouteCollector=lambda: collector,
                                               install_request_shim=lambda: None, aiohttp_routes=lambda routes: []),
            'her': types.SimpleNamespace(Her=FakeHer),
            'history_store': types.SimpleNamespace(HistoryStore=lambda path: history),
            'panel_server': types.SimpleNamespace(PanelServer=lambda **kwargs: panel),
        }
        args = Namespace(data=str(test_basics.DATA), model='fallback-model', panel_port=0, onebot_port=0)
        instance = app.App(args)
        with patch.dict(sys.modules, modules), patch.object(app, 'prepare_data', return_value=test_basics.DATA), \
                patch.object(key_store, 'KeyStore', return_value=keys), \
                patch.object(deepseek_client, 'DeepSeekModel', FakeModel):
            await instance.start()
            await instance.stop()
        return instance.her._neutral_model, captured

    async def test_panel_model_and_key_are_used(self):
        model, calls = await self.start_with({'source': 'custom', 'base_url': 'https://api.deepseek.com/v1',
                                              'model': 'made-up-model'})
        self.assertEqual((model.base_url, model.model, model.test_key),
                         ('https://api.deepseek.com/v1', 'made-up-model', 'made-up-key'))
        self.assertEqual(len(calls), 1)

    async def test_astrbot_and_incomplete_config_fall_back(self):
        for config in ({'source': 'astrbot', 'base_url': 'https://api.deepseek.com/v1', 'model': 'other'},
                       {'source': 'custom', 'model': 'other'}, {'source': 'custom', 'base_url': 'https://api.deepseek.com'}):
            with self.subTest(config=config):
                model, calls = await self.start_with(config)
                self.assertEqual((model.model, model.base_url), ('fallback-model', deepseek_client.BASE_URL))
                self.assertNotIn('base_url', calls[0])

    async def test_invalid_addresses_fall_back_without_logging_address(self):
        for url in ('https://example.invalid/v1', 'http://api.deepseek.com',
                    'https://api.deepseek.com.evil.test', 'https://api.deepseek.com@evil.test'):
            with self.subTest(url=url), self.assertLogs('ams-life.app', level='WARNING') as logs:
                model, calls = await self.start_with({'source': 'custom', 'base_url': url, 'model': 'other'})
                self.assertEqual((model.model, model.base_url), ('fallback-model', deepseek_client.BASE_URL))
                self.assertEqual(len(calls), 1)
                self.assertNotIn(url, '\n'.join(logs.output))

    async def test_constructor_value_error_falls_back(self):
        model, calls = await self.start_with({'source': 'custom', 'base_url': 'https://api.deepseek.com/v1',
                                              'model': 'other'}, reject_panel=True)
        self.assertEqual((model.model, model.base_url), ('fallback-model', deepseek_client.BASE_URL))
        self.assertEqual(len(calls), 2)


class PageModelsTests(unittest.IsolatedAsyncioTestCase):
    async def call_page(self, body, keys=None):
        fetch = AsyncMock(return_value={'status': 'ok'})
        page = types.SimpleNamespace(_key_store=keys, _fetch_models=fetch)
        request = types.SimpleNamespace(get_json=AsyncMock(return_value=body))
        with patch.dict(sys.modules, {'quart': types.SimpleNamespace(request=request)}):
            result = await mixin_pages.PagesMixin.page_models(page)
        return result, fetch

    async def test_standalone_uses_stored_key(self):
        keys = Mock()
        keys.has.return_value = True
        keys.get.return_value = 'made-up-key'
        result, fetch = await self.call_page({'kind': 'llm', 'source': 'astrbot',
                                              'base_url': 'https://api.deepseek.com/v1', 'api_key': ''}, keys)
        self.assertEqual(result, {'status': 'ok'})
        fetch.assert_awaited_once_with('llm', 'custom', 'https://api.deepseek.com/v1', 'made-up-key')

    async def test_invalid_address_never_fetches(self):
        result, fetch = await self.call_page({'kind': 'llm', 'base_url': 'https://example.invalid/v1'}, Mock())
        self.assertEqual(result, {'status': 'error', 'message': '只认 DeepSeek 的地址（https://api.deepseek.com）'})
        fetch.assert_not_awaited()

    async def test_astrbot_keeps_page_key(self):
        _, fetch = await self.call_page({'kind': 'llm', 'base_url': 'https://example.invalid/v1',
                                         'api_key': 'made-up-page-key'})
        fetch.assert_awaited_once_with('llm', 'custom', 'https://example.invalid/v1', 'made-up-page-key')

    async def test_missing_or_unreadable_key_is_empty(self):
        for missing in (True, False):
            keys = Mock()
            keys.has.return_value = not missing
            keys.get.side_effect = key_store.KeyStoreError('unreadable')
            _, fetch = await self.call_page({'kind': 'llm', 'base_url': 'https://api.deepseek.com',
                                             'api_key': 'ignored-key'}, keys)
            fetch.assert_awaited_once_with('llm', 'custom', 'https://api.deepseek.com', '')

    async def test_other_kind_keeps_page_key(self):
        _, fetch = await self.call_page({'kind': 'embedding', 'base_url': 'https://example.invalid/v1',
                                         'api_key': 'made-up-page-key'}, Mock())
        fetch.assert_awaited_once_with('embedding', 'custom', 'https://example.invalid/v1', 'made-up-page-key')

    async def test_standalone_model_fetch_refuses_redirects(self):
        import urllib.request
        response = MagicMock()
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        response.read.return_value = b'{"data": []}'
        opener = Mock()
        opener.open.return_value = response
        page = types.SimpleNamespace(_key_store=Mock(), _astrbot_llm_default=lambda: None,
                                     _models_url=mixin_pages.PagesMixin._models_url)
        with patch.object(urllib.request, 'build_opener', return_value=opener) as build:
            await mixin_pages.PagesMixin._fetch_models(page, 'llm', 'custom',
                                                       'https://api.deepseek.com/v1', 'made-up-key')
        handlers = build.call_args.args
        redirect = next(handler for handler in handlers if isinstance(handler, urllib.request.HTTPRedirectHandler))
        self.assertIsNone(redirect.redirect_request(None, None, 302, '', {}, 'https://example.invalid'))

