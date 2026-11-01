# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for what may go out (1h): the send check on a search, an address or what she
would type; a trip's names wall; where a web memory belongs; a page kept after her reply was
held back; "此刻" in another chat; and the browser that resolves every name once and connects
by the address it checked. No network, no model, no AstrBot, no files."""
import asyncio
import json
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import browse  # noqa: E402
import discretion  # noqa: E402
import harness  # noqa: E402
import mixin_browse  # noqa: E402
import mixin_selfie  # noqa: E402
import mixin_send_check  # noqa: E402
import mixin_turn  # noqa: E402
import real_browser  # noqa: E402
import send_check  # noqa: E402

URL = 'https://example.com/page'
PUBLIC = '93.184.216.34'


class FakeLedger:
    def money_left(self):
        return True

    def add(self, **counts):
        pass


class FakeTool:
    """AstrBot's DeepSeek search / fetch, recorded (a search finds nothing)."""

    def __init__(self, calls, kind):
        self.calls, self.kind = calls, kind

    async def call(self, context, **kwargs):
        self.calls.append((self.kind, kwargs))
        if self.kind == 'search':
            return json.dumps({'results': []})
        return 'URL: x\nTitle: t\nContent: c'


KNOWN_NAMES = {'10003': ('阿星',), '10001': ('柠檬',), '20002': ('小爱',)}


class FakeStore:
    """The people/ folder, as far as the names wall reads it."""

    def __init__(self):
        self.root = Path('made-up-people')
        self.names = {person: list(names) for person, names in KNOWN_NAMES.items()}

    def _read(self, path):
        return dict(self.names) if str(path).endswith('names.json') else {}

    def places(self):
        return []

    def load(self, place):
        return {'people': {}}


class TestPlugin(mixin_browse.BrowseMixin, mixin_send_check.SendCheckMixin):
    enabled = browse_enabled = True
    global_memory = False
    self_decide = False
    config = {}
    context = types.SimpleNamespace()

    def __init__(self):
        self.calls = []
        self.library = {'entries': []}
        self._store = FakeStore()

    def _browse_ledger(self):
        return FakeLedger()

    def _browse_names(self):
        return []

    def _builtin_web_tool(self, kind):
        return FakeTool(self.calls, kind)

    def _impression_store(self):
        return self._store

    def _embedding_runtime_config(self):
        return {}

    def _here(self, event):
        return discretion.place_of(getattr(event, 'unified_msg_origin', ''))

    def _speaker(self, event):
        sender = getattr(event, 'get_sender_id', None)
        name = getattr(event, 'get_sender_name', None)
        return (str(sender() or '') if callable(sender) else '',
                str(name() or '') if callable(name) else '')

    def _present_people(self, event):
        return set()

    def _known_names(self, people):
        return [name for person in people for name in [str(person)] + list(KNOWN_NAMES.get(str(person), ()))]

    def _source_ids(self, event):
        return [str(event.message_obj.message_id)]

    def _job_stale(self):
        return False

    async def _embed_text(self, text):
        return []

    def _read_library(self, vectors=True):
        return self.library

    def _write_library(self, lib):
        self.library = lib
        return True

    def _new_memory_id(self, kind, key, now, text):
        return 'web-%d' % len(self.library['entries'])

    def _save_self_model(self):
        pass


def web_pages(pages):
    """A page record as _tool_read keeps it."""
    from mixin_browse import page_of
    made = []
    for url, said in pages:
        page = page_of(url, 'URL: %s\nTitle: 一页\nContent: %s' % (url, said))
        made.append(page)
    return made


