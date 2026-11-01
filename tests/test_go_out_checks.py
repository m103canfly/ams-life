# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for what may go out (1h): the send check on a search, an address or what she
would type; a trip's names wall; where a web memory belongs and where it may not be brought up;
a page kept after her reply was held back; "此刻" in another chat; and the browser that resolves
every name once, connects by the address it checked, fetches on its own small pool and speaks
only an HTTP proxy. No network, no model, no AstrBot, no files."""
import asyncio
import json
import sys
import threading
import time
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
import mixin_memory  # noqa: E402
import mixin_selfie  # noqa: E402
import mixin_send_check  # noqa: E402
import mixin_turn  # noqa: E402
import real_browser  # noqa: E402
import send_check  # noqa: E402

URL = 'https://example.com/page'
PUBLIC = '93.184.216.34'
PUBLIC_V6 = '2606:2800:220:1:248:1893:25c8:1946'


class _RealNetwork(BaseException):
    """Raised when a test would reach the real network. A BaseException so nothing that
    swallows Exception (a resolver, a fetch) can hide it."""


class Sealed(unittest.TestCase):
    """Every browser test is offline: the real resolver and the real sockets are booby traps
    (tests that mean to use one replace it with a fake of their own), and the system proxy is
    empty unless the test sets it."""

    def setUp(self):
        super().setUp()
        for target, name in ((real_browser.socket, 'getaddrinfo'),
                             (real_browser.socket, 'create_connection'),
                             (real_browser.ssl, 'create_default_context')):
            patch = mock.patch.object(target, name, side_effect=_RealNetwork(name))
            patch.start()
            self.addCleanup(patch.stop)
        proxy_patch = mock.patch.object(real_browser, 'getproxies', return_value={})
        proxy_patch.start()
        self.addCleanup(proxy_patch.stop)


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


class OutboundChecks(Sealed):
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
        # a link given in a private chat: the page itself, usable only in that chat
        private = harness.FakeEvent('看看', sender='10003', name='小甲')
        setattr(private, mixin_browse.READ_ATTR, web_pages([('https://example.com/private', '私下给的')]))
        for page in getattr(private, mixin_browse.READ_ATTR):
            page['from'] = 'given'
        self.assertEqual(asyncio.run(plugin._browse_keep_reply(private)), 1)
        entry = plugin.library['entries'][-1]
        self.assertEqual(entry['origin']['where'], 'web:https://example.com/private')
        self.assertEqual(entry['origin']['visibility'], 'public')
        self.assertEqual(entry['origin']['shared_in'], 'private:10003')
        self.assertEqual(discretion.may_recall(entry['origin'], 'group:900001'), discretion.DROP)
        self.assertEqual(discretion.may_recall(entry['origin'], 'private:10003'), discretion.SAY)
        self.assertEqual(discretion.verdict(entry['origin'], 'group:900001'), discretion.DROP)
        self.assertEqual(discretion.verdict(entry['origin'], 'private:10003'), discretion.FULL)
        lab = discretion.label(entry['origin'], 'group:900001', '10001',
                               asked_in=entry['asked_in'])
        self.assertEqual((lab['may'], lab['web']), (discretion.NO, True))
        self.assertIn('这里不能讲', discretion.tag(lab, partner='小甲'))
        # a link given in a group: the page itself, not a room's memory, usable anywhere
        group = harness.FakeEvent('看看', sender='10001', name='柠檬', group='900001')
        setattr(group, mixin_browse.READ_ATTR, web_pages([('https://example.com/group', '群里给的')]))
        for page in getattr(group, mixin_browse.READ_ATTR):
            page['from'] = 'given'
        asyncio.run(plugin._browse_keep_reply(group))
        entry = plugin.library['entries'][-1]
        self.assertEqual(entry['origin']['where'], 'web:https://example.com/group')
        self.assertNotIn('shared_in', entry['origin'])
        self.assertEqual(discretion.may_recall(entry['origin'], 'group:900002'), discretion.SAY)
        self.assertEqual(discretion.label(entry['origin'], 'group:900002')['web'], True)
        # a page her own search found: the page itself, material anywhere, not her own memory
        searched = harness.FakeEvent('看看', sender='10001', name='柠檬', group='900001')
        setattr(searched, mixin_browse.READ_ATTR, web_pages([('https://example.com/search', '自己搜的')]))
        for page in getattr(searched, mixin_browse.READ_ATTR):
            page['from'] = 'search'
        asyncio.run(plugin._browse_keep_reply(searched))
        entry = plugin.library['entries'][-1]
        self.assertEqual(entry['origin']['where'], 'web:https://example.com/search')
        self.assertNotIn('shared_in', entry['origin'])
        lab = discretion.label(entry['origin'], 'private:10005')
        self.assertEqual((lab['may'], lab['web'], lab['self']), (discretion.SAY, True, False))
        self.assertIn('网上看到的，只是资料', discretion.tag(lab, partner='小甲'))
        self.assertEqual(discretion.may_recall(entry['origin'], 'private:10005'), discretion.SAY)

    def test_a_page_given_in_a_private_chat_is_only_that_chats(self):
        origin = browse.web_origin('https://example.com/a', 'private:10003')
        asked = discretion.make_origin('private:10003', ['10003'], ['m1'])
        for here in ('group:900001', 'private:10005'):
            lab = discretion.label(origin, here, '10001', asked_in=asked)
            self.assertEqual((lab['may'], lab['web']), (discretion.NO, True), here)
            self.assertIn('这里不能讲', discretion.tag(lab, partner='小甲'))
            # the real recall wall drops it outside that chat too
            self.assertEqual(discretion.may_recall(origin, here), discretion.DROP)
            self.assertEqual(discretion.verdict(origin, here), discretion.DROP)
        inside = discretion.label(origin, 'private:10003', '10003', asked_in=asked)
        self.assertEqual((inside['may'], inside['web'], inside['self']), (discretion.SAY, True, False))
        self.assertEqual(discretion.may_recall(origin, 'private:10003'), discretion.SAY)
        # once the one who gave it is forgotten, the page does not become material again: it
        # stays private to that chat, and that chat is nobody's, so it is dropped everywhere
        forgotten = dict({'origin': origin}, asked_in=discretion.gone_origin())
        kept = discretion.origin_of(forgotten)
        self.assertEqual(kept['shared_in'], 'private:10003')
        for here in ('group:900001', 'private:10005'):
            lab = discretion.label(kept, here, '10001', asked_in=discretion.gone_origin())
            self.assertEqual((lab['may'], lab['web']), (discretion.NO, True), here)
            self.assertIn('这里不能讲', discretion.tag(lab, partner='小甲'))
            self.assertEqual(discretion.may_recall(kept, here), discretion.DROP, here)
            self.assertEqual(discretion.verdict(kept, here), discretion.DROP, here)

    def test_a_web_page_is_not_a_rooms_memory(self):
        class FakeMemory(mixin_memory.MemoryMixin):
            def __init__(self, lib):
                self.lib = lib

            def _here(self, event):
                return 'group:900001'

            def _job_stale(self):
                return False

            def _read_library(self, vectors=True):
                return self.lib

            def _write_library(self, lib):
                self.lib = lib
                return True

        group_room = discretion.make_origin('group:900001', ['10001'], ['m1'])
        lib = {'rooms': {}, 'entries': [
            {'id': 'm1', 'text': '群里说过的话', 'origin': group_room},
            {'id': 'w1', 'text': '私下给的网页', 'role': 'web',
             'origin': browse.web_origin('https://example.com/a', 'private:10003')},
            {'id': 'w2', 'text': '群里给的网页', 'role': 'web',
             'origin': browse.web_origin('https://example.com/b')},
            {'id': 'p1', 'text': '私聊说过的话', 'origin': discretion.make_origin('private:10003')},
        ]}
        plugin = FakeMemory(lib)
        doc = plugin._load_memory(types.SimpleNamespace())
        self.assertEqual([e['id'] for e in doc['entries']], ['m1'])
        # tidying memories never takes a web page for a room
        self.assertEqual(plugin._library_places(), ['group:900001', 'private:10003'])
        doc['entries'].append({'id': 'm2', 'text': '又一句话', 'origin': group_room})
        plugin._save_memory(types.SimpleNamespace(), doc)
        ids = {e['id'] for e in plugin.lib['entries']}
        self.assertTrue({'w1', 'w2'} <= ids)      # the pages are still there
        self.assertIn('m2', ids)


class HeldReply(Sealed):
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
        self.assertEqual(entry['origin']['where'], 'web:https://example.com/held')


class NowInAnotherChat(Sealed):
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
        super().setUp()
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
        super().tearDown()

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
        self.timeout = None

    def settimeout(self, value):
        self.timeout = value

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


class EndlessSocket(FakeSocket):
    """A server that answers, keeps the connection open and dribbles a byte at a time: a read
    that does not look at Content-Length waits for the deadline, one that does stops at once."""

    def __init__(self, raw):
        super().__init__(raw)
        self.reads = 0

    def recv(self, size):
        self.reads += 1
        if self.raw:
            return super().recv(size)
        time.sleep(0.005)
        return b'x'


class PinnedBrowser(Sealed):
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

    def test_connect_connects_the_checked_address_and_keeps_the_name_for_tls(self):
        # C2: _connect itself, not a test's replacement of it. It resolves nothing, connects the
        # address it was given, and gives TLS the page's name (SNI and the certificate check).
        created, wrapped = [], {}

        class FakeTLS:
            def wrap_socket(self, sock, server_hostname=None):
                wrapped['sock'], wrapped['name'] = sock, server_hostname
                return sock

        def create_connection(address, timeout=None):
            created.append((address, timeout))
            return FakeSocket(b'')

        with mock.patch.object(real_browser.socket, 'create_connection', side_effect=create_connection), \
             mock.patch.object(real_browser.ssl, 'create_default_context', return_value=FakeTLS()):
            real_browser._connect(PUBLIC, 443, 'example.com', True, 5)
        self.assertEqual(created, [((PUBLIC, 443), 5)])
        self.assertEqual(wrapped['name'], 'example.com')
        self.assertIsInstance(wrapped['sock'], FakeSocket)
        # plain http: no TLS at all, the same checked address
        created.clear()
        with mock.patch.object(real_browser.socket, 'create_connection', side_effect=create_connection):
            real_browser._connect(PUBLIC, 80, 'example.com', False, 5)
        self.assertEqual(created, [((PUBLIC, 80), 5)])
        # a TLS failure still closes the socket it opened
        sock = FakeSocket(b'')
        class BrokenTLS:
            def wrap_socket(self, *args, **kwargs):
                raise OSError('fictional tls failure')
        with mock.patch.object(real_browser.socket, 'create_connection', return_value=sock), \
             mock.patch.object(real_browser.ssl, 'create_default_context', return_value=BrokenTLS()):
            with self.assertRaises(OSError):
                real_browser._connect(PUBLIC, 443, 'example.com', True, 5)
        self.assertTrue(sock.closed)

    def test_an_address_that_does_not_answer_falls_through_to_the_next(self):
        resolved, tried = [], []

        def resolve(host):
            resolved.append(host)
            return [PUBLIC_V6, PUBLIC]      # the resolver gives IPv6 first here

        def fetch(url, ip, timeout=real_browser.OPEN_SECONDS, connect=real_browser._connect):
            tried.append(ip)
            if ip == PUBLIC:        # this one does not answer; the next address must be tried
                raise OSError('unreachable here')
            return 200, {}, b'page'

        gate = real_browser._RequestGate(browse.check_url, resolve, lambda reason: None)
        route = FakeRoute(navigation=True)
        with mock.patch.object(real_browser, '_fetch_once', new=fetch):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'fulfill')
        self.assertEqual(resolved, ['example.com'])       # resolved exactly once
        self.assertEqual(tried, [PUBLIC, PUBLIC_V6])      # IPv4 first, then the next address

    def test_an_address_embedding_this_computer_is_never_public(self):
        for address in ('::127.0.0.1', '64:ff9b::7f00:1', '::ffff:0:7f00:1', '::ffff:127.0.0.1',
                        '2002:7f00:1::', '2002:0a00:1::', 'fe80::1', 'fd00::1', '::1'):
            self.assertFalse(real_browser._public_address(address), address)
            self.assertTrue(browse._bad_address(address), address)
        # an address that only carries a public IPv4 stays public
        for address in (PUBLIC, PUBLIC_V6, '::ffff:93.184.216.34', '64:ff9b::5db8:d822'):
            self.assertTrue(real_browser._public_address(address), address)
            self.assertFalse(browse._bad_address(address), address)

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


class ResponseLimits(Sealed):
    def test_a_response_is_cut_at_two_megabytes_and_loses_its_encoding(self):
        raw = http_response(headers=[('Content-Encoding', 'gzip'), ('Content-Length', '1')],
                            body=b'a' * (real_browser.MAX_RESPONSE_BYTES + 10))
        status, headers, body = real_browser._parse_response(raw)
        self.assertEqual(status, 200)
        self.assertEqual(len(body), real_browser.MAX_RESPONSE_BYTES)
        self.assertNotIn('content-encoding', headers)
        self.assertEqual(headers['content-length'], str(real_browser.MAX_RESPONSE_BYTES))
        self.assertFalse(any(key in headers for key in ('transfer-encoding', 'connection')))

    def test_the_direct_request_asks_for_identity_and_strips_the_encoding(self):
        sockets = []

        def connect(ip, port, hostname, tls, timeout):
            sock = FakeSocket(http_response(headers=[('Content-Encoding', 'gzip')], body=b'page'))
            sockets.append((sock, (ip, port, hostname, tls, timeout)))
            return sock

        status, headers, body = real_browser._fetch_once(URL, PUBLIC, 5, connect)
        self.assertEqual((status, body), (200, b'page'))
        self.assertNotIn('content-encoding', headers)
        self.assertIn(b'Accept-Encoding: identity\r\n', sockets[0][0].sent)
        self.assertEqual(sockets[0][1][:3], (PUBLIC, 443, 'example.com'))
        self.assertTrue(sockets[0][0].closed)

    def test_the_body_is_read_only_up_to_its_content_length(self):
        # the answer says two bytes; the server then keeps the connection open and dribbles
        sock = EndlessSocket(http_response(body=b'ok'))
        started = time.monotonic()
        status, headers, body = real_browser._fetch_once(URL, PUBLIC, 5, lambda *args: sock)
        self.assertLess(time.monotonic() - started, 1)   # did not wait for the server to close
        self.assertEqual((status, body), (200, b'ok'))
        self.assertLess(sock.reads, 4)                   # did not dribble on to the deadline
        self.assertTrue(sock.closed)

    def test_an_ipv6_address_keeps_its_brackets_in_host_and_connect(self):
        self.assertEqual(real_browser._host_header(PUBLIC_V6, 443, 'https'), '[%s]' % PUBLIC_V6)
        self.assertEqual(real_browser._host_header(PUBLIC_V6, 8443, 'https'),
                         '[%s]:8443' % PUBLIC_V6)
        # the absolute form a proxy is asked for
        request = real_browser._get_request('http://[%s]:8080/a?b=1' % PUBLIC_V6, via_proxy=True)
        self.assertIn(('GET http://[%s]:8080/a?b=1 HTTP/1.1\r\n' % PUBLIC_V6).encode('ascii'), request)
        # the CONNECT line for an https page through a proxy
        plain = FakeSocket(b'HTTP/1.1 200 Connection established\r\n\r\n')

        class FakeTLS:
            def wrap_socket(self, sock, server_hostname=None):
                return FakeSocket(http_response(body=b'page'))

        with mock.patch.object(real_browser.ssl, 'create_default_context', return_value=FakeTLS()):
            status, headers, body = real_browser._fetch_once_proxy(
                'https://[%s]/a' % PUBLIC_V6, 'http://proxy.example.test:8080', 5,
                lambda *args: plain)
        self.assertEqual((status, body), (200, b'page'))
        self.assertIn(('CONNECT [%s]:443 HTTP/1.1\r\n' % PUBLIC_V6).encode('ascii'), plain.sent)


class ProxyRule(Sealed):
    def test_only_an_http_proxy_is_spoken(self):
        self.assertEqual(real_browser._proxy_for(URL), (None, ''))
        with mock.patch.object(real_browser, 'getproxies',
                               return_value={'https': 'http://proxy.example.test:8080'}):
            self.assertEqual(real_browser._proxy_for(URL), ('http://proxy.example.test:8080', ''))
        for proxies in ({'all': 'socks5://127.0.0.1:1080'}, {'socks': 'socks5://127.0.0.1:1080'},
                        {'https': 'socks5://127.0.0.1:1080'}):
            with mock.patch.object(real_browser, 'getproxies', return_value=proxies):
                self.assertEqual(real_browser._proxy_for(URL), (None, 'proxy scheme'), proxies)
        # a refused proxy kind aborts the request; it never falls back to a direct connection
        gate = real_browser._RequestGate(browse.check_url, lambda host: [PUBLIC], lambda reason: None)
        route = FakeRoute(navigation=True)
        with mock.patch.object(real_browser, 'getproxies',
                               return_value={'all': 'socks5://127.0.0.1:1080'}), \
             mock.patch.object(real_browser, '_fetch_once', side_effect=_RealNetwork('direct')):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'abort')

    def test_a_host_in_no_proxy_takes_the_checked_address_path(self):
        proxies = {'https': 'http://proxy.example.test:8080', 'no': 'localhost; .example.com'}
        with mock.patch.object(real_browser, 'getproxies', return_value=proxies):
            self.assertEqual(real_browser._proxy_for(URL), (None, ''))
            self.assertEqual(real_browser._proxy_for('https://other.example.org/'),
                             ('http://proxy.example.test:8080', ''))
        gate = real_browser._RequestGate(browse.check_url, lambda host: [PUBLIC], lambda reason: None)
        route = FakeRoute(navigation=True)
        with mock.patch.object(real_browser, 'getproxies', return_value=proxies), \
             mock.patch.object(real_browser, '_fetch_once', new=lambda url, ip,
                               timeout=real_browser.OPEN_SECONDS,
                               connect=real_browser._connect: (200, {}, b'page')), \
             mock.patch.object(real_browser, '_fetch_once_proxy', side_effect=_RealNetwork('proxy')):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'fulfill')        # our own checked-address path
        self.assertEqual(route.fulfilled['body'], b'page')

    def test_a_proxied_page_is_fetched_by_our_own_fetch(self):
        seen = []

        def proxied(url, proxy, timeout=real_browser.OPEN_SECONDS, connect=real_browser._connect):
            seen.append((url, proxy, timeout))
            return 200, {'content-type': 'text/html'}, b'page'

        gate = real_browser._RequestGate(browse.check_url, lambda host: [PUBLIC], lambda reason: None)
        route = FakeRoute(navigation=True)
        proxies = {'https': 'http://proxy.example.test:8080'}
        with mock.patch.object(real_browser, 'getproxies', return_value=proxies), \
             mock.patch.object(real_browser, '_fetch_once_proxy', new=proxied), \
             mock.patch.object(real_browser, '_fetch_once', side_effect=_RealNetwork('direct')):
            asyncio.run(real_browser._route_pinned(route, gate))
        self.assertEqual(route.result, 'fulfill')
        self.assertEqual(seen, [(URL, 'http://proxy.example.test:8080', real_browser.HOP_SECONDS)])

    def test_the_proxy_request_has_the_same_limits_as_a_direct_one(self):
        sockets = []

        def connect(ip, port, hostname, tls, timeout):
            sock = FakeSocket(http_response(headers=[('Content-Encoding', 'gzip')], body=b'page'))
            sockets.append((sock, (ip, port, hostname, tls)))
            return sock

        status, headers, body = real_browser._fetch_once_proxy(
            'http://example.com/a', 'http://proxy.example.test:8080', 5, connect)
        self.assertEqual((status, body), (200, b'page'))
        self.assertNotIn('content-encoding', headers)
        self.assertEqual(sockets[0][1], ('proxy.example.test', 8080, '', False))
        sent = sockets[0][0].sent
        self.assertIn(b'GET http://example.com/a HTTP/1.1\r\n', sent)     # absolute form to the proxy
        self.assertIn(b'Accept-Encoding: identity\r\n', sent)
        self.assertTrue(sockets[0][0].closed)

    def test_an_https_page_goes_through_the_proxy_by_connect(self):
        wrapped = {}

        class FakeTLS:
            def wrap_socket(self, sock, server_hostname=None):
                tunneled = FakeSocket(http_response(body=b'page'))
                wrapped['plain'], wrapped['sock'], wrapped['name'] = sock, tunneled, server_hostname
                return tunneled

        def connect(ip, port, hostname, tls, timeout):
            return FakeSocket(b'HTTP/1.1 200 Connection established\r\n\r\n')

        with mock.patch.object(real_browser.ssl, 'create_default_context', return_value=FakeTLS()):
            status, headers, body = real_browser._fetch_once_proxy(
                URL, 'http://proxy.example.test:8080', 5, connect)
        self.assertEqual((status, body), (200, b'page'))
        self.assertEqual(wrapped['name'], 'example.com')             # TLS to the page, not the proxy
        self.assertIn(b'CONNECT example.com:443 HTTP/1.1\r\n', wrapped['plain'].sent)
        self.assertIn(b'GET /page HTTP/1.1\r\n', wrapped['sock'].sent)   # origin form inside the tunnel

    def test_the_shared_launch_keeps_the_proxy_without_a_bypass_list(self):
        class FakePlaywright:
            chromium = None

            def __init__(self):
                self.chromium = self
                self.context_args = None

            async def launch(self, **kwargs):
                return self

            async def new_context(self, **kwargs):
                self.context_args = kwargs
                return types.SimpleNamespace(add_init_script=self._init, close=self._close)

            async def _init(self, *args):
                pass

            async def _close(self, *args):
                pass

            async def close(self):
                pass

        fake = FakePlaywright()
        proxies = {'https': 'http://proxy.example.test', 'no': 'localhost; .example.test'}
        with mock.patch.object(real_browser, 'getproxies', return_value=proxies):
            asyncio.run(real_browser._launch_browser(fake, None, False))
        self.assertEqual(fake.context_args['proxy'], {'server': 'http://proxy.example.test'})
        fake = FakePlaywright()
        with mock.patch.object(real_browser, 'getproxies', return_value=proxies):
            asyncio.run(real_browser._launch_browser(fake, None, True))
        self.assertNotIn('proxy', fake.context_args)   # the pinned browser gets no proxy at all


class FetchPool(Sealed):
    """Pages are fetched on our own small pool, each hop on a deadline, and a page that cannot
    get a thread is refused instead of queued."""

    class SlowSocket:
        def __init__(self):
            self.closed, self.sent, self.timeout = False, b'', None

        def settimeout(self, value):
            self.timeout = value

        def sendall(self, data):
            self.sent += data

        def recv(self, size):
            time.sleep(0.01)
            return b'x'     # a server that dribbles one byte at a time

        def close(self):
            self.closed = True

    class BlockingSocket:
        def __init__(self, release):
            self.release, self.closed, self.timeout = release, False, None

        def settimeout(self, value):
            self.timeout = value

        def sendall(self, data):
            pass

        def recv(self, size):
            self.release.wait(5)
            return b''

        def close(self):
            self.closed = True

    def test_a_slow_server_is_cut_at_the_hop_deadline_and_the_default_pool_lives(self):
        sockets = []

        def connect(ip, port, hostname, tls, timeout):
            sock = self.SlowSocket()
            sockets.append(sock)
            return sock

        async def exercise():
            started = time.monotonic()
            slow = asyncio.create_task(
                real_browser._pool_call(real_browser._fetch_once, URL, PUBLIC, 0.3, connect))
            # the default pool is untouched while a page dribbles
            other = await asyncio.wait_for(asyncio.to_thread(lambda: 'done'), 2)
            # a deadline that is not watched must fail here, not after hours of dribbling
            result = await asyncio.wait_for(slow, 2)
            return other, result, time.monotonic() - started

        other, result, elapsed = asyncio.run(exercise())
        self.assertEqual(other, 'done')
        self.assertLess(elapsed, 2)                     # the hop's deadline ended it
        self.assertEqual(result, (0, {}, b''))          # nothing was read past the deadline
        self.assertTrue(sockets[0].closed)              # and the socket was closed

    def test_the_fifth_page_at_once_is_refused(self):
        release = threading.Event()

        def connect(ip, port, hostname, tls, timeout):
            return self.BlockingSocket(release)

        async def exercise():
            tasks = [asyncio.create_task(
                real_browser._pool_call(real_browser._fetch_once, URL, PUBLIC, 5, connect))
                for _ in range(real_browser.FETCH_WORKERS)]
            await asyncio.sleep(0.1)                    # let them take the threads
            self.assertTrue(all(not task.done() for task in tasks))
            with self.assertRaises(real_browser.FetchBusy):
                await real_browser._pool_call(real_browser._fetch_once, URL, PUBLIC, 5, connect)
            release.set()
            await asyncio.gather(*tasks, return_exceptions=True)

        try:
            asyncio.run(exercise())
        finally:
            release.set()

    def test_the_final_look_at_a_page_takes_no_fetch_thread(self):
        # a page that timed out keeps every fetch thread; the last look must still find the page
        resolved = []

        def resolve(host):
            resolved.append(host)
            return [PUBLIC]

        gate = real_browser._RequestGate(browse.check_url, resolve, lambda reason: None)
        self.assertEqual(asyncio.run(real_browser._checked(URL, gate)), ([PUBLIC], ''))
        taken = 0
        try:
            while real_browser._take_fetch_slot():
                taken += 1
            self.assertEqual(taken, real_browser.FETCH_WORKERS)
            with self.assertRaises(real_browser.FetchBusy):
                asyncio.run(real_browser._checked('https://example.com/other', gate))
            # an address this visit already checked: answered, not resolved again
            self.assertEqual(asyncio.run(real_browser._checked_free(URL, gate)), ([PUBLIC], ''))
            self.assertEqual(len(resolved), 1)
            # an address it never checked: resolved, but never on a fetch thread
            started = time.monotonic()
            self.assertEqual(asyncio.run(real_browser._checked_free('https://example.com/other', gate)),
                             ([PUBLIC], ''))
            self.assertLess(time.monotonic() - started, 1)
            self.assertEqual(resolved, ['example.com', 'example.com'])
        finally:
            for _ in range(taken):
                real_browser._release_fetch_slot()
        self.assertEqual(real_browser._active_fetches, 0)

    def test_a_subrequest_that_cannot_get_a_thread_is_aborted(self):
        release = threading.Event()

        def fetch(url, ip, timeout=real_browser.HOP_SECONDS, connect=real_browser._connect):
            release.wait(5)
            return 200, {}, b'ok'

        gate = real_browser._RequestGate(browse.check_url, lambda host: [PUBLIC], lambda reason: None)
        async def exercise():
            first = [asyncio.create_task(real_browser._route_pinned(
                FakeRoute('https://example.com/%d' % n, navigation=True), gate))
                for n in range(real_browser.FETCH_WORKERS)]
            await asyncio.sleep(0.1)
            fifth = FakeRoute('https://example.com/fifth', navigation=True)
            await real_browser._route_pinned(fifth, gate)
            release.set()
            await asyncio.gather(*first)
            return fifth

        try:
            with mock.patch.object(real_browser, '_fetch_once', new=fetch):
                fifth = asyncio.run(exercise())
        finally:
            release.set()
        self.assertEqual(fifth.result, 'abort')
        self.assertEqual(gate.blocked, 1)


if __name__ == '__main__':
    unittest.main()
