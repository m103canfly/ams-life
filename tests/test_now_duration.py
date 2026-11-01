# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for the duration of the shared now state."""
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import harness
import mixin_selfie as phone
from test_selfie import Event, Phone


class NowDuration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'now.json'
        path_patch = patch.object(phone, 'NOW_PATH', self.path)
        path_patch.start()
        self.addCleanup(path_patch.stop)
        self.clock = harness.Clock(datetime(2026, 10, 30, 14, 10).timestamp())
        clock_patch = patch.object(phone.time, 'time', self.clock)
        clock_patch.start()
        self.addCleanup(clock_patch.stop)
        self.p = Phone()
        self.event = Event()

    def state(self):
        return json.loads(self.path.read_text(encoding='utf-8'))

    async def test_repeat_keeps_start_and_change_restarts(self):
        await self.p._tool_set_now(self.event, '办事大厅', '排队')
        start = self.state()['start']
        self.clock.advance(30 * 60)
        await self.p._tool_set_now(self.event, '办事大厅', '排队')
        self.assertEqual(self.state()['start'], start)
        self.assertIn('已经 30 分钟', self.p._now_line(self.event))
        await self.p._tool_set_now(self.event, '家', '看书')
        self.assertNotEqual(self.state()['start'], start)

    async def test_duration_reminder_and_update(self):
        await self.p._tool_set_now(self.event, '家', '看书', minutes=40)
        self.clock.advance(30 * 60)
        reminder = '这件事按说已经做完了，现在干什么由你定。'
        self.assertNotIn(reminder, self.p._now_line(self.event))
        self.clock.advance(20 * 60)
        self.assertIn(reminder, self.p._now_line(self.event))
        await self.p._tool_set_now(self.event, '家', '看书', minutes=80)
        self.assertEqual(self.state()['minutes'], 80)
        self.assertNotIn(reminder, self.p._now_line(self.event))

    async def test_repeats_do_not_delay_schedule(self):
        await self.p._tool_set_now(self.event, '家', '看书')
        start = self.state()['start']
        for _ in range(8):
            self.clock.advance(20 * 60)
            await self.p._tool_set_now(self.event, '家', '看书')
            self.assertEqual(self.state()['start'], start)
        self.assertIn('已经 2 小时 40 分钟', self.p._now_line(self.event))
        self.clock.advance(20 * 60)
        self.p._now_line(self.event)
        self.assertEqual(self.state()['source'], 'schedule')

    async def test_minutes_clamped_and_invalid_ignored(self):
        await self.p._tool_set_now(self.event, '家', '看书', minutes=1000)
        self.assertEqual(self.state()['minutes'], 240)
        await self.p._tool_set_now(self.event, '家', '散步', minutes='abc')
        self.assertNotIn('minutes', self.state())
        await self.p._tool_set_now(self.event, '家', '散步', minutes=1)
        self.assertEqual(self.state()['minutes'], 5)
        await self.p._tool_set_now(self.event, '家', '散步', minutes='abc')
        self.assertEqual(self.state()['minutes'], 5)

    async def test_schedule_has_elapsed_time(self):
        line = self.p._now_line(self.event)
        self.assertEqual(self.state()['source'], 'schedule')
        self.assertIn('已经 ', line)
        self.assertIn('分钟', line)
