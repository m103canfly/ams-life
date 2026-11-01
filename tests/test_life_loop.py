# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline choices, sleep accounting and one-shot background entries."""
import asyncio
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

import app
import body
import daily
import discretion
import harness
import her_days
import life_loop as life
import look
import mixin_autonomy
import mixin_browse
import mixin_group_browse
import mixin_llm
import mixin_selfie as phone


class Person(phone.SelfieMixin):
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
        self.answer = {'do': '什么都不干', 'detail': '在家里发呆', 'minutes': 30}
        self._make_photo = AsyncMock(return_value=None)
        self._save_self_model = Mock()
        self._maybe_write_notebook = AsyncMock(return_value=True)

    def _core(self, event=None): return self.core
    def _attention_cfg(self): return {'soft': 8, 'hard': 10}
    def _spent_today(self): return self.spent
    def _browse_on(self): return self.config.get('browse_enabled', False)
    def _browse_names(self): return self._known_names(self._names_index())
    def _names_index(self): return {'10001': {'虚构小甲'}, '10003': {'虚构小乙'}}
    def _known_names(self, people):
        return [name for person in people for name in [str(person), *self._names_index()[person]]]
    def _here(self, event): return event.place if event else ''
    def _addresses_her(self, event): return event.at_me
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows[here]}
    def _llm_allowed(self, kind): return self.allowed
    async def _persona_text(self, event): return 'A fictional persona.'
    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answer if isinstance(self.answer, str) else json.dumps(self.answer, ensure_ascii=False)
        return parser(raw)


