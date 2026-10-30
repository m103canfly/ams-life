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
import mixin_browse
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
        if name == 'href':
            return self.page.hrefs.get(self.ref)
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
        self.types, self.hrefs, self.clicked, self.filled = {}, {}, [], []
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

    async def test_snapshot_link_allowlist_tracks_current_snapshot(self):
        page = self.fake.context.page
        page.hrefs['e1'] = '/linked'
        result = await self.session.open(URL)
        self.assertIn('https://example.com/linked', result)
        self.assertEqual(self.session.page_links, {'https://example.com/linked'})
        page.aria = '- button "Go" [ref=e3]'
        await self.session.snapshot()
        self.assertEqual(self.session.page_links, set())

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

    async def test_busy_session_limits_wait_for_read_screenshot_and_session(self):
        self.assertEqual(real_browser.LOCK_WAIT_SECONDS, 3)
        with mock.patch.object(real_browser, '_lock', asyncio.Lock()), \
             mock.patch.object(real_browser, 'LOCK_WAIT_SECONDS', 0.01):
            owner = ib.BrowsingSession(lambda url: (True, ''), browser_enabled=True,
                                       browser_interactive_enabled=True)
            async with owner:
                with self.assertLogs(real_browser.logger, level='INFO') as logs:
                    self.assertIsNone(await real_browser.read_page(URL, lambda url: (True, '')))
                    with tempfile.TemporaryDirectory() as tmp:
                        self.assertIsNone(await real_browser.screenshot(URL, lambda url: (True, ''), Path(tmp) / 'shot.jpg'))
                    other = ib.BrowsingSession(lambda url: (True, ''), browser_enabled=True,
                                               browser_interactive_enabled=True)
                    async with other:
                        self.assertEqual(await other.open(URL), ib.UNAVAILABLE)
        self.assertEqual(sum('浏览器正忙' in line for line in logs.output), 3)

    async def test_busy_browser_keeps_deepseek_text_and_counts_failed_read(self):
        class Tool:
            async def call(self, *args, **kwargs): return 'short'
        class Reader(mixin_browse.BrowseMixin):
            enabled = browse_enabled = browser_enabled = True
            context = None
            def _browse_ledger(self): return ledger
            def _builtin_web_tool(self, kind): return Tool()
            async def _may_go_out(self, event, words): return True
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(real_browser, '_lock', asyncio.Lock()), \
             mock.patch.object(real_browser, 'LOCK_WAIT_SECONDS', 0.01), \
             mock.patch.object(mixin_browse, 'resolve_host', return_value=['93.184.216.34']):
            ledger = browse.Ledger(Path(tmp) / 'ledger.json')
            reader, event = Reader(), types.SimpleNamespace()
            reader._browse_urls(event).add(URL)
            owner = ib.BrowsingSession(lambda url: (True, ''), browser_enabled=True,
                                       browser_interactive_enabled=True)
            async with owner:
                result = await reader._tool_read(event, URL)
            self.assertEqual(result, browse.wrap(URL, 'short'))
            self.assertEqual(ledger.row()['browser_reads_failed'], 1)

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


class TripTool:
    def __init__(self, name, description='', parameters=None, handler=None):
        self.name, self.parameters, self.handler = name, parameters or {}, handler


class TripTools:
    def __init__(self, tools):
        self.tools = list(tools)

    def add_tool(self, tool):
        self.tools.append(tool)


class TripProvider:
    def __init__(self, calls):
        self.calls, self.rounds = calls, []

    async def text_chat(self, contexts=None, func_tool=None, **kwargs):
        self.rounds.append((list(contexts), func_tool))
        index = len(self.rounds) - 1
        calls = [self.calls[index]] if index < len(self.calls) and func_tool else []
        return types.SimpleNamespace(
            completion_text='' if calls else json.dumps({'notes': [{'url': URL, 'title': 'Example',
                                                                      'said': 'A page'}], 'share': []}),
            tools_call_name=[name for name, args in calls], tools_call_args=[args for name, args in calls],
            tools_call_ids=['call%d' % n for n in range(len(calls))], reasoning_content=None,
            usage={'input_other': 100, 'output': 10})


