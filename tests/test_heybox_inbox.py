# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""One look at 小黑盒 also sees the private messages and the notices: who wrote, how many
are unread and the last line, kept for that look only and never written into her day,
memory or state. Offline: every answer here is a fake in the shape the trial read showed."""
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import body  # noqa: E402
import harness  # noqa: E402
import her_days  # noqa: E402
import heybox  # noqa: E402
import life_loop as life  # noqa: E402
import mixin_selfie as phone  # noqa: E402

# made up: one conversation with four unread, one with none, and a last line to protect
NAME = '虚构甲'
QUIET = '虚构乙'
LAST_LINE = '明天记得带伞，外面要下雨'
OTHER_LINE = '不用回我'
SAVED = {'device_id': 'a' * 32, 'cookies': {}}
POST = {'links': [{'link_id': '10001', 'title': '假标题'}]}


def conversation(count=4, name=NAME, text=LAST_LINE, key='username'):
    """One row of `messages`, as the trial read showed it (avatar and name in user_a)."""
    return {'count': count, 'text': text, 'message_id': '9001',
            'user_a': {key: name} if name is not None else {}}


def read_result(messages=None, header=None, unread=None):
    """The trial read's own shape: header, messages, message_unread_num and two flags."""
    if messages is None:
        messages = [conversation(), conversation(count=0, name=QUIET, text=OTHER_LINE, key='nickname')]
    if header is None:
        header = [{'count': 0, 'text': '回复', 'user_a': {}},
                  {'count': 0, 'text': '赞', 'user_a': {}},
                  {'count': 0, 'text': '关注', 'user_a': {}},
                  {'count': 0, 'text': '系统', 'user_a': {}}]
    return {'header': header, 'messages': messages,
            'message_unread_num': dict(unread or {'award': 0, 'comment': 0}),
            'feedback_unread': 0, 'community_notify': 0}


class Admits(unittest.TestCase):
    """1. the one address added, and no others. No files: a refused address sends nothing."""

    def test_the_message_address_is_the_only_one_added(self):
        self.assertEqual(heybox.PATHS, frozenset((
            '/account/get_qrcode_url/', '/account/qr_state/',
            '/bbs/app/feeds', '/bbs/app/link/tree', '/bbs/app/user/message')))

    def test_other_addresses_are_still_not_sent(self):
        for path in ('/chat/send_message/', '/bbs/app/link/like', '/bbs/app/user/message/read'):
            with self.subTest(path=path), patch('heybox.build_opener') as opener:
                self.assertEqual(heybox.request(path, {}, 'device', '', now=100), (None, []))
                opener.assert_not_called()


