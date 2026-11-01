"""Offline browser and wiring checks: no browser, model or network."""
import asyncio
import ast
import concurrent.futures
import json
import signal
import socket
import sys
import tempfile
import threading
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'tests' / 'stubs'))
import test_basics  # noqa: E402,F401
import browse
import mixin_browse
import mixin_selfie
import mixin_attention
import real_browser
import vision

URL = 'https://example.com/page'
PUBLIC = '93.184.216.34'


def resolver(host, port):
    addresses = {'example.com': PUBLIC, 'private.example.com': '10.0.0.1'}
    if host not in addresses:
        raise socket.gaierror()
    return [(socket.AF_INET, socket.SOCK_STREAM, 0, '', (addresses[host], 0))]


def check(url):
    return browse.check_url(url)


class Route:
    def __init__(self, url=URL, method='GET', status=200):
        self.request = types.SimpleNamespace(url=url, method=method)
        self.result = None
        self.response = FakeResponse(url, status)
        self.fetch_args = None

    async def abort(self):
        self.result = 'abort'

    async def continue_(self):
        self.result = 'continue'

    async def fetch(self, **kwargs):
        self.fetch_args = kwargs
        return self.response

    def transfer(self):
        return self.response

    async def fulfill(self, response=None, **kwargs):
        self.result = 'fulfill'
        self.fulfilled_response = response or FakeResponse(self.request.url, kwargs['status'], kwargs['headers'])


class FakeResponse:
    def __init__(self, url=URL, status=200, headers=None):
        self.url, self.status, self.headers = url, status, headers or {}
        self.disposed = False

    async def dispose(self):
        self.disposed = True


class FakeRequest:
    def __init__(self):
        self.calls, self.responses = [], {}

    async def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.get(url, FakeResponse(url))


class FakePage:
    def __init__(self, ctx):
        self.ctx, self.url, self.handlers = ctx, URL, {}
        self.closed = False

    def on(self, name, callback):
        self.handlers[name] = callback

    async def close(self):
        self.closed = True

    async def goto(self, url, **kwargs):
        self.ctx.goto_args = kwargs
        self.ctx.goto_url = url
        self.ctx.main_route = Route(url, status=self.ctx.main_route_status)
        self.ctx.active_route = self.ctx.main_route
        await self.ctx.route_handler(self.ctx.main_route)
        if self.ctx.main_route.result == 'abort':
            return None
        for route in self.ctx.routes:
            self.ctx.active_route = route
            await self.ctx.route_handler(route)
        for address in self.ctx.responses:
            response = FakeResponse(address) if isinstance(address, str) else address
            route = Route(response.url, status=response.status)
            route.response = response
            self.ctx.active_route = route
            await self.ctx.route_handler(route)
            if route.result == 'abort':
                return None
        if self.ctx.popup:
            self.ctx.handlers['page'](self.ctx.popup)
        if self.ctx.dialog:
            self.handlers['dialog'](self.ctx.dialog)
        self.url = self.ctx.final_url or url
        if self.ctx.fail:
            raise TimeoutError()
        return (self.ctx.main_route.fulfilled_response if self.ctx.main_response is self.ctx.default_response
                else self.ctx.main_response)

    async def wait_for_load_state(self, state, **kwargs):
        self.ctx.settle_args = (state, kwargs)
        if self.ctx.settle_timeout:
            raise TimeoutError()
        if self.ctx.settled_body is not None:
            self.ctx.body = self.ctx.settled_body

    async def title(self):
        return 'Example'

    def locator(self, selector):
        assert selector == 'body'
        return self

    async def inner_text(self, **kwargs):
        return self.ctx.body

    async def content(self):
        self.ctx.content_calls += 1
        return self.ctx.html

    async def screenshot(self, **kwargs):
        self.ctx.shot_args = kwargs
        Path(kwargs['path']).write_bytes(b'fictional jpeg')


class FakeDialog:
    def __init__(self):
        self.dismissed = False

    async def dismiss(self):
        self.dismissed = True


class FakeContext:
    def __init__(self):
        self.handlers, self.routes, self.responses = {}, [], []
        self.final_url, self.body = None, 'readable words'
        self.html, self.content_calls = '<html>page</html>', 0
        self.request = FakeRequest()
        self.main_response = FakeResponse()
        self.default_response = self.main_response
        self.main_route_status = 200
        self.settle_timeout, self.settled_body = False, None
        self.popup = self.dialog = None
        self.closed = self.fail = False
        self.page = FakePage(self)

    def transfer(self, url, address, headers, proxy=None, deadline=None):
        self.request.calls.append((url, {'address': address, 'proxy': proxy}))
        response = self.request.responses.get(url)
        if response is None:
            route = getattr(self, 'active_route', None)
            response = route.transfer() if route and route.request.url == url else FakeResponse(url)
        response.disposed = True
        return response.status, response.headers, b'fictional response'

    async def route(self, pattern, handler):
        self.pattern, self.route_handler = pattern, handler

    async def route_web_socket(self, pattern, handler):
        self.ws_pattern, self.ws_handler = pattern, handler

    async def add_init_script(self, script):
        self.init_script = script

    async def new_page(self):
        return self.page

    def on(self, name, callback):
        self.handlers[name] = callback

    async def unroute_all(self, **kwargs):
        self.unroute_args = kwargs

    async def close(self):
        self.closed = True


class FakePlaywright:
    def __init__(self):
        self.chromium = self
        self.context = FakeContext()
        self.closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def launch(self, **kwargs):
        self.launch_args = kwargs
        return self

    async def new_context(self, **kwargs):
        self.context_args = kwargs
        return self.context

    async def close(self):
        self.closed = True


class Offline(unittest.TestCase):
    def setUp(self):
        # Windows' asyncio wake-up socketpair uses loopback. No test needs it:
        # fake transports run inline and never wake the loop from another thread.
        async def inline(fn, *args, **kwargs):
            return fn(*args, **kwargs)
        patcher = mock.patch.object(asyncio, 'to_thread', new=inline)
        patcher.start()
        self.addCleanup(patcher.stop)
        if sys.platform == 'win32':
            def make_pipe(loop):
                loop._ssock = mock.Mock()
                loop._csock = mock.Mock()
                loop._csock.fileno.return_value = -1
            patcher = mock.patch.object(asyncio.ProactorEventLoop, '_make_self_pipe', new=make_pipe)
            patcher.start()
            self.addCleanup(patcher.stop)
            patcher = mock.patch.object(signal, 'set_wakeup_fd', return_value=-1)
            patcher.start()
            self.addCleanup(patcher.stop)
            for name in ('_close_self_pipe', '_write_to_self', '_loop_self_reading'):
                patcher = mock.patch.object(asyncio.ProactorEventLoop, name, return_value=None)
                patcher.start()
                self.addCleanup(patcher.stop)
        for target, name in ((socket, 'getaddrinfo'), (socket, 'create_connection'),
                             (socket.socket, 'connect'), (socket.socket, 'connect_ex')):
            patcher = mock.patch.object(target, name, side_effect=AssertionError('real network is forbidden'))
            guard = patcher.start()
            self.addCleanup(patcher.stop)
            self.addCleanup(guard.assert_not_called)


