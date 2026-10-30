# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The one model client: how a chat is asked for (adapter_astrbot_model.py) and what comes
back (model_client.py).

A fake provider records the arguments every text_chat receives and gives back a reply built
here; no network, no service, nothing real. All tools, names, ids, usage numbers and replies
are made up.
"""
import asyncio
import json
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import adapter_astrbot_model  # noqa: E402
import browse  # noqa: E402
import model_client  # noqa: E402


class FakeProvider:
    """A provider that records every text_chat and gives back one reply, or raises one error."""

    def __init__(self, reply=None, error=None):
        self.calls = []
        self.reply = reply if reply is not None else types.SimpleNamespace(completion_text='ok')
        self.error = error

    async def text_chat(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.reply


def tool(name='ams_web_search', description='Search the web', parameters=None):
    return model_client.Tool(name=name, description=description,
                             parameters={'type': 'object'} if parameters is None else parameters)


class FakeToolModule:
    """A fake astrbot.core.agent.tool in sys.modules for one test, taken away afterwards.

    The real stub folder (tests/stubs) is not changed.
    """

    NAMES = ('astrbot', 'astrbot.core', 'astrbot.core.agent', 'astrbot.core.agent.tool')

    def __init__(self):
        self.saved = {}
        self.function_tools = []
        self.toolsets = []
        self.module = None

    def __enter__(self):
        self.saved = {name: sys.modules.get(name) for name in self.NAMES}
        outer = self

        class FunctionTool:
            def __init__(self, name='', description='', parameters=None, handler=None):
                self.name, self.description = name, description
                self.parameters, self.handler = parameters or {}, handler
                outer.function_tools.append(self)

        class ToolSet:
            def __init__(self, tools=()):
                self.tools = list(tools)
                outer.toolsets.append(self)

        self.module = types.ModuleType('astrbot.core.agent.tool')
        self.module.FunctionTool, self.module.ToolSet = FunctionTool, ToolSet
        parents = {}
        for name in ('astrbot', 'astrbot.core', 'astrbot.core.agent'):
            parents[name] = sys.modules[name] = types.ModuleType(name)
        parents['astrbot'].core = parents['astrbot.core']
        parents['astrbot.core'].agent = parents['astrbot.core.agent']
        parents['astrbot.core.agent'].tool = self.module
        sys.modules['astrbot.core.agent.tool'] = self.module
        return self

    def __exit__(self, *exc):
        for name, module in self.saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module
        return False


class CallShape(unittest.TestCase):
    """The call text_chat receives is exactly today's call: one key more or less fails."""

    def ask(self, toolset_of=None, **kwargs):
        provider = FakeProvider()
        model = adapter_astrbot_model.AstrBotModel(provider, toolset_of=toolset_of)
        asyncio.run(model.chat(**kwargs))
        self.assertEqual(len(provider.calls), 1)
        return provider.calls[0]

    def test_only_a_prompt(self):
        self.assertEqual(self.ask(prompt='hello'), {'prompt': 'hello'})

    def test_a_system_prompt(self):
        self.assertEqual(self.ask(prompt='hello', system='be brief'),
                         {'prompt': 'hello', 'system_prompt': 'be brief'})

    def test_images(self):
        images = ['ref']
        sent = self.ask(prompt='what is this', images=images)
        self.assertEqual(sent, {'prompt': 'what is this', 'image_urls': ['ref']})
        self.assertIsNot(sent['image_urls'], images)

    def test_messages_and_tools_and_system(self):
        contexts = [{'role': 'user', 'content': 'go out'}]
        one = tool()
        sentinel = object()
        seen = []

        def toolset_of(tools):
            seen.append(list(tools))
            return sentinel

        sent = self.ask(toolset_of=toolset_of, messages=contexts, tools=[one], system='persona')
        self.assertEqual(sent, {'contexts': contexts, 'func_tool': sentinel,
                                'system_prompt': 'persona'})
        self.assertIsNot(sent['contexts'], contexts)
        self.assertEqual(seen, [[one]])

    def test_empty_tools_and_no_system_are_not_sent(self):
        self.assertEqual(self.ask(prompt='hello', tools=[], system=None), {'prompt': 'hello'})

    def test_empty_strings_are_given(self):
        self.assertEqual(self.ask(prompt='', system=''), {'prompt': '', 'system_prompt': ''})

    def test_empty_messages_and_images_are_given(self):
        sent = self.ask(messages=[], images=[])
        self.assertEqual(sent, {'contexts': [], 'image_urls': []})


class ToolsetOf(unittest.TestCase):
    def test_the_tools_reach_toolset_of_in_order(self):
        first, second = tool('one', 'First'), tool('two', 'Second')
        seen = []

        def toolset_of(tools):
            seen.append(list(tools))
            return 'fake toolset'

        provider = FakeProvider()
        model = adapter_astrbot_model.AstrBotModel(provider, toolset_of=toolset_of)
        asyncio.run(model.chat(messages=[{'role': 'user', 'content': 'x'}], tools=[first, second]))
        self.assertEqual(seen, [[first, second]])
        self.assertIs(seen[0][0], first)
        self.assertIs(seen[0][1], second)
        self.assertEqual(provider.calls[0]['func_tool'], 'fake toolset')

    def test_the_default_makes_function_tools_whose_handler_never_runs(self):
        one = tool('ams_web_search', 'Search the web', {'type': 'object', 'properties': {}})
        with FakeToolModule() as fake:
            provider = FakeProvider()
            model = adapter_astrbot_model.AstrBotModel(provider)
            asyncio.run(model.chat(messages=[{'role': 'user', 'content': 'x'}], tools=[one]))
            self.assertIs(provider.calls[0]['func_tool'], fake.toolsets[0])
            built = fake.toolsets[0].tools
            self.assertEqual(len(built), 1)
            self.assertEqual(built[0].name, 'ams_web_search')
            self.assertEqual(built[0].description, 'Search the web')
            self.assertEqual(built[0].parameters, one.parameters)
            with self.assertRaises(RuntimeError):
                built[0].handler()
        # The fake module is gone again; the real stub folder was never touched.
        self.assertIsNot(sys.modules.get('astrbot.core.agent.tool'), fake.module)


