# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The half of the NapCat (OneBot 11) connection that needs no aiohttp.

``check_handshake`` says whether one connection attempt may come in; ``self_id_of`` reads the
account NapCat reports; ``parse_frame`` reads one text frame; ``kind_of`` says whether a frame is
an event or the answer to a call; ``Calls`` keeps the calls that wait for an answer, pairs an
answer by its ``echo``, and closes cleanly. Opening the socket itself comes later, with aiohttp;
nothing here opens one.
"""
from __future__ import annotations

import asyncio
import hmac
import ipaddress
import json
import secrets

MAX_FRAME_BYTES = 16 * 1024 * 1024   # one frame; base64 pictures make frames big
CALL_SECONDS = 30                    # how long one call waits for its answer


def _text(value) -> str:
    """A value as a string; anything unreadable is ""."""
    try:
        return "" if value is None else str(value)
    except Exception:
        return ""


def _lower(headers) -> dict:
    """The headers with lower-case names, so a lookup ignores case."""
    items = headers.items() if hasattr(headers, "items") else headers
    out = {}
    try:
        for name, value in items or ():
            out[_text(name).lower()] = value
    except (TypeError, ValueError):
        return out
    return out


def _is_local(peer) -> bool:
    """Whether an address is this machine's; an IPv4-mapped IPv6 address is read as its IPv4."""
    if isinstance(peer, (tuple, list)):
        if not peer:
            return False
        peer = peer[0]
    try:
        address = ipaddress.ip_address(peer)
    except (TypeError, ValueError):
        return False
    mapped = getattr(address, "ipv4_mapped", None)
    if mapped is not None:
        address = mapped
    return address.is_loopback


def _authorized(value, token) -> bool:
    """Whether an Authorization value is "<Bearer|Token> <the token>"; the scheme ignores case."""
    parts = _text(value).strip().split(None, 1)
    if len(parts) != 2:
        return False
    scheme, given = parts
    if scheme.lower() not in ("bearer", "token"):
        return False
    try:
        return hmac.compare_digest(given.encode("utf-8"), _text(token).encode("utf-8"))
    except Exception:
        return False


def check_handshake(headers, *, token, peer, port) -> tuple:
    """(ok, reason) for one connection attempt. reason is a short word, never a header value."""
    found = _lower(headers)
    if not token:
        return (False, "no token")
    if not _is_local(peer):
        return (False, "not local")
    host = _text(found.get("host"))
    if host not in ("127.0.0.1:%s" % port, "localhost:%s" % port, "[::1]:%s" % port):
        return (False, "host")
    if "origin" in found:
        return (False, "origin")
    if not _authorized(found.get("authorization"), token):
        return (False, "token")
    role = found.get("x-client-role")
    if role is not None and _text(role).lower() != "universal":
        return (False, "role")
    return (True, "")


def self_id_of(headers) -> str:
    """The X-Self-ID header when it is all digits, else ""."""
    text = _text(_lower(headers).get("x-self-id"))
    return text if text.isdigit() else ""


def parse_frame(raw) -> dict | None:
    """One text frame (str or bytes) as a dict; None when too big, not JSON, or not an object."""
    if isinstance(raw, (bytes, bytearray, memoryview)):
        data = bytes(raw)
        if len(data) > MAX_FRAME_BYTES:
            return None
    elif isinstance(raw, str):
        if len(raw) > MAX_FRAME_BYTES:
            return None
        try:
            data = raw.encode("utf-8")
        except Exception:
            return None
        if len(data) > MAX_FRAME_BYTES:
            return None
    else:
        return None
    try:
        frame = json.loads(data)
    except Exception:
        return None
    return frame if isinstance(frame, dict) else None


def kind_of(frame) -> str:
    """'response' when it has 'echo' and ('status' or 'retcode'); 'event' when it has 'post_type'; else ''."""
    if not isinstance(frame, dict):
        return ""
    if "echo" in frame and ("status" in frame or "retcode" in frame):
        return "response"
    if "post_type" in frame:
        return "event"
    return ""


class Calls:
    """The calls that wait for an answer, paired with it by the frame's ``echo``."""

    def __init__(self, send_frame, *, seconds=CALL_SECONDS):
        self.send_frame = send_frame
        self.seconds = seconds
        self._waiting = {}   # echo -> the future the call waits on
        self._closed = False

    def _new_echo(self) -> str:
        """An echo nobody is waiting for, so two calls never share one."""
        echo = secrets.token_hex(8)
        while echo in self._waiting:
            echo = secrets.token_hex(8)
        return echo

    async def call(self, action, params) -> dict:
        """Send one action and wait for its answer; the whole answering frame is given back.

        No answer within ``seconds`` raises asyncio.TimeoutError. After ``close()``, or when
        ``close()`` arrives while waiting, ConnectionError. However this ends, the echo is taken
        out of the waiting table."""
        if self._closed:
            raise ConnectionError("the link is closed")
        echo = self._new_echo()
        future = asyncio.get_running_loop().create_future()
        self._waiting[echo] = future
        try:
            await self.send_frame({"action": action, "params": dict(params), "echo": echo})
            done, _ = await asyncio.wait({future}, timeout=self.seconds)
            if not done:
                raise asyncio.TimeoutError("no answer in time")
            return future.result()
        finally:
            self._waiting.pop(echo, None)

    def settle(self, frame) -> bool:
        """Give one answering frame to the call that waits for its echo; False when nobody waits."""
        if not isinstance(frame, dict):
            return False
        try:
            future = self._waiting.pop(frame.get("echo"), None)
        except TypeError:   # an echo that cannot be a key is nobody's
            return False
        if future is None:
            return False
        future.set_result(frame)
        return True

    def close(self) -> None:
        """Fail every call that still waits, and refuse the calls after this one."""
        self._closed = True
        waiting, self._waiting = self._waiting, {}
        for future in waiting.values():
            if not future.done():
                future.set_exception(ConnectionError("the link is closed"))