class Browser(Offline):
    def setUp(self):
        super().setUp()
        proxy_patch = mock.patch.object(real_browser, 'getproxies', return_value={})
        proxy_patch.start()
        self.addCleanup(proxy_patch.stop)
        bypass_patch = mock.patch.object(real_browser, 'proxy_bypass', return_value=False)
        bypass_patch.start()
        self.addCleanup(bypass_patch.stop)
        async def inline_fetch(url, headers, check):
            return real_browser._fetch_checked(url, headers, check)
        fetch_patch = mock.patch.object(real_browser, '_fetch_page', new=inline_fetch)
        fetch_patch.start()
        self.addCleanup(fetch_patch.stop)

    def run_browser(self, fake, shot=None, on_block=None, extractor=None, url=URL):
        api = types.ModuleType('playwright.async_api')
        api.async_playwright = lambda: fake
        api.TimeoutError = TimeoutError
        package = types.ModuleType('playwright')
        package.__path__ = []
        with mock.patch.dict(sys.modules, {'playwright': package, 'playwright.async_api': api,
                                           'trafilatura': extractor}), \
             mock.patch.object(real_browser, '_resolve_addresses', side_effect=lambda host: [resolver(host, None)[0][4][0]]), \
             mock.patch.object(real_browser, '_pinned_get', side_effect=fake.context.transfer), \
             mock.patch.object(Route, 'fetch', side_effect=AssertionError('browser fetch is forbidden')), \
             mock.patch.object(FakeRequest, 'get', side_effect=AssertionError('browser request is forbidden')):
            task = (real_browser.screenshot(url, check, shot, on_block=on_block) if shot is not None else
                    real_browser.read_page(url, check, on_block=on_block))
            return asyncio.run(task)

    def test_shared_launch_closes_resources_when_setup_fails(self):
        fake = FakePlaywright()
        fake.context.add_init_script = mock.AsyncMock(side_effect=RuntimeError('setup failed'))
        with self.assertRaises(RuntimeError):
            asyncio.run(real_browser._launch_browser(fake))
        self.assertTrue(fake.context.closed and fake.closed)

    def test_context_uses_system_https_proxy_and_bypass(self):
        fake = FakePlaywright()
        proxies = {'https': 'http://proxy.example.test', 'http': 'http://other.example.test',
                   'no': 'localhost; .example.test'}
        with mock.patch.object(real_browser, 'getproxies', return_value=proxies):
            self.assertIsNotNone(self.run_browser(fake))
        self.assertNotIn('proxy', fake.context_args)
        self.assertEqual(fake.context.request.calls[0][1]['proxy'], proxies['https'])

    def test_context_uses_http_proxy_or_omits_proxy(self):
        fake = FakePlaywright()
        with mock.patch.object(real_browser, 'getproxies', return_value={'http': 'http://proxy.example.test'}):
            self.assertIsNotNone(self.run_browser(fake))
        self.assertNotIn('proxy', fake.context_args)
        self.assertEqual(fake.context.request.calls[0][1]['proxy'], 'http://proxy.example.test')
        fake = FakePlaywright()
        self.assertIsNotNone(self.run_browser(fake))
        self.assertNotIn('proxy', fake.context_args)

    def test_proxy_does_not_bypass_page_address_checks(self):
        fake = FakePlaywright()
        fake.context.routes = [Route('https://private.example.com/')]
        with mock.patch.object(real_browser, 'getproxies', return_value={'https': 'http://proxy.example.test'}):
            self.assertIsNotNone(self.run_browser(fake))
        self.assertEqual(fake.context.routes[0].result, 'abort')

    def test_proxy_lookup_failure_keeps_browser_available(self):
        fake = FakePlaywright()
        with mock.patch.object(real_browser, 'getproxies', side_effect=OSError('unavailable')):
            self.assertIsNotNone(self.run_browser(fake))
        self.assertNotIn('proxy', fake.context_args)

    def test_unsupported_proxy_logs_only_protocol_and_never_connects(self):
        fake = FakePlaywright()
        proxy = 'socks5://fictional-user:fictional-password@proxy.invalid'
        with mock.patch.object(real_browser, 'getproxies', return_value={'https': proxy}), \
             self.assertLogs(real_browser.logger, level='INFO') as logs:
            self.assertIsNone(self.run_browser(fake))
        text = '\n'.join(logs.output)
        self.assertIn('unsupported proxy protocol (socks5)', text)
        for secret in (proxy, 'fictional-user', 'fictional-password', 'proxy.invalid'):
            self.assertNotIn(secret, text)
        self.assertEqual(fake.context.request.calls, [])
        self.assertEqual(fake.context.main_route.result, 'abort')

    def test_no_proxy_uses_checked_ip_without_proxy(self):
        fake = FakePlaywright()
        with mock.patch.object(real_browser, 'getproxies', return_value={
                'https': 'http://proxy.invalid', 'no': 'example.com'}), \
             mock.patch.object(real_browser, 'proxy_bypass', return_value=True) as bypass:
            self.assertIsNotNone(self.run_browser(fake))
        bypass.assert_called_once_with('example.com')
        self.assertEqual(fake.context.request.calls, [(URL, {'address': PUBLIC, 'proxy': None})])

    def test_proxy_address_is_not_logged_on_browser_error(self):
        fake = FakePlaywright()
        address = 'http://proxy.example.test'
        fake.context.add_init_script = mock.AsyncMock(side_effect=RuntimeError(address))
        with mock.patch.object(real_browser, 'getproxies', return_value={'https': address}), \
             self.assertLogs(real_browser.logger, level='INFO') as logs:
            self.assertIsNone(self.run_browser(fake))
        self.assertNotIn(address, '\n'.join(logs.output))

    def test_article_extraction_uses_html_and_preserves_title(self):
        fake = FakePlaywright()
        fake.context.body = 'visible ' * 40
        extractor = types.SimpleNamespace(extract=mock.Mock(return_value='article ' * 30))
        result = self.run_browser(fake, extractor=extractor)
        self.assertEqual((result['title'], result['text']), ('Example', 'article ' * 30))
        extractor.extract.assert_called_once_with(fake.context.html, include_comments=False,
                                                  include_tables=True, favor_precision=True)

    def test_article_extraction_falls_back_for_empty_short_error_and_missing(self):
        for extracted in (None, '', 'short', 'a' * 200, RuntimeError('failed')):
            with self.subTest(extracted=extracted):
                fake = FakePlaywright()
                fake.context.body = 'visible ' * 200
                method = mock.Mock(side_effect=extracted) if isinstance(extracted, Exception) else mock.Mock(return_value=extracted)
                result = self.run_browser(fake, extractor=types.SimpleNamespace(extract=method))
                self.assertEqual(result['text'], fake.context.body)
        fake = FakePlaywright()
        self.assertEqual(self.run_browser(fake)['text'], fake.context.body)

    def test_article_extraction_timeout_falls_back(self):
        fake = FakePlaywright()
        original = asyncio.to_thread
        async def slow_thread(*args, **kwargs):
            if args[0] is real_browser._fetch_checked:
                return await original(*args, **kwargs)
            await asyncio.sleep(1)
        with mock.patch.object(real_browser, 'EXTRACT_SECONDS', 0.01), \
             mock.patch.object(real_browser.asyncio, 'to_thread', side_effect=slow_thread):
            result = self.run_browser(fake, extractor=types.SimpleNamespace(extract=mock.Mock()))
        self.assertEqual(result['text'], fake.context.body)

    def test_article_html_is_limited_by_utf8_bytes(self):
        fake = FakePlaywright()
        fake.context.html = 'a' * (real_browser.HTML_MAX_BYTES - 1) + '中文字'
        extractor = types.SimpleNamespace(extract=mock.Mock(return_value='article ' * 30))
        self.run_browser(fake, extractor=extractor)
        html = extractor.extract.call_args.args[0]
        self.assertEqual(html, 'a' * (real_browser.HTML_MAX_BYTES - 1))
        self.assertLessEqual(len(html.encode('utf-8')), real_browser.HTML_MAX_BYTES)

    def test_article_extraction_only_on_read_not_screenshot(self):
        extractor = types.SimpleNamespace(extract=mock.Mock(return_value='article ' * 30))
        fake = FakePlaywright()
        self.run_browser(fake, extractor=extractor)
        self.assertEqual(fake.context.content_calls, 1)
        extractor.extract.assert_called_once()
        fake = FakePlaywright()
        extractor.extract.reset_mock()
        with tempfile.TemporaryDirectory() as tmp:
            self.run_browser(fake, Path(tmp) / 'shot.jpg', extractor=extractor)
        self.assertEqual(fake.context.content_calls, 0)
        extractor.extract.assert_not_called()

    def test_trafilatura_never_fetches_or_extracts_from_url(self):
        forbidden = ('fetch_' + 'url', 'fetch_' + 'response', 'trafilatura.' + 'downloads')
        for path in ROOT.rglob('*.py'):
            if any(part in ('.git', 'venv', '.venv') for part in path.parts):
                continue
            source = path.read_text('utf-8')
            for word in forbidden:
                self.assertNotIn(word, source, str(path))
            tree = ast.parse(source, filename=str(path))
            modules = set()
            functions = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules.update(alias.asname or alias.name for alias in node.names if alias.name == 'trafilatura')
                elif isinstance(node, ast.ImportFrom) and node.module == 'trafilatura':
                    functions.update(alias.asname or alias.name for alias in node.names
                                     if alias.name in ('extract', 'bare_extraction'))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                fn = node.func
                direct = isinstance(fn, ast.Name) and fn.id in functions
                member = (isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name)
                          and fn.value.id in modules and fn.attr in ('extract', 'bare_extraction'))
                if direct or member:
                    self.assertLessEqual(len(node.args), 1, str(path))
                    self.assertFalse(any(k.arg is None or k.arg == 'url' for k in node.keywords), str(path))

    def test_launch_and_context_are_temporary_and_sandboxed(self):
        fake = FakePlaywright()
        self.assertEqual(self.run_browser(fake)['text'], 'readable words')
        self.assertEqual(fake.launch_args, {'channel': 'msedge', 'headless': True, 'chromium_sandbox': True,
                                            'args': ['--disable-features=DnsOverHttps',
                                                     '--force-webrtc-ip-handling-policy=disable_non_proxied_udp',
                                                     '--host-resolver-rules=MAP * ~NOTFOUND']})
        self.assertEqual(fake.context_args, {'accept_downloads': False, 'permissions': [], 'service_workers': 'block',
                                             'ignore_https_errors': False, 'bypass_csp': False})
        self.assertEqual(fake.context.pattern, '**/*')
        self.assertEqual(fake.context.ws_pattern, '**/*')
        self.assertEqual(fake.context.goto_args['timeout'], 20000)
        self.assertTrue(fake.closed and fake.context.closed)

    def test_request_method_and_public_addresses(self):
        fake = FakePlaywright()
        fake.context.routes = [Route(), Route(method='HEAD'), Route(method='POST'),
                               Route('http://127.0.0.1/'), Route('https://private.example.com/'),
                               Route('https://missing.example.com/')]
        self.run_browser(fake)
        self.assertEqual([r.result for r in fake.context.routes],
                         ['fulfill', 'abort', 'abort', 'abort', 'abort', 'abort'])

    def test_subrequest_fetch_error_is_counted_and_page_is_read(self):
        class Error(Exception):
            pass
        fake = FakePlaywright()
        route = Route('https://example.com/image')
        route.transfer = mock.Mock(side_effect=Error('fictional connection failure'))
        fake.context.routes = [route]
        counts = []
        with self.assertLogs(real_browser.logger, level='INFO') as logs:
            result = self.run_browser(fake, on_block=counts.append)
        self.assertEqual(result['text'], 'readable words')
        self.assertEqual(route.result, 'abort')
        self.assertEqual(counts, [1])
        self.assertEqual(len(logs.output), 1)
        self.assertIn('request failed (Error)', logs.output[0])
        self.assertNotIn('fictional connection failure', logs.output[0])

    def test_main_request_fetch_error_returns_no_page(self):
        class Error(Exception):
            pass
        def fail_fetch(route):
            raise Error('fictional connection failure')
        fake = FakePlaywright()
        counts = []
        with mock.patch.object(Route, 'transfer', new=fail_fetch):
            self.assertIsNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual(fake.context.main_route.result, 'abort')
        self.assertEqual(counts, [1])

    def test_request_failure_and_abort_failure_do_not_escape(self):
        class Error(Exception):
            pass
        fake = FakePlaywright()
        route = Route('https://example.com/image')
        route.transfer = mock.Mock(side_effect=Error('fetch detail'))
        route.abort = mock.AsyncMock(side_effect=Error('abort detail'))
        fake.context.routes = [route]
        counts = []
        with self.assertLogs(real_browser.logger, level='INFO') as logs:
            result = self.run_browser(fake, on_block=counts.append)
        self.assertEqual(result['text'], 'readable words')
        self.assertEqual(counts, [1])
        self.assertEqual(route.abort.await_count, 1)
        self.assertEqual(len(logs.output), 1)
        self.assertNotIn('fetch detail', logs.output[0])
        self.assertNotIn('abort detail', logs.output[0])

    def test_subrequest_fulfill_timeout_and_programming_error_are_contained(self):
        for phase, error in (('fulfill', TimeoutError('fictional timeout')),
                             ('transfer', TypeError('fictional coding error'))):
            with self.subTest(phase=phase):
                fake = FakePlaywright()
                route = Route('https://example.com/resource')
                setattr(route, phase, (mock.Mock if phase == 'transfer' else mock.AsyncMock)(side_effect=error))
                fake.context.routes = [route]
                counts = []
                with self.assertLogs(real_browser.logger, level='INFO') as logs:
                    result = self.run_browser(fake, on_block=counts.append)
                self.assertEqual(result['text'], 'readable words')
                self.assertEqual(route.result, 'abort')
                self.assertEqual(counts, [1])
                self.assertEqual(len(logs.output), 1)
                self.assertIn(type(error).__name__, logs.output[0])

    def test_failed_abort_of_blocked_request_is_counted_once(self):
        fake = FakePlaywright()
        route = Route('https://example.com/resource', method='POST')
        route.abort = mock.AsyncMock(side_effect=RuntimeError('fictional abort'))
        fake.context.routes = [route]
        counts = []
        with self.assertLogs(real_browser.logger, level='INFO') as logs:
            result = self.run_browser(fake, on_block=counts.append)
        self.assertEqual(result['text'], 'readable words')
        self.assertEqual(counts, [1])
        self.assertEqual(route.abort.await_count, 2)
        self.assertEqual(sum('request failed (RuntimeError)' in line for line in logs.output), 1)

    def test_main_redirect_to_private_is_checked_before_request(self):
        fake = FakePlaywright()
        target = 'http://127.0.0.1/'
        fake.context.request.responses[URL] = FakeResponse(URL, 302, {'location': target})
        counts = []
        self.assertIsNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual([url for url, _ in fake.context.request.calls], [URL])
        self.assertEqual(counts, [1])
        self.assertEqual(fake.context.main_route.result, 'abort')
        self.assertTrue(fake.context.closed and fake.closed)
        fake = FakePlaywright()
        fake.context.request.responses[URL] = FakeResponse(URL, 302, {'location': target})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'shot.jpg'
            self.assertIsNone(self.run_browser(fake, path))
            self.assertFalse(path.exists())
            self.assertEqual([url for url, _ in fake.context.request.calls], [URL])

    def test_main_public_redirect_is_followed_only_after_check(self):
        fake = FakePlaywright()
        target = 'https://example.com/next'
        fake.context.request.responses[URL] = FakeResponse(URL, 302, {'location': '/next'})
        result = self.run_browser(fake)
        self.assertEqual(result['url'], target)
        self.assertEqual([url for url, _ in fake.context.request.calls], [URL, target])
        self.assertTrue(all(kw['address'] == PUBLIC for _, kw in fake.context.request.calls))
        self.assertEqual(fake.context.goto_url, URL)
        self.assertEqual(fake.context.main_route.result, 'fulfill')
        self.assertIsNone(fake.context.main_route.fetch_args)

    def test_main_redirect_limit_and_loop(self):
        for redirects in (real_browser.MAX_HOPS, real_browser.MAX_HOPS + 1):
            with self.subTest(redirects=redirects):
                fake = FakePlaywright()
                urls = [URL] + ['https://example.com/hop%d' % n for n in range(redirects)]
                for current, following in zip(urls, urls[1:]):
                    fake.context.request.responses[current] = FakeResponse(current, 302, {'location': following})
                result = self.run_browser(fake)
                if redirects == real_browser.MAX_HOPS:
                    self.assertEqual(result['url'], urls[-1])
                    self.assertEqual(fake.context.goto_url, URL)
                else:
                    self.assertIsNone(result)
                    self.assertEqual(fake.context.main_route.result, 'abort')
                self.assertEqual(len(fake.context.request.calls), real_browser.MAX_HOPS + 1)
        fake = FakePlaywright()
        fake.context.request.responses[URL] = FakeResponse(URL, 302, {'location': URL})
        self.assertIsNone(self.run_browser(fake))
        self.assertEqual(len(fake.context.request.calls), real_browser.MAX_HOPS + 1)
        fake = FakePlaywright()
        fake.context.request.responses[URL] = FakeResponse(URL, 302)
        self.assertIsNone(self.run_browser(fake))
        self.assertEqual(fake.context.main_route.result, 'abort')

    def test_route_fetch_aborts_redirects_and_fulfills_other_responses(self):
        fake = FakePlaywright()
        fake.context.routes = [Route(status=302), Route(status=200), Route(status=404), Route(method='POST')]
        counts = []
        self.assertIsNotNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual([r.result for r in fake.context.routes], ['abort', 'fulfill', 'fulfill', 'abort'])
        self.assertEqual(counts, [2])
        for route in fake.context.routes[:3]:
            self.assertIsNone(route.fetch_args)
            self.assertTrue(route.response.disposed)
        self.assertIsNone(fake.context.routes[-1].fetch_args)

    def test_route_source_never_continues_unchecked(self):
        async def exercise():
            for url, result in (('data:text/plain,sample', 'continue'), ('blob:https://example.com/id', 'continue'),
                                ('ws://example.com/', 'abort'), ('javascript:example', 'abort')):
                route = Route(url)
                await real_browser._pinned_route(route, lambda reason: None, [0])
                self.assertEqual(route.result, result)
        asyncio.run(exercise())

    def test_main_route_redirect_after_preflight_is_aborted(self):
        fake = FakePlaywright()
        fake.context.main_route_status = 302
        counts = []
        self.assertIsNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual(fake.context.main_route.result, 'abort')
        self.assertIsNone(fake.context.main_route.fetch_args)
        self.assertEqual(counts, [1])

    def test_webrtc_disabled_and_local_network_protection_preserved(self):
        fake = FakePlaywright()
        self.run_browser(fake)
        args = fake.launch_args['args']
        self.assertIn('--force-webrtc-ip-handling-policy=disable_non_proxied_udp', args)
        self.assertFalse(any('PrivateNetworkAccess' in arg or 'LocalNetworkAccess' in arg for arg in args))
        self.assertIn('RTCPeerConnection', fake.context.init_script)
        self.assertIn('webkitRTCPeerConnection', fake.context.init_script)
        self.assertIn('value: undefined', fake.context.init_script)

    def test_strict_check_rejects_private_dns_even_when_check_allows(self):
        with mock.patch.object(real_browser.socket, 'getaddrinfo', side_effect=resolver):
            ok, reason = real_browser._strict_url('https://private.example.com/', lambda url: (True, ''))
        self.assertFalse(ok)
        self.assertEqual(reason, 'local address')

    def test_response_redirect_to_local_is_rejected(self):
        fake = FakePlaywright()
        fake.context.responses = ['http://127.0.0.1/']
        self.assertIsNone(self.run_browser(fake))
        self.assertTrue(fake.closed and fake.context.closed)

    def test_redirect_location_to_local_is_rejected_without_followup_request(self):
        for status in (301, 302):
            with self.subTest(status=status):
                fake = FakePlaywright()
                fake.context.responses = [FakeResponse(URL, status, {'location': 'http://127.0.0.1/'})]
                self.assertIsNone(self.run_browser(fake))
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / 'shot.jpg'
                    self.assertIsNone(self.run_browser(fake, path))
                    self.assertFalse(path.exists())

    def test_relative_redirect_location_is_resolved_and_allowed(self):
        fake = FakePlaywright()
        fake.context.responses = [FakeResponse(URL, 302, {'location': '/next'})]
        self.assertEqual(self.run_browser(fake)['text'], 'readable words')

    def test_missing_or_error_main_response_is_rejected(self):
        for response in (None, FakeResponse(status=404), FakeResponse(status=500), FakeResponse(status=302)):
            with self.subTest(response=response):
                fake = FakePlaywright()
                fake.context.main_response = response
                self.assertIsNone(self.run_browser(fake))
                self.assertTrue(fake.context.closed and fake.closed)

    def test_browser_error_url_is_rejected(self):
        fake = FakePlaywright()
        fake.context.final_url = 'chrome-error://chromewebdata/'
        self.assertIsNone(self.run_browser(fake))

    def test_fragment_does_not_hide_fetched_document(self):
        for address in (URL, URL + '#section'):
            fake = FakePlaywright()
            fake.context.final_url = URL + '#another-section'
            self.assertEqual(self.run_browser(fake, url=address)['text'], 'readable words')

    def test_response_encoding_is_removed_before_fulfill(self):
        fake = FakePlaywright()
        fake.context.request.responses[URL] = FakeResponse(URL, headers={'Content-Encoding': 'gzip'})
        self.assertIsNotNone(self.run_browser(fake))
        self.assertNotIn('Content-Encoding', fake.context.main_route.fulfilled_response.headers)

    def test_networkidle_timeout_still_reads_page(self):
        fake = FakePlaywright()
        fake.context.settle_timeout = True
        self.assertEqual(self.run_browser(fake)['text'], 'readable words')
        self.assertEqual(fake.context.settle_args, ('networkidle', {'timeout': 8000}))
        fake = FakePlaywright()
        fake.context.settle_timeout = True
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'shot.jpg'
            self.assertEqual(self.run_browser(fake, path), path)

    def test_networkidle_waits_for_script_content_and_screenshot(self):
        fake = FakePlaywright()
        fake.context.body, fake.context.settled_body = '', 'script content'
        self.assertEqual(self.run_browser(fake)['text'], 'script content')
        fake = FakePlaywright()
        fake.context.body, fake.context.settled_body = '', 'script content'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'shot.jpg'
            self.assertEqual(self.run_browser(fake, path), path)
            self.assertEqual(fake.context.settle_args, ('networkidle', {'timeout': 8000}))

    def test_empty_body_is_not_read_or_screenshot(self):
        for body in ('', ' \n\t'):
            with self.subTest(body=body):
                fake = FakePlaywright()
                fake.context.body = body
                self.assertIsNone(self.run_browser(fake))
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / 'shot.jpg'
                    self.assertIsNone(self.run_browser(fake, path))
                    self.assertFalse(path.exists())

    def test_final_redirect_to_local_is_rejected(self):
        fake = FakePlaywright()
        fake.context.final_url = 'http://127.0.0.1/'
        self.assertIsNone(self.run_browser(fake))

    def test_popup_and_dialog_are_closed(self):
        fake = FakePlaywright()
        fake.context.popup, fake.context.dialog = FakePage(fake.context), FakeDialog()
        self.run_browser(fake)
        self.assertTrue(fake.context.popup.closed)
        self.assertTrue(fake.context.dialog.dismissed)

    def test_websocket_is_closed(self):
        fake = FakePlaywright()
        self.run_browser(fake)
        closed = []
        async def close():
            closed.append(True)
        async def exercise():
            fake.context.ws_handler(types.SimpleNamespace(close=close))
            await asyncio.sleep(0)
        asyncio.run(exercise())
        self.assertEqual(closed, [True])

    def test_timeout_closes_context_and_browser(self):
        fake = FakePlaywright()
        fake.context.fail = True
        self.assertIsNone(self.run_browser(fake))
        self.assertTrue(fake.closed and fake.context.closed)

    def test_verification_page_is_not_read(self):
        fake = FakePlaywright()
        fake.context.body = 'Please verify you are human'
        self.assertIsNone(self.run_browser(fake))

    def test_short_challenge_and_long_cloudflare_article(self):
        fake = FakePlaywright()
        fake.context.body = 'Just a moment... Cloudflare'
        self.assertIsNone(self.run_browser(fake))
        fake = FakePlaywright()
        fake.context.body = 'Cloudflare ' + 'a' * real_browser.CHALLENGE_MAX_CHARS
        self.assertEqual(self.run_browser(fake)['text'], fake.context.body)

    def test_screenshot_uses_common_safety_and_viewport(self):
        fake = FakePlaywright()
        fake.context.routes = [Route(method='POST'), Route(), Route('https://private.example.com/')]
        counts = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'shot.jpg'
            self.assertEqual(self.run_browser(fake, path, counts.append), path)
            self.assertTrue(path.exists())
            self.assertEqual(fake.context.shot_args, {'path': str(path), 'type': 'jpeg', 'quality': 70,
                                                       'full_page': False, 'timeout': 10000})
        self.assertEqual(counts, [2])
        self.assertEqual([r.result for r in fake.context.routes], ['abort', 'fulfill', 'abort'])
        self.assertEqual(fake.context_args['viewport'], {'width': 390, 'height': 844})
        self.assertEqual(fake.context_args['permissions'], [])
        self.assertFalse(fake.context_args['accept_downloads'])
        self.assertEqual(fake.context_args['service_workers'], 'block')
        self.assertTrue(fake.launch_args['chromium_sandbox'])
        self.assertEqual(fake.context.ws_pattern, '**/*')
        self.assertTrue(fake.context.closed and fake.closed)

    def test_screenshot_redirect_refused_and_partial_file_removed(self):
        fake = FakePlaywright()
        fake.context.responses = ['http://127.0.0.1/']
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'shot.jpg'
            self.assertIsNone(self.run_browser(fake, path))
            self.assertFalse(path.exists())

    def test_blocked_request_count_survives_failure(self):
        fake = FakePlaywright()
        fake.context.routes = [Route(method='POST'), Route('https://missing.example.com/')]
        fake.context.fail = True
        counts = []
        self.assertIsNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual(counts, [2])

    def test_missing_playwright_returns_none(self):
        with mock.patch.dict(sys.modules, {'playwright': None, 'playwright.async_api': None}):
            self.assertIsNone(asyncio.run(real_browser.read_page(URL, check)))

    def test_one_page_at_a_time(self):
        active, maximum = [], []
        class SerialPlaywright(FakePlaywright):
            async def launch(self, **kwargs):
                active.append(self)
                maximum.append(len(active))
                await asyncio.sleep(0)
                return await super().launch(**kwargs)
            async def close(self):
                active.remove(self)
                await super().close()
        api = types.ModuleType('playwright.async_api')
        api.async_playwright = SerialPlaywright
        api.TimeoutError = TimeoutError
        package = types.ModuleType('playwright')
        package.__path__ = []
        async def exercise(path):
            return await asyncio.gather(real_browser.read_page(URL, check), real_browser.screenshot(URL, check, path))
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.dict(sys.modules, {'playwright': package, 'playwright.async_api': api}), \
             mock.patch.object(real_browser, '_resolve_addresses', side_effect=lambda host: [resolver(host, None)[0][4][0]]), \
             mock.patch.object(real_browser, '_pinned_get', side_effect=lambda *args: active[-1].context.transfer(*args)), \
             mock.patch.object(Route, 'fetch', side_effect=AssertionError('browser fetch is forbidden')), \
             mock.patch.object(FakeRequest, 'get', side_effect=AssertionError('browser request is forbidden')):
            results = asyncio.run(exercise(Path(tmp) / 'shot.jpg'))
        self.assertEqual(maximum, [1, 1])
        self.assertTrue(all(results))

    def test_source_has_no_persistent_or_debug_access(self):
        # Split the forbidden words so this test does not itself match a source scan.
        forbidden = ('launch_' + 'persistent_context', 'connect_over_' + 'cdp',
                     'user_' + 'data_dir', 'remote-' + 'debugging-port')
        for path in ROOT.rglob('*.py'):
            if any(part in ('.git', 'venv', '.venv') for part in path.parts):
                continue
            source = path.read_text('utf-8')
            for word in forbidden:
                self.assertNotIn(word, source, str(path))


