# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her own tool loop: one plain loop that asks a model, runs the tools it asks for, and stops.

The loop is what a reply and a trip need alike: a few rounds, every tool call run in order, every
result sent back, and a last round without tools so she says her words. Only the standard library
and model_client; nothing here touches a service, a framework, a file or the network itself.
"""
from __future__ import annotations

import asyncio
import inspect
import json
from dataclasses import dataclass

try:
    from . import model_client
except ImportError:
    import model_client


MAX_ROUNDS = 8            # model calls in one loop, the last one without tools
RESULT_CHARS = 4000       # one tool result, cut to this
REPEAT_WARN = 10          # the same call this many times: a note to her
REPEAT_STOP = 20          # this many: not run; the next round is the last

CLOSING = "该收尾了，直接说你要说的话。"
NO_TOOL = "没有这个工具。"
REPEATED = "你已经重复做了很多次同样的事，换个办法或者直接说。"
TOO_MANY = "同样的事做太多次了，先停下。"
FAILED = "这一步出错了（%s）。"


@dataclass(frozen=True)
class LoopTool:
    """A tool the loop may run: what the model is told, and what runs for it."""

    tool: model_client.Tool
    handler: object       # async callable(**arguments) -> str


@dataclass(frozen=True)
class LoopResult:
    """What one loop gave back."""

    text: str             # her final words ("" when none)
    rounds: int           # model calls made
    calls: tuple          # (name, arguments) of every tool call made, in order
    usage: dict           # the rounds' usage added up: {"input_miss", "input_hit", "output"}
    reason: str           # "done" | "rounds" | "repeat" | "timeout"


def call_key(name, arguments) -> str:
    """The same call, written in another key order, gets the same key."""
    try:
        body = json.dumps(arguments, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        body = str(arguments)
    return name + "\n" + body


async def run(client, *, system=None, messages=(), tools=(), max_rounds=MAX_ROUNDS,
              round_seconds=None) -> LoopResult:
    """Ask the model up to max_rounds times, run the tools it asks for, and stop.

    The messages given are copied, never changed: the turns this loop adds stay inside it.
    A call the loop has seen REPEAT_STOP times is not run, and the next round is the last.
    """
    current = list(messages)
    entries = list(tools)
    by_name = {entry.tool.name: entry for entry in entries}
    schemas = [entry.tool for entry in entries]
    made = []
    totals = {"input_miss": 0, "input_hit": 0, "output": 0}
    seen = {}
    rounds = 0
    closing = False       # this round is the last one: no tools, and a note to say her words
    repeated = False      # the loop ends because one call was made too many times
    while True:
        rounds += 1
        final = closing or rounds >= max_rounds
        asked = list(current)
        if final:
            asked.append({"role": "user", "content": CLOSING})
        ask = {"system": system, "messages": asked,
               "tools": None if final or not schemas else list(schemas)}
        if round_seconds is None:
            reply = await client.chat(**ask)
        else:
            try:
                reply = await asyncio.wait_for(client.chat(**ask), round_seconds)
            except asyncio.TimeoutError:
                return LoopResult(text="", rounds=rounds, calls=tuple(made),
                                  usage=dict(totals), reason="timeout")
        usage = getattr(reply, "usage", None) or {}
        for key in totals:
            totals[key] += int(usage.get(key) or 0)
        calls = tuple(getattr(reply, "tool_calls", None) or ())
        said = str(reply.text or "")
        if not calls:
            reason = "repeat" if repeated else ("rounds" if final else "done")
            return LoopResult(text=said, rounds=rounds, calls=tuple(made),
                              usage=dict(totals), reason=reason)
        words = [{"id": call.id, "type": "function",
                  "function": {"name": call.name,
                               "arguments": json.dumps(call.arguments, ensure_ascii=False)}}
                 for call in calls]
        turn = {"role": "assistant", "content": said, "tool_calls": words}
        thinking = getattr(reply, "reasoning", "") or ""
        if thinking:
            turn["reasoning_content"] = thinking   # DeepSeek wants its thinking back
        current.append(turn)
        for call in calls:
            made.append((call.name, dict(call.arguments)))
            entry = by_name.get(call.name)
            if entry is None:
                out = NO_TOOL
            else:
                allowed = (entry.tool.parameters or {}).get("properties") or {}
                arguments = {key: value for key, value in call.arguments.items() if key in allowed}
                key = call_key(call.name, call.arguments)
                count = seen.get(key, 0) + 1
                seen[key] = count
                if count >= REPEAT_STOP:
                    out = TOO_MANY
                    repeated = True
                    closing = True
                else:
                    try:
                        result = entry.handler(**arguments)
                        if inspect.isawaitable(result):
                            result = await result
                        out = result if isinstance(result, str) else str(result)
                    except Exception as exc:
                        out = FAILED % type(exc).__name__
                    out = out[:RESULT_CHARS]
                    if count == REPEAT_WARN:
                        out = out + REPEATED
            current.append({"role": "tool", "tool_call_id": call.id, "content": out})
        if final:
            return LoopResult(text=said, rounds=rounds, calls=tuple(made),
                              usage=dict(totals), reason="repeat" if repeated else "rounds")
