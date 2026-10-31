# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for the neutral turn and its AstrBot adapter."""
import ast
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for path in (str(ROOT), str(ROOT / 'tests' / 'stubs')):
    if path not in sys.path:
        sys.path.insert(0, path)

from astrbot.api.provider import ProviderRequest, LLMResponse
from astrbot.api.event import MessageChain
from astrbot.api.message_components import Reply, Plain, At
import adapter_astrbot_turn as adapter
import browse
import events
import model_client
import turn


class FakeTools:
    names = ('astrbot.core', 'astrbot.core.agent', 'astrbot.core.agent.tool')

    def __enter__(self):
        self.saved = {name: sys.modules.get(name) for name in self.names}
        class FunctionTool:
            def __init__(self, name='', description='', parameters=None, handler=None):
                self.name, self.description = name, description
                self.parameters, self.handler = parameters, handler
        class ToolSet:
            def __init__(self, tools=()):
                self.tools = list(tools)
            def names(self):
                return [tool.name for tool in self.tools]
            def remove_tool(self, name):
                self.tools = [tool for tool in self.tools if tool.name != name]
            def add_tool(self, tool):
                self.tools.append(tool)
        for name in self.names:
            sys.modules[name] = types.ModuleType(name)
        self.module = sys.modules[self.names[-1]]
        self.module.FunctionTool, self.module.ToolSet = FunctionTool, ToolSet
        return self.module

    def __exit__(self, *args):
        for name, module in self.saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


