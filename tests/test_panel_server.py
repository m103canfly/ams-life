# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Tests for the local panel server."""
import ast
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from key_store import KeyStore

HAS_AIOHTTP = importlib.util.find_spec('aiohttp') is not None
if HAS_AIOHTTP:
    from aiohttp import ClientSession, ClientConnectorError
    from yarl import URL
    from panel_server import PanelServer, TOKEN_HEADER, TOKEN_META


class KeyDamageTest(unittest.TestCase):
    def test_damage_detection_without_decryption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'keys.json'
            store = KeyStore(path)
            with patch('key_store._crypt', side_effect=AssertionError('unexpected decryption')):
                self.assertFalse(store.damaged())
                for content in ('{"version": 1, "keys": {}}',
                                '{"version": 1, "keys": {"valid": "opaque"}}'):
                    path.write_text(content, encoding='utf-8')
                    self.assertFalse(store.damaged())
                for content in ('not json', '[]', '{"version": 2, "keys": {}}',
                                '{"version": true, "keys": {}}', '{"version": 1, "keys": []}',
                                '{"version": 1, "keys": {"Bad": "opaque"}}',
                                '{"version": 1, "keys": {"valid": 1}}'):
                    with self.subTest(content=content):
                        path.write_text(content, encoding='utf-8')
                        self.assertTrue(store.damaged())
                        self.assertEqual(store.status(), {})
                path.write_bytes(b'\xff')
                self.assertTrue(store.damaged())
                with patch.object(Path, 'open', side_effect=PermissionError):
                    self.assertTrue(store.damaged())
                    self.assertEqual(store.status(), {})


