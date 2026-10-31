# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The mutable request and reply of one turn, independent of the platform."""
from dataclasses import dataclass, field


@dataclass
class TurnTool:
    name: str
    description: str
    parameters: dict
    handler: object = None
    native: object = None


@dataclass
class TurnRequest:
    prompt: str = ''
    system_prompt: str = ''
    contexts: list = field(default_factory=list)
    image_urls: list = field(default_factory=list)
    extra_user_content_parts: list = field(default_factory=list)
    tools: list = field(default_factory=list)
    extras: dict = field(default_factory=dict)

    def tool_names(self) -> list:
        return [tool.name for tool in self.tools]

    def remove_tool(self, name) -> None:
        self.tools[:] = [tool for tool in self.tools if tool.name != name]

    def add_tool(self, tool) -> None:
        for index, existing in enumerate(self.tools):
            if existing.name == tool.name:
                self.tools[index] = tool
                return
        self.tools.append(tool)


@dataclass
class TurnReply:
    text: str = ''
    chain_prefix: list = field(default_factory=list)
    tool_calls: tuple = ()
    usage: dict = field(default_factory=dict)
    reasoning: str = ''
    extras: dict = field(default_factory=dict)
