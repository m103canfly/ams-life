# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for the last reply walls."""
import asyncio
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import discretion
import harness
import impressions
import main
import mixin_discretion
import mixin_send_check as walls
import send_check
from astrbot.api.provider import LLMResponse


class SendWalls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = impressions.Store(self.root / 'people')
        self.user_patch = patch.object(mixin_discretion, 'USER_DIR', self.root)
        self.user_patch.start()
        self.addCleanup(self.user_patch.stop)
        self.p = main.BioCorePlugin(harness.FakeContext(), config={})
        self.p._impression_store = lambda: self.store
        self.p._present_people = lambda event: set()
        self.p._read_library = lambda vectors=False: {'entries': []}
        self.p._event_archive = lambda limit, read_only=False: []
        self.p.self_model = {'notebook': []}
        self.p._embedding_runtime_config = lambda: None

    def person(self, person, name, sessions):
        self.store.keep_names(person, [name])
        if sessions is not None:
            (self.root / (person + '.json')).write_text(json.dumps({'sessions': sessions}), encoding='utf-8')

    def event(self, group=None, sender='10001'):
        return harness.FakeEvent('hello', sender=sender, group=group)

    def check(self, event, reply):
        return asyncio.run(self.p._check_reply(event, reply))

    def test_group_names_and_unknown(self):
        self.person('10003', '紫藤旅人', ['group:900001'])
        self.person('20002', '青竹旅人', ['group:900002'])
        self.person('10005', '琥珀旅人', None)
        event = self.event('900002')
        with patch.object(walls.logger, 'info') as log:
            self.assertTrue(self.check(event, '紫藤旅人来了')['leak'])
            self.assertFalse(self.check(event, '青竹旅人来了')['leak'])
            self.assertFalse(self.check(event, '琥珀旅人来了')['leak'])
        self.assertTrue(any(call.args[-1] == 1 for call in log.call_args_list))

    def test_one_character_name_in_ordinary_text(self):
        self.person('10003', '鹿', ['group:900001'])
        self.assertFalse(self.check(self.event('900002'), '小鹿乱撞')['leak'])

    def test_private_name_and_shared_group(self):
        self.person('10003', '紫藤旅人', ['private:20002'])
        self.person('20002', '青竹旅人', ['group:900001'])
        self.person('10001', '琥珀旅人', ['group:900001'])
        self.assertTrue(self.check(self.event(), '紫藤旅人来了')['leak'])
        self.assertFalse(self.check(self.event(), '青竹旅人来了')['leak'])
        self.p.config['shared_groups'] = [['900001', '900002']]
        self.assertFalse(self.check(self.event('900002'), '青竹旅人来了')['leak'])

    def test_after_reply_checks_names_with_global_memory_off(self):
        self.person('10003', '紫藤旅人', ['group:900001'])
        p = self.p
        p.enabled = True
        p.global_memory = False
        p.self_decide = False
        p._ignored_sender = lambda event: False
        p._browse_on = lambda: False
        p._continue_job = MagicMock()
        p._check_registry = MagicMock()
        p._core = lambda event: MagicMock()
        p._sticker_named = lambda event, reply, text: (text, '')
        p._stickers_on = lambda: False
        p._count_check = MagicMock()
        p._redo_reply = AsyncMock(return_value=None)
        event = self.event('900002')
        event._ams_phone_queue = {'voice': 'queued'}
        asyncio.run(p.on_llm_response(event, LLMResponse('紫藤旅人来了')))
        self.assertTrue(event.stopped)
        self.assertEqual(event._ams_check['outcome'], 'held')
        self.assertEqual(event._ams_phone_queue, {})

    def test_private_words_and_user_echo(self):
        secret = '蓝鲸三号'
        item = {'id': 'm', 'text': secret, 'origin': discretion.make_origin('private:10003', ['10003'])}
        self.p._read_library = lambda vectors=False: {'entries': [item]}
        group = self.event('900002')
        self.p._forbid(group, 'memory:m', secret)
        self.assertTrue(self.check(group, '蓝 鲸 三 号')['leak'])
        self.assertTrue(self.check(group, '蓝，鲸，三，号')['leak'])
        group._ams_check['user_text'] = '蓝鲸三号是谁的？'
        self.assertFalse(self.check(group, '蓝鲸三号是谁的？')['leak'])
        self.assertTrue(self.check(group, '蓝鲸三号是主人私聊里说的')['leak'])
        self.assertFalse(self.check(self.event(sender='10003'), secret)['leak'])
        self.assertFalse(self.check(group, 'l j s h')['leak'])

    def test_public_group_and_self_are_not_private_words(self):
        self.p._read_library = lambda vectors=False: {'entries': [
            {'id': 'public', 'text': '蓝鲸三号', 'origin': discretion.make_origin('group:900001', ['10003'])},
            {'id': 'self', 'text': '琥珀行程', 'origin': discretion.make_origin('self')}]}
        event = self.event('900002')
        self.assertFalse(self.check(event, '蓝鲸三号')['leak'])
        self.assertFalse(self.check(event, '琥珀行程')['leak'])

    def test_unrecalled_private_library_does_not_block_ordinary_reply(self):
        entries = [{'id': str(i), 'text': '今天晚上吃什么呀哈哈哈哈好的',
                    'origin': discretion.make_origin('private:10003', ['10003'])} for i in range(40)]
        self.p._read_library = lambda vectors=False: {'entries': entries}
        event = self.event('900002')
        self.p._redo_reply = AsyncMock(return_value=None)
        self.p._count_check = MagicMock()
        self.assertEqual(asyncio.run(self.p._look_at_reply(event, LLMResponse('今天晚上一起打游戏吗'),
                                                          '今天晚上一起打游戏吗')),
                         '今天晚上一起打游戏吗')
        self.p._redo_reply.assert_not_awaited()

    def test_dropped_memory_with_global_memory_off_is_checked(self):
        p = self.p
        p.global_memory = False
        p._usable_memory_text = lambda text: True
        p._schedule_consolidation = lambda *args: None
        p._save_memory = lambda *args: None
        p._load_memory = lambda event: {'entries': []}
        p._memory_top_k = lambda *args: 3
        p._cosine = lambda *args: 0.8
        p._memory_score = lambda *args, **kwargs: 1.0
        p._restabilize_if_expired = lambda *args: False
        p._chain_event_lines = lambda *args, **kwargs: []
        item = {'id': 'm', 'text': '暗号蓝鲸三号', 'vector': [1.0],
                'origin': discretion.make_origin('private:10003', ['10003'])}
        p._cross_session_memory_entries = lambda event: [('private:10003', item)]
        event = self.event('900002')
        asyncio.run(p._memory_recall(event, '暗号是什么', vec=[1.0]))
        self.assertTrue(self.check(event, '暗号蓝鲸三号')['leak'])
        self.assertEqual(event._ams_check['forbidden'][0]['vec'], [1.0])

    def test_group_private_recall_records_words_without_names(self):
        p = self.p
        p.global_memory = True
        item = {'id': 'm', 'text': '暗号蓝鲸三号', 'vector': [1.0], 'sender_id': '10003',
                'origin': discretion.make_origin('group:900001', ['10003'], visibility=discretion.PRIVATE)}
        p._cross_session_memory_entries = lambda event: [('group:900001', item)]
        p._cosine = lambda *args: 0.8
        p._memory_score = lambda *args, **kwargs: 1.0
        event = self.event('900002')
        p._labeled_elsewhere(event, [1.0], None, [])
        self.assertTrue(self.check(event, '暗号蓝鲸三号')['leak'])
        self.assertEqual(event._ams_check['forbidden'][0]['names'], [])

    def test_remote_embedding_never_called(self):
        self.p.self_model = {'notebook': [{'id': 'n', 'text': '蓝鲸三号',
            'origin': discretion.make_origin('private:10003', ['10003'])}]}
        self.p._embed_text = AsyncMock(return_value=[1.0])
        self.p._embedding_runtime_config = lambda: {'base_url': 'https://example.invalid'}
        event = self.event('900002')
        self.p._notebook_for(event)
        self.check(event, '普通回话')
        self.p._embed_text.assert_not_awaited()
        self.p._embedding_runtime_config = lambda: {'base_url': 'http://localhost'}
        self.check(event, '普通回话')
        self.assertGreaterEqual(self.p._embed_text.await_count, 2)
