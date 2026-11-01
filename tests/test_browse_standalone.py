# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for standalone browsing trips."""
import asyncio
import json
import sys
import tempfile
import types
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import browse
import harness
import main
import mixin_attention
import mixin_browse
import model_client


URL = 'https://example.invalid/page'
OTHER = 'https://example.invalid/other'
USAGE = {'input_miss': 100000, 'input_hit': 0, 'output': 10000}


class FakeModel(model_client.ModelClient):
    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []

    async def chat(self, **kwargs):
        self.requests.append(kwargs)
        text, calls = self.replies.pop(0)
        return model_client.ModelReply(text, tuple(calls), USAGE, '')


def call(name, **kwargs):
    return model_client.ToolCall('call', name, kwargs)


class Trip(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        tmp = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.stack.enter_context(patch.object(mixin_attention, 'SPEND_PATH', tmp / 'spend.json'))
        self.stack.enter_context(patch.object(mixin_browse, 'resolve_host', return_value=['93.184.216.34']))
        self.plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        test_basics.PLUGINS.append(self.plugin)
        self.plugin.enabled = self.plugin.browse_enabled = True
        self.plugin.browse_trips_enabled = True
        self.plugin.browser_enabled = False
        self.plugin.self_decide = False
        self.plugin._browse_ledger_obj = browse.Ledger(tmp / 'ledger.json')
        self.plugin._browse_names = lambda: []
        self.plugin._browse_topics = lambda: []
        self.plugin._persona_text = AsyncMock(return_value='persona')
        self.plugin._job_stale = lambda: False
        self.plugin._embed_text = AsyncMock(return_value=[])
        self.library = {'entries': []}
        self.plugin._read_library = lambda **kwargs: self.library
        self.plugin._write_library = lambda lib: True
        self.plugin._save_self_model = Mock()
        self.search = AsyncMock(return_value=json.dumps({'results': [{'title': 'Made up', 'url': URL, 'snippet': 'text'}]}))
        self.read = AsyncMock(return_value='Title: Made up\nContent: Page text')
        self.plugin._builtin_web_tool = lambda kind: types.SimpleNamespace(call=self.search if kind == 'search' else self.read)
        self.core = types.SimpleNamespace(boredom=0.8, novelty_need=0.8)

    def run_trip(self, replies):
        self.plugin._neutral_model = FakeModel(replies)
        return asyncio.run(self.plugin._browse_trip(self.core, 100000))

    def test_search_read_memory_wish_and_both_accounts_without_astrbot(self):
        final = json.dumps({'notes': [{'url': URL, 'title': 'Made up', 'said': 'Page text'}],
                            'share': [{'url': URL, 'what': 'A page'}]})
        replies = [('', [call(browse.SEARCH_TOOL, query='cats')]),
                   ('', [call(browse.READ_TOOL, url=URL)]), (final, [])]
        modules = {k: v for k, v in sys.modules.items() if k == 'astrbot' or k.startswith('astrbot.')}
        with patch.dict(sys.modules):
            for name in modules:
                del sys.modules[name]
            result = self.run_trip(replies)
        self.assertEqual(result['notes'], 1)
        self.assertEqual(result['share'], 1)
        self.assertEqual(self.library['entries'][0]['web']['url'], URL)
        self.assertEqual(self.library['entries'][0]['asked_in'], browse.SELF_ASKED_IN)
        self.assertEqual(len(self.plugin.self_model['share_wishes']), 1)
        self.assertAlmostEqual(self.core.boredom, 0.6)
        self.assertAlmostEqual(self.core.novelty_need, 0.65)
        self.assertEqual(self.plugin._browse_ledger().row()['input_miss'], 300000)
        day = next(iter(json.loads(mixin_attention.SPEND_PATH.read_text('utf-8')).values()))
        self.assertGreater(day['browse'], 0)
        self.assertEqual(day['calls'], 3)

    def test_unlisted_address_is_not_read_or_kept(self):
        final = json.dumps({'notes': [{'url': OTHER, 'said': 'Made up'}],
                            'share': [{'url': OTHER, 'what': 'Made up'}]})
        result = self.run_trip([('', [call(browse.READ_TOOL, url=OTHER)]), (final, [])])
        self.read.assert_not_awaited()
        self.assertEqual((result['notes'], result['share']), (0, 0))
        self.assertIn(mixin_browse.NOT_LISTED, self.plugin._neutral_model.requests[1]['messages'][-1]['content'])

    def test_sixth_search_is_refused_and_eighth_round_is_last(self):
        replies = [('', [call(browse.SEARCH_TOOL, query='topic %d' % i)]) for i in range(7)] + [('done', [])]
        self.run_trip(replies)
        model = self.plugin._neutral_model
        self.assertEqual(self.search.await_count, 5)
        self.assertEqual(len(model.requests), 8)
        self.assertIn(browse.NO_MORE, model.requests[6]['messages'][-1]['content'])
        self.assertIsNone(model.requests[-1]['tools'])

    def test_hard_budget_stops_trip_before_state_changes(self):
        mixin_attention.SPEND_PATH.write_text(json.dumps({mixin_attention.time.strftime('%Y-%m-%d'): {'browse': 10}}), 'utf-8')
        self.plugin._neutral_model = FakeModel([])
        self.assertFalse(asyncio.run(self.plugin._maybe_go_browse()))
        self.assertEqual(asyncio.run(self.plugin._browse_trip(self.core, 100000)), {})
        self.assertEqual(self.plugin._browse_ledger().row()['trips'], 0)
        self.assertEqual(self.plugin._neutral_model.requests, [])

    def test_interactive_switch_uses_ordinary_trip(self):
        self.plugin.browser_interactive_enabled = True
        with patch.object(mixin_browse.logger, 'info') as info:
            self.run_trip([('done', [])])
        self.assertTrue(any('新程序的出门还不带互动浏览器' in str(item) for item in info.call_args_list))
        self.assertEqual(len(self.plugin._neutral_model.requests[0]['tools']), 2)

    def test_counting_with_self_decide_enabled_and_mid_trip_budget(self):
        self.plugin.self_decide = True
        self.plugin.config['day_budget_yuan'] = 0.01
        self.run_trip([('', [call(browse.SEARCH_TOOL, query='cats')]), ('unused', [])])
        day = next(iter(json.loads(mixin_attention.SPEND_PATH.read_text('utf-8')).values()))
        self.assertEqual(day['calls'], 1)
        self.assertEqual(len(self.plugin._neutral_model.requests), 1)
