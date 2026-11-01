# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Keep local sends within the two media folders and validate raw actions."""
import ast
import asyncio
import base64
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import messenger
import app
import mixin_selfie
import mixin_stickers
import turn_runner
import vision
from adapter_onebot_messenger import OneBotMessenger
from events import Segment

ROOT = Path(__file__).resolve().parent.parent
PNG = b'\x89PNG\r\n\x1a\nmade-up'
IMAGE = 'base64://' + base64.b64encode(PNG).decode('ascii')


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
                   {'type': 'image', 'data': {'file': IMAGE}},
                   {'type': 'record', 'data': {'file': 'base64://AAAA'}}]
        asyncio.run(self.bot.call('send_private_msg', user_id=10001, message=message))
        asyncio.run(self.bot.call('get_msg', message_id='m-1'))
        self.assertEqual([action for action, _ in self.calls], ['send_private_msg', 'get_msg'])

    def test_url_images(self):
        for url in ('http://127.0.0.1:6190/x.png', 'https://example.com/x.png'):
            with self.assertRaises(ValueError):
                asyncio.run(self.bot.send('private:10001', (Segment('image', {'url': url}),)))
        self.assertEqual(self.calls, [])

    def test_base64_images_are_checked(self):
        for value in ('AAAA', 'base64://AAAA', 'base64://bad!',
                      'base64://' + base64.b64encode(PNG + b'x' * (5 * 1024 * 1024)).decode('ascii')):
            with self.subTest(value=value[:20]):
                with self.assertRaises(ValueError):
                    asyncio.run(self.bot.send('private:10001', (Segment('image', {'base64': value}),)))
                with self.assertRaises(messenger.ActionRefused):
                    asyncio.run(self.bot.call('send_private_msg', message=[{'type': 'image', 'data': {'file': value}}]))
        self.assertEqual(self.calls, [])
        asyncio.run(self.bot.send('private:10001', (Segment('image', {'base64': IMAGE}),)))
        asyncio.run(self.bot.call('send_private_msg', message=[{'type': 'image', 'data': {'file': IMAGE}}]))
        self.assertEqual(len(self.calls), 2)

    def test_vision_local_roots(self):
        shots = self.root / 'browser' / 'shots'
        photo = shots / 'b.jpg'
        with patch.object(mixin_selfie, 'SELFIE_DIR', self.root / 'selfie'), \
             patch.object(mixin_selfie, 'SHOT_DIR', shots), \
             patch.object(mixin_stickers, 'STICKERS_DIR', self.root / 'stickers'):
            with patch('pathlib.Path.open') as opened:
                for path in (str(self.root / 'keys.dat'), str(shots / '..' / '..' / 'keys.dat'),
                             r'\\server\share\image.png', r'\\?\C:\image.png'):
                    self.assertEqual(vision._bytes(path), b'')
                opened.assert_not_called()
            self.assertEqual(vision._bytes(str(photo)), b'\xff\xd8\xff\xd9')

    def test_quoted_messages_stay_in_the_same_place(self):
        async def run(kind, place, quote):
            instance = app.App(type('Args', (), {'history': 10})())
            instance.her = object()
            async def lookup(action, params):
                return quote
            seen = []
            async def capture(her, event, **kwargs):
                seen.append(event.incoming)
            instance._lookup = lookup
            frame = {'post_type': 'message', 'message_type': kind, 'self_id': 20002,
                     'user_id': 10001, 'message': [{'type': 'reply', 'data': {'id': '1'}}]}
            if kind == 'group':
                frame['group_id'] = place
            with patch.object(turn_runner, 'run_turn', side_effect=capture):
                await instance.on_event(frame)
            return seen[0]
        message = [{'type': 'text', 'data': {'text': 'made up quote'}}]
        for kind, field, place, other in (('group', 'group_id', 900001, 900002),
                                          ('private', 'user_id', 10001, 10003)):
            for value, expected in ((place, True), (other, False), (None, False)):
                quote = {'message_type': kind, field: value, 'message': message,
                         'sender': {'user_id': 10001}}
                result = asyncio.run(run(kind, place, quote))
                self.assertEqual('made up quote' in str(result), expected)
        for extra, expected in (({}, True), ({'target_id': 10001}, True),
                                ({'peer_id': '10001'}, True), ({'target_id': 10003}, False),
                                ({'peer_id': 10003}, False),
                                ({'target_id': 10001, 'peer_id': 10003}, False),
                                ({'target_id': None}, False)):
            with self.subTest(extra=extra):
                quote = {'message_type': 'private', 'user_id': 20002, 'message': message,
                         'sender': {'user_id': 20002}, **extra}
                result = asyncio.run(run('private', 10001, quote))
                self.assertEqual('made up quote' in str(result), expected)

    def test_app_does_not_allow_the_whole_root(self):
        self.assertNotIn('roots=[root]', (ROOT / 'app.py').read_text(encoding='utf-8'))
