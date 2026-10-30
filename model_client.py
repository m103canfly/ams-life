# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""One chat model, whichever service answers: the one place the plugin asks a model.

A chat is some words (prompt), an optional system prompt, whole messages (contexts), images,
and tools. The answer is the words, the tool calls it asked for, the usage, and the model's
own reasoning.

Only the standard library and browse.usage_of; nothing here talks to a service or a plugin
framework, so this file stays the same when another client is added.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

try:
    from . import browse
except ImportError:
    import browse


@dataclass(frozen=True)
class Tool:
    """A tool the model may ask for."""

    name: str
    description: str
    parameters: dict      # JSON Schema, as the plugin's *_PARAMS are today


@dataclass(frozen=True)
class ToolCall:
    """One tool call the model asked for."""

    id: str
    name: str
    arguments: dict       # {} when the model gave none or gave something unreadable


@dataclass(frozen=True)
class ModelReply:
    """What one chat gave back."""

    text: str             # "" when none
    tool_calls: tuple     # tuple of ToolCall, in the model's order
    usage: dict           # exactly browse.usage_of(...): {"input_miss", "input_hit", "output"}
    reasoning: str        # the model's reasoning_content when it gives one, else ""


class ModelClient:
    """One chat model. A client for a service overrides chat()."""

    async def chat(self, *, prompt=None, system=None, messages=None, images=None,
                   tools=None) -> ModelReply:
        """Ask the model once. Only the arguments given are used; None means not given."""
        raise NotImplementedError


def arguments_of(raw) -> dict:
    """A tool call's arguments: a dict as is; a JSON object string parsed; anything else {}."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            value = json.loads(raw)
        except ValueError:
            return {}
        return value if isinstance(value, dict) else {}
    return {}
