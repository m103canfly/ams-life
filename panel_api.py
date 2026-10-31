# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The owner's panel API, as the plugin registers it for AstrBot, served by panel_server.

The page handlers read their request the way Quart lets them (`from quart import request`).
In our own program there is no Quart: `install_request_shim()` puts a small stand-in at
sys.modules["quart"] whose `request` is the request being answered (a ContextVar)."""
import contextvars
import functools
import json
import re
import sys
import types
from urllib.parse import parse_qsl

from aiohttp import web

PREFIX = '/astrbot_plugin_ams_life/'
_CURRENT = contextvars.ContextVar('ams_life_panel_request', default=None)
_PATH_ARG = re.compile(r'<(?:(?P<converter>[a-z]+):)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)>')


class RouteCollector:
    """What a context offers the plugin for its pages: register_web_api, as AstrBot's."""

    def __init__(self):
        self.routes = []          # (path, handler, methods, desc), in order

    def register_web_api(self, route, handler, methods, desc):
        if not str(route).startswith(PREFIX):
            raise ValueError('a page route must start with ' + PREFIX)
        self.routes.append((str(route), handler, tuple(methods), str(desc)))


class _Args:
    """`request.args`: a query argument by name, the first value of a repeated name."""

    def __init__(self, items):
        self._items = items

    def get(self, name, default=None):
        for key, value in self._items:
            if key == name:
                return value
        return default


class _Request:
    """One request as the page handlers read it: the method, its query, its JSON body."""

    def __init__(self, method, query, body):
        self._method = str(method).upper()
        self._args = _Args(query)
        self._body = body

    @property
    def method(self):
        return self._method

    @property
    def args(self):
        return self._args

    async def get_json(self, force=False, silent=False, cache=True):
        return self._body


class _RequestProxy:
    """The `request` the page handlers import: whatever request is being answered now."""

    @property
    def method(self):
        return _current().method

    @property
    def args(self):
        return _current().args

    async def get_json(self, force=False, silent=False, cache=True):
        return await _current().get_json(force=force, silent=silent, cache=cache)


def _current():
    request = _CURRENT.get()
    if request is None:
        raise RuntimeError('no panel request is being answered')
    return request


_QUART = types.ModuleType('quart')
_QUART.request = _RequestProxy()


def install_request_shim() -> None:
    """Put our `quart` stand-in at sys.modules["quart"], or find it already there.

    Somebody else's `quart` (the real one, or a stand-in of another test) is never covered."""
    installed = sys.modules.get('quart')
    if installed is not None and installed is not _QUART:
        raise RuntimeError('another quart module is already loaded')
    sys.modules['quart'] = _QUART


def _convert_path(path):
    """AstrBot's `<name>` and `<path:name>` in aiohttp's `{name}` and `{name:.+}`."""

    def swap(match):
        converter, name = match.group('converter'), match.group('name')
        if converter is None:
            return '{%s}' % name
        if converter == 'path':
            return '{%s:.+}' % name
        raise ValueError('unsupported path converter: %s' % converter)

    return _PATH_ARG.sub(swap, path)


def _api_path(path):
    if not str(path).startswith(PREFIX):
        raise ValueError('a page route must start with ' + PREFIX)
    return '/api/' + _convert_path(str(path)[len(PREFIX):])


def _served(handler, method):
    """One route's handler: the body for writes, this request as the current one, the answer."""

    async def serve(request):
        body = None
        if method not in ('GET', 'HEAD'):
            try:
                body = json.loads(await request.read())
            except ValueError:
                body = None
        token = _CURRENT.set(_Request(
            method, parse_qsl(request.rel_url.query_string, keep_blank_values=True), body))
        try:
            result = await handler(**request.match_info)
        finally:
            _CURRENT.reset(token)
        return web.json_response(result, dumps=functools.partial(json.dumps, ensure_ascii=False))

    return serve


def aiohttp_routes(routes) -> list:
    """The plugin's page routes as aiohttp wants them: one route for each method."""
    made = []
    for path, handler, methods, _desc in routes:
        api_path = _api_path(path)
        for method in methods:
            method = str(method).upper()
            made.append((method, api_path, _served(handler, method)))
    return made
