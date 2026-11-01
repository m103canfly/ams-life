# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""A quiet chat counts only after the other side has spoken in it."""
import json
import sys
import time
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import body
import harness
import life_loop as life
import mixin_selfie as phone


class Windows:
    """A fake plugin with chat windows only."""
    def __init__(self, rows):
        self.rows = rows

    def _window_places(self):
        return list(self.rows)

    def _read_window(self, here):
        return {'recent': self.rows[here]}


class QuietChatTests(unittest.TestCase):
    def test_her_own_message_alone_is_not_quiet(self):
        start = 1_000_000.0
        plugin = Windows({'private:10001': [{'role': 'assistant', 'ts': start}]})
        state = {}
        self.assertEqual(life.quiet_chats(plugin, state, start + 600), [])
        self.assertEqual(life.quiet_chats(plugin, state, start + 1800), [])

    def test_their_message_and_her_reply_are_quiet_once(self):
        start = 2_000_000.0
        plugin = Windows({'private:10001': [{'role': 'user', 'ts': start},
                                            {'role': 'assistant', 'ts': start + 60}]})
        state = {}
        self.assertEqual(life.quiet_chats(plugin, state, start + 60 + 599), [])
        due = life.quiet_chats(plugin, state, start + 60 + 600)
        self.assertEqual(due, [('private:10001', start + 60)])
        for here, exchange in due:
            state.setdefault('quiet_seen', {})[here] = exchange
        self.assertEqual(life.quiet_chats(plugin, state, start + 60 + 1200), [])

    def test_called_exchange_is_quiet_once(self):
        start = 3_000_000.0
        plugin = Windows({'group:900001': [{'role': 'user', 'ts': start}]})
        state = {'called': {'group:900001': start}}
        self.assertEqual(life.quiet_chats(plugin, state, start + 599), [])
        due = life.quiet_chats(plugin, state, start + 600)
        self.assertEqual(due, [('group:900001', start)])
        for here, exchange in due:
            state.setdefault('quiet_seen', {})[here] = exchange
        self.assertEqual(life.quiet_chats(plugin, state, start + 1200), [])


class Person:
    """A fake plugin for one life tick; the model only counts calls."""
    def __init__(self):
        self.enabled = True
        self.config = {'life_loop_enabled': True, 'proactive_owner_enabled': True,
                       'owner_qq': '900001'}
        self._neutral_model = object()
        self.core = body.BioCore()
        self.core.sleepiness = self.core.hunger = self.core.physical_fatigue = .1
        self.core._life_body_loaded = True
        self.core._life_now_path = phone.NOW_PATH
        self.core._life_state_path = life.STATE_DIR / 'life.json'
        self.windows = {}
        self.calls = []
        self.answer = {'do': '什么都不干', 'detail': '在家里发呆', 'minutes': 120}
        self._life_start_checked = True
        self.sent = AsyncMock(return_value=SimpleNamespace(ok=True))
        self._neutral_messenger = SimpleNamespace(send=self.sent)

    def _core(self, event=None): return self.core
    def _attention_cfg(self): return {'soft': 8, 'hard': 10}
    def _spent_today(self): return 0
    def _browse_on(self): return False
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows[here]}
    def _llm_allowed(self, kind): return True
    def _read_library(self, **kwargs): return {'entries': []}
    def _red_line(self, text, where): return ''
    def _owner_rules(self): return []
    def _names_index(self): return {}
    def _set_now(self, *args, **kwargs): pass

    async def _persona_text(self, event): return 'A fictional persona.'

    async def _check_reply(self, event, text): return {}

    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        return parser(json.dumps(self.answer, ensure_ascii=False))

    def _window_add_reply(self, event, text):
        here = 'private:' + self.config['owner_qq']
        self.windows.setdefault(here, []).append({'role': 'assistant', 'ts': time.time()})


class LifeLoopQuietTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.clock = harness.Clock(datetime(2026, 11, 1, 10).timestamp())
        self.state = {'last_think_ts': 0, 'today': {}, 'last_body': {},
                      'pending': {'group_browse': False, 'go_browse': False},
                      'last_item_id': ''}
        self.store = Mock()
        self.store.return_value.day.return_value = []
        self.store.return_value.add.return_value = {'id': 'fake-row'}
        for target, name, value in ((life, 'read_state', lambda: self.state),
                                    (life, 'save_state', lambda state: None),
                                    (life, 'current', lambda: {}),
                                    (life.her_days, 'Store', self.store),
                                    (life.time, 'time', self.clock)):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = Person()

    async def test_tell_owner_does_not_make_quiet_after_ten_minutes(self):
        now = self.clock()
        self.assertTrue(await life.tell_owner(self.p, '今天看到一棵树', now, []))
        self.assertEqual(len(self.p.windows['private:900001']), 1)
        self.assertEqual(self.p.windows['private:900001'][0]['role'], 'assistant')
        await life.tick(self.p, now + 600)
        self.assertEqual(self.p.calls, [])


if __name__ == '__main__':
    unittest.main()
