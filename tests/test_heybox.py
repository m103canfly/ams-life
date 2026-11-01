# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for the ParseHub signature."""
import asyncio
import base64
import hashlib
import io
import json
import sys
import tempfile
import unittest
from email.message import Message
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import heybox
import life_loop
try:
    import panel_server
except ModuleNotFoundError as exc:
    if exc.name != 'aiohttp':
        raise
    panel_server = None


def reference(path, stamp, nonce):
    table = 'AB45STUVWZEFGJ6CH01D237IXYPQRKLMN89'
    path = '/' + '/'.join(part for part in path.split('/') if part) + '/'
    parts = [str(stamp), path, nonce]
    tables = [table[:-2], table, table]
    mapped = [''.join(t[ord(c) % len(t)] for c in part) for part, t in zip(parts, tables)]
    interleaved = ''.join(part[i] for i in range(max(map(len, mapped)))
                          for part in mapped if i < len(part))[:20]
    digest = hashlib.md5(interleaved.encode()).hexdigest()

    def multiply(a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            a = ((a << 1) ^ (0x11b if a & 0x80 else 0)) & 255
            b >>= 1
        return result

    tail = list(map(ord, digest[-6:]))
    coefficients = ((17, 20, 6, 3), (3, 17, 20, 6),
                    (6, 3, 17, 20), (20, 6, 3, 17))
    mixed = []
    for row in coefficients:
        v = 0
        for coefficient, value in zip(row, tail):
            v ^= multiply(value, coefficient)
        mixed.append(v)
    prefix = ''.join(table[:-4][ord(c) % len(table[:-4])] for c in digest[:5])
    return prefix + str((sum(mixed) + sum(tail[4:])) % 100).zfill(2)


class SignatureTest(unittest.TestCase):
    def test_reference_vectors(self):
        signer = heybox.XiaoHeiHeSign()
        for path, stamp, nonce, expected in (
            ('/bbs/app/link/tree/', 1700000001, '0123456789ABCDEF0123456789ABCDEF', 'YT27P47'),
            ('/bbs/app/feeds/', 1730000000, 'FEDCBA9876543210FEDCBA9876543210', '02T1259'),
        ):
            result = signer._ov(path, stamp, nonce)
            self.assertEqual(result, expected)
            self.assertEqual(reference(path, stamp, nonce), expected)


class ReadOnlyTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.state = Path(temp.name)
        patcher = patch.object(heybox, 'STATE_DIR', self.state)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_seen_expires_after_seven_days(self):
        heybox.mark_seen(['one'], now=100)
        posts = [{'id': 'one'}, {'id': 'two'}]
        self.assertEqual(heybox.unseen(posts, now=101), [posts[1]])
        self.assertEqual(heybox.unseen(posts, now=100 + 7 * 86400), posts)

    def test_captcha_stops_requests_for_the_day(self):
        heybox.handle_status('show_captcha', now=100)
        with patch('heybox.build_opener') as opener:
            self.assertEqual(heybox.request('/bbs/app/feeds', {}, 'device', '', now=101), (None, []))
            opener.assert_not_called()

    def test_login_failure_status_requests_scan(self):
        self.assertFalse(heybox.handle_status('lack_token', now=100))
        self.assertTrue(heybox.read_json(self.state / 'heybox-status.json')['login_required'])
        self.assertFalse(heybox.captcha_paused(now=100))

    def test_first_signed_failure_holds_later_reads(self):
        self.assertFalse(heybox.handle_status('failed', now=100, path='/bbs/app/feeds'))
        with patch('heybox.build_opener') as opener:
            self.assertEqual(heybox.request('/bbs/app/link/tree', {}, 'device', '', now=101), (None, []))
            opener.assert_not_called()

    def test_feed_and_text_strip_person_metadata(self):
        posts = heybox.feed_items({'links': [{'link_id': '10001', 'title': '假标题',
                                               'nickname': '虚构作者'}]})
        self.assertEqual(posts, [{'id': '10001', 'title': '假标题'}])
        body = json.dumps([{'type': 'html', 'text': '<p>假正文</p>'},
                           {'type': 'img', 'url': 'https://example.test/picture'}])
        self.assertEqual(heybox.post_text({'link': {'text': body, 'nickname': '虚构作者'}}), '假正文')

    def test_fixed_host_and_no_credential_logging(self):
        class Response(io.BytesIO):
            status = 200
            headers = Message()

        def fake_open(req, timeout):
            self.assertTrue(req.full_url.startswith('https://api.xiaoheihe.cn/'))
            self.assertEqual(timeout, 10)
            return Response(json.dumps({'status': 'failed'}).encode())

        with self.assertLogs('ams-life.heybox', level='WARNING') as logs:
            heybox.request('/bbs/app/feeds', {}, 'fake-device', 'fake-secret', get=fake_open, now=100)
        self.assertNotIn('fake-device', str(logs.output))
        self.assertNotIn('fake-secret', str(logs.output))
        self.assertEqual(heybox.request('/unexpected', {}, 'fake-device', '', get=fake_open), (None, []))

    def test_local_token_shape_and_fixed_input(self):
        values = iter(['a' * 32, 'b' * 32, 'c' * 32])
        token = heybox.local_token(1700000000, lambda: next(values))
        expected = b''.join(hashlib.md5(x.encode()).digest()
                            for x in ('1700000000', 'a' * 32, 'b' * 32, 'c' * 32)) + b'\x00'
        self.assertEqual(base64.b64decode(token), expected)
        self.assertTrue(token.endswith('='))


class FakeKeys:
    def __init__(self):
        self.values = {}

    def get(self, name):
        return self.values[name]

    def set(self, name, value):
        self.values[name] = value

    def clear(self, name):
        self.values.pop(name, None)


class LoginTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.state = Path(temp.name)
        patcher = patch.object(heybox, 'STATE_DIR', self.state)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.keys = FakeKeys()

    async def test_qr_cookie_storage_and_logout(self):
        def fake_request(path, params, device, cookies):
            self.assertTrue(cookies.startswith('x_xhh_tokenid='))
            if path == '/account/get_qrcode_url/':
                return {'qr_url': 'https://example.test/scan?qr=fictional', 'expire': 120}, []
            return {'error': 'ok', 'heyboxid': '900001'}, [
                'user_pkey=fake-secret; Path=/', 'x_xhh_tokenid=fake-token; Path=/']

        login = heybox.Login(self.keys)
        with patch.object(heybox, 'request', side_effect=fake_request), \
                patch.object(heybox.asyncio, 'sleep', new_callable=AsyncMock):
            response = await login.start()
            await login.task
        self.assertEqual(response['state'], 'waiting')
        self.assertEqual(login.status()['state'], 'logged_in')
        saved = heybox.credential(self.keys)
        self.assertEqual(saved['cookies']['x_xhh_tokenid'], 'fake-token')
        self.assertEqual(len(saved['device_id']), 32)
        self.assertEqual(await login.logout(), {'state': 'idle'})
        self.assertIsNone(heybox.credential(self.keys))

    async def test_missing_cookie_token_is_generated_once(self):
        login = heybox.Login(self.keys)
        def fake_request(path, params, device, cookies):
            if path == '/account/get_qrcode_url/':
                return {'qr_url': 'https://example.test/scan?qr=fictional', 'expire': 120}, []
            return {'error': 'ok'}, ['user_pkey=fake-secret']

        with patch.object(heybox, 'request', side_effect=fake_request), \
                patch.object(heybox, 'local_token', return_value='generated') as token, \
                patch.object(heybox.asyncio, 'sleep', new_callable=AsyncMock):
            await login.start()
            await login.task
        token.assert_called_once()
        self.assertEqual(heybox.credential(self.keys)['cookies']['x_xhh_tokenid'], 'generated')

    async def test_browse_limits_budget_and_excludes_names(self):
        self.keys.set('heybox', json.dumps({'device_id': 'a' * 32,
                      'cookies': {'user_pkey': 'fake', 'x_xhh_tokenid': 'fake'}}))
        prompts, entries = [], []

        async def model(kind, prompt, parser, **kwargs):
            prompts.append(prompt)
            raw = '{"read":["10001"]}' if len(prompts) == 1 else '{"thought":"有点意思","tell_owner":""}'
            return parser(raw)

        plugin = SimpleNamespace(enabled=True, config={'life_loop_enabled': True, 'heybox_enabled': True},
            _key_store=self.keys, _spent_today=lambda: 0, _attention_cfg=lambda: {'soft': 8, 'hard': 10},
            _llm_allowed=lambda kind: True, _persona_text=AsyncMock(return_value='fictional'),
            _llm_v2_call=model, _red_line=lambda text, where: '',
            _read_library=lambda: {'entries': entries}, _write_library=Mock(return_value=True),
            _new_memory_id=lambda *args: 'memory')

        def fake_read(path, params, saved):
            if path.endswith('/feeds'):
                return {'links': [{'link_id': '10001', 'title': '假标题', 'nickname': '虚构作者'}]}
            if params.get('owner_only') == 1:
                return {'link': {'text': '<p>假正文</p>', 'nickname': '虚构作者'}}
            return {'comments': [{'text': '假评论', 'nickname': '虚构评论人'}]}

        with patch.object(life_loop, 'current', return_value={}), \
                patch.object(life_loop, 'read_state', return_value={}), \
                patch.object(heybox, 'read_request', side_effect=fake_read):
            self.assertTrue(await life_loop.browse_heybox(plugin, 1700000000))
            plugin._spent_today = lambda: 8
            self.assertFalse(await life_loop.browse_heybox(plugin, 1700000001))
        self.assertEqual(len(prompts), 2)
        self.assertNotIn('虚构作者', str(prompts) + str(entries))
        self.assertNotIn('虚构评论人', str(prompts) + str(entries))
        self.assertEqual(entries[0]['origin']['where'], 'self')

    async def test_logged_out_and_daily_limit_do_not_request(self):
        plugin = SimpleNamespace(enabled=True, config={'life_loop_enabled': True, 'heybox_enabled': True},
            _key_store=self.keys, _spent_today=lambda: 0, _attention_cfg=lambda: {'soft': 8, 'hard': 10},
            _llm_allowed=lambda kind: True)
        with patch.object(heybox, 'read_request') as request:
            self.assertFalse(await life_loop.browse_heybox(plugin, 1700000000))
            self.keys.set('heybox', json.dumps({'device_id': 'a' * 32,
                          'cookies': {'user_pkey': 'fake', 'x_xhh_tokenid': 'fake'}}))
            day = life_loop.datetime.fromtimestamp(1700000000).date().isoformat()
            heybox.write_json(self.state / 'heybox-usage.json', {'date': day, 'count': 6})
            with patch.object(life_loop, 'current', return_value={}), \
                    patch.object(life_loop, 'read_state', return_value={}):
                self.assertFalse(await life_loop.browse_heybox(plugin, 1700000000))
            request.assert_not_called()

    async def test_automatic_occasions_once_per_day(self):
        self.keys.set('heybox', json.dumps({'device_id': 'a' * 32,
                      'cookies': {'user_pkey': 'fake', 'x_xhh_tokenid': 'fake'}}))
        plugin = SimpleNamespace(config={'heybox_enabled': True}, _key_store=self.keys,
            _spent_today=lambda: 0, _attention_cfg=lambda: {'soft': 8, 'hard': 10})
        state = {}
        with patch.object(life_loop, 'read_state', return_value=state), \
                patch.object(life_loop, 'save_state'), \
                patch.object(life_loop, 'browse_heybox', new_callable=AsyncMock, return_value=True) as browse:
            self.assertTrue(await life_loop.automatic_heybox(plugin, 1700000000, 'wake'))
            self.assertFalse(await life_loop.automatic_heybox(plugin, 1700000001, 'wake'))
            self.assertTrue(await life_loop.automatic_heybox(plugin, 1700000001, 'lunch'))
        self.assertEqual(browse.await_count, 2)

    @unittest.skipIf(panel_server is None, 'aiohttp is unavailable')
    async def test_panel_security_requires_token_and_origin(self):
        server = panel_server.PanelServer(root=self.state, keys=self.keys)
        host = 'localhost:' + str(server.port)
        request = SimpleNamespace(method='POST', headers={'Host': host, 'Origin': 'http://' + host})
        handler = AsyncMock(return_value=panel_server.web.Response(status=200))
        self.assertEqual((await server._security(request, handler)).status, 403)
        request.headers[panel_server.TOKEN_HEADER] = server.token
        self.assertEqual((await server._security(request, handler)).status, 200)
        request.headers['Origin'] = 'https://example.test'
        self.assertEqual((await server._security(request, handler)).status, 403)
        handler.assert_awaited_once()