class Arguments(unittest.TestCase):
    def test_a_dict_comes_back_as_is(self):
        value = {'action': 'press'}
        self.assertIs(model_client.arguments_of(value), value)

    def test_a_json_object_string_is_parsed(self):
        self.assertEqual(model_client.arguments_of('{"query": "news", "n": 2}'), {'query': 'news', 'n': 2})

    def test_anything_else_is_empty(self):
        for raw in ('', 'not json', '{"a": 1}}', '[]', '[1, 2]', '3', 'null', 'true', 3, None,
                    ['a'], ('a',), True):
            self.assertEqual(model_client.arguments_of(raw), {}, repr(raw))


class Replies(unittest.TestCase):
    def reply(self, **fields):
        provider = FakeProvider(types.SimpleNamespace(**fields))
        return asyncio.run(adapter_astrbot_model.AstrBotModel(provider).chat(prompt='x'))

    def test_words_only(self):
        reply = self.reply(completion_text='hello')
        self.assertEqual(reply.text, 'hello')
        self.assertEqual(reply.tool_calls, ())
        self.assertEqual(reply.reasoning, '')

    def test_two_tool_calls_in_order(self):
        reply = self.reply(completion_text='', tools_call_name=['one', 'two'],
                           tools_call_args=[{'a': 1}, json.dumps({'b': 2})],
                           tools_call_ids=['x', 'y'])
        self.assertEqual(reply.text, '')
        self.assertIsInstance(reply.tool_calls, tuple)
        self.assertEqual([call.name for call in reply.tool_calls], ['one', 'two'])
        self.assertEqual([call.id for call in reply.tool_calls], ['x', 'y'])
        self.assertEqual(reply.tool_calls[0].arguments, {'a': 1})
        self.assertEqual(reply.tool_calls[1].arguments, {'b': 2})
        self.assertIsInstance(reply.tool_calls[0], model_client.ToolCall)

    def test_unreadable_arguments_are_empty(self):
        for raw in ('not json', '[]', '[1, 2]', '3', 3, None, ['a'], True):
            reply = self.reply(tools_call_name=['one'], tools_call_args=[raw], tools_call_ids=['x'])
            self.assertEqual(reply.tool_calls[0].arguments, {}, repr(raw))

    def test_missing_ids_and_arguments(self):
        reply = self.reply(tools_call_name=['one', 'two'], tools_call_args=[{}])
        self.assertEqual([call.id for call in reply.tool_calls], ['call_0', 'call_1'])
        self.assertEqual([call.arguments for call in reply.tool_calls], [{}, {}])

    def test_an_empty_name_is_skipped(self):
        reply = self.reply(tools_call_name=['', 'two'], tools_call_args=[{}, {}],
                           tools_call_ids=['a', 'b'])
        self.assertEqual(len(reply.tool_calls), 1)
        self.assertEqual(reply.tool_calls[0].name, 'two')
        self.assertEqual(reply.tool_calls[0].id, 'b')

    def test_usage_both_shapes_match_browse(self):
        astrbot_usage = {'input_other': 1200, 'input_cached': 300, 'output': 450}
        openai_usage = {'prompt_tokens': 1500, 'completion_tokens': 450,
                        'prompt_cache_hit_tokens': 300}
        for usage in (astrbot_usage, openai_usage):
            reply = self.reply(completion_text='ok', usage=usage)
            self.assertEqual(reply.usage, browse.usage_of(usage))
            self.assertEqual(reply.usage, {'input_miss': 1200, 'input_hit': 300, 'output': 450})

    def test_no_usage_is_three_zeros(self):
        self.assertEqual(self.reply(completion_text='ok').usage,
                         {'input_miss': 0, 'input_hit': 0, 'output': 0})

    def test_reasoning_is_carried_when_there_is_one(self):
        self.assertEqual(self.reply(completion_text='ok', reasoning_content='because').reasoning,
                         'because')
        self.assertEqual(self.reply(completion_text='ok', reasoning_content=None).reasoning, '')
        self.assertEqual(self.reply(completion_text='ok').reasoning, '')

    def test_unreadable_fields_give_empty_values(self):
        provider = FakeProvider(types.SimpleNamespace())
        reply = asyncio.run(adapter_astrbot_model.AstrBotModel(provider).chat())
        self.assertEqual(reply.text, '')
        self.assertEqual(reply.tool_calls, ())
        self.assertEqual(reply.usage, {'input_miss': 0, 'input_hit': 0, 'output': 0})
        self.assertEqual(reply.reasoning, '')


class Errors(unittest.TestCase):
    def test_a_provider_error_passes_through(self):
        for error in (asyncio.TimeoutError(), RuntimeError('no model')):
            provider = FakeProvider(error=error)
            with self.assertRaises(type(error)) as caught:
                asyncio.run(adapter_astrbot_model.AstrBotModel(provider).chat(prompt='x'))
            self.assertIs(caught.exception, error)


class TheInterface(unittest.TestCase):
    def test_the_base_chat_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            asyncio.run(model_client.ModelClient().chat(prompt='x'))

    def test_the_interface_mentions_no_astrbot(self):
        source = (ROOT / 'model_client.py').read_text(encoding='utf-8')
        self.assertNotIn('astrbot', source.lower())


if __name__ == '__main__':
    unittest.main()
