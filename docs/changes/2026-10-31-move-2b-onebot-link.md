# 2026-10-31 move-2b-onebot-link: the OneBot 11 link without aiohttp

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Step 2 is our own reverse WebSocket server for NapCat (OneBot 11). Opening a port needs `aiohttp`,
which waits for the owner to say yes; this change is the half that needs no `aiohttp` and is easy
to test offline: who may connect, what one frame is, and one call waiting for its answer. The
`aiohttp` card later only wires these pieces to a socket, and the safety checks stay covered here.

New files only; no existing file is changed, so no behaviour changes and the golden traces stay
the same:

* `onebot_link.py`: `check_handshake`, `self_id_of`, `parse_frame`, `kind_of`, and `Calls`.
  Standard library only (`asyncio`, `hmac`, `ipaddress`, `json`, `secrets`); no AstrBot, no
  `aiohttp`, and no socket.
* `tests/test_onebot_link.py`: 30 offline tests; every number, token and host in them is made up.

The handshake checks, in this order; the first one that fails gives its word:

1. no token configured: `no token`;
2. the peer is not this machine: `not local`. `ipaddress` decides `is_loopback`, and an
   IPv4-mapped IPv6 address (`::ffff:127.0.0.1`) is unwrapped first; an address that cannot be
   parsed is not local;
3. `Host` is not exactly `127.0.0.1:<port>`, `localhost:<port>` or `[::1]:<port>`: `host`;
4. an `Origin` header is present (only a browser sends one; NapCat does not): `origin`;
5. `Authorization` is not `Bearer <token>` or `Token <token>` (the scheme ignores case) with the
   token compared by `hmac.compare_digest`: `token`;
6. `X-Client-Role` is present and is not `Universal` (ignoring case): `role`;
7. otherwise `(True, "")`.

The reason is always one of the fixed words above; no header value, and so never the token, is
put into it.

The token is read from the header only, never from `?access_token=` in the URL: the query string
ends up in logs (the aiohttp access log, proxies, error messages), and a secret in a log is a
leaked secret. NapCat can send the header form; the aiohttp card checks once on the machine that
it does.

A frame is read whole: `MAX_FRAME_BYTES` is 16 MiB because base64 pictures make frames big;
`parse_frame` accepts one text frame (str or bytes, UTF-8) and gives a dict, or None when it is
too big, not JSON, or not an object. `kind_of` says `response` when a frame has `echo` and
`status` or `retcode`, `event` when it has `post_type`, and `""` otherwise.

`Calls` pairs an answer with its call by `echo`: `secrets.token_hex(8)`, never one already
waiting; the sent frame is `{"action", "params", "echo"}`, OneBot 11's shape. The call waits at
most `CALL_SECONDS` (30) and gives back the whole answering frame. A timeout raises
`asyncio.TimeoutError`; `close()` raises `ConnectionError` in every call that still waits and
also in calls after it. However a call ends, its `echo` is removed from the waiting table, so a
late or repeated answer is nobody's (`settle` gives `False` and does nothing). A `send_frame`
that raises is passed through as it is.

Tests: `tests/test_onebot_link.py` adds 30 tests. Only this file was run in the sandbox:
`python -m unittest tests.test_onebot_link` (30 tests, all OK).

Full suite: 1102 tests OK (main 7e92514 had 1072; +30 in `tests/test_onebot_link.py`). Golden traces unchanged.

Written by dsh (DeepSeek Harness, headless, workspace-write), dispatched and checked by the build
window.