class OutboundChecks(unittest.TestCase):
    def test_forbidden_words_are_checked_with_global_memory_off(self):
        # The card's first check: with global_memory off, this turn's forbidden list still counts.
        plugin = TestPlugin()
        plugin.global_memory = False
        event = harness.FakeEvent('看看', sender='10001', name='柠檬', group='900001')
        plugin._forbid(event, 'm-x', text='蓝鲸三号，别外传', people=['10002'])
        self.assertEqual(asyncio.run(plugin._tool_search(event, query='蓝鲸三号是什么')), mixin_browse.NOT_SENT)
        self.assertEqual(plugin.calls, [])
        sent = asyncio.run(plugin._tool_search(event, query='今天天气'))
        self.assertIn('搜索：今天天气', sent)
        self.assertEqual([call for call in plugin.calls], [('search', {'query': '今天天气', 'count': browse.RESULTS_MAX})])

    def test_a_trip_keeps_the_names_wall(self):
        plugin = TestPlugin()
        plugin.config = {'owner_qq': '10001', 'her_names': ['小爱']}
        plugin._her_ids = {'20002'}
        stand_in = mixin_browse._trip_stand_in()
        with mock.patch.object(mixin_send_check, '_sessions', return_value={'group:900002'}):
            self.assertEqual(asyncio.run(plugin._tool_search(stand_in, query='阿星最近怎么样')),
                             mixin_browse.NOT_SENT)
            self.assertEqual(plugin.calls, [])
            self.assertIn('搜索：今天天气', asyncio.run(plugin._tool_search(stand_in, query='今天天气')))
            # the owner's name and her own are not names to keep out of a search
            self.assertIn('搜索：柠檬最近怎么样', asyncio.run(plugin._tool_search(stand_in, query='柠檬最近怎么样')))
            self.assertIn('搜索：小爱最近怎么样', asyncio.run(plugin._tool_search(stand_in, query='小爱最近怎么样')))

    def test_where_a_web_memory_belongs(self):
        plugin = TestPlugin()
        # a link given in a private chat: that private chat, privately
        private = harness.FakeEvent('看看', sender='10003', name='小甲')
        setattr(private, mixin_browse.READ_ATTR, web_pages([('https://example.com/private', '私下给的')]))
        for page in getattr(private, mixin_browse.READ_ATTR):
            page['from'] = 'given'
        self.assertEqual(asyncio.run(plugin._browse_keep_reply(private)), 1)
        entry = plugin.library['entries'][-1]
        self.assertEqual(entry['origin']['where'], 'private:10003')
        self.assertEqual(entry['origin']['visibility'], 'private')
        self.assertEqual(discretion.verdict(entry['origin'], 'group:900001'), discretion.DROP)
        self.assertEqual(discretion.verdict(entry['origin'], 'private:10003'), discretion.FULL)
        # a link given in a group: that group, openly
        group = harness.FakeEvent('看看', sender='10001', name='柠檬', group='900001')
        setattr(group, mixin_browse.READ_ATTR, web_pages([('https://example.com/group', '群里给的')]))
        for page in getattr(group, mixin_browse.READ_ATTR):
            page['from'] = 'given'
        asyncio.run(plugin._browse_keep_reply(group))
        entry = plugin.library['entries'][-1]
        self.assertEqual(entry['origin']['where'], 'group:900001')
        self.assertEqual(entry['origin']['visibility'], 'public')
        self.assertEqual(discretion.verdict(entry['origin'], 'group:900002'), discretion.ANON)
        self.assertEqual(discretion.verdict(entry['origin'], 'group:900001'), discretion.FULL)
        # a page her own search found: hers, anywhere
        searched = harness.FakeEvent('看看', sender='10001', name='柠檬', group='900001')
        setattr(searched, mixin_browse.READ_ATTR, web_pages([('https://example.com/search', '自己搜的')]))
        for page in getattr(searched, mixin_browse.READ_ATTR):
            page['from'] = 'search'
        asyncio.run(plugin._browse_keep_reply(searched))
        entry = plugin.library['entries'][-1]
        self.assertEqual(entry['origin']['where'], 'self')
        self.assertEqual(discretion.verdict(entry['origin'], 'group:900002'), discretion.FULL)
        self.assertEqual(discretion.verdict(entry['origin'], 'private:10005'), discretion.FULL)


class HeldReply(unittest.TestCase):
    def test_pages_are_kept_after_the_send_check_even_when_nothing_is_sent(self):
        class Plugin(mixin_turn.TurnMixin, TestPlugin):
            pass

        plugin = Plugin()
        order = []
        plugin._browse_after_reply = lambda event, reply: None
        plugin._continue_job = lambda place: None
        plugin._check_registry = lambda event: None
        plugin._core = lambda event: types.SimpleNamespace()
        plugin._ignored_sender = lambda event: False
        plugin._sticker_named = lambda event, reply, text: (text, '')
        plugin._stickers_on = lambda: False
        plugin._phone_queue = lambda event: {}
        plugin._stop = lambda event: order.append('stop')

        async def held(event, reply, text):
            order.append('check')
            return ''   # the send check held the reply back: nothing is sent

        async def keep(event):
            order.append('keep')
            return await mixin_browse.BrowseMixin._browse_keep_reply(plugin, event)

        plugin._look_at_reply = held
        plugin._browse_keep_reply = keep
        event = harness.FakeEvent('看看', sender='10001', name='柠檬', group='900001')
        setattr(event, mixin_browse.READ_ATTR, web_pages([('https://example.com/held', '挡下了')]))
        for page in getattr(event, mixin_browse.READ_ATTR):
            page['from'] = 'given'
        reply = types.SimpleNamespace(map_words=lambda fn: fn('好呀'))
        asyncio.run(plugin._after_reply(event, reply))
        self.assertEqual(order, ['check', 'keep', 'stop'])   # kept after the check, then not sent
        entry = plugin.library['entries'][-1]
        self.assertEqual(entry['origin']['where'], 'group:900001')


