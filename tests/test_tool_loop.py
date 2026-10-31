# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The plain tool loop (tool_loop.py): what it asks the model, what it runs, when it stops.

A fake model client answers from a script and records every round's system, messages and tools.
Every name, id, number, usage number and line of text here is made up; nothing goes out.
"""
import asyncio
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import model_client  # noqa: E402
import tool_loop  # noqa: E402

ZERO = {"input_miss": 0, "input_hit": 0, "output": 0}


def reply(text="", calls=(), reasoning="", usage=None):
    """One answer from the fake model."""
    return model_client.ModelReply(text=text, tool_calls=tuple(calls), reasoning=reasoning,
                                   usage=dict(ZERO if usage is None else usage))


def call(name="one", arguments=None, id="call_1"):
    """One tool call the fake model asks for."""
    return model_client.ToolCall(id=id, name=name, arguments={} if arguments is None else arguments)


class FakeClient:
    """A model client answering from a script; it keeps every round's arguments."""

    def __init__(self, replies=(), error=None, slow=0):
        self.replies = list(replies)
        self.error = error
        self.slow = slow
        self.rounds = []       # {"system", "messages", "tools"} as each round received them

    async def chat(self, *, prompt=None, system=None, messages=None, images=None, tools=None):
        self.rounds.append({"system": system, "messages": messages, "tools": tools})
        if self.slow:
            await asyncio.sleep(self.slow)
        if self.error is not None:
            raise self.error
        return self.replies.pop(0) if self.replies else reply(text="")


class Handler:
    """A tool handler that keeps the arguments it got, and answers or raises."""

    def __init__(self, result="ok", error=None):
        self.result = result
        self.error = error
        self.got = []

    async def __call__(self, **arguments):
        self.got.append(arguments)
        if self.error is not None:
            raise self.error
        return self.result


def a_tool(name="one", properties=None, handler=None):
    """A loop tool with a made-up schema and the given handler."""
    return tool_loop.LoopTool(
        tool=model_client.Tool(name=name, description=name + " tool",
                               parameters={"type": "object", "properties": dict(properties or {})}),
        handler=handler if handler is not None else Handler())


class SmallRepeat:
    """REPEAT_WARN and REPEAT_STOP made small for one test, put back afterwards."""

    def __init__(self, warn, stop):
        self.warn, self.stop, self.saved = warn, stop, None

    def __enter__(self):
        self.saved = (tool_loop.REPEAT_WARN, tool_loop.REPEAT_STOP)
        tool_loop.REPEAT_WARN, tool_loop.REPEAT_STOP = self.warn, self.stop
        return self

    def __exit__(self, *exc):
        tool_loop.REPEAT_WARN, tool_loop.REPEAT_STOP = self.saved
        return False


def go(client, **kwargs):
    return asyncio.run(tool_loop.run(client, **kwargs))


def tools_of(messages):
    return [message for message in messages if message.get("role") == "tool"]


class OneRound(unittest.TestCase):
    """1. No tool call: one model call and her words."""

    def test_words_only_end_the_loop(self):
        client = FakeClient([reply(text="你好呀")])
        given = [{"role": "user", "content": "在吗"}]
        result = go(client, system="你是小爱", messages=given, tools=[a_tool()])
        self.assertEqual(result.text, "你好呀")
        self.assertEqual(result.reason, "done")
        self.assertEqual(result.rounds, 1)
        self.assertEqual(result.calls, ())
        self.assertEqual(result.usage, dict(ZERO))
        self.assertEqual(client.rounds[0]["system"], "你是小爱")
        self.assertEqual(client.rounds[0]["messages"], [{"role": "user", "content": "在吗"}])
        self.assertEqual(client.rounds[0]["tools"], [a_tool().tool])
        self.assertEqual(given, [{"role": "user", "content": "在吗"}])