class TripSession:
    instances = []

    def __init__(self, check, **kwargs):
        self.instances.append(self)
        self.typing_check, self.on_block = kwargs['typing_check'], kwargs['on_block']
        self.allowed_urls, self.page_links = set(), set()
        self.page = types.SimpleNamespace(url='about:blank')
        self.game = self.finished = False
        self.steps, self.started, self.last_read = 0, 1, None
        self.typed = []

    async def __aenter__(self): return self
    async def __aexit__(self, *args): await self.close()
    async def close(self): self.closed = True
    def _remaining(self): return 600

    async def act(self, action):
        name = action['action']
        if name == 'finish':
            self.finished = True
            return 'finished'
        if self.steps >= ib.MAX_STEPS:
            return ib.LIMIT
        self.steps += 1
        if name == 'open':
            if action['url'] not in self.allowed_urls:
                return ib.BLOCKED
            self.page.url = action['url']
            self.page_links = {'https://example.com/linked', 'https://example.com/blocked'}
        if name == 'type':
            cleaned = await self.typing_check(action['text'])
            if cleaned is None:
                return ib.BLOCKED
            self.typed.append(cleaned)
        if name == 'click':
            self.on_block(1)
            return ib.BLOCKED
        if name == 'read':
            self.last_read = {'url': self.page.url, 'title': 'Example', 'text': 'Article'}
        return 'snapshot'


class TripPlugin(mixin_browse.BrowseMixin):
    enabled = browse_enabled = browser_enabled = browser_interactive_enabled = True
    global_memory = True

    def __init__(self, provider, ledger):
        self.context = types.SimpleNamespace(get_using_provider_async=mock.AsyncMock(return_value=provider))
        self.ledger, self.self_model, self.checked, self.notes = ledger, {}, [], []

    def _browse_ledger(self): return self.ledger
    def _browse_names(self): return ['Mango']
    def _browse_topics(self): return ['fictional topic']
    async def _persona_text(self, event): return ''
    async def _may_go_out(self, event, words):
        self.checked.append(words)
        return 'blocked' not in words
    async def _tool_search(self, event, query=''):
        self._browse_urls(event).add(URL)
        return 'search result'
    async def _tool_read(self, event, url=''): return 'page'
    async def _remember_web(self, note, trip, asked_in):
        self.notes.append(note)
        return 'memory'
    def _save_self_model(self): pass


class TripIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = browse.Ledger(Path(self.tmp.name) / 'ledger.json')
        self.tool_module = types.ModuleType('astrbot.core.agent.tool')
        self.tool_module.FunctionTool, self.tool_module.ToolSet = TripTool, TripTools
        self.modules = mock.patch.dict(sys.modules, {'astrbot.core': types.ModuleType('astrbot.core'),
                                                      'astrbot.core.agent': types.ModuleType('astrbot.core.agent'),
                                                      'astrbot.core.agent.tool': self.tool_module})
        self.modules.start()
        TripSession.instances = []
        self.session_patch = mock.patch.object(ib, 'BrowsingSession', TripSession)
        self.session_patch.start()

    async def asyncTearDown(self):
        self.session_patch.stop()
        self.modules.stop()
        self.tmp.cleanup()

    async def run_trip(self, calls, **switches):
        provider = TripProvider(calls)
        plugin = TripPlugin(provider, self.ledger)
        for name, value in switches.items():
            setattr(plugin, name, value)
        core = types.SimpleNamespace(boredom=1.0, novelty_need=1.0)
        result = await plugin._browse_trip(core, 1000)
        return plugin, provider, result

    async def test_trip_interactive_tools_typing_accounting_and_memory(self):
        action = mixin_browse.INTERACTIVE_TOOL
        calls = [(browse.SEARCH_TOOL, {'query': 'topic'}),
                 (action, {'action': 'open', 'url': URL}),
                 (action, {'action': 'type', 'n': 2, 'text': 'Mango 900001 hello'}),
                 (action, {'action': 'type', 'n': 2, 'text': 'blocked'}),
                 (action, {'action': 'click', 'n': 1}),
                 (action, {'action': 'read'}), (action, {'action': 'finish'})]
        plugin, provider, result = await self.run_trip(calls)
        session = TripSession.instances[0]
        self.assertEqual(session.typed, ['hello'])
        self.assertIn('hello', plugin.checked)
        self.assertIn('blocked', plugin.checked)
        self.assertTrue(session.closed)
        self.assertEqual(result['notes'], 1)
        self.assertEqual(plugin.notes[0]['url'], URL)
        row = self.ledger.row()
        self.assertEqual([row[k] for k in ('interactive_steps', 'interactive_clicks', 'interactive_types',
                                           'interactive_blocked', 'browser_blocked_requests')], [5, 1, 2, 2, 1])
        self.assertEqual((row['input_miss'], row['output']), (800, 80))
        panel = plugin._browse_for_panel()
        self.assertEqual(panel['interactive_steps'], 5)
        names = [tool.name for tool in provider.rounds[0][1].tools]
        self.assertEqual(names, [browse.SEARCH_TOOL, browse.READ_TOOL, action])
        action_tool = provider.rounds[0][1].tools[-1]
        self.assertNotIn('screenshot', action_tool.parameters['properties']['action']['enum'])
        self.assertIsNone(provider.rounds[-1][1])

    async def test_trip_opens_only_search_and_current_page_links(self):
        action = mixin_browse.INTERACTIVE_TOOL
        calls = [(browse.SEARCH_TOOL, {'query': 'topic'}), (action, {'action': 'open', 'url': URL}),
                 (action, {'action': 'open', 'url': 'https://example.com/linked'}),
                 (action, {'action': 'open', 'url': 'https://example.com/unlisted'}),
                 (action, {'action': 'finish'})]
        _, _, result = await self.run_trip(calls)
        self.assertEqual(TripSession.instances[0].page.url, 'https://example.com/linked')
        self.assertEqual(self.ledger.row()['interactive_blocked'], 1)
        self.assertEqual(result['notes'], 0)

    async def test_trip_link_open_also_passes_outbound_check(self):
        action = mixin_browse.INTERACTIVE_TOOL
        calls = [(browse.SEARCH_TOOL, {'query': 'topic'}), (action, {'action': 'open', 'url': URL}),
                 (action, {'action': 'open', 'url': 'https://example.com/blocked'}),
                 (action, {'action': 'finish'})]
        plugin, _, _ = await self.run_trip(calls)
        self.assertIn('https://example.com/blocked', plugin.checked)
        self.assertEqual(TripSession.instances[0].page.url, URL)
        self.assertEqual(self.ledger.row()['interactive_blocked'], 1)

    async def test_trip_switch_off_keeps_old_two_tools(self):
        for switches in ({'browser_enabled': False}, {'browser_interactive_enabled': False},
                         {'browse_enabled': False}):
            with self.subTest(switches=switches):
                _, provider, _ = await self.run_trip([], **switches)
                self.assertEqual([t.name for t in provider.rounds[0][1].tools],
                                 [browse.SEARCH_TOOL, browse.READ_TOOL])
        self.assertEqual(TripSession.instances, [])

    async def test_trip_thirty_steps_forces_final_without_tools(self):
        action = mixin_browse.INTERACTIVE_TOOL
        calls = [(action, {'action': 'press', 'key': 'ArrowDown'}) for _ in range(31)]
        _, provider, result = await self.run_trip(calls)
        self.assertEqual(TripSession.instances[0].steps, 30)
        self.assertEqual(self.ledger.row()['interactive_steps'], 30)
        self.assertIsNone(provider.rounds[-1][1])
        self.assertTrue(result['final'])

    async def test_trip_time_limit_closes_before_final(self):
        action = mixin_browse.INTERACTIVE_TOOL
        original = TripSession.act
        async def expire(session, instruction):
            result = await original(session, instruction)
            session._remaining = lambda: 0
            return result
        with mock.patch.object(TripSession, 'act', new=expire):
            _, provider, result = await self.run_trip([(action, {'action': 'press', 'key': 'ArrowDown'})])
        self.assertTrue(TripSession.instances[0].closed)
        self.assertIsNone(provider.rounds[-1][1])
        self.assertTrue(result['final'])

    async def test_trip_only_executes_one_browser_action_per_model_round(self):
        class BatchProvider(TripProvider):
            async def text_chat(self, contexts=None, func_tool=None, **kwargs):
                self.rounds.append((list(contexts), func_tool))
                if len(self.rounds) == 1:
                    return types.SimpleNamespace(completion_text='',
                        tools_call_name=[mixin_browse.INTERACTIVE_TOOL] * 2,
                        tools_call_args=[{'action': 'press', 'key': 'ArrowDown'}] * 2,
                        tools_call_ids=['a', 'b'], reasoning_content=None, usage={'input_other': 100})
                return types.SimpleNamespace(completion_text='{}', tools_call_name=[], usage={'input_other': 100})
        provider = BatchProvider([])
        plugin = TripPlugin(provider, self.ledger)
        await plugin._browse_trip(types.SimpleNamespace(boredom=1, novelty_need=1), 1000)
        self.assertEqual(TripSession.instances[0].steps, 1)
        self.assertEqual(self.ledger.row()['interactive_steps'], 1)
