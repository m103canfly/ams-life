# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for standalone and AstrBot routing."""
import asyncio
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import deepseek_tools
import harness
import main
import mixin_browse
import mixin_media
import mixin_pages
import mixin_turn
import turn
from test_her import route_collector
from astrbot.api.message_components import Record


class StandaloneRouting(unittest.TestCase):
    def plugin(self, standalone=True):
        plugin = main.BioCorePlugin(route_collector() if standalone else harness.FakeContext(),
                                    config={'kb_enabled': True, 'kb_names': ['made-up']})
        test_basics.PLUGINS.append(plugin)
        if standalone:
            plugin._neutral_model = object()
        return plugin

    def browse_setup(self, plugin):
        ledger = Mock()
        ledger.money_left.return_value = True
        plugin._browse_ledger = lambda: ledger
        plugin._browse_names = lambda: []
        plugin._key_store = {'deepseek': 'made-up-deepseek'}

    def test_search_and_read_use_deepseek_without_network(self):
        plugin = self.plugin()
        self.browse_setup(plugin)
        event = harness.FakeEvent('hello')
        url = 'https://example.invalid/'
        calls = []

        async def post(tools, endpoint, payload, failure):
            calls.append((tools._api_key, endpoint, payload))
            if endpoint == deepseek_tools.SEARCH_URL:
                return {'results': [{'title': 'Made up', 'url': url, 'summary': 'Snippet'}]}
            return {'title': 'Made up', 'content': 'Page text'}

        with patch.object(deepseek_tools.DeepSeekTools, '_post', post), \
                patch.object(mixin_browse.browse, 'check_url', return_value=(True, '')):
            result = asyncio.run(plugin._tool_search(event, query='编的'))
            self.assertIn('Snippet', result)
            self.assertEqual(calls, [('made-up-deepseek', deepseek_tools.SEARCH_URL,
                                      {'query': '编的', 'count': 5, 'need_content': False})])
            result = asyncio.run(plugin._tool_read(event, url=url))
            self.assertIn('Page text', result)
            self.assertEqual(calls[1], ('made-up-deepseek', deepseek_tools.FETCH_URL, {'url': url}))
            plugin._key_store = {}
            self.assertEqual(asyncio.run(plugin._tool_search(harness.FakeEvent('hello'), query='编的')), '现在搜不了。')
            missing = harness.FakeEvent('hello')
            plugin._browse_urls(missing).add(url)
            self.assertEqual(asyncio.run(plugin._tool_read(missing, url=url)), '现在读不了。')
            self.assertEqual(len(calls), 2)

    def test_standalone_prepare_skips_knowledge_base(self):
        plugin = self.plugin()
        with patch.object(mixin_turn.logger, 'warning') as warning:
            asyncio.run(plugin._prepare_turn(harness.FakeEvent('hello'), turn.TurnRequest(prompt='hello')))
        self.assertFalse(any('kb retrieve failed' in str(call) for call in warning.call_args_list))

    def test_standalone_voice_uses_qq_and_kb_list_is_empty(self):
        plugin = self.plugin()
        messenger = types.SimpleNamespace(call=AsyncMock(return_value={'text': 'made-up words'}))
        plugin._messenger = lambda event: messenger
        event = harness.FakeEvent('hello')
        event.get_messages = lambda: [Record(file='made-up-voice')]
        with patch.object(mixin_media.logger, 'warning') as voice_warning, \
                patch.object(mixin_pages.logger, 'warning') as kb_warning:
            self.assertEqual(asyncio.run(plugin._voice_context(event)), 'made-up words')
            self.assertEqual(asyncio.run(plugin._kb_available()), [])
        messenger.call.assert_awaited_once_with('fetch_ptt_text', message_id=event.message_obj.message_id)
        self.assertFalse(any('voice context failed' in str(c) for c in voice_warning.call_args_list))
        self.assertFalse(any('kb list failed' in str(c) for c in kb_warning.call_args_list))

    def test_astrbot_still_uses_its_tools_and_context(self):
        plugin = self.plugin(False)
        self.browse_setup(plugin)
        event = harness.FakeEvent('hello')
        tool = types.SimpleNamespace(call=AsyncMock(return_value='{"results": [{"title": "Made up", "url": "https://example.invalid/", "snippet": "AstrBot"}]}'))
        manager = types.SimpleNamespace(get_builtin_tool=Mock(return_value=tool))
        plugin.context.get_llm_tool_manager = Mock(return_value=manager)
        web = types.ModuleType('astrbot.core.tools.web_search_tools')
        web.DeepSeekWebSearchTool = type('Search', (), {})
        web.DeepSeekFetchWebPageTool = type('Fetch', (), {})
        with patch.dict(sys.modules, {'astrbot.core.tools.web_search_tools': web}):
            self.assertIn('AstrBot', asyncio.run(plugin._tool_search(event, query='编的')))
        manager.get_builtin_tool.assert_called_once_with(web.DeepSeekWebSearchTool)
        tool.call.assert_awaited_once()

        kb = types.SimpleNamespace(retrieve=AsyncMock(return_value={'context_text': 'made-up kb'}),
                                   list_kbs=AsyncMock(return_value=[]))
        plugin.context.kb_manager = kb
        plugin.context.get_using_stt_provider_async = AsyncMock(return_value=None)
        asyncio.run(plugin._prepare_turn(event, turn.TurnRequest(prompt='hello')))
        kb.retrieve.assert_awaited_once()
        asyncio.run(plugin._voice_context(event))
        self.assertGreaterEqual(plugin.context.get_using_stt_provider_async.await_count, 1)
        self.assertEqual(asyncio.run(plugin._kb_available()), [])
        kb.list_kbs.assert_awaited_once()
