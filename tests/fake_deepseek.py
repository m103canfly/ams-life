# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""A fake DeepSeek chat client for tests: it stands in for ``openai.AsyncOpenAI``.

A test scripts one reply with ``say`` or ``call_tools``; every call to
``.chat.completions.create(**kwargs)`` gives back the next scripted reply, shaped as the SDK
shapes a ``ChatCompletion``: the words, the tool calls (their arguments a JSON string), the
usage, and the reasoning in ``message.model_extra``, where the SDK keeps a field it does not
know. A call with no scripted reply left is a mistake in the test, so it raises
``AssertionError`` at once. Only the standard library; no SDK, no network.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

# The made-up numbers a reply carries when the test does not say; nothing here is a real count.
DEFAULT_USAGE = {"prompt_tokens": 100, "completion_tokens": 8,
                 "prompt_cache_hit_tokens": 40, "prompt_cache_miss_tokens": 60}


class FakeUsage:
    """The usage of one reply: the SDK's four attributes, and ``model_dump()``."""

    FIELDS = ("prompt_tokens", "completion_tokens", "prompt_cache_hit_tokens",
              "prompt_cache_miss_tokens")

    def __init__(self, values=None):
        data = dict(DEFAULT_USAGE)
        data.update(values or {})
        self._data = {name: max(0, int(data.get(name) or 0)) for name in self.FIELDS}
        for name, value in self._data.items():
            setattr(self, name, value)

    def model_dump(self) -> dict:
        """The same numbers as a plain dict, as the SDK does it."""
        return dict(self._data)


class FakeDeepSeek:
    """Stands in for openai.AsyncOpenAI: .chat.completions.create(**kwargs) -> a ChatCompletion-shaped object."""

    def __init__(self):
        self.chat = SimpleNamespace(completions=self)
        self.requests = []    # every create() kwargs, in order; messages copied
        self.responses = []   # every object given back, in order
        self._scripted = []   # the replies still to use, in order
        self._calls_made = 0  # tool calls scripted so far, for their ids

    def say(self, text, *, reasoning="", usage=None):
        """Script one reply of words."""
        self._scripted.append({"text": str(text or ""), "calls": (),
                               "reasoning": str(reasoning or ""), "usage": usage})

    def call_tools(self, *calls, text="", reasoning="", usage=None):
        """Script one reply of tool calls; each call is a (name, arguments dict)."""
        made = []
        for call in calls:
            name, arguments = call
            self._calls_made += 1
            made.append(("call_%d" % self._calls_made, str(name), dict(arguments or {})))
        self._scripted.append({"text": str(text or ""), "calls": tuple(made),
                               "reasoning": str(reasoning or ""), "usage": usage})

    async def create(self, **kwargs):
        """One reply: the next scripted one, shaped as the SDK shapes it."""
        request = dict(kwargs)
        request["messages"] = [dict(message) for message in (kwargs.get("messages") or ())]
        self.requests.append(request)
        if not self._scripted:
            raise AssertionError("no scripted reply")
        script = self._scripted.pop(0)
        response = self._response(script, kwargs.get("model"), len(self.responses) + 1)
        self.responses.append(response)
        return response

    def _response(self, script, model, number):
        """One ChatCompletion-shaped object for one scripted reply."""
        calls = [SimpleNamespace(
            id=call_id, type="function",
            function=SimpleNamespace(name=name,
                                     arguments=json.dumps(arguments, ensure_ascii=False)))
            for call_id, name, arguments in script["calls"]]
        reasoning = script["reasoning"]
        message = SimpleNamespace(content=script["text"], role="assistant",
                                  tool_calls=calls or None,
                                  model_extra={"reasoning_content": reasoning} if reasoning else {})
        return SimpleNamespace(id="chatcmpl-fake-%d" % number, model=model,
                               choices=[SimpleNamespace(
                                   message=message,
                                   finish_reason="tool_calls" if calls else "stop")],
                               usage=FakeUsage(script["usage"]))
