# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Standalone stand-in; use AstrBot itself when installed."""


class EventMessageType:
    GROUP_MESSAGE = 1
    PRIVATE_MESSAGE = 2
    OTHER_MESSAGE = 4
    ALL = 7


class _Filter:
    """Every filter.xxx(...) returns a decorator that leaves the function unchanged."""

    EventMessageType = EventMessageType

    def __getattr__(self, name):
        def factory(*args, **kwargs):
            if len(args) == 1 and callable(args[0]) and not kwargs:
                return args[0]

            def deco(fn):
                return fn
            return deco
        return factory


filter = _Filter()


class AstrMessageEvent:
    pass


class MessageChain:
    def __init__(self, chain=None):
        self.chain = list(chain or [])

    def message(self, text):
        from .message_components import Plain
        self.chain.append(Plain(text))
        return self

    def get_plain_text(self):
        from .message_components import Plain
        return " ".join(c.text for c in self.chain if isinstance(c, Plain))

    def __bool__(self):
        return bool(self.chain)


class MessageEventResult(MessageChain):
    def use_t2i(self, flag):
        self.t2i = flag
        return self
