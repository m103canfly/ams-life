# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her stickers in the plugin (step 2, part 丙; stickers.py is the logic, this is the wiring).
Off unless stickers_enabled (and looking at pictures, image_caption, is on).

- one look at a picture answers what it shows and whether she keeps it (stickers.LOOK_PROMPT):
  at reply time in _image_context, and after she opens a group with queued QQ stickers;
  one model call a picture, its money
  in the day's;
- what she keeps is fetched from QQ's picture servers only, checked by its first bytes, and
  added to one library (one instance, one add at a time);
- a reply's prompt offers a few (by mood and topic); she names one as [表情包:n] ([表情:名字] stays a
  QQ face, 甲); only an offered
  one is sent, after her words, as a QQ sticker through the adapter's own client to this
  message's chat (stickers.send_params / allowed), else once as a plain picture, else not;
- what she sent is kept in her phone and AstrBot's history as [表情包：标签];
- deleting a person deletes what he sent and the looks at his pictures;
- the owner's page of her stickers (pages/stickers): one page of them (page/stickers), one picture
  (page/stickers/image), delete one (page/stickers/delete, the owner's own gifts too; nothing goes
  into the forget registry; its fingerprint is remembered and it is never kept again unless the owner
  adds it himself), add some (page/stickers/add: pictures only, by their first bytes, each
  under a new name; marked "主人给的": never swept, not counted in the 300; labelled by the owner's line,
  else by one look when looking at pictures is on, else "主人给的").