class NowInAnotherChat(unittest.TestCase):
    class FakeNowPath:
        def __init__(self):
            self.text = None

        def read_text(self, encoding=None):
            if self.text is None:
                raise FileNotFoundError
            return self.text

        def exists(self):
            return self.text is not None

    class Phone(mixin_selfie.SelfieMixin):
        enabled = True

        def _browse_names(self):
            return self.names

        def _speaker(self, event):
            return ('10003', '小甲')

        def _core(self, event):
            return types.SimpleNamespace(snapshot=lambda: {'v': 0.3, 'energy': 0.2, 'stress': 0.2})

    def setUp(self):
        self.path = self.FakeNowPath()
        self.patches = [mock.patch.object(mixin_selfie, 'NOW_PATH', self.path),
                        mock.patch.object(mixin_selfie, '_write_json',
                                          lambda path, data: setattr(path, 'text',
                                                                     json.dumps(data, ensure_ascii=False)))]
        for item in self.patches:
            item.start()
        self.phone = self.Phone()
        self.phone.names = []

    def tearDown(self):
        for item in self.patches:
            item.stop()

    def test_private_place_is_only_rough_elsewhere(self):
        private = harness.FakeEvent('在呢', sender='10003', name='小甲')
        group = harness.FakeEvent('在吗', sender='10001', name='柠檬', group='900001')
        self.phone._set_now('家', '帮阿星查考试的事', event=private)
        self.phone.names = ['阿星']
        inside = self.phone._now_line(private)
        self.assertIn('帮阿星查考试的事', inside)
        self.assertIn('从', inside)
        elsewhere = self.phone._now_line(group)
        self.assertNotIn('阿星', elsewhere)
        self.assertIn('查考试的事', elsewhere)
        self.assertNotIn('从', elsewhere)   # no original sentence, no exact start/duration

    def test_place_self_or_empty_is_as_before(self):
        group = harness.FakeEvent('在吗', sender='10001', name='柠檬', group='900001')
        self.phone._set_now('家', '看电视', event=None)   # place is empty
        self.assertIn('从', self.phone._now_line(group))
        self.assertIn('看电视', self.phone._now_line(group))


class FakeRoute:
    def __init__(self, url=URL, method='GET', navigation=False):
        self.request = types.SimpleNamespace(
            url=url, method=method,
            is_navigation_request=lambda: navigation,
            frame=None)
        self.result = None
        self.fulfilled = None

    async def abort(self):
        self.result = 'abort'

    async def fallback(self):
        self.result = 'fallback'

    async def fulfill(self, **kwargs):
        self.result = 'fulfill'
        self.fulfilled = kwargs


class FakeSocket:
    def __init__(self, raw):
        self.raw, self.sent, self.closed = raw, b'', False

    def sendall(self, data):
        self.sent += data

    def recv(self, size):
        out, self.raw = self.raw[:size], self.raw[size:]
        return out

    def close(self):
        self.closed = True


def http_response(status=200, headers=(), body=b'ok'):
    head = 'HTTP/1.1 %d X\r\n' % status
    for name, value in headers:
        head += '%s: %s\r\n' % (name, value)
    head += 'Content-Length: %d\r\nConnection: close\r\n\r\n' % len(body)
    return head.encode() + body


