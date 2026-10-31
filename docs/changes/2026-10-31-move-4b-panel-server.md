# 2026-10-31 move-4b: local panel server

The owner chose a panel without a password (sign-off item 96). The standalone server
binds only to loopback; exact Host checks block DNS rebinding. Writes require an exact
local HTTP Origin and a fresh per-server token, which is inserted into the served index
as a meta tag. The token is not saved or logged. The server adds restrictive response
headers and does not enable cross-origin access. Static paths are confined to the root
and to an allowlist of file types.

The key page API exposes only presence flags, accepts writes and clears, and never
returns key values. `KeyStore.damaged()` shares file validation with normal reads and
reports unreadable or malformed files without decrypting keys. Missing files and valid
empty files are not damaged, avoiding a false warning after the last key is cleared.
`tests/test_panel_server.py` covers the server boundary, static files and key API.
The server is not connected to the plugin or dashboard, has no feature switch, and
does not change existing behavior or golden files. There are no changes outside this card.

Full suite: 1231 tests OK outside the sandbox with `venv-ams-life` (aiohttp 3.14.5; main aee4e7a had 1220;
+11 in `tests/test_panel_server.py`); one skipped where symlinks cannot be made. With the owner's Python (no
aiohttp) also 1231 OK, the aiohttp tests skipped. Golden traces unchanged.
