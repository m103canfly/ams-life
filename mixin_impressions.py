# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""ams-life: the group members she knows (impressions.py) in the plugin.

- every night, after impressions_time, each group's phone window updates what she
  thinks of the people who talked a lot that day: at most one model call per group
  per day (switch "group_impressions" in the panel, off by default);
- in a reply, a "[认识的人]" line describes the people in this chat as the owner's
  table allows: in that group all of it; in another group where he is, only what he
  is called; in his own private chat his name and how he talks (topics only those he
  brought up there); in anyone else's private chat nothing;
- what people are called -- the owner's names first (setting member_aliases), then
  what she found -- joins the names that are made anonymous elsewhere;
- the owner sees them in the panel and can delete what she thinks of someone.
"""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from . import impressions
except ImportError:
    import impressions

PEOPLE_DIR = DATA_DIR / "people"
PEOPLE_IN_LINE = 5   # people described in one reply


class ImpressionsMixin:
    def _impression_store(self):
        store = getattr(self, "_people_store", None)
        if store is None:
            store = self._people_store = impressions.Store(PEOPLE_DIR)
        return store

    def _impression_records(self, qq) -> list:
        """[(place, record)] of `qq` in every group, most recently updated first."""
        store, out = self._impression_store(), []
        for place in store.places():
            rec = store.load(place)["people"].get(str(qq))
            if isinstance(rec, dict):
                out.append((place, rec))
        out.sort(key=lambda x: str(x[1].get("updated") or ""), reverse=True)
        return out

    # ------------------------------------------------------------------
    # What people are called: the owner's names first
    # ------------------------------------------------------------------
    def _owner_aliases(self) -> dict:
        """Setting member_aliases, one per line: "<QQ>:<name>,<name>" -> {qq: [names]}."""
        out = {}
        raw = (getattr(self, "config", None) or {}).get("member_aliases") or []
        for line in raw if isinstance(raw, (list, tuple)) else str(raw).splitlines():
            qq, _, names = str(line or "").replace("：", ":").partition(":")
            qq = qq.strip()
            if not qq.isdigit():
                continue
            for n in names.replace("，", ",").split(","):
                n = n.strip()
                if n and n not in out.setdefault(qq, []):
                    out[qq].append(n)
        return out

    def _aliases_of(self, qq, found=()) -> list:
        """The owner's names for him, then those she found -- minus any the owner gave someone else."""
        owner = self._owner_aliases()
        taken = {n for other, ns in owner.items() if other != str(qq) for n in ns}
        mine = list(owner.get(str(qq), []))
        return list(dict.fromkeys(mine + [n for n in found if n not in taken]))

    def _impression_names(self, person) -> list:
        """Name source for making things anonymous (register_name_source): every name and
        alias he goes by in any group, and the owner's names for him."""
        names = self._impression_store().names_of(person)   # kept when his impression goes
        for _place, rec in self._impression_records(person):
            names.append(rec.get("name"))
            names.extend(rec.get("aliases") or [])
        return [n for n in self._aliases_of(person, [n for n in names if n]) if n]

    # ------------------------------------------------------------------
    # The "[认识的人]" line
    # ------------------------------------------------------------------
    def _people_lines(self, event) -> list:
        here = self._here(event)
        if not here:
            return []
        sid, name = self._speaker(event)
        recent = [x for x in self._read_window(here)["recent"] if isinstance(x, dict) and x.get("role") != "assistant"]
        present = []
        for x in [{"sender_id": sid}] + list(reversed(recent)):
            who = str(x.get("sender_id") or "")
            if who and who not in present:
                present.append(who)
        if here.startswith("private:"):
            present = [p for p in present if here == "private:" + p]
        out = []
        for who in present[:PEOPLE_IN_LINE]:
            records = self._impression_records(who)
            if not records:
                continue
            own = next(((p, r) for p, r in records if p == here), None)
            place, rec = own or records[0]
            said_here = "\n".join(str(x.get("text") or "") for x in recent if str(x.get("sender_id") or "") == who)
            v = impressions.view(rec, place, here, present_here=True, private_text=said_here)
            if not v:
                continue
            found = [a for _p, r in records for a in (r.get("aliases") or [])] if not own else list(v["aliases"])
            v["aliases"] = self._aliases_of(who, found)
            if not own:   # the name he goes by here, not another group's card
                v["name"] = (name if who == sid and name else next(
                    (str(x.get("sender_name")) for x in reversed(recent)
                     if str(x.get("sender_id") or "") == who and x.get("sender_name")), "")) or v["name"]
            line = impressions.describe(v)
            if line:
                out.append(line)
        return out

    # ------------------------------------------------------------------
    # Every night (the 5-minute loop)
    # ------------------------------------------------------------------
    def _impressions_time_reached(self, now=None) -> bool:
        if not self._llm_allowed("group_impressions"):
            return False
        local = time.localtime(time.time() if now is None else now)
        try:
            hh, mm = [int(x) for x in str(getattr(self, "impressions_time", "23:15") or "23:15").split(":")[:2]]
        except Exception:
            hh, mm = 23, 15
        return (local.tm_hour, local.tm_min) >= (hh, mm)

    def _material_names(self, place, lines) -> dict:
        """{qq: names} the nightly material turns into codes besides this window's cards: for
        everyone in this group (in the window, or with an impression here) and everyone the
        owner named, every name they are known by -- the owner's and those seen elsewhere."""
        who = {str(x.get("sender_id") or "") for x in lines if isinstance(x, dict) and x.get("role") != "assistant"}
        who |= set(self._impression_store().load(place)["people"]) | set(self._owner_aliases())
        return {qq: [n for n in self._known_names([qq]) if n != qq] for qq in sorted(who) if qq}

    async def _maybe_update_impressions(self, now=None) -> dict:
        """Each group window once a day after impressions_time; impressions.nightly marks the
        group as tried before its one model call (a failure or a restart does not call again)."""
        if not self._impressions_time_reached(now):
            return {}
        day = time.strftime("%Y-%m-%d", time.localtime(time.time() if now is None else now))
        provider = None
        try:
            provider = await self._provider_for("group_impressions", None)
        except Exception as exc:
            logger.warning("[ams-life] impressions provider failed: %s", exc)
        if provider is None:
            return {}

        async def ask(prompt):
            resp = await provider.text_chat(prompt=prompt)
            return str(getattr(resp, "completion_text", "") or "")

        done = {}
        for place in self._window_places():
            if not place.startswith("group:"):
                continue
            try:
                lines = self._read_window(place)["recent"]
                done[place] = await impressions.nightly(self._impression_store(), place, lines, ask, day,
                                                        registry=self._registry(),
                                                        extra_names=self._material_names(place, lines))
            except Exception as exc:
                logger.warning("[ams-life] impressions for %s failed: %s", place, exc)
        if any(r.get("called") for r in done.values()):
            logger.info("[ams-life] impressions: %s", {p: r for p, r in done.items() if r.get("called")})
        return done

    # ------------------------------------------------------------------
    # The panel: see them, delete what she thinks of someone
    # ------------------------------------------------------------------
    def _impressions_for_page(self) -> list:
        store, out = self._impression_store(), []
        for place in store.places():
            data = store.load(place)
            people = []
            for qq, rec in sorted(data["people"].items(), key=lambda kv: -int((kv[1].get("stats") or {}).get("msgs", 0) or 0)):
                stats = rec.get("stats") or {}
                people.append({"qq": qq, "name": rec.get("name", ""), "aliases": self._aliases_of(qq, rec.get("aliases") or []),
                               "style": rec.get("style", ""), "topics": list(rec.get("topics") or []),
                               "msgs": int(stats.get("msgs", 0) or 0), "days": int(stats.get("days", 0) or 0),
                               "updated": rec.get("updated", "")})
            out.append({"place": place, "people": people})
        return out

    def _owner_forget_impression(self, qq) -> int:
        """Delete what she thinks of `qq` in every group, and note it so she does not write
        one again (only the impression: what she remembers of him stays, and so do the names
        he went by, so it is still made anonymous elsewhere)."""
        qq = str(qq or "").strip()
        if not qq:
            return 0
        self._registry().stop_impression(qq)
        return self._impression_store().forget_impression(qq)
