# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Build an ``events.Incoming`` from an AstrBot event, field by field as the plugin does today.

``from_astrbot`` is pure and forgiving: it never changes the event, writes nothing, logs
nothing and calls no plugin method (``_message_text`` has side effects, so it is not used).
A field that cannot be read becomes "" / False / an empty tuple. Components are told apart
by class name, so this module imports no AstrBot.
"""
from __future__ import annotations

import time

try:
    from . import discretion
except ImportError:
    import discretion
try:
    from . import events
except ImportError:
    import events


# The component classes the plugin knows, and the segment each one becomes.
_SEGMENT_OF = {"Plain": "text", "At": "at", "Reply": "reply", "Image": "image",
               "Face": "face", "Record": "record", "Forward": "forward"}
_REPLY_ID_CHARS = 80   # as PhoneMixin._reply_to


def _text(value) -> str:
    """A field as a string; anything unreadable is ""."""
    try:
        return str(value or "")
    except Exception:
        return ""


def _attr(obj, name) -> str:
    """One attribute as a string; missing or unreadable is ""."""
    try:
        return _text(getattr(obj, name, "") or "")
    except Exception:
        return ""


def _message_attr(event, name) -> str:
    """An attribute of event.message_obj as a string; no message_obj or unreadable is ""."""
    try:
        return _attr(getattr(event, "message_obj", None), name)
    except Exception:
        return ""


def _components(event) -> list:
    """The message's parts, in order; unreadable is an empty list."""
    try:
        return list(event.get_messages() or [])
    except Exception:
        return []


def _place(event) -> str:
    """What mixin_memory._here gives: discretion.place_of(event.unified_msg_origin)."""
    try:
        return discretion.place_of(getattr(event, "unified_msg_origin", "") or "")
    except Exception:
        return ""


def _speaker(event) -> tuple:
    """What mixin_settings._speaker gives: (sender id, sender name), "" when unknown."""
    sid, name = "", ""
    try:
        fn = getattr(event, "get_sender_id", None)
        if callable(fn):
            sid = _text(fn())
    except Exception:
        pass
    try:
        fn = getattr(event, "get_sender_name", None)
        if callable(fn):
            name = _text(fn())
    except Exception:
        pass
    try:
        obj = getattr(event, "message_obj", None)
        sender = getattr(obj, "sender", None) if obj is not None else None
        if sender is not None:
            if not sid:
                sid = _text(getattr(sender, "user_id", ""))
            if not name:
                name = _text(getattr(sender, "nickname", ""))
    except Exception:
        pass
    return sid, name


def _at_me(event) -> bool:
    """What mixin_phone._addresses_her gives: an @ of her own id, a quote of her own
    message, or the platform's wake check. Unreadable is False, the plugin's answer too."""
    try:
        self_id = _text(getattr(getattr(event, "message_obj", None), "self_id", "") or "")
        if self_id:
            for comp in event.get_messages() or []:
                kind = type(comp).__name__
                if kind == "At" and _text(getattr(comp, "qq", "") or "") == self_id:
                    return True
                if kind == "Reply" and _text(getattr(comp, "sender_id", "") or "") == self_id:
                    return True
        return bool(getattr(event, "is_at_or_wake_command", False))
    except Exception:
        return False


def _reply_to(components) -> str:
    """What mixin_phone._reply_to gives: the first Reply's id, cut to 80 characters."""
    for comp in components:
        try:
            if type(comp).__name__ == "Reply":
                return _text(getattr(comp, "id", "") or "")[:_REPLY_ID_CHARS]
        except Exception:
            continue
    return ""


def _image_ref(comp) -> str:
    """What mixin_media._image_ref gives: url, else file, else path, stripped."""
    try:
        return str(getattr(comp, "url", "") or getattr(comp, "file", "")
                   or getattr(comp, "path", "") or "").strip()
    except Exception:
        return ""


def _image_refs(components) -> tuple:
    """The ref of every Image in this message, in order; images inside a quote are not here."""
    return tuple(_image_ref(comp) for comp in components if type(comp).__name__ == "Image")


def _segment_data(kind, comp) -> dict:
    """The OneBot-like fields of one component, as the table in events.py says."""
    if kind == "Plain":
        return {"text": _attr(comp, "text")}
    if kind == "At":
        return {"qq": _attr(comp, "qq"), "name": _attr(comp, "name")}
    if kind == "Reply":
        return {"id": _attr(comp, "id"), "sender_id": _attr(comp, "sender_id")}
    if kind in ("Image", "Record"):
        return {"url": _attr(comp, "url"), "file": _attr(comp, "file")}
    if kind in ("Face", "Forward"):
        return {"id": _attr(comp, "id")}
    return {"kind": type(comp).__name__}


def _segments(components) -> tuple:
    """One Segment per component, in order; a part that cannot be read is left out."""
    out = []
    for comp in components:
        try:
            kind = type(comp).__name__
            out.append(events.Segment(type=_SEGMENT_OF.get(kind, "other"),
                                      data=_segment_data(kind, comp)))
        except Exception:
            continue
    return tuple(out)


def from_astrbot(event) -> events.Incoming:
    """One Incoming from one AstrBot event. Pure; never raises for an unreadable event."""
    components = _components(event)
    place = _place(event)
    sender_id, sender_name = _speaker(event)
    self_id = _message_attr(event, "self_id")
    return events.Incoming(
        place=place,
        sender_id=sender_id,
        sender_name=sender_name,
        self_id=self_id,
        message_id=_message_attr(event, "message_id"),
        segments=_segments(components),
        at_me=_at_me(event),
        reply_to=_reply_to(components),
        image_refs=_image_refs(components),
        is_private=place.startswith("private:"),
        is_self=bool(sender_id) and sender_id == self_id,
        ts=time.time(),
    )
