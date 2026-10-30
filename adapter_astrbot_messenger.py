# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""``messenger.Messenger`` over the bot framework.

``send`` builds the very components the plugin builds today (``mixin_attention._chain_of``,
``mixin_selfie``, ``mixin_stickers``) and hands the chain to ``context.send_message``.
``call`` asks the bot for one of ``messenger.ALLOWED_ACTIONS``. The framework's components are
imported inside the functions, as ``mixin_attention._chain_of`` does, so this module imports no
framework at the top.
"""
from __future__ import annotations

try:
    from . import messenger
except ImportError:
    import messenger


def _component(segment):
    """One component for one sendable segment (checked by messenger.check_segments first)."""
    from astrbot.api.message_components import Face, Image, Plain, Record
    kind, data = segment.type, segment.data
    if kind == "text":
        return Plain(str(data["text"]))
    if kind == "face":
        return Face(id=data["id"])
    if kind == "image":
        if "path" in data:
            return Image.fromFileSystem(str(data["path"]))
        if "base64" in data:
            return Image.fromBase64(str(data["base64"]))
        return Image.fromURL(str(data["url"]))
    return Record.fromFileSystem(str(data["path"]))


class AstrBotMessenger(messenger.Messenger):
    """Messenger over AstrBot: one context, the umo of a place, and the bot of the moment.

    ``context`` is the plugin's ``self.context``; ``umo_of(place) -> str`` gives the AstrBot
    session of a place ("" when there is none); ``bot_of() -> bot or None`` gives the bot now.
    """

    def __init__(self, context, umo_of, bot_of, event_send=None, event_place=""):
        self.context = context
        self.umo_of = umo_of
        self.bot_of = bot_of
        self.event_send = event_send
        self.event_place = event_place

    async def send(self, place: str, segments: tuple) -> messenger.Sent:
        """The whole message in one place, or nothing at all; a failed send raises as AstrBot does."""
        segments = messenger.check_segments(segments)
        if self.event_send is not None and place == self.event_place:
            from astrbot.api.event import MessageChain
            await self.event_send(MessageChain([_component(segment) for segment in segments]))
            return messenger.Sent(True, "")
        umo = str(self.umo_of(place) or "")
        if not umo:
            return messenger.Sent(False, "")
        from astrbot.api.event import MessageChain
        chain = MessageChain([_component(segment) for segment in segments])
        result = await self.context.send_message(umo, chain)
        return messenger.Sent(ok=result is not False, message_id="")

    async def call(self, action: str, **params) -> dict:
        """One allowed action, with these parameters; whatever is not a dict becomes {}."""
        if action not in messenger.ALLOWED_ACTIONS:
            raise messenger.ActionRefused(action)
        bot = self.bot_of()
        if bot is None:
            raise RuntimeError("no bot")
        call_action = getattr(getattr(bot, "api", None), "call_action", None)
        if not callable(call_action):
            call_action = bot.call_action
        result = await call_action(action, **params)
        return result if isinstance(result, dict) else {}
