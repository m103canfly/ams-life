# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Sleepiness decides sleep: how fast it moves, how long she sleeps, and when a quiet chat may reach her."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import body
import harness
import life_loop as life
import mixin_selfie as phone


def make_core():
    """A body with the life loop on and known numbers; no files are read."""
    core = body.BioCore()
    core.sleepiness, core.hunger, core.physical_fatigue = .2, .3, .1
    core.v, core.stress, core.energy = 0.0, 0.1, 0.5
    core._life_now_path = 'now.json'
    return core


def advance(core, start, hours, chosen=()):
    """Advance her needs over a stretch; `chosen` stands in for her life intervals."""
    with patch.object(body, '_chosen_needs', return_value=list(chosen)):
        body._advance_needs(core, start, start + hours * 3600.0)


class Rates(unittest.TestCase):
    def test_awake_in_the_day_rises_0_035_an_hour(self):
        core = make_core()
        advance(core, datetime(2026, 11, 2, 9).timestamp(), 1)
        self.assertAlmostEqual(core.sleepiness, .235)
        self.assertAlmostEqual(core.physical_fatigue, .12)

    def test_awake_at_night_rises_0_06_an_hour(self):
        for hour in (23, 0, 3, 6):
            core = make_core()
            advance(core, datetime(2026, 11, 2, hour).timestamp(), 1)
            self.assertAlmostEqual(core.sleepiness, .26)

    def test_asleep_falls_0_066_an_hour(self):
        core = make_core()
        start = datetime(2026, 11, 2, 1).timestamp()
        advance(core, start, 1, [(start, start + 3 * 3600, True)])
        self.assertAlmostEqual(core.sleepiness, .134)

    def test_the_schedule_counts_as_sleep_only_with_the_loop_off(self):
        early = datetime(2026, 11, 2, 1).timestamp()
        off = make_core()
        off.__dict__.pop('_life_now_path')
        advance(off, early, 1)
        self.assertAlmostEqual(off.sleepiness, .134)
        on = make_core()
        advance(on, early, 1)
        self.assertAlmostEqual(on.sleepiness, .26)

    def test_seven_am_crosses_0_7_about_quarter_to_eleven(self):
        core = make_core()
        core.sleepiness = .15
        start = datetime(2026, 11, 2, 7).timestamp()
        advance(core, start, 15.5)                      # 22:30, still short of 0.7
        self.assertLess(core.sleepiness, .7)
        advance(core, start + 15.5 * 3600, .25)         # 22:45
        self.assertGreaterEqual(core.sleepiness, .7)
        self.assertLess(core.sleepiness, .71)


class Lengths(unittest.TestCase):
    def test_a_night_sleep_started_at_quarter_to_eleven_ends_about_seven(self):
        start = datetime(2026, 11, 2, 22, 45)
        minutes = life.sleep_minutes(.7, start.timestamp())
        wake = start + timedelta(minutes=minutes)
        self.assertGreaterEqual(wake.hour * 60 + wake.minute, 6 * 60 + 30)
        self.assertLessEqual(wake.hour * 60 + wake.minute, 7 * 60 + 30)

    def test_an_afternoon_nap_is_twenty_to_ninety_minutes(self):
        start = datetime(2026, 11, 2, 14)
        self.assertEqual(life.sleep_minutes(.55, start.timestamp()), 90)
        self.assertEqual(life.sleep_minutes(.3, start.timestamp()), 20)
        self.assertEqual(life.sleep_minutes(.9, start.timestamp()), 90)

    def test_a_late_night_is_nine_hours_or_more_but_at_most_ten(self):
        late = datetime(2026, 11, 3, 1)
        self.assertEqual(life.sleep_minutes(.82, late.timestamp()), 600)
        self.assertGreaterEqual(life.sleep_minutes(.8, late.timestamp()), 9 * 60)
        self.assertLessEqual(life.sleep_minutes(1.0, late.timestamp()), 10 * 60)

    def test_the_night_starts_at_eight_and_ends_at_six(self):
        at_eight = datetime(2026, 11, 2, 20)
        at_dusk = datetime(2026, 11, 2, 19, 59)
        before_six = datetime(2026, 11, 3, 5, 59)
        at_six = datetime(2026, 11, 3, 6)
        self.assertEqual(life.sleep_minutes(.6, at_eight.timestamp()), 409)
        self.assertEqual(life.sleep_minutes(.6, at_dusk.timestamp()), 90)
        self.assertEqual(life.sleep_minutes(.6, before_six.timestamp()), 409)
        self.assertEqual(life.sleep_minutes(.6, at_six.timestamp()), 90)


class Person(phone.SelfieMixin):
    """The few things life_loop wants from the plugin; all files stay in the test's own folder."""

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
        self.calls = []
        self.answer = {'do': '什么都不干', 'detail': '在家里发呆', 'minutes': 30}
        self._maybe_write_notebook = AsyncMock(return_value=True)
        self._save_self_model = Mock()

    def _core(self, event=None): return self.core
    def _attention_cfg(self): return {'soft': 8, 'hard': 10}
    def _spent_today(self): return 0
    def _browse_on(self): return False
    def _browse_names(self): return self._known_names(self._names_index())
    def _names_index(self): return {'10001': {'虚构小甲'}}
    def _known_names(self, people):
        return [name for person in people for name in [str(person), *self._names_index().get(person, set())]]
    def _here(self, event): return ''
    def _addresses_her(self, event): return bool(getattr(event, 'at_me', False))
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows.get(here, [])}
    def _llm_allowed(self, kind): return True
    async def _persona_text(self, event): return 'A fictional persona.'
    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answer if isinstance(self.answer, str) else json.dumps(self.answer, ensure_ascii=False)
        return parser(raw)


