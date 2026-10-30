# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The model client over AstrBot's provider: today's model call, behind one interface.

The plugin still asks a provider's text_chat; this turns that call into ModelClient.chat, with
the same arguments as today's call sites and the same fields read of the reply:

- prompt -> prompt; system -> system_prompt; messages -> contexts; images -> image_urls;
  tools (when not empty) -> func_tool, one ToolSet of FunctionTool made by toolset_of;
- the reply: completion_text -> text, tools_call_name / tools_call_args / tools_call_ids paired
  by position -> tool_calls, usage -> browse.usage_of, reasoning_content -> reasoning.

Only what was given is passed on: None is not given, "" is. An error text_chat raises passes
through as it is; nothing is logged here.
"""
from __future__ import annotations

try:
    from . import browse, model_client
except ImportError:
    import browse
    import model_client


def _not_run_here(*args, **kwargs):
    """A tool's placeholder handler: the plugin runs its own tools, AstrBot must not run them."""
    raise RuntimeError("tools are run by the plugin, not by the model provider")


def _default_toolset_of(tools):
    """One AstrBot ToolSet of FunctionTool, each with the placeholder handler above."""
    from astrbot.core.agent.tool import FunctionTool, ToolSet
    return ToolSet([FunctionTool(name=tool.name, description=tool.description,
                                 parameters=tool.parameters, handler=_not_run_here)
                    for tool in tools])


class AstrBotModel(model_client.ModelClient):
    """A ModelClient over one provider -- the one a received message came in on, usually."""

    def __init__(self, provider, toolset_of=None):
        self.provider = provider
        self.toolset_of = toolset_of or _default_toolset_of

    async def chat(self, *, prompt=None, system=None, messages=None, images=None,
                   tools=None) -> model_client.ModelReply:
        sent = {}
        if prompt is not None:
            sent["prompt"] = prompt
        if system is not None:
            sent["system_prompt"] = system
        if messages is not None:
            sent["contexts"] = list(messages)
        if images is not None:
            sent["image_urls"] = list(images)
        if tools:
            sent["func_tool"] = self.toolset_of(tools)
        return _reply_of(await self.provider.text_chat(**sent))


def _reply_of(resp) -> model_client.ModelReply:
    """A provider's reply as a ModelReply; a field that cannot be read gives its empty value."""
    names = list(getattr(resp, "tools_call_name", None) or [])
    args = list(getattr(resp, "tools_call_args", None) or [])
    ids = list(getattr(resp, "tools_call_ids", None) or [])
    calls = []
    for i, name in enumerate(names):
        name = str(name or "")
        if not name:
            continue
        call_id = ids[i] if i < len(ids) else None
        calls.append(model_client.ToolCall(
            id=str(call_id) if call_id else "call_%d" % i,
            name=name,
            arguments=model_client.arguments_of(args[i] if i < len(args) else {})))
    return model_client.ModelReply(
        text=str(getattr(resp, "completion_text", "") or ""),
        tool_calls=tuple(calls),
        usage=browse.usage_of(getattr(resp, "usage", None)),
        reasoning=str(getattr(resp, "reasoning_content", "") or ""))
