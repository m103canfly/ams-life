# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""ams-life: her phone.

Three layers, after "she has a phone of her own":

- phone: every group and every private chat is one window. Everything said
  there (everyone's messages, woken or not, her replies) and the open loops
  are kept only in that window, one file per window under PHONE_DIR. Wherever
  she is, she only sees that window. What others said is kept for
  WINDOW_OTHERS_SECONDS only; each window holds at most WINDOW_MAX lines.
- body: moods and drives only; it keeps no text at all (see body.py).
- memory: what she keeps, each item with an origin (mixin_memory, discretion).

Every line and loop in a window carries an origin like a memory does, so
forgetting finds them the same way.
"""
from __future__ import annotations
import hashlib
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403

WINDOW_MAX = 200                    # lines per window, everyone's
WINDOW_OWN_MAX = 80                 # her own replies per window (as core.history kept before)
WINDOW_OTHERS_SECONDS = 6 * 3600    # what others said stays 6 hours
WINDOW_LINE_CHARS = 80              # her reply lines
WINDOW_MESSAGE_CHARS = 300          # others' messages
# What non-text parts of a message become in the window (no files are kept).
_PART_NAMES = {"Image": "[图片]", "Face": "[表情]", "Record": "[语音]", "Video": "[视频]",
               "File": "[文件]", "Forward": "[聊天记录]", "Node": "[聊天记录]", "Nodes": "[聊天记录]",
               "Poke": "[戳一戳]", "Json": "[卡片]", "Share": "[分享]", "Location": "[位置]",
               "Music": "[音乐]", "Dice": "[骰子]", "RPS": "[猜拳]", "Contact": "[名片]"}
# Body fields of older state files that held text; they never come back into the body.
_OLD_BODY_TEXT_KEYS = ("open_loops", "event_anchors", "autobiography", "self_timeline",
                       "core_self", "narrative_self")


class PhoneMixin:
    # ------------------------------------------------------------------
    # Windows on disk: a readable prefix plus a hash of the full window name,
    # and the file says which window it is (checked on every read).
    # ------------------------------------------------------------------
    @staticmethod
    def _window_file(place):
        place = str(place)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in place)[:60]
        digest = hashlib.sha1(place.encode("utf-8")).hexdigest()[:12]
        return PHONE_DIR / ("%s-%s.json" % (safe, digest))

    def _read_window(self, place) -> dict:
        win = {}
        try:
            path = self._window_file(place)
            if path.exists():
                win = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            win = {}
        if not isinstance(win, dict) or str(win.get("place") or "") != str(place):
            win = {}  # not this window's file: start empty rather than read another chat
        win["place"] = str(place)
        for key in ("recent", "open_loops"):
            if not isinstance(win.get(key), list):
                win[key] = []
        win["recent"] = self._window_pruned(win["recent"])
        return win

    def _write_window(self, place, win) -> None:
        PHONE_DIR.mkdir(parents=True, exist_ok=True)
        path = self._window_file(place)
        win["place"] = str(place)
        win["recent"] = self._window_pruned(win.get("recent") or [])
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(win, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(str(tmp), str(path))

    @staticmethod
    def _window_pruned(lines, now=None) -> list:
        """Others' messages older than WINDOW_OTHERS_SECONDS go; her replies keep the last
        WINDOW_OWN_MAX; the window keeps the last WINDOW_MAX lines."""
        now = time.time() if now is None else now
        lines = [x for x in (lines or []) if isinstance(x, dict)]
        own = [x for x in lines if x.get("role") == "assistant"][-WINDOW_OWN_MAX:]
        own_ids = {id(x) for x in own}
        kept = []
        for x in lines:
            if x.get("role") == "assistant":
                if id(x) in own_ids:
                    kept.append(x)
            elif now - float(x.get("ts", 0) or 0) <= WINDOW_OTHERS_SECONDS:
                kept.append(x)
        return kept[-WINDOW_MAX:]

    def _window_places(self) -> list:
        out = []
        if PHONE_DIR.exists():
            for path in sorted(PHONE_DIR.glob("*.json")):
                try:
                    place = str(json.loads(path.read_text(encoding="utf-8")).get("place") or "")
                except Exception:
                    place = ""
                if place and self._window_file(place) == path:
                    out.append(place)
        return out

    def _event_origin(self, event) -> dict:
        try:
            sid, _name = self._speaker(event)
        except Exception:
            sid = ""
        try:
            refs = self._message_refs(event)
        except Exception:
            refs = []
        return discretion.make_origin(self._here(event), [sid], refs)

    @staticmethod
    def _message_id(event) -> str:
        try:
            return str(getattr(getattr(event, "message_obj", None), "message_id", "") or "")
        except Exception:
            return ""

    @staticmethod
    def _message_text(event) -> str:
        """The message as text; pictures, stickers and the like become a short placeholder."""
        parts = []
        try:
            for comp in event.get_messages() or []:
                kind = type(comp).__name__
                if kind == "Plain":
                    parts.append(str(getattr(comp, "text", "") or ""))
                elif kind == "At":
                    parts.append("@" + str(getattr(comp, "name", "") or getattr(comp, "qq", "") or ""))
                elif kind == "AtAll":
                    parts.append("@全体成员")
                elif kind == "Reply":
                    continue
                else:
                    parts.append(_PART_NAMES.get(kind, "[消息]"))
        except Exception:
            parts = []
        text = "".join(parts).strip()
        if not text:
            text = str(getattr(event, "message_str", "") or "").strip()
        return text

    # ------------------------------------------------------------------
    # Everyone's messages, and her replies, in their own window
    # ------------------------------------------------------------------
    def _window_add_message(self, event) -> None:
        """Store one incoming message in its window. Nothing else: no model, no vectors,
        no reply, no body change."""
        here = self._here(event)
        if not here or self._job_stale():
            return
        try:
            sid, name = self._speaker(event)
        except Exception:
            sid, name = "", ""
        try:
            self_id = str(getattr(getattr(event, "message_obj", None), "self_id", "") or "")
        except Exception:
            self_id = ""
        if self_id and str(sid) == self_id:
            return  # her own messages come in through on_llm_response
        text = self._message_text(event)
        if not text:
            return
        win = self._read_window(here)
        win["recent"].append({"ts": time.time(), "role": "user", "sender_id": str(sid or ""),
                              "sender_name": str(name or ""), "msg_id": self._message_id(event),
                              "text": text[:WINDOW_MESSAGE_CHARS], "origin": self._event_origin(event)})
        self._write_window(here, win)

    def _window_add_reply(self, event, text) -> None:
        text = str(text or "").strip()
        here = self._here(event)
        if not text or not here or self._job_stale():
            return
        win = self._read_window(here)
        win["recent"].append({"ts": time.time(), "role": "assistant", "text": text[:WINDOW_LINE_CHARS],
                              "origin": self._event_origin(event)})
        self._write_window(here, win)

    def _window_lines(self, event, n=6) -> list:
        """The last `n` lines (anyone's) of the window she is in now, before the current message."""
        here = self._here(event)
        if not here or not n:
            return []
        lines = [x for x in self._read_window(here)["recent"] if str(x.get("text") or "").strip()]
        current = self._message_id(event)
        if current:
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].get("role") != "assistant" and str(lines[i].get("msg_id") or "") == current:
                    del lines[i]
                    break
        return lines[-n:]

    def _window_replies(self, event, n=6) -> list:
        """Her last `n` replies in the window she is in now (dicts with text and origin)."""
        here = self._here(event)
        if not here or not n:
            return []
        lines = [x for x in self._read_window(here)["recent"]
                 if x.get("role") == "assistant" and str(x.get("text") or "").strip()]
        return lines[-n:]

    # ------------------------------------------------------------------
    # Open loops: matched, merged, closed and capped per window
    # ------------------------------------------------------------------
    def _window_loops(self, event) -> list:
        here = self._here(event)
        if not here:
            return []
        return [x for x in self._read_window(here)["open_loops"] if isinstance(x, dict)]

    def _window_update_loops(self, event, text, core=None) -> None:
        """One message, its own window: close what it settles there, add what it asks for there."""
        here = self._here(event)
        if not here or self._job_stale():
            return
        try:
            stamp = time.time()
            win = self._read_window(here)
            loops = [x for x in win["open_loops"] if isinstance(x, dict)]
            before = json.dumps(loops, ensure_ascii=False, sort_keys=True)
            memory_meta.resolve_open_loops(loops, text, stamp)
            for new_loop in memory_meta.detect_open_loops(text, stamp):
                merged = False
                for existing in loops:
                    if str(existing.get("status") or "open") != "open":
                        continue
                    if memory_meta.text_similarity(
                            existing.get("text", ""), new_loop.get("text", "")) >= memory_meta.OPEN_LOOP_MERGE_SIMILARITY:
                        existing["last_mentioned_ts"] = stamp
                        existing["mentioned"] = int(existing.get("mentioned", 1) or 1) + 1
                        merged = True
                        break
                if not merged:
                    new_loop["origin"] = self._event_origin(event)
                    loops.append(new_loop)
            loops = loops[-int(memory_meta.OPEN_LOOP_MAX):]
            if json.dumps(loops, ensure_ascii=False, sort_keys=True) != before:
                win["open_loops"] = loops
                self._write_window(here, win)
        except Exception as exc:
            logger.warning("[ams-life] open loop update failed: %s", exc)
        self._refresh_loop_pressure(core)

    def _refresh_loop_pressure(self, core=None) -> None:
        """Tell the body how many loops are due, over every window (a number, no text)."""
        if core is None:
            return
        due, delay_min = 0, 0.0
        now = time.time()
        try:
            for place in self._window_places():
                loops = [dict(x) for x in self._read_window(place)["open_loops"] if isinstance(x, dict)]
                memory_meta.resolve_open_loops(loops, "", now)  # only lets old ones expire
                for loop in loops:
                    if str(loop.get("status") or "open") != "open":
                        continue
                    hint = str(loop.get("due_hint") or "")
                    if hint == "soon":
                        due += 1
                        delay_min = max(delay_min, 60.0)
                    elif hint == "tomorrow":
                        due += 1
                        delay_min = max(delay_min, 1440.0)
        except Exception:
            pass
        core.loop_pressure = {"due": due, "delay_min": delay_min}

    # ------------------------------------------------------------------
    # Older body states: their text goes into the windows it came from
    # ------------------------------------------------------------------
    @staticmethod
    def _body_state_has_text(state) -> bool:
        if not isinstance(state, dict):
            return False
        if any(isinstance(x, dict) and "text" in x
               for key in ("history", "stimuli") for x in (state.get(key) or [])):
            return True
        for key in _OLD_BODY_TEXT_KEYS:
            value = state.get(key)
            if key == "self_timeline" and isinstance(value, dict):
                value = value.get("past") or value.get("present")
            if value:
                return True
        return False

    def _move_body_texts_to_phone(self, state, fallback_where="") -> bool:
        """Move reply lines and open loops of an older body state into their windows.

        Items whose window cannot be worked out are dropped here (the caller
        keeps the old file in the archive). The state is stripped of every text
        field in place. Returns True when it carried any text.
        """
        if not isinstance(state, dict):
            return False
        moved = {}

        def window_for(item):
            where = discretion.origin_of(item, fallback_where)["where"]
            if not where or where == discretion.SELF:
                return None
            if where not in moved:
                moved[where] = self._read_window(where)
            return moved[where]

        had_text = False
        for item in state.get("history") or []:
            if not isinstance(item, dict) or "text" not in item:
                continue
            had_text = True
            text = str(item.pop("text") or "").strip()
            origin = item.pop("origin", None)
            win = window_for({"origin": origin} if isinstance(origin, dict) else {})
            if win is not None and text:
                win["recent"].append({"ts": item.get("ts", 0), "role": "assistant", "text": text[:WINDOW_LINE_CHARS],
                                      "origin": discretion.origin_of({"origin": origin} if isinstance(origin, dict)
                                                                     else {}, fallback_where)})
        for item in state.get("open_loops") or []:
            if not isinstance(item, dict):
                continue
            had_text = True
            win = window_for(item)
            if win is not None:
                win["open_loops"].append(dict(item, origin=discretion.origin_of(item, fallback_where)))
        had_text = had_text or self._body_state_has_text(state)
        for item in state.get("stimuli") or []:
            if isinstance(item, dict):
                item.pop("text", None)
        for key in _OLD_BODY_TEXT_KEYS:
            state.pop(key, None)
        for where, win in moved.items():
            win["recent"] = sorted(win["recent"], key=lambda x: float(x.get("ts", 0) or 0))
            win["open_loops"] = win["open_loops"][-int(memory_meta.OPEN_LOOP_MAX):]
            self._write_window(where, win)
        return had_text
