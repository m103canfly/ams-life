# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Strong-event cooldowns belong to places."""
import inspect
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot
import harness
import main
import mixin_events
import turn


class StrongEventPlace(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin._llm_allowed = Mock(return_value=True)
        self.plugin._window_lines = Mock(return_value=[])
        self.plugin._event_origin = Mock(return_value={})
        self.plugin._mask_if_safety = lambda text: text
        self.plugin._provider_for = AsyncMock(return_value=object())
        self.model = types.SimpleNamespace(chat=AsyncMock(return_value=types.SimpleNamespace(text='{}')))
        self.plugin._model = Mock(return_value=self.model)
        self.core = types.SimpleNamespace(_intensity=lambda: 0.8, v=0.0, a=0.8, stress=0.0)

    def event(self, group, neutral=True):
        event = harness.FakeEvent('invented text', sender='10001', name='Example', group=group, self_id='20002')
        return turn.TurnEvent(adapter_astrbot.from_astrbot(event)) if neutral else event

    async def archive(self, event):
        await self.plugin._maybe_archive_strong_event(event, self.core, 'invented text')

    async def test_neutral_groups_have_independent_cooldowns(self):
        first, second = self.event('900001'), self.event('900002')
        self.assertEqual((first.unified_msg_origin, second.unified_msg_origin), ('', ''))
        with patch.object(mixin_events.time, 'time', return_value=1000):
            await self.archive(first)
            await self.archive(second)
        self.assertEqual(self.model.chat.await_count, 2)

    async def test_same_place_waits_600_seconds(self):
        event = self.event('900001')
        with patch.object(mixin_events.time, 'time', side_effect=lambda: self.now):
            self.now = 1000
            await self.archive(event)
            self.now = 1599
            await self.archive(event)
            self.assertEqual(self.model.chat.await_count, 1)
            self.now = 1601
            await self.archive(event)
        self.assertEqual(self.model.chat.await_count, 2)

    async def test_astrbot_groups_have_independent_cooldowns(self):
        first, second = self.event('900001', False), self.event('900002', False)
        self.assertNotEqual(first.unified_msg_origin, second.unified_msg_origin)
        with patch.object(mixin_events.time, 'time', return_value=1000):
            await self.archive(first)
            await self.archive(second)
        self.assertEqual(self.model.chat.await_count, 2)

    def test_hook_does_not_read_session_string(self):
        self.assertNotIn('unified_msg_origin', inspect.getsource(mixin_events.EventsMixin._maybe_archive_strong_event))
