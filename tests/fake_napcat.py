# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""A fake NapCat for tests: one OneBot 11 client that sends events and answers the server's calls.

It connects to 2d's ``OneBotServer`` on this machine, sends the events a test builds, and
answers every ``{action, params, echo}`` frame the server sends back. Each call is recorded in
``calls``; ``send_group_msg`` and ``send_private_msg`` are also recorded in ``sent`` and get a
message id from 1 up; ``get_msg`` finds a message it sent out; ``fetch_ptt_text`` answers QQ's
words for a voice (one string field, ``text``); ``get_forward_msg`` and any other action answer
``failed``. ``answer`` scripts the answers to one action: they are used once each, in order.
aiohttp is imported when the connection opens, so the message builders work without it. Nothing
here touches a real account or a real message.
"""
from __future__ import annotations

import asyncio
import json
from collections import deque
from urllib.parse import urlsplit

SEND_ACTIONS = ("send_group_msg", "send_private_msg")
FAILED = {"status": "failed", "retcode": 1404, "data": None}
PTT_TEXT = "明天几点出门"   # made up: QQ's own words for a voice


def _number(value):
    """An id as NapCat sends it: a number when it looks like one, else the value itself."""
    text = str(value)
    return int(text) if text.isdigit() else value


def _id_text(value) -> str:
    """A message id as a lookup key, so the same number written either way is the same."""
    return "" if value is None else str(value).strip()


class FakeNapCat:
    """One fake NapCat client: connect, send events, answer the server's calls."""

    def __init__(self, *, url, token, self_id="20002"):
        parts = urlsplit(str(url))
        if parts.hostname != "127.0.0.1":
            raise ValueError("a fake NapCat connects to 127.0.0.1 only: %r" % (url,))
        self.url = str(url)
        self.token = str(token)
        self.self_id = str(self_id)
        self.sent = []       # the params of every send_group_msg/send_private_msg, in order
        self.calls = []      # (action, params) of every call the server made, in order
        self.error = None    # the error that ended the receive loop, if one did
        self._scripted = {}  # action -> the answers to use first, in order
        self._known = {}     # message id -> the message event, for get_msg
        self._next_sent_id = 1        # the message ids the sends get, from 1 up
        self._next_made_up_id = 800001   # the ids of the events a test sends
        self._session = None
        self._ws = None
        self._reader = None

    def answer(self, action, data=None, status="ok", retcode=0):
        """Script the next answer to one action; it is used once, and in order."""
        self._scripted.setdefault(str(action), deque()).append(
            {"status": status, "retcode": retcode, "data": data})

    async def __aenter__(self):
        """Connect with the headers NapCat sends, and start answering calls in the background."""
        import aiohttp
        headers = {"Authorization": "Bearer " + self.token,
                   "X-Self-ID": self.self_id,
                   "X-Client-Role": "Universal"}
        session = aiohttp.ClientSession()
        try:
            ws = await session.ws_connect(self.url, headers=headers)
        except BaseException:
            await session.close()
            raise
        self._session, self._ws = session, ws
        self._reader = asyncio.create_task(self._read())
        return self

    async def __aexit__(self, *exc):
        """Stop answering, close the socket, and close the session."""
        reader, self._reader = self._reader, None
        if reader is not None:
            reader.cancel()
            try:
                await reader
            except asyncio.CancelledError:
                pass
            except Exception as error:   # a socket closing under the reader is not a failure
                self.error = error
        ws, self._ws = self._ws, None
        if ws is not None:
            await ws.close()
        session, self._session = self._session, None
        if session is not None:
            await session.close()
        return False

    async def send_event(self, payload):
        """Send one event frame; a message event is remembered, so get_msg can find it."""
        if self._ws is None:
            raise RuntimeError("the fake NapCat is not connected")
        self._know(payload)
        await self._ws.send_json(payload)

    def group_message(self, *, group, user, text="", message_id=None, at_me=False,
                      reply_to=None, images=(), name="", card="") -> dict:
        """One OneBot 11 group message event, in array format."""
        return self._message("group", user=user, group=group, text=text, message_id=message_id,
                             at_me=at_me, reply_to=reply_to, images=images, name=name, card=card)

    def private_message(self, *, user, text="", message_id=None, images=(), name="") -> dict:
        """One OneBot 11 private message event, in array format."""
        return self._message("private", user=user, text=text, message_id=message_id,
                             images=images, name=name)

    async def _read(self):
        """Record and answer every call until the socket closes; cancelled on the way out."""
        import aiohttp
        try:
            async for message in self._ws:
                if message.type != aiohttp.WSMsgType.TEXT:
                    continue
                try:
                    frame = json.loads(message.data)
                except ValueError:
                    continue
                if not isinstance(frame, dict) or "action" not in frame:
                    continue
                action = str(frame.get("action"))
                params = frame.get("params")
                params = dict(params) if isinstance(params, dict) else {}
                self.calls.append((action, params))
                answer = self._answer(action, params)
                answer["echo"] = frame.get("echo")
                await self._ws.send_json(answer)
        except asyncio.CancelledError:
            raise
        except Exception as error:   # the connection closing is not a test failure
            self.error = error

    def _answer(self, action, params) -> dict:
        """The frame to answer one call with: a scripted one first, else that action's default."""
        if action in SEND_ACTIONS:
            self.sent.append(params)
        scripted = self._scripted.get(action)
        if scripted:
            return dict(scripted.popleft())
        if action in SEND_ACTIONS:
            message_id = self._next_sent_id
            self._next_sent_id += 1
            self._know(self._sent_event(action, params, message_id))
            return {"status": "ok", "retcode": 0, "data": {"message_id": message_id}}
        if action == "get_msg":
            found = self._known.get(_id_text(params.get("message_id")))
            if found is not None:
                return {"status": "ok", "retcode": 0, "data": found}
        if action == "fetch_ptt_text":
            # NapCat's return schema for QQ's own speech-to-text: one field, the words.
            if _id_text(params.get("message_id")):
                return {"status": "ok", "retcode": 0, "data": {"text": PTT_TEXT}}
        return dict(FAILED)

    def _sent_event(self, action, params, message_id) -> dict:
        """The event of one message the server asked her to send, as get_msg gives it back."""
        group = action == "send_group_msg"
        event = {"post_type": "message_sent",
                 "message_type": "group" if group else "private",
                 "self_id": _number(self.self_id),
                 "user_id": _number(self.self_id) if group else params.get("user_id"),
                 "message_id": message_id,
                 "sender": {"user_id": _number(self.self_id), "nickname": "", "card": ""},
                 "message": list(params.get("message") or ())}
        if group:
            event["group_id"] = params.get("group_id")
        return event

    def _know(self, payload) -> None:
        """Remember one outgoing message event by its id, so get_msg can find it."""
        if not isinstance(payload, dict):
            return
        if payload.get("post_type") not in ("message", "message_sent"):
            return
        message_id = _id_text(payload.get("message_id"))
        if message_id:
            self._known[message_id] = payload

    def _message(self, kind, *, user, group=None, text="", message_id=None, at_me=False,
                 reply_to=None, images=(), name="", card="") -> dict:
        """One message event of this kind, with the segments in the order NapCat sends them."""
        if message_id is None:
            message_id = self._next_made_up_id
            self._next_made_up_id += 1
        event = {"post_type": "message", "message_type": kind, "self_id": _number(self.self_id),
                 "user_id": _number(user), "message_id": message_id,
                 "sender": {"user_id": _number(user), "nickname": str(name), "card": str(card)},
                 "message": self._segments(text=text, at_me=at_me, reply_to=reply_to,
                                           images=images)}
        if kind == "group":
            event["group_id"] = _number(group)
        return event

    def _segments(self, *, text="", at_me=False, reply_to=None, images=()) -> list:
        """The array-format message: an at of her, a reply, the words, then the images."""
        segments = []
        if at_me:
            segments.append({"type": "at", "data": {"qq": self.self_id}})
        if reply_to is not None:
            segments.append({"type": "reply", "data": {"id": str(reply_to)}})
        if text:
            segments.append({"type": "text", "data": {"text": str(text)}})
        for image in images or ():
            reference = str(image)
            segments.append({"type": "image", "data": {"url": reference, "file": reference}})
        return segments
