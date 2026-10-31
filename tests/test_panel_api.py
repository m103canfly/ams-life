# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The panel's page API: the plugin's routes, served by our own panel server.

The plugin still registers its pages the way AstrBot asks for them; a RouteCollector stands
in for the context. The page handlers read their request through `quart`; a small stand-in
supplies the request being answered. Every example is invented (10001, 20002, 900001).
The server listens on loopback only; nothing goes out."""
import ast
import asyncio
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import test_basics  # noqa: E402  the offline settings and data directory, before main
import harness  # noqa: E402
from key_store import KeyStore  # noqa: E402

HAS_AIOHTTP = importlib.util.find_spec('aiohttp') is not None
if HAS_AIOHTTP:
    from aiohttp import ClientSession
    from yarl import URL
    import panel_api
    from panel_server import PanelServer, TOKEN_HEADER, TOKEN_META

_MISSING = object()


def saved_quart():
    """What sys.modules["quart"] was before the stand-in is installed."""
    return sys.modules.get('quart', _MISSING)


def restore_quart(before):
    """Put sys.modules["quart"] back; the other tests here and in tests/*_cases.py use it too."""
    if before is _MISSING:
        sys.modules.pop('quart', None)
    else:
        sys.modules['quart'] = before


@unittest.skipUnless(HAS_AIOHTTP, 'aiohttp is required')
class CollectedRoutes(unittest.TestCase):
    """The plugin registers its own pages; the collector records them as AstrBot would."""

    def test_collects_the_plugin_routes_in_order(self):
        context = harness.FakeContext()
        plugin = test_basics.make_plugin(context)
        self.assertEqual(len(context.web_routes), 28)
        collector = panel_api.RouteCollector()
        original = plugin.context
        plugin.context = collector
        try:
            plugin._register_page_api()
        finally:
            plugin.context = original
        self.assertEqual(len(collector.routes), 28)
        self.assertEqual([route[0] for route in collector.routes], context.web_routes)
        names = {route[0]: route[1].__name__ for route in collector.routes}
        self.assertEqual(names[panel_api.PREFIX + 'page/status'], 'page_status')
        self.assertEqual(names[panel_api.PREFIX + 'page/brain/search'], 'page_brain_search')
        self.assertEqual(names[panel_api.PREFIX + 'page/memory/delete/<path:session>/<entry_id>'],
                         'page_memory_delete')
        for path, handler, methods, desc in collector.routes:
            self.assertIs(handler.__self__, plugin, path)
            self.assertTrue(methods, path)
            self.assertTrue(desc, path)

    def test_rejects_a_route_outside_the_panel_prefix(self):
        collector = panel_api.RouteCollector()
        with self.assertRaises(ValueError):
            collector.register_web_api('/astrbot_plugin_other/page/status', len, ['GET'], 'made up')
        self.assertEqual(collector.routes, [])
        collector.register_web_api(panel_api.PREFIX + 'page/status', len, ['GET', 'POST'], 'made up')
        self.assertEqual(len(collector.routes), 1)
        self.assertEqual(collector.routes[0][2], ('GET', 'POST'))


@unittest.skipUnless(HAS_AIOHTTP, 'aiohttp is required')
class RequestShim(unittest.TestCase):
    """sys.modules["quart"]: our stand-in only, never over somebody else's."""

    def setUp(self):
        self.before = saved_quart()
        sys.modules.pop('quart', None)
        self.addCleanup(restore_quart, self.before)

    def test_refuses_to_cover_another_quart(self):
        other = types.ModuleType('quart')
        sys.modules['quart'] = other
        with self.assertRaises(RuntimeError):
            panel_api.install_request_shim()
        self.assertIs(sys.modules['quart'], other)

    def test_installs_itself_and_installing_twice_is_harmless(self):
        panel_api.install_request_shim()
        installed = sys.modules['quart']
        self.assertTrue(hasattr(installed, 'request'))
        panel_api.install_request_shim()
        self.assertIs(sys.modules['quart'], installed)

    def test_outside_a_request_it_raises(self):
        panel_api.install_request_shim()
        from quart import request
        with self.assertRaises(RuntimeError):
            _ = request.method
        with self.assertRaises(RuntimeError):
            _ = request.args
        with self.assertRaises(RuntimeError):
            asyncio.run(request.get_json(silent=True))


@unittest.skipUnless(HAS_AIOHTTP, 'aiohttp is required')
class ServedApi(unittest.IsolatedAsyncioTestCase):
    """The plugin's own routes, answered by PanelServer."""

    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'web'
        self.root.mkdir()
        (self.root / 'index.html').write_text('<html><head></head><body>panel</body></html>',
                                              encoding='utf-8')
        self.keys = KeyStore(Path(self.tmp.name) / 'keys.json')
        self.client = ClientSession()
        self.addAsyncCleanup(self.client.close)
        self.before_quart = saved_quart()
        panel_api.install_request_shim()
        self.addCleanup(restore_quart, self.before_quart)
        context = harness.FakeContext()
        self.plugin = test_basics.make_plugin(context)
        collector = panel_api.RouteCollector()
        original = self.plugin.context
        self.plugin.context = collector
        try:
            self.plugin._register_page_api()
        finally:
            self.plugin.context = original
        self.server, self.base = await self.start(
            api_routes=panel_api.aiohttp_routes(collector.routes))

    async def start(self, **kwargs):
        server = PanelServer(root=self.root, keys=self.keys, **kwargs)
        port = await server.start()
        self.addAsyncCleanup(server.stop)
        return server, 'http://127.0.0.1:%d' % port

    @staticmethod
    def auth(server, base):
        return {'Origin': base, TOKEN_HEADER: server.token}

    async def request(self, method, path, base=None, **kwargs):
        url = URL((base or self.base) + path, encoded=True)
        async with self.client.request(method, url, **kwargs) as response:
            return response.status, dict(response.headers), await response.text()

    async def test_get_answers_as_the_plugin_does(self):
        status, headers, body = await self.request('GET', '/api/page/status')
        self.assertEqual(status, 200)
        self.assertTrue(headers['Content-Type'].startswith('application/json'), headers)
        served = json.loads(body)
        direct = await self.plugin.page_status()
        self.assertEqual(served['status'], direct['status'])
        self.assertEqual(set(served['data']), set(direct['data']))
        self.assertIn('enabled', served['data'])

    async def test_post_toggle_changes_the_setting(self):
        before = self.plugin.proactive_reply
        status, _, body = await self.request('POST', '/api/page/toggle',
                                             headers=self.auth(self.server, self.base),
                                             json={'key': 'proactive_reply', 'value': not before})
        self.assertEqual(status, 200)
        result = json.loads(body)
        self.assertEqual(result['status'], 'ok')
        self.assertIs(result['data']['value'], not before)
        self.assertIs(self.plugin.proactive_reply, not before)

    async def test_writes_need_the_origin_and_the_token(self):
        calls = []

        async def made_up():
            calls.append(1)
            return {'status': 'ok', 'data': {'called': True}}

        routes = panel_api.aiohttp_routes([
            (panel_api.PREFIX + 'page/made_up', made_up, ['POST'], 'made up')])
        server, base = await self.start(api_routes=routes)
        for headers in ({}, {'Origin': base},
                        {'Origin': 'http://evil.test', TOKEN_HEADER: server.token},
                        {'Origin': base, TOKEN_HEADER: 'wrong'}):
            status, _, _ = await self.request('POST', '/api/page/made_up', base=base,
                                              headers=headers, json={})
            self.assertEqual(status, 403, headers)
        self.assertEqual(calls, [])
        status, _, body = await self.request('POST', '/api/page/made_up', base=base,
                                             headers=self.auth(server, base), json={})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['data'], {'called': True})
        self.assertEqual(calls, [1])

    async def test_path_parameters_arrive_as_keywords(self):
        seen = []

        async def made_up(session=None, entry_id=None):
            seen.append((session, entry_id))
            return {'status': 'ok', 'data': {'session': session, 'entry_id': entry_id}}

        routes = panel_api.aiohttp_routes([
            (panel_api.PREFIX + 'page/memory/delete/<path:session>/<entry_id>', made_up,
             ['POST'], 'made up')])
        server, base = await self.start(api_routes=routes)
        status, _, body = await self.request(
            'POST', '/api/page/memory/delete/default/abc%2F1', base=base,
            headers=self.auth(server, base), json={})
        self.assertEqual(status, 200)
        self.assertEqual(seen, [('default', 'abc/1')])
        self.assertEqual(json.loads(body)['data'], {'session': 'default', 'entry_id': 'abc/1'})

    async def test_query_arguments_take_the_first_value(self):
        seen = []

        async def made_up():
            from quart import request
            seen.append(request.args.get('q'))
            return {'status': 'ok', 'data': {'q': request.args.get('q')}}

        routes = panel_api.aiohttp_routes([
            (panel_api.PREFIX + 'page/brain/search', made_up, ['GET'], 'made up')])
        server, base = await self.start(api_routes=routes)
        query = urlencode([('q', '编造'), ('q', '第二个')])
        status, _, body = await self.request('GET', '/api/page/brain/search?' + query, base=base)
        self.assertEqual(status, 200)
        self.assertEqual(seen, ['编造'])
        self.assertEqual(json.loads(body)['data'], {'q': '编造'})

    async def test_the_method_is_the_requests_own(self):
        seen = []

        async def made_up():
            from quart import request
            seen.append(request.method)
            return {'status': 'ok', 'data': {'method': request.method}}

        routes = panel_api.aiohttp_routes([
            (panel_api.PREFIX + 'page/made_up', made_up, ['GET', 'POST'], 'made up')])
        server, base = await self.start(api_routes=routes)
        self.assertEqual((await self.request('GET', '/api/page/made_up', base=base))[0], 200)
        self.assertEqual((await self.request('POST', '/api/page/made_up', base=base,
                                             headers=self.auth(server, base), json={}))[0], 200)
        self.assertEqual(seen, ['GET', 'POST'])

    async def test_bodies_are_read_per_request(self):
        async def made_up():
            from quart import request
            first = await request.get_json(silent=True)
            await asyncio.sleep(0.05)   # both requests are in the handler at the same time
            again = await request.get_json(silent=True)
            return {'status': 'ok', 'data': {'body': first, 'again': again}}

        routes = panel_api.aiohttp_routes([
            (panel_api.PREFIX + 'page/made_up', made_up, ['GET', 'POST'], 'made up')])
        server, base = await self.start(api_routes=routes)
        good = self.auth(server, base)
        status, _, body = await self.request('POST', '/api/page/made_up', base=base,
                                             headers=good, data=b'not json')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['data'], {'body': None, 'again': None})
        first, second = await asyncio.gather(
            self.request('POST', '/api/page/made_up', base=base, headers=good,
                         json={'who': 'first'}),
            self.request('POST', '/api/page/made_up', base=base, headers=good,
                         json={'who': 'second'}))
        self.assertEqual(json.loads(first[2])['data'],
                         {'body': {'who': 'first'}, 'again': {'who': 'first'}})
        self.assertEqual(json.loads(second[2])['data'],
                         {'body': {'who': 'second'}, 'again': {'who': 'second'}})

    async def test_a_failing_handler_becomes_a_500_without_its_words(self):
        async def made_up():
            raise RuntimeError('made-up failure text')

        routes = panel_api.aiohttp_routes([
            (panel_api.PREFIX + 'page/made_up', made_up, ['POST'], 'made up')])
        server, base = await self.start(api_routes=routes)
        status, _, body = await self.request('POST', '/api/page/made_up', base=base,
                                             headers=self.auth(server, base), json={})
        self.assertEqual(status, 500)
        self.assertEqual(body, '')
        self.assertNotIn('made-up', body)
        self.assertNotIn('failure', body)

    async def test_max_body(self):
        calls = []

        async def made_up():
            calls.append(1)
            return {'status': 'ok', 'data': {'reached': True}}

        routes = panel_api.aiohttp_routes([
            (panel_api.PREFIX + 'page/made_up', made_up, ['POST'], 'made up')])
        small, small_base = await self.start(api_routes=routes)
        big, big_base = await self.start(api_routes=routes, max_body=4 * 1024 * 1024)
        payload = {'blob': 'x' * (2 * 1024 * 1024)}
        status, _, _ = await self.request('POST', '/api/page/made_up', base=small_base,
                                          headers=self.auth(small, small_base), json=payload)
        self.assertEqual(status, 413)
        self.assertEqual(calls, [])
        status, _, body = await self.request('POST', '/api/page/made_up', base=big_base,
                                             headers=self.auth(big, big_base), json=payload)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['data'], {'reached': True})
        self.assertEqual(calls, [1])


@unittest.skipUnless(HAS_AIOHTTP, 'aiohttp is required')
class StaticPages(unittest.IsolatedAsyncioTestCase):
    """The panel page and its files, served from the root folder."""

    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'web'
        dash = self.root / 'dashboard'
        dash.mkdir(parents=True)
        (self.root / 'index.html').write_text('<html><head></head><body>panel</body></html>',
                                              encoding='utf-8')
        (dash / 'index.html').write_text('<html><head></head><body>dash</body></html>',
                                         encoding='utf-8')
        (dash / 'app.js').write_text('dash app', encoding='utf-8')
        (self.root / 'empty').mkdir()
        self.keys = KeyStore(Path(self.tmp.name) / 'keys.json')
        self.client = ClientSession()
        self.addAsyncCleanup(self.client.close)
        self.server = PanelServer(root=self.root, keys=self.keys, start_page='dashboard/')
        self.port = await self.server.start()
        self.addAsyncCleanup(self.server.stop)
        self.base = 'http://127.0.0.1:%d' % self.port

    async def request(self, path, **kwargs):
        async with self.client.get(URL(self.base + path, encoded=True), **kwargs) as response:
            return response.status, dict(response.headers), await response.text()

    async def test_the_root_sends_the_panel_page(self):
        status, headers, _ = await self.request('/', allow_redirects=False)
        self.assertEqual((status, headers['Location']), (302, '/static/dashboard/'))

    async def test_a_folder_serves_its_index_with_the_token(self):
        status, _, body = await self.request('/static/dashboard/')
        self.assertEqual(status, 200)
        meta = TOKEN_META % self.server.token
        self.assertIn(meta, body)
        self.assertLess(body.index(meta), body.index('</head>'))
        self.assertNotIn(self.server.token,
                         (self.root / 'dashboard' / 'index.html').read_text(encoding='utf-8'))
        status, _, body = await self.request('/static/dashboard/index.html')
        self.assertEqual(status, 200)
        self.assertIn(meta, body)

    async def test_other_static_files_and_missing_ones(self):
        self.assertEqual((await self.request('/static/dashboard/app.js'))[2], 'dash app')
        for path in ('/static/', '/static/empty/', '/static/nothing/'):
            self.assertEqual((await self.request(path))[0], 404, path)


class Sources(unittest.TestCase):
    """The two new parts stand alone: no AstrBot, and no cross-origin access."""

    def test_panel_api_offers_the_three_parts(self):
        tree = ast.parse((ROOT / 'panel_api.py').read_text(encoding='utf-8'))
        names = {node.name for node in tree.body
                 if isinstance(node, (ast.ClassDef, ast.FunctionDef))}
        self.assertTrue({'RouteCollector', 'install_request_shim', 'aiohttp_routes'} <= names, names)

    def test_panel_api_imports_no_astrbot(self):
        tree = ast.parse((ROOT / 'panel_api.py').read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotEqual(alias.name.split('.')[0], 'astrbot')
            if isinstance(node, ast.ImportFrom):
                self.assertNotEqual((node.module or '').split('.')[0], 'astrbot')

    def test_panel_server_says_no_to_cross_origin(self):
        source = (ROOT / 'panel_server.py').read_text(encoding='utf-8')
        self.assertNotIn('Access-Control-Allow', source)


if __name__ == '__main__':
    unittest.main()
