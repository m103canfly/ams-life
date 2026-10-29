"""Offline checks for bounded mood events; all examples are invented."""
import sys
import re
from unittest import mock
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_body_heart import CLOCK, body, interpretation  # noqa: E402
import attention  # noqa: E402
import mixin_phone  # noqa: E402
import mixin_attention  # noqa: E402
import harness  # noqa: E402
import main  # noqa: E402


class MoodEvents(unittest.TestCase):
    def test_every_event_changes_its_stated_fields(self):
        for kind, changes in body.MOOD_EVENT_CHANGES.items():
            if kind == 'sleep':
                continue
            core = body.BioCore()
            before = {name: getattr(core, name) for name in changes}
            core.mood_event(kind)
            for name, delta in changes.items():
                self.assertGreater((getattr(core, name) - before[name]) * delta, 0, (kind, name))

    def test_event_limit_and_repeat_discount(self):
        core = body.BioCore()
        v = core.v
        core.mood_event('criticism')
        first = v - core.v
        core.mood_event('criticism')
        second = v - core.v - first
        self.assertLessEqual(first, body.MOOD_EVENT_LIMIT)
        self.assertAlmostEqual(second, first * body.MOOD_REPEAT_FACTOR)

    def test_event_effects_fade(self):
        core = body.BioCore()
        core.mood_event('woken')
        stress = core._mood_stress
        energy = core._mood_energy
        CLOCK.advance(body.MOOD_EVENT_HALF_LIFE_MINUTES * 60)
        core._decay_to_now()
        self.assertAlmostEqual(core._mood_stress, stress / 2)
        self.assertAlmostEqual(core._mood_energy, energy / 2)

    def test_fun_page_curiosity_need_recovers(self):
        core = body.BioCore()
        initial = core.novelty_need
        core.mood_event('fun_page')
        self.assertLess(core.novelty_need, initial)
        CLOCK.advance(body.MOOD_EVENT_HALF_LIFE_MINUTES * 60)
        core._decay_to_now()
        self.assertAlmostEqual(initial - core.novelty_need, .025)

    def test_sleep_reduces_distress(self):
        core = body.BioCore()
        core.mood_event('woken')
        core.mood_event('ignored')
        stress, v = core._mood_stress, core.v
        core.mood_event('sleep')
        self.assertLess(core._mood_stress, stress / 2)
        self.assertGreater(core.v, v)

    def test_night_transition_recovers_once_after_restart(self):
        class ClockOwner(mixin_attention.AttentionMixin):
            mood_events_enabled = True
            def __init__(self, core): self.core = core
            def _core(self, event): return self.core
            def _attention_cfg(self): return {'night_start': '01:00', 'night_end': '08:25'}

        core = body.BioCore()
        core.mood_event('woken')
        saved = {}
        def read(path, default): return dict(saved)
        def write(path, state):
            saved.clear()
            saved.update(state)
        with mock.patch.object(mixin_attention, '_read_json', read), \
             mock.patch.object(mixin_attention, '_write_json', write), \
             mock.patch.object(attention, 'is_night', side_effect=[True, False, False]):
            ClockOwner(core)._mood_clock(100)
            ClockOwner(core)._mood_clock(200)
            ClockOwner(core)._mood_clock(300)
        self.assertEqual([x['kind'] for x in core.mood_events].count('sleep'), 1)
        self.assertFalse(saved)

    def test_classification_requires_address_for_interpersonal_events(self):
        self.assertIn('praise', body.mood_kinds('谢谢你', True))
        self.assertNotIn('praise', body.mood_kinds('谢谢你', False))
        self.assertIn('quarrel', body.mood_kinds('他们吵架了', False))
        for text, kind in [('你是机器人', 'robot'), ('叫错名字了', 'wrong_name'),
                           ('你真棒', 'praise'), ('你闭嘴', 'criticism'),
                           ('聊聊你喜欢的', 'liked_topic')]:
            self.assertIn(kind, body.mood_kinds(text, True))
            self.assertNotIn(kind, body.mood_kinds(text, False))

    def test_brief_describes_without_directing(self):
        core = body.BioCore()
        for kind, word in [('woken', '吵醒'), ('ignored', '失落'), ('criticism', '不高兴'),
                           ('quarrel', '气氛有点紧')]:
            core.mood_event(kind)
            brief = interpretation.body_brief(core)
            self.assertIn(word, brief)
            self.assertNotIn('请', brief)

    def test_owner_is_always_closest(self):
        self.assertEqual(attention.familiarity({}, owner=True), 1.0)

    def test_heard_bystander_is_one_third_of_familiar(self):
        familiar, stranger = body.BioCore(), body.BioCore()
        initial = familiar.v
        familiar.mood_hear('今天真开心', familiar=True)
        stranger.mood_hear('今天真开心', familiar=False)
        self.assertGreater(abs(familiar.v - initial), 0)
        self.assertAlmostEqual(stranger.v - initial, (familiar.v - initial) / 3)

    def test_weight_mutation_would_be_detected(self):
        with mock.patch.object(body, 'MOOD_BYSTANDER_WEIGHT', 1.0):
            with self.assertRaises(AssertionError):
                self.test_heard_bystander_is_one_third_of_familiar()

    def test_panel_labels_contain_no_message_or_number(self):
        core = body.BioCore()
        core.mood_event('praise')
        rows = [{'kind': body.MOOD_EVENT_LABELS[x['kind']], 'ts': x['ts']}
                for x in core.mood_events]
        self.assertEqual(set(rows[0]), {'kind', 'ts'})
        self.assertNotRegex(rows[0]['kind'], re.compile(r'\d'))
        self.assertNotIn('谢谢你', rows[0]['kind'])

    def test_ignored_by_familiarity_and_broadcast(self):
        class Phone(mixin_phone.PhoneMixin):
            mood_events_enabled = True

            def __init__(self, familiarity, direct=True):
                self.core = body.BioCore()
                self.familiarity = familiarity
                self.win = {'recent': [{'role': 'assistant', 'ts': CLOCK(),
                                        'origin': {'people': ['10005'], 'mood_direct': direct}}]}

            def _window_places(self):
                return ['group:900001']

            def _read_window(self, place):
                return self.win

            def _write_window(self, place, win):
                self.win = win

            def _familiarity(self, person):
                return self.familiarity

            def _core(self, event):
                return self.core

        close, familiar, stranger, broadcast = Phone(1), Phone(.5), Phone(.1), Phone(1, False)
        CLOCK.advance(600)
        for phone in (close, familiar, stranger, broadcast):
            phone._sweep_windows()
        self.assertEqual(close.core.mood_events[-1]['kind'], 'ignored')
        for phone in (familiar, stranger, broadcast):
            self.assertFalse(getattr(phone.core, 'mood_events', []))
        CLOCK.advance(1200)
        familiar._sweep_windows()
        self.assertEqual(familiar.core.mood_events[-1]['kind'], 'ignored')
        self.assertLess(abs(familiar.core.v - .05), abs(close.core.v - .05))

    def test_answered_share_is_not_ignored_and_unanswered_share_is(self):
        class Phone(mixin_phone.PhoneMixin):
            mood_events_enabled = True
            def __init__(self, answered):
                self.core = body.BioCore()
                self.win = {'recent': [{'role': 'assistant', 'ts': CLOCK(), 'mood_share': True,
                                        'origin': {'people': ['10005'], 'mood_direct': True}}]}
                if answered:
                    self.win['recent'].append({'role': 'user', 'sender_id': '10005', 'ts': CLOCK() + 30})
            def _window_places(self): return ['private:10005']
            def _read_window(self, place): return self.win
            def _write_window(self, place, win): self.win = win
            def _familiarity(self, person): return 1
            def _core(self, event): return self.core

        answered, silent = Phone(True), Phone(False)
        CLOCK.advance(600)
        answered._sweep_windows()
        silent._sweep_windows()
        self.assertFalse(getattr(answered.core, 'mood_events', []))
        self.assertEqual(silent.core.mood_events[-1]['kind'], 'unanswered_share')


