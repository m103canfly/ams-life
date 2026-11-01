# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for bodily needs and the unchanged turn contract."""
import asyncio
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import bodily
import body
import daily
import harness
import main
from astrbot.api.provider import ProviderRequest


class BodyNeedsTests(unittest.TestCase):
    def test_old_state_and_snapshot(self):
        with patch('time.time', return_value=1000000.0):
            core = body.BioCore()
            core.load_state({})
            snap = core.snapshot()
        self.assertEqual([snap[k] for k in ('sleepiness', 'hunger', 'physical_fatigue')], [0.2, 0.3, 0.1])
        self.assertEqual([snap[k] for k in ('last_sleep_end', 'last_meal', 'last_rest')], [1000000.0] * 3)

    def test_day_and_night_decay(self):
        start = datetime(2026, 10, 30, 14)
        with patch('time.time', return_value=start.timestamp()):
            core = body.BioCore()
        with patch('time.time', return_value=(start + timedelta(hours=4)).timestamp()):
            core._decay_to_now()
        self.assertAlmostEqual(core.sleepiness, 0.44)
        self.assertAlmostEqual(core.hunger, 0.62)
        self.assertAlmostEqual(core.physical_fatigue, 0.18)
        day = next(datetime(2026, 10, 1) + timedelta(days=i) for i in range(31)
                   if daily.schedule(datetime(2026, 10, 1) + timedelta(days=i), 0.5, 0, 0.1)[1] == '睡觉')
        start = day.replace(hour=5)
        with patch('time.time', return_value=start.timestamp()):
            core = body.BioCore()
        core.sleepiness, core.physical_fatigue = 0.9, 0.5
        with patch('time.time', return_value=(start + timedelta(hours=2)).timestamp()):
            core._decay_to_now()
        self.assertAlmostEqual(core.sleepiness, 0.4)
        self.assertEqual(core.last_sleep_end, (start + timedelta(hours=2)).timestamp())

    def test_midnight_preparing_sleep_is_asleep_but_evening_is_awake(self):
        day = next(datetime(2026, 11, 1) + timedelta(days=i) for i in range(30)
                   if daily.schedule(datetime(2026, 11, 1) + timedelta(days=i), 0.5, 0, 0.1)[1] == '准备睡觉')
        with patch('time.time', return_value=day.timestamp()):
            core = body.BioCore()
        core.sleepiness, core.physical_fatigue = 0.9, 0.8
        wake = day + timedelta(hours=7)
        with patch('time.time', return_value=wake.timestamp()):
            core._decay_to_now()
        self.assertEqual(core.sleepiness, 0)
        self.assertAlmostEqual(core.physical_fatigue, 0.1)
        self.assertEqual(core.last_sleep_end, wake.timestamp())

        evening = day.replace(hour=20)
        with patch('time.time', return_value=evening.timestamp()):
            core = body.BioCore()
        with patch.object(daily, 'schedule', return_value=('家', '准备睡觉', evening)):
            with patch('time.time', return_value=(evening + timedelta(hours=1)).timestamp()):
                core._decay_to_now()
        self.assertAlmostEqual(core.sleepiness, 0.26)
        self.assertEqual(core.last_sleep_end, evening.timestamp())

    def test_meal_midpoint_and_later_hunger(self):
        start = datetime(2026, 10, 30, 12)
        with patch('time.time', return_value=start.timestamp()):
            core = body.BioCore()
        core.hunger = 0.9
        midpoint = start + timedelta(hours=1)
        with patch('time.time', return_value=midpoint.timestamp()):
            core._decay_to_now()
        self.assertEqual(core.hunger, 0.1)
        self.assertEqual(core.last_meal, midpoint.timestamp())
        with patch('time.time', return_value=(midpoint + timedelta(minutes=30)).timestamp()):
            core._decay_to_now()
        self.assertAlmostEqual(core.hunger, 0.14)

    def test_event_helpers_and_bounds(self):
        core = body.BioCore()
        core.hunger = 1
        body.ate(core, 100)
        self.assertEqual((core.hunger, core.last_meal), (0.1, 100))
        core.sleepiness = core.physical_fatigue = 0.5
        body.slept(core, 100, 3700)
        self.assertEqual((core.sleepiness, core.physical_fatigue, core.last_sleep_end), (0.25, 0.4, 3700))
        body.rested(core, 60, 4000)
        self.assertAlmostEqual(core.physical_fatigue, 0.3)
        self.assertEqual(core.last_rest, 4000)
        body.exerted(core, 5, 4100)
        self.assertEqual(core.physical_fatigue, 1)
        body.slept(core, 0, 100000)
        self.assertEqual((core.sleepiness, core.physical_fatigue), (0, 0))
        body.rested(core, 999, 4200)
        self.assertEqual(core.physical_fatigue, 0)

    def test_feel_lines(self):
        self.assertEqual(bodily.feel_lines({}), [])
        lines = bodily.feel_lines({'sleepiness': 0.5, 'hunger': 0.8, 'physical_fatigue': 1})
        self.assertEqual(lines, ['有点困。', '很饿。'])
        self.assertEqual(bodily.feel_lines({'sleepiness': 0.35, 'hunger': 0.7}), ['有点困。', '有点饿。'])

    def test_typical_and_schedule(self):
        day = datetime(2026, 10, 30)
        self.assertEqual(len({daily.typical_now(day.replace(hour=h)) for h in (9, 12, 23)}), 3)
        for hour in (0, 8, 12, 14, 18, 23):
            now = day.replace(hour=hour)
            before = daily.schedule(now, 0.7, 0.1, 0.1)
            daily.typical_now(now)
            self.assertEqual(daily.schedule(now, 0.7, 0.1, 0.1), before)

    def test_derive_ignores_needs(self):
        core = body.BioCore()
        core.v, core.a, core.d, core.social = 0.2, 0.6, 0.4, 0.7
        core._derive()
        expected = core.energy, core.stress, core.v
        core.sleepiness = core.hunger = core.physical_fatigue = 1
        core._derive()
        self.assertEqual((core.energy, core.stress, core.v), expected)

    def test_turn_has_no_bodily_lines(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        test_basics.PLUGINS.append(plugin)
        event = harness.FakeEvent('hello', sender='10001', group='900001')
        core = plugin._core(event)
        core.sleepiness = core.hunger = core.physical_fatigue = 1
        request = ProviderRequest(prompt='hello')
        asyncio.run(plugin._prepare_turn(event, request))
        text = str(request.prompt) + str(request.system_prompt) + str(request.extra_user_content_parts)
        for line in bodily.feel_lines(core.snapshot()):
            self.assertNotIn(line, text)


if __name__ == '__main__':
    unittest.main()
