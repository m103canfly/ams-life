# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Weekly reply samples, their privacy gates and panel routes."""
import importlib.util
import json
import random
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot
import forget_registry
import harness
import likeness
import messenger
import mixin_discretion
import mixin_pages
import mixin_turn
import turn
import turn_runner

STAMP = 1793534400.0
WEEK = likeness.week_of(STAMP)


class Samples(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=test_basics.DATA)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = likeness.Store(self.root, random.Random(7))

    def add(self, person='10003', text='hello'):
        self.store.add('group:900001', 'reply', [{'sender_id': person, 'name': 'Alice', 'text': text}], STAMP)

    def test_limit_random_and_global_state(self):
        state = random.getstate()
        for i in range(350):
            self.add(text=str(i))
        self.assertEqual(len(self.store.samples(WEEK)), 300)
        self.assertEqual(random.getstate(), state)
        self.assertNotEqual([x['context'][0]['text'] for x in self.store.samples(WEEK)], [str(i) for i in range(300)])

    def test_selection_persists_rating_and_public_fields(self):
        for i in range(25):
            self.add(text=str(i))
        chosen = self.store.select(WEEK)
        self.assertEqual(len(chosen), 20)
        self.assertEqual(chosen, likeness.Store(self.root, random.Random(99)).select(WEEK))
        self.assertTrue(self.store.rate(WEEK, chosen[0]['id'], 'like', 'clear'))
        public = likeness.public(self.store.select(WEEK))
        self.assertEqual((public[0]['rating'], public[0]['reason']), ('like', 'clear'))
        encoded = json.dumps(public)
        self.assertNotIn('sender_id', encoded)
        self.assertNotIn('10003', encoded)
        self.assertNotIn('900001', encoded)

    def test_fewer_than_twenty_and_invalid_week(self):
        self.add()
        self.assertEqual(len(self.store.select(WEEK)), 1)
        with self.assertRaises(ValueError):
            self.store.select('../outside')

    def test_ids_are_repeatable_and_distinct_for_duplicate_samples(self):
        with tempfile.TemporaryDirectory(dir=test_basics.DATA) as other:
            second = likeness.Store(other, random.Random(99))
            context = [{'sender_id': '10003', 'name': 'Alice', 'text': 'hello'}]
            for store in (self.store, second):
                for _ in range(2):
                    store.add('group:900001', 'reply', context, STAMP)
            first_ids = [row['id'] for row in self.store.samples(WEEK)]
            self.assertEqual(first_ids, [row['id'] for row in second.samples(WEEK)])
            self.assertEqual(len(set(first_ids)), 2)

    def test_forget_removes_samples_and_selection_without_refill(self):
        self.add('10003')
        self.add('10001')
        self.store.select(WEEK)
        self.assertEqual(self.store.forget('10003'), 2)
        self.assertEqual(len(self.store.samples(WEEK)), 1)
        self.assertEqual(len(self.store.select(WEEK)), 1)


