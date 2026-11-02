# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""One sleep for both sides (card E2s): the reply side follows life_loop.asleep, a call while
asleep is weighed by how sleepy she is and who calls, and the calls she slept through are kept
for her first thinking awake. All made up: no network, a fake plugin, a fake clock."""
import json
import shutil
import sys
import tempfile
import time as clock_module
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import attention  # noqa: E402
import body  # noqa: E402
import harness  # noqa: E402
import life_loop as life  # noqa: E402
import mixin_attention  # noqa: E402
import mixin_group_browse  # noqa: E402
import mixin_selfie as phone  # noqa: E402


class Event:
    def __init__(self, here, why='', sender='10002', text='随便说说'):
        self.here, self.why, self.sender, self.text = here, why, sender, text
        self.is_at_or_wake_command = False
        self.stopped = False

    def stop_event(self):
        self.stopped = True


class Person(phone.SelfieMixin, mixin_attention.AttentionMixin):
    """The few things the decision and the life loop want; all files stay in the test's folder."""

    def __init__(self, life_on=True):
        self.enabled = True
        self.config = {'life_loop_enabled': life_on, 'owner_qq': '10009'}
        self.self_decide = True
        self.mood_events_enabled = False
        self._neutral_model = object()
        self.core = body.BioCore()
        self.core.sleepiness = self.core.hunger = self.core.physical_fatigue = .1
        self.core._life_now_path = phone.NOW_PATH
        self.core._life_state_path = life.STATE_DIR / 'life.json'
        self._attention_state = {}
        self.windows = {}
        self.self_model = {}
        self.familiar = {}
        self.calls = []
        self.mood = []
        self.score = 0.0
        self.answer = {'do': '什么都不干', 'detail': '在家里发呆', 'minutes': 30}
        self._maybe_write_notebook = AsyncMock(return_value=True)
        self._save_self_model = Mock()

    def _core(self, event=None): return self.core
    def _private_allowed(self, event): return True
    def _message_may_speak(self, event): return True
    def _here(self, event): return event.here if event else ''
    def _speaker(self, event): return event.sender, ''
    def _why_called(self, event): return event.why
    def _note_tie(self, person, called_her=False, private=False): pass
    def _familiarity(self, person): return float(self.familiar.get(str(person), 0.0))
    def _hear_mood(self, event): pass
    def _mood_clock(self, now=None): pass
    def _save_attention(self): pass
    def _attention_cfg(self):
        return {'owner': '10009', 'level': 'normal', 'soft': 8.0, 'hard': 10.0,
                'night_start': '01:00', 'night_end': '08:25', 'group_hour_max': 30, 'names': ['小爱']}
    def _spent_today(self): return 0.0
    def _browse_on(self): return False
    def _browse_names(self): return self._known_names(self._names_index())
    def _names_index(self): return {'10009': {'主人'}}
    def _known_names(self, people):
        return [name for person in people for name in [str(person), *self._names_index().get(person, set())]]
    def _addresses_her(self, event): return bool(event.why)
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows.get(here, [])}
    def _llm_allowed(self, kind): return True
    async def _persona_text(self, event): return 'A fictional persona.'
    async def _score(self, event): return self.score
    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answer if isinstance(self.answer, str) else json.dumps(self.answer, ensure_ascii=False)
        return parser(raw)


class WithTheClock(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.mkdtemp(prefix='ams-life-one-sleep-')
        self.addCleanup(shutil.rmtree, self.temp, True)
        self.root = Path(self.temp)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 2, 22).timestamp())
        for target, name, value in ((life, 'STATE_DIR', self.root / 'states'),
                                    (life, 'DATA_DIR', self.root),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json'),
                                    (phone, 'LOOK_PATH', self.root / 'states' / 'look.json'),
                                    (phone, 'STATE_DIR', self.root / 'states'),
                                    (clock_module, 'time', self.clock),
                                    (mixin_attention, 'WAIT_SECONDS', {'group': 0, 'called': 0, 'private': 0})):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = Person()

    async def asyncTearDown(self):
        await life.stop(self.p)

    def now(self):
        return self.clock()

    async def fall_asleep(self, sleepiness, start):
        """She chooses sleep at `start`, as the life loop records it."""
        self.clock.now = start.timestamp()
        self.p.core.last_tick = self.clock()
        self.p.core._life_body_loaded = True
        self.p.core.sleepiness = sleepiness
        value = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 30,
                 'liked_last': '', 'post': '', 'look': '', 'used_wishes': []}
        await life.apply_choice(self.p, value, self.p.core, self.clock(), '')
        return life.read_state()['sleep']


