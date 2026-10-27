# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""ams-life: her phone.

Three layers, after "she has a phone of her own":

- phone: every group and every private chat is one window. What was said there
  (her latest replies, the open loops) is kept only in that window, one file
  per window under PHONE_DIR. Wherever she is, she only sees that window.
- body: moods and drives only; it keeps no text at all (see body.py).
- memory: what she keeps, each item with an origin (mixin_memory, discretion).

Every line and loop in a window carries an origin like a memory does, so
forgetting finds them the same way.
"""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403

WINDOW_RECENT_MAX = 80
WINDOW_LINE_CHARS = 80
# Body fields of older state files that held text; they never come back into the body.
_OLD_BODY_TEXT_KEYS = ("open_loops", "event_anchors", "autobiography", "self_timeline",
                       "core_self", "narrative_self")


class PhoneMixin:
    # ------------------------------------------------------------------
    # Windows on disk
    # ------------------------------------------------------------------
    @staticmethod
    def _window_file(place):
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(place))[:100]
        return PHONE_DIR / (safe + ".json")

    def _read_window(self, place) -> dict:
        win = {}
        try:
            path = self._window_file(place)
            if path.exists():
                win = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            win = {}
        if not isinstance(win, dict):
            win = {}
        win["place"] = str(place)
        for key in ("recent", "open_loops"):
            if not isinstance(win.get(key), list):
                win[key] = []
        return win

    def _write_window(self, place, win) -> None:
        PHONE_DIR.mkdir(parents=True, exist_ok=True)
        path = self._window_file(place)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(win, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(str(tmp), str(path))

    def _window_places(self) -> list:
        out = []
        if PHONE_DIR.exists():
            for path in sorted(PHONE_DIR.glob("*.json")):
                try:
                    place = str(json.loads(path.read_text(encoding="utf-8")).get("place") or "")
                except Exception:
                    place = ""
                if place:
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

    # ------------------------------------------------------------------
    # Her latest replies, in this window only
    # ------------------------------------------------------------------
    def _window_add_reply(self, event, text) -> None:
        text = str(text or "").strip()
        here = self._here(event)
        if not text or not here:
            return
        win = self._read_window(here)
        win["recent"] = (win["recent"] + [{"ts": time.time(), "role": "assistant",
                                           "text": text[:WINDOW_LINE_CHARS],
                                           "origin": self._event_origin(event)}])[-WINDOW_RECENT_MAX:]
        self._write_window(here, win)

    def _window_replies(self, event, n=6) -> list:
        """Her last `n` replies in the window she is in now (dicts with text and origin)."""
        here = self._here(event)
        if not here:
            return []
        lines = [x for x in self._read_window(here)["recent"]
                 if isinstance(x, dict) and str(x.get("text") or "").strip()]
        return lines[-n:] if n else []

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
        if not here:
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
            win["recent"] = sorted(win["recent"], key=lambda x: float(x.get("ts", 0) or 0))[-WINDOW_RECENT_MAX:]
            win["open_loops"] = win["open_loops"][-int(memory_meta.OPEN_LOOP_MAX):]
            self._write_window(where, win)
        return had_text
