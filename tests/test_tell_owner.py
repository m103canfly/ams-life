# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for owner-only autonomy."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import life_loop
import discretion
import mixin_autonomy
import send_check


class OwnerMaterialsTest(unittest.TestCase):
    def test_unanswered_after_last_owner_message(self):
        rows = [{'role': 'assistant'}, {'role': 'user'},
                {'role': 'assistant'}, {'role': 'assistant'}, {'role': 'assistant'}]
        plugin = SimpleNamespace(config={'owner_qq': '900001'},
                                 _read_window=lambda place: {'recent': rows})
        self.assertEqual(life_loop.owner_unanswered(plugin), 3)

    def test_materials_show_unanswered_count(self):
        rows = [{'role': 'user'}] + [{'role': 'assistant'} for _ in range(3)]
        plugin = SimpleNamespace(config={'owner_qq': '900001', 'proactive_owner_enabled': True},
                                 self_model={}, _read_window=lambda place: {'recent': rows})
        core = SimpleNamespace(sleepiness=0, hunger=0, physical_fatigue=0,
                               last_sleep_end=0, last_meal=0)
        with patch.object(life_loop.weather, 'weather_line', return_value=''), \
                patch.object(life_loop.her_days, 'Store') as store:
            store.return_value.day.return_value = []
            text = life_loop.materials(plugin, {}, {}, core, 'test', 100, ['休息'], False)
        self.assertIn('主人还没回的有 3 条', text)


class OwnerSendingTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.forbidden = []
        self.sent = AsyncMock(return_value=SimpleNamespace(ok=True))
        self.plugin = SimpleNamespace(
            config={'owner_qq': '900001', 'proactive_owner_enabled': True},
            _spent_today=lambda: 0, _attention_cfg=lambda: {'soft': 8, 'hard': 10},
            _neutral_messenger=SimpleNamespace(send=self.sent),
            _read_library=lambda **kwargs: {'entries': [{'text': '秘密暗号蓝鲸漫步',
                'origin': discretion.make_origin('private:10003', ['10003'])}]},
            _window_places=lambda: [], _here=lambda event: event.incoming.place,
            _speaker=lambda event: (event.incoming.sender_id, ''),
            _forbid=lambda event, ident, text, people: self.forbidden.append({'id': ident, 'text': text}),
            _check_reply=self.check, _red_line=lambda text, where: '', _owner_rules=lambda: [],
            _window_add_reply=Mock(), self_model={}, _save_self_model=Mock())
        self.state_patch = patch.object(life_loop, 'read_state', return_value={})
        self.current_patch = patch.object(life_loop, 'current', return_value={})
        self.state_patch.start()
        self.current_patch.start()
        self.addCleanup(self.state_patch.stop)
        self.addCleanup(self.current_patch.stop)

    async def check(self, event, text):
        return send_check.check(text, self.forbidden)

    async def test_send_only_owner_and_check(self):
        self.assertTrue(await life_loop.tell_owner(self.plugin, '今天看到有趣的东西', 100, []))
        self.assertEqual(self.sent.await_args.args[0], 'private:900001')
        self.assertFalse(await life_loop.tell_owner(self.plugin, '秘密暗号蓝鲸漫步', 101, []))
        self.assertEqual(self.sent.await_count, 1)

    async def test_budget_and_sleep_block(self):
        self.plugin._spent_today = lambda: 8
        self.assertFalse(await life_loop.tell_owner(self.plugin, '你好', 100, []))
        self.plugin._spent_today = lambda: 0
        self.state_patch.stop()
        with patch.object(life_loop, 'read_state', return_value={'sleep': {'end': 200}}):
            self.assertFalse(await life_loop.tell_owner(self.plugin, '你好', 100, []))
        self.sent.assert_not_awaited()


class OwnerAutonomyTest(unittest.IsolatedAsyncioTestCase):
    async def test_owner_switch_does_not_send_old_templates_to_anyone(self):
        core = SimpleNamespace(autonomy_enabled=True, autonomy_loop_enabled=False,
                               noise_tick=Mock())
        plugin = SimpleNamespace(config={'proactive_owner_enabled': True, 'owner_qq': '900001'},
                                 autonomy_loop_enabled=False, proactive_autonomy=True,
                                 proactive_send=True, autonomy_loop_token_only=True,
                                 _autonomy_private_sessions={
                                     'friend': {'sender_id': '10003', 'ts': 100},
                                     'owner': {'sender_id': '900001', 'ts': 100}},
                                 cores={'friend': core, 'owner': core},
                                 _autonomy_exit_plan=Mock(return_value='send'),
                                 _maybe_proactive_send=AsyncMock())
        result = await mixin_autonomy.AutonomyMixin._autonomy_tick(plugin, now=101)
        self.assertEqual(result, [])
        core.noise_tick.assert_called_once()
        plugin._maybe_proactive_send.assert_not_awaited()