class Transport(Offline):
    def connection(self):
        conn = mock.MagicMock()
        conn.sock = object()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.getheaders.return_value = [('Content-Type', 'text/plain')]
        conn.getresponse.return_value.read1.side_effect = [b'fictional page', b'']
        return conn

    def test_http_proxy_connect_and_absolute_request(self):
        for scheme in ('https', 'http'):
            with self.subTest(scheme=scheme):
                conn, tls = self.connection(), mock.MagicMock()
                sock = mock.MagicMock()
                conn.host, conn.port = '127.0.0.1', 80
                # A local proxy is allowed; only the target page is checked.
                proxy = 'http://fictional-user:fictional-password@127.0.0.1'
                with mock.patch.object(real_browser, 'getproxies', return_value={'https': proxy}), \
                     mock.patch.object(real_browser, 'proxy_bypass', return_value=False), \
                     mock.patch.object(real_browser, '_resolve_addresses', side_effect=lambda host: [PUBLIC if host == 'example.com' else '127.0.0.1']), \
                     mock.patch.object(real_browser.http.client, 'HTTPConnection', return_value=conn) as connect, \
                     mock.patch.object(real_browser.socket, 'socket', return_value=sock), \
                     mock.patch.object(real_browser.ssl, 'create_default_context', return_value=tls):
                    result = real_browser._fetch_checked(scheme + '://example.com/page#fragment', {}, check)
                connect.assert_called_once_with('127.0.0.1', 80, timeout=real_browser.OPEN_SECONDS)
                sock.connect.assert_called_once_with(('127.0.0.1', 80))
                self.assertEqual(result[0], 200)
                outgoing = conn.request.call_args.kwargs['headers']
                self.assertEqual(outgoing['Host'], 'example.com')
                if scheme == 'https':
                    conn.set_tunnel.assert_called_once()
                    self.assertEqual(conn.set_tunnel.call_args.args, ('example.com', 443))
                    self.assertIn('Proxy-Authorization', conn.set_tunnel.call_args.kwargs['headers'])
                    self.assertNotIn('Proxy-Authorization', outgoing)
                    self.assertEqual(tls.wrap_socket.call_args.kwargs['server_hostname'], 'example.com')
                    self.assertEqual(conn.request.call_args.args, ('GET', '/page'))
                else:
                    conn.set_tunnel.assert_not_called()
                    self.assertIn('Proxy-Authorization', outgoing)
                    self.assertEqual(conn.request.call_args.args, ('GET', 'http://example.com/page'))
                conn.close.assert_called_once()

    def test_direct_connection_uses_numeric_socket_host_and_tls_name(self):
        conn, sock, tls = self.connection(), mock.MagicMock(), mock.MagicMock()
        with mock.patch.object(real_browser.http.client, 'HTTPConnection', return_value=conn), \
             mock.patch.object(real_browser.socket, 'socket', return_value=sock), \
             mock.patch.object(real_browser.ssl, 'create_default_context', return_value=tls):
            real_browser._pinned_get(URL, PUBLIC, {'Host': 'wrong.invalid', 'Proxy-Authorization': 'fictional',
                                                  'accept-encoding': 'gzip, br'})
        sock.connect.assert_called_once_with((PUBLIC, 443))
        self.assertEqual(conn.request.call_args.kwargs['headers']['Host'], 'example.com')
        self.assertNotIn('Proxy-Authorization', conn.request.call_args.kwargs['headers'])
        self.assertEqual(conn.request.call_args.kwargs['headers']['Accept-Encoding'], 'identity')
        self.assertNotIn('accept-encoding', conn.request.call_args.kwargs['headers'])
        self.assertEqual(tls.wrap_socket.call_args.kwargs['server_hostname'], 'example.com')
        conn.close.assert_called_once()

    def test_tls_failure_and_oversize_response_close_connection(self):
        for failure in ('tls', 'body'):
            with self.subTest(failure=failure):
                conn, sock, tls = self.connection(), mock.MagicMock(), mock.MagicMock()
                if failure == 'tls':
                    tls.wrap_socket.side_effect = RuntimeError('fictional TLS failure')
                else:
                    conn.getresponse.return_value.read1.side_effect = [b'x' * (real_browser.HTML_MAX_BYTES + 1)]
                with mock.patch.object(real_browser.http.client, 'HTTPConnection', return_value=conn), \
                     mock.patch.object(real_browser.socket, 'socket', return_value=sock), \
                     mock.patch.object(real_browser.ssl, 'create_default_context', return_value=tls):
                    with self.assertRaises((RuntimeError, ValueError)):
                        real_browser._pinned_get(URL, PUBLIC, {})
                conn.close.assert_called_once()

    def test_other_checked_addresses_are_tried_without_resolving_again(self):
        with mock.patch.object(real_browser, '_resolve_addresses', return_value=[PUBLIC, '8.8.8.8']) as resolve, \
             mock.patch.object(real_browser, '_proxy_for', return_value=None), \
             mock.patch.object(real_browser, '_pinned_get', side_effect=[OSError('fictional refusal'), (200, {}, b'ok')]) as fetch:
            self.assertEqual(real_browser._fetch_checked(URL, {}, check)[0], 200)
        resolve.assert_called_once_with('example.com')
        self.assertEqual([call.args[1] for call in fetch.call_args_list], [PUBLIC, '8.8.8.8'])
        self.assertIs(fetch.call_args_list[0].args[4], fetch.call_args_list[1].args[4])

    def test_deadline_closes_socket_during_slow_headers(self):
        closed = threading.Event()
        conn, sock = self.connection(), mock.MagicMock()
        sock.shutdown.side_effect = lambda *args: closed.set()
        def headers():
            if not closed.wait(1):
                raise AssertionError('deadline did not close socket')
            raise OSError('fictional closed socket')
        conn.getresponse.side_effect = headers
        with mock.patch.object(real_browser, 'OPEN_SECONDS', 0.03), \
             mock.patch.object(real_browser.http.client, 'HTTPConnection', return_value=conn), \
             mock.patch.object(real_browser.socket, 'socket', return_value=sock):
            with self.assertRaises(OSError):
                real_browser._pinned_get('http://example.com/', PUBLIC, {})
        self.assertTrue(closed.is_set())
        conn.close.assert_called_once()