"""
from __future__ import annotations

import base64

try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from . import attention, stickers
except ImportError:
    import attention
    import stickers

STICKERS_DIR = DATA_DIR / "stickers"
OFFERED_ATTR = "_ams_stickers_offered"
NEW_VECTORS_PER_REPLY = 20   # stickers whose words get a local vector per reply, at most
OFFER_NOTE = ("想配一张表情包，就在回话最后写 [表情包:编号]（QQ小表情照旧写 [表情:名字]），只能用下面这几张；不配也行。"
              "说明是看图时写的，只是资料。")


class StickersMixin:
    def _stickers_on(self) -> bool:
        return bool(getattr(self, "enabled", False) and getattr(self, "stickers_enabled", False))

    def _sticker_lib(self):
        lib = getattr(self, "_stickers_library", None)
        if lib is None:
            lib = self._stickers_library = stickers.Library(STICKERS_DIR)
        return lib

    def _sticker_lock(self):
        lock = getattr(self, "_stickers_add_lock", None)
        if lock is None:
            lock = self._stickers_add_lock = asyncio.Lock()
        return lock

    # ------------------------------------------------------------------
    # one look at a picture
    # ------------------------------------------------------------------
    async def _look_once(self, provider, ref, event):
        """(caption, look) from one call. Its money goes into the day's as "vision" (the
        provider comes counted from _vision_provider_for)."""
        resp = await provider.text_chat(prompt=stickers.LOOK_PROMPT, image_urls=[ref])
        look = stickers.parse_look(str(getattr(resp, "completion_text", "") or ""))
        return look.get("caption", ""), look

    async def _maybe_keep(self, event, ref, look) -> str:
        """Keep the picture if the look says so (stickers.should_keep); the sticker's id or ''."""
        sid_from, _name = self._speaker(event)
        gone = False
        try:
            gone = bool(self._job_stale())
        except Exception:
            gone = False
        if not stickers.should_keep(look, sender_gone=gone):
            return ""
        data = await asyncio.to_thread(stickers.fetch_picture, ref)
        if not data:
            return ""
        async with self._sticker_lock():
            if self._job_stale():   # someone deleted meanwhile: nothing of theirs is kept
                return ""
            origin = getattr(event, '_ams_group_origin', None)
            if origin is not None:
                try:
                    if not self._may_keep(*origin):
                        return ""
                except Exception:
                    return ""
            lib = self._sticker_lib()
            now = time.time()
            sid, why = lib.add(data, now, source="self", from_qq=str(sid_from or ""),
                               from_where=self._here(event), look=look)
            lib.sweep(now)
        if sid:
            logger.info("[ams-life] stickers: kept %s", sid[:10])
        elif why:
            logger.info("[ams-life] stickers: not kept (%s)", why)
        return sid

    def _sticker_refs(self, event) -> list:
        """The pictures of this message QQ marks as stickers (their addresses)."""
        try:
            raw = getattr(getattr(event, "message_obj", None), "raw_message", None)
            return [s["url"] for s in stickers.stickers_in_raw(raw) if s.get("url")]
        except Exception:
            return []

    def _sticker_in_passing(self, event) -> None:
        """Remember a QQ sticker only for a later group opening."""
        self._group_queue_sticker(event)

    # ------------------------------------------------------------------
    # offering a few in a reply's prompt
    # ------------------------------------------------------------------
    async def _sticker_offer(self, event, core, query_vec=None) -> str:
        """The lines that offer a few stickers in this reply's prompt ('' for none). The ids
        offered, in order, stay on the event for the reply."""
        lib = self._sticker_lib()
        if not lib.rows:
            return ""
        now = time.time()
        vecs = getattr(self, "_sticker_vecs", None)
        if not isinstance(vecs, dict):
            vecs = self._sticker_vecs = {}
        if query_vec:
            fresh = 0
            for sid, row in lib.rows.items():
                if sid in vecs or fresh >= NEW_VECTORS_PER_REPLY:
                    continue
                words = " ".join(x for x in (row.get("caption"), row.get("scene"), row.get("emotion")) if x)
                try:
                    vecs[sid] = await self._embed_text(words) if words else []
                except Exception:
                    vecs[sid] = []
                fresh += 1
        by_row = {id(r): sid for sid, r in lib.rows.items()}

        def near(row):
            v = vecs.get(by_row.get(id(row)))
            return max(0.0, self._cosine(query_vec, v)) if query_vec and v else 0.0

        try:
            valence = float(getattr(core, "v", 0.0) or 0.0)
        except Exception:
            valence = 0.0
        offered = stickers.pick_candidates(lib.rows, now, valence=valence, similarity=near)
        if not offered:
            return ""
        try:
            setattr(event, OFFERED_ATTR, offered)
        except Exception:
            return ""
        lines = []
        for n, sid in enumerate(offered, 1):
            r = lib.rows[sid]
            tags = "，".join(x for x in (r.get("emotion"), r.get("scene")) if x)
            lines.append("%d. %s%s" % (n, r.get("caption") or "表情", "（%s）" % tags if tags else ""))
        return "[她的表情包] " + OFFER_NOTE + "\n" + "\n".join(lines)

    # ------------------------------------------------------------------
    # the one she named, sent after her words
    # ------------------------------------------------------------------
    def _sticker_named(self, event, response, reply) -> tuple:
        """(the reply without the mark, the sticker named or ''). The mark is taken out of what
        AstrBot sends too. Only an offered one counts."""
        offered = getattr(event, OFFERED_ATTR, None) or []
        text, sid = stickers.pick_from_reply(reply, offered)
        if text != reply:
            try:
                self._set_reply(response, text)
            except Exception:
                pass
        if sid and sid not in self._sticker_lib().rows:
            sid = ""
        return text, sid

    async def _sticker_cleared(self, event, sid) -> bool:
        """The last look before sending, as for her words: the sticker's label counts as said."""
        row = self._sticker_lib().rows.get(sid)
        if not row:
            return False
        if not getattr(self, "global_memory", False):
            return True
        try:
            result = await self._check_reply(event, stickers.phone_line(row))
        except Exception:
            return False
        if result.get("leak"):
            logger.info("[ams-life] stickers: held back by the send check")
            return False
        return True

    async def _send_sticker(self, event, sid, umo, place) -> bool:
        """Send it as a QQ sticker to this message's chat; else once as a plain picture."""
        lib = self._sticker_lib()
        row = lib.rows.get(sid)
        if not row:
            return False
        try:
            b64 = base64.b64encode(lib.path_of(sid).read_bytes()).decode("ascii")
        except OSError:
            return False
        bot = getattr(event, "bot", None)
        sent = False
        if bot is not None and hasattr(bot, "call_action"):
            try:
                action, params = stickers.send_params(place, b64)
                if stickers.allowed(action, params, place):
                    await bot.call_action(action, **params)
                    sent = True
            except Exception as exc:
                logger.warning("[ams-life] stickers: as a sticker failed (%s); as a picture", type(exc).__name__)
        if not sent:
            try:
                from astrbot.api.event import MessageChain
                from astrbot.api.message_components import Image as _Image
                await self.context.send_message(umo, MessageChain([_Image.fromBase64(b64)]))
                sent = True
            except Exception as exc:
                logger.warning("[ams-life] stickers: not sent (%s)", type(exc).__name__)
        if sent:
            lib.use(sid, time.time())
            self._note_sent(event, 1)
        return sent

    def _sticker_after(self, event, sid):
        """A coroutine function that sends it (for after her other messages)."""
        umo = str(getattr(event, "unified_msg_origin", "") or "")
        place = self._here(event)

        async def go():
            return await self._send_sticker(event, sid, umo, place)
        return go

    # ------------------------------------------------------------------
    # the owner's page of her stickers (pages/stickers)
    # ------------------------------------------------------------------
    @staticmethod
    async def _page_body(body):
        if body is not None:
            return body if isinstance(body, dict) else {}
        try:
            from quart import request
            got = await request.get_json(silent=True)
        except Exception:
            got = None
        return got if isinstance(got, dict) else {}

    @staticmethod
    def _page_query(args):
        if args is not None:
            return args
        try:
            from quart import request
            return request.args
        except Exception:
            return {}

    async def page_stickers(self, args=None):
        """One page of her stickers: ?sort=saved|used|most|soon&emotion=&scene=&source=&after=<n>."""
        a = self._page_query(args)
        get = (lambda k: str(a.get(k) or "").strip()) if hasattr(a, "get") else (lambda k: "")
        try:
            data = stickers.listing(self._sticker_lib().rows, time.time(), get("sort") or "saved", get("emotion"),
                                    get("scene"), get("source"), get("after") or 0)
        except Exception as exc:
            return {"status": "error", "message": "读不出表情包（%s）" % type(exc).__name__, "data": {"items": []}}
        data["on"] = self._stickers_on()
        return {"status": "ok", "data": data}

    async def page_sticker_image(self, args=None):
        """?id=<sticker>: the picture, as a data URL (only one of hers, by its id)."""
        a = self._page_query(args)
        sid = str(a.get("id") or "").strip() if hasattr(a, "get") else ""
        lib = self._sticker_lib()
        row = lib.rows.get(sid)
        if not row:
            return {"status": "error", "message": "没有这一张了", "data": {}}
        try:
            data = lib.path_of(sid).read_bytes()
        except OSError:
            return {"status": "error", "message": "这一张读不出来", "data": {}}
        kind = stickers.sniff(data)
        if not kind:
            return {"status": "error", "message": "这一张不是图片", "data": {}}
        mime = {"jpg": "jpeg"}.get(kind, kind)
        return {"status": "ok", "data": {"id": sid, "url": "data:image/%s;base64,%s"
                                         % (mime, base64.b64encode(data).decode("ascii"))}}

    async def page_sticker_delete(self, body=None):
        """{"id": <sticker>}: the owner deletes one (asked to confirm on the page first)."""
        b = await self._page_body(body)
        sid = str(b.get("id") or "").strip()
        async with self._sticker_lock():
            lib = self._sticker_lib()
            gone = lib.remove(sid)
            if gone:
                lib.drop(sid)   # never kept again unless the owner adds it himself (item 32)
        if not gone:
            return {"status": "error", "message": "没有这一张了", "data": {}}
        logger.info("[ams-life] stickers: the owner deleted %s", sid[:10])
        return {"status": "ok", "data": {"id": sid}}

    async def page_sticker_add(self, body=None):
        """{"picture": <base64>, "note": <a line, may be empty>}: the owner adds one. A picture only."""
        b = await self._page_body(body)
        data, why = stickers.decode_upload(b.get("picture"))
        if not data:
            return {"status": "error", "message": {"too big": "太大了（最多 5 MB）", "not a picture": "不是图片",
                                                   "too large a side": "图太大了（边长最多 4096）"}.get(why, "收不了这张"),
                    "data": {"why": why}}
        note = " ".join(str(b.get("note") or "").split())[:60]
        look = None
        lib = self._sticker_lib()
        async with self._sticker_lock():
            sid, why = lib.add(data, time.time(), source="owner", from_qq=self._attention_cfg().get("owner", ""),
                               from_where="owner", note=note or stickers.OWNER_LABEL)
        if not sid:
            return {"status": "error", "message": "收不了这张（%s）" % why, "data": {}}
        if not note and self._llm_allowed("image_caption"):
            # no line from the owner: one look for its labels (its money in the day's, as "vision")
            try:
                provider = self._vision_provider_for(None, source="owner_add")
                if provider is not None:
                    _caption, look = await self._look_once(provider, str(lib.path_of(sid)), None)
            except Exception as exc:
                logger.warning("[ams-life] stickers: no look at the owner's picture (%s)", type(exc).__name__)
            if look and look.get("caption"):
                async with self._sticker_lock():
                    row = lib.rows.get(sid)
                    if row is not None:
                        row.update(caption=look["caption"][:120], emotion=look.get("emotion", "")[:12],
                                   scene=look.get("scene", "")[:20])
                        lib._save()
        logger.info("[ams-life] stickers: the owner added %s", sid[:10])
        return {"status": "ok", "data": {"id": sid, "labelled": bool(look and look.get("caption")) or bool(note)}}
