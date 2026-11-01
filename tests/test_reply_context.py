# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What one reply sees: this place's last day, at most 200 lines, hers and theirs.

Every number here is made up, and every file lives in the test's own temporary
directory. The model is the offline fake; it keeps the messages it was sent.
"""
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_onebot
import history_store
import mixin_phone
import test_turn_runner
import turn
import turn_runner

PLACE = 'group:900001'


class ReplyContextTests(unittest.IsolatedAsyncioTestCase):
    setUp = test_turn_runner.OneTurn.setUp
    close_cached_stores = test_turn_runner.OneTurn.close_cached_stores

    # ------------------------------------------------------------------
    def event(self, text='这条是新的', *, sender='10005', name='小雨',
              message_id='new-1', private=False, called=True):
        parts = [{'type': 'text', 'data': {'text': text}}]
        if called:
            parts.insert(0, {'type': 'at', 'data': {'qq': '20002'}})
        payload = {'post_type': 'message', 'message_type': 'private' if private else 'group',
                   'self_id': 20002, 'user_id': sender, 'group_id': 900001 if not private else '',
                   'message_id': message_id, 'sender': {'user_id': sender, 'nickname': name},
                   'message': parts}
        return turn.TurnEvent(adapter_onebot.from_onebot(payload))

    @staticmethod
    def line(role, text, ts, *, sender='', name='', message_id=''):
        return {'ts': float(ts), 'role': role, 'sender_id': str(sender), 'sender_name': name,
                'msg_id': message_id, 'text': text,
                'origin': {'where': PLACE, 'people': [sender] if sender else [],
                           'source_ids': [message_id] if message_id else [],
                           'visibility': 'public'}}

    def window(self, lines, place=PLACE):
        self.her._write_window(place, {'recent': list(lines), 'open_loops': []})

    def contents(self, contexts):
        return [item['content'] for item in contexts]

    def positions(self, contexts, parts):
        text = '\n'.join(self.contents(contexts))
        return [text.index(part) for part in parts]

    # ------------------------------------------------------------------
    async def test_reply_sees_answered_turns_and_the_lines_she_did_not_answer(self):
        now = time.time()
        rows = [
            # round one: she answered him
            ('user', '第一个问题', '10003', 'Alice', 'w-1', now - 3000),
            ('assistant', '第一个回答', '', '', '', now - 2999),
            # someone she did not answer
            # round two: she answered him again
            ('user', '第二个问题', '10003', 'Alice', 'w-3', now - 2000),
            ('assistant', '第二个回答', '', '', '', now - 1999),
        ]
        for role, text, sender, name, message_id, stamp in rows:
            self.store.append(PLACE, role, text, sender_id=sender, sender_name=name,
                              message_id=message_id, about=(sender,) if sender else (),
                              ts=stamp)
        self.window([
            self.line('user', '第一个问题', now - 3000, sender='10003', name='Alice', message_id='w-1'),
            self.line('assistant', '第一个回答', now - 2999),
            self.line('user', '插一句甲', now - 2500, sender='10004', name='小云', message_id='w-2'),
            self.line('user', '第二个问题', now - 2000, sender='10003', name='Alice', message_id='w-3'),
            self.line('assistant', '第二个回答', now - 1999),
            self.line('user', '插一句乙', now - 1500, sender='10004', name='小云', message_id='w-4'),
            self.line('user', '插一句丙', now - 1000, sender='10004', name='小云', message_id='w-5'),
        ])
        self.fake.say('好的')
        await turn_runner.run_turn(self.her, self.event())

        messages = self.fake.requests[0]['messages']
        contexts = messages[1:-1]
        parts = ['第一个问题', '第一个回答', '插一句甲', '第二个问题', '第二个回答',
                 '插一句乙', '插一句丙']
        found = self.positions(contexts, parts)
        self.assertEqual(found, sorted(found), self.contents(contexts))
        # her two answered turns come from the store once, not again from the window
        self.assertEqual(sum('第一个问题' in x for x in self.contents(contexts)), 1)
        self.assertEqual(sum('第二个问题' in x for x in self.contents(contexts)), 1)
        # the message this reply is to is not history
        self.assertFalse(any('这条是新的' in x for x in self.contents(contexts)))
        self.assertIn('（原文）这条是新的', messages[-1]['content'])

    async def test_only_the_last_day(self):
        now = time.time()
        self.store.append(PLACE, 'user', '一天前的历史', sender_id='10003', message_id='old-h',
                          ts=now - 25 * 3600)
        self.store.append(PLACE, 'user', '一天内的历史', sender_id='10003', message_id='new-h',
                          ts=now - 23 * 3600)
        with patch.object(mixin_phone, 'WINDOW_SECONDS', 48 * 3600):
            self.window([
                self.line('user', '一天前的窗口', now - 25 * 3600, sender='10004',
                          name='小云', message_id='old-w'),
                self.line('user', '一天内的窗口', now - 23 * 3600, sender='10004',
                          name='小云', message_id='new-w'),
            ])
            contexts = self.her._reply_context(self.event())
        text = '\n'.join(self.contents(contexts))
        self.assertIn('一天内的历史', text)
        self.assertIn('一天内的窗口', text)
        self.assertNotIn('一天前的历史', text)
        self.assertNotIn('一天前的窗口', text)

    async def test_at_most_the_last_rows_of_the_day(self):
        now = time.time()
        lines = [self.line('user', '话%03d' % i, now - 250 + i, sender='10004',
                           name='小云', message_id='m-%03d' % i) for i in range(250)]
        self.window(lines)
        contexts = self.her._reply_context(self.event())
        self.assertEqual(len(contexts), history_store.CONTEXT_ROWS)
        text = '\n'.join(self.contents(contexts))
        self.assertIn('话049', text)     # the oldest 50 make room for the newest 200
        self.assertNotIn('话048', text)
        self.assertIn('话249', text)
        self.assertLess(text.index('话049'), text.index('话249'))

    async def test_her_full_words_come_once(self):
        now = time.time()
        long_reply = '这是一段超过八十个字的话' * 8   # 104 characters, all made up
        self.assertTrue(len(long_reply) > mixin_phone.WINDOW_LINE_CHARS)
        self.store.append(PLACE, 'user', '问了一句', sender_id='10003', message_id='w-long',
                          ts=now - 600)
        self.store.append(PLACE, 'assistant', long_reply, about=('10003',), sources=('w-long',),
                          ts=now - 599)
        self.window([
            self.line('user', '问了一句', now - 600, sender='10003', name='Alice',
                      message_id='w-long'),
            self.line('assistant', long_reply[:mixin_phone.WINDOW_LINE_CHARS], now - 599),
        ])
        contexts = self.her._reply_context(self.event())
        self.assertEqual(sum(long_reply in x for x in self.contents(contexts)), 1)
        short = long_reply[:mixin_phone.WINDOW_LINE_CHARS]
        self.assertEqual(sum(short in x for x in self.contents(contexts)), 1)

    async def test_forgetting_leaves_nothing_to_see(self):
        now = time.time()
        gone = '要忘掉的话'
        self.store.append(PLACE, 'user', gone, sender_id='10003', sender_name='Alice',
                          message_id='f-1', ts=now - 600)
        self.store.append(PLACE, 'assistant', '回他的话', about=('10003',), sources=('f-1',),
                          ts=now - 599)
        self.store.append(PLACE, 'user', '留着的话', sender_id='10004', sender_name='小云',
                          message_id='f-2', ts=now - 500)
        self.window([
            self.line('user', gone, now - 600, sender='10003', name='Alice', message_id='f-1'),
            dict(self.line('assistant', '回他的话', now - 599),
                 origin={'where': PLACE, 'people': ['10003'], 'source_ids': ['f-1'],
                         'visibility': 'public'}),
            self.line('user', '留着的话', now - 500, sender='10004', name='小云', message_id='f-2'),
        ])
        self.her._forget(person='10003')
        self.assertEqual([row['content'] for row in self.store.recent(PLACE)], ['留着的话'])
        self.assertEqual([str(x.get('text') or '') for x in self.her._read_window(PLACE)['recent']],
                         ['留着的话'])
        text = '\n'.join(self.contents(self.her._reply_context(self.event())))
        self.assertNotIn(gone, text)
        self.assertNotIn('回他的话', text)
        self.assertIn('留着的话', text)

    async def test_places_stay_apart(self):
        now = time.time()
        self.store.append(PLACE, 'user', '群里的话', sender_id='10004', message_id='g-1',
                          ts=now - 600)
        self.store.append('private:10005', 'user', '私聊的话', sender_id='10005',
                          message_id='p-1', ts=now - 600)
        self.window([self.line('user', '群窗口的话', now - 500, sender='10004',
                               name='小云', message_id='g-2')], place=PLACE)
        self.window([self.line('user', '私窗口的话', now - 500, sender='10005',
                               name='小雨', message_id='p-2')], place='private:10005')
        group = '\n'.join(self.contents(self.her._reply_context(self.event())))
        private = '\n'.join(self.contents(self.her._reply_context(
            self.event(private=True, sender='10005', name='小雨'))))
        self.assertIn('群里的话', group)
        self.assertIn('群窗口的话', group)
        self.assertNotIn('私聊的话', group)
        self.assertNotIn('私窗口的话', group)
        self.assertIn('私聊的话', private)
        self.assertIn('私窗口的话', private)
        self.assertNotIn('群里的话', private)
        self.assertNotIn('群窗口的话', private)

    def test_recent_without_since_is_unchanged(self):
        self.store.append(PLACE, 'user', '第一句', sender_id='10003')
        self.store.append(PLACE, 'assistant', '第二句')
        self.store.append(PLACE, 'user', '第三句', sender_id='10003')
        self.assertEqual(self.store.recent(PLACE, 2),
                         [{'role': 'assistant', 'content': '第二句'},
                          {'role': 'user', 'content': '第三句'}])


if __name__ == '__main__':
    unittest.main()
