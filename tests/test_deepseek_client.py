# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for the DeepSeek model client."""
import ast
import asyncio
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

import deepseek_client
import model_client
import tool_loop


def response(content='ok', calls=None, usage=None, **extra):
    return NS(choices=[NS(message=NS(content=content, tool_calls=calls, **extra))], usage=usage)


def call(name, arguments, id=None):
    return NS(id=id, function=NS(name=name, arguments=arguments))


class FakeClient:
    def __init__(self, replies=(), error=None):
        self.chat = NS(completions=self)
        self.replies = list(replies) or [response()]
        self.error = error
        self.calls = []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.replies.pop(0)


def make(fake=None, **kwargs):
    return deepseek_client.DeepSeekModel(api_key='fake-key', model='fake-model',
                                         client=fake or FakeClient(), **kwargs)


class DeepSeekTests(unittest.TestCase):
    def test_construction_and_key_safety(self):
        with self.assertRaisesRegex(ValueError, '^no key$'):
            deepseek_client.DeepSeekModel(api_key='', model='m', client=FakeClient())
        for url in ('https://example.test', 'https://api.deepseek.com.evil.test',
                    'https://api.deepseek.com@evil.test'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                make(base_url=url)
        self.assertNotIn('fake-key', repr(make()))
        self.assertIn('fake-model', repr(make()))

    def test_messages_and_none_semantics(self):
        for kwargs, expected in [
            ({'prompt': 'hi'}, [{'role': 'user', 'content': 'hi'}]),
            ({'system': 'rules', 'prompt': 'hi'}, [{'role': 'system', 'content': 'rules'},
                                                     {'role': 'user', 'content': 'hi'}]),
            ({'system': '', 'prompt': ''}, [{'role': 'system', 'content': ''},
                                             {'role': 'user', 'content': ''}]),
            ({'system': None}, [])]:
            fake = FakeClient()
            asyncio.run(make(fake).chat(**kwargs))
            self.assertEqual(fake.calls[0]['messages'], expected)
        messages = [{'role': 'assistant', 'content': '', 'reasoning_content': 'think'}]
        fake = FakeClient()
        asyncio.run(make(fake).chat(system='rules', messages=messages, prompt='next'))
        self.assertEqual(messages, [{'role': 'assistant', 'content': '', 'reasoning_content': 'think'}])
        self.assertEqual(fake.calls[0]['messages'], [{'role': 'system', 'content': 'rules'},
                          *messages, {'role': 'user', 'content': 'next'}])

    def test_images_and_tools(self):
        fake = FakeClient()
        with self.assertRaisesRegex(ValueError, '^DeepSeek chat does not take images$'):
            asyncio.run(make(fake).chat(images=['x']))
        self.assertEqual(fake.calls, [])
        tools = [model_client.Tool('one', 'first', {'type': 'object'}),
                 model_client.Tool('two', 'second', {'type': 'object'})]
        asyncio.run(make(fake).chat(images=[], tools=tools))
        self.assertEqual(fake.calls[0]['tools'], [
            {'type': 'function', 'function': {'name': t.name, 'description': t.description,
                                               'parameters': t.parameters}} for t in tools])
        fake = FakeClient()
        asyncio.run(make(fake).chat(tools=[]))
        self.assertNotIn('tools', fake.calls[0])

    def test_reply_calls_reasoning_and_usage(self):
        usage = NS(prompt_tokens=100, completion_tokens=7, prompt_cache_hit_tokens=40,
                   prompt_cache_miss_tokens=60)
        calls = [call('one', '{"x": 1}', 'id1'), call('two', 'bad'),
                 call('three', {'x': 2}), call('', '{}')]
        reply = asyncio.run(make(FakeClient([response('words', calls, usage,
                                                       reasoning_content='thinking')])).chat())
        self.assertEqual(reply.text, 'words')
        self.assertEqual(reply.tool_calls, (model_client.ToolCall('id1', 'one', {'x': 1}),
                                            model_client.ToolCall('call_1', 'two', {}),
                                            model_client.ToolCall('call_2', 'three', {'x': 2})))
        self.assertEqual(reply.reasoning, 'thinking')
        self.assertEqual(reply.usage, {'input_miss': 60, 'input_hit': 40, 'output': 7})
        extra = response(model_extra={'reasoning_content': 'extra'})
        self.assertEqual(asyncio.run(make(FakeClient([extra])).chat()).reasoning, 'extra')
        dumped = NS(model_dump=lambda: {'prompt_tokens': 9, 'completion_tokens': 2,
                                       'prompt_cache_hit_tokens': 3, 'prompt_cache_miss_tokens': 6})
        self.assertEqual(asyncio.run(make(FakeClient([response(usage=dumped)])).chat()).usage,
                         {'input_miss': 6, 'input_hit': 3, 'output': 2})

    def test_missing_response_fields(self):
        reply = asyncio.run(make(FakeClient([NS(choices=[])] )).chat())
        self.assertEqual((reply.text, reply.tool_calls, reply.reasoning), ('', (), ''))
        self.assertEqual(reply.usage, {'input_miss': 0, 'input_hit': 0, 'output': 0})
        self.assertEqual(asyncio.run(make(FakeClient([response()])).chat()).text, 'ok')

    def test_error_passes_through(self):
        error = RuntimeError('fake error')
        with self.assertRaises(RuntimeError) as caught:
            asyncio.run(make(FakeClient(error=error)).chat())
        self.assertIs(caught.exception, error)

    def test_tool_loop_preserves_reasoning_and_calls(self):
        fake = FakeClient([response(calls=[call('one', '{"q": "x"}', 'id1')],
                                    reasoning_content='thinking'), response('done')])
        tool = model_client.Tool('one', 'first', {'type': 'object', 'properties': {'q': {}}})
        result = asyncio.run(tool_loop.run(make(fake), tools=[tool_loop.LoopTool(tool, lambda q: q)]))
        self.assertEqual(result.text, 'done')
        assistant, tool_message = fake.calls[1]['messages']
        self.assertEqual(assistant['reasoning_content'], 'thinking')
        self.assertEqual(assistant['tool_calls'][0]['id'], 'id1')
        self.assertEqual(tool_message, {'role': 'tool', 'tool_call_id': 'id1', 'content': 'x'})

    @unittest.skipUnless(importlib.util.find_spec('openai'), 'openai not installed')
    def test_real_sdk_construction(self):
        client = deepseek_client.DeepSeekModel(api_key='fake-key', model='fake-model')
        self.assertEqual(str(client._client.base_url).rstrip('/'), deepseek_client.BASE_URL)

    def test_source_imports(self):
        source = (Path(__file__).resolve().parent.parent / 'deepseek_client.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        for node in imports:
            self.assertNotIn('astrbot', ast.unparse(node).lower())
            self.assertNotIn('logging', ast.unparse(node).lower())
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self.assertNotIn('openai', ast.unparse(node).lower())


if __name__ == '__main__':
    unittest.main()