class Inbox(unittest.TestCase):
    """2-4. what is taken from the answer, and what is quietly left out."""

    def test_only_the_unread_conversation_is_carried(self):
        self.assertEqual(heybox.inbox(read_result()), {
            'messages': [{'name': NAME, 'count': 4, 'text': LAST_LINE}], 'notices': []})

    def test_at_most_five_conversations(self):
        rows = [conversation(count=1, name='虚构%d' % index) for index in range(8)]
        got = heybox.inbox(read_result(messages=rows))
        self.assertEqual([row['name'] for row in got['messages']],
                         ['虚构0', '虚构1', '虚构2', '虚构3', '虚构4'])

    def test_a_conversation_without_a_name_is_somebody(self):
        for user_a in ({}, {'avatar': 'picture'}, None, 'not a person', {'username': '', 'name': 7}):
            with self.subTest(user_a=user_a):
                row = conversation()
                row['user_a'] = user_a
                got = heybox.inbox(read_result(messages=[row]))
                self.assertEqual(got['messages'], [{'name': '有人', 'count': 4, 'text': LAST_LINE}])

    def test_the_name_keys_are_tried_in_order(self):
        for key, value in (('username', '甲'), ('nickname', '乙'), ('name', '丙')):
            with self.subTest(key=key):
                row = conversation()
                row['user_a'] = {key: value}
                got = heybox.inbox(read_result(messages=[row]))
                self.assertEqual(got['messages'][0]['name'], value)
        row = conversation()
        row['user_a'] = {'username': '', 'nickname': '先看它', 'name': '再看它'}
        self.assertEqual(heybox.inbox(read_result(messages=[row]))['messages'][0]['name'], '先看它')

    def test_the_last_line_is_stripped_and_cut_short(self):
        row = conversation(text='<p>' + '字' * 80 + '</p>')
        self.assertEqual(heybox.inbox(read_result(messages=[row]))['messages'][0]['text'], '字' * 60)

    def test_the_notices_are_the_header_labels_and_the_other_counts(self):
        got = heybox.inbox(read_result(
            header=[{'count': 2, 'text': '回复'}, {'count': 0, 'text': '赞'},
                    {'count': 3, 'text': '关注'}],
            unread={'award': 1, 'comment': 0, 'like': '2'}))
        self.assertEqual(got['notices'], [{'text': '回复', 'count': 2},
                                          {'text': '关注', 'count': 3},
                                          {'text': 'award', 'count': 1}])

    def test_missing_or_wrong_fields_skip_that_row_and_do_not_raise(self):
        got = heybox.inbox({
            'messages': ['not a row', {'count': '4'}, {'count': True}, {'count': -1},
                         {'count': 2}, {'count': 3, 'text': 12, 'user_a': {'nickname': 9}}],
            'header': ['not a row', {'count': '2', 'text': '回复'}, {'count': 1},
                       {'count': 2, 'text': ' 回复 '}],
            'message_unread_num': {'award': '3', 'comment': 2, 'like': True}})
        self.assertEqual(got['messages'], [{'name': '有人', 'count': 2, 'text': ''},
                                           {'name': '有人', 'count': 3, 'text': ''}])
        self.assertEqual(got['notices'], [{'text': '回复', 'count': 2},
                                          {'text': 'comment', 'count': 2}])
        for empty in ({}, None, [], 'not a result'):
            with self.subTest(empty=empty):
                self.assertEqual(heybox.inbox(empty), {'messages': [], 'notices': []})


class Person(phone.SelfieMixin):
    """The few things one look at 小黑盒 wants from the plugin; the model is a queue."""

    def __init__(self):
        self.enabled = True
        self.config = {'life_loop_enabled': True, 'heybox_enabled': True}
        self._neutral_model = object()
        self.browse_groups_enabled = self.browse_trips_enabled = False
        self.core = body.BioCore()
        self.core.sleepiness = self.core.hunger = self.core.physical_fatigue = .1
        self.core._life_now_path = phone.NOW_PATH
        self.core._life_state_path = life.STATE_DIR / 'life.json'
        self.windows = {}
        self.self_model = {}
        self.spent = 0
        self.allowed = True
        self.calls = []
        self.answers = []
        self.answer = {'do': '休息', 'detail': '在家里歇着', 'minutes': 30}
        self.memories = []
        self._key_store = object()
        self._make_photo = AsyncMock(return_value=None)
        self._save_self_model = Mock()
        self._maybe_write_notebook = AsyncMock(return_value=True)

    def _core(self, event=None): return self.core
    def _attention_cfg(self): return {'soft': 8, 'hard': 10}
    def _spent_today(self): return self.spent
    def _browse_on(self): return self.config.get('browse_enabled', False)
    def _browse_names(self): return self._known_names(self._names_index())
    def _names_index(self): return {}
    def _known_names(self, people): return [str(person) for person in people]
    def _here(self, event): return event.place if event else ''
    def _addresses_her(self, event): return event.at_me
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows.get(here, [])}
    def _llm_allowed(self, kind): return self.allowed
    def _red_line(self, text, where): return ''
    def _read_library(self, vectors=True): return {'entries': list(self.memories)}
    def _write_library(self, lib):
        self.memories = lib['entries']
        return True
    def _new_memory_id(self, *args): return 'memory'
    def _job_stale(self): return False
    async def _embed_text(self, text): return [0.3, 0.4]
    async def _persona_text(self, event): return 'A fictional persona.'

    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answers.pop(0) if self.answers else json.dumps(self.answer, ensure_ascii=False)
        return parser(raw)