class PinnedBrowser(unittest.TestCase):
    """R7 the way Playwright works: no name in the browser, every request fetched by us."""

    def test_launch_takes_the_host_resolver_rule(self):
        async def launch(pin_dns):
            class Chromium:
                async def launch(self, **kwargs):
                    self.args = kwargs['args']
                    return self

                async def new_context(self, **kwargs):
                    return types.SimpleNamespace(add_init_script=self._init, close=self._close)

                async def _init(self, *args):
                    pass

                async def _close(self, *args):
                    pass

                async def close(self):
                    pass
            inner = Chromium()
            await real_browser._launch_browser(types.SimpleNamespace(chromium=inner), None, pin_dns)
            return inner.args

        pinned = asyncio.run(launch(True))
        self.assertIn(real_browser.HOST_RESOLVER_RULE, pinned)
        # the interactive browser keeps its own way (this card does not touch it)
        self.assertNotIn(real_browser.HOST_RESOLVER_RULE, asyncio.run(launch(False)))

    def test_one_resolution_and_the_address_checked_is_the_one_connected(self):
        resolved, connects, sockets = [], [], []

        def resolve(host):
            resolved.append(host)
            return [PUBLIC] if len(resolved) == 1 else ['127.0.0.1']

        def connect(ip, port, hostname, tls, timeout):
            connects.append((ip, port, hostname))
            sock = FakeSocket(http_response(body=b'page'))
            sockets.append(sock)
            return sock

        gate = real_browser._RequestGate(browse.check_url, resolve, lambda reason: None)
        route = FakeRoute(navigation=True)
        with mock.patch.object(real_browser, '_connect', new=connect):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'fulfill')
        self.assertEqual(resolved, ['example.com'])                     # resolved once
        self.assertEqual(connects, [(PUBLIC, 443, 'example.com')])      # connected the first address
        self.assertEqual(connects[0][2], 'example.com')                 # TLS's SNI keeps the name
        self.assertIn(b'Host: example.com\r\n', sockets[0].sent)        # and so does the Host header

    def test_subrequest_hosts_methods_and_schemes(self):
        def resolve(host):
            return {'private.example': ['10.0.0.7'], 'loop.example': ['127.0.0.1']}.get(host, [PUBLIC])

        gate = real_browser._RequestGate(browse.check_url, resolve, lambda reason: None)
        for route in (FakeRoute('https://private.example/a'),
                      FakeRoute('https://loop.example/a'),
                      FakeRoute(URL, method='POST'),
                      FakeRoute('ws://example.com/socket')):
            asyncio.run(real_browser._route_pinned(route, gate))
            self.assertEqual(route.result, 'abort', route.request.url)
        self.assertEqual(gate.blocked, 4)

    def test_redirects_are_followed_by_us_and_every_hop_is_checked(self):
        def fetch(mapping):
            def one(url, ip, timeout=real_browser.OPEN_SECONDS, connect=real_browser._connect):
                item = mapping.get(url)
                if item is None:
                    return 200, {}, b'ok'
                return item
            return one

        # a redirect to an address that resolves here to this computer: not followed
        gate = real_browser._RequestGate(browse.check_url,
                                         lambda host: ['127.0.0.1'] if host == 'loop.example' else [PUBLIC],
                                         lambda reason: None)
        route = FakeRoute(navigation=True)
        with mock.patch.object(real_browser, '_fetch_once',
                               new=fetch({URL: (302, {'location': 'https://loop.example/secret'}, b'')})):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'abort')

        # a public redirect is followed; each hop is resolved and checked again
        resolved = []

        def resolve(host):
            resolved.append(host)
            return [PUBLIC]

        hops = [URL] + ['https://example.com/hop%d' % n for n in range(real_browser.MAX_HOPS)]
        mapping = {current: (302, {'location': following}, b'')
                   for current, following in zip(hops, hops[1:])}
        mapping[hops[-1]] = (200, {}, b'page')
        gate = real_browser._RequestGate(browse.check_url, resolve, lambda reason: None)
        route = FakeRoute(navigation=True)
        with mock.patch.object(real_browser, '_fetch_once', new=fetch(mapping)):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'fulfill')
        self.assertEqual(route.fulfilled['status'], 200)
        self.assertEqual(len(resolved), len(hops))    # every hop resolved once

        # a sixth redirect: stopped
        mapping[hops[-1]] = (302, {'location': 'https://example.com/never'}, b'')
        gate = real_browser._RequestGate(browse.check_url, resolve, lambda reason: None)
        route = FakeRoute(navigation=True)
        with mock.patch.object(real_browser, '_fetch_once', new=fetch(mapping)):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'abort')
        self.assertEqual(gate.blocked, 1)

    def test_the_sixty_first_subrequest_is_aborted(self):
        gate = real_browser._RequestGate(browse.check_url, lambda host: [PUBLIC], lambda reason: None)
        with mock.patch.object(real_browser, '_fetch_once',
                               new=lambda url, ip, timeout=real_browser.OPEN_SECONDS,
                               connect=real_browser._connect: (200, {}, b'ok')):
            results = []
            for n in range(real_browser.MAX_SUBREQUESTS + 1):
                route = FakeRoute('https://example.com/sub%d' % n)
                asyncio.run(real_browser._route_pinned(route, gate))
                results.append(route.result)
        self.assertEqual(results[:real_browser.MAX_SUBREQUESTS], ['fulfill'] * real_browser.MAX_SUBREQUESTS)
        self.assertEqual(results[-1], 'abort')
        self.assertEqual(gate.requests, real_browser.MAX_SUBREQUESTS)


if __name__ == '__main__':
    unittest.main()
