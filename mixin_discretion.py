# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""ams-life: apply the discretion table to everything that can reach a reply prompt,
and forget a person (or some messages) for real.

The memory library itself lives in mixin_memory; the table is in discretion.py.
"""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403

import contextvars

# ams-life: the forget count when the current job (one request, one reply, one
# background task) started. A task started from a request inherits its mark.
_FORGET_MARK = contextvars.ContextVar("ams_life_forget_mark", default=None)

_EVENT_TEXT_FIELDS = ("title", "event", "central_details", "meaning_to_her", "reflection",
                      "big_summary", "small_summary", "peripheral_details")


class DiscretionMixin:
    # ------------------------------------------------------------------
    # Forget count: work that waited (for the model, the vector service)
    # holds copies from before; if anything was forgotten meanwhile, its
    # writes are dropped instead of putting the forgotten things back.
    # ------------------------------------------------------------------
    def _forget_count(self) -> int:
        return len(getattr(self, "_forget_log", None) or [])

    def _begin_job(self) -> None:
        _FORGET_MARK.set(self._forget_count())

    def _job_stale(self) -> bool:
        """True when something was forgotten since this job started: do not write."""
        mark = _FORGET_MARK.get()
        if mark is None or self._forget_count() <= mark:
            return False
        logger.info("[ams-life] write dropped: something was forgotten since this work started")
        return True

    # ------------------------------------------------------------------
    # Events (the one global archive; each record carries its origin).
    # ------------------------------------------------------------------
    def _visible_events(self, event, events) -> list:
        """Events that may be brought up here; ones from elsewhere lose who said what."""
        here = self._here(event)
        out = []
        for ev in events or []:
            if not isinstance(ev, dict):
                continue
            v = discretion.verdict(discretion.origin_of(ev), here)
            if v == discretion.DROP:
                continue
            if v == discretion.ANON:
                names = discretion.names_in(ev)
                ev = dict(ev)
                for key in _EVENT_TEXT_FIELDS:
                    if ev.get(key):
                        ev[key] = discretion.anonymize(ev[key], names)
            out.append(ev)
        return out

    # ------------------------------------------------------------------
    # Her self-description and the speaker's relationship record.
    # ------------------------------------------------------------------
    def _self_model_for(self, event) -> dict:
        """Self model as seen from here: the "recently" narrative only keeps lines allowed here.

        Narrative text written before ams-life has no origin and is left out.
        """
        model = dict(self.self_model or {})
        here = self._here(event)
        lines = []
        for item in model.get("narrative_items") or []:
            if not isinstance(item, dict):
                continue
            v = discretion.verdict(discretion.origin_of(item), here)
            if v == discretion.DROP:
                continue
            text = str(item.get("text") or "")
            if v == discretion.ANON:
                text = discretion.anonymize(text, discretion.origin_of(item)["people"] + list(item.get("names") or []))
            if text:
                lines.append(text)
        model["narrative"] = "；".join(lines)[:600]
        return model

    def _user_view(self, event, user_data) -> dict:
        """The speaker's record as shown here: shared memories only in his own private chat.

        Shared ("we") memories carry no origin; outside his private chat they are
        left out rather than risk repeating something he only said in private.
        """
        if not isinstance(user_data, dict):
            return user_data
        sid, _name = self._speaker(event)
        if self._here(event) == "private:" + str(sid or ""):
            return user_data
        rel = user_data.get("relationship")
        if not isinstance(rel, dict) or not rel.get("we_memory"):
            return user_data
        return dict(user_data, relationship=dict(rel, we_memory=[]))

    # ------------------------------------------------------------------
    # Forgetting: delete for real, by person or by source message.
    # ------------------------------------------------------------------
    def _forget(self, person: str = "", source_ids=None) -> dict:
        """Delete every memory, event, note and phone line that came from `person`
        (or from one of `source_ids`), and his relationship record.

        Returns counts per store. Files moved aside by the one-her migration
        (per-session legacy/archive folders) are not touched here. Every call
        is logged; the log length is the forget count (see _job_stale).
        """
        person = str(person or "").strip()
        ids = [str(x) for x in (source_ids or []) if str(x or "").strip()]
        if not person and not ids:
            return {}
        if not isinstance(getattr(self, "_forget_log", None), list):
            self._forget_log = []
        self._forget_log.append((person, list(ids)))
        counts = {"memories": 0, "events": 0, "relationship": 0, "notes": 0, "phone": 0}

        def about(item):
            return discretion.is_about(discretion.origin_of(item), person, ids)

        # 1) the memory library (and the person's private room)
        lib = self._read_library()
        gone = {str(e.get("id") or "") for e in lib["entries"] if isinstance(e, dict) and about(e)}
        keep = [e for e in lib["entries"] if not (isinstance(e, dict) and about(e))]
        counts["memories"] = len(lib["entries"]) - len(keep)
        lib["entries"] = keep
        if person:
            lib["rooms"].pop("private:" + person, None)
        for room in lib["rooms"].values():
            if isinstance(room, dict) and isinstance(room.get("working_set"), list):
                room["working_set"] = [x for x in room["working_set"] if str(x) not in gone]
            if isinstance(room, dict) and isinstance(room.get("last_recall_trace"), list):
                room["last_recall_trace"] = [x for x in room["last_recall_trace"]
                                             if not (isinstance(x, dict) and str(x.get("entry_id") or "") in gone)]
        if counts["memories"] or person:
            self._write_library(lib)

        # 2) the event archive and its per-place copies
        paths = [EVENT_ARCHIVE_PATH]
        if EVENT_SESSION_DIR.exists():
            paths.extend(sorted(EVENT_SESSION_DIR.glob("*/events.jsonl")))
        for path in paths:
            if not path.exists():
                continue
            kept, dropped = [], 0
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    rec = json.loads(line)
                except Exception:
                    kept.append(line)
                    continue
                if isinstance(rec, dict) and about(rec):
                    dropped += 1
                    continue
                kept.append(line)
            if dropped:
                tmp = path.with_suffix(".tmp")
                tmp.write_text("".join(x + "\n" for x in kept), encoding="utf-8")
                os.replace(str(tmp), str(path))
                if path == EVENT_ARCHIVE_PATH:
                    counts["events"] += dropped

        # 3) his relationship record
        if person:
            safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in person)[:60]
            upath = USER_DIR / (safe + ".json")
            if upath.exists():
                upath.unlink()
                counts["relationship"] = 1

        # 4) her notes about him (narrative lines, diary, relationship narratives)
        changed = False
        for key in ("narrative_items", "diary", "relationship_narratives"):
            items = self.self_model.get(key)
            if not isinstance(items, list):
                continue
            kept_items = [x for x in items if not (isinstance(x, dict) and about(x))]
            if len(kept_items) != len(items):
                counts["notes"] += len(items) - len(kept_items)
                self.self_model[key] = kept_items
                changed = True
        if changed:
            self.self_model["narrative"] = "；".join(
                str(x.get("text") or "") for x in self.self_model.get("narrative_items") or []
                if isinstance(x, dict))[:600]
            self._save_self_model()

        # 5) her phone: his private window, and lines and loops from him elsewhere
        for place in self._window_places():
            if person and place == "private:" + person:
                win = self._read_window(place)
                counts["phone"] += len(win["recent"]) + len(win["open_loops"])
                self._window_file(place).unlink()
                continue
            win = self._read_window(place)
            changed = False
            for key in ("recent", "open_loops"):
                kept_items = [x for x in win[key] if not (isinstance(x, dict) and about(x))]
                if len(kept_items) != len(win[key]):
                    counts["phone"] += len(win[key]) - len(kept_items)
                    win[key] = kept_items
                    changed = True
            if changed:
                self._write_window(place, win)
        self._refresh_loop_pressure(self._core(None))
        logger.info("[ams-life] forgot person=%s sources=%d: %s", "yes" if person else "no", len(ids), counts)
        return counts
