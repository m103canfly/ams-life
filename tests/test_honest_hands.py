# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What her hands and eyes can see, said as it is; a look that failed or was left half done, said too."""
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


class Person(phone.SelfieMixin):
    """The few things life_loop wants from the plugin; the model is a queue of answers."""

    def __init__(self):
        self.enabled = True
        self.config = {'life_loop_enabled': True}
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
    def _read_window(self, here): return {'recent': self.windows[here]}
    def _llm_allowed(self, kind): return self.allowed
    def _red_line(self, text, where): return ''
    def _read_library(self, vectors=True): return {'entries': []}
    def _write_library(self, lib): return True
    async def _persona_text(self, event): return 'A fictional persona.'
    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answers.pop(0) if self.answers else (
            self.answer if isinstance(self.answer, str) else json.dumps(self.answer, ensure_ascii=False))
        return parser(raw)


def choice(action, minutes=30, detail='在这个时候做这个'):
    return json.dumps({'do': action, 'detail': detail, 'minutes': minutes}, ensure_ascii=False)


class HonestHandsTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 2, 10).timestamp())
        for target, name, value in ((life, 'STATE_DIR', self.root / 'states'),
                                    (life, 'DATA_DIR', self.root),
                                    (heybox, 'STATE_DIR', self.root / 'states'),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json'),
                                    (phone, 'LOOK_PATH', self.root / 'states' / 'look.json'),
                                    (phone, 'STATE_DIR', self.root / 'states'),
                                    (life.time, 'time', self.clock)):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = Person()

    def now(self): return datetime.fromtimestamp(self.clock())

    def rows(self): return her_days.Store(self.root).recent(20)

    def materials(self, choices):
        return life.materials(self.p, {}, {}, self.p.core, 'test', self.clock(), choices, False)

    async def tick(self, minutes=0):
        self.clock.advance(minutes * 60)
        return await life.tick(self.p)

    # 1. what the menu shows her, and only what is on it
    async def test_the_menu_says_what_these_things_can_show(self):
        self.p.config.update(heybox_enabled=True)
        with patch.object(life, 'heybox_ready', return_value=True):
            choices = life.menu(self.p)
            self.assertIn('刷小黑盒', choices)
            text = self.materials(choices)
            self.assertIn('这些事能做到什么', text)
            self.assertIn('能看到谁私信了你', text)
            self.p.config['heybox_enabled'] = False
            choices = life.menu(self.p)
            self.assertNotIn('刷小黑盒', choices)
            text = self.materials(choices)
            self.assertNotIn('私信、通知看不到', text)
            self.assertNotIn('这些事能做到什么', text)

    # 2. nothing new to read: the day says so
    async def test_heybox_with_nothing_new_is_written_as_it_is(self):
        self.p.config.update(heybox_enabled=True)
        self.p.answers = [choice('刷小黑盒', 30, '在刷小黑盒')]
        with patch.object(life, 'heybox_ready', return_value=True), \
                patch.object(heybox, 'credential', return_value={'device_id': 'a' * 32, 'cookies': {}}), \
                patch.object(heybox, 'read_request', return_value={}), \
                patch.object(heybox, 'feed_items', return_value=[]), \
                patch.object(heybox, 'unseen', return_value=[]):
            self.assertTrue(await self.tick())
        self.assertIn('能看到谁私信了你', self.p.calls[0][1])
        self.assertEqual(self.rows()[0]['detail'], '想刷小黑盒，没看成：没有新帖子')

    # 3. six looks today already: the day says why
    async def test_heybox_when_today_is_already_full_is_written_as_it_is(self):
        self.p.config.update(heybox_enabled=True)
        day = self.now().date().isoformat()
        heybox.write_json(heybox.STATE_DIR / 'heybox-usage.json', {'date': day, 'count': 6})
        self.p.answers = [choice('刷小黑盒', 30, '在刷小黑盒')]
        with patch.object(life, 'heybox_ready', return_value=True), \
                patch.object(heybox, 'read_request') as request:
            self.assertTrue(await self.tick())
            request.assert_not_called()
        self.assertEqual(self.rows()[0]['detail'], '想刷小黑盒，没看成：今天刷够了')

    # 4. one post read: how many, no title
    async def test_heybox_one_post_read_is_counted_without_its_title(self):
        self.p.config.update(heybox_enabled=True)
        self.p.answers = [choice('刷小黑盒', 30, '在刷小黑盒'),
                          '{"read":["1"]}', '{"thought":"","tell":""}']
        for name, value in (('credential', {'device_id': 'a' * 32, 'cookies': {}}),
                            ('read_request', {}),
                            ('feed_items', [{'id': '1', 'title': '假标题'}]),
                            ('post_text', '假正文'), ('comment_texts', [])):
            caller = patch.object(heybox, name, return_value=value)
            caller.start()
            self.addCleanup(caller.stop)
        with patch.object(life, 'heybox_ready', return_value=True), \
                patch.object(heybox, 'unseen', side_effect=lambda posts, now: posts), \
                patch.object(heybox, 'mark_seen'):
            self.assertTrue(await self.tick())
        detail = self.rows()[0]['detail']
        self.assertEqual(detail, '看了 1 篇')
        self.assertNotIn('假标题', detail)
        self.assertEqual(life.read_state()['last_item_id'], self.rows()[0]['id'])

    # 5. a song put down after 20 of its 60 minutes
    async def test_a_song_put_down_early_says_how_far_it_got(self):
        self.p.answers = [choice('写歌', 60, '在写歌')]
        self.assertTrue(await self.tick())
        self.assertEqual(self.rows()[0]['do'], '写歌')
        self.assertEqual(self.rows()[0]['minutes'], 60)
        self.p.core.hunger = .75          # her body crosses a line
        self.p.answers = [choice('吃饭', 30, '在吃饭')]
        self.assertTrue(await self.tick(20))
        song = [row for row in self.rows() if row['do'] == '写歌'][0]
        self.assertEqual(song['stopped_after'], 20)
        self.assertEqual(song['minutes'], 60)
        text = self.materials(life.menu(self.p))
        self.assertIn('打算 60 分钟，做了 20 分钟就放下了', text)

    # 6. a song that ran its whole time was not put down
    async def test_a_song_that_ran_its_whole_time_was_not_put_down(self):
        self.p.answers = [choice('写歌', 60, '在写歌')]
        self.assertTrue(await self.tick())
        self.p.answers = [choice('吃饭', 30, '在吃饭')]
        self.assertTrue(await self.tick(60))
        song = [row for row in self.rows() if row['do'] == '写歌'][0]
        self.assertNotIn('stopped_after', song)
        self.assertEqual(song['minutes'], 60)

    # 7. dazing and sleeping are not things put down
    async def test_dazing_or_sleeping_is_not_a_thing_put_down(self):
        def value(action, minutes):
            return {'do': action, 'detail': '在这个时候做这个', 'minutes': minutes,
                    'liked_last': '', 'post': '', 'look': '', 'wish': '', 'used_wishes': []}

        start = self.clock()
        await life.apply_choice(self.p, value('发呆', 120), self.p.core, start, False)
        await life.apply_choice(self.p, value('休息', 30), self.p.core, start + 1800, False)
        self.assertNotIn('stopped_after', [row for row in self.rows() if row['do'] == '发呆'][0])
        self.p.core.sleepiness = .9
        await life.apply_choice(self.p, value('睡觉', 60), self.p.core, start + 3600, False)
        await life.apply_choice(self.p, value('休息', 30), self.p.core, start + 5400, False)
        sleep = [row for row in self.rows() if row['do'] == '睡觉'][0]
        self.assertNotIn('stopped_after', sleep)

    # 8. the looks that are not hers (on waking) never write a day line
    async def test_the_automatic_look_never_writes_a_day_line(self):
        self.p.config.update(heybox_enabled=True)
        await life.apply_choice(self.p, {'do': '休息', 'detail': '在家里歇着', 'minutes': 30,
                                         'liked_last': '', 'post': '', 'look': '', 'wish': '',
                                         'used_wishes': []}, self.p.core, self.clock(), False)
        before = self.rows()
        with patch.object(life, 'heybox_ready', return_value=True), \
                patch.object(heybox, 'credential', return_value={'device_id': 'a' * 32, 'cookies': {}}), \
                patch.object(heybox, 'read_request', return_value={}), \
                patch.object(heybox, 'feed_items', return_value=[]), \
                patch.object(heybox, 'unseen', return_value=[]):
            self.assertFalse(await life.automatic_heybox(self.p, self.clock(), 'wake'))
        self.assertEqual(self.rows(), before)
        self.assertEqual(self.p.calls, [])


