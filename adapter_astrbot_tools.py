# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her tools (turn.TurnTool) put into AstrBot's request, as the plugin did by hand."""


def available() -> bool:
    """Whether AstrBot's tool classes can be imported (astrbot.core.agent.tool)."""
    try:
        from astrbot.core.agent.tool import FunctionTool, ToolSet  # noqa: F401
    except ImportError:
        return False
    return True


def function_tool(tool):
    """One FunctionTool from one TurnTool: name, description, parameters, handler."""
    from astrbot.core.agent.tool import FunctionTool
    return FunctionTool(name=tool.name, description=tool.description,
                        parameters=tool.parameters, handler=tool.handler)


def add_to_request(req, tools) -> None:
    """As the plugin did: no tool set yet -> req.func_tool = ToolSet([...]);
    else existing.add_tool(each), in order."""
    from astrbot.core.agent.tool import ToolSet
    existing = getattr(req, "func_tool", None)
    if existing is None:
        req.func_tool = ToolSet([function_tool(tool) for tool in tools])
    else:
        for tool in tools:
            existing.add_tool(function_tool(tool))
