# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for preparing a neutral turn and writing it back."""
import ast
import asyncio
import sys
import types
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import harness

if __package__:
    from tests import test_basics
else:
    import test_basics
import main
import adapter_astrbot_turn as adapter
from test_turn import FakeTools
from astrbot.api.provider import ProviderRequest

class PrepareTurnTests(unittest.TestCase):
    def plugin(self, config=None):
        plugin = main.BioCorePlugin(harness.FakeContext(), config=config or {})
        test_basics.PLUGINS.append(plugin)
        return plugin

    def test_write_back_only_changes(self):
        req = types.SimpleNamespace(prompt=None, extra_user_content_parts=[])
        parts = req.extra_user_content_parts
        converted = adapter.request_from_astrbot(req)
        adapter.request_into_astrbot(converted, req)
        self.assertIsNone(req.prompt)
        self.assertFalse(hasattr(req, 'func_tool'))
        self.assertFalse(hasattr(req, 'image_urls'))
        converted.prompt = 'changed'
        converted.extra_user_content_parts.append({'text': 'block'})
        adapter.request_into_astrbot(converted, req)
        self.assertEqual(req.prompt, 'changed')
        self.assertIs(req.extra_user_content_parts, parts)
        self.assertEqual(parts, [{'text': 'block'}])
        req.extra_user_content_parts = None
        converted = adapter.request_from_astrbot(req)
        self.assertIsNone(converted.extra_user_content_parts)
        adapter.request_into_astrbot(converted, req)
        self.assertIsNone(req.extra_user_content_parts)
        with FakeTools() as fake:
            req.func_tool = fake.ToolSet()
            empty = req.func_tool
            adapter.request_into_astrbot(adapter.request_from_astrbot(req), req)
            self.assertIs(req.func_tool, empty)

    def test_hook_writes_back_and_retains_platform_request(self):
        plugin = self.plugin()
        event = harness.FakeEvent('hello', sender='10001', group='900001')
        req = ProviderRequest(prompt='hello')
        req.extra_user_content_parts = []
        parts = req.extra_user_content_parts
        async def prepare(event, request):
            request.prompt = 'changed'
            request.extra_user_content_parts.append({'text': 'block'})
            plugin._note_allowed(event, request, 'block')
        plugin._prepare_turn = prepare
        asyncio.run(plugin.on_llm_request(event, req))
        self.assertEqual(req.prompt, 'changed')
        self.assertIs(req.extra_user_content_parts, parts)
        self.assertEqual(parts, [{'text': 'block'}])
        self.assertIs(event._ams_check['req'], req)

    def test_hook_writes_back_on_error(self):
        plugin = self.plugin()
        event = harness.FakeEvent('hello')
        req = ProviderRequest(prompt='hello')
        async def prepare(event, request):
            request.prompt = 'changed'
            raise ValueError('failure')
        plugin._prepare_turn = prepare
        with self.assertRaises(ValueError):
            asyncio.run(plugin.on_llm_request(event, req))
        self.assertEqual(req.prompt, 'changed')

    def test_hook_skips_disabled_and_ignored(self):
        async def prepare(event, request):
            self.fail('prepare called')
        plugin = self.plugin({'enabled': False})
        plugin._prepare_turn = prepare
        asyncio.run(plugin.on_llm_request(harness.FakeEvent('hello'), ProviderRequest()))
        plugin = self.plugin()
        plugin._ignored_sender = lambda event: True
        plugin._prepare_turn = prepare
        event = harness.FakeEvent('hello')
        asyncio.run(plugin.on_llm_request(event, ProviderRequest()))
        self.assertTrue(event.stopped)

    def test_source_boundaries(self):
        tree = ast.parse((ROOT / 'mixin_turn.py').read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(a.name.startswith('astrbot') for a in node.names))
            if isinstance(node, ast.ImportFrom):
                self.assertFalse((node.module or '').startswith('astrbot'))
        tree = ast.parse((ROOT / 'main.py').read_text(encoding='utf-8'))
        plugin = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'BioCorePlugin')
        hook = next(n for n in plugin.body if isinstance(n, ast.AsyncFunctionDef) and n.name == 'on_llm_request')
        attrs = {n.attr for n in ast.walk(hook) if isinstance(n, ast.Attribute)
                 and isinstance(n.value, ast.Name) and n.value.id == 'req'}
        self.assertLessEqual(attrs, {'func_tool'})


if __name__ == '__main__':
    unittest.main()
