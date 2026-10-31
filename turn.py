# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The mutable request and reply of one turn, independent of the platform."""
from dataclasses import dataclass, field


@dataclass(eq=False)
class TurnEvent:
    """One received message as the plugin handles it, apart from AstrBot: the Incoming, and
    whether handling it stopped. The plugin may keep its own notes for this turn on it, as
    attributes, as it does on AstrBot's event."""
    incoming: object
    stopped: bool = False

    def stop_event(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped


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
    extra_user_content_parts: list = field(default_factory=list)  # None: platform puts the turn block in system prompt
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
    first_message: list = None

    def set_text(self, text):
        self.text = str(text or '')

    def map_words(self, fn):
        self.text = fn(self.text)
        return self.text

    def spend_usage(self):
        return dict(self.usage)

    def reported_usage(self):
        return dict(self.usage)

    def shape_first(self, first_text):
        try:
            from . import messenger
        except ImportError:
            import messenger
        self.first_message = list(self.chain_prefix) + list(messenger.text_segments(first_text))
