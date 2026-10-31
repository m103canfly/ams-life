# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The two shared fakes, checked against the real modules they stand in for.

``FakeDeepSeek`` is given to 3b's ``DeepSeekModel`` and to 3a's ``tool_loop.run``;
``FakeNapCat`` connects to 2d's ``OneBotServer``, hands its events to 2a's ``from_onebot`` and
answers the messenger's calls. Everything is offline and made up: 20002 is her, 10001 and
900001 are a made-up person and group. The NapCat connection tests need aiohttp and skip
without it.
"""
import ast
import asyncio
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for path in (str(ROOT), str(HERE)):
    if path not in sys.path:
        sys.path.insert(0, path)

import model_client  # noqa: E402
import tool_loop  # noqa: E402
from adapter_onebot import from_onebot  # noqa: E402
from deepseek_client import DeepSeekModel  # noqa: E402
from events import Segment, plain_text  # noqa: E402
from fake_deepseek import FakeDeepSeek  # noqa: E402
from fake_napcat import FakeNapCat  # noqa: E402

try:
    import aiohttp
except ImportError:
    aiohttp = None

if aiohttp is not None:
    from adapter_onebot_messenger import ActionFailed  # noqa: E402
    from onebot_server import OneBotServer  # noqa: E402

TOKEN = 'fake-secret'
MADE_UP_USAGE = {'prompt_tokens': 100, 'completion_tokens': 7,
                 'prompt_cache_hit_tokens': 40, 'prompt_cache_miss_tokens': 60}


def a_model(fake):
    """3b's client over the given fake SDK client; the key and the model are made up."""
    return DeepSeekModel(api_key='fake-key', model='fake-model', client=fake)


def a_tool(name='one', properties=None, handler=None):
    """One loop tool with a made-up schema and the given handler."""
    return tool_loop.LoopTool(
        tool=model_client.Tool(name=name, description=name + ' tool',
                               parameters={'type': 'object', 'properties': dict(properties or {})}),
        handler=handler if handler is not None else Handler())


class Handler:
    """A tool handler that keeps the arguments it got and answers with fixed words."""

    def __init__(self, result='ok'):
        self.result = result
        self.got = []

    async def __call__(self, **arguments):
        self.got.append(arguments)
        return self.result


class DeepSeekReply(unittest.TestCase):
    """1. Words, reasoning and usage; then two tool calls, as 3b's DeepSeekModel reads them."""

    def test_words_reasoning_and_usage(self):
        fake = FakeDeepSeek()
        fake.say('你好呀', reasoning='先想一想', usage=MADE_UP_USAGE)
        reply = asyncio.run(a_model(fake).chat(prompt='在吗'))
        self.assertEqual(reply.text, '你好呀')
        self.assertEqual(reply.tool_calls, ())
        self.assertEqual(reply.reasoning, '先想一想')
        self.assertEqual(reply.usage, {'input_miss': 60, 'input_hit': 40, 'output': 7})
        self.assertEqual(fake.requests[0]['messages'], [{'role': 'user', 'content': '在吗'}])
        # the SDK keeps a field it does not know in model_extra, which is where 3b looks
        message = fake.responses[0].choices[0].message
        self.assertEqual(message.model_extra, {'reasoning_content': '先想一想'})
        self.assertEqual(fake.responses[0].usage.model_dump(), MADE_UP_USAGE)

    def test_two_tool_calls(self):
        fake = FakeDeepSeek()
        fake.call_tools(('one', {'q': '天气'}), ('two', {}))
        reply = asyncio.run(a_model(fake).chat(tools=[
            model_client.Tool('one', 'first', {'type': 'object'}),
            model_client.Tool('two', 'second', {'type': 'object'})]))
        self.assertEqual(reply.text, '')
        self.assertEqual(reply.tool_calls, (
            model_client.ToolCall('call_1', 'one', {'q': '天气'}),
            model_client.ToolCall('call_2', 'two', {})))
        self.assertEqual({tool['function']['name'] for tool in fake.requests[0]['tools']},
                         {'one', 'two'})
        functions = [call.function for call in fake.responses[0].choices[0].message.tool_calls]
        self.assertEqual([json.loads(function.arguments) for function in functions],
                         [{'q': '天气'}, {}])


