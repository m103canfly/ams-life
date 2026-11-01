# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for outbound browsing and pinned browser requests."""
import asyncio
import socket
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import browse
import discretion
import harness
import main
import mixin_browse
import mixin_selfie
import mixin_turn
import real_browser
import send_check


def address(ip):
    return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (ip, 0))]


class Route:
    def __init__(self, url="https://example.com/", method="GET"):
        self.request = types.SimpleNamespace(url=url, method=method, headers={})
        self.result = None

    async def abort(self):
        self.result = "abort"

    async def fulfill(self, **kwargs):
        self.result = "fulfill"

    async def continue_(self):
        self.result = "continue"


class PinnedBrowser(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        async def inline_fetch(url, headers, check):
            return real_browser._fetch_checked(url, headers, check)
        patcher = mock.patch.object(real_browser, "_fetch_page", new=inline_fetch)
        patcher.start()
        self.addCleanup(patcher.stop)

    async def test_launch_disables_browser_dns(self):
        class Fake:
            chromium = None
            def __init__(self):
                self.chromium = self
            async def launch(self, **kwargs):
                self.args = kwargs
                return self
            async def new_context(self, **kwargs):
                return self
            async def add_init_script(self, script):
                pass
        fake = Fake()
        with mock.patch.object(real_browser, "getproxies", return_value={}):
            await real_browser._launch_browser(fake, pinned=True)
        self.assertIn("--host-resolver-rules=MAP * ~NOTFOUND", fake.args["args"])

    async def test_connection_uses_checked_address_and_original_host(self):
        with mock.patch.object(real_browser.socket, "getaddrinfo", side_effect=[address("93.184.216.34"), address("127.0.0.1")]) as resolve, \
             mock.patch.object(real_browser, "proxy_bypass", return_value=True), \
             mock.patch.object(real_browser, "_pinned_get", return_value=(200, {}, b"ok")) as fetch:
            route = Route()
            await real_browser._pinned_route(route, lambda reason: None, [0])
        self.assertEqual(route.result, "fulfill")
        self.assertEqual(resolve.call_count, 1)
        self.assertEqual(fetch.call_args.args[1], "93.184.216.34")
        self.assertEqual(fetch.call_args.args[0], "https://example.com/")

    async def test_transport_preserves_host_and_tls_name(self):
        conn = mock.MagicMock()
        sock = mock.MagicMock()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read1.side_effect = [b"ok", b""]
        conn.getresponse.return_value.getheaders.return_value = []
        tls = mock.MagicMock()
        with mock.patch.object(real_browser.http.client, "HTTPConnection", return_value=conn) as connection, \
             mock.patch.object(real_browser.socket, "socket", return_value=sock), \
             mock.patch.object(real_browser.ssl, "create_default_context", return_value=tls):
            real_browser._pinned_get("https://example.com/path", "93.184.216.34", {})
        self.assertEqual(connection.call_args.args, ("93.184.216.34", 443))
        sock.connect.assert_called_once_with(("93.184.216.34", 443))
        self.assertEqual(conn.request.call_args.kwargs["headers"]["Host"], "example.com")
        self.assertEqual(tls.wrap_socket.call_args.kwargs["server_hostname"], "example.com")

    async def test_proxy_connects_to_proxy_and_tunnels_original_host(self):
        conn = mock.MagicMock()
        conn.sock = object()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read1.side_effect = [b"ok", b""]
        conn.getresponse.return_value.getheaders.return_value = []
        conn.host, conn.port = "proxy.invalid", 80
        tls = mock.MagicMock()
        with mock.patch.object(real_browser.http.client, "HTTPConnection", return_value=conn) as connection, \
             mock.patch.object(real_browser, "_resolve_addresses", return_value=["93.184.216.34"]), \
             mock.patch.object(real_browser.socket, "socket", return_value=mock.MagicMock()), \
             mock.patch.object(real_browser.ssl, "create_default_context", return_value=tls):
            real_browser._pinned_get("https://example.com/path", "93.184.216.34", {}, "http://proxy.invalid")
        self.assertEqual(connection.call_args.args, ("proxy.invalid", 80))
        conn.set_tunnel.assert_called_once_with("example.com", 443, headers={})
        self.assertEqual(tls.wrap_socket.call_args.kwargs["server_hostname"], "example.com")

    async def test_local_and_non_get_requests_abort(self):
        for ip in ("10.0.0.1", "127.0.0.1"):
            route = Route()
            with mock.patch.object(real_browser.socket, "getaddrinfo", return_value=address(ip)), \
                 mock.patch.object(real_browser, "_pinned_get") as fetch:
                await real_browser._pinned_route(route, lambda reason: None, [0])
            self.assertEqual(route.result, "abort")
            fetch.assert_not_called()
        for route in (Route(method="POST"), Route(url="ws://example.com/")):
            await real_browser._pinned_route(route, lambda reason: None, [0])
            self.assertEqual(route.result, "abort")

    async def test_redirects_are_checked_and_bounded(self):
        with mock.patch.object(real_browser.socket, "getaddrinfo", side_effect=[address("93.184.216.34"), address("127.0.0.1")]), \
             mock.patch.object(real_browser, "proxy_bypass", return_value=True), \
             mock.patch.object(real_browser, "_pinned_get", return_value=(302, {"Location": "https://example.org/"}, b"")) as fetch:
            route = Route()
            await real_browser._pinned_route(route, lambda reason: None, [0])
            self.assertEqual(route.result, "abort")
            self.assertEqual(fetch.call_count, 1)
        with mock.patch.object(real_browser.socket, "getaddrinfo", return_value=address("93.184.216.34")) as resolve, \
             mock.patch.object(real_browser, "proxy_bypass", return_value=True), \
             mock.patch.object(real_browser, "_pinned_get", side_effect=[(302, {"Location": "https://example.org/"}, b""), (200, {}, b"ok")]) as fetch:
            route = Route()
            await real_browser._pinned_route(route, lambda reason: None, [0])
            self.assertEqual(route.result, "fulfill")
            self.assertEqual(resolve.call_count, 2)
            self.assertEqual(fetch.call_count, 2)
        with mock.patch.object(real_browser.socket, "getaddrinfo", return_value=address("93.184.216.34")), \
             mock.patch.object(real_browser, "proxy_bypass", return_value=True), \
             mock.patch.object(real_browser, "_pinned_get", return_value=(302, {"Location": "/next"}, b"")) as fetch:
            route = Route()
            await real_browser._pinned_route(route, lambda reason: None, [0])
            self.assertEqual(route.result, "abort")
            self.assertEqual(fetch.call_count, real_browser.MAX_HOPS + 1)

    async def test_sixty_first_subrequest_aborts(self):
        route = Route()
        with mock.patch.object(real_browser, "_fetch_checked") as fetch:
            await real_browser._pinned_route(route, lambda reason: None, [61])
        self.assertEqual(route.result, "abort")
        fetch.assert_not_called()


class WebOrigin(unittest.TestCase):
    def test_private_group_and_self_recall(self):
        note = {"url": "https://example.com/", "said": "sample"}
        private = discretion.make_origin("private:10001", ["10001"])
        group = discretion.make_origin("group:900001", ["10001"])
        for origin, expected in ((private, discretion.DROP), (group, discretion.FULL),
                                 (browse.SELF_ASKED_IN, discretion.FULL)):
            memory = browse.web_memory(note, 1, "reply", origin)
            self.assertEqual(discretion.verdict(memory["origin"], "group:20002"), expected)
            lab = discretion.label(discretion.origin_of(memory), "group:20002", asked_in=origin)
            self.assertTrue(lab["web"])
            self.assertEqual(lab["may"], discretion.NO if origin == private else discretion.SAY)
            self.assertIn("网上看到的", discretion.tag(lab))

    def test_real_recall_keeps_private_pages_outside_rooms(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        test_basics.PLUGINS.append(plugin)
        asked = discretion.make_origin("private:10001", ["10001"])
        memory = browse.web_memory({"url": "https://example.com/doc", "said": "虚构文档正文"}, 1, "trip", asked)
        memory.update(id="page", vector=[1.0], ts=1)
        library = {"entries": [memory], "rooms": {}}
        plugin._read_library = lambda **kwargs: library
        plugin._write_library = lambda lib: True
        plugin._job_stale = lambda: False
        plugin._cosine = lambda *args: 1.0
        plugin._memory_score = lambda *args, **kwargs: 1.0
        plugin._known_names = lambda people: ["阿星"]
        plugin._present_people = lambda event: []
        for event, allowed in ((harness.FakeEvent("hello", sender="10001"), True),
                               (harness.FakeEvent("hello", sender="10003"), False),
                               (harness.FakeEvent("hello", sender="10001", group="900001"), False)):
            self.assertEqual(plugin._load_memory(event)["entries"], [])
            plugin._save_memory(event, {"entries": []})
            self.assertIn(memory, library["entries"])
            lines, _, _ = plugin._labeled_elsewhere(event, [1.0], None, [])
            text = "\n".join(lines)
            self.assertEqual("虚构文档正文" in text, allowed)
            if allowed:
                self.assertIn("网上看到的", text)
                self.assertNotIn("对方说过", text)
        plugin.memory_dedup_embedding = True
        plugin._usable_memory_text = lambda text: True
        plugin._schedule_consolidation = lambda *args: None
        plugin._memory_top_k = lambda *args: 3
        plugin._restabilize_if_expired = lambda *args: False
        plugin._chain_event_lines = lambda *args, **kwargs: []
        for enabled in (False, True):
            plugin.global_memory = enabled
            for event, allowed in ((harness.FakeEvent("hello", sender="10001"), True),
                                   (harness.FakeEvent("hello", sender="10003", group="900001"), False)):
                text = asyncio.run(plugin._memory_recall(event, "普通提问", vec=[1.0]))
                self.assertEqual("虚构文档正文" in text, allowed)
                if enabled and allowed:
                    self.assertIn("网上看到的", text)
        # A self-found page still protects who requested it in private.
        memory["origin"].pop("shared_in")
        event = harness.FakeEvent("hello", sender="10003", group="900001")
        lines, _, _ = plugin._labeled_elsewhere(event, [1.0], None, [])
        self.assertIn("网上看到的", "\n".join(lines))
        self.assertIn("asked:page", {item["id"] for item in plugin._check_note(event)["forbidden"]})

    def test_shared_origin_survives_origin_copy_and_merge(self):
        memory = browse.web_memory({"url": "https://example.com/", "said": "sample"}, 1, "trip",
                                   discretion.make_origin("private:10001"))
        origin = discretion.origin_of(memory)
        self.assertEqual(origin["shared_in"], "private:10001")
        self.assertEqual(discretion.may_recall(discretion.merge([origin, origin]), "group:900001"), discretion.DROP)


class Outbound(unittest.IsolatedAsyncioTestCase):
    async def test_forbidden_words_checked_when_global_memory_off(self):
        forbidden = [{"id": "private", "text": "蓝鲸三号", "private": True, "names": []}]
        class Plugin:
            global_memory = False
            def _check_note(self, event):
                return {"forbidden": forbidden, "user_text": "蓝鲸三号"}
            async def _check_reply(self, event, words):
                return send_check.check(words, forbidden, user_text="蓝鲸三号")
        plugin = Plugin()
        self.assertFalse(await mixin_browse.BrowseMixin._may_go_out(plugin, object(), "蓝鲸三号是什么"))
        self.assertTrue(await mixin_browse.BrowseMixin._may_go_out(plugin, object(), "今天天气"))

    async def test_search_does_not_send_forbidden_words(self):
        class Plugin(mixin_browse.BrowseMixin):
            global_memory = False
            def __init__(self):
                self.ledger = types.SimpleNamespace(money_left=lambda: True, add=mock.Mock())
                self.search = mock.AsyncMock(return_value='{"results": []}')
                self.context = object()
            def _browse_ledger(self):
                return self.ledger
            def _browse_names(self):
                return []
            def _check_note(self, event):
                return {"forbidden": [{"id": "private", "text": "蓝鲸三号", "private": True}]}
            async def _check_reply(self, event, words):
                return {"leak": False}
            def _builtin_web_tool(self, kind):
                return types.SimpleNamespace(call=self.search)
        plugin = Plugin()
        event = types.SimpleNamespace()
        result = await plugin._tool_search(event, "蓝鲸三号是什么")
        self.assertEqual(result, "这个不能拿去搜。")
        plugin.search.assert_not_awaited()
        await plugin._tool_search(event, "今天天气")
        plugin.search.assert_awaited_once()

    async def test_blocked_reply_keeps_pages_after_check(self):
        steps = []
        async def check(event, reply, text):
            steps.append("check")
            return ""
        async def keep(event):
            steps.append("keep")
        plugin = types.SimpleNamespace(
            enabled=True, self_decide=False, _ignored_sender=lambda event: False,
            _browse_on=lambda: True, _browse_after_reply=lambda event, reply: None,
            _continue_job=lambda here: None, _here=lambda event: "group:900001",
            _check_registry=lambda event: None, _core=lambda event: object(),
            _sticker_named=lambda event, reply, text: (text, ""), _stickers_on=lambda: False,
            _look_at_reply=check, _browse_keep_reply=keep, _phone_queue=lambda event: {},
            _stop=mock.Mock())
        event = types.SimpleNamespace()
        reply = types.SimpleNamespace(map_words=lambda fn: "blocked")
        await mixin_turn.TurnMixin._after_reply(plugin, event, reply)
        self.assertEqual(steps, ["check", "keep"])
        plugin._stop.assert_called_once_with(event)

    async def test_link_origin_and_search_origin_are_distinct(self):
        link = "https://example.com/private"
        search = "https://example.com/search"
        asked = discretion.make_origin("private:10001", ["10001"], ["m1"])
        kept = []
        async def remember(page, trip, asked_in, origin):
            kept.append((page["url"], asked_in, origin))
            return "id"
        plugin = types.SimpleNamespace(
            _here=lambda event: "private:10001", _speaker=lambda event: ("10001", ""),
            _source_ids=lambda event: ["m1"], _message_words=lambda event: link,
            _remember_web=remember)
        event = types.SimpleNamespace(_ams_browse_read=[{"url": link}, {"url": search}])
        with mock.patch.object(mixin_browse.adapter_astrbot_turn, "incoming_of",
                               return_value=types.SimpleNamespace(message_id="m1")):
            await mixin_browse.BrowseMixin._browse_keep_reply(plugin, event)
        self.assertEqual(kept, [(link, asked, asked), (search, asked, browse.SELF_ASKED_IN)])

    async def test_trip_uses_name_wall_with_no_forbidden_items(self):
        names = {"10001": ["虚构主人"], "10003": ["虚构角色"], "20002": ["阿星"]}
        store = types.SimpleNamespace(root=Path("unused"), _read=lambda path: names, places=lambda: [])
        class Plugin:
            global_memory = False
            config = {"owner_qq": "10001"}
            _her_ids = {"10003"}
            def _impression_store(self):
                return store
            def _here(self, event):
                return "self"
            def _speaker(self, event):
                return "", ""
            def _present_people(self, event):
                return []
            def _known_names(self, people):
                return [name for person in people for name in names.get(person, [])]
            def _check_note(self, event):
                return {"forbidden": []}
        plugin = Plugin()
        event = mixin_browse._trip_stand_in()
        with mock.patch.object(mixin_browse.mixin_send_check, "_sessions", return_value={"group:900001"}):
            self.assertFalse(await mixin_browse.BrowseMixin._may_go_out(plugin, event, "阿星是什么"))
            for words in ("今天天气", "虚构主人是什么", "虚构角色是什么"):
                self.assertTrue(await mixin_browse.BrowseMixin._may_go_out(plugin, event, words))


class NowLine(unittest.TestCase):
    def test_private_now_from_set_now_is_generic_elsewhere(self):
        plugin = types.SimpleNamespace(_here=lambda event: event, _browse_names=lambda: ["阿星"])
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(mixin_selfie, "NOW_PATH", Path(tmp) / "now.json"):
            mixin_selfie.SelfieMixin._set_now(plugin, "家", "帮阿星查考试", event="private:10001")
            same = mixin_selfie.SelfieMixin._now_line(plugin, "private:10001")
            self.assertIn("考试", same)
            for here in ("group:900001", "private:10003"):
                self.assertEqual(mixin_selfie.SelfieMixin._now_line(plugin, here), "此刻：在家，正在跟人私聊。")


class EmbeddedAddresses(unittest.TestCase):
    def test_embedded_private_ipv4_is_refused(self):
        for ip in ("::127.0.0.1", "::10.0.0.1", "2002:7f00:1::", "2002:c0a8:1::",
                   "64:ff9b::7f00:1", "64:ff9b::a00:1", "64:ff9b:1::a00:1"):
            self.assertTrue(browse._bad_address(ip), ip)
            self.assertFalse(browse.check_url("http://[" + ip + "]/")[0], ip)

    def test_public_nat64_is_allowed(self):
        self.assertFalse(browse._bad_address("64:ff9b::5db8:d822"))
