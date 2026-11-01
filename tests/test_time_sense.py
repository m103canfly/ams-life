# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for time material and its conversation boundary."""
import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402
import harness  # noqa: E402
import interpretation  # noqa: E402
import main  # noqa: E402
import mixin_turn  # noqa: E402
from astrbot.api.provider import ProviderRequest  # noqa: E402


class TimeSenseTests(unittest.TestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        test_basics.PLUGINS.append(self.plugin)

    def test_continuity_private_and_group(self):
        plugin = self.plugin
        plugin._continuity_summary = lambda event, core: '原来那句摘要'
        plugin._speaker = lambda event: ('10001', 'Alice')
        for place, days, expected, summary in (
                ('private:10001', 5, '上次跟他说话是 5 天前', True),
                ('private:10001', 1, '', True),
                ('group:900001', 5, '好久没见他了（5 天）', True)):
            plugin._here = lambda event, place=place: place
            cont = plugin._continuity_context(None, None, {'absence': {'gap_days': days}}, prior_loops=[])
            text = interpretation.render_compact(None, continuity=cont)
            if expected:
                self.assertIn(expected, text)
            else:
                self.assertNotIn('上次跟他说话是', text)
            self.assertEqual('原来那句摘要' in text, summary)

    def test_calendar_after_now_in_both_paths(self):
        for enabled in (False, True):
            plugin = self.plugin
            plugin.inject_intent = enabled
            plugin._now_line = lambda event: '此刻：测试'
            event = harness.FakeEvent('hello', sender='10001', group='900001')
            req = ProviderRequest(prompt='hello')
            with patch.object(mixin_turn.calendar_cn, 'today_line', return_value='今天春节。'):
                asyncio.run(plugin.on_llm_request(event, req))
            text = str(req.system_prompt) + ''.join(part.get('text', '') for part in req.extra_user_content_parts)
            self.assertIn('此刻：测试\n[日子] 今天春节。', text)
