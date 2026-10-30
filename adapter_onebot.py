# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Build an ``events.Incoming`` from one NapCat (OneBot 11) message event.

``from_onebot`` is what ``adapter_astrbot.from_astrbot`` is for AstrBot's events: one received
message, field by field as AstrBot 4.29.3 splits it, so the same message gives the same Incoming
on both roads. It takes the raw JSON dict NapCat pushes (array format) and is pure and forgiving:
no I/O, no logging, and it never raises. A part it cannot read is left out; a payload that is not
one message event gives None.

Two things AstrBot looks up itself are passed in by the caller instead:
``quoted`` (the data of ``get_msg`` for the first quoted message) and ``names``
(``{qq: name}`` for the @ segments).
"""
from __future__ import annotations

import time

try:
    from . import events
except ImportError:
    import events

_REPLY_ID_CHARS = 80   # as adapter_astrbot: the first reply's id, cut to this

# The OneBot 11 segments events.py keeps as "other", and the AstrBot class name each one is.
_OTHER_KIND = {"video": "Video", "file": "File", "rps": "RPS", "dice": "Dice", "shake": "Shake",
               "share": "Share", "contact": "Contact", "location": "Location", "music": "Music",
               "poke": "Poke", "node": "Node", "nodes": "Nodes", "json": "Json"}


def _text(value) -> str:
    """A field as a string; anything unreadable is ""."""
    try:
        return str(value or "")
    except Exception:
        return ""


def _sender(payload) -> dict:
    """The sender object, or {} when there is none (or it is not one)."""
    sender = payload.get("sender")
    return sender if isinstance(sender, dict) else {}


def _sender_id(payload) -> str:
    """Who wrote it: the sender's number, else the event's own user_id, else ""."""
    sid = _text(_sender(payload).get("user_id"))
    if sid:
        return sid
    return _text(payload.get("user_id"))


def _sender_name(payload) -> str:
    """What they are called here: the card, else the nickname, else "" (AstrBot says "N/A")."""
    sender = _sender(payload)
    return _text(sender.get("card")) or _text(sender.get("nickname"))


def _place(payload) -> str:
    """A group is "group:<group id>"; a private chat is "private:<sender>" (AstrBot's session)."""
    if payload.get("message_type") == "group":
        return "group:" + _text(payload.get("group_id"))
    return "private:" + _sender_id(payload)


def _at_name(qq, names) -> str:
    """The name of the @: "全体成员" for all, else what the caller looked up; "" when unknown.

    A number may be written as a string on either side (NapCat's segment, the caller's table),
    so both forms are looked up."""
    text = _text(qq)
    if text == "all":
        return "全体成员"
    keys = [text, qq]
    if text.isdigit():
        keys.append(int(text))
    for key in keys:
        try:
            name = names.get(key) if hasattr(names, "get") else None
        except Exception:   # an unhashable qq is no key
            name = None
        if name:
            return _text(name)
    return ""


def _quoted_sender(quoted) -> str:
    """The sender of the quoted message, as the caller fetched it; "" when unknown."""
    try:
        sender = quoted.get("sender") if isinstance(quoted, dict) else None
        return _text(sender.get("user_id")) if isinstance(sender, dict) else ""
    except Exception:
        return ""


def _parts(payload) -> tuple:
    """The parts of the message that can be read, in order (dicts with a dict of data)."""
    out = []
    for part in payload.get("message") or []:
        try:
            if isinstance(part, dict) and isinstance(part.get("data"), dict):
                out.append(part)
        except Exception:
            continue
    return tuple(out)


def _segments(parts, self_id, quoted, names) -> tuple:
    """One Segment per part, in order, as AstrBot 4.29.3 splits the same chain."""
    out = []
    run = []   # the words of a row of text parts, joined when the row ends

    def flush():
        if run:
            words = "".join(run).strip()
            run.clear()
            if words:
                out.append(events.Segment(type="text", data={"text": words}))

    for part in parts:
        data = part.get("data") or {}
        kind = part.get("type")
        if not isinstance(kind, str):
            continue   # no known part: it is left out, as AstrBot leaves out what it does not know
        if kind == "text":
            run.append(_text(data.get("text")))
            continue
        flush()
        if kind == "at":
            out.append(events.Segment(type="at", data={"qq": _text(data.get("qq")),
                                                       "name": _at_name(data.get("qq"), names)}))
        elif kind == "reply":
            out.append(events.Segment(type="reply", data={"id": _text(data.get("id")),
                                                          "sender_id": _quoted_sender(quoted)}))
        elif kind == "image":
            out.append(events.Segment(type="image", data={"url": _text(data.get("url")),
                                                          "file": _text(data.get("file"))}))
        elif kind == "face":
            out.append(events.Segment(type="face", data={"id": _text(data.get("id"))}))
        elif kind == "record":
            out.append(events.Segment(type="record", data={"url": _text(data.get("url")),
                                                           "file": _text(data.get("file"))}))
        elif kind == "forward":
            out.append(events.Segment(type="forward", data={"id": _text(data.get("id"))}))
        elif kind == "markdown":
            # one piece of text as it is: not stripped and not joined with the text beside it
            out.append(events.Segment(type="text", data={
                "text": _text(data.get("markdown")) or _text(data.get("content"))}))
        elif kind in _OTHER_KIND:
            out.append(events.Segment(type="other", data={"kind": _OTHER_KIND[kind]}))
        # mface (the shop sticker) and the kinds not in the table are left out
    flush()
    return tuple(out)


def _reply_to(parts) -> str:
    """The first reply's id, cut to 80 characters, as adapter_astrbot gives it."""
    for part in parts:
        if part.get("type") == "reply":
            return _text((part.get("data") or {}).get("id"))[:_REPLY_ID_CHARS]
    return ""


def _image_ref(data) -> str:
    """One image's url, else its file, else "", as adapter_astrbot's _image_ref does."""
    try:
        return (_text(data.get("url")) or _text(data.get("file"))).strip()
    except Exception:
        return ""


def _image_refs(parts) -> tuple:
    """Every image of this message, in order; an image with neither url nor file is not one."""
    out = []
    for part in parts:
        if part.get("type") == "image":
            ref = _image_ref(part.get("data") or {})
            if ref:
                out.append(ref)
    return tuple(out)


def _at_me(parts, self_id, quoted) -> bool:
    """An @ of her own number, or the quoted message being her own; as adapter_astrbot's _at_me."""
    if not self_id:
        return False
    quoted_sender = _quoted_sender(quoted)
    for part in parts:
        kind = part.get("type")
        data = part.get("data") or {}
        if kind == "at" and _text(data.get("qq")) == self_id:
            return True
        if kind == "reply" and quoted_sender == self_id:
            return True
    return False


def from_onebot(payload, *, quoted=None, names=None) -> events.Incoming | None:
    """One OneBot 11 message event (array format) as an Incoming; None for anything else.

    quoted: the data of get_msg for the first quoted message, when the caller fetched it;
    names:  {qq: name} for @ segments, when the caller knows them.
    Pure: no I/O, no logging; never raises."""
    if not isinstance(payload, dict):
        return None
    if payload.get("post_type") not in ("message", "message_sent"):
        return None
    if payload.get("message_type") not in ("group", "private"):
        return None
    if not isinstance(payload.get("message"), list):
        return None
    place = _place(payload)
    sender_id = _sender_id(payload)
    self_id = _text(payload.get("self_id"))
    parts = _parts(payload)
    return events.Incoming(
        place=place,
        sender_id=sender_id,
        sender_name=_sender_name(payload),
        self_id=self_id,
        message_id=_text(payload.get("message_id")),
        segments=_segments(parts, self_id, quoted, names),
        at_me=_at_me(parts, self_id, quoted),
        reply_to=_reply_to(parts),
        image_refs=_image_refs(parts),
        is_private=place.startswith("private:"),
        is_self=bool(sender_id) and sender_id == self_id,
        ts=time.time(),
    )
