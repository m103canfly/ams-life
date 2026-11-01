"""Offline browser and wiring checks: no browser, model or network."""
import asyncio
import ast
import json
import socket
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests' / 'stubs'))
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
    # structure only (scheme, port, no user, no local name): real_browser resolves once itself
    return browse.check_url(url)


class Route:
    def __init__(self, url=URL, method='GET', status=200, headers=None, navigation=False, frame=None):
        self.request = types.SimpleNamespace(
            url=url, method=method,
            is_navigation_request=lambda: navigation,
            frame=frame)
        self.result = None
        self.response = FakeResponse(url, status)
        self.fetch_args = None
        self.fulfilled = None

    async def abort(self):
        self.result = 'abort'

    async def fallback(self):
        self.result = 'fallback'

    async def fetch(self, **kwargs):
        self.fetch_args = kwargs
        return self.response

    async def fulfill(self, response=None, **kwargs):
        self.result = 'fulfill'
        if response is not None:
            self.fulfilled_response = response
        else:
            self.fulfilled = kwargs


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
        self.ctx.main_route = Route(url, status=self.ctx.main_route_status, navigation=True, frame=None)
        await self.ctx.route_handler(self.ctx.main_route)
        if self.ctx.main_route.result == 'abort':
            return None
        for route in self.ctx.routes:
            await self.ctx.route_handler(route)
        if self.ctx.popup:
            self.ctx.handlers['page'](self.ctx.popup)
        if self.ctx.dialog:
            self.handlers['dialog'](self.ctx.dialog)
        self.url = self.ctx.final_url or url
        if self.ctx.fail:
            raise TimeoutError()
        return self.ctx.main_response

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
        self.main_route_status = 200
        self.settle_timeout, self.settled_body = False, None
        self.popup = self.dialog = None
        self.closed = self.fail = False
        self.fetches, self.fetch_calls = {}, []
        self.page = FakePage(self)

    def fetch(self, url, ip, timeout=real_browser.OPEN_SECONDS, connect=real_browser._connect):
        self.fetch_calls.append((url, ip))
        item = self.fetches.get(url)
        if isinstance(item, Exception):
            raise item
        if item is None:
            return 200, {'content-type': 'text/html'}, b'<html>page</html>'
        return item

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


