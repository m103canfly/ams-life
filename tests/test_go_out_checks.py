# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for outbound browsing and pinned browser requests."""
import asyncio
import json
import socket
import sys
import types
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import browse
import discretion
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
        conn.getresponse.return_value.read.return_value = b"ok"
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
        conn.getresponse.return_value.read.return_value = b"ok"
        conn.getresponse.return_value.getheaders.return_value = []
        tls = mock.MagicMock()
        with mock.patch.object(real_browser.http.client, "HTTPConnection", return_value=conn) as connection, \
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
        for origin, expected in ((private, discretion.DROP), (group, discretion.ANON),
                                 (browse.SELF_ASKED_IN, discretion.FULL)):
            memory = browse.web_memory(note, 1, "reply", origin)
            self.assertEqual(discretion.verdict(memory["origin"], "group:20002"), expected)


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
        self.assertEqual(result, mixin_browse.NOT_SENT)
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
        class Plugin:
            global_memory = False
            def _check_note(self, event):
                return {"forbidden": []}
            async def _check_reply(self, event, words):
                return send_check.check(words, [{"id": "names", "names": ["阿星"], "strict_names": True}])
        plugin = Plugin()
        self.assertFalse(await mixin_browse.BrowseMixin._may_go_out(plugin, object(), "阿星是什么"))
        self.assertTrue(await mixin_browse.BrowseMixin._may_go_out(plugin, object(), "今天天气"))


class NowLine(unittest.TestCase):
    def test_private_now_is_anonymized_elsewhere(self):
        state = {"where": "家", "doing": "帮「阿星」查考试的事", "source": "her",
                 "place": "private:10001", "start": datetime.fromtimestamp(mixin_selfie.time.time()).isoformat()}
        plugin = types.SimpleNamespace(_here=lambda event: event, _browse_names=lambda: ["阿星"])
        path = mock.Mock()
        path.read_text.return_value = json.dumps(state, ensure_ascii=False)
        with mock.patch.object(mixin_selfie, "NOW_PATH", path):
            same = mixin_selfie.SelfieMixin._now_line(plugin, "private:10001")
            group = mixin_selfie.SelfieMixin._now_line(plugin, "group:900001")
        self.assertIn("阿星", same)
        self.assertNotIn("阿星", group)
        self.assertNotIn(state["doing"], group)
