# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.

# 2026-10-31 - DeepSeek tools stand-in

Prepare direct DeepSeek search and fetch for the future move away from AstrBot's builtin tools.
The stand-in keeps the search and fetch request fields, validation constraints and returned result
formats used by the plugin. It is not wired into the plugin yet; there is no new switch and no
change to browsing checks, accounting or golden traces. Future integration changes
`_builtin_web_tool` once the key store is available.

The direct client does not use environment proxies, does not include error response bodies in
exceptions, and does not save icons. Redirects are disabled so the key stays at the fixed endpoints.
The card did not provide AstrBot's exact validation error sentences, so those sentences could not
be verified; invalid arguments return `Error: ...` and make no request.

Files: `deepseek_tools.py`, `tests/test_deepseek_tools.py`, and this note. No other source files changed.

## Full suite

1276 tests OK outside the sandbox (main b541afe had 1265; +11 in `tests/test_deepseek_tools.py`):
with `venv-ams-life` (aiohttp 3.14.5) all of them run, the default-session test included; with the
owner's Python (no aiohttp) also 1276 OK, the aiohttp ones skipped. Golden traces unchanged.
