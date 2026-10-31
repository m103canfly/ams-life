# 2026-10-31 move-4c: the panel's page API on our own server

The plugin's 28 page routes exist today only inside AstrBot: `_register_page_api` hands them to
`context.register_web_api`, and the handlers read their request through `quart`. The move plan
serves the same pages from the panel server of 4b. This card brings the routes over without
touching one handler: a later series (4d onward) makes the handlers take plain arguments, one
mixin at a time.

## What was added

- `panel_api.py` (new, needs aiohttp) has three parts:
  - `RouteCollector` stands in for a context: `register_web_api` records `(path, handler,
    methods, desc)` in order and refuses a path outside `/astrbot_plugin_ams_life/` with
    `ValueError`. The plugin's own `_register_page_api()` needs no change.
  - `install_request_shim()` puts a small stand-in at `sys.modules["quart"]` whose only
    attribute is `request`: a proxy to the request being answered, kept in a `contextvars`
    ContextVar so two requests at once each see their own. `request.method`, `request.args`
    (`.get(name)`, first value of a repeated name) and `await request.get_json(silent=True)`
    (the JSON body, `None` when there is no body or it is not JSON) are what the handlers use;
    nothing else is offered because no handler uses anything else. Used outside a request it
    raises `RuntimeError`. It never covers another `quart` already in `sys.modules`
    (`RuntimeError`), and installing it twice is harmless.
  - `aiohttp_routes(routes)` turns each recorded route into one aiohttp route per method,
    moves the path under `/api/` (`/api/page/status`), rewrites `<path:name>` to `{name:.+}`
    and `<name>` to `{name}`, reads the body only for writes, sets the current request for the
    handler, calls it with the path parameters as keywords, resets the ContextVar in
    `finally`, and answers `web.json_response(result, dumps=functools.partial(json.dumps, ensure_ascii=False))`
    (aiohttp's `json_response` has no `ensure_ascii` argument). An exception from
    a handler is not caught here; it becomes the 500 that `panel_server` already makes. No
    logging, no body printed.
- `panel_server.py` gets three constructor parameters, all defaulting to today's behavior:
  - `api_routes` (default empty): installed in `start()`; a path not under `/api/page/` is a
    `ValueError`. The existing middleware guards them like the key routes: Host on every
    request, Origin and token on writes, nothing on GET, and no cross-origin headers.
  - `start_page` (default `None`): when given, `/` answers 302 to `/static/` + it; without
    it `/` serves `root/index.html` as before.
  - `max_body` (default aiohttp's 1 MB): passed to `web.Application(client_max_size=...)`.
- Static files: a non-empty name ending in `/` (`dashboard/`, `dashboard/stickers/`) now
  serves that folder's `index.html`; an empty name (`/static/`) is still 404, as
  `test_static_paths` requires, and the other checks (`..`, backslashes, staying inside the
  root, links) are unchanged. A served `.html` gets the token meta line inserted before
  `</head>`, the same as `/`; the page card will read the token from there.

## Behavior

The handlers, `mixin_*.py` and `main.py` are not changed; the plugin keeps registering the
same 28 routes with AstrBot, and the shim is only ever installed by our own program. The old
server constructor and the key API behave as before, which is why the 4b tests pass unchanged.
The dashboard and its scripts are not touched; pages still reach the old bridge until the page
card.

## Tests

New `tests/test_panel_api.py` (the plugin is made the way the card asks: `import test_basics`
first; the server listens on port 0; temporary folders are cleaned): 20 tests for route
collection and its order (28 routes, the plugin's own handlers), the wrong-prefix `ValueError`,
serving `page/status` and comparing it with the handler, a real toggle through
POST + Origin + token, 403 without token or with a wrong Origin and the handler never called,
the path parameter arriving as `session`/`entry_id`, `request.args` taking the first `q`,
`request.method` per request, a non-JSON body being `None`, two requests at once each reading
their own body, a failing handler becoming an empty 500, `max_body` (2 MB: 413 with the
default, through with 4 MB), the start page redirect, a folder's `index.html` with the token,
other static files and the 404s, and the source checks (`panel_api.py` imports no AstrBot;
`panel_server.py` has no `Access-Control-Allow`).

The old `tests/test_panel_server.py` is not changed.

New module line for README's table of modules (brought up to date later):

| `panel_api.py` | 面板的页接口：插件照旧把这 28 条路由交出来（`RouteCollector`），面板服务端在自己的 `/api/page/...` 上一条方法一条地应答；页面处理函数读的 `quart` 请求由一个小替身按当前请求给出 |

## Run in the build sandbox

aiohttp is not installed for the sandbox's Python, so in `python -m unittest tests.test_panel_api
tests.test_panel_server` only the three source tests ran and passed; the 27 aiohttp tests
skipped. The one file-based old test (`test_damage_detection_without_decryption`) raised
`PermissionError` only while deleting its temporary directory (the sandbox forbids it), not
from an assertion. The new logic was therefore also checked with a stand-in `aiohttp` held in
memory (no files written): path conversion, the collector, the shim, concurrent bodies,
keywords from the path, the 500 path, and the static folder/token/redirect/404 rules all
passed.

Tests: `tests.test_panel_api` and `tests.test_panel_server` pass outside the sandbox with `venv-ams-life`
(aiohttp 3.14.5; 31 tests, one skipped where symlinks cannot be made), also with DeprecationWarning
as an error. The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).

## Outside the card

Nothing. This change adds `panel_api.py`, `tests/test_panel_api.py` and this note, and changes
`panel_server.py`. No commit was made.
