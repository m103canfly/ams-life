# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check assistant history sent to the model and kept in storage."""
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import turn
import turn_runner
import test_turn_runner


class HistoryOneLineTests(unittest.IsolatedAsyncioTestCase):
    setUp = test_turn_runner.OneTurn.setUp
    close_cached_stores = test_turn_runner.OneTurn.close_cached_stores
    event = test_turn_runner.OneTurn.event

    async def prepare(self, contexts):
        request = turn.TurnRequest(prompt='hello', contexts=contexts)
        await self.her._prepare_turn(self.event(), request)
        return request.contexts

    async def toggle(self, value):
        async def get_json(silent=False):
            return {'key': 'history_one_line', 'value': value}

        quart = types.ModuleType('quart')
        quart.request = types.SimpleNamespace(get_json=get_json)
        self.her._config_path = Path(self.tmp.name) / 'config.json'
        with patch.dict(sys.modules, {'quart': quart}):
            return await self.her.page_toggle()

    async def test_assistant_lines_and_user_history(self):
        contexts = await self.prepare([
            {'role': 'assistant', 'content': '嗯嗯\n我也是'},
            {'role': 'user', 'content': 'hello\nthere'},
        ])
        self.assertEqual(contexts[0]['content'], '嗯嗯 我也是')
        self.assertEqual(contexts[1]['content'],
                         '（历史消息，发言人和时间未核实）（原文）hello\n（原文）there')

    async def test_switch_off_keeps_assistant_lines(self):
        self.her.config['history_one_line'] = False
        contexts = await self.prepare([{'role': 'assistant', 'content': 'a\nb'}])
        self.assertEqual(contexts[0]['content'], 'a\nb')

    async def test_missing_switch_defaults_to_on(self):
        self.her.config.pop('history_one_line', None)
        contexts = await self.prepare([{'role': 'assistant', 'content': 'a\nb'}])
        self.assertEqual(contexts[0]['content'], 'a b')

    async def test_panel_toggle_changes_next_preparation(self):
        config = self.her.config
        result = await self.toggle(False)
        self.assertEqual(result['status'], 'ok')
        self.assertIs(self.her.config, config)
        self.assertIs(config['history_one_line'], False)
        contexts = await self.prepare([{'role': 'assistant', 'content': 'a\nb'}])
        self.assertEqual(contexts[0]['content'], 'a\nb')

    async def test_panel_toggle_between_turns(self):
        self.store.append('group:900001', 'assistant', 'a\nb')
        self.fake.say('first')
        self.fake.say('second')
        await turn_runner.run_turn(self.her, self.event())
        self.assertIn({'role': 'assistant', 'content': 'a b'}, self.fake.requests[0]['messages'])
        self.assertEqual((await self.toggle(False))['status'], 'ok')
        await turn_runner.run_turn(self.her, self.event())
        self.assertIn({'role': 'assistant', 'content': 'a\nb'}, self.fake.requests[1]['messages'])

    async def test_code_and_list_blocks(self):
        contexts = await self.prepare([
            {'role': 'assistant', 'content': '看这个\n- 一\n- 二\n再看\n```\na\nb\n```'},
        ])
        self.assertEqual(contexts[0]['content'], '看这个 - 一\n- 二 再看 ```\na\nb\n```')

    async def test_list_content(self):
        contexts = await self.prepare([
            {'role': 'assistant', 'content': [{'type': 'text', 'text': 'a\nb'},
                                              {'type': 'image', 'url': 'fake'}]},
        ])
        self.assertEqual(contexts[0]['content'], [{'type': 'text', 'text': 'a b'},
                                                  {'type': 'image', 'url': 'fake'}])

    async def test_stored_history_remains_multiline(self):
        self.store.append('group:900001', 'assistant', '嗯嗯\n我也是')
        self.fake.say('okay')
        await turn_runner.run_turn(self.her, self.event())
        messages = self.fake.requests[0]['messages']
        self.assertIn({'role': 'assistant', 'content': '嗯嗯 我也是'}, messages)
        self.assertEqual(self.store.recent('group:900001')[0]['content'], '嗯嗯\n我也是')


if __name__ == '__main__':
    unittest.main()