class Browser(unittest.TestCase):
    def setUp(self):
        proxy_patch = mock.patch.object(real_browser, 'getproxies', return_value={})
        proxy_patch.start()
        self.addCleanup(proxy_patch.stop)

    def run_browser(self, fake, shot=None, on_block=None, extractor=None):
        api = types.ModuleType('playwright.async_api')
        api.async_playwright = lambda: fake
        api.TimeoutError = TimeoutError
        package = types.ModuleType('playwright')
        package.__path__ = []
        with mock.patch.dict(sys.modules, {'playwright': package, 'playwright.async_api': api,
                                           'trafilatura': extractor}), \
             mock.patch.object(real_browser.socket, 'getaddrinfo', side_effect=resolver), \
             mock.patch.object(real_browser, '_fetch_once', new=fake.context.fetch):
            task = (real_browser.screenshot(URL, check, shot, on_block=on_block) if shot is not None else
                    real_browser.read_page(URL, check, on_block=on_block))
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
        self.assertEqual(fake.context_args['proxy'], {'server': proxies['https'],
                                                      'bypass': 'localhost,.example.test'})

    def test_context_uses_http_proxy_or_omits_proxy(self):
        fake = FakePlaywright()
        with mock.patch.object(real_browser, 'getproxies', return_value={'http': 'http://proxy.example.test'}):
            self.assertIsNotNone(self.run_browser(fake))
        self.assertEqual(fake.context_args['proxy'], {'server': 'http://proxy.example.test'})
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
            if args[0] in (real_browser._pin_address, real_browser._fetch_once):
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
                                                     real_browser.HOST_RESOLVER_RULE]})
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
        # only GET goes out; a name that resolves here to the home network or nowhere is refused
        self.assertEqual([r.result for r in fake.context.routes],
                         ['fulfill', 'abort', 'abort', 'abort', 'abort', 'abort'])

    def test_subrequest_fetch_error_is_counted_and_page_is_read(self):
        class Error(Exception):
            pass
        fake = FakePlaywright()
        route = Route('https://example.com/image')
        fake.context.fetches['https://example.com/image'] = Error('fictional connection failure')
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
        fake = FakePlaywright()
        fake.context.fetches[URL] = Error('fictional connection failure')
        counts = []
        self.assertIsNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual(fake.context.main_route.result, 'abort')
        self.assertEqual(counts, [1])

    def test_request_failure_and_abort_failure_do_not_escape(self):
        class Error(Exception):
            pass
        fake = FakePlaywright()
        route = Route('https://example.com/image')
        fake.context.fetches['https://example.com/image'] = Error('fetch detail')
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
                             ('fetch', TypeError('fictional coding error'))):
            with self.subTest(phase=phase):
                fake = FakePlaywright()
                route = Route('https://example.com/resource')
                if phase == 'fulfill':
                    route.fulfill = mock.AsyncMock(side_effect=error)
                else:
                    fake.context.fetches['https://example.com/resource'] = error
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
        fake.context.fetches[URL] = (302, {'location': target}, b'')
        counts = []
        self.assertIsNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual([url for url, _ in fake.context.fetch_calls], [URL])
        self.assertEqual(counts, [1])
        self.assertTrue(fake.context.closed and fake.closed)
        fake = FakePlaywright()
        fake.context.fetches[URL] = (302, {'location': target}, b'')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'shot.jpg'
            self.assertIsNone(self.run_browser(fake, path))
            self.assertFalse(path.exists())
            self.assertEqual([url for url, _ in fake.context.fetch_calls], [URL])

    def test_main_public_redirect_is_followed_only_after_check(self):
        fake = FakePlaywright()
        target = 'https://example.com/next'
        fake.context.fetches[URL] = (302, {'location': '/next'}, b'')
        result = self.run_browser(fake)
        self.assertEqual(result['url'], target)
        # both hops resolved here and connected by the address checked
        self.assertEqual(fake.context.fetch_calls, [(URL, PUBLIC), (target, PUBLIC)])
        self.assertEqual(fake.context.goto_url, URL)   # the browser never follows the redirect
        self.assertEqual(fake.context.main_route.result, 'fulfill')

    def test_main_redirect_limit_and_loop(self):
        for redirects in (real_browser.MAX_HOPS, real_browser.MAX_HOPS + 1):
            with self.subTest(redirects=redirects):
                fake = FakePlaywright()
                urls = [URL] + ['https://example.com/hop%d' % n for n in range(redirects)]
                for current, following in zip(urls, urls[1:]):
                    fake.context.fetches[current] = (302, {'location': following}, b'')
                result = self.run_browser(fake)
                if redirects == real_browser.MAX_HOPS:
                    self.assertEqual(result['url'], urls[-1])
                else:
                    self.assertIsNone(result)
                # MAX_HOPS redirects followed, then the next one stops it
                self.assertEqual(len(fake.context.fetch_calls), real_browser.MAX_HOPS + 1)
        fake = FakePlaywright()
        fake.context.fetches[URL] = (302, {'location': URL}, b'')
        self.assertIsNone(self.run_browser(fake))
        self.assertEqual(len(fake.context.fetch_calls), real_browser.MAX_HOPS + 1)
        fake = FakePlaywright()
        fake.context.fetches[URL] = (302, {}, b'')
        fake.context.main_response = FakeResponse(URL, 302)
        self.assertIsNone(self.run_browser(fake))

    def test_route_serves_redirects_and_other_responses(self):
        fake = FakePlaywright()
        fake.context.routes = [Route('https://example.com/a'), Route('https://example.com/b'),
                               Route('https://example.com/c'), Route(method='POST')]
        fake.context.fetches['https://example.com/a'] = (302, {}, b'')   # no Location: served as it is
        fake.context.fetches['https://example.com/b'] = (200, {}, b'ok')
        fake.context.fetches['https://example.com/c'] = (404, {}, b'')
        counts = []
        self.assertIsNotNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual([r.result for r in fake.context.routes], ['fulfill', 'fulfill', 'fulfill', 'abort'])
        self.assertEqual(counts, [1])
        self.assertEqual([r.fulfilled['status'] for r in fake.context.routes[:3]], [302, 200, 404])

    def test_route_source_never_continues_unchecked(self):
        source = (ROOT / 'real_browser.py').read_text('utf-8')
        self.assertNotIn('.continue_', source)
        # only data:/blob: (not network requests) go back to the browser
        self.assertEqual(source.count('route.fallback()'), 1)

    def test_main_route_redirect_to_a_private_name_is_aborted(self):
        fake = FakePlaywright()
        fake.context.fetches[URL] = (302, {'location': 'https://private.example.com/'}, b'')
        counts = []
        self.assertIsNone(self.run_browser(fake, on_block=counts.append))
        self.assertEqual(fake.context.main_route.result, 'abort')
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
        fake.context.fetches[URL] = (302, {'location': 'http://127.0.0.1/'}, b'')
        self.assertIsNone(self.run_browser(fake))
        self.assertTrue(fake.closed and fake.context.closed)

    def test_redirect_location_to_local_is_rejected_without_followup_request(self):
        for status in (301, 302):
            with self.subTest(status=status):
                fake = FakePlaywright()
                fake.context.fetches[URL] = (status, {'location': 'http://127.0.0.1/'}, b'')
                self.assertIsNone(self.run_browser(fake))
                self.assertEqual(len(fake.context.fetch_calls), 1)   # the next hop is never fetched
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / 'shot.jpg'
                    self.assertIsNone(self.run_browser(fake, path))
                    self.assertFalse(path.exists())

    def test_relative_redirect_location_is_resolved_and_allowed(self):
        fake = FakePlaywright()
        fake.context.fetches[URL] = (302, {'location': '/next'}, b'')
        fake.context.fetches['https://example.com/next'] = (200, {}, b'page')
        result = self.run_browser(fake)
        self.assertEqual(result['text'], 'readable words')
        self.assertEqual(result['url'], 'https://example.com/next')

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
        fake.context.fetches[URL] = (302, {'location': 'http://127.0.0.1/'}, b'')
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
             mock.patch.object(real_browser.socket, 'getaddrinfo', side_effect=resolver), \
             mock.patch.object(real_browser, '_fetch_once',
                               new=lambda url, ip, timeout=real_browser.OPEN_SECONDS, connect=real_browser._connect:
                               (200, {}, b'page')):
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


class Wiring(unittest.TestCase):
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
        async def fallback(url, check, on_block=None, resolve=None):
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
            async def success(url, check, on_block=None, resolve=None):
                on_block(2)
                return {'url': url, 'title': 'Title', 'text': 'text'}
            async def failure(url, check, on_block=None, resolve=None):
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


class ScreenshotWiring(unittest.TestCase):
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
        async def success(url, check, path, on_block=None, resolve=None):
            on_block(2)
            path.write_bytes(b'fictional jpeg')
            return path
        async def failure(url, check, path, on_block=None, resolve=None):
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
