# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""One received message, apart from AstrBot.

A message is a place, who sent it, her own account id, the message id, the parts in
order (segments), whether it addresses her, the id it quotes, the images it carries,
and whether it is in a private chat or is her own. The future QQ layer will build the
same shape from NapCat's raw message; ``adapter_astrbot`` builds it from an AstrBot
event today. Pure data only: no I/O, no AstrBot.

What ``Segment.data`` holds, by type:

    text     {"text": the words}
    at       {"qq": number, "name": name or ""}
    reply    {"id": quoted message id or "", "sender_id": quoted sender id or ""}
    image    {"url": ..., "file": ...} (either may be "")
    face     {"id": face id}
    record   {"url": ..., "file": ...}
    forward  {"id": forwarded message id}
    other    {"kind": the component's class name}
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:
    """One part of a message, with OneBot-like fields."""

    type: str    # one of: "text", "at", "reply", "image", "face", "record", "forward", "other"
    data: dict   # OneBot-like fields, see the table above


@dataclass(frozen=True)
class Incoming:
    """One message as she receives it."""

    place: str            # "group:<id>" or "private:<id>", exactly as discretion.place_of() gives
    sender_id: str        # "" when unknown
    sender_name: str      # "" when unknown
    self_id: str          # her own account id, "" when unknown
    message_id: str       # "" when unknown
    segments: tuple       # tuple of Segment, in order
    at_me: bool           # someone @-ed her, quoted her, or the platform says it woke her
    reply_to: str         # id of the quoted message, "" when none
    image_refs: tuple     # url/file of images in THIS message (not in quotes), in order
    is_private: bool      # place starts with "private:"
    is_self: bool         # sender_id == self_id and both are not ""
    ts: float             # time.time() when built


def plain_text(incoming) -> str:
    """Only the text segments joined in order; nothing else (no @, no placeholders)."""
    return "".join(str(seg.data.get("text", "") or "") for seg in incoming.segments if seg.type == "text")
