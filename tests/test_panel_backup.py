# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for panel backup and restore."""
import base64
import importlib.util
import io
import json
import stat
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import harness  # noqa: E402
import mixin_pages  # noqa: E402


def archive(items):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            z.writestr(name, data)
    return out.getvalue()


class BackupRestore(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = self.root / 'data'
        self.data.mkdir()
        self.plugin = MagicMock()
        self.plugin._vectors_db = None
        self.patch = patch.object(mixin_pages, 'DATA_DIR', self.data)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    async def restore(self, raw):
        request = MagicMock()
        async def get_json(silent=True):
            return {'base64': base64.b64encode(raw).decode('ascii')}
        request.get_json = get_json
        with patch.dict(sys.modules, {'quart': types.SimpleNamespace(request=request)}):
            return await mixin_pages.PagesMixin.page_restore(self.plugin)

    async def test_backup_excludes_and_redacts(self):
        for name, content in {'keys.dat': 'secret', 'logs/a.log': 'log',
                              'likeness/a': 'x', 'restore_backups/a': 'x',
                              'cache.tmp': 'x', 'memory/x.json': '{}',
                              'api_config.json': '{"api_key":"secret","nested":[{"api_key":"secret"}]}'}.items():
            path = self.data / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        result = await mixin_pages.PagesMixin.page_backup(self.plugin)
        self.assertEqual(result['status'], 'ok')
        with zipfile.ZipFile(io.BytesIO(base64.b64decode(result['data']['base64']))) as z:
            names = set(z.namelist())
            self.assertIn('data/memory/x.json', names)
            for name in ('keys.dat', 'logs/a.log', 'likeness/a', 'restore_backups/a', 'cache.tmp'):
                self.assertNotIn('data/' + name, names)
            self.assertEqual(json.loads(z.read('data/api_config.json')),
                             {'api_key': '', 'nested': [{'api_key': ''}]})
            self.assertIn('refill', z.read('BACKUP_INFO.txt').decode())

    async def test_route_is_post(self):
        context = harness.FakeContext()
        plugin = test_basics.make_plugin(context)
        routes = []
        plugin.context = types.SimpleNamespace(register_web_api=lambda *args: routes.append(args))
        plugin._register_page_api()
        route = next(r for r in routes if r[0].endswith('/page/backup'))
        self.assertEqual(route[2], ['POST'])

    async def test_invalid_archives_leave_data_unchanged(self):
        original = self.data / 'keep.txt'
        original.write_text('old', encoding='utf-8')
        link = zipfile.ZipInfo('data/link')
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        bad = [archive([('data/good', 'new'), (name, 'bad')]) for name in
               ('data/..\\..\\evil.txt', 'data/C:/x', 'data/\\\\server\\x', 'data//abs')]
        bad.append(archive([('data/good', 'new'), (link, 'target')]))
        bad.append(archive([('data/f%d' % i, 'x') for i in range(20001)]))
        bad.append(archive([('data/bomb', b'0' * 100000)]))
        for raw in bad:
            with self.subTest(size=len(raw)):
                self.assertEqual((await self.restore(raw))['status'], 'error')
                self.assertEqual([(p.relative_to(self.data).as_posix(), p.read_text())
                                  for p in self.data.rglob('*') if p.is_file()], [('keep.txt', 'old')])
                self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['data'])

    async def test_existing_link_cannot_escape(self):
        outside = self.root / 'outside'
        outside.mkdir()
        link = self.data / 'link'
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('directory symlinks unavailable')
        result = await self.restore(archive([('data/link/evil.txt', 'bad')]))
        self.assertEqual(result['status'], 'error')
        self.assertFalse((outside / 'evil.txt').exists())

    async def test_resolved_destination_must_stay_inside(self):
        original = Path.resolve
        target = self.data / 'link' / 'evil.txt'
        def resolve(path, *args, **kwargs):
            if path == target:
                return self.root / 'outside' / 'evil.txt'
            return original(path, *args, **kwargs)
        with patch.object(Path, 'resolve', resolve):
            result = await self.restore(archive([('data/link/evil.txt', 'bad')]))
        self.assertEqual(result['status'], 'error')
        self.assertEqual(list(self.data.iterdir()), [])
        self.assertFalse((self.root / 'outside').exists())

    async def test_restore_preserves_protected_files(self):
        registry = mixin_pages.forget_registry.FILE_NAME
        for name in ('keys.dat', registry, 'logs/a.log'):
            path = self.data / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('old', encoding='utf-8')
        raw = archive([('data/keys.dat', 'new'), ('data/' + registry, 'new'),
                       ('data/logs/a.log', 'new'), ('data/sub/file', 'new')])
        self.assertEqual((await self.restore(raw))['status'], 'ok')
        for name in ('keys.dat', registry, 'logs/a.log'):
            self.assertEqual((self.data / name).read_text(), 'old')
        self.assertEqual((self.data / 'sub/file').read_text(), 'new')
        self.assertTrue(any((self.root / 'restore_backups').iterdir()))

    async def test_staging_write_failure_leaves_data_unchanged(self):
        (self.data / 'keep').write_text('old', encoding='utf-8')
        with patch.object(mixin_pages.shutil, 'copyfileobj', side_effect=OSError('write failed')):
            result = await self.restore(archive([('data/keep', 'new')]))
        self.assertEqual(result['status'], 'error')
        self.assertEqual((self.data / 'keep').read_text(), 'old')
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['data'])

    async def test_commit_failure_rolls_back(self):
        (self.data / 'keep').write_text('old', encoding='utf-8')
        replace = mixin_pages.os.replace
        calls = 0
        def failing_replace(src, dst):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('move failed')
            return replace(src, dst)
        with patch.object(mixin_pages.os, 'replace', side_effect=failing_replace):
            result = await self.restore(archive([('data/keep', 'new'), ('data/sub/new', 'new')]))
        self.assertEqual(result['status'], 'error')
        self.assertEqual((self.data / 'keep').read_text(), 'old')
        self.assertFalse((self.data / 'sub').exists())
        self.assertFalse(any(p.name.startswith('ams-restore-') for p in self.root.iterdir()))


@unittest.skipUnless(importlib.util.find_spec('aiohttp'), 'aiohttp is required')
class Security(unittest.IsolatedAsyncioTestCase):
    async def test_post_requires_token_and_origin_without_network(self):
        from panel_server import PanelServer, TOKEN_HEADER
        server = PanelServer(root='.', keys=MagicMock(), port=1)
        async def handler(request):
            from aiohttp import web
            return web.Response(status=200)
        def request(method, token=''):
            return types.SimpleNamespace(method=method, headers={'Host': 'localhost:1',
                                         'Origin': 'http://localhost:1', TOKEN_HEADER: token})
        self.assertEqual((await server._security(request('POST'), handler)).status, 403)
        self.assertEqual((await server._security(request('POST', server.token), handler)).status, 200)
