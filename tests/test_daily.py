"""Offline checks for the daily schedule."""
import unittest
from datetime import datetime, timedelta

import daily


class DailyTests(unittest.TestCase):
    def test_night_and_meals(self):
        day = datetime(2026, 10, 30)
        for hour in (0, 2, 6):
            where, doing, _ = daily.schedule(day.replace(hour=hour), 0.7, 0.1, 0.1)
            self.assertEqual(where, '家')
            self.assertIn('睡', doing)
        for hour in (8, 12, 18):
            self.assertIn('吃', daily.schedule(day.replace(hour=hour), 0.7, 0.1, 0.1)[1])

    def test_same_period_is_stable_and_dates_vary(self):
        day = datetime(2026, 10, 1, 14)
        seen = set()
        for offset in range(40):
            now = day + timedelta(days=offset)
            first = daily.schedule(now, 0.8, 0.1, 0.1)
            self.assertEqual(first, daily.schedule(now + timedelta(minutes=40), 0.8, 0.1, 0.1))
            seen.add(first[:2])
        self.assertGreater(len(seen), 1)

    def test_low_energy_mood_or_high_stress_favors_home(self):
        day = datetime(2026, 10, 1, 14)
        def home_count(energy, mood, stress):
            return sum(daily.schedule(day + timedelta(days=i), energy, mood, stress)[0] == '家'
                       for i in range(120))
        baseline = home_count(0.8, 0.1, 0.1)
        for values in ((0.2, 0.1, 0.1), (0.8, -0.5, 0.1), (0.8, 0.1, 0.7)):
            self.assertGreater(home_count(*values), baseline)