def run_offline_loop(coro, default_executor=None):
    """Poll worker completions without a Windows loopback wake-up socket."""
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        if default_executor is not None:
            loop.set_default_executor(default_executor)
        def pulse():
            loop.call_later(0.005, pulse)
        pulse()
        return loop.run_until_complete(coro)
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.run_until_complete(loop.shutdown_default_executor())
        loop.close()
        asyncio.set_event_loop(None)


class FetchLimits(Offline):
    def test_slow_body_expires_without_using_default_pool_or_queuing(self):
        entered, closed = threading.Event(), threading.Event()
        sock, conn = mock.MagicMock(), mock.MagicMock()
        reads = []
        sock.shutdown.side_effect = lambda *args: closed.set()
        conn.close.side_effect = lambda: closed.set()
        response = types.SimpleNamespace(status=200, getheaders=lambda: [], close=lambda: None)
        def read(size):
            reads.append(size)
            if closed.wait(0.005):
                raise OSError('fictional closed socket')
            return b'x'
        response.read1 = read
        def headers():
            entered.set()
            return response
        conn.getresponse.side_effect = headers

        async def exercise():
            route = Route()
            task = asyncio.create_task(real_browser._pinned_route(route, lambda reason: None, [0]))
            for _ in range(200):
                if entered.is_set():
                    break
                await asyncio.sleep(0.001)
            self.assertTrue(entered.is_set())
            loop = asyncio.get_running_loop()
            self.assertEqual(await asyncio.wait_for(loop.run_in_executor(None, lambda: 'default ready'), 0.2), 'default ready')
            self.assertFalse(task.done())
            refused = Route()
            await real_browser._pinned_route(refused, lambda reason: None, [0])
            self.assertEqual(refused.result, 'abort')
            self.assertFalse(task.done())
            self.assertEqual(conn.getresponse.call_count, 1)
            await asyncio.wait_for(task, 2)
            self.assertEqual(route.result, 'abort')
            self.assertTrue(closed.is_set())
            self.assertGreater(len(reads), 1)
            for _ in range(200):
                if slots.acquire(blocking=False):
                    slots.release()
                    break
                await asyncio.sleep(0.001)
            else:
                self.fail('page worker was not released')

        slots = threading.BoundedSemaphore(1)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool, \
             concurrent.futures.ThreadPoolExecutor(max_workers=1) as default_pool, \
             mock.patch.object(real_browser, '_fetch_pool', pool), \
             mock.patch.object(real_browser, '_fetch_slots', slots), \
             mock.patch.object(real_browser, 'OPEN_SECONDS', 0.4), \
             mock.patch.object(real_browser, '_resolve_addresses', return_value=[PUBLIC]), \
             mock.patch.object(real_browser, '_proxy_for', return_value=None), \
             mock.patch.object(real_browser.http.client, 'HTTPConnection', return_value=conn), \
             mock.patch.object(real_browser.socket, 'socket', return_value=sock), \
             mock.patch.object(real_browser.ssl, 'create_default_context') as tls:
            tls.return_value.wrap_socket.return_value = sock
            run_offline_loop(exercise(), default_pool)

    def test_fifth_simultaneous_fetch_is_rejected_by_real_admission_limit(self):
        release = threading.Event()
        entered = []
        lock = threading.Lock()
        def fetch(url, headers, check, job):
            with lock:
                entered.append(url)
            if not release.wait(5):
                raise AssertionError('fake fetch was not released')
            return 200, {}, b'fictional page', url

        async def exercise():
            routes = [Route(URL + '?request=' + str(index)) for index in range(5)]
            tasks = [asyncio.create_task(real_browser._pinned_route(route, lambda reason: None, [0]))
                     for route in routes[:4]]
            try:
                for _ in range(200):
                    with lock:
                        ready = len(entered) == 4
                    if ready:
                        break
                    await asyncio.sleep(0.005)
                self.assertTrue(ready)
                fifth = asyncio.create_task(real_browser._pinned_route(routes[4], lambda reason: None, [0]))
                tasks.append(fifth)
                await asyncio.wait_for(asyncio.shield(fifth), 0.2)
                self.assertEqual(routes[4].result, 'abort')
                self.assertTrue(all(not task.done() for task in tasks[:4]))
                with lock:
                    self.assertEqual(len(entered), 4)
            finally:
                release.set()
                if len(tasks) == 5 and not tasks[-1].done():
                    tasks[-1].cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
            self.assertEqual([route.result for route in routes[:4]], ['fulfill'] * 4)

        # Keep the real admission semaphore: replacing it with an unlimited one
        # must make the fifth request queue here and fail the assertion above.
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool, \
             mock.patch.object(real_browser, '_fetch_pool', pool), \
             mock.patch.object(real_browser, '_fetch_checked', side_effect=fetch):
            run_offline_loop(exercise())


