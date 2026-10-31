# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""ams-life: what happened today in each chat window (digest.py) in the plugin.

- every night, after digest_time (before the group impressions and her notebook, so
  that the notebook can use what it finds), each window that had messages today -- every
  group, and the busiest digest.PRIVATE_MAX private chats -- gets one model call (switch
  "daily_digest" in the panel, off by default). A window is marked as tried before its
  call (in self_model.json, by a hash of the window), so a failure or a restart does not
  call again that day;
- what it finds goes into the event archive like any other event: recalled, in
  "[最近的事]", in her notebook's material; a duplicate of an event of that window is
  merged into it, origins together;
- its origin is that window (a group's public, a private chat's private), the people and
  message ids of the lines it was drawn from (or of the whole day, see digest.sources),
  so deleting a person or a message, from the panel or by restoring a backup, takes it
  too (_forget).
"""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from . import digest
except ImportError:
    import digest


class DigestMixin:
    def _digest_time_reached(self, now=None) -> bool:
        if not self._llm_allowed("daily_digest"):
            return False
        local = time.localtime(time.time() if now is None else now)
        try:
            hh, mm = [int(x) for x in str(getattr(self, "digest_time", "23:05") or "23:05").split(":")[:2]]
        except Exception:
            hh, mm = 23, 5
        return (local.tm_hour, local.tm_min) >= (hh, mm)

    @staticmethod
    def _digest_mark(place) -> str:
        return _sha256("digest|" + str(place))[:16]

    def _digest_windows(self, day) -> list:
        """Tonight's windows: every group with messages from others today, then the busiest
        private chats talked in today (at most digest.PRIVATE_MAX)."""
        groups, private = [], {}
        for place in self._window_places():
            n = sum(1 for x in self._read_window(place)["recent"]
                    if isinstance(x, dict) and x.get("role") != "assistant" and digest._day(x.get("ts")) == day)
            if not n:
                continue
            if place.startswith("group:"):
                groups.append(place)
            elif place.startswith("private:"):
                private[place] = n
        return groups + sorted(private, key=lambda p: (-private[p], p))[:digest.PRIVATE_MAX]

    async def _maybe_daily_digest(self, now=None) -> dict:
        """Each window of today once, after digest_time: {place: what happened}."""
        if not self._digest_time_reached(now):
            return {}
        now = time.time() if now is None else now
        day = time.strftime("%Y-%m-%d", time.localtime(now))
        night = (self.self_model or {}).get("digest_night")
        if not isinstance(night, dict) or night.get("date") != day:
            night = {"date": day, "tried": []}
            self.self_model["digest_night"] = night
        done = {}
        for place in self._digest_windows(day):
            if self._digest_mark(place) in night["tried"]:
                continue
            try:
                done[place] = await self._digest_window(place, day, night, now)
            except Exception as exc:
                logger.warning("[ams-life] daily digest failed: %s", exc)
                done[place] = {"error": type(exc).__name__}
        if done:
            logger.info("[ams-life] daily digest: %s", {("group" if p.startswith("group:") else "private"): r
                                                         for p, r in done.items()})
        return done

    async def _digest_window(self, place, day, night, now) -> dict:
        win = self._read_window(place)
        day_all = digest.day_lines(win["recent"], day, place, self._registry())
        if not any(x.get("role") != "assistant" for x in day_all):
            return {"skipped": "nothing kept"}
        private = place.startswith("private:")
        # every name anyone in the window goes by becomes a code -- those the registry rules out too
        names = {qq: set(ns) for qq, ns in self._material_names(place, win["recent"]).items()}
        text, codes, shown = digest.material(day_all, names, self._red_lines_for("digest"))
        if not shown:
            return {"skipped": "nothing to show"}
        night["tried"].append(self._digest_mark(place))   # before the call: a failure counts
        self._save_self_model()
        items = await self._llm_v2_call(
            "daily_digest", digest.prompt_for(text, private),
            lambda raw: digest.parse_answer(raw, codes, len(shown), self._red_lines_for("digest"),
                                            self._judgements_for("digest")))
        if not items or self._job_stale():
            return {"called": 1, "written": 0}
        written = 0
        for item in items:
            people, ids = digest.sources(item, codes, shown, day_all)
            record = self._digest_event(place, place, item, codes, day_all, people, ids,
                                        private, now)
            if not self._new_item_kept(record):
                continue   # someone or something the registry rules out: not kept, nor merged in
            dup = self._find_any_duplicate_event(record["session"], record["event_key"], record["event"], now)
            if dup is not None and discretion.origin_of(dup)["where"] == place:
                self._merge_archive_duplicate(dup, record)
            else:
                self._append_event_archive(record)
            written += 1
        return {"called": 1, "written": written}

    def _digest_event(self, place, session, item, codes, day_all, people, ids, private, now) -> dict:
        """One thing that happened, as an event record of that window."""
        called = {}
        for ln in day_all:   # the name each goes by here today, else one she knows
            if ln.get("role") != "assistant" and ln.get("sender_id") and ln.get("sender_name"):
                called[str(ln["sender_id"])] = str(ln["sender_name"])
        for qq in codes.values():
            if qq not in called:
                known = [n for n in self._known_names([qq]) if n != qq and not n.isdigit()]
                called[qq] = known[0] if known else ""
        title = digest.named(item["title"], codes, called)
        what = digest.named(item["what"], codes, called)
        used = [ln for ln in day_all if discretion.is_about(discretion.origin_of(ln), source_ids=ids)]
        private = private or any(discretion.origin_of(ln)["visibility"] == discretion.PRIVATE for ln in used)
        origin = discretion.make_origin(place, people, ids, discretion.PRIVATE if private else discretion.PUBLIC)
        return {"id": "dig_" + _sha256("%s|%s|%s" % (place, now, title))[:16], "ts": now, "session": str(session),
                "kind": "daily_digest", "title": title, "event": what, "big_summary": what,
                "small_summary": what[:80], "summary_status": "digest",
                "event_key": self._normalize_event_key(title, title),
                "importance": 0.5, "centrality": 0.5, "strength": 0.5, "confidence": 0.6,
                "source_count": len(ids), "recall_count": 0, "last_recall": now,
                "names": sorted({n for qq, n in called.items() if n and qq in people}),
                "origin": origin}
