# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for private dates and forgetting."""
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import test_her  # noqa: E402
import adapter_onebot  # noqa: E402
import her  # noqa: E402
import mixin_discretion  # noqa: E402
import mixin_selfie  # noqa: E402
import mixin_turn  # noqa: E402
import our_days  # noqa: E402
import turn  # noqa: E402


def event(sender='10001', group=None):
    payload = {'post_type': 'message', 'message_type': 'group' if group else 'private',
               'self_id': 20002, 'user_id': int(sender), 'sender': {'user_id': int(sender), 'nickname': 'Alice'},
               'message': [{'type': 'text', 'data': {'text': 'hello'}}]}
    if group:
        payload['group_id'] = int(group)
    return turn.TurnEvent(adapter_onebot.from_onebot(payload))


class OurDaysTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for p in test_her.data_paths(self.root):
            p.start()
            self.addCleanup(p.stop)
        for module in (mixin_selfie, mixin_discretion):
            p = patch.object(module, 'DATA_DIR', self.root)
            p.start()
            self.addCleanup(p.stop)
        self.plugin = her.Her(test_her.route_collector(), config={'owner_qq': '10001'})
        self.addCleanup(self.close_stores)

    def close_stores(self):
        for name in ('_forget_reg', '_vectors_db'):
            store = getattr(self.plugin, name, None)
            if store is not None:
                store.close()

    async def test_tool_private_boundary_and_record(self):
        owner, other, group = event(), event('10003'), event(group='900001')
        tool = next(t for t in self.plugin._phone_tools(owner) if t.name == 'remember_day')
        for elsewhere in (other, group):
            self.assertNotIn('remember_day', [t.name for t in self.plugin._phone_tools(elsewhere)])
            self.assertNotEqual(await tool.handler(elsewhere, date='02-17', what='相遇'), '记下了。')
        self.assertEqual(await tool.handler(owner, date='2026-02-17', what='相遇'), '记下了。')
        row = json.loads((self.root / 'states' / 'our_days.json').read_text(encoding='utf-8'))[0]
        self.assertEqual((row['date'], row['what'], row['related_users']), ('2026-02-17', '相遇', ['10001']))
        self.assertEqual(row['origin']['where'], 'private:10001')
        self.assertIn('ts', row)
        for bad_date, what in [('02-30', '相遇'), ('2026-2-17', '相遇'), ('02-17', '字' * 21)]:
            self.assertNotEqual(await tool.handler(owner, date=bad_date, what=what), '记下了。')
        self.assertEqual(len(json.loads((self.root / 'states' / 'our_days.json').read_text(encoding='utf-8'))), 1)

    async def test_prompt_order_and_privacy_in_both_paths(self):
        our_days.remember(self.root, '10001', '02-17', '相遇')
        with patch.object(mixin_turn.calendar_cn, 'today_line', return_value='今天春节。'), \
                patch.object(mixin_selfie, '_our_days_line', wraps=mixin_selfie._our_days_line):
            for enabled in (False, True):
                self.plugin.inject_intent = enabled
                self.plugin._now_line = lambda event: '此刻：在家'
                for ev, allowed in ((event(), True), (event('10003'), False), (event(group='900001'), False)):
                    request = turn.TurnRequest(prompt='hello')
                    await self.plugin._prepare_turn(ev, request)
                    text = request.system_prompt + ''.join(x.get('text', '') for x in request.extra_user_content_parts)
                    self.assertEqual('你们之间记下的日子：' in text, allowed)
                    if allowed:
                        self.assertIn('[日子] 今天春节。\n你们之间记下的日子：', text)

    def test_line_dates_and_empty(self):
        self.assertEqual(our_days.line(self.root, '10001', date(2026, 2, 14)), '你们之间记下的日子：还没有。')
        our_days.remember(self.root, '10001', '12-25', '远日')
        our_days.remember(self.root, '10001', '02-17', '相遇')
        line = our_days.line(self.root, '10001', date(2026, 2, 14))
        self.assertIn('再过 3 天是相遇。', line)
        self.assertLess(line.index('相遇'), line.index('远日'))
        self.assertIn('今天是相遇。', our_days.line(self.root, '10001', date(2026, 2, 17)))
        self.assertEqual(our_days.line(self.root, '10003', date(2026, 2, 14)), '你们之间记下的日子：还没有。')

    def test_forget_and_failure_does_not_block(self):
        our_days.remember(self.root, '10001', '02-17', '相遇')
        our_days.remember(self.root, '10003', '03-01', '另一日')
        self.plugin._forget(person='10001')
        rows = json.loads((self.root / 'states' / 'our_days.json').read_text(encoding='utf-8'))
        self.assertEqual([row['what'] for row in rows], ['另一日'])
        with patch.object(our_days, 'forget', side_effect=OSError('private details')), \
                patch.object(mixin_discretion.logger, 'warning') as warning:
            result = self.plugin._forget(person='10003')
        self.assertIn('memories', result)
        self.assertTrue(any('our days delete failed' in call.args[0] for call in warning.call_args_list))