class ToolRound(unittest.TestCase):
    """2. One call, one handler, then her words; what the next round sees."""

    def test_a_call_then_words(self):
        seen = Handler(result="查到了")
        one = a_tool("one", {"q": {}}, seen)
        client = FakeClient([reply(text="我看一眼", calls=[call("one", {"q": "天气"}, id="call_7")]),
                             reply(text="今天很热")])
        result = go(client, messages=[{"role": "user", "content": "去"}], tools=[one])
        self.assertEqual(result.text, "今天很热")
        self.assertEqual(result.reason, "done")
        self.assertEqual(result.rounds, 2)
        self.assertEqual(result.calls, (("one", {"q": "天气"}),))
        self.assertEqual(seen.got, [{"q": "天气"}])
        sent = client.rounds[1]["messages"]
        self.assertEqual(len(sent), 3)
        self.assertEqual(sent[0], {"role": "user", "content": "去"})
        self.assertEqual(sent[1], {"role": "assistant", "content": "我看一眼", "tool_calls": [
            {"id": "call_7", "type": "function",
             "function": {"name": "one", "arguments": json.dumps({"q": "天气"}, ensure_ascii=False)}}]})
        self.assertEqual(sent[2], {"role": "tool", "tool_call_id": "call_7", "content": "查到了"})


class Reasoning(unittest.TestCase):
    """3. The model's reasoning goes back with the assistant message; empty means no key."""

    def said_after_one_call(self, thinking):
        client = FakeClient([reply(calls=[call()], reasoning=thinking), reply(text="好了")])
        go(client, tools=[a_tool(handler=Handler())])
        assistant = [message for message in client.rounds[1]["messages"]
                     if message.get("role") == "assistant"]
        self.assertEqual(len(assistant), 1)
        return assistant[0]

    def test_reasoning_is_given_back(self):
        self.assertEqual(self.said_after_one_call("先想一想")["reasoning_content"], "先想一想")

    def test_no_reasoning_is_no_key(self):
        self.assertNotIn("reasoning_content", self.said_after_one_call(""))
        self.assertNotIn("reasoning_content", self.said_after_one_call(None))


class UnknownTool(unittest.TestCase):
    """4. A name the loop does not know runs nothing."""

    def test_an_unknown_tool_is_not_run(self):
        known = Handler(result="跑了")
        client = FakeClient([reply(calls=[call("nope", {"q": "x"}, id="c1")]), reply(text="说完了")])
        result = go(client, tools=[a_tool("one", {"q": {}}, known)])
        self.assertEqual(known.got, [])
        self.assertEqual(client.rounds[1]["messages"][1],
                         {"role": "tool", "tool_call_id": "c1", "content": "没有这个工具。"})
        self.assertEqual(result.text, "说完了")
        self.assertEqual(result.calls, (("nope", {"q": "x"}),))


class Arguments(unittest.TestCase):
    """5. Only the arguments the tool's schema names reach the handler."""

    def test_arguments_not_in_the_schema_are_dropped(self):
        seen = Handler()
        client = FakeClient([reply(calls=[call("one", {"q": "x", "n": 3, "url": "u"})]),
                             reply(text="好")])
        go(client, tools=[a_tool("one", {"q": {}, "n": {}}, seen)])
        self.assertEqual(seen.got, [{"q": "x", "n": 3}])


class Failures(unittest.TestCase):
    """6. A handler's error is one sentence, with no error text, and the loop goes on."""

    def test_a_handler_error_is_one_sentence(self):
        seen = Handler(error=ValueError("很私密的内容"))
        client = FakeClient([reply(calls=[call()]), reply(text="接着说")])
        result = go(client, tools=[a_tool(handler=seen)])
        content = client.rounds[1]["messages"][1]["content"]
        self.assertEqual(content, "这一步出错了（ValueError）。")
        self.assertNotIn("很私密的内容", content)
        self.assertEqual(result.text, "接着说")
        self.assertEqual(result.reason, "done")
        self.assertEqual(len(seen.got), 1)


class Results(unittest.TestCase):
    """7. A result is cut to RESULT_CHARS, and anything that is not text becomes text."""

    def test_a_long_result_is_cut(self):
        client = FakeClient([reply(calls=[call()]), reply(text="好")])
        go(client, tools=[a_tool(handler=Handler(result="啊" * (tool_loop.RESULT_CHARS + 99)))])
        content = client.rounds[1]["messages"][1]["content"]
        self.assertEqual(len(content), tool_loop.RESULT_CHARS)

    def test_a_number_becomes_text(self):
        client = FakeClient([reply(calls=[call()]), reply(text="好")])
        go(client, tools=[a_tool(handler=Handler(result=10001))])
        self.assertEqual(client.rounds[1]["messages"][1]["content"], "10001")