class Look(unittest.IsolatedAsyncioTestCase):
    """5-10. what one look asks, what it says in the day, and what it marks as private."""

    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 2, 10).timestamp())
        for target, name, value in ((life, 'STATE_DIR', self.root / 'states'),
                                    (life, 'DATA_DIR', self.root),
                                    (life, 'heybox_ready', lambda plugin: True),
                                    (heybox, 'STATE_DIR', self.root / 'states'),
                                    (heybox, 'credential', lambda keys: dict(SAVED)),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json'),
                                    (phone, 'LOOK_PATH', self.root / 'states' / 'look.json'),
                                    (phone, 'STATE_DIR', self.root / 'states'),
                                    (life.time, 'time', self.clock)):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = Person()

    def requests(self, message_result=None, feed=None):
        """A fake read of each address: the message answer is the test's, the rest a stub."""
        calls = []

        def read(path, params, saved):
            calls.append(path)
            if path == '/bbs/app/user/message':
                return message_result
            if path.endswith('/feeds'):
                return feed or {}
            if params.get('owner_only') == 1:
                return {'link': {'text': '<p>假正文</p>'}}
            return {'comments': [{'text': '假评论'}]}

        return read, calls

    def day_row(self, detail='在刷小黑盒'):
        return her_days.Store(self.root).add({'ts': self.clock(), 'do': '刷小黑盒',
                                              'detail': detail, 'minutes': 30})

    def impression(self):
        return [text for kind, text in self.p.calls if kind == 'heybox'][-1]

    # 5. a post and a private message: both are material, the private part said as it is
    async def test_a_post_and_a_private_message_are_asked_together(self):
        read, _calls = self.requests(message_result=read_result(), feed=POST)
        self.p.answers = ['{"read":["10001"]}', '{"thought":"有点意思","tell":""}']
        with patch.object(heybox, 'read_request', side_effect=read):
            result = await life.browse_heybox(self.p, self.clock())
        self.assertEqual(result.read, 1)
        prompt = self.impression()
        self.assertIn('小黑盒资料', prompt)
        for must in ('小黑盒的私信', '只能在他面前说', '回不了', '看不到完整的对话', NAME, LAST_LINE):
            self.assertIn(must, prompt)

    # 6. nothing new on the front page: the private messages are still asked once
    async def test_no_new_posts_but_a_private_message_is_still_asked_once(self):
        read, calls = self.requests(message_result=read_result(), feed={})
        self.p.answers = ['{"thought":"有人记着我","tell":""}']
        row = self.day_row()
        life.save_state({'last_item_id': row['id']})
        with patch.object(heybox, 'read_request', side_effect=read):
            result = await life.browse_heybox(self.p, self.clock())
            self.assertTrue(life.day_heybox_line(result))
        self.assertEqual((result.read, result.why), (0, '没有新帖子'))
        self.assertEqual(len(self.p.calls), 1)
        prompt = self.p.calls[0][1]
        self.assertNotIn('小黑盒资料', prompt)
        self.assertIn(NAME, prompt)
        self.assertIn(LAST_LINE, prompt)
        self.assertEqual(calls, ['/bbs/app/user/message', '/bbs/app/feeds'])
        self.assertEqual(her_days.Store(self.root).recent(5)[0]['detail'], '没有新帖子；有 4 条私信')

    # 7. a private name or line is not kept, not sent; "有人私信我" is said
    async def test_a_private_name_or_line_is_not_kept_and_not_sent(self):
        cases = [(NAME + '人挺好', '', False, False),
                 ('她说外面要下雨，让我带伞', '', False, False),
                 ('今天有点累', NAME + '说外面要下雨', True, False),
                 ('今天有点累', '有人私信我', True, True)]
        self.p.config['proactive_owner_enabled'] = True
        for thought, tell, kept, sent in cases:
            with self.subTest(thought=thought, tell=tell):
                read, _calls = self.requests(message_result=read_result(), feed=POST)
                self.p.memories = []
                self.p.answers = ['{"read":["10001"]}',
                                  json.dumps({'thought': thought, 'tell': tell}, ensure_ascii=False)]
                with patch.object(heybox, 'read_request', side_effect=read), \
                        patch.object(heybox, 'mark_seen'), \
                        patch.object(life, 'tell_owner', AsyncMock()) as told:
                    await life.browse_heybox(self.p, self.clock())
                self.assertEqual(bool(self.p.memories), kept)
                self.assertEqual(told.await_count, 1 if sent else 0)

    # 8. the message read failed: the front page is read all the same, and said as it is
    async def test_a_failed_message_read_does_not_stop_the_front_page(self):
        read, calls = self.requests(message_result=None, feed=POST)
        self.p.answers = ['{"read":["10001"]}', '{"thought":"有点意思","tell":""}']
        with patch.object(heybox, 'read_request', side_effect=read):
            result = await life.browse_heybox(self.p, self.clock())
        self.assertEqual(result.read, 1)
        self.assertEqual(calls[0], '/bbs/app/user/message')
        self.assertIn('/bbs/app/feeds', calls)
        self.assertFalse(result.seen)
        self.assertIn('这次没看到私信和通知', self.impression())

    # 9. neither the name nor the line reaches her day, memory or state files
    async def test_no_name_or_line_of_it_reaches_her_files(self):
        read, _calls = self.requests(message_result=read_result(), feed={})
        self.p.answers = [json.dumps({'do': '刷小黑盒', 'detail': '在刷小黑盒', 'minutes': 30},
                                     ensure_ascii=False),
                          '{"thought":"看到有人留言，有点惦记","tell":""}']
        with patch.object(heybox, 'read_request', side_effect=read):
            self.assertTrue(await life.tick(self.p))
        self.assertEqual(her_days.Store(self.root).recent(5)[0]['detail'], '没有新帖子；有 4 条私信')
        self.assertEqual([row['text'] for row in self.p.memories], ['看到有人留言，有点惦记'])
        files = [path for path in self.root.rglob('*') if path.is_file()]
        self.assertTrue(files)
        for path in files:
            text = path.read_text(encoding='utf-8', errors='replace')
            for value in (NAME, QUIET, LAST_LINE, OTHER_LINE):
                self.assertNotIn(value, text, str(path))
        for value in (NAME, LAST_LINE):
            self.assertNotIn(value, str(self.p.memories))

    # 10. one look adds one request; the seventh look of a day does not happen
    async def test_one_look_adds_one_request_and_six_are_the_most(self):
        read, calls = self.requests(message_result=read_result(), feed=POST)
        self.p.answers = ['{"read":["10001"]}', '{"thought":"","tell":""}']
        with patch.object(heybox, 'read_request', side_effect=read):
            await life.browse_heybox(self.p, self.clock())
        self.assertEqual(calls, ['/bbs/app/user/message', '/bbs/app/feeds',
                                 '/bbs/app/link/tree', '/bbs/app/link/tree'])
        day = life.datetime.fromtimestamp(self.clock()).date().isoformat()
        heybox.write_json(heybox.STATE_DIR / 'heybox-usage.json', {'date': day, 'count': 6})
        with patch.object(heybox, 'read_request', side_effect=read):
            self.assertFalse(await life.browse_heybox(self.p, self.clock()))
        self.assertEqual(calls, ['/bbs/app/user/message', '/bbs/app/feeds',
                                 '/bbs/app/link/tree', '/bbs/app/link/tree'])


if __name__ == '__main__':
    unittest.main()
