# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline calendar checks."""
import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import calendar_cn  # noqa: E402
import look  # noqa: E402


class CalendarTests(unittest.TestCase):
    def test_festivals_and_upcoming(self):
        for day, expected in ((date(2026, 2, 17), '今天春节。'),
                              (date(2026, 2, 14), '今天情人节。'),
                              (date(2026, 9, 22), '再过 3 天是中秋。'),
                              (date(2027, 2, 6), '今天春节。'),
                              (date(2028, 10, 26), '今天重阳。')):
            self.assertEqual(calendar_cn.today_line(day), expected)

    def test_term_and_look(self):
        day = date(2026, 11, 7)
        self.assertEqual(calendar_cn.today_line(day), '今天立冬。')
        self.assertEqual(look.season_of(day), ('冬', '立冬'))
        self.assertIn('季节：冬，立冬', look.look_line(day, '', {}))

    def test_outside_table_warns_once(self):
        with patch.object(calendar_cn, '_warned', False):
            with self.assertLogs('calendar_cn', level='WARNING') as logs:
                self.assertEqual(calendar_cn.today_line(date(2031, 10, 1)), '今天国庆。')
                calendar_cn.today_line(date(2031, 10, 2))
            self.assertEqual(len(logs.output), 1)
            self.assertNotIn('中秋', calendar_cn.today_line(date(2031, 10, 1)))

    def test_same_day_precedence_and_year_boundary(self):
        self.assertEqual(calendar_cn.today_line(date(2027, 8, 8)), '今天立秋。')
        self.assertEqual(calendar_cn.today_line(date(2026, 12, 30)), '再过 2 天是元旦。')