class LifeLoopTests(unittest.IsolatedAsyncioTestCase):
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

    def now(self): return datetime.fromtimestamp(self.clock())

    def chosen(self, action='休息', minutes=30, detail='在家里歇着'):
        self.p._set_now('家里', detail, now=self.now(), minutes=minutes, source='her', kind=action)

    def rows(self): return her_days.Store(self.root).recent(20)

    async def tick(self, minutes=0):
        self.clock.advance(minutes * 60)
        return await life.tick(self.p)

    async def test_expiry_calls_once_after_thirty_minutes(self):
        self.chosen()
        for _ in range(29):
            await self.tick(1)
        self.assertEqual(self.p.calls, [])
        self.assertTrue(await self.tick(1))
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)

    async def test_private_quiet_once_and_later_messages_delay_it(self):
        # Only while she is dazing (not busy with a chosen thing) does quiet reach her.
        self.chosen(action='什么都不干', minutes=120)
        start = self.clock()
        self.p.windows['private:10001'] = [{'role': 'assistant', 'ts': start}]
        await self.tick(5)
        self.p.windows['private:10001'].append({'role': 'user', 'ts': self.clock()})
        await self.tick(9)
        self.assertEqual(self.p.calls, [])
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)
        await self.tick(11)
        self.assertEqual(len(self.p.calls), 1)

    async def test_called_group_and_only_that_places_silence(self):
        self.chosen(action='什么都不干', minutes=120)
        self.p.windows['group:900001'] = [{'role': 'user', 'ts': self.clock()}]
        life.note_called(self.p, SimpleNamespace(place='group:900001', at_me=True))
        await self.tick(9)
        self.p.windows['group:900003'] = [{'role': 'user', 'ts': self.clock()}]
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)
        await self.tick(10)
        self.assertEqual(len(self.p.calls), 1)

    async def test_unaddressed_group_never_triggers(self):
        self.chosen(action='什么都不干', minutes=120)
        self.p.windows['group:900001'] = [{'role': 'user', 'ts': self.clock()}]
        life.note_called(self.p, SimpleNamespace(place='group:900001', at_me=False))
        await self.tick(10)
        self.assertEqual(self.p.calls, [])

    async def test_threshold_crossing_not_sustained_high(self):
        self.chosen(minutes=120)
        self.p.core.hunger = .6
        await self.tick()
        self.p.core.hunger = .75
        self.assertTrue(await self.tick())
        self.p.core.hunger = .8
        for _ in range(11):
            await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)

    async def test_cooldown_and_expiry_exception(self):
        await self.tick()
        self.p.core.hunger = .75
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)
        self.assertTrue(life.read_state()['crossed_pending'])
        self.p.answer['minutes'] = 5
        self.chosen(minutes=5)
        await self.tick(5)
        self.assertEqual(len(self.p.calls), 2)
        self.assertFalse(life.read_state().get('crossed_pending'))

    async def test_crossing_during_cooldown_waits_then_thinks_once(self):
        await self.tick()
        self.p.core.hunger = .75
        await self.tick(1)
        self.assertTrue(life.read_state()['crossed_pending'])
        await self.tick(8)
        self.assertEqual(len(self.p.calls), 1)
        self.assertTrue(await self.tick(1))
        self.assertEqual(len(self.p.calls), 2)
        self.assertIn('身体有了新的感觉', self.p.calls[-1][1])
        self.assertFalse(life.read_state().get('crossed_pending'))
        await self.tick(10)
        self.assertEqual(len(self.p.calls), 2)

    async def test_crossing_during_cooldown_survives_restart(self):
        await self.tick()
        self.p.core.hunger = .75
        await self.tick(1)
        self.p = Person()
        await self.tick(9)
        self.assertEqual(len(self.p.calls), 1)
        self.assertIn('身体有了新的感觉', self.p.calls[0][1])
        self.assertFalse(life.read_state().get('crossed_pending'))

    async def test_materials_exclude_identifiers_and_keep_activity_fields(self):
        self.chosen(minutes=120, detail='在家里看树')
        item = life.current()
        item.update(place='group:900001', origin={'people': ['20002']}, id='metadata-only-now')
        phone._write_json(phone.NOW_PATH, item)
        her_days.Store(self.root).add({'id': 'metadata-only-day', 'ts': self.clock() - 1800,
                                      'do': '休息', 'detail': '窗边看树，记下10003', 'minutes': 15,
                                      'feel': '轻松', 'liked': '很喜欢', 'related_users': ['10001'],
                                      'origin': {'people': ['20002'], 'source_ids': ['metadata-only-source']}})
        life.save_state(dict(life.read_state(), crossed_pending=True))
        await self.tick()
        prompt = self.p.calls[0][1]
        for hidden in ('900001', '10001', '10003', '20002', 'place', 'origin', 'related_users',
                       'metadata-only-now', 'metadata-only-day', 'metadata-only-source'):
            self.assertNotIn(hidden, prompt)
        for shown in ('家里', '在家里看树', '10:00', '09:30', '休息', '15', '轻松', '很喜欢'):
            self.assertIn(shown, prompt)

    async def test_fenced_json_numeric_minutes_and_null_text_are_accepted(self):
        self.p.answer = '```json\n' + json.dumps({'do': '休息', 'detail': '在家里坐着',
                                                'minutes': '30', 'liked_last': None,
                                                'post': None, 'look': None}, ensure_ascii=False) + '\n```'
        with self.assertNoLogs('ams-life.life', level='WARNING'):
            self.assertTrue(await self.tick())
        self.assertEqual(len(self.p.calls), 1)
        self.assertEqual(life.current()['minutes'], 30)
        self.assertEqual(self.rows()[0]['do'], '休息')
        self.assertEqual(life.read_state()['today']['count'], 1)

    async def test_menu_disabled_choices_and_invalid_answer_warning(self):
        self.p.answer['do'] = '拍照'
        with self.assertLogs('ams-life.life', level='WARNING') as logs:
            self.assertFalse(await self.tick())
        prompt = self.p.calls[0][1]
        for action in ('拍照', '去测试群看看', '刷手机', '发说说'):
            self.assertNotIn(action, prompt)
        self.assertEqual(self.rows(), [])
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)
        self.assertEqual(len(logs.output), 1)

    async def test_eat_and_like_previous_record(self):
        self.p.core.hunger = .9
        self.p.answer = {'do': '吃饭', 'detail': '在家里，吃一碗面', 'minutes': 30}
        await self.tick()
        self.assertEqual(life.current()['source'], 'her')
        self.assertEqual(life.current()['kind'], '吃饭')
        self.assertEqual(self.p.core.hunger, .1)
        self.assertEqual(len(self.rows()), 1)
        self.p.answer = {'do': '休息', 'detail': '在沙发上坐着', 'liked_last': '很好吃'}
        await self.tick(30)
        self.assertEqual(self.rows()[1]['liked'], '很好吃')

    async def test_sleep_kind_eight_hours_no_interrupt_and_outfit(self):
        # At 22:45, 0.678 is eight hours above the night's 0.15 waking line.
        self.clock.advance(12 * 3600 + 45 * 60)
        self.p.core.last_tick = self.clock()
        self.p.core.sleepiness, self.p.core.physical_fatigue = .678, .9
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 480}
        await self.tick()
        item = life.current()
        self.assertEqual((item['kind'], item['doing'], item['minutes']), ('睡觉', '在床上睡觉', 480))
        start = self.clock()
        self.p.windows['private:10001'] = [{'role': 'assistant', 'ts': start}]
        for _ in range(7):
            self.p.core.hunger = .9
            await self.tick(60)
            self.assertTrue(phone._her_now_valid(item, self.now()))
            self.assertEqual(len(self.p.calls), 1)
        self.p.answer = {'do': '吃饭', 'detail': '在家里吃饭', 'look': '虚构蓝色上衣'}
        with patch.object(body, 'slept', wraps=body.slept) as settled, patch.object(look, 'datetime') as clock:
            clock.now.return_value = self.now() + timedelta(hours=1)
            await self.tick(60)
        self.assertEqual(settled.call_count, 1)
        self.assertEqual(self.p.core.last_sleep_end, start + 480 * 60)
        self.assertEqual(len(self.p.calls), 2)
        self.assertIn('今天还没定打扮', self.p.calls[-1][1])
        self.assertEqual(look.read_look(phone.LOOK_PATH, self.now().date()), '虚构蓝色上衣')

    async def test_sleep_recovery_never_double_counts_and_awake_at_night(self):
        # At 10:00 with 0.9 she naps 90 minutes; the day's 0.45 line is miles away.
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 60}
        self.p.core.sleepiness, self.p.core.physical_fatigue = .9, .8
        await self.tick()
        await self.tick(30)
        self.assertAlmostEqual(self.p.core.sleepiness, .867)
        self.assertAlmostEqual(self.p.core.physical_fatigue, .75)
        self.p.answer = {'do': '休息', 'detail': '在家里坐着', 'minutes': 5}
        await self.tick(30)
        self.assertAlmostEqual(self.p.core.sleepiness, .834)
        self.assertAlmostEqual(self.p.core.physical_fatigue, .7)
        await self.tick(30)
        self.assertAlmostEqual(self.p.core.sleepiness, .801)
        self.assertAlmostEqual(self.p.core.physical_fatigue, .65 - .10 * 5 / 60)
        old_wake = self.p.core.last_sleep_end
        await self.tick(1)
        self.assertEqual(self.p.core.last_sleep_end, old_wake)
        self.clock.advance(13 * 3600)
        self.p.core.last_tick = self.clock()
        self.chosen(action='什么都不干', minutes=120)
        self.p.core.sleepiness = .1
        await self.tick(30)
        self.assertAlmostEqual(self.p.core.sleepiness, .13)

    async def test_fractional_clock_nap_twenty_minutes_marks_integer_wake_once(self):
        self.clock.advance(.456789)
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 480}
        await self.tick()
        sleep = life.read_state()['sleep']
        self.assertIs(type(sleep['start']), int)
        self.assertIs(type(sleep['end']), int)
        self.assertEqual(sleep['start'], int(self.clock()))
        self.assertEqual(sleep['end'], sleep['start'] + 20 * 60)
        self.assertEqual(datetime.fromisoformat(life.current()['start']).timestamp(), sleep['start'])
        self.clock.advance(sleep['end'] - self.clock() - 1)
        await self.tick()
        self.assertEqual(len(self.p.calls), 1)
        self.p.answer = {'do': '吃饭', 'detail': '在家里吃饭'}
        with patch.object(body, 'slept', wraps=body.slept) as settled:
            await self.tick(1 / 60)
            self.assertEqual(self.p.core.last_sleep_end, sleep['end'])
            settled.assert_called_once_with(self.p.core, sleep['end'], sleep['end'])
            await self.tick(1)
            self.assertEqual(settled.call_count, 1)
        self.assertEqual(len(self.p.calls), 2)

    async def test_legacy_fractional_sleep_deadline_marks_wake(self):
        self.clock.advance(.456789)
        self.p.core.last_tick = self.clock()
        self.chosen(action='睡觉', minutes=480, detail='在床上睡觉')
        start = self.clock()
        end = start + 480 * 60
        life.save_state(dict(life.read_state(), sleep={'start': start, 'end': end}))
        self.clock.advance(480 * 60 + 1)
        with patch.object(body, 'slept', wraps=body.slept) as settled:
            self.p.core._decay_to_now()
        self.assertEqual(self.p.core.last_sleep_end, int(end))
        settled.assert_called_once_with(self.p.core, int(end), int(end))

    async def test_sleep_restart_restores_checkpoint_and_recovers_offline_once(self):
        # At 10:00 with 0.9 she naps 90 minutes, so the restart is still within the sleep.
        self.p.core.sleepiness, self.p.core.physical_fatigue = .9, .8
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 120}
        await self.tick()
        await self.tick(30)
        self.clock.advance(30 * 60)
        self.p = Person()
        await self.tick()
        self.assertAlmostEqual(self.p.core.sleepiness, .834)
        self.assertAlmostEqual(self.p.core.physical_fatigue, .7)
        await self.tick(20)
        self.assertAlmostEqual(self.p.core.sleepiness, .812)
        self.assertAlmostEqual(self.p.core.physical_fatigue, .7 - .10 * 20 / 60)
        self.assertEqual(self.p.calls, [])

    async def test_expired_sleep_still_settles_after_now_line_fallback(self):
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 60}
        await self.tick()
        start = self.clock()
        self.clock.advance(60 * 60)
        self.p._now_line(None)
        self.assertEqual(life.current()['source'], 'schedule')
        self.p.answer = {'do': '吃饭'}
        await self.tick()
        self.assertEqual(self.p.core.last_sleep_end, start + 20 * 60)
        self.assertEqual(len(self.p.calls), 2)

    async def test_wake_settles_even_after_a_recent_chat_decay(self):
        # At 10:00 with 0.9 she naps 90 minutes; the chat decays her 15 seconds before waking.
        self.p.core.sleepiness = .9
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 60}
        await self.tick()
        start = self.clock()
        self.clock.advance(90 * 60 - 15)
        self.p.core._decay_to_now()
        self.clock.advance(15)
        self.p.answer = {'do': '什么都不干'}
        await self.tick()
        self.assertEqual(self.p.core.last_sleep_end, start + 90 * 60)
        self.assertAlmostEqual(self.p.core.sleepiness, .801)

    async def test_chosen_awake_skips_scheduled_meal(self):
        self.clock.advance(2 * 3600)
        self.p.core.last_tick = self.clock()
        self.chosen(action='什么都不干', minutes=120)
        self.p.core.hunger = .5
        self.p.core.last_meal = self.clock()
        await self.tick(60)
        self.assertAlmostEqual(self.p.core.hunger, .58)

    async def test_browse_choices_set_flags_and_menu_only_when_available(self):
        self.p.browse_groups_enabled = self.p.browse_trips_enabled = True
        self.p.config['browse_enabled'] = True
        self.p.answer = {'do': '去测试群看看', 'minutes': 5}
        await self.tick()
        self.assertTrue(life.read_state()['pending']['group_browse'])
        self.assertIn('刷手机', self.p.calls[0][1])
        self.p.answer = {'do': '刷手机', 'minutes': 5}
        await self.tick(5)
        self.assertTrue(life.read_state()['pending']['go_browse'])

    async def test_function_switch_blocks_model_and_invalid_expiry_is_not_retried(self):
        self.chosen(minutes=5)
        self.p.allowed = False
        await self.tick(5)
        self.assertEqual(self.p.calls, [])
        self.p.allowed = True
        self.p.answer = {'do': 'not on menu'}
        with self.assertLogs('ams-life.life', level='WARNING'):
            await self.tick()
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)

    async def test_reply_tool_keeps_twelve_characters_and_no_kind(self):
        event = SimpleNamespace(place='private:10001')
        self.assertEqual(await self.p._tool_set_now(event, '家里', '字' * 13), '不能这样写')
        self.assertEqual(life.current(), {})
        await self.p._tool_set_now(event, '家里', '睡觉', minutes=1000)
        self.assertNotIn('kind', life.current())

    async def test_detail_forty_characters_cleaning_and_now_line(self):
        self.p.answer['detail'] = '看' * 45
        await self.tick()
        self.assertEqual(life.current()['doing'], '看' * 40)
        self.assertIn('看' * 40, self.p._now_line(None))
        self.assertEqual(self.rows()[0]['detail'], '看' * 40)

    async def test_soft_budget_falls_back_hard_budget_no_side_effects(self):
        self.chosen()
        self.p.spent = 8.01
        await self.tick()
        self.assertEqual(self.p.calls, [])
        self.assertEqual(life.current()['source'], 'schedule')
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.p.spent = 10.01
        await self.tick(30)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    async def test_forty_ninth_call_is_blocked_and_daily_reset(self):
        life.save_state({'today': {'date': self.now().date().isoformat(), 'count': 48}})
        await self.tick()
        self.assertEqual(self.p.calls, [])
        self.clock.advance(86400)
        self.p._life_start_checked = False
        await self.tick()
        self.assertEqual(len(self.p.calls), 1)

    async def test_anonymization_and_forget(self):
        self.p.answer.update(detail='和虚构小甲在公园看树', post='虚构小乙也喜欢这里')
        await self.tick()
        row = self.rows()[0]
        self.assertNotIn('虚构小甲', row['detail'])
        # The card writes the public line in its own call, only for 发说说.
        self.assertEqual(row['related_users'], ['10001'])
        self.assertEqual(row['origin']['where'], 'self')
        self.assertEqual(her_days.Store(self.root).forget('10001'), 1)
        self.assertEqual(self.rows(), [])

    async def test_owner_name_is_kept_and_other_names_are_anonymized(self):
        self.p.config.update(owner_qq='10001', qzone_enabled=True)
        self.p.answer = {'do': '发说说', 'detail': '陪虚构小甲和虚构小乙看树',
                         'post': '虚构小甲说虚构小乙喜欢树', 'minutes': 5}
        with patch('qzone.post', new_callable=AsyncMock) as post:
            await self.tick()
        row = self.rows()[0]
        self.assertIn('虚构小甲', row['detail'])
        self.assertNotIn('虚构小乙', row['detail'])
        self.assertEqual(row['related_users'], ['10001', '10003'])
        self.assertIn('虚构小甲', post.await_args.args[1])
        self.assertNotIn('虚构小乙', post.await_args.args[1])
        self.p.answer = {'do': '休息', 'liked_last': '虚构小甲喜欢虚构小乙选的树'}
        await self.tick(5)
        liked = self.rows()[1]['liked']
        self.assertIn('虚构小甲', liked)
        self.assertNotIn('虚构小乙', liked)

    async def test_due_table_once(self):
        self.chosen(minutes=120)
        life.save_state(dict(life.read_state(), due=[{'id': 'alarm1', 'ts': self.clock() + 600}]))
        await self.tick(9)
        self.assertEqual(self.p.calls, [])
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)
        self.assertEqual(life.read_state()['due'], [])

    async def test_late_model_and_switch_are_checked_at_tick(self):
        self.p._neutral_model = None
        life.start(self.p)
        await asyncio.sleep(0)
        self.assertIsNotNone(self.p._life_task)
        self.assertEqual(self.p.calls, [])
        self.p._neutral_model = object()
        await self.tick()
        self.assertEqual(len(self.p.calls), 1)
        self.p.config['life_loop_enabled'] = False
        await self.tick(30)
        self.assertEqual(len(self.p.calls), 1)

    async def test_disabled_does_not_write_state(self):
        self.p.config['life_loop_enabled'] = False
        await self.tick()
        self.assertEqual(self.p.calls, [])
        self.assertFalse((life.STATE_DIR / 'life.json').exists())

    async def test_notebook_sleep_evening_once_and_three_am_fallback(self):
        self.clock.advance(11 * 3600)
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 480}
        await self.tick()
        self.p._maybe_write_notebook.assert_awaited_once()
        at_2330 = self.clock() + 150 * 60
        self.assertFalse(life.notebook_due(self.p, at_2330))
        self.assertFalse(life.notebook_due(self.p, self.clock() + 6 * 3600))
        # A separate evening with no chosen sleep falls back after 03:00.
        self.assertTrue(life.notebook_due(self.p, self.clock() + 30 * 3600))

    async def test_notebook_gate_keeps_old_time_when_disabled(self):
        self.p._notebook_time_reached = mixin_llm.LLMMixin._notebook_time_reached.__get__(self.p)
        self.p.notebook_time = '23:30'
        self.p.config['life_loop_enabled'] = False
        evening = self.now().replace(hour=23, minute=30).timestamp()
        self.assertTrue(self.p._notebook_time_reached(evening))
        self.assertFalse(self.p._notebook_time_reached(evening - 60))
        self.p.config['life_loop_enabled'] = True
        self.assertFalse(self.p._notebook_time_reached(evening))

    async def test_notebook_sleep_before_three_am_writes_previous_evening_once(self):
        self.clock.advance(15 * 3600)
        evening = (self.now() - timedelta(days=1)).date().isoformat()
        self.p.answer = {'do': '睡觉', 'detail': '在床上睡觉', 'minutes': 480}
        await self.tick()
        self.p._maybe_write_notebook.assert_awaited_once()
        state = life.read_state()
        self.assertEqual(state['notebook_sleep'], evening)
        self.assertEqual(state['notebook_done'], evening)
        self.assertFalse(life.notebook_due(self.p, self.now().replace(hour=3).timestamp()))

    async def test_photo_background_and_post_uses_own_photo_today(self):
        self.p.config.update(photo_enabled=True, qzone_enabled=True)
        path = self.root / 'fake-photo.png'
        path.write_bytes(b'fake')
        self.p._make_photo.return_value = path
        self.p.answer = {'do': '拍照', 'detail': '窗边的花', 'minutes': 5}
        await self.tick()
        await asyncio.sleep(0)
        self.p._make_photo.assert_awaited_once_with('photo', '窗边的花')
        self.p.answer = {'do': '发说说', 'post': '虚构小甲说花开了', 'minutes': 5}
        with patch('qzone.post', new_callable=AsyncMock) as post:
            await self.tick(5)
        self.assertEqual(post.await_args.kwargs['photo'], str(path))
        self.assertNotIn('虚构小甲', post.await_args.args[1])

    async def test_group_entry_consumes_once_and_bypasses_score(self):
        groups = {'group:900001': {'unread': 1}}
        p = SimpleNamespace(config={'life_loop_enabled': True}, enabled=True,
                            browse_groups_enabled=True, _neutral_model=object(),
                            _attention_cfg=self.p._attention_cfg, _spent_today=self.p._spent_today,
                            _group_prune=Mock(), _group_state=lambda: groups, _may_speak_in=lambda here: True,
                            _group_action=Mock(), _group_open=Mock(return_value=([object()], (0, 0))),
                            _group_look=AsyncMock())
        with patch.object(p, '_group_action', side_effect=AssertionError('score must not run')):
            await mixin_group_browse.GroupBrowseMixin._group_browse_tick(p)
            p._group_look.assert_not_awaited()
            state = life.read_state()
            state.setdefault('pending', {})['group_browse'] = True
            life.save_state(state)
            await mixin_group_browse.GroupBrowseMixin._group_browse_tick(p)
            await asyncio.sleep(0)
            await mixin_group_browse.GroupBrowseMixin._group_browse_tick(p)
        p._group_look.assert_awaited_once()
        self.assertFalse(life.read_state()['pending'].get('group_browse'))

    async def test_message_observer_uses_at_flag_without_text_keywords(self):
        self.p._window_add_message = Mock(return_value='stored')
        original = self.p._window_add_message
        life.observe_messages(self.p)
        ev = SimpleNamespace(place='group:900001', at_me=True, text='plain fictional words')
        self.assertEqual(self.p._window_add_message(ev), 'stored')
        original.assert_called_once_with(ev)
        self.assertEqual(life.read_state()['called'], {'group:900001': self.clock()})

    async def test_browse_entry_consumes_once_without_should_go(self):
        p = SimpleNamespace(config={'life_loop_enabled': True}, enabled=True,
                            browse_trips_enabled=True, _neutral_model=object(),
                            _attention_cfg=self.p._attention_cfg, _spent_today=self.p._spent_today,
                            _browse_on=lambda: True, _core=lambda ev: self.p.core,
                            _browse_state=lambda: {}, _browse_save_state=Mock(), _browse_trip=AsyncMock())
        state = life.read_state()
        state.setdefault('pending', {})['go_browse'] = True
        life.save_state(state)
        with patch.object(mixin_browse, '_trip_budget_left', return_value=True), \
                patch.object(mixin_browse.browse, 'should_go', side_effect=AssertionError('old gate')):
            self.assertTrue(await mixin_browse.BrowseMixin._maybe_go_browse(p))
            self.assertFalse(await mixin_browse.BrowseMixin._maybe_go_browse(p))
        p._browse_trip.assert_awaited_once()

    async def test_stop_cancels_life_and_all_leaked_background_tasks(self):
        life.start(self.p)
        self.p._autonomy_task = asyncio.create_task(asyncio.sleep(3600))
        self.p._sticker_vector_task = asyncio.create_task(asyncio.sleep(3600))
        self.p._sticker_relook_task = asyncio.create_task(asyncio.sleep(3600))
        self.p._image_idle_task = asyncio.create_task(asyncio.sleep(3600))
        instance = app.App(SimpleNamespace())
        instance.her = self.p
        await instance.stop()
        for name in ('_life_task', '_autonomy_task', '_sticker_vector_task', '_sticker_relook_task', '_image_idle_task'):
            self.assertTrue(getattr(self.p, name).done(), name)


class ParserTests(unittest.TestCase):
    def test_null_text_fields_are_empty(self):
        value = life.parse(json.dumps({'do': '休息', 'detail': None, 'liked_last': None,
                                       'post': None, 'look': None}), life.BASE_MENU)
        self.assertEqual([value[key] for key in ('detail', 'liked_last', 'post', 'look')], [''] * 4)

    def test_minutes_bounds_and_bad_json(self):
        for action, value, expected in (('睡觉', 10, 60), ('睡觉', 999, 720),
                                        ('休息', 1, 5), ('休息', 999, 120)):
            self.assertEqual(life.parse(json.dumps({'do': action, 'minutes': value}), life.BASE_MENU)['minutes'], expected)
        for text, expected in ((' 30 ', 30), ('999', 120), ('1', 5)):
            self.assertEqual(life.parse(json.dumps({'do': '休息', 'minutes': text}), life.BASE_MENU)['minutes'], expected)
        for raw in ('no json', '[]', '{"do":"休息","minutes":true}', '{"do":"休息","detail":{}}',
                    '{"do":"休息","minutes":"soon"}'):
            self.assertIsNone(life.parse(raw, life.BASE_MENU))