class TheSameSleep(WithTheClock):
    async def test_asleep_at_2300_an_uncalled_group_message_is_not_judged(self):
        await self.fall_asleep(.9, datetime(2026, 11, 2, 22))
        self.clock.now = datetime(2026, 11, 2, 23).timestamp()
        event = Event('group:900001')
        self.assertIsNone(await self.p._decision(event))
        self.assertEqual(self.p.calls, [])

    async def test_awake_at_0200_a_listed_group_is_handled_as_by_day(self):
        self.clock.now = datetime(2026, 11, 2, 2).timestamp()
        self.p.score = 0.9
        self.assertFalse(life.asleep(self.p, self.clock()))
        self.assertEqual(await self.p._decision(Event('group:900001')), 'reply')

    async def test_with_the_loop_on_the_clock_is_not_asked(self):
        await self.fall_asleep(.9, datetime(2026, 11, 2, 14))     # an afternoon nap: 90 minutes
        self.clock.now = datetime(2026, 11, 2, 15, 30).timestamp()   # past its end, the clock still says night
        with patch.object(attention, 'is_night', return_value=True), \
                patch.object(self.p, '_score', AsyncMock(return_value=0.9)):
            self.assertEqual(await self.p._decision(Event('group:900001')), 'reply')


class WeighingACall(unittest.TestCase):
    """The pure rule: one call's weight, its fading, and how much sleepiness it must beat."""

    def test_drowsy_owner_call_does_not_wake_her_but_a_few_do(self):
        now = 10000.0
        self.assertFalse(attention.wake_check([(now, attention.wake_weight(0.0, owner=True))], 0.9, now))
        calls = [(now - 60, 1.0), (now - 30, 1.0), (now, 1.0)]
        self.assertTrue(attention.wake_check(calls, 0.9, now))
        self.assertTrue(attention.wake_check([(now, 1.0)], 0.3, now))

    def test_a_stranger_is_harder_to_wake_than_the_owner(self):
        now = 10000.0
        owner = [(now - 60, attention.wake_weight(0.0, owner=True)),
                 (now - 30, attention.wake_weight(0.0, owner=True)),
                 (now, attention.wake_weight(0.0, owner=True))]
        stranger = [(when, attention.wake_weight(0.0)) for when, _weight in owner]
        self.assertTrue(attention.wake_check(owner, 0.9, now))
        self.assertFalse(attention.wake_check(stranger, 0.9, now))

    def test_a_call_long_ago_fades_and_does_not_add_up(self):
        now = 10000.0
        self.assertTrue(attention.wake_check([(now - 60, 1.0), (now, 1.0)], 0.9, now))
        self.assertFalse(attention.wake_check([(now - 1800, 1.0), (now, 1.0)], 0.9, now))


