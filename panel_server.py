# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Local-only panel server and write-only key endpoints."""
import hmac
import logging
import secrets
from pathlib import Path
from urllib.parse import unquote

from aiohttp import web

try:
    from .key_store import KeyStoreError
except ImportError:
    from key_store import KeyStoreError

TOKEN_HEADER = 'X-AMS-Token'
TOKEN_META = '<meta name="ams-token" content="%s">'
_LOG = logging.getLogger('panel_server')
_SUFFIXES = {'.html', '.js', '.css', '.png', '.jpg', '.svg', '.ico', '.woff2', '.json'}
_SECURITY_HEADERS = {'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY',
                     'Referrer-Policy': 'no-referrer', 'Cache-Control': 'no-store'}


class PanelServer:
    def __init__(self, *, root, keys, host='127.0.0.1', port=0, key_names=('deepseek', 'vision')):
        if host not in ('127.0.0.1', '::1'):
            raise ValueError('host must be loopback')
        self.root = Path(root).resolve()
        self.keys = keys
        self.host = host
        self.port = port
        self.key_names = tuple(key_names)
        self._token = secrets.token_urlsafe(32)
        self._runner = None

    @property
    def token(self):
        return self._token

    @web.middleware
    async def _security(self, request, handler):
        hosts = {f'127.0.0.1:{self.port}', f'localhost:{self.port}', f'[::1]:{self.port}'}
        method = request.method
        if request.headers.get('Host') not in hosts:
            _LOG.info('blocked: host')
            response = web.Response(status=421, text='bad host')
        elif method in ('POST', 'PUT', 'PATCH', 'DELETE') and request.headers.get('Origin') not in {
                'http://' + host for host in hosts}:
            _LOG.info('blocked: origin')
            response = web.Response(status=403, text='bad origin')
        elif method in ('POST', 'PUT', 'PATCH', 'DELETE') and not hmac.compare_digest(
                request.headers.get(TOKEN_HEADER, '').encode('utf-8'), self._token.encode('ascii')):
            _LOG.info('blocked: token')
            response = web.Response(status=403, text='bad token')
        elif method not in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'):
            _LOG.info('blocked: method')
            response = web.Response(status=405)
        else:
            try:
                response = await handler(request)
            except web.HTTPMethodNotAllowed:
                response = web.Response(status=404)
            except web.HTTPException as error:
                response = error
            except Exception:
                response = web.Response(status=500)
        response.headers.update(_SECURITY_HEADERS)
        return response

    async def start(self):
        app = web.Application(middlewares=[self._security])
        app.router.add_get('/', self._index, allow_head=False)
        app.router.add_get('/static/{path:.*}', self._static, allow_head=False)
        app.router.add_get('/api/keys', self._get_keys, allow_head=False)
        app.router.add_post('/api/keys', self._set_key)
        app.router.add_delete('/api/keys/{name}', self._delete_key)
        self._runner = web.AppRunner(app, access_log=None)
        try:
            await self._runner.setup()
            site = web.TCPSite(self._runner, self.host, self.port)
            await site.start()
            self.port = self._runner.addresses[0][1]
        except BaseException:
            await self._runner.cleanup()
            self._runner = None
            raise
        _LOG.info('started')
        return self.port

    async def stop(self):
        if self._runner is not None:
            await self._runner.cleanup()
            self._runner = None
            _LOG.info('stopped')

    def _file(self, name):
        if not name or name.startswith(('/', '\\')) or '\\' in name or '..' in name.split('/'):
            raise web.HTTPNotFound()
        try:
            path = (self.root / name).resolve()
            if not path.is_relative_to(self.root) or not path.is_file():
                raise web.HTTPNotFound()
        except (OSError, ValueError, RuntimeError):
            raise web.HTTPNotFound() from None
        return path

    async def _index(self, request):
        path = self._file('index.html')
        try:
            html = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError):
            raise web.HTTPNotFound() from None
        return web.Response(text=html.replace('</head>', TOKEN_META % self._token + '\n</head>', 1),
                            content_type='text/html')

    async def _static(self, request):
        raw = unquote(request.raw_path.split('?', 1)[0])
        name = raw[len('/static/'):]
        path = self._file(name)
        if path.suffix.lower() not in _SUFFIXES:
            raise web.HTTPNotFound()
        return web.FileResponse(path)

    async def _get_keys(self, request):
        status = self.keys.status()
        result = {'keys': {name: bool(status.get(name)) for name in self.key_names}}
        if self.keys.damaged():
            result['damaged'] = True
        return web.json_response(result)

    async def _set_key(self, request):
        try:
            data = await request.json()
            if not isinstance(data, dict) or data.get('name') not in self.key_names:
                raise web.HTTPBadRequest(text='invalid')
            self.keys.set(data['name'], data.get('value'))
        except (ValueError, KeyStoreError):
            raise web.HTTPBadRequest(text='invalid') from None
        return web.json_response({'ok': True})

    async def _delete_key(self, request):
        name = request.match_info['name']
        if name not in self.key_names:
            raise web.HTTPBadRequest(text='invalid')
        try:
            self.keys.clear(name)
        except KeyStoreError:
            raise web.HTTPBadRequest(text='invalid') from None
        return web.json_response({'ok': True})