class DeepSeekToolLoop(unittest.TestCase):
    """2. A tool round then words; the second request carries the thinking and the result."""

    def test_a_tool_round_then_words(self):
        seen = Handler(result='晴，三十度')
        fake = FakeDeepSeek()
        fake.call_tools(('one', {'q': '天气'}), reasoning='先想一想')
        fake.say('今天很热')
        result = asyncio.run(tool_loop.run(
            a_model(fake), messages=[{'role': 'user', 'content': '去'}],
            tools=[a_tool('one', {'q': {}}, seen)]))
        self.assertEqual(result.text, '今天很热')
        self.assertEqual(result.reason, 'done')
        self.assertEqual(seen.got, [{'q': '天气'}])
        sent = fake.requests[1]['messages']
        self.assertEqual([message['role'] for message in sent], ['user', 'assistant', 'tool'])
        assistant = sent[1]
        self.assertEqual(assistant['reasoning_content'], '先想一想')
        self.assertEqual(assistant['tool_calls'], [
            {'id': 'call_1', 'type': 'function',
             'function': {'name': 'one',
                          'arguments': json.dumps({'q': '天气'}, ensure_ascii=False)}}])
        self.assertEqual(sent[2], {'role': 'tool', 'tool_call_id': 'call_1', 'content': '晴，三十度'})

    def test_one_call_more_than_scripted(self):
        fake = FakeDeepSeek()
        fake.call_tools(('one', {'q': 'x'}))   # no words scripted after the tool round
        with self.assertRaisesRegex(AssertionError, 'no scripted reply'):
            asyncio.run(tool_loop.run(a_model(fake), tools=[a_tool('one', {'q': {}}, Handler())]))
        self.assertEqual(len(fake.requests), 2)


@unittest.skipUnless(aiohttp is not None, 'aiohttp is not installed')
class NapCatOverTheServer(unittest.IsolatedAsyncioTestCase):
    """3. The fake client and 2d's server, over a real loopback socket and an OS-chosen port."""

    async def asyncSetUp(self):
        self.events = []
        self.arrived = asyncio.Event()

        async def on_event(frame):
            self.events.append(frame)
            self.arrived.set()

        self.server = OneBotServer(token=TOKEN, on_event=on_event, port=0, call_seconds=1)
        self.port = await self.server.start()
        self.addAsyncCleanup(self.server.stop)
        self.napcat = FakeNapCat(url='ws://127.0.0.1:%d/ws' % self.port, token=TOKEN)
        await self.napcat.__aenter__()
        self.addAsyncCleanup(self.napcat.__aexit__, None, None, None)
        await self.wait_connected()

    async def wait_connected(self, seconds=2):
        """Wait until the server has this connection; its name and role are already checked."""
        for _ in range(int(seconds * 1000)):
            if self.server.connected:
                return
            await asyncio.sleep(0.001)
        self.fail('the fake NapCat did not finish the handshake')

    async def test_handshake(self):
        self.assertTrue(self.server.connected)
        self.assertEqual(self.server.self_id, '20002')

    async def test_an_event_arrives_as_an_incoming(self):
        event = self.napcat.group_message(group=900001, user=10001, text='你好呀', at_me=True,
                                          name='柠檬')
        await asyncio.wait_for(self.napcat.send_event(event), 2)
        await asyncio.wait_for(self.arrived.wait(), 2)
        self.assertEqual(self.events, [event])
        incoming = from_onebot(self.events[0])
        self.assertEqual(incoming.place, 'group:900001')
        self.assertTrue(incoming.at_me)
        self.assertEqual(plain_text(incoming), '你好呀')
        self.assertEqual(incoming.sender_id, '10001')
        self.assertEqual(incoming.sender_name, '柠檬')

    async def test_a_message_she_sends(self):
        messenger = self.server.messenger(())
        sent = await asyncio.wait_for(
            messenger.send('group:900001', (Segment('text', {'text': '我来了'}),)), 2)
        self.assertTrue(sent.ok)
        self.assertEqual(sent.message_id, '1')
        self.assertEqual(len(self.napcat.sent), 1)
        self.assertEqual(self.napcat.sent[0]['group_id'], 900001)
        self.assertIsInstance(self.napcat.sent[0]['group_id'], int)
        self.assertEqual(self.napcat.sent[0]['message'],
                         [{'type': 'text', 'data': {'text': '我来了'}}])
        self.assertEqual(self.napcat.calls[-1][0], 'send_group_msg')

    async def test_get_msg_finds_what_it_sent_out(self):
        event = self.napcat.group_message(group=900001, user=10001, text='上一句')
        await asyncio.wait_for(self.napcat.send_event(event), 2)
        await asyncio.wait_for(self.arrived.wait(), 2)
        found = await asyncio.wait_for(
            self.server.call_api('get_msg', {'message_id': event['message_id']}), 2)
        self.assertEqual(found['status'], 'ok')
        self.assertEqual(found['data']['message_id'], event['message_id'])
        self.assertEqual(found['data']['user_id'], 10001)
        sent = await asyncio.wait_for(
            self.server.messenger(()).send('group:900001', (Segment('text', {'text': '嗯'}),)), 2)
        found = await asyncio.wait_for(
            self.server.call_api('get_msg', {'message_id': sent.message_id}), 2)
        self.assertEqual(found['status'], 'ok')
        self.assertEqual(str(found['data']['message_id']), sent.message_id)
        missing = await asyncio.wait_for(
            self.server.call_api('get_msg', {'message_id': 700001}), 2)
        self.assertEqual(missing['status'], 'failed')

    async def test_a_scripted_failure_reaches_the_messenger(self):
        self.napcat.answer('get_forward_msg', status='failed', retcode=1401)
        messenger = self.server.messenger(())
        with self.assertRaises(ActionFailed) as caught:
            await asyncio.wait_for(messenger.call('get_forward_msg', id='fake-forward-1'), 2)
        self.assertEqual(caught.exception.retcode, 1401)
        self.assertEqual(self.napcat.calls[-1], ('get_forward_msg', {'id': 'fake-forward-1'}))