class LastRound(unittest.TestCase):
    """8. The last round has no tools and a closing note, and the loop ends as "rounds"."""

    def test_the_last_round_has_no_tools(self):
        client = FakeClient([reply(calls=[call("one", {"q": "x"})]) for _ in range(5)])
        result = go(client, tools=[a_tool("one", {"q": {}}, Handler())], max_rounds=3)
        self.assertEqual(result.reason, "rounds")
        self.assertEqual(result.rounds, 3)
        self.assertEqual(len(client.rounds), 3)
        self.assertIsNotNone(client.rounds[0]["tools"])
        self.assertIsNotNone(client.rounds[1]["tools"])
        self.assertIsNone(client.rounds[2]["tools"])
        self.assertEqual(client.rounds[2]["messages"][-1],
                         {"role": "user", "content": "该收尾了，直接说你要说的话。"})
        self.assertEqual(len(tools_of(client.rounds[2]["messages"])), 2)


class Repeats(unittest.TestCase):
    """9 and 10. The same call too often is warned, then not run; key order does not matter."""

    def test_warned_then_stopped(self):
        seen = Handler(result="一样")
        client = FakeClient([reply(calls=[call()]), reply(calls=[call()]), reply(calls=[call()]),
                             reply(text="我说完了")])
        with SmallRepeat(2, 3):
            result = go(client, tools=[a_tool(handler=seen)])
        self.assertEqual(len(seen.got), 2)   # the third one is not run
        self.assertEqual(client.rounds[2]["messages"][-1]["content"],
                         "一样" + tool_loop.REPEATED)
        self.assertEqual(client.rounds[3]["messages"][-2],
                         {"role": "tool", "tool_call_id": "call_1",
                          "content": "同样的事做太多次了，先停下。"})
        self.assertEqual(client.rounds[3]["messages"][-1],
                         {"role": "user", "content": "该收尾了，直接说你要说的话。"})
        self.assertIsNone(client.rounds[3]["tools"])
        self.assertEqual(result.text, "我说完了")
        self.assertEqual(result.reason, "repeat")
        self.assertEqual(result.rounds, 4)

    def test_another_key_order_is_the_same_call(self):
        seen = Handler()
        client = FakeClient([reply(calls=[call("one", {"a": 1, "b": 2})]),
                             reply(calls=[call("one", {"b": 2, "a": 1})]),
                             reply(text="好")])
        with SmallRepeat(2, 9):
            go(client, tools=[a_tool("one", {"a": {}, "b": {}}, seen)])
        self.assertEqual(len(seen.got), 2)
        self.assertEqual(client.rounds[2]["messages"][-1]["content"],
                         "ok" + tool_loop.REPEATED)


class Stops(unittest.TestCase):
    """11. A round too slow ends as "timeout"; another error comes out as it is."""

    def test_a_slow_client_times_out(self):
        client = FakeClient([reply(text="太晚了")], slow=0.2)
        result = go(client, messages=[{"role": "user", "content": "在吗"}], round_seconds=0.01)
        self.assertEqual(result.reason, "timeout")
        self.assertEqual(result.text, "")
        self.assertEqual(result.rounds, 1)
        self.assertEqual(result.calls, ())
        self.assertEqual(result.usage, dict(ZERO))

    def test_another_error_passes_through(self):
        error = RuntimeError("模型坏了")
        client = FakeClient([reply()], error=error)
        with self.assertRaises(RuntimeError) as caught:
            go(client)
        self.assertIs(caught.exception, error)


class Usage(unittest.TestCase):
    """12. Every round's usage is added up."""

    def test_usage_is_added_up(self):
        client = FakeClient([
            reply(calls=[call()], usage={"input_miss": 100, "input_hit": 10, "output": 5}),
            reply(text="好", usage={"input_miss": 20, "input_hit": 2, "output": 7})])
        result = go(client, tools=[a_tool(handler=Handler())])
        self.assertEqual(result.usage, {"input_miss": 120, "input_hit": 12, "output": 12})


class TheSource(unittest.TestCase):
    """13. The loop knows nothing of the plugin framework, files or the network."""

    def test_the_loop_has_no_other_world(self):
        source = (ROOT / "tool_loop.py").read_text(encoding="utf-8").lower()
        for word in ("astrbot", "mixin_", "import os", "import subprocess", "import socket"):
            self.assertNotIn(word, source, word)


if __name__ == "__main__":
    unittest.main()
