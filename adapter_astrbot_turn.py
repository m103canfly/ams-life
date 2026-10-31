# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Convert one turn to and from AstrBot's request and response."""
try:
    from . import adapter_astrbot, adapter_astrbot_model, attention, browse, turn
except ImportError:
    import adapter_astrbot
    import adapter_astrbot_model
    import attention
    import browse
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


class AstrBotReply:
    """AstrBot's LLMResponse behind the reply handle: every change is made the way the plugin
    made it by hand before, so nothing AstrBot sends or saves changes."""

    def __init__(self, response):
        self.response = response

    @property
    def text(self):
        # main.py 751 at c209cf5.
        return str(getattr(self.response, "completion_text", "") or "")

    def set_text(self, text):
        response = self.response
        # mixin_send_check.py 199-212 at c209cf5.
        response.completion_text = text
        chain = getattr(response, "result_chain", None)
        if chain is not None and getattr(chain, "chain", None):
            first = True
            kept = []
            for comp in chain.chain:
                if hasattr(comp, "text"):
                    if first:
                        comp.text = text
                        kept.append(comp)
                        first = False
                    continue   # the other text parts were the old words
                kept.append(comp)
            chain.chain = kept

    def map_words(self, fn):
        # main.py 754-765 at c209cf5, with fn in place of strip_state_tags.
        response = self.response
        text = self.text
        new = fn(text)
        if new != text:
            try:
                response.completion_text = new
                chain = getattr(response, "result_chain", None)
                if chain is not None and getattr(chain, "chain", None):
                    for comp in chain.chain:
                        if hasattr(comp, "text"):
                            comp.text = fn(str(comp.text or ""))
            except Exception:
                pass
        return new

    def spend_usage(self):
        resp = self.response
        # mixin_attention.py 117-126 at c209cf5.
        raw = getattr(getattr(resp, "raw_completion", None), "usage", None)
        hit = getattr(raw, "prompt_cache_hit_tokens", None) if raw is not None else None
        miss = getattr(raw, "prompt_cache_miss_tokens", None) if raw is not None else None
        if isinstance(hit, int) and isinstance(miss, int):
            return {"input_hit": hit, "input_miss": miss, "output": int(getattr(raw, "completion_tokens", 0) or 0)}
        u = getattr(resp, "usage", None)
        if u is None:
            return {}
        return {"input_hit": int(getattr(u, "input_cached", 0) or 0),
                "input_miss": int(getattr(u, "input_other", 0) or 0), "output": int(getattr(u, "output", 0) or 0)}

    def reported_usage(self):
        return browse.usage_of(getattr(self.response, "usage", None))

    def shape_first(self, first_text):
        response = self.response
        first = first_text
        # mixin_attention.py 429-434 at c209cf5, using chain_of directly.
        from astrbot.api.message_components import At, Reply
        previous = getattr(getattr(response, "result_chain", None), "chain", None) or []
        prefix = [component for component in previous if isinstance(component, (Reply, At))]
        shaped = chain_of(first)
        shaped.chain = prefix + shaped.chain
        response.result_chain = shaped


def reply_handle(obj):
    """A reply handle as it is; anything else is AstrBot's LLMResponse, wrapped."""
    if isinstance(obj, (turn.TurnReply, AstrBotReply)):
        return obj
    return AstrBotReply(obj)


def chain_of(text):
    # mixin_attention.py 379-385 at c209cf5.
    """One message as a chain: words and QQ faces (attention.pieces)."""
    from astrbot.api.event import MessageChain
    from astrbot.api.message_components import Face, Plain
    chain = []
    for kind, value in attention.pieces(text):
        chain.append(Face(id=value) if kind == "face" else Plain(value))
    return MessageChain(chain)