class TurnTests(unittest.TestCase):
    def test_tool_operations(self):
        a, b, replacement = (turn.TurnTool('a', '', {}), turn.TurnTool('b', '', {}),
                             turn.TurnTool('a', 'new', {}))
        request = turn.TurnRequest(tools=[a, b])
        request.add_tool(replacement)
        request.add_tool(turn.TurnTool('c', '', {}))
        self.assertEqual(request.tool_names(), ['a', 'b', 'c'])
        self.assertIs(request.tools[0], replacement)
        request.remove_tool('b')
        request.remove_tool('missing')
        self.assertEqual(request.tool_names(), ['a', 'c'])

    def test_round_trip_preserves_fields_and_tool_identity(self):
        with FakeTools() as fake:
            tools = [fake.FunctionTool('a', 'A', {'x': 1}, object()),
                     fake.FunctionTool('b', 'B', {}, object())]
            req = ProviderRequest('hello', 'system', [{'role': 'user'}])
            req.image_urls = ['image']
            req.extra_user_content_parts = [{'type': 'text', 'text': 'extra', '_no_save': True}]
            req.func_tool = fake.ToolSet(tools)
            original = (req.prompt, req.system_prompt, list(req.contexts), list(req.image_urls),
                        list(req.extra_user_content_parts))
            converted = adapter.request_from_astrbot(req)
            adapter.request_into_astrbot(converted, req)
            self.assertEqual((req.prompt, req.system_prompt, req.contexts, req.image_urls,
                              req.extra_user_content_parts), original)
            self.assertEqual(req.func_tool.names(), ['a', 'b'])
            for actual, expected in zip(req.func_tool.tools, tools):
                self.assertIs(actual, expected)

    def test_empty_and_removed_tools(self):
        with FakeTools() as fake:
            req = ProviderRequest()
            adapter.request_into_astrbot(adapter.request_from_astrbot(req), req)
            self.assertFalse(hasattr(req, 'func_tool'))
            req.func_tool = fake.ToolSet([fake.FunctionTool('a')])
            converted = adapter.request_from_astrbot(req)
            converted.remove_tool('a')
            adapter.request_into_astrbot(converted, req)
            self.assertIsNone(req.func_tool)

    def test_new_tool(self):
        with FakeTools() as fake:
            req = ProviderRequest()
            native = fake.FunctionTool('existing', 'Existing', {}, None)
            req.func_tool = fake.ToolSet([native])
            handler = object()
            item = turn.TurnTool('new', 'description', {'type': 'object'}, handler)
            converted = adapter.request_from_astrbot(req)
            converted.add_tool(item)
            adapter.request_into_astrbot(converted, req)
            self.assertEqual(req.func_tool.names(), ['existing', 'new'])
            self.assertIs(req.func_tool.tools[0], native)
            built = req.func_tool.tools[1]
            self.assertIsInstance(built, fake.FunctionTool)
            self.assertEqual((built.name, built.description, built.parameters),
                             (item.name, item.description, item.parameters))
            self.assertIs(built.handler, handler)

    def test_lists_are_shallow_copies(self):
        req = ProviderRequest(contexts=[{'role': 'user'}])
        req.image_urls = ['image']
        req.extra_user_content_parts = [{'text': 'extra'}]
        converted = adapter.request_from_astrbot(req)
        for name in ('contexts', 'image_urls', 'extra_user_content_parts'):
            self.assertIsNot(getattr(converted, name), getattr(req, name))
            self.assertIs(getattr(converted, name)[0], getattr(req, name)[0])
        converted.contexts.append({'role': 'assistant'})
        self.assertEqual(len(req.contexts), 1)
        adapter.request_into_astrbot(converted, req)
        self.assertEqual(len(req.contexts), 2)

    def test_reply_words_and_all_prefix_components(self):
        self.assertEqual(adapter.reply_from_astrbot(LLMResponse('hello')).text, 'hello')
        chain = MessageChain([Reply(id='m1', sender_id='10001'), Plain('hello'),
                              At(qq='10003', name='Alex')])
        result = adapter.reply_from_astrbot(LLMResponse(result_chain=chain))
        self.assertEqual(result.chain_prefix, [events.Segment('reply', {'id': 'm1', 'sender_id': '10001',
                                                                       'chain': (), 'text': '', 'message_str': ''}),
                                               events.Segment('at', {'qq': '10003', 'name': 'Alex'})])

    def test_reply_tool_calls_usage_and_reasoning(self):
        resp = LLMResponse('hello')
        resp.tools_call_name = ['one', '', 'two']
        resp.tools_call_args = [{'x': 1}, {}, '{"y": 2}']
        resp.tools_call_ids = ['id1']
        resp.usage = {'input_other': 20, 'input_cached': 3, 'output': 4}
        resp.reasoning_content = 'reason'
        result = adapter.reply_from_astrbot(resp)
        self.assertEqual(result.tool_calls, (model_client.ToolCall('id1', 'one', {'x': 1}),
                                             model_client.ToolCall('call_2', 'two', {'y': 2})))
        self.assertEqual(result.usage, browse.usage_of(resp.usage))
        self.assertEqual(result.reasoning, 'reason')
        self.assertNotIn(resp, result.extras.values())

    def test_reply_into_preserves_non_text_components(self):
        quote, at = Reply(id='m1'), At(qq='10003')
        chain = MessageChain([quote, Plain('old'), at])
        resp = LLMResponse(result_chain=chain)
        adapter.reply_into_astrbot(turn.TurnReply(text='new'), resp)
        self.assertEqual(resp.completion_text, 'new')
        self.assertIn(quote, chain.chain)
        self.assertIn(at, chain.chain)
        plain = LLMResponse('old')
        adapter.reply_into_astrbot(turn.TurnReply(text='new'), plain)
        self.assertEqual(plain.completion_text, 'new')

    def test_missing_and_none_fields(self):
        for obj in (None, types.SimpleNamespace(), types.SimpleNamespace(
                prompt=None, system_prompt=None, contexts=None, image_urls=None,
                extra_user_content_parts=None, func_tool=None, completion_text=None,
                result_chain=None, tools_call_name=None, tools_call_args=None,
                tools_call_ids=None, usage=None, reasoning_content=None)):
            request = adapter.request_from_astrbot(obj)
            self.assertEqual((request.prompt, request.system_prompt, request.contexts,
                              request.image_urls, request.extra_user_content_parts, request.tools),
                             ('', '', [], [], None, []))
            reply = adapter.reply_from_astrbot(obj)
            self.assertEqual((reply.text, reply.chain_prefix, reply.tool_calls, reply.reasoning),
                             ('', [], (), ''))
            self.assertEqual(reply.usage, browse.usage_of(None))

    def test_turn_does_not_import_astrbot(self):
        tree = ast.parse((ROOT / 'turn.py').read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(alias.name.startswith('astrbot') for alias in node.names))
            if isinstance(node, ast.ImportFrom):
                self.assertFalse((node.module or '').startswith('astrbot'))

