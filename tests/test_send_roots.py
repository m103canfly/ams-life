# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Keep local sends within the two media folders and validate raw actions."""
import ast
import asyncio
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import messenger
from adapter_onebot_messenger import OneBotMessenger
from events import Segment

ROOT = Path(__file__).resolve().parent.parent


class SendRoots(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ams-send-roots-', dir=os.environ['TEMP'])
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, data in (('selfie/a.png', b'\x89PNG\r\n\x1a\n'),
                           ('browser/shots/b.jpg', b'\xff\xd8\xff\xd9'),
                           ('keys.dat', b'fake'), ('history.sqlite3', b'fake'),
                           ('memory/x.json', b'{}')):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.calls = []

        async def api(action, params):
            self.calls.append((action, params))
            return {'status': 'ok', 'data': {}}

        source = (ROOT / 'app.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Attribute) and node.func.attr == 'messenger'
                 and any(key.arg == 'roots' for key in node.keywords)]
        self.assertEqual(len(calls), 1)
        roots = next(key.value for key in calls[0].keywords if key.arg == 'roots')
        paths = eval(compile(ast.Expression(roots), 'app.py', 'eval'),
                     {'root': self.root, 'SELFIE_DIR': self.root / 'selfie',
                      'SHOT_DIR': self.root / 'browser' / 'shots'})
        self.bot = OneBotMessenger(api, roots=paths)

    def send_file(self, path):
        return asyncio.run(self.bot.send('private:10001', (Segment('image', {'path': str(path)}),)))

    def test_media_roots_and_other_files(self):
        for name in ('selfie/a.png', 'browser/shots/b.jpg'):
            with self.subTest(name=name):
                self.assertTrue(self.send_file(self.root / name).ok)
        self.assertEqual(len(self.calls), 2)
        self.calls.clear()
        paths = [self.root / name for name in ('keys.dat', 'history.sqlite3', 'memory/x.json')]
        paths += [self.root / 'selfie' / '..' / 'keys.dat', Path('Z:/other.png')]
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.send_file(path)
        self.assertEqual(self.calls, [])

    def test_raw_send_actions(self):
        for action in ('send_private_msg', 'send_group_msg'):
            for value in ('file:///keys.dat', str(self.root / 'keys.dat'),
                          'http://127.0.0.1:6190/x', None):
                for kind in ('image', 'record'):
                    with self.subTest(action=action, value=value, kind=kind):
                        with self.assertRaises(messenger.ActionRefused):
                            asyncio.run(self.bot.call(action, message=[{'type': kind, 'data': {'file': value}}]))
            for message in (None, 'text', [{}], [{'type': 'at', 'data': {}}],
                            [{'type': 'text', 'data': None}]):
                with self.assertRaises(messenger.ActionRefused):
                    asyncio.run(self.bot.call(action, message=message))
        self.assertEqual(self.calls, [])
        message = [{'type': 'text', 'data': {'text': 'hello'}},
                   {'type': 'face', 'data': {'id': '1'}},
                   {'type': 'image', 'data': {'file': 'base64://AAAA'}},
                   {'type': 'record', 'data': {'file': 'base64://AAAA'}}]
        asyncio.run(self.bot.call('send_private_msg', user_id=10001, message=message))
        asyncio.run(self.bot.call('get_msg', message_id='m-1'))
        self.assertEqual([action for action, _ in self.calls], ['send_private_msg', 'get_msg'])

    def test_url_images(self):
        with patch('adapter_onebot_messenger.resolve_host', return_value=['8.8.8.8']):
            for url in ('http://127.0.0.1:6190/x.png', 'http://192.168.1.2/x.png'):
                with self.assertRaises(ValueError):
                    asyncio.run(self.bot.send('private:10001', (Segment('image', {'url': url}),)))
            self.assertEqual(self.calls, [])
            asyncio.run(self.bot.send('private:10001', (Segment('image', {'url': 'https://example.com/x.png'}),)))
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0][1]['message'][0]['data']['file'], 'https://example.com/x.png')
        for addresses in ([], ['8.8.8.8', '192.168.1.2'], ['invalid']):
            with patch('adapter_onebot_messenger.resolve_host', return_value=addresses):
                with self.assertRaises(ValueError):
                    asyncio.run(self.bot.send('private:10001', (Segment('image', {'url': 'https://example.com/x.png'}),)))
        with patch('adapter_onebot_messenger.resolve_host', side_effect=OSError('unresolved')):
            with self.assertRaises(ValueError):
                asyncio.run(self.bot.send('private:10001', (Segment('image', {'url': 'https://example.com/x.png'}),)))
        self.assertEqual(len(self.calls), 1)

    def test_app_does_not_allow_the_whole_root(self):
        self.assertNotIn('roots=[root]', (ROOT / 'app.py').read_text(encoding='utf-8'))
