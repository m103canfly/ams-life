# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her stickers in the plugin (step 2, part 丙; stickers.py is the logic, this is the wiring).
Off unless stickers_enabled (and looking at pictures, image_caption, is on).

- one look at a picture answers what it shows and whether she keeps it (stickers.LOOK_PROMPT):
  at reply time in _image_context, and when someone sends a QQ sticker in a chat she was not
  called in (a task of its own, after the message is kept); one model call a picture, its money
  in the day's;
- what she keeps is fetched from QQ's picture servers only, checked by its first bytes, and
  added to one library (one instance, one add at a time);
- a reply's prompt offers a few (by mood and topic); she names one as [表情包:n] ([表情:名字] stays a
  QQ face, 甲); only an offered
  one is sent, after her words, as a QQ sticker through the adapter's own client to this
  message's chat (stickers.send_params / allowed), else once as a plain picture, else not;
- what she sent is kept in her phone and AstrBot's history as [表情包：标签];
- deleting a person deletes what he sent and the looks at his pictures.
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

    async def _look_at_sticker_in_passing(self, event) -> None:
        """A QQ sticker in a chat she was not called in: one look, kept if she likes it. A task
        of its own: the message is already kept, nothing is answered."""
        refs = self._sticker_refs(event)
        if not refs or not self._llm_allowed("image_caption"):
            return
        try:
            cfg = self._attention_cfg()
            if attention.budget(self._spent_today(), cfg["soft"], cfg["hard"]) == "hard":
                return
        except Exception:
            pass
        provider = self._vision_provider_for(event)
        if provider is None:
            return
        cache = self._load_image_cache()
        changed = False
        for ref in refs[:3]:
            key = _sha256(ref)
            if key in cache:
                continue
            try:
                caption, look = await self._look_once(provider, ref, event)
            except Exception as exc:
                logger.warning("[ams-life] stickers: a look failed: %s", type(exc).__name__)
                continue
            if caption:
                cache[key] = stickers.cache_entry(ref, look, self._speaker(event)[0], self._here(event), time.time())
                changed = True
                await self._maybe_keep(event, ref, look)
        if changed:
            self._save_image_cache(cache)

    def _sticker_in_passing(self, event) -> None:
        """on_message: start the look above for a QQ sticker (stickers on, not called)."""
        if not self._stickers_on() or not self._sticker_refs(event):
            return
        try:
            if self._job_stale():
                return   # someone (or a message) she may not keep: not even looked at
        except Exception:
            return
        try:
            if self._addresses_her(event):
                return   # the reply's own look takes it
        except Exception:
            pass
        try:
            asyncio.create_task(self._look_at_sticker_in_passing(event))
        except Exception:
            pass

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
            await self._send_sticker(event, sid, umo, place)
        return go
