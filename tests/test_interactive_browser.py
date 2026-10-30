"""Offline interactive browser checks with a fake Playwright."""
import asyncio
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'tests' / 'stubs'))
import browse
import interactive_browser as ib
import real_browser
from test_real_browser import FakePlaywright, FakeResponse, FakePage, Route, URL


class Request:
    def __init__(self, page, url=URL, method='GET', navigation=True):
        self.url, self.method, self.frame = url, method, types.SimpleNamespace(page=page)
        self.navigation = navigation

    def is_navigation_request(self):
        return self.navigation


class InteractiveRoute(Route):
    def __init__(self, page, url=URL, method='GET', status=200, location=None, navigation=True):
        super().__init__(url, method, status)
        self.request = Request(page, url, method, navigation)
        if page is not None and navigation:
            self.request.frame = page.main_frame
        self.response.headers = {'location': location} if location else {}

    async def continue_(self):
        self.result = 'continue'


class Locator:
    def __init__(self, page, ref):
        self.page, self.ref = page, ref

    async def get_attribute(self, name):
        return self.page.types.get(self.ref)

    async def click(self, **kwargs):
        self.page.clicked.append(self.ref)
        if self.page.click_route:
            await self.page.ctx.route_handler(self.page.click_route)

    async def fill(self, text, **kwargs):
        self.page.filled.append((self.ref, text))


class InteractivePage(FakePage):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.main_frame = types.SimpleNamespace(page=self)
        self.keyboard = types.SimpleNamespace(press=mock.AsyncMock())
        self.mouse = types.SimpleNamespace(wheel=mock.AsyncMock())
        self.aria = ('- link "Next" [ref=e1]\n- textbox "Search" [ref=e2]\n'
                     '- button "Go" [ref=e3] [cursor=pointer]')
        self.types, self.clicked, self.filled = {}, [], []
        self.snapshots, self.click_route = 0, None

    async def goto(self, url, **kwargs):
        route = InteractiveRoute(self, url)
        self.ctx.last_route = route
        await self.ctx.route_handler(route)
        if route.result == 'abort':
            return None
        self.url = url
        return FakeResponse(url)

    async def aria_snapshot(self, **kwargs):
        self.snapshots += 1
        self.snapshot_args = kwargs
        return self.aria

    def get_by_ref(self, ref):
        return Locator(self, ref)

    async def go_back(self, **kwargs):
        self.back_called = True


class InteractiveTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.fake = FakePlaywright()
        self.fake.context.page = InteractivePage(self.fake.context)
        api = types.ModuleType('playwright.async_api')
        api.async_playwright = lambda: self.fake
        package = types.ModuleType('playwright')
        package.__path__ = []
        self.modules = mock.patch.dict(sys.modules, {'playwright': package, 'playwright.async_api': api,
                                                    'trafilatura': None})
        self.modules.start()
        self.strict = mock.patch.object(real_browser, '_strict_url', side_effect=self.check)
        self.strict.start()
        self.session = ib.BrowsingSession(lambda url: (True, ''), browser_enabled=True,
                                          browser_interactive_enabled=True, allowed_urls={URL},
                                          typing_check=lambda text: text.replace('900001', ''))
        await self.session.__aenter__()

    async def asyncTearDown(self):
        await self.session.close()
        self.strict.stop()
        self.modules.stop()

    @staticmethod
    def check(url, check):
        return (url.startswith('https://example.com/'), 'refused')

    async def opened(self):
        result = await self.session.open(URL)
        self.assertIn('[1] 链接 “Next”', result)
        return self.fake.context.page

    async def test_snapshot_refs_and_refresh_after_each_action(self):
        page = await self.opened()
        self.assertEqual(page.snapshot_args['mode'], 'ai')
        self.assertEqual(self.session.refs[2][0], 'e2')
        page.aria = '- button "Changed" [ref=e9]'
        result = await self.session.act({'action': 'click', 'n': 1})
        self.assertEqual(page.clicked, ['e1'])
        self.assertIn('[1] 按钮 “Changed”', result)
        self.assertEqual(self.session.refs[1][0], 'e9')
        self.assertEqual(page.snapshots, 2)

    async def test_snapshot_limits_elements_and_material(self):
        page = self.fake.context.page
        page.aria = '\n'.join('- button "item" [ref=e%d]' % n for n in range(100))
        self.fake.context.body = 'a' * (ib.VISIBLE_CHARS + 50)
        result = await self.session.open(URL)
        self.assertEqual(len(self.session.refs), ib.MAX_ELEMENTS)
        self.assertLess(len(result), ib.SNAPSHOT_CHARS + 300)

    async def test_stale_reference_after_navigation_is_rejected(self):
        page = await self.opened()
        page.url = 'https://example.com/changed'
        self.assertEqual(await self.session.act({'action': 'click', 'n': 1}), ib.BLOCKED)
        self.assertEqual(page.clicked, [])

    async def test_only_allowed_actions_and_keys(self):
        page = await self.opened()
        self.assertEqual(await self.session.act({'action': 'submit'}), ib.BLOCKED)
        self.assertEqual(await self.session.act({'action': 'press', 'key': 'F12'}), ib.BLOCKED)
        await self.session.act({'action': 'press', 'key': 'Enter'})
        page.keyboard.press.assert_awaited_once()
        await self.session.act({'action': 'scroll_down'})
        await self.session.act({'action': 'scroll_up'})
        await self.session.act({'action': 'back'})
        self.assertEqual(page.mouse.wheel.await_count, 2)
        self.assertTrue(page.back_called)

    async def test_open_requires_supplied_address(self):
        self.assertEqual(await self.session.open('https://example.com/other'), ib.BLOCKED)

    async def test_typing_requires_check_and_uses_cleaned_text(self):
        page = await self.opened()
        await self.session.act({'action': 'type', 'n': 2, 'text': 'find 900001'})
        self.assertEqual(page.filled, [('e2', 'find ')])
        self.session.typing_check = lambda text: None
        self.assertEqual(await self.session.act({'action': 'type', 'n': 2, 'text': 'private'}), ib.BLOCKED)
        self.assertEqual(len(page.filled), 1)
        self.session.typing_check = None
        await self.session.snapshot()
        self.assertEqual(await self.session.act({'action': 'type', 'n': 2, 'text': 'x'}), ib.BLOCKED)

    async def test_typing_rejects_password_login_and_non_text_roles(self):
        page = await self.opened()
        page.types['e2'] = 'password'
        self.assertEqual(await self.session.act({'action': 'type', 'n': 2, 'text': 'x'}), ib.BLOCKED)
        page.types.clear()
        page.aria = '- textbox "Account" [ref=e5]'
        await self.session.snapshot()
        self.assertEqual(await self.session.act({'action': 'type', 'n': 1, 'text': 'x'}), ib.BLOCKED)
        page.aria = '- button "Go" [ref=e3]'
        await self.session.snapshot()
        self.assertEqual(await self.session.act({'action': 'type', 'n': 1, 'text': 'x'}), ib.BLOCKED)
        self.assertEqual(page.filled, [])

    async def test_post_is_blocked_and_reported(self):
        page = await self.opened()
        page.click_route = InteractiveRoute(page, method='POST')
        self.assertEqual(await self.session.act({'action': 'click', 'n': 1}), ib.BLOCKED)
        self.assertEqual(page.click_route.result, 'abort')

    async def test_click_redirect_checked_per_hop_and_local_rejected(self):
        page = await self.opened()
        page.click_route = InteractiveRoute(page, status=302, location='/next')
        self.fake.context.request.responses['https://example.com/next'] = FakeResponse(
            'https://example.com/next', 302, {'location': '/final'})
        await self.session.act({'action': 'click', 'n': 1})
        self.assertEqual(page.click_route.result, 'abort')
        self.assertEqual(page.url, 'https://example.com/final')
        page.click_route = InteractiveRoute(page, status=302, location='http://private.invalid/')
        self.assertEqual(await self.session.act({'action': 'click', 'n': 1}), ib.BLOCKED)
        self.assertEqual(page.url, 'https://example.com/final')

    async def test_subresource_redirect_is_not_followed(self):
        page = await self.opened()
        route = InteractiveRoute(page, status=302, location='/next', navigation=False)
        await self.session._route(route)
        self.assertEqual(route.result, 'abort')
        self.assertIsNone(self.session.redirect)

    async def test_popup_closed_and_checked_before_opening(self):
        page = await self.opened()
        popup = InteractivePage(self.fake.context)
        popup.url = 'https://example.com/new'
        await self.session._popup(popup)
        self.assertTrue(popup.closed)
        self.assertTrue(await self.session._follow())
        self.assertEqual(page.url, popup.url)
        popup.url = 'http://private.invalid/'
        await self.session._popup(popup)
        self.assertFalse(await self.session._follow())

    async def test_filechooser_and_dialog_are_handled(self):
        page = await self.opened()
        chooser = mock.Mock()
        page.handlers['filechooser'](chooser)
        chooser.assert_not_called()
        dialog = types.SimpleNamespace(dismiss=mock.AsyncMock())
        page.handlers['dialog'](dialog)
        await self.session._drain()
        dialog.dismiss.assert_awaited_once()

    async def test_shared_browser_security_and_websocket(self):
        await self.opened()
        self.assertTrue(self.fake.launch_args['chromium_sandbox'])
        self.assertFalse(self.fake.context_args['accept_downloads'])
        self.assertEqual(self.fake.context_args['permissions'], [])
        self.assertEqual(self.fake.context_args['service_workers'], 'block')
        self.assertEqual(self.fake.context.init_script, real_browser.WEBRTC_INIT)
        ws = types.SimpleNamespace(close=mock.AsyncMock())
        self.fake.context.ws_handler(ws)
        await self.session._drain()
        ws.close.assert_awaited_once()

    async def test_popup_initial_navigation_is_aborted_before_network(self):
        await self.opened()
        popup = InteractivePage(self.fake.context)
        route = InteractiveRoute(popup, 'https://example.com/new')
        await self.session._route(route)
        self.assertEqual(route.result, 'abort')
        self.assertIsNone(route.fetch_args)
        self.assertTrue(await self.session._follow())
        self.assertEqual(self.fake.context.page.url, 'https://example.com/new')

    async def test_unsafe_response_stops_session_reads(self):
        await self.opened()
        self.fake.context.handlers['response'](FakeResponse('http://private.invalid/'))
        await self.session._drain()
        self.assertEqual(await self.session.snapshot(), ib.BLOCKED)
        self.assertEqual(await self.session.act({'action': 'read'}), ib.BLOCKED)

    async def test_step_and_time_limits_only_allow_finish(self):
        await self.opened()
        self.session.steps = ib.MAX_STEPS
        self.assertEqual(await self.session.act({'action': 'press', 'key': 'Enter'}), ib.LIMIT)
        self.session.steps = 0
        self.session.started -= ib.MAX_SECONDS
        self.assertEqual(await self.session.act({'action': 'press', 'key': 'Enter'}), ib.LIMIT)
        self.assertEqual(await self.session.act({'action': 'finish'}), '已结束')

    async def test_read_material_and_screenshot_refresh_snapshot(self):
        page = await self.opened()
        result = await self.session.act({'action': 'read'})
        self.assertIn(browse.wrap(URL, 'Title: Example\nContent: readable words'), result)
        self.assertIn('[1] 链接', result)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'shot.jpg'
            shot = await self.session.act({'action': 'screenshot', 'path': path})
            self.assertEqual(shot['path'], path)
            self.assertIn('[1] 链接', shot['snapshot'])
            self.assertTrue(path.exists())
        self.assertEqual(page.snapshots, 3)

    async def test_read_uses_article_extraction(self):
        await self.opened()
        with mock.patch.object(real_browser, '_article_text', new=mock.AsyncMock(return_value='article')) as extract:
            result = await self.session.act({'action': 'read'})
        extract.assert_awaited_once()
        self.assertIn(browse.wrap(URL, 'Title: Example\nContent: article'), result)

    async def test_game_allows_only_files_inside_games(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'games'
            root.mkdir()
            (root / 'game.html').write_text('game', encoding='utf-8')
            self.session.games_dir = root
            result = await self.session.open_game('game.html')
            self.assertIn('[1] 链接', result)
            for address, expected in ((root.joinpath('inside.js').as_uri(), 'continue'),
                                      (root.parent.joinpath('secret.txt').as_uri(), 'abort'),
                                      ('https://example.com/page', 'abort')):
                route = InteractiveRoute(self.fake.context.page, url=address, navigation=False)
                await self.session._route(route)
                self.assertEqual(route.result, expected)
            self.assertEqual(await self.session.open_game('../secret.html'), ib.BLOCKED)
            self.assertEqual(await self.session.open_game('https://example.com/x.html'), ib.BLOCKED)
            self.assertEqual(await self.session.open(URL), ib.BLOCKED)
            self.assertFalse(ib._file_in_games(root.as_uri() + '/%2e%2e/secret.txt', root))
            self.assertFalse(ib._file_in_games(root.as_uri() + '-other/secret.txt', root))

    async def test_disabled_switches_do_not_start_browser(self):
        for browser, interactive in ((False, False), (True, False), (False, True)):
            disabled = ib.BrowsingSession(lambda url: (True, ''), browser_enabled=browser,
                                          browser_interactive_enabled=interactive)
            async with disabled:
                self.assertEqual(await disabled.open(URL), ib.UNAVAILABLE)

    async def test_challenge_is_not_read_or_screenshot(self):
        await self.opened()
        self.fake.context.body = 'Please verify you are human'
        self.assertEqual(await self.session.act({'action': 'read'}), ib.BLOCKED)
        self.assertEqual(await self.session.act({'action': 'screenshot', 'path': 'unused.jpg'}), ib.BLOCKED)

    async def test_close_releases_browser_context_and_lock(self):
        await self.session.close()
        self.assertTrue(self.fake.closed and self.fake.context.closed)
        self.assertFalse(self.session.locked)


class SourceTests(unittest.TestCase):
    def test_no_file_upload_api(self):
        forbidden = ('set_input_' + 'files', 'set_' + 'files')
        for path in ROOT.rglob('*.py'):
            if any(part in ('.git', 'venv', '.venv') for part in path.parts):
                continue
            source = path.read_text('utf-8')
            for word in forbidden:
                self.assertNotIn(word, source, str(path))

    def test_interactive_switch_defaults_off(self):
        schema = json.loads((ROOT / '_conf_schema.json').read_text('utf-8'))
        self.assertFalse(schema['browser_interactive_enabled']['default'])