@unittest.skipUnless(HAS_AIOHTTP, 'aiohttp is required')
class PanelTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'web'
        self.root.mkdir()
        (self.root / 'index.html').write_text('<html><head></head><body>panel</body></html>', encoding='utf-8')
        (self.root / 'app.js').write_text('app', encoding='utf-8')
        (self.root / 'private.py').write_text('private', encoding='utf-8')
        self.keys = KeyStore(Path(self.tmp.name) / 'keys.json')
        self.server = PanelServer(root=self.root, keys=self.keys)
        self.port = await self.server.start()
        self.addAsyncCleanup(self.server.stop)
        self.client = ClientSession()
        self.addAsyncCleanup(self.client.close)
        self.base = f'http://127.0.0.1:{self.port}'

    async def request(self, method, path, **kwargs):
        async with self.client.request(method, URL(self.base + path, encoded=True), **kwargs) as response:
            return response.status, dict(response.headers), await response.text()

    def auth(self):
        return {'Origin': self.base, TOKEN_HEADER: self.server.token}

    async def test_constructor_and_token(self):
        with self.assertRaises(ValueError):
            PanelServer(root=self.root, keys=self.keys, host='0.0.0.0')
        other = PanelServer(root=self.root, keys=self.keys)
        self.assertNotEqual(self.server.token, other.token)
        status, _, body = await self.request('GET', '/')
        self.assertEqual(status, 200)
        self.assertIn(TOKEN_META % self.server.token, body)
        self.assertLess(body.index(TOKEN_META % self.server.token), body.index('</head>'))
        self.assertNotIn(self.server.token, (self.root / 'index.html').read_text(encoding='utf-8'))

    async def test_host_validation(self):
        for host in (f'evil.test:{self.port}', '127.0.0.1:1'):
            status, _, body = await self.request('GET', '/', headers={'Host': host})
            self.assertEqual((status, body), (421, 'bad host'))
        for host in (f'127.0.0.1:{self.port}', f'localhost:{self.port}', f'[::1]:{self.port}'):
            self.assertEqual((await self.request('GET', '/', headers={'Host': host}))[0], 200)

    async def test_origin_and_token_validation(self):
        for origin in (None, 'http://evil.test', 'null'):
            headers = {TOKEN_HEADER: self.server.token}
            if origin is not None:
                headers['Origin'] = origin
            status, _, body = await self.request('POST', '/api/keys', headers=headers)
            self.assertEqual((status, body), (403, 'bad origin'))
        for token in (None, 'wrong'):
            headers = {'Origin': self.base}
            if token is not None:
                headers[TOKEN_HEADER] = token
            status, _, body = await self.request('POST', '/api/keys', headers=headers)
            self.assertEqual((status, body), (403, 'bad token'))
        for origin in (self.base, f'http://localhost:{self.port}', f'http://[::1]:{self.port}'):
            status, _, _ = await self.request('DELETE', '/api/keys/deepseek',
                                              headers={'Origin': origin, TOKEN_HEADER: self.server.token})
            self.assertEqual(status, 200)

    async def test_read_only_and_headers(self):
        for path in ('/', '/static/app.js', '/api/keys', '/missing'):
            status, headers, body = await self.request('GET', path)
            self.assertEqual(status, 404 if path == '/missing' else 200)
            self.assertFalse(any(k.lower().startswith('access-control-allow-') for k in headers))
            for key, value in {'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY',
                               'Referrer-Policy': 'no-referrer', 'Cache-Control': 'no-store'}.items():
                self.assertEqual(headers[key], value)
            if path != '/':
                self.assertNotIn(self.server.token, body)
        self.assertEqual((await self.request('OPTIONS', '/'))[0], 405)
        self.assertEqual((await self.request('TRACE', '/'))[0], 405)

    async def test_key_damage_status(self):
        for content, damaged in ((None, False), ('{"version": 1, "keys": {}}', False),
                                 ('broken', True)):
            if content is not None:
                self.keys.path.write_text(content, encoding='utf-8')
            status, _, body = await self.request('GET', '/api/keys')
            self.assertEqual(status, 200)
            result = json.loads(body)
            self.assertEqual(result['keys'], {'deepseek': False, 'vision': False})
            self.assertEqual(result.get('damaged', False), damaged)
            if not damaged:
                self.assertNotIn('damaged', result)

    async def test_static_paths(self):
        self.assertEqual((await self.request('GET', '/static/app.js'))[2], 'app')
        for path in ('/static/../outside.js', '/static/%2e%2e/outside.js', '/static//outside.js',
                     '/static/', '/static/private.py'):
            self.assertEqual((await self.request('GET', path))[0], 404, path)

    async def test_static_symlink(self):
        outside = Path(self.tmp.name) / 'outside.js'
        outside.write_text('outside', encoding='utf-8')
        try:
            (self.root / 'link.js').symlink_to(outside)
        except OSError:
            self.skipTest('symlink creation is unavailable')
        self.assertEqual((await self.request('GET', '/static/link.js'))[0], 404)

    async def test_stop_closes_port(self):
        await self.server.stop()
        async with ClientSession() as client:
            with self.assertRaises(ClientConnectorError):
                await client.get(self.base + '/')

    async def test_source_constraints(self):
        source = (Path(__file__).resolve().parent.parent / 'panel_server.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        self.assertNotIn('0.0.0.0', source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(alias.name.startswith('astrbot') for alias in node.names))
            if isinstance(node, ast.ImportFrom):
                self.assertFalse((node.module or '').startswith('astrbot'))
        self.assertIn('secrets.token_urlsafe(32)', source)

    @unittest.skipUnless(os.name == 'nt', 'DPAPI requires Windows')
    async def test_keys_write_only_and_damaged(self):
        value = 'invented-test-value-123'
        with self.assertLogs('panel_server', level='INFO') as logs:
            status, _, body = await self.request('POST', '/api/keys', headers=self.auth(),
                                                 json={'name': 'deepseek', 'value': value})
            self.assertEqual((status, body), (200, '{"ok": true}'))
            status, _, body = await self.request('GET', '/api/keys')
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)['keys'], {'deepseek': True, 'vision': False})
            self.assertNotIn(value, body)
            await self.request('GET', '/', headers={'Host': 'evil.test'})
        self.assertNotIn(value, '\n'.join(logs.output))
        self.assertNotIn(self.server.token, '\n'.join(logs.output))
        self.assertEqual((await self.request('DELETE', '/api/keys/deepseek', headers=self.auth()))[0], 200)
        self.assertFalse(json.loads((await self.request('GET', '/api/keys'))[2])['keys']['deepseek'])
        for method, path, data in (('POST', '/api/keys', {'name': 'unknown', 'value': value}),
                                   ('DELETE', '/api/keys/unknown', None)):
            self.assertEqual((await self.request(method, path, headers=self.auth(), json=data))[0], 400)
        status, _, body = await self.request('POST', '/api/keys', headers=self.auth(),
                                             json={'name': 'deepseek', 'value': ''})
        self.assertEqual((status, body), (400, 'invalid'))
        self.keys.path.write_text('broken', encoding='utf-8')
        self.assertTrue(json.loads((await self.request('GET', '/api/keys'))[2])['damaged'])