class DecisionHearing(unittest.IsolatedAsyncioTestCase):
    async def test_message_through_decision_and_panel(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={
            'mood_events_enabled': True, 'self_decide': True, 'owner_qq': '10005'})
        event = harness.FakeEvent('今天真开心', sender='10005', name='测试者', group='900001')
        event.is_at_or_wake_command = False
        event.stop_event = lambda: None
        async def no_wait(_): pass
        with mock.patch.object(mixin_attention.attention, 'is_night', return_value=False), \
             mock.patch.object(mixin_attention.asyncio, 'sleep', no_wait), \
             mock.patch.object(plugin, '_score', new=mock.AsyncMock(return_value=0)), \
             mock.patch.object(plugin, '_ensure_autonomy_task'), \
             mock.patch.object(plugin, '_sticker_in_passing'):
            await plugin.on_message(event)
            core = plugin._core(None)
            before = core.v
            self.assertEqual([x async for x in plugin.on_message_decide(event)], [])
            self.assertNotEqual(core.v, before)
            core.mood_event('praise')
            rows = (await plugin.page_status())['data']['mood_events']
            self.assertEqual(set(rows[-1]), {'kind', 'ts'})
            self.assertNotIn('10005', str(rows))
            self.assertNotIn('今天真开心', str(rows))

    async def test_only_unanswered_message_is_observed(self):
        class Decision(mixin_attention.AttentionMixin):
            mood_events_enabled = True

            def __init__(self, score, called=False):
                self.core = body.BioCore()
                self.state = {}
                self.score = score
                self.called = called

            def _attention_cfg(self):
                return {'night_start': '01:00', 'night_end': '08:25', 'level': 'normal',
                        'soft': 8, 'hard': 10, 'owner': '', 'group_hour_max': 30}

            def _here(self, event): return 'group:900001'
            def _speaker(self, event): return ('10005', '')
            def _why_called(self, event): return 'at' if self.called else ''
            def _note_tie(self, *args, **kwargs): pass
            def _window_state(self, here): return self.state
            def _core(self, event): return self.core
            def _familiarity(self, person): return .5
            def _spent_today(self): return 0
            async def _score(self, event): return self.score
            async def _ask_for_reply(self, event): return 'request'

        class Event:
            message_str = '今天真开心'
            is_at_or_wake_command = False
            message_obj = None
            def stop_event(self): pass

        async def no_wait(_): pass
        with mock.patch.object(mixin_attention.attention, 'is_night', return_value=False), \
             mock.patch.object(mixin_attention.asyncio, 'sleep', no_wait):
            quiet, selected, called = Decision(0), Decision(1), Decision(0, True)
            initial = quiet.core.v
            self.assertIsNone(await quiet._decide(Event()))
            self.assertGreater(quiet.core.v, initial)
            self.assertEqual(await selected._decide(Event()), 'request')
            self.assertEqual(await called._decide(Event()), 'request')
            self.assertEqual(selected.core.v, initial)
            self.assertEqual(called.core.v, initial)

    async def test_media_only_share_is_recorded_after_successful_send(self):
        class MediaBase:
            async def _media_after_reply(self, event, reply):
                await event.send('image')
        class Owner(mixin_attention.AttentionMixin, MediaBase):
            mood_events_enabled = True
            def __init__(self): self.lines = []
            def _window_add_reply(self, event, text): self.lines.append(text)
        class Event:
            async def send(self, chain): return None

        owner, event = Owner(), Event()
        await owner._media_after_reply(event, '')
        self.assertEqual(owner.lines, ['[分享]'])
        self.assertNotIn('send', event.__dict__)


if __name__ == '__main__':
    unittest.main()
