"""Offline browser and wiring checks: no browser, model or network."""
import asyncio
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
    return browse.check_url(url, lambda host: [resolver(host, None)[0][4][0]] if host in
                            ('example.com', 'private.example.com') else [])


class Route:
    def __init__(self, url=URL, method='GET'):
        self.request = types.SimpleNamespace(url=url, method=method)
        self.result = None

    async def abort(self):
        self.result = 'abort'

    async def continue_(self):
        self.result = 'continue'


class FakeResponse:
    def __init__(self, url=URL, status=200, headers=None):
        self.url, self.status, self.headers = url, status, headers or {}


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
        for route in self.ctx.routes:
            await self.ctx.route_handler(route)
        for address in self.ctx.responses:
            self.ctx.handlers['response'](FakeResponse(address) if isinstance(address, str) else address)
        if self.ctx.popup:
            self.ctx.handlers['page'](self.ctx.popup)
        if self.ctx.dialog:
            self.handlers['dialog'](self.ctx.dialog)
        self.url = self.ctx.final_url
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
        self.final_url, self.body = URL, 'readable words'
        self.main_response = FakeResponse()
        self.settle_timeout, self.settled_body = False, None
        self.popup = self.dialog = None
        self.closed = self.fail = False
        self.page = FakePage(self)

    async def route(self, pattern, handler):
        self.pattern, self.route_handler = pattern, handler

    async def route_web_socket(self, pattern, handler):
        self.ws_pattern, self.ws_handler = pattern, handler

    async def new_page(self):
        return self.page

    def on(self, name, callback):
        self.handlers[name] = callback

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
    def run_browser(self, fake, shot=None, on_block=None):
        api = types.ModuleType('playwright.async_api')
        api.async_playwright = lambda: fake
        api.TimeoutError = TimeoutError
        package = types.ModuleType('playwright')
        package.__path__ = []
        with mock.patch.dict(sys.modules, {'playwright': package, 'playwright.async_api': api}), \
             mock.patch.object(real_browser.socket, 'getaddrinfo', side_effect=resolver):
            task = (real_browser.screenshot(URL, check, shot, on_block=on_block) if shot is not None else
                    real_browser.read_page(URL, check, on_block=on_block))
            return asyncio.run(task)

    def test_launch_and_context_are_temporary_and_sandboxed(self):
        fake = FakePlaywright()
        self.assertEqual(self.run_browser(fake)['text'], 'readable words')
        self.assertEqual(fake.launch_args, {'channel': 'msedge', 'headless': True, 'chromium_sandbox': True,
                                            'args': ['--disable-features=DnsOverHttps']})
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
                         ['continue', 'continue', 'abort', 'abort', 'abort', 'abort'])

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
        self.assertEqual([r.result for r in fake.context.routes], ['abort', 'continue', 'abort'])
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
             mock.patch.object(real_browser.socket, 'getaddrinfo', side_effect=resolver):
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