class WakingUp(WithTheClock):
    async def test_woken_her_mood_the_reason_and_the_reply(self):
        await self.fall_asleep(.3, datetime(2026, 11, 2, 23))
        self.clock.advance(5 * 60)
        self.p.mood_events_enabled = True
        self.p.core.mood_event = Mock()
        with patch.object(self.p.core, '_decay_to_now'), \
                patch.object(attention, 'mood_wait', return_value=0):
            self.assertEqual(await self.p._decision(
                Event('group:900001', why='at', sender='10009')), 'reply')
        self.p.core.mood_event.assert_called_once_with('woken')
        self.assertEqual(life.read_state()['sleep']['end'], int(self.clock()))
        self.assertTrue(await life.tick(self.p, self.clock() + 60))
        self.assertIn('这会儿想：被叫醒了', self.p.calls[0][1])
        self.assertEqual(self.p.core.last_sleep_end, int(self.clock()))

    async def test_calls_slept_through_are_told_once_and_never_in_their_words(self):
        await self.fall_asleep(.9, datetime(2026, 11, 2, 23))
        self.clock.advance(10 * 60)
        self.assertIsNone(await self.p._decision(
            Event('group:900001', why='at', sender='10002', text='小爱 醒醒 老板来了')))
        self.p.familiar['10003'] = 0.8
        self.clock.advance(60)
        self.assertIsNone(await self.p._decision(
            Event('group:900001', why='at', sender='10003', text='小爱 快看看这个')))
        missed = life.read_state()['missed']
        self.assertEqual([row['place'] for row in missed], ['group:900001', 'group:900001'])
        self.assertEqual([row['tier'] for row in missed], ['不认识', '很熟'])
        kept = (self.root / 'states' / 'life.json').read_text('utf-8')
        self.assertNotIn('老板', kept)
        self.assertNotIn('10002', kept)
        self.assertNotIn('10003', kept)
        for _ in range(3):                                        # the owner, three times
            self.clock.advance(60)
            await self.p._decision(Event('group:900001', why='at', sender='10009'))
        self.assertIn('sleep', life.read_state())                 # woken by the owner's call, not yet ticked
        self.assertTrue(await life.tick(self.p, self.clock() + 60))
        prompt = self.p.calls[0][1]
        self.assertIn('你睡着的时候：', prompt)
        self.assertIn('群1 有人叫了你 2 次（一个不认识的，一个很熟的）', prompt)
        self.assertNotIn('900001', prompt)
        self.assertNotIn('老板', prompt)
        self.assertNotIn('missed', life.read_state())


class TheOldClock(WithTheClock):
    """With the life loop off, the night is the clock's, as before (test 8 of the card)."""

    def setUp(self):
        super().setUp()
        self.p = Person(life_on=False)

    async def test_three_calls_within_ten_minutes_wake_her(self):
        with patch.object(attention, 'is_night', return_value=True):
            first = Event('group:900001', why='at')
            self.assertIsNone(await self.p._decision(first))
            self.assertTrue(first.stopped)
            self.clock.advance(60)
            second = Event('group:900001', why='at')
            self.assertIsNone(await self.p._decision(second))
            self.assertTrue(second.stopped)
            self.clock.advance(60)
            self.assertEqual(await self.p._decision(Event('group:900001', why='at')), 'reply')
            self.assertEqual(getattr(self.p, '_woken_at', 0), self.clock())
            # not called at night: never speaks up herself
            self.p.score = 0.9
            self.assertIsNone(await self.p._decision(Event('group:900001')))


class GroupBrowsing(unittest.IsolatedAsyncioTestCase):
    """`_group_action` follows her sleep with the loop on, and the clock with it off (test 9)."""

    class Groups(mixin_group_browse.GroupBrowseMixin):
        def __init__(self, life_on=True):
            self.enabled = True
            self.config = {'life_loop_enabled': life_on}
            self.browse_groups_enabled = True
            self._group_open_state = {'group:900001': {'unread': 8, 'opened': 0, 'first_unread': 0}}
        def _may_speak_in(self, place): return True
        def _attention_cfg(self): return {'night_start': '01:00', 'night_end': '08:25'}
        def _familiarity(self, person): return .7
        def _core(self, event): return SimpleNamespace(v=0)

    def setUp(self):
        self.temp = tempfile.mkdtemp(prefix='ams-life-one-sleep-')
        self.addCleanup(shutil.rmtree, self.temp, True)
        self.root = Path(self.temp)
        (self.root / 'states').mkdir()
        self.now = datetime(2026, 11, 2, 23).timestamp()
        for target, name, value in ((life, 'STATE_DIR', self.root / 'states'),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json')):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)

    def test_sleep_decides_and_not_the_clock(self):
        groups = self.Groups()
        life.save_state({'sleep': {'start': self.now - 600, 'end': self.now + 600}})
        with patch.object(mixin_group_browse.attention, 'is_night', return_value=False):
            self.assertEqual(groups._group_action(self.now)[0], 'none')     # asleep though not night
        life.save_state({})
        with patch.object(mixin_group_browse.attention, 'is_night', return_value=True):
            self.assertEqual(groups._group_action(self.now)[0], 'group')    # awake though night
        life.save_state({'sleep': {'start': self.now - 600, 'end': self.now + 600}})
        off = self.Groups(life_on=False)
        with patch.object(mixin_group_browse.attention, 'is_night', return_value=True):
            self.assertEqual(off._group_action(self.now)[0], 'none')


if __name__ == '__main__':
    unittest.main()
