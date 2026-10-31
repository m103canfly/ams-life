# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Where everything she sends goes through, apart from the bot framework.

``Messenger.send`` puts one message in one place; ``Messenger.call`` asks the platform for one
of ``ALLOWED_ACTIONS``. The future QQ layer implements the same two methods; the adapter module
in this repository implements them over the bot framework today. This module holds the rules
only: it imports nothing from the framework.

A message is a tuple of ``events.Segment``. Only the four types in ``SEND_TYPES`` are sendable
(``check_segments``); the words and QQ faces she picks come from ``attention.pieces``
(``text_segments``).
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    from . import attention
    from . import events
except ImportError:
    import attention
    import events

# The platform actions she may ask for, and nothing else.
# fetch_ptt_text reads only: QQ's own speech-to-text for one voice.
ALLOWED_ACTIONS = frozenset(("get_msg", "get_forward_msg", "send_group_msg", "send_private_msg", "fetch_ptt_text"))
# What a message she sends may be made of.
SEND_TYPES = ("text", "face", "image", "record")
_IMAGE_KEYS = ("path", "base64", "url")   # an image takes exactly one of these
_URL_PREFIXES = ("http://", "https://")


class ActionRefused(PermissionError):
    """An action that is not in ALLOWED_ACTIONS."""


@dataclass(frozen=True)
class Sent:
    """What came of one send: whether it went, and the platform's message id."""

    ok: bool
    message_id: str   # "" when the platform does not say


class Messenger:
    """Where everything she sends goes through. Subclasses implement both methods."""

    async def send(self, place: str, segments: tuple) -> Sent:
        raise NotImplementedError

    async def call(self, action: str, **params) -> dict:
        raise NotImplementedError


def _value(data, key) -> str:
    """One field as a string; missing or None is ""."""
    value = data.get(key, "")
    return "" if value is None else str(value)


def _check_text(data) -> None:
    if not _value(data, "text").strip():
        raise ValueError("text segment: the words are empty")


def _check_face(data) -> None:
    if not _value(data, "id").strip():
        raise ValueError("face segment: the id is empty")


def _check_image(data) -> None:
    """Exactly one of path, base64, url; a url must be http or https."""
    given = [key for key in _IMAGE_KEYS if key in data]
    if len(given) != 1:
        raise ValueError("image segment: exactly one of path, base64, url")
    key = given[0]
    value = _value(data, key).strip()
    if not value:
        raise ValueError("image segment: the %s is empty" % key)
    if key == "url" and not value.lower().startswith(_URL_PREFIXES):
        raise ValueError("image segment: the url is not http or https")


def _check_record(data) -> None:
    if not _value(data, "path").strip():
        raise ValueError("record segment: the path is empty")


_CHECKS = {"text": _check_text, "face": _check_face, "image": _check_image, "record": _check_record}


def check_segments(segments) -> tuple:
    """The segments as a tuple if every one is sendable, else ValueError."""
    out = tuple(segments or ())
    for seg in out:
        kind = getattr(seg, "type", None)
        data = getattr(seg, "data", None)
        if not isinstance(kind, str) or not isinstance(data, dict):
            raise ValueError("not a sendable segment")
        check = _CHECKS.get(kind)
        if check is None:
            raise ValueError("cannot send a %s segment" % kind)
        check(data)
    return out


def text_segments(text) -> tuple:
    """One message of words and QQ faces, as attention.pieces splits it."""
    out = []
    for kind, value in attention.pieces(text):
        if kind == "face":
            out.append(events.Segment(type="face", data={"id": value}))
        else:
            out.append(events.Segment(type="text", data={"text": value}))
    return tuple(out)