class WithTheClock(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 1, 10).timestamp())
        for target, name, value in ((life, 'STATE_DIR', self.root / 'states'),
                                    (life, 'DATA_DIR', self.root),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json'),
                                    (phone, 'LOOK_PATH', self.root / 'states' / 'look.json'),
                                    (phone, 'STATE_DIR', self.root / 'states'),
                                    (life.time, 'time', self.clock)):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = Person()

    async def asyncTearDown(self):
        await life.stop(self.p)

    def now(self):
        return datetime.fromtimestamp(self.clock())

    async def tick(self, minutes=0):
        self.clock.advance(minutes * 60)
        return await life.tick(self.p)


class SleepingAtOnce(WithTheClock):
    async def choose_sleep(self, sleepiness, start, reported):
        self.clock.now = start.timestamp()
        self.p.core.last_tick = self.clock()
        self.p.core._life_body_loaded = True   # the running loop already has its body
        self.p.core.sleepiness = sleepiness
        value = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': reported,
                 'liked_last': '', 'post': '', 'look': '', 'used_wishes': []}
        await life.apply_choice(self.p, value, self.p.core, self.clock(), '')
        return life.read_state()['sleep'], life.current()

    async def test_at_quarter_to_eleven_a_sleep_ends_between_half_six_and_half_seven(self):
        sleep, item = await self.choose_sleep(.7, datetime(2026, 11, 2, 22, 45), 30)
        self.assertEqual(sleep['end'] - sleep['start'], 500 * 60)
        self.assertEqual(item['minutes'], 500)
        wake = datetime.fromtimestamp(sleep['end'])
        self.assertGreaterEqual(wake.hour * 60 + wake.minute, 6 * 60 + 30)
        self.assertLessEqual(wake.hour * 60 + wake.minute, 7 * 60 + 30)

    async def test_what_she_writes_in_minutes_is_not_used(self):
        sleep, item = await self.choose_sleep(.7, datetime(2026, 11, 2, 22, 45), 999)
        self.assertEqual(sleep['end'] - sleep['start'], 500 * 60)
        self.assertEqual(item['minutes'], 500)

    async def test_an_afternoon_nap_is_short_and_a_mild_one_twenty_minutes(self):
        sleep, item = await self.choose_sleep(.55, datetime(2026, 11, 2, 14), 120)
        self.assertEqual(sleep['end'] - sleep['start'], 90 * 60)
        self.assertEqual(item['minutes'], 90)
        sleep, item = await self.choose_sleep(.3, datetime(2026, 11, 2, 14), 120)
        self.assertEqual(sleep['end'] - sleep['start'], 20 * 60)
        self.assertEqual(item['minutes'], 20)

    async def test_a_late_night_sleeps_ten_hours(self):
        sleep, item = await self.choose_sleep(.82, datetime(2026, 11, 3, 1), 60)
        self.assertEqual(sleep['end'] - sleep['start'], 600 * 60)
        self.assertEqual(item['minutes'], 600)

    async def test_she_wakes_when_the_sleep_the_body_chose_is_over(self):
        await self.choose_sleep(.3, datetime(2026, 11, 2, 14), 120)
        self.assertEqual(len(self.p.calls), 0)
        self.assertTrue(await self.tick(20))
        self.assertEqual(len(self.p.calls), 1)
        self.assertNotIn('sleep', life.read_state())


class QuietWhileBusy(WithTheClock):
    async def test_a_quiet_chat_does_not_cut_her_work(self):
        self.p._set_now('家里', '看书', now=self.now(), minutes=120, source='her', kind='看书')
        self.p.windows['group:900001'] = [{'role': 'assistant', 'ts': self.clock()}]
        life.note_called(self.p, SimpleNamespace(place='group:900001', at_me=True))
        for _ in range(20):
            self.assertFalse(await self.tick(1))
        self.assertEqual(self.p.calls, [])

    async def test_a_quiet_chat_reaches_her_while_she_is_dazing(self):
        self.p._set_now('家里', '发呆', now=self.now(), minutes=120, source='her', kind='什么都不干')
        self.p.windows['group:900001'] = [{'role': 'assistant', 'ts': self.clock()}]
        life.note_called(self.p, SimpleNamespace(place='group:900001', at_me=True))
        self.assertTrue(await self.tick(10))
        self.assertEqual(len(self.p.calls), 1)
        self.assertIn('静下来了', self.p.calls[0][1])

    async def test_a_finished_thing_lets_her_think(self):
        self.p._set_now('家里', '看书', now=self.now(), minutes=5, source='her', kind='看书')
        self.assertTrue(await self.tick(6))
        self.assertEqual(len(self.p.calls), 1)
        self.assertIn('刚才那件事到时候了', self.p.calls[0][1])

    async def test_a_crossing_line_reaches_her_even_while_busy(self):
        self.p._set_now('家里', '看书', now=self.now(), minutes=120, source='her', kind='看书')
        self.p.core.hunger = .6
        await self.tick(1)
        self.p.core.hunger = .75
        self.assertTrue(await self.tick(1))
        self.assertEqual(len(self.p.calls), 1)
        self.assertIn('身体有了新的感觉', self.p.calls[0][1])


if __name__ == '__main__':
    unittest.main()