class StoreFields(unittest.TestCase):
    """Her days can be corrected in place; an id that is gone changes nothing."""

    TS = 1_793_000_000.0

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = her_days.Store(self.root)
        self.day = datetime.fromtimestamp(self.TS).date().isoformat()
        self.path = self.root / 'her_days' / (self.day + '.jsonl')

    def test_detail_and_stopped_are_written_in_place(self):
        row = self.store.add({'ts': self.TS, 'do': '写歌', 'detail': '在写歌', 'minutes': 60})
        self.assertTrue(self.store.set_detail(row['id'], '在窗边看树'))
        self.assertTrue(self.store.set_stopped(row['id'], 12))
        kept = self.store.day(self.day)[0]
        self.assertEqual((kept['detail'], kept['stopped_after'], kept['minutes']), ('在窗边看树', 12, 60))

    def test_a_missing_id_says_false_and_changes_no_file(self):
        row = self.store.add({'ts': self.TS, 'do': '休息', 'detail': '看树', 'minutes': 30})
        before = self.path.read_bytes()
        self.assertFalse(self.store.set_detail('missing', '别的'))
        self.assertFalse(self.store.set_stopped('missing', 10))
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.store.day(self.day)[0]['id'], row['id'])
        empty = her_days.Store(self.root / 'nothing')
        self.assertFalse(empty.set_detail('missing', '别的'))
        self.assertFalse(empty.set_stopped('missing', 10))
        self.assertFalse((self.root / 'nothing').exists())


if __name__ == '__main__':
    unittest.main()