class Wiring(Offline):
    def test_default_switch_is_off(self):
        schema = json.loads((ROOT / '_conf_schema.json').read_text('utf-8'))
        self.assertFalse(schema['browser_enabled']['default'])
        self.assertFalse(schema['browser_interactive_enabled']['default'])

    def test_short_empty_and_script_prompts(self):
        self.assertTrue(mixin_browse.needs_browser(''))
        self.assertTrue(mixin_browse.needs_browser('URL: x\nTitle: x\nContent: short'))
        self.assertTrue(mixin_browse.needs_browser('x' * 200 + ' Please enable JavaScript'))
        self.assertFalse(mixin_browse.needs_browser('x' * 200))

    def test_read_fallback_switch_and_material_wrapper(self):
        class Ledger:
            def money_left(self): return True
            def add(self, **kwargs): pass
        class Tool:
            async def call(self, *args, **kwargs): return self.text
        class Reader(mixin_browse.BrowseMixin):
            enabled = browse_enabled = True
            context = None
            def _browse_ledger(self): return Ledger()
            def _builtin_web_tool(self, kind): return self.tool
            async def _may_go_out(self, event, words): return True
        reader, event = Reader(), types.SimpleNamespace()
        reader.tool = Tool()
        mixin_browse.BrowseMixin._browse_urls(event).add(URL)
        async def fallback(url, check, on_block=None):
            calls.append(url)
            return {'url': URL, 'title': 'Example', 'text': 'material text'}
        calls = []
        async def exercise(text, enabled):
            reader.tool.text, reader.browser_enabled = text, enabled
            setattr(event, mixin_browse.QUOTA_ATTR, browse.Quota.for_reply())
            return await reader._tool_read(event, URL)
        with mock.patch.object(mixin_browse, 'resolve_host', return_value=[PUBLIC]), \
             mock.patch.object(real_browser, 'read_page', side_effect=fallback):
            asyncio.run(exercise('short', False))
            asyncio.run(exercise('x' * 200, True))
            self.assertEqual(calls, [])
            result = asyncio.run(exercise('URL: x\nTitle: x\nContent:', True))
            self.assertEqual(calls, [URL])
            self.assertEqual(result, browse.wrap(URL, 'URL: %s\nTitle: Example\nContent: material text' % URL))
            self.assertEqual(getattr(event, mixin_browse.READ_ATTR)[-1]['title'], 'Example')
            asyncio.run(exercise('short', True))
            self.assertEqual(len(calls), 2)
            asyncio.run(exercise('x' * 200 + ' enable JavaScript', True))
            self.assertEqual(len(calls), 3)
            reader.browse_enabled = False
            asyncio.run(exercise('short', True))
            self.assertEqual(len(calls), 3)
            reader.browse_enabled = True
            with mock.patch.object(real_browser, 'read_page', return_value=None):
                self.assertEqual(asyncio.run(exercise('short', True)), browse.wrap(URL, 'short'))

    def test_material_is_limited(self):
        self.assertTrue(len(browse.wrap(URL, 'x' * (browse.PAGE_CHARS + 100))) < browse.PAGE_CHARS + 300)

    def test_browser_ledger_and_panel(self):
        class Tool:
            async def call(self, *args, **kwargs): return 'short'
        class Reader(mixin_browse.BrowseMixin):
            enabled = browse_enabled = browser_enabled = True
            context = None
            def _builtin_web_tool(self, kind): return Tool()
            async def _may_go_out(self, event, words): return True
        async def exercise(reader, event):
            async def success(url, check, on_block=None):
                on_block(2)
                return {'url': url, 'title': 'Title', 'text': 'text'}
            async def failure(url, check, on_block=None):
                on_block(1)
                return None
            with mock.patch.object(real_browser, 'read_page', side_effect=success):
                await reader._tool_read(event, URL)
            with mock.patch.object(real_browser, 'read_page', side_effect=failure):
                await reader._tool_read(event, URL)
        with tempfile.TemporaryDirectory() as tmp:
            reader, event = Reader(), types.SimpleNamespace()
            reader._browse_ledger_obj = browse.Ledger(Path(tmp) / 'ledger.json')
            reader._browse_urls(event).add(URL)
            with mock.patch.object(mixin_browse, 'resolve_host', return_value=[PUBLIC]):
                asyncio.run(exercise(reader, event))
            reader._browse_ledger_obj.add(browser_shots=1, browser_shots_failed=2, browser_blocked_requests=4)
            panel = reader._browse_for_panel()
            self.assertEqual([panel[k] for k in ('browser_reads', 'browser_reads_failed', 'browser_shots',
                                                   'browser_shots_failed', 'browser_blocked_requests')], [1, 1, 1, 2, 7])


