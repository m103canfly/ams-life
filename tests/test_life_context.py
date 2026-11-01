# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What she sees when she thinks: his chat, her wishes, and what may not go public."""
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot_turn  # noqa: E402
import body  # noqa: E402
import discretion  # noqa: E402
import events  # noqa: E402
import harness  # noqa: E402
import her_days  # noqa: E402
import heybox  # noqa: E402
import history_store  # noqa: E402
import life_loop as life  # noqa: E402
import messenger  # noqa: E402
import mixin_selfie as phone  # noqa: E402
import turn  # noqa: E402
import turn_runner  # noqa: E402

OWNER = '10001'          # a made-up number
NAMED = '阿柚'            # a made-up name: the owner_name setting
OTHER = '10003'          # a made-up number
PRIVATE_SECRET = '明天去医院复查'
NOW_WORDS = '在虚构此刻暗号里坐着'


class Person(phone.SelfieMixin):
    """The few things life_loop and turn_runner want from the plugin; nothing on disk."""

    def __init__(self):
        self.enabled = True
        self.config = {'life_loop_enabled': True, 'owner_qq': OWNER, 'owner_name': NAMED,
                       'proactive_owner_enabled': True, 'qzone_enabled': True}
        self._neutral_model = object()
        self.browse_groups_enabled = self.browse_trips_enabled = False
        self.core = body.BioCore()
        self.core.sleepiness = self.core.hunger = self.core.physical_fatigue = .1
        self.core.last_sleep_end = self.core.last_meal = 0
        self.core._life_now_path = phone.NOW_PATH
        self.core._life_state_path = life.STATE_DIR / 'life.json'
        self.windows = {}
        self.self_model = {}
        self.calls = []
        self.forbidden = []
        self.replies = []
        self.answer = {'do': '休息', 'detail': '在家里坐着', 'minutes': 30}
        self._history = None
        self._neutral_messenger = None
        self._make_photo = AsyncMock(return_value=None)
        self._save_self_model = Mock()

    def _core(self, event=None): return self.core

    def _attention_cfg(self): return {'soft': 8, 'hard': 10}
    def _spent_today(self): return 0
    def _browse_on(self): return False
    def _browse_names(self): return self._known_names(self._names_index())
    def _names_index(self): return {OWNER: {NAMED}, OTHER: {'虚构小乙'}}
    def _known_names(self, people):
        return [name for person in people for name in [str(person), *self._names_index().get(person, set())]]
    def _here(self, event):
        return '' if event is None else adapter_astrbot_turn.incoming_of(event).place
    def _speaker(self, event):
        incoming = adapter_astrbot_turn.incoming_of(event)
        return incoming.sender_id, incoming.sender_name
    def _addresses_her(self, event): return False
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows.get(here, [])}
    def _llm_allowed(self, kind): return True
    def _read_library(self, vectors=True): return {'entries': []}
    def _write_library(self, lib): return True
    def _window_add_reply(self, event, text): self.replies.append((self._here(event), text))
    def _forbid(self, event, ident, text, people, vec=None):
        self.forbidden.append({'id': ident, 'text': text})
    def _red_line(self, text, where): return ''
    def _owner_rules(self): return []
    def _history_store(self): return self._history
    def _source_ids(self, event): return []

    async def _persona_text(self, event): return 'A fictional persona.'
    async def _check_reply(self, event, text): return {'leak': False}
    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answer if isinstance(self.answer, str) else json.dumps(self.answer, ensure_ascii=False)
        return parser(raw)


class RecordingModel:
    """One model that records what it was sent."""

    def __init__(self, words):
        self.words = words
        self.requests = []

    async def chat(self, **kwargs):
        self.requests.append(kwargs)
        return SimpleNamespace(text=self.words, tool_calls=(), usage={}, reasoning='')


class LifeContextTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 1, 10).timestamp())
        for target, name, value in ((life.time, 'time', self.clock),
                                    (life, 'STATE_DIR', self.root / 'states'),
                                    (life, 'DATA_DIR', self.root),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json'),
                                    (phone, 'LOOK_PATH', self.root / 'states' / 'look.json'),
                                    (phone, 'STATE_DIR', self.root / 'states')):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = Person()
        self.p.core.last_sleep_end = self.p.core.last_meal = self.clock()

    def now(self):
        return datetime.fromtimestamp(self.clock())

    def chat(self, rows):
        self.p.windows['private:' + OWNER] = rows

    def materials(self):
        return life.materials(self.p, {}, {}, self.p.core, 'test', self.clock(), ['休息'], False)

    def rows(self):
        return her_days.Store(self.root).recent(5)

    async def test_materials_show_both_sides_with_time(self):
        now = self.clock()
        self.chat([{'role': 'user', 'ts': now - 600, 'text': PRIVATE_SECRET},
                   {'role': 'assistant', 'ts': now - 300, 'text': '好，我记着'}])
        text = self.materials()
        early = datetime.fromtimestamp(now - 600).strftime('%m-%d %H:%M')
        late = datetime.fromtimestamp(now - 300).strftime('%m-%d %H:%M')
        self.assertIn('%s %s：%s' % (early, NAMED, PRIVATE_SECRET), text)
        self.assertIn('%s 她：好，我记着' % late, text)

    async def test_materials_prompt_does_not_nudge(self):
        text = self.materials()
        self.assertIn('"tell"', text)
        self.assertNotIn('"post"', text)
        self.assertNotIn('还没回的有', text)
        self.assertNotIn('想和%s说什么就在 tell 写一句' % NAMED, text)
        self.assertIn('要是想跟%s说点什么就写在 tell，不写也行' % NAMED, text)

    async def test_public_line_is_a_separate_call_without_the_chat_or_now(self):
        now = self.clock()
        self.chat([{'role': 'user', 'ts': now - 60, 'text': '秘密私聊字眼'}])
        self.p._set_now('家里', NOW_WORDS, now=self.now(), minutes=5, source='her', kind='休息')
        self.p.answer = {'do': '发说说', 'minutes': 5}
        self.clock.advance(301)
        self.assertTrue(await life.tick(self.p))
        self.assertEqual(len(self.p.calls), 2)
        first, second = (prompt for _kind, prompt in self.p.calls)
        self.assertIn('秘密私聊字眼', first)
        self.assertIn(NOW_WORDS, first)
        self.assertNotIn('秘密私聊字眼', second)
        self.assertNotIn(NOW_WORDS, second)
        self.assertIn('{"post"', second)

    async def test_private_detail_is_not_kept_but_an_unrelated_one_is(self):
        self.chat([{'role': 'user', 'ts': self.clock() - 120, 'text': PRIVATE_SECRET}])
        self.p.answer = {'do': '休息', 'detail': '在担心明天复查', 'minutes': 10}
        self.assertTrue(await life.tick(self.p))
        self.assertEqual(life.current()['doing'], '休息')
        self.assertEqual(self.rows()[0]['detail'], '')
        self.clock.advance(11 * 60)
        self.p.answer = {'do': '休息', 'detail': '在家里看树', 'minutes': 10}
        self.assertTrue(await life.tick(self.p))
        self.assertEqual(self.rows()[0]['detail'], '在家里看树')

    def heybox_plugin(self, answers, entries):
        prompts = []

        async def call(kind, prompt, parser, **kwargs):
            prompts.append(prompt)
            return parser(answers.pop(0))

        plugin = SimpleNamespace(
            enabled=True,
            config={'life_loop_enabled': True, 'heybox_enabled': True, 'owner_qq': OWNER,
                    'owner_name': NAMED, 'proactive_owner_enabled': True},
            self_model={}, _key_store=object(), _spent_today=lambda: 0,
            _attention_cfg=lambda: {'soft': 8, 'hard': 10}, _llm_allowed=lambda kind: True,
            _persona_text=AsyncMock(return_value='fictional'), _llm_v2_call=call,
            _red_line=lambda text, where: '', _read_library=lambda **kwargs: {'entries': entries},
            _write_library=Mock(return_value=True), _new_memory_id=lambda *args: 'memory',
            _job_stale=lambda: False, _embed_text=AsyncMock(return_value=[0.3, 0.4]),
            _here=lambda event: adapter_astrbot_turn.incoming_of(event).place,
            _speaker=lambda event: (OWNER, ''),
            _read_window=lambda place: {'recent': self.p.windows.get(place, [])})
        return plugin, prompts

    async def run_heybox(self, thought, entries):
        plugin, prompts = self.heybox_plugin(['{"read":["1"]}', json.dumps({'thought': thought, 'tell': ''},
                                                                          ensure_ascii=False)], entries)
        with patch.object(life, 'current', return_value={}), \
                patch.object(life, 'read_state', return_value={}), \
                patch.object(life, 'heybox_ready', return_value=True), \
                patch.object(heybox, 'credential', return_value={'device_id': 'a' * 32,
                                                                 'cookies': {'x_xhh_tokenid': 'fake'}}), \
                patch.object(heybox, 'read_json', return_value={}), \
                patch.object(heybox, 'write_json'), \
                patch.object(heybox, 'feed_items', return_value=[{'id': '1', 'title': '假标题'}]), \
                patch.object(heybox, 'unseen', side_effect=lambda posts, now: posts), \
                patch.object(heybox, 'post_text', return_value='假正文'), \
                patch.object(heybox, 'comment_texts', return_value=['假评论']), \
                patch.object(heybox, 'mark_seen'), \
                patch.object(heybox, 'read_request', return_value={}):
            self.assertTrue(await life.browse_heybox(plugin, self.clock()))
        return prompts

    async def test_heybox_thought_that_repeats_the_chat_is_not_kept(self):
        self.chat([{'role': 'user', 'ts': self.clock() - 60, 'text': PRIVATE_SECRET}])
        entries = []
        await self.run_heybox('在担心明天复查', entries)
        self.assertEqual(entries, [])
        await self.run_heybox('这个帖子讲的是虚构的故事', entries)
        self.assertEqual([entry['text'] for entry in entries], ['这个帖子讲的是虚构的故事'])

    async def test_notebook_wishes_only_where_he_can_be_told(self):
        self.p.self_model = {'notebook': [
            {'text': '我想去看虚构的海', 'section': '想做的',
             'origin': discretion.make_origin(discretion.SELF)},
            {'text': '别处私聊的打算', 'section': '想做的',
             'origin': discretion.make_origin('private:' + OTHER, [OTHER])},
            {'text': '每天早睡', 'section': '习惯',
             'origin': discretion.make_origin(discretion.SELF)}]}
        text = self.materials()
        self.assertIn('我想去看虚构的海', text)
        self.assertNotIn('别处私聊的打算', text)
        self.assertNotIn('每天早睡', text)

    async def test_sent_words_are_in_the_history_a_reply_reads(self):
        store = history_store.HistoryStore(self.root / 'history.sqlite3')
        self.addCleanup(store.close)
        self.p._history = store
        self.p._neutral_messenger = SimpleNamespace(send=AsyncMock(return_value=messenger.Sent(True, '')))
        with patch.object(life, 'read_state', return_value={}), \
                patch.object(life, 'current', return_value={}):
            self.assertTrue(await life.tell_owner(self.p, '你今天在做什么呀', self.clock(), []))
        self.assertEqual(store.recent('private:' + OWNER),
                         [{'role': 'assistant', 'content': '你今天在做什么呀'}])
        model = RecordingModel('在想你呢')
        self.p._neutral_model = model
        self.p._messenger = lambda event: SimpleNamespace(send=AsyncMock(return_value=messenger.Sent(True, '')))
        self.p._on_message = AsyncMock()
        self.p._decide_turn = AsyncMock(return_value='reply')
        self.p._ignored_sender = Mock(return_value=False)
        self.p._prepare_tools = AsyncMock()
        self.p._prepare_turn = AsyncMock()
        self.p._after_reply = AsyncMock()
        self.p._group_reply_open = Mock()
        self.p._group_reply_after = Mock()
        self.p._keep_turn = Mock()
        self.p._keep_likeness = Mock()
        event = turn.TurnEvent(events.Incoming('private:' + OWNER, OWNER, '', '', '', (), False,
                                               '', (), True, False, self.clock(), '在干嘛'))
        await turn_runner.run_turn(self.p, event, history_limit=20)
        messages = model.requests[0]['messages']
        self.assertEqual([row['content'] for row in messages],
                         ['你今天在做什么呀', '在干嘛'])


if __name__ == '__main__':
    unittest.main()