class Admission(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=test_basics.DATA)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plugin = test_basics.make_plugin(harness.FakeContext())
        self.plugin.config = {'reply_groups': ['900001'], 'owner_qq': '10001', 'reply_private': ['10003']}
        self.plugin._forget_reg = forget_registry.ForgetRegistry()
        self.addCleanup(self.plugin._forget_reg.close)
        self.patcher = patch.object(mixin_turn, 'DATA_DIR', self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.lines = [{'role': 'user', 'sender_id': '10003', 'sender_name': 'Alice',
                       'text': 'line %d' % i, 'ts': STAMP, 'msg_id': 'msg-%d' % i} for i in range(6)]
        self.plugin._read_window = lambda place: {'recent': self.lines}

    def event(self, group='900001', sender='10001'):
        fake = harness.FakeEvent('hello', sender=sender, name='Bob', group=group)
        return turn.TurnEvent(adapter_astrbot.from_astrbot(fake))

    def rows(self):
        return likeness.Store(self.root).samples(likeness.week_of(mixin_turn.time.time()))

    def test_group_and_private_admission_and_five_context_lines(self):
        reply = turn.TurnReply(text='answer')
        self.plugin._keep_likeness(self.event(), reply)
        self.plugin._keep_likeness(self.event(group='900002'), reply)
        self.plugin._keep_likeness(self.event(group=None, sender='10003'), reply)
        self.plugin._keep_likeness(self.event(group=None, sender='10001'), reply)
        rows = self.rows()
        self.assertEqual(len(rows), 2)
        self.assertEqual([line['text'] for line in rows[0]['context']],
                         ['line %d' % i for i in range(2, 6)] + ['hello'])
        self.assertEqual(rows[0]['context'][0]['name'], 'Alice')
        self.assertTrue(rows[1]['place'].startswith('private:'))

    def test_registry_filters_context_and_unreadable_fails_closed(self):
        self.plugin._forget_reg.forget_person('10003')
        self.plugin._keep_likeness(self.event(), turn.TurnReply(text='answer'))
        self.assertEqual([row['sender_id'] for row in self.rows()[0]['context']], ['10001'])
        with patch.object(self.plugin, '_may_keep', side_effect=OSError('private details')):
            self.plugin._keep_likeness(self.event(), turn.TurnReply(text='answer'))
        self.assertEqual(len(self.rows()), 1)

    def test_forget_wiring_and_failure_continues(self):
        self.plugin._keep_likeness(self.event(), turn.TurnReply(text='answer'))
        store = likeness.Store(self.root)
        week = likeness.week_of(mixin_turn.time.time())
        store.select(week)
        with patch.object(mixin_discretion, 'DATA_DIR', self.root):
            self.plugin._forget(person='10003')
        self.assertEqual((store.samples(week), store.select(week)), ([], []))
        with patch.object(mixin_discretion.likeness.Store, 'forget', side_effect=OSError('private details')):
            result = self.plugin._forget(person='10003')
        self.assertIn('memories', result)


class SendGate(unittest.IsolatedAsyncioTestCase):
    async def test_send_failure_does_not_sample_but_history_is_called(self):
        her = MagicMock()
        her.enabled = False
        her._on_message = AsyncMock()
        her._decide_turn = AsyncMock(return_value='reply')
        her._ignored_sender.return_value = False
        her._prepare_tools = AsyncMock()
        her._after_reply = AsyncMock()
        her._here.return_value = 'group:900001'
        her._history = None
        her._messenger.return_value.send = AsyncMock(side_effect=OSError('failed'))
        event = turn.TurnEvent(types.SimpleNamespace(text='hello'))
        result = types.SimpleNamespace(text='answer', calls=(), usage={})
        with patch.object(turn_runner.tool_loop, 'run', AsyncMock(return_value=result)):
            await turn_runner.run_turn(her, event)
        her._keep_turn.assert_called_once()
        her._keep_likeness.assert_not_called()
        her._messenger.return_value.send = AsyncMock(return_value=messenger.Sent(False, ''))
        with patch.object(turn_runner.tool_loop, 'run', AsyncMock(return_value=result)):
            await turn_runner.run_turn(her, event)
        her._keep_likeness.assert_not_called()


class PanelHandlers(unittest.IsolatedAsyncioTestCase):
    async def test_get_and_post(self):
        with tempfile.TemporaryDirectory(dir=test_basics.DATA) as tmp:
            plugin = test_basics.make_plugin(harness.FakeContext())
            store = likeness.Store(tmp, random.Random(4))
            store.add('group:900001', 'answer', [{'sender_id': '10003', 'name': 'Alice', 'text': 'hello'}], STAMP)
            request = types.SimpleNamespace(args={'week': WEEK}, get_json=AsyncMock())
            with patch.object(mixin_pages, 'DATA_DIR', Path(tmp)), patch.dict(sys.modules, {'quart': types.SimpleNamespace(request=request)}):
                first = await plugin.page_likeness()
                self.assertEqual(first, await plugin.page_likeness())
                row = first['data'][0]
                self.assertNotIn('10003', json.dumps(row))
                request.get_json.return_value = {'week': WEEK, 'id': row['id'], 'rating': 'unsure', 'reason': 'maybe'}
                self.assertEqual((await plugin.page_likeness_rate())['status'], 'ok')
                self.assertEqual((await plugin.page_likeness())['data'][0]['rating'], 'unsure')


HAS_AIOHTTP = importlib.util.find_spec('aiohttp') is not None


@unittest.skipUnless(HAS_AIOHTTP, 'aiohttp is required')
class PanelSecurity(unittest.IsolatedAsyncioTestCase):
    async def test_host_origin_and_token(self):
        from aiohttp import ClientSession
        import panel_api
        from panel_server import PanelServer, TOKEN_HEADER
        with tempfile.TemporaryDirectory(dir=test_basics.DATA) as tmp:
            collector = panel_api.RouteCollector()
            plugin = test_basics.make_plugin(harness.FakeContext())
            plugin.context = collector
            plugin._register_page_api()
            panel_api.install_request_shim()
            server = PanelServer(root=tmp, keys=MagicMock(), api_routes=panel_api.aiohttp_routes(collector.routes))
            port = await server.start()
            self.addAsyncCleanup(server.stop)
            base = 'http://127.0.0.1:%d' % port
            async with ClientSession() as client:
                async with client.get(base + '/api/page/likeness', headers={'Host': 'wrong'}) as response:
                    self.assertEqual(response.status, 421)
                for headers in ({'Origin': base}, {'Origin': 'http://wrong', TOKEN_HEADER: server.token}):
                    async with client.post(base + '/api/page/likeness/rate', headers=headers, json={}) as response:
                        self.assertEqual(response.status, 403)