class ScreenshotWiring(Offline):
    def test_retention_only_removes_own_old_jpegs(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(mixin_selfie, 'SHOT_DIR', Path(tmp)):
            folder = Path(tmp)
            files = [folder / ('ams-browser-%032x.jpg' % n) for n in range(24)]
            for n, path in enumerate(files):
                path.write_bytes(b'x')
                import os
                os.utime(path, (1000 + n, 1000 + n))
            other = folder / 'unrelated.jpg'
            other.write_bytes(b'x')
            mixin_selfie._prune_browser_shots(files[-1])
            self.assertEqual(len([p for p in files if p.exists()]), 20)
            self.assertTrue(files[-1].exists() and other.exists())
            self.assertFalse(files[0].exists())

    def test_capture_counts_and_uses_screenshot_vision_source(self):
        class Provider:
            async def text_chat(self, **kwargs):
                self.args = kwargs
                return types.SimpleNamespace(completion_text=getattr(self, 'text', 'A page'))
        class Plugin:
            def __init__(self, led): self.led, self.provider, self.sources = led, Provider(), []
            def _browse_ledger(self): return self.led
            def _vision_provider_for(self, event, source):
                self.sources.append(source)
                return self.provider
        async def success(url, check, path, on_block=None):
            on_block(2)
            path.write_bytes(b'fictional jpeg')
            return path
        async def failure(url, check, path, on_block=None):
            on_block(1)
            return None
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plugin = Plugin(browse.Ledger(root / 'ledger.json'))
            with mock.patch.object(mixin_selfie, 'SHOT_DIR', root / 'shots'), \
                 mock.patch.object(real_browser, 'screenshot', side_effect=success):
                result = asyncio.run(mixin_selfie._browser_screenshot(plugin, object(), URL))
                self.assertEqual(result[1], 'A page')
                self.assertEqual(plugin.sources, ['screenshot'])
                self.assertEqual(plugin.provider.args['image_urls'], [str(result[0])])
                plugin.provider.text = ''
                self.assertIsNone(asyncio.run(mixin_selfie._browser_screenshot(plugin, object(), URL)))
                with mock.patch.object(real_browser, 'screenshot', side_effect=failure):
                    self.assertIsNone(asyncio.run(mixin_selfie._browser_screenshot(plugin, object(), URL)))
            row = plugin.led.row()
            self.assertEqual((row['browser_shots'], row['browser_shots_failed'], row['browser_blocked_requests']),
                             (2, 1, 5))

    def test_vision_gate_counts_screenshot_separately(self):
        class Plugin:
            def _speaker(self, event): return ('10005', 'Example')
            def _here(self, event): return 'group:900001'
            def _load_image_cache(self): return {}
            def _save_image_cache(self, cache): pass
            def _job_stale(self): return False
        class Provider:
            async def text_chat(self, **kwargs): return types.SimpleNamespace(completion_text='page')
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(mixin_attention, 'SPEND_PATH', Path(tmp) / 'spend.json'), \
             mock.patch.object(vision, 'DATA_DIR', Path(tmp)), \
             mock.patch.object(vision, '_bytes', return_value=b'\x89PNG\r\n\x1a\nfictional'):
            gate = vision.VisionGate(Plugin(), Provider(), object(), source='screenshot')
            asyncio.run(gate.text_chat(prompt='describe', image_urls=['fake']))
            counts = vision.vision_for_panel({})
            self.assertEqual((counts['calls'], counts['screenshot'], counts['browse'], counts['unattributed']),
                             (1, 1, 0, 0))

    def test_media_sends_image_only_after_description_and_checks(self):
        class Event:
            def __init__(self): self.sent = []
            def is_stopped(self): return False
            async def send(self, chain): self.sent.append(chain)
        class Phone(mixin_selfie.SelfieMixin):
            browser_enabled = True
            config = {'screenshot_enabled': True}
            def __init__(self): self.reject = ''
            async def _phone_clear(self, event, text): return self.reject not in text if self.reject else True
            def _phone_account(self, *args, **kwargs): pass
            def _note_she_sent(self, *args): pass
        queue = {'screenshot': (URL, 'Title', 'Caption')}
        async def exercise(phone, result):
            event = Event()
            with mock.patch.object(mixin_selfie, 'SEND_DELAY', 0), \
                 mock.patch.object(mixin_selfie, '_browser_screenshot', return_value=result) as capture:
                await phone._media_after_reply(event, queue)
            return event.sent[0], capture.await_count
        phone = Phone()
        chain, count = asyncio.run(exercise(phone, (Path('fake.jpg'), 'image description')))
        self.assertEqual(count, 1)
        self.assertEqual(chain.get_plain_text(), 'Caption')
        self.assertEqual(len(chain.chain), 2)
        for result in (None,):
            chain, _ = asyncio.run(exercise(phone, result))
            self.assertEqual(chain.get_plain_text(), 'Title\n' + URL + '\nCaption')
        phone.reject = 'image description'
        chain, _ = asyncio.run(exercise(phone, (Path('fake.jpg'), 'image description')))
        self.assertEqual(chain.get_plain_text(), 'Title\n' + URL + '\nCaption')
        phone.reject, phone.browser_enabled = '', False
        chain, count = asyncio.run(exercise(phone, (Path('fake.jpg'), 'image description')))
        self.assertEqual(count, 0)
        self.assertEqual(chain.get_plain_text(), 'Title\n' + URL + '\nCaption')
        phone.browser_enabled = True
        phone.config = {'screenshot_enabled': False}
        chain, count = asyncio.run(exercise(phone, (Path('fake.jpg'), 'image description')))
        self.assertEqual(count, 0)
        self.assertEqual(chain.get_plain_text(), 'Title\n' + URL + '\nCaption')


if __name__ == '__main__':
    unittest.main()
