# 2026-10-31 move-2d-onebot-server: local OneBot reverse WebSocket

The future QQ layer needs a reverse WebSocket server to join the OneBot link and messenger.
This adds `onebot_server.py` and its tests, without wiring the server into the existing entry
point. Existing message behaviour and golden traces are unchanged. There is no new switch.

The server accepts only the two loopback bind addresses. Before upgrading a request, it checks
the peer, actual listening port and Host, absence of Origin, authorization and client role via
`onebot_link.check_handshake`. It disables access logging and logs no headers, tokens or frames.
Only the configured WebSocket path is registered. A new connection closes the old one and
fails its waiting calls, so each response belongs to the active connection. Events are delivered
in separate tasks; stopping closes the connection and cancels outstanding event tasks.

`onebot_link.Calls.settle` also ignores a future that has already finished. The tests use a fake
client and an operating-system-selected port; this change did not start anything on the default
port or connect to NapCat. No files outside the card were changed.
The connection-replacement test bounds each wait so a missing close fails instead of hanging.

Full suite: 1231 tests OK outside the sandbox with `venv-ams-life` (aiohttp 3.14.5; main aee4e7a had 1220;
+11 in `tests/test_onebot_server.py`); with the owner's Python (no aiohttp) also 1231 OK, the server tests
skipped. To be rerun after main is merged in. Golden traces unchanged.
The connection-replacement test waits with asyncio.wait_for (5 s): without it, a server that kept the old
link open made the test wait forever instead of failing.