class NapCatLocalOnly(unittest.TestCase):
    """4. The fake client connects to this machine only; building one connects to nothing."""

    def test_a_non_local_url_is_refused(self):
        with self.assertRaises(ValueError):
            FakeNapCat(url='ws://192.168.1.5:6199/ws', token=TOKEN)

    def test_a_local_url_is_accepted(self):
        napcat = FakeNapCat(url='ws://127.0.0.1:6199/ws', token=TOKEN)
        self.assertEqual(napcat.self_id, '20002')
        self.assertEqual((napcat.sent, napcat.calls), ([], []))


class FakeMessages(unittest.TestCase):
    """The array-format messages the fake builds, as 2a's from_onebot reads them (no socket)."""

    def test_a_group_message(self):
        napcat = FakeNapCat(url='ws://127.0.0.1:6199/ws', token=TOKEN)
        event = napcat.group_message(group=900001, user=10001, text='看这个', at_me=True,
                                     reply_to='910001', images=('https://example.test/a.png',),
                                     name='柠檬', card='')
        self.assertEqual(event['post_type'], 'message')
        self.assertEqual(event['message_type'], 'group')
        self.assertEqual(event['self_id'], 20002)
        self.assertEqual(event['user_id'], 10001)
        self.assertEqual(event['group_id'], 900001)
        self.assertEqual(event['sender'], {'user_id': 10001, 'nickname': '柠檬', 'card': ''})
        self.assertEqual([segment['type'] for segment in event['message']],
                         ['at', 'reply', 'text', 'image'])
        self.assertEqual(event['message'][0]['data'], {'qq': '20002'})
        self.assertEqual(event['message'][1]['data'], {'id': '910001'})
        self.assertEqual(event['message'][2]['data'], {'text': '看这个'})
        self.assertEqual(event['message'][3]['data'],
                         {'url': 'https://example.test/a.png', 'file': 'https://example.test/a.png'})
        second = napcat.group_message(group=900001, user=10001, text='再来')
        self.assertNotEqual(event['message_id'], second['message_id'])

    def test_a_private_message(self):
        napcat = FakeNapCat(url='ws://127.0.0.1:6199/ws', token=TOKEN)
        event = napcat.private_message(user=10001, text='悄悄话',
                                       images=('https://example.test/b.png',), name='柠檬')
        self.assertEqual(event['message_type'], 'private')
        self.assertNotIn('group_id', event)
        self.assertEqual([segment['type'] for segment in event['message']], ['text', 'image'])
        self.assertEqual(event['sender']['user_id'], 10001)
        incoming = from_onebot(event)
        self.assertEqual(incoming.place, 'private:10001')
        self.assertTrue(incoming.is_private)
        self.assertEqual(plain_text(incoming), '悄悄话')
        self.assertEqual(incoming.image_refs, ('https://example.test/b.png',))


class FakeSources(unittest.TestCase):
    """5. Neither fake imports AstrBot; the model fake needs no SDK and no network either."""

    def imports_of(self, name):
        """The import statements of one fake, each written out as its source line."""
        source = (HERE / name).read_text(encoding='utf-8')
        tree = ast.parse(source)
        return [ast.unparse(node).lower() for node in ast.walk(tree)
                if isinstance(node, (ast.Import, ast.ImportFrom))]

    def test_neither_fake_knows_astrbot(self):
        for name in ('fake_napcat.py', 'fake_deepseek.py'):
            with self.subTest(name=name):
                imports = self.imports_of(name)
                self.assertFalse(any('astrbot' in line for line in imports), imports)

    def test_the_model_fake_needs_no_sdk(self):
        imports = self.imports_of('fake_deepseek.py')
        for word in ('openai', 'aiohttp', 'socket', 'urllib'):
            self.assertFalse(any(word in line for line in imports), (word, imports))


if __name__ == '__main__':
    unittest.main()
