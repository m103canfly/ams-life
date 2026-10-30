"""Offline checks for bounded mood events; all examples are invented."""
import sys
import re
from contextlib import ExitStack
from unittest import mock
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_body_heart import CLOCK, body, interpretation  # noqa: E402
import attention  # noqa: E402
import mixin_phone  # noqa: E402
import mixin_attention  # noqa: E402
import mixin_selfie  # noqa: E402
import harness  # noqa: E402
import main  # noqa: E402


class MoodPhone(mixin_phone.PhoneMixin):
    mood_events_enabled = True

    def __init__(self):
        self.core = body.BioCore()
        self.origin = {'where': 'private:10005', 'people': ['10005'],
                       'source_ids': ['made-up-message'], 'visibility': 'private'}
        self.win = {'recent': []}

    def _here(self, event): return 'private:10005'
    def _speaker(self, event): return ('10005', '测试者')
    def _job_stale(self): return False
    def _read_window(self, place): return self.win
    def _write_window(self, place, win): self.win = win
    def _event_origin(self, event): return dict(self.origin)
    def _without_gone(self, text, event): return text
    def _addresses_her(self, event): return True
    def _window_places(self): return ['private:10005']
    def _familiarity(self, person): return 1.0
    def _core(self, event): return self.core


class MoodEvents(unittest.TestCase):
    def _check_answer_once(self, phone):
        event = object()
        phone._window_add_reply(event, '一句话')
        for _ in range(20):
            if phone._mood_note_answer(event, 'private'):
                phone.core.mood_event('answered')
        self.assertEqual(sum(x['kind'] == 'answered' for x in phone.core.mood_events), 1)
        phone._window_add_reply(event, '另一句话')
        if phone._mood_note_answer(event, 'private'):
            phone.core.mood_event('answered')
        self.assertEqual(sum(x['kind'] == 'answered' for x in phone.core.mood_events), 2)

    def test_each_reply_is_answered_once(self):
        self._check_answer_once(MoodPhone())

    def test_answer_dedup_mutation_is_detected(self):
        class NoDedup(MoodPhone):
            def _mood_note_answer(self, event, why):
                for line in self.win['recent']:
                    line.pop('mood_answered', None)
                return super()._mood_note_answer(event, why)
        with self.assertRaises(AssertionError):
            self._check_answer_once(NoDedup())

    def test_origin_reconstruction_preserves_ignore_tracking(self):
        phone = MoodPhone()
        event = type('Event', (), {'_mood_direct': True})()
        phone._window_add_reply(event, '一句话')
        line = phone.win['recent'][0]
        self.assertNotIn('mood_direct', line['origin'])
        line['origin'] = mixin_phone.discretion.origin_of(line)
        CLOCK.advance(600)
        phone._sweep_windows()
        self.assertEqual(phone.core.mood_events[-1]['kind'], 'ignored')

    def test_media_note_rejects_unknown_kind_and_off_switch(self):
        phone = MoodPhone()
        event = type('Event', (), {'_mood_direct': True})()
        phone._window_add_reply(event, '一句话')
        phone._note_she_sent(event, 'raw text')
        phone.mood_events_enabled = False
        phone._note_she_sent(event, 'selfie')
        self.assertEqual(len(phone.win['recent']), 1)
        self.assertNotIn('mood_share', phone.win['recent'][0])

    def test_media_note_uses_phone_kinds_only(self):
        event = type('Event', (), {'_mood_direct': True})()
        for kind, label in [('selfie', '[自拍]'), ('snap', '[随手拍]'),
                            ('screenshot', '[分享网页]'), ('voice', '[语音]')]:
            phone = MoodPhone()
            phone._window_add_reply(event, '一句话')
            phone._note_she_sent(event, kind)
            self.assertEqual(phone.win['recent'][-1]['text'], label)
            self.assertTrue(phone.win['recent'][0]['mood_share'])
        for kind in ('photo', 'web'):
            phone = MoodPhone()
            phone._window_add_reply(event, '一句话')
            phone._note_she_sent(event, kind)
            self.assertEqual(len(phone.win['recent']), 1)

    def test_brief_keeps_event_and_body_details(self):
        core = body.BioCore()
        core.mood_event('criticism')
        core.talked = .9
        core.ambient = .8
        brief = interpretation.body_brief(core)
        self.assertIn('刚才被说得有点不高兴', brief)
        self.assertIn('今天说得太多了', brief)
        self.assertIn('各处这会儿挺热闹', brief)

    def test_brief_replaces_only_mood_and_energy_phrases(self):
        core = body.BioCore()
        core.mood_event('praise')
        core.v, core.energy, core.talked = .5, .2, .9
        brief = interpretation.body_brief(core)
        self.assertIn('心情很好，话也多了起来', brief)
        self.assertIn('有点困了', brief)
        self.assertIn('今天说得太多了', brief)
        self.assertNotIn('心情不错', brief)
        self.assertNotIn('不太起劲', brief)
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
                                        'mood_direct': direct, 'origin': {'people': ['10005']}}]}

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
                                        'mood_direct': True, 'origin': {'people': ['10005']}}]}
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
    async def test_sent_selfie_counts_once_and_answer_prevents_loss(self):
        class MediaPhone(mixin_selfie.SelfieMixin, MoodPhone):
            async def _phone_clear(self, event, text): return True
            async def _make_photo(self, kind, what): return Path('selfie.png')
            def _phone_account(self, kind, sent=False): pass
            def _phone_prune(self, kind): pass

        class Event:
            _mood_direct = True
            def __init__(self): self.sent = []
            async def send(self, chain): self.sent.append(chain)
            def is_stopped(self): return False

        async def no_wait(_): pass
        silent, answered = MediaPhone(), MediaPhone()
        with mock.patch.object(mixin_selfie.asyncio, 'sleep', no_wait):
            for phone in (silent, answered):
                event = Event()
                phone._window_add_reply(event, '一句话')
                await phone._media_after_reply(event, {'photo': ('selfie', '在家')})
                self.assertEqual(len(event.sent), 1)
                self.assertEqual(phone.win['recent'][-1]['text'], '[自拍]')
                self.assertTrue(phone.win['recent'][-1]['mood_checked'])
                self.assertTrue(phone.win['recent'][0]['mood_share'])
        answered.win['recent'].append({'role': 'user', 'sender_id': '10005', 'ts': CLOCK() + 10})
        CLOCK.advance(600)
        silent._sweep_windows()
        answered._sweep_windows()
        self.assertEqual([x['kind'] for x in silent.core.mood_events], ['unanswered_share'])
        self.assertFalse(getattr(answered.core, 'mood_events', []))

    async def test_media_send_success_and_failure_control_mood_note(self):
        class Sender(mixin_selfie.SelfieMixin):
            def __init__(self):
                self.notes = []
            async def _phone_clear(self, event, text): return True
            def _phone_account(self, kind, sent=False): pass
            def _phone_prune(self, kind): pass
            def _note_she_sent(self, event, kind): self.notes.append((event, kind))
            async def _make_voice(self, text): return Path('voice.wav')
            async def _make_photo(self, kind, what): return Path('photo.png')

        class Event:
            def __init__(self, fails): self.fails = fails
            async def send(self, chain):
                if self.fails:
                    raise RuntimeError('simulated send failure')

        async def no_wait(_): pass
        with mock.patch.object(mixin_selfie.asyncio, 'sleep', no_wait):
            queues = {'selfie': {'photo': ('selfie', '在家')},
                      'snap': {'photo': ('snap', '天空')},
                      'screenshot': {'screenshot': ('https://example.invalid/', '网页', '分享')},
                      'voice': {'voice': '一段话'}}
            for kind, queue in queues.items():
                for fails in (False, True):
                    with self.subTest(kind=kind, fails=fails):
                        sender, event = Sender(), Event(fails)
                        await sender._media_after_reply(event, queue)
                        self.assertEqual(sender.notes, [] if fails else [(event, kind)])

    async def test_on_message_counts_first_answer_per_reply(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'mood_events_enabled': True})
        phone = MoodPhone()
        event = harness.FakeEvent('继续', sender='10005', name='测试者')
        event._mood_direct = True
        methods = {'_here': phone._here, '_speaker': phone._speaker, '_job_stale': phone._job_stale,
                   '_read_window': phone._read_window, '_write_window': phone._write_window,
                   '_event_origin': phone._event_origin, '_without_gone': phone._without_gone,
                   '_addresses_her': phone._addresses_her, '_core': phone._core,
                   '_why_called': lambda e: 'private'}
        with ExitStack() as stack:
            for name, implementation in methods.items():
                stack.enter_context(mock.patch.object(plugin, name, side_effect=implementation))
            for name in ('_begin_job', '_check_registry', '_window_add_message', '_listen_body',
                         '_mood_clock', '_ensure_autonomy_task', '_sticker_in_passing'):
                stack.enter_context(mock.patch.object(plugin, name))
            plugin._window_add_reply(event, '一句话')
            for _ in range(20):
                await plugin.on_message(event)
            self.assertEqual(sum(x['kind'] == 'answered' for x in phone.core.mood_events), 1)
            plugin._window_add_reply(event, '另一句话')
            await plugin.on_message(event)
            self.assertEqual(sum(x['kind'] == 'answered' for x in phone.core.mood_events), 2)

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

if __name__ == '__main__':
    unittest.main()
