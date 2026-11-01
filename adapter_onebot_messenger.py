# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""``messenger.Messenger`` over NapCat (OneBot 11), sending the way AstrBot 4.29.3 does.

``send`` turns the segments into OneBot 11 message segments and calls ``send_group_msg`` or
``send_private_msg``; ``call`` asks for one of ``messenger.ALLOWED_ACTIONS`` and answers its
``data``, as aiocqhttp's ``call_action`` does. The connection itself is not here: one
``call_api(action, params) -> dict`` is passed in (later 2b's ``Calls.call``).

What NapCat receives is what AstrBot 4.29.3 sends today: a local picture or voice is read and
sent as base64, never as a local path. One check AstrBot does not have is added here: a local
file may only come from ``roots``, her own folders, so a wrong path cannot send another file of
the computer.
"""
from __future__ import annotations

import base64
import ipaddress
import os
import socket
from pathlib import Path
from urllib.parse import urlsplit

try:
    from . import browse, messenger
except ImportError:
    import browse
    import messenger

MAX_FILE_BYTES = 20 * 1024 * 1024   # one picture or voice she sends
_PREFIX = "base64://"
_DIGITS = frozenset("0123456789")   # a group id and a user id are made of these only
_SEND_ACTION = {"group": "send_group_msg", "private": "send_private_msg"}
_SEND_KEY = {"group": "group_id", "private": "user_id"}


class ActionFailed(RuntimeError):
    """NapCat answered a call with a failure (status is not "ok")."""

    def __init__(self, action, retcode):
        self.action = action
        self.retcode = retcode
        super().__init__("%s failed with retcode %s" % (action, retcode))


def _inside(path, root) -> bool:
    """Whether one resolved path is inside one resolved root (drive and case ignored on Windows)."""
    try:
        relative = os.path.relpath(os.path.normcase(str(path)), os.path.normcase(str(root)))
    except ValueError:   # another drive has no relative path
        return False
    return relative != "." and relative != ".." and not relative.startswith(".." + os.sep)


def _file_ref(path, roots) -> str:
    """The "base64://" reference of one local file, if she may send it; ValueError otherwise."""
    try:
        target = Path(str(path)).resolve()
        allowed = any(_inside(target, Path(str(root)).resolve()) for root in roots or ())
    except (OSError, ValueError) as error:
        raise ValueError("cannot read this path: %r" % (path,)) from error
    if not allowed:
        raise ValueError("this path is not inside her folders: %r" % (path,))
    try:
        if not target.is_file():
            raise ValueError("this path is not a file: %r" % (path,))
        if target.stat().st_size > MAX_FILE_BYTES:
            raise ValueError("this file is too big to send: %r" % (path,))
        payload = target.read_bytes()
    except OSError as error:
        raise ValueError("cannot read this file: %r" % (path,)) from error
    return _PREFIX + base64.b64encode(payload).decode("ascii")


def resolve_host(host):
    """Resolve a host to addresses for a URL image."""
    return [item[4][0] for item in socket.getaddrinfo(host, None)]


def _public_image_url(url) -> bool:
    if not browse.check_url(url)[0]:
        return False
    try:
        addresses = list(resolve_host(urlsplit(url).hostname))
        if not addresses:
            return False
        for address in addresses:
            ip = ipaddress.ip_address(address.split("%", 1)[0])
            if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
                ip = ip.ipv4_mapped
            if not ip.is_global or ip.is_multicast:
                return False
        return True
    except Exception:
        return False


def _image_ref(data, roots) -> str:
    """The image's OneBot reference: base64 for a local file or given data, the url for a url."""
    if "path" in data:
        return _file_ref(data["path"], roots)
    if "base64" in data:
        given = str(data["base64"])
        return given if given.startswith(_PREFIX) else _PREFIX + given
    url = str(data["url"])
    if not _public_image_url(url):
        raise ValueError("image url is not public")
    return url


def _safe_message(message) -> bool:
    """Allow only simple segments and base64 media in raw send actions."""
    if not isinstance(message, list):
        return False
    for part in message:
        if not isinstance(part, dict) or part.get("type") not in ("text", "face", "image", "record"):
            return False
        data = part.get("data")
        if not isinstance(data, dict):
            return False
        if part["type"] in ("image", "record"):
            file = data.get("file")
            if not isinstance(file, str) or not file.startswith(_PREFIX):
                return False
    return True


def to_onebot(segments, roots) -> list:
    """OneBot 11 message segments for sendable segments (messenger.check_segments first)."""
    out = []
    for segment in messenger.check_segments(segments):
        kind, data = segment.type, segment.data
        if kind == "text":
            out.append({"type": "text", "data": {"text": str(data["text"])}})
        elif kind == "face":
            out.append({"type": "face", "data": {"id": str(data["id"])}})
        elif kind == "image":
            out.append({"type": "image", "data": {"file": _image_ref(data, roots)}})
        else:
            out.append({"type": "record", "data": {"file": _file_ref(data["path"], roots)}})
    return out


def _target(place):
    """A place as (kind, number): group or private, and its digits; None for anything else."""
    text = place if isinstance(place, str) else ""
    kind, sep, number = text.partition(":")
    if sep and kind in _SEND_ACTION and number and all(char in _DIGITS for char in number):
        return kind, int(number)
    return None


class OneBotMessenger(messenger.Messenger):
    """Messenger over NapCat: one API call, and her own folders for local files.

    ``call_api(action, params) -> dict`` is one API call answering the whole frame
    (``{"status", "retcode", "data", ...}``); ``roots`` are the folders a local file may come
    from (later her data folder). With no roots no local path is accepted.
    """

    def __init__(self, call_api, *, roots=()):
        self.call_api = call_api
        self.roots = tuple(roots or ())

    async def send(self, place: str, segments: tuple) -> messenger.Sent:
        """The whole message in one place, or nothing at all."""
        target = _target(place)
        if target is None:
            return messenger.Sent(False, "")
        message = to_onebot(segments, self.roots)
        if not message:
            return messenger.Sent(False, "")
        kind, number = target
        frame = await self.call_api(_SEND_ACTION[kind],
                                    {_SEND_KEY[kind]: number, "message": message})
        frame = frame if isinstance(frame, dict) else {}
        if frame.get("status") != "ok":
            return messenger.Sent(False, "")
        data = frame.get("data")
        message_id = data.get("message_id") if isinstance(data, dict) else None
        return messenger.Sent(True, "" if message_id is None else str(message_id))

    async def call(self, action: str, **params) -> dict:
        """One allowed action with these parameters; its data, or ActionFailed."""
        if action not in messenger.ALLOWED_ACTIONS:
            raise messenger.ActionRefused(action)
        if action in _SEND_ACTION.values() and not _safe_message(params.get("message")):
            raise messenger.ActionRefused(action)
        frame = await self.call_api(action, dict(params))
        frame = frame if isinstance(frame, dict) else {}
        if frame.get("status") != "ok":
            raise ActionFailed(action, frame.get("retcode"))
        data = frame.get("data")
        return data if isinstance(data, dict) else {}
