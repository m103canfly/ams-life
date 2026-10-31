# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""One offline turn through her neutral interfaces."""
import ast
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_onebot
import attention
import deepseek_client
import her
import history_store
import messenger
import mixin_attention
import test_her
import tool_loop
import turn
import turn_runner
from fake_deepseek import FakeDeepSeek


class Helpers(unittest.IsolatedAsyncioTestCase):
    def test_messages_of(self):
        contexts = [{'role': 'assistant', 'content': 'old'}]
        req = turn.TurnRequest(prompt='hello', system_prompt='persona', contexts=contexts,
                               extra_user_content_parts=[{'type': 'text', 'text': 'now', '_no_save': True},
                                                         {'type': 'image', 'url': 'ignored'}])
        system, messages = turn_runner.messages_of(req)
        self.assertEqual(system, 'persona')
        self.assertEqual(messages, contexts + [{'role': 'user', 'content': 'hello\n\nnow'}])
        self.assertIsNot(messages, contexts)
        self.assertIsNone(turn_runner.messages_of(turn.TurnRequest())[0])

    async def test_loop_tools_receive_event_and_none(self):
        event = object()
        seen = []

        async def handler(first, **args):
            seen.append((first, args))

        req = turn.TurnRequest(tools=[turn.TurnTool('one', 'desc', {'properties': {}}, handler),
                                      turn.TurnTool('skip', '', {})])
        tools = turn_runner.loop_tools_of(req, event)
        self.assertEqual(len(tools), 1)
        self.assertEqual((tools[0].tool.name, tools[0].tool.description), ('one', 'desc'))
        self.assertEqual(await tools[0].handler(value=3), '')
        self.assertEqual(seen, [(event, {'value': 3})])

    def test_reply_of(self):
        result = tool_loop.LoopResult('words', 1, (('one', {'x': 1}),), {'output': 8}, 'done')
        reply = turn_runner.reply_of(result)
        self.assertEqual((reply.text, reply.tool_calls, reply.usage),
                         ('words', result.calls, {'output': 8}))
        self.assertIsNot(reply.usage, result.usage)
        self.assertEqual(reply.chain_prefix, [])

    def test_import_boundary(self):
        tree = ast.parse((Path(__file__).resolve().parent.parent / 'turn_runner.py').read_text('utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ''] + [a.name for a in node.names]
            else:
                continue
            self.assertFalse(any(n.split('.')[0] in ('main', 'her', 'astrbot') for n in names))


class FakeMessenger:
    def __init__(self, fail=False):
        self.sent = []
        self.fail = fail

    async def send(self, place, segments):
        if self.fail:
            raise RuntimeError('made-up send failure')
        self.sent.append((place, tuple(segments)))
        return messenger.Sent(True, 'made-up')


class OneTurn(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=test_basics.DATA)
        self.addCleanup(self.tmp.cleanup)
        for p in test_her.data_paths(Path(self.tmp.name)):
            p.start()
            self.addCleanup(p.stop)
        self.her = her.Her(test_her.route_collector(), config={
            'self_decide': True, 'reply_groups': ['900001'], 'owner_qq': '10001'})
        self.addCleanup(self.close_cached_stores)
        self.fake = FakeDeepSeek()
        self.her._neutral_model = deepseek_client.DeepSeekModel(api_key='fake-key', model='fake-model', client=self.fake)
        self.sends = FakeMessenger()
        self.her._neutral_messenger = self.sends
        self.her._neutral_persona = '编的人设'
        self.store = history_store.HistoryStore(Path(self.tmp.name) / 'history.sqlite', gate=self.her._history_gate)
        self.addCleanup(self.store.close)
        self.her._history = self.store

    def close_cached_stores(self):
        for name in ('_forget_reg', '_vectors_db'):
            store = getattr(self.her, name, None)
            if store is not None:
                store.close()
                setattr(self.her, name, None)

    def event(self, *, called=True, private=False):
        parts = [{'type': 'text', 'data': {'text': '你好'}}]
        if called:
            parts.insert(0, {'type': 'at', 'data': {'qq': '20002'}})
        payload = {'post_type': 'message', 'message_type': 'private' if private else 'group',
                   'self_id': 20002, 'user_id': 10003, 'group_id': 900001,
                   'message_id': 10001, 'sender': {'user_id': 10003, 'nickname': 'Alice'},
                   'message': parts}
        return turn.TurnEvent(adapter_onebot.from_onebot(payload))

    async def test_called_turn_sends_keeps_and_counts_once(self):
        self.fake.say('你好呀')
        event = self.event()
        reply = await turn_runner.run_turn(self.her, event)
        messages = self.fake.requests[0]['messages']
        self.assertIn('编的人设', messages[0]['content'])
        self.assertIn('[她现在]', messages[-1]['content'])
        self.assertEqual(self.sends.sent, [('group:900001', messenger.text_segments('你好呀'))])
        rows = self.store.recent('group:900001')
        self.assertEqual([row['role'] for row in rows], ['user', 'assistant'])
        self.assertEqual(rows[-1]['content'], reply.text)
        spend = json.loads(mixin_attention.SPEND_PATH.read_text('utf-8'))[time.strftime('%Y-%m-%d')]
        self.assertEqual(spend['calls'], 1)
        self.assertGreater(spend['reply'], 0)

    async def test_uncalled_does_not_reply(self):
        event = self.event(called=False)
        with patch.object(attention, 'is_night', return_value=True):
            self.assertIsNone(await turn_runner.run_turn(self.her, event))
        self.assertEqual((self.fake.requests, self.sends.sent, self.store.recent('group:900001')), ([], [], []))

    async def test_unapproved_private_stops_before_model(self):
        event = self.event(private=True)
        self.assertIsNone(await turn_runner.run_turn(self.her, event))
        self.assertTrue(event.is_stopped())
        self.assertEqual((self.fake.requests, self.sends.sent), ([], []))

    async def test_split_reply_sends_both(self):
        self.fake.say('第一条【下一条】第二条')
        event = self.event()
        with patch.object(attention, 'typing_seconds', return_value=0):
            await turn_runner.run_turn(self.her, event)
            await event._ams_rest_task
        self.assertEqual(self.sends.sent, [('group:900001', messenger.text_segments('第一条')),
                                           ('group:900001', messenger.text_segments('第二条'))])

    async def test_first_send_failure_still_keeps_history(self):
        self.fake.say('你好呀')
        self.sends.fail = True
        with self.assertLogs('turn_runner', level='WARNING'):
            reply = await turn_runner.run_turn(self.her, self.event())
        self.assertEqual(reply.text, '你好呀')
        self.assertEqual(len(self.store.recent('group:900001')), 2)
