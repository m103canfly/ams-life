# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her mood reaches the material she picks a thing to do, a song, a note or a post from."""
import sys
import time
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import body  # noqa: E402
import interpretation  # noqa: E402
import life_loop as life  # noqa: E402

NOW = datetime(2026, 11, 2, 10, 0).timestamp()
# A root that is never created: these tests only read, and every read of a missing
# file is empty, so no test data of hers is touched or written.
ROOT = Path(__file__).resolve().parent.parent / '_life_mood_test_root_'


class Fake:
    """The few things the material builders want; the fake model is never called."""

    enabled = True
    config = {}
    _neutral_model = object()

    def __init__(self):
        self.core = body.BioCore()
        self.core.sleepiness = self.core.hunger = self.core.physical_fatigue = .1
        self.core.last_sleep_end = self.core.last_meal = NOW


class LifeMoodTests(unittest.TestCase):
    def setUp(self):
        self.p = Fake()
        for target, name, value in ((life, 'STATE_DIR', ROOT / 'states'),
                                    (life, 'DATA_DIR', ROOT / 'data')):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)

    def choice_materials(self):
        return life.materials(self.p, {}, {}, self.p.core, 'test', NOW, ['休息'], False)

    def song_lines(self):
        return '\n'.join(life.own_lines(self.p, self.p.core, NOW, 'test'))

    def post_materials(self):
        return life.post_materials(self.p, self.p.core, NOW, 'test')

    def mood_lines(self, text):
        return [line for line in text.splitlines() if line.startswith('心情：')]

    def test_1_her_choice_material_says_how_she_feels_now(self):
        self.p.core.v = -0.5
        self.assertIn('心情：心里有点沉', self.choice_materials())
        self.p.core.v = 0.5
        text = self.choice_materials()
        self.assertIn('心情：心情不错', text)
        self.assertNotIn('心里有点沉', text)

    def test_2_the_same_line_is_in_a_song_and_in_a_public_line(self):
        self.p.core.v = -0.5
        line = '心情：心里有点沉'
        self.assertIn(line, self.song_lines())
        self.assertIn(line, self.post_materials())
        self.assertIn(line, life.song_materials(self.p, self.p.core, NOW, 'test'))

    def test_3_no_line_when_the_brief_says_nothing(self):
        for empty in ('', None):
            with patch.object(interpretation, 'body_brief', return_value=empty):
                for text in (self.choice_materials(), self.song_lines(), self.post_materials()):
                    self.assertEqual(self.mood_lines(text), [])

    def test_4_a_recent_mood_event_is_said_in_every_material(self):
        self.p.core.mood_events = [{'kind': 'woken', 'ts': time.time() - 60}]
        for text in (self.choice_materials(), self.song_lines(), self.post_materials()):
            self.assertIn('刚被吵醒', text)

    def test_5_the_line_is_read_now_not_remembered(self):
        self.p.core.v, self.p.core.social = -0.5, 0.0
        first = self.choice_materials()
        self.assertIn('心里有点沉', first)
        self.assertIn('不太想说话', first)
        # The numbers change; the next material is built from them, not from the last.
        self.p.core.v, self.p.core.social = 0.5, 0.8
        second = self.choice_materials()
        self.assertIn('心情不错', second)
        self.assertIn('挺想说话', second)
        self.assertNotIn('心里有点沉', second)
        self.assertNotIn('不太想说话', second)
        # A mood event that just happened is said at once, in the same material.
        self.p.core.mood_events = [{'kind': 'woken', 'ts': time.time() - 30}]
        third = self.choice_materials()
        self.assertIn('刚被吵醒', third)
        self.assertNotIn('刚被吵醒', second)


if __name__ == '__main__':
    unittest.main()
