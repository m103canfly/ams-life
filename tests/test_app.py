# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for the standalone entry point."""
import ast
import asyncio
import importlib.util
import json
import logging
import os
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import app
import common

HAS_AIOHTTP = importlib.util.find_spec('aiohttp') is not None


class EntryTests(unittest.TestCase):
    def test_panel_llm_selection_requires_complete_custom_settings(self):
        self.assertIsNone(app.panel_llm_config({'llm': {'source': 'astrbot'}}))
        self.assertIsNone(app.panel_llm_config({'llm': {'source': 'custom', 'model': 'made-up-model'}}))
        self.assertEqual(app.panel_llm_config({'llm': {'source': 'custom',
                         'base_url': 'https://api.deepseek.com/v1', 'model': 'made-up-model'}}),
                         ('https://api.deepseek.com/v1', 'made-up-model'))

    def test_log_data_directory_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'logs' / 'app.log'
            self.assertEqual(app.main(['--data', str(test_basics.DATA / 'other'), '--log', str(path)]), 2)
            self.assertIn('data directory differs', path.read_text('utf-8'))
            path.unlink()

    def test_log_repeated_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'app.log'
            handlers = logging.getLogger().handlers[:]
            for _ in range(2):
                self.assertEqual(app.main(['--data', str(test_basics.DATA / 'other'), '--log', str(path)]), 2)
                self.assertEqual(logging.getLogger().handlers, handlers)
            self.assertEqual(path.read_text('utf-8').count('data directory differs'), 2)
            path.unlink()

    def test_refuses_live_and_different_data(self):
        original = os.environ.get('AMS_LIFE_DATA_DIR')
        self.addCleanup(self.restore_env, original)
        live = test_basics.DATA / 'astrbot' / 'data' / 'plugin_data' / 'example'
        self.assertEqual(app.main(['--data', str(live)]), 2)
        self.assertEqual(app.main(['--data', str(test_basics.DATA / 'other')]), 2)
        self.assertEqual(os.environ.get('AMS_LIFE_DATA_DIR'), original)

    @staticmethod
    def restore_env(original):
        if original is None:
            os.environ.pop('AMS_LIFE_DATA_DIR', None)
        else:
            os.environ['AMS_LIFE_DATA_DIR'] = original

    def test_compat_selection(self):
        original = sys.path[:]
        self.addCleanup(lambda: sys.path.__setitem__(slice(None), original))
        path = str(Path(app.__file__).resolve().parent / 'compat')
        sys.path[:] = [item for item in sys.path if item != path]
        app.ensure_astrbot(lambda name: object())
        self.assertNotIn(path, sys.path)

        def missing(name):
            raise ModuleNotFoundError(name)

        app.ensure_astrbot(missing)
        self.assertEqual(sys.path[0], path)

    def test_source_boundary(self):
        tree = ast.parse(Path(app.__file__).read_text('utf-8'))
        imports = [alias.name for node in ast.walk(tree) if isinstance(node, ast.Import)
                   for alias in node.names]
        imports += [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        self.assertNotIn('main', imports)
        self.assertIn('127.0.0.1', Path(app.__file__).read_text('utf-8'))


@unittest.skipUnless(HAS_AIOHTTP, 'aiohttp is not installed')
class AppTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import deepseek_client
        import test_her
        from fake_deepseek import FakeDeepSeek
        self.original_env = os.environ.get('AMS_LIFE_DATA_DIR')
        self.addCleanup(EntryTests.restore_env, self.original_env)
        self.tmp = tempfile.TemporaryDirectory(dir=test_basics.DATA)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for p in test_her.data_paths(self.root):
            p.start()
            self.addCleanup(p.stop)
        crypt = patch('key_store._crypt', side_effect=lambda data, protect: data)
        crypt.start()
        self.addCleanup(crypt.stop)
        from key_store import KeyStore
        keys = KeyStore(self.root / 'keys.dat')
        keys.set('deepseek', 'test-deepseek-key')
        keys.set('napcat', 'test-napcat-key')
        (self.root / 'config.json').write_text(json.dumps({'reply_groups': ['900001'],
                                                           'owner_qq': '10001'}), encoding='utf-8')
        self.fake = FakeDeepSeek()
        model = deepseek_client.DeepSeekModel(api_key='test-deepseek-key', model='fake', client=self.fake)
        args = Namespace(data=str(self.root), onebot_port=0, panel_port=0, model='fake', history=20)
        self.app = app.App(args, model=model)
        self.addCleanup(self.close_cached_stores)
        self.addAsyncCleanup(self.app.stop)

    def close_cached_stores(self):
        for name in ('_forget_reg', '_vectors_db'):
            store = getattr(self.app.her, name, None)
            if store is not None:
                store.close()
                setattr(self.app.her, name, None)

    async def start(self):
        self.ports = await self.app.start()
        return self.ports

    async def wait_for(self, predicate):
        for _ in range(500):
            if predicate():
                return
            await asyncio.sleep(.01)
        self.fail('event was not processed')

    async def test_log_file_and_close(self):
        path = self.root / 'logs' / 'app.log'
        self.app.args.log = str(path)
        await self.start()
        logging.getLogger('ams-life').warning('Made up warning')
        content = path.read_text('utf-8')
        self.assertIn('OneBot port:', content)
        self.assertIn('Made up warning', content)
        self.assertNotIn('test-deepseek-key', content)
        self.assertNotIn('test-napcat-key', content)
        handler = self.app._log_handler
        await self.app.stop()
        self.assertNotIn(handler, logging.getLogger().handlers)
        self.assertIsNone(handler.stream)
        path.unlink()

    async def test_no_log_file_by_default(self):
        await self.start()
        self.assertIsNone(self.app._log_handler)
        self.assertFalse((self.root / 'logs').exists())

    async def test_group_turn_and_history(self):
        from fake_napcat import FakeNapCat
        await self.start()
        self.fake.say('Made up reply')
        async with FakeNapCat(url='http://127.0.0.1:%d/ws' % self.ports['onebot'], token='test-napcat-key') as nap:
            await nap.send_event(nap.group_message(group='900001', user='10003', text='hello', at_me=True))
            await self.wait_for(lambda: len(self.app.history.recent('group:900001')) == 2)
            self.assertTrue(any(action == 'send_group_msg' for action, _ in nap.calls))
            self.assertIn('Made up reply', str(nap.sent))

    async def test_reply_and_member_name(self):
        from fake_napcat import FakeNapCat
        import turn_runner
        await self.start()
        seen = []

        async def capture(her, event, **kwargs):
            seen.append(event.incoming)

        with patch.object(turn_runner, 'run_turn', side_effect=capture):
            async with FakeNapCat(url='http://127.0.0.1:%d/ws' % self.ports['onebot'], token='test-napcat-key') as nap:
                nap.answer('get_group_member_info', {'card': 'Made up name'})
                frame = nap.group_message(group='900001', user='10003', text='hello', reply_to='10001')
                frame['message'].append({'type': 'at', 'data': {'qq': '10005'}})
                await nap.send_event(frame)
                await self.wait_for(lambda: bool(seen))
                self.assertEqual(sum(a == 'get_msg' for a, _ in nap.calls), 1)
                self.assertEqual(sum(a == 'get_group_member_info' for a, _ in nap.calls), 1)
                self.assertIn('Made up name', str(seen[0]))

    async def test_self_messages_do_not_call_model(self):
        from fake_napcat import FakeNapCat
        import turn_runner
        await self.start()
        seen = []

        async def capture(her, event, **kwargs):
            seen.append(event.incoming)

        with patch.object(turn_runner, 'run_turn', side_effect=capture):
            async with FakeNapCat(url='http://127.0.0.1:%d/ws' % self.ports['onebot'], token='test-napcat-key') as nap:
                frame = nap.group_message(group='900001', user='20002', at_me=True)
                await nap.send_event(frame)
                frame['post_type'] = 'message_sent'
                await nap.send_event(frame)
                await nap.send_event(nap.group_message(group='900001', user='10003', text='hello'))
                await self.wait_for(lambda: bool(seen))
                await self.wait_for(lambda: not self.app.onebot._events)
                self.assertEqual([incoming.sender_id for incoming in seen], ['10003'])
                self.assertEqual(self.fake.requests, [])

    async def test_missing_key_panel(self):
        import aiohttp
        from key_store import KeyStore
        KeyStore(self.root / 'keys.dat').clear('napcat')
        ports = await self.start()
        self.assertIsNone(ports['onebot'])
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:%d/api/page/status' % ports['panel']) as response:
                self.assertEqual(response.status, 200)

    async def test_bad_persona(self):
        (self.root / 'persona.md').write_bytes(b'\xff')
        ports = await self.start()
        self.assertIsNotNone(ports['onebot'])
        self.assertEqual(self.app.her._neutral_persona, '')

    async def test_bad_deepseek_key_keeps_panel(self):
        import aiohttp
        path = self.root / 'keys.dat'
        data = json.loads(path.read_text('utf-8'))
        data['keys']['deepseek'] = 'not*base64'
        path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertLogs('ams-life.app', level='WARNING') as logs:
            ports = await self.start()
        self.assertIsNone(ports['onebot'])
        self.assertIn('deepseek', '\n'.join(logs.output))
        self.assertIn('cannot decrypt', '\n'.join(logs.output))
        self.assertNotIn('not*base64', '\n'.join(logs.output))
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:%d/api/page/status' % ports['panel']) as response:
                self.assertEqual(response.status, 200)

    async def test_bad_vision_key_keeps_onebot(self):
        path = self.root / 'keys.dat'
        data = json.loads(path.read_text('utf-8'))
        data['keys']['vision'] = 'not*base64'
        path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertLogs('ams-life.app', level='WARNING') as logs:
            ports = await self.start()
        self.assertIsNotNone(ports['onebot'])
        self.assertIn('vision', '\n'.join(logs.output))
        self.assertNotIn('not*base64', '\n'.join(logs.output))

    async def test_stop_and_self_decide(self):
        import aiohttp
        original_config = (self.root / 'config.json').read_bytes()
        ports = await self.start()
        task = self.app.her._autonomy_task
        self.assertTrue(self.app.her.self_decide)
        self.assertEqual((self.root / 'config.json').read_bytes(), original_config)
        async with aiohttp.ClientSession() as session:
            base = 'http://127.0.0.1:%d' % ports['panel']
            url = base + '/api/page/toggle'
            async with session.post(url, json={'key': 'proactive_reply', 'value': True},
                                    headers={'X-AMS-Token': self.app.panel.token, 'Origin': base}) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual((await response.json())['status'], 'ok')
        config = json.loads((self.root / 'config.json').read_text('utf-8'))
        self.assertIsNot(config.get('self_decide'), True)
        self.assertIs(config.get('proactive_reply'), True)
        await self.app.stop()
        self.assertTrue(task.done())
        for port in ports.values():
            with self.assertRaises(OSError):
                await asyncio.open_connection('127.0.0.1', port)
