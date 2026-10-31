# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Convert one turn to and from AstrBot's request and response."""
try:
    from . import adapter_astrbot, adapter_astrbot_model, turn
except ImportError:
    import adapter_astrbot
    import adapter_astrbot_model
    import turn


def request_from_astrbot(req) -> turn.TurnRequest:
    toolset = getattr(req, 'func_tool', None)
    parts = getattr(req, 'extra_user_content_parts', None)
    tools = [turn.TurnTool(name=getattr(tool, 'name', '') or '',
                           description=getattr(tool, 'description', '') or '',
                           parameters=getattr(tool, 'parameters', None) or {},
                           handler=getattr(tool, 'handler', None), native=tool)
             for tool in (getattr(toolset, 'tools', None) or [])]
    return turn.TurnRequest(
        prompt=getattr(req, 'prompt', '') or '',
        system_prompt=getattr(req, 'system_prompt', '') or '',
        contexts=list(getattr(req, 'contexts', None) or []),
        image_urls=list(getattr(req, 'image_urls', None) or []),
        extra_user_content_parts=list(parts) if isinstance(parts, list) else None,
        tools=tools)


def request_into_astrbot(turn_request, req) -> None:
    """Write changed fields back, preserving unchanged objects and missing fields."""
    for name in ('prompt', 'system_prompt'):
        value = getattr(turn_request, name)
        if (getattr(req, name, None) or '') != value:
            setattr(req, name, value)
    for name in ('contexts', 'image_urls', 'extra_user_content_parts'):
        value = getattr(turn_request, name)
        if value is None:
            continue
        original = getattr(req, name, None)
        if isinstance(original, list):
            if original != value:
                original[:] = value
        elif value:
            setattr(req, name, value)
    original_tools = getattr(getattr(req, 'func_tool', None), 'tools', None) or []
    if (len(turn_request.tools) == len(original_tools) and
            all(tool.native is not None and tool.native is native
                for tool, native in zip(turn_request.tools, original_tools))):
        return
    if not turn_request.tools:
        req.func_tool = None
        return
    from astrbot.core.agent.tool import FunctionTool, ToolSet
    req.func_tool = ToolSet([tool.native if tool.native is not None else
                             FunctionTool(name=tool.name, description=tool.description,
                                          parameters=tool.parameters, handler=tool.handler)
                             for tool in turn_request.tools])


def reply_from_astrbot(resp) -> turn.TurnReply:
    reply = adapter_astrbot_model._reply_of(resp)
    chain = getattr(getattr(resp, 'result_chain', None), 'chain', None) or []
    components = [component for component in chain if type(component).__name__ in ('Reply', 'At')]
    return turn.TurnReply(text=reply.text, chain_prefix=list(adapter_astrbot._segments(components)),
                          tool_calls=reply.tool_calls, usage=reply.usage, reasoning=reply.reasoning)


def reply_into_astrbot(turn_reply, resp) -> None:
    resp.completion_text = turn_reply.text
