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
# ams-life: set when the message this job is about comes from someone (or is a message)
# the forget registry rules out: she may still answer, but nothing of it is kept.
_KEEP_NOTHING = contextvars.ContextVar("ams_life_keep_nothing", default=False)

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
        _KEEP_NOTHING.set(False)

    def _continue_job(self) -> None:
        """A later step of the same message (the reply) keeps the mark its request set
        (AstrBot runs one message, request to reply, in one task); only when this
        context has none does it start one."""
        if _FORGET_MARK.get() is None:
            self._begin_job()

    def _job_stale(self) -> bool:
        """True when something was forgotten since this job started, or the message it is
        about may not be kept (forget registry): do not write."""
        if _KEEP_NOTHING.get():
            return True
        mark = _FORGET_MARK.get()
        if mark is None or self._forget_count() <= mark:
            return False
        logger.info("[ams-life] write dropped: something was forgotten since this work started")
        return True

    # ------------------------------------------------------------------
    # The forget registry (forget_registry.py): who and what she must not keep.
    # What the old companion was asked to forget, and what the owner deleted in
    # the panel. No one can add to it by saying something in a chat.
    # ------------------------------------------------------------------
    def _registry(self):
        reg = getattr(self, "_forget_reg", None)
        if reg is None:
            reg = self._forget_reg = forget_registry.ForgetRegistry(FORGET_REGISTRY_PATH)
            self._forget_snap = None
        return reg

    def _registry_sets(self) -> tuple:
        """(people with any row, message ids with a row), reread when the registry grows."""
        reg = self._registry()
        seq = reg.last_seq()
        snap = getattr(self, "_forget_snap", None)
        if not snap or snap[0] != seq:
            rows = reg.rows()
            snap = self._forget_snap = (seq, {r["qq"] for r in rows if r["kind"] in ("qq", "optout", "optin")},
                                        {r["source_id"] for r in rows if r["kind"] == "source"})
        return snap[1], snap[2]

    def _may_keep(self, people=(), place="", at=None, source_ids=()) -> bool:
        """May she keep something about these people / from these messages, said here and
        then? When the registry cannot be read this raises forget_registry.Unreadable: the
        caller writes nothing this time (it never drops what is already kept)."""
        try:
            gone_people, gone_ids = self._registry_sets()
            people = {str(x) for x in (people or ()) if str(x or "").strip()}
            ids = {str(x) for x in (source_ids or ()) if str(x or "").strip()}
            if "*" not in gone_people and not (people & gone_people) and not (ids & gone_ids):
                return True
            return self._registry().may_keep_all(sorted(people), place, at, sorted(ids))
        except Exception as exc:
            raise forget_registry.Unreadable(str(exc)) from exc

    def _new_item_kept(self, item) -> bool:
        """One new item (an event, an insight): may it be written? Not when the registry
        cannot be read (it is just not written)."""
        try:
            return self._origin_kept(item)
        except forget_registry.Unreadable as exc:
            logger.warning("[ams-life] forget registry unreadable, not written: %s", exc)
            return False

    def _origin_kept(self, item) -> bool:
        """May an item (memory, event, note, phone line) with this origin be kept? Raises
        forget_registry.Unreadable when the registry cannot be read."""
        if not isinstance(item, dict):
            return True
        o = discretion.origin_of(item)
        try:
            at = float(item.get("ts")) if item.get("ts") is not None else None
        except (TypeError, ValueError):
            at = None
        return self._may_keep(o["people"], o["where"], at, o["source_ids"])

    def _check_registry(self, event) -> bool:
        """The message this job is about: may she keep anything of it? If not, nothing this
        job (and the work it starts) writes is kept."""
        try:
            sid, _name = self._speaker(event)
        except Exception:
            sid = ""
        try:
            if self._may_keep([sid] if sid else [], self._here(event), time.time(), self._source_ids(event)):
                return True
            logger.info("[ams-life] a message she may not keep: nothing of it is written")
        except forget_registry.Unreadable as exc:
            logger.warning("[ams-life] forget registry unreadable: nothing of this message is written: %s", exc)
        _KEEP_NOTHING.set(True)
        return False

    # ------------------------------------------------------------------
    # Every name a person is known by, for making things anonymous.
    # ------------------------------------------------------------------
    def register_name_source(self, source) -> None:
        """Add a source of names: source(person_id) -> names. For what she calls people
        (step 1-3's impressions) to join the names below."""
        sources = getattr(self, "_name_sources", None)
        if not isinstance(sources, list):
            sources = self._name_sources = []
        if source not in sources:
            sources.append(source)

    def _names_index(self) -> dict:
        """person id -> the nicknames and group cards seen with it: from every chat window
        and the memory library once, then kept up as messages come (_note_name)."""
        idx = getattr(self, "_name_index", None)
        if isinstance(idx, dict):
            return idx
        idx = self._name_index = {}
        for place in self._window_places():
            for x in self._read_window(place)["recent"]:
                self._note_name(x.get("sender_id"), x.get("sender_name"))
        for e in self._read_library()["entries"]:
            if not isinstance(e, dict):
                continue
            self._note_name(e.get("sender_id"), e.get("sender_name"))
            prov = e.get("provenance") if isinstance(e.get("provenance"), dict) else {}
            for src in [prov] + [s for s in (prov.get("sources") or []) if isinstance(s, dict)]:
                self._note_name(src.get("sender_id"), src.get("sender_name"))
        return idx

    def _note_name(self, person, name) -> None:
        person, name = str(person or "").strip(), str(name or "").strip()
        idx = getattr(self, "_name_index", None)
        if not person or not name or not isinstance(idx, dict):
            return
        idx.setdefault(person, set()).add(name)

    def _known_names(self, people) -> list:
        """Every name these people are known by: the ids themselves, the nicknames and
        group cards they used in any window or memory, the names kept in their
        relationship records, and whatever the registered name sources add."""
        idx = self._names_index()
        out = set()
        for person in people or []:
            person = str(person or "").strip()
            if not person:
                continue
            out.add(person)
            out |= idx.get(person, set())
            try:
                safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in person)[:60]
                path = USER_DIR / (safe + ".json")
                if path.exists():
                    rec = json.loads(path.read_text(encoding="utf-8"))
                    out |= {str(x) for x in [rec.get("sender_name")] + list(rec.get("names") or []) if x}
            except Exception:
                pass
            for source in getattr(self, "_name_sources", None) or []:
                try:
                    out |= {str(x) for x in (source(person) or []) if x}
                except Exception as exc:
                    logger.warning("[ams-life] name source failed: %s", exc)
        return sorted(out)

    # ------------------------------------------------------------------
    # No numbers in what she keeps; someone deleted is 某人
    # ------------------------------------------------------------------
    def _note_her(self, event) -> None:
        """Her own number, as each message tells it (an @ of her becomes her name)."""
        try:
            sid = str(getattr(getattr(event, "message_obj", None), "self_id", "") or "")
        except Exception:
            sid = ""
        if sid:
            if not isinstance(getattr(self, "_her_ids", None), set):
                self._her_ids = set()
            self._her_ids.add(sid)

    def _gone_people(self) -> set:
        """People the forget registry rules out now (reread when it grows)."""
        try:
            reg = self._registry()
            seq = reg.last_seq()
            snap = getattr(self, "_gone_snap", None)
            if not snap or snap[0] != seq:
                snap = self._gone_snap = (seq, {p for p in reg.people() if reg.why_not(qq=p)})
            return set(snap[1])
        except Exception:
            return set()

    def _known_numbers(self) -> set:
        """Every number she knows to be someone's or some chat's: her own, everyone who wrote
        in a window or a memory, each chat's number, and the forget registry's people and
        messages."""
        nums = set(getattr(self, "_her_ids", None) or ())
        nums |= set(self._names_index())
        nums |= {p.split(":", 1)[1] for p in self._window_places() if ":" in p}
        try:
            gone_people, gone_ids = self._registry_sets()
            nums |= set(gone_people) | set(gone_ids)
        except Exception:
            pass
        return {n for n in nums if n.isdigit() and len(n) >= 5}

    def _scrubber(self, event=None):
        """_scrub with what it needs looked up once (for many texts at a time)."""
        ats = []
        if event is not None:
            self._note_her(event)
            try:  # the message's own @ parts: their numbers are known, their "@名字(号码)" exact
                for comp in event.get_messages() or []:
                    if type(comp).__name__ == "At":
                        qq = str(getattr(comp, "qq", "") or "")
                        if qq.isdigit():
                            ats.append((str(getattr(comp, "name", "") or "").strip(), qq))
            except Exception:
                pass
        gone, numbers = self._gone_people(), self._known_numbers() | {qq for _n, qq in ats}
        her = set(getattr(self, "_her_ids", None) or ())
        seen = getattr(self, "_gone_names", None)
        if not isinstance(seen, dict):
            seen = self._gone_names = {}
        gone_names = {p: set(self._known_names([p])) for p in gone}

        def scrub(text):
            text = str(text or "")
            if not text:
                return text
            for name, qq in discretion.at_names(text):
                if qq in gone and name:
                    seen.setdefault(qq, set()).add(name)
            out = discretion.strip_numbers(text, numbers, her, HER_NAME, gone, ats)
            if gone:
                names = {n for p in gone for n in gone_names[p] | seen.get(p, set()) if not str(n).isdigit()}
                out = discretion.anonymize(out, names, to=discretion.SOMEBODY)
            return out
        return scrub

    def _scrub(self, text, event=None) -> str:
        """What is kept of a text (her phone, memories, events): no number she knows of, an @
        with the name only (her own name for an @ of her), and someone the registry rules
        out -- by an @ or by a name she knows him by -- is 某人."""
        return self._scrubber(event)(text) if str(text or "") else str(text or "")

    # text fields of what she keeps (memories, phone lines, events, insights, notes,
    # relationship records): numbers are taken out of these, never out of ids
    _SCRUB_KEYS = {"text", "latest_text", "title", "key", "event", "small_summary", "big_summary",
                   "meaning_to_her", "reflection", "summary", "insight", "lesson", "image_caption",
                   "voice_text", "source_texts", "evidence", "narrative"}

    def _scrub_tree(self, obj, scrub, key=None):
        """`obj` with the text fields scrubbed (a new object; ids and numbers fields untouched)."""
        if isinstance(obj, dict):
            return {k: self._scrub_tree(v, scrub, k) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._scrub_tree(v, scrub, key) for v in obj]
        if isinstance(obj, str) and key in self._SCRUB_KEYS:
            return scrub(obj)
        return obj

    def _migrate_numbers(self) -> dict:
        """Numbers kept before step 1-3-5 (an @ with a number, anyone's number in a text, a
        deleted person's name) are taken out of the library, her phone, events and insights,
        the relationship records and her notes. Each file that changes is copied into
        MEMORY_ARCHIVE_DIR first (never deleted); nothing to change: nothing is written."""
        scrub = self._scrubber()
        stamp = time.strftime("%Y%m%d-%H%M%S")
        folder = MEMORY_ARCHIVE_DIR / ("before-numbers-" + stamp)
        counts = {}

        def archive(path):
            if path == MEMORY_LIBRARY_PATH:
                dest = MEMORY_ARCHIVE_DIR / ("library.before-numbers-%s.json" % stamp)
            else:
                dest = folder / path.relative_to(DATA_DIR)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(path), str(dest))

        def json_file(path, what):
            try:
                body = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return
            new = self._scrub_tree(body, scrub)
            if new != body:
                archive(path)
                tmp = path.with_suffix(".tmp")
                tmp.write_text(json.dumps(new, ensure_ascii=False, indent=None if path == MEMORY_LIBRARY_PATH else 1),
                               encoding="utf-8")
                os.replace(str(tmp), str(path))
                counts[what] = counts.get(what, 0) + 1

        if MEMORY_LIBRARY_PATH.exists():
            json_file(MEMORY_LIBRARY_PATH, "library")
        for path in sorted(PHONE_DIR.glob("*.json")) if PHONE_DIR.exists() else []:
            json_file(path, "phone")
        for path in sorted(USER_DIR.glob("*.json")) if USER_DIR.exists() else []:
            json_file(path, "users")
        paths = [EVENT_ARCHIVE_PATH, INSIGHT_ARCHIVE_PATH]
        if EVENT_SESSION_DIR.exists():
            paths.extend(sorted(EVENT_SESSION_DIR.glob("*/events.jsonl")))
        for path in paths:
            if not path.exists():
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            out = []
            for line in lines:
                try:
                    rec = json.loads(line)
                except Exception:
                    out.append(line)
                    continue
                out.append(json.dumps(self._scrub_tree(rec, scrub), ensure_ascii=False))
            if out != lines:
                archive(path)
                tmp = path.with_suffix(".tmp")
                tmp.write_text("".join(x + "\n" for x in out), encoding="utf-8")
                os.replace(str(tmp), str(path))
                counts["events"] = counts.get("events", 0) + 1
        if isinstance(getattr(self, "self_model", None), dict):
            new = self._scrub_tree(self.self_model, scrub)
            if new != self.self_model:
                if SELF_MODEL_PATH.exists():
                    archive(SELF_MODEL_PATH)
                self.self_model = new
                self._save_self_model()
                counts["notes"] = 1
        if counts:
            logger.info("[ams-life] numbers taken out of what she keeps: %s files", counts)
        return counts

    def _red_line(self, text, what="") -> str:
        """The red line (health, money, love life, family...) `text` crosses, when it must not
        be kept for it: only while the switch redline_filter is on (off by default: nothing is
        held back). Nothing is recorded of a hit; the panel counts what is kept now
        (_red_line_census)."""
        if not getattr(self, "redline_filter", False):
            return ""
        line = redline.hit(text)
        if line:
            logger.info("[ams-life] not kept (%s): red line %s", what, line)
        return line

    def _red_lines_for(self, what):
        """_red_line as impressions.py takes it: text -> the line it may not cross, or ''."""
        return lambda text: self._red_line(text, what)

    def _sweep_red_lines(self) -> dict:
        """With the switch on, at start: what was kept before that crosses a red line goes --
        memories, events and insights, her notes. Each file that changes is copied into
        MEMORY_ARCHIVE_DIR first, so turning the switch on loses nothing for good. Off: nothing."""
        if not getattr(self, "redline_filter", False):
            return {}
        stamp = time.strftime("%Y%m%d-%H%M%S")
        counts = {}

        def archive(path, name):
            dest = MEMORY_ARCHIVE_DIR / name if path == MEMORY_LIBRARY_PATH else \
                MEMORY_ARCHIVE_DIR / ("before-redline-" + stamp) / path.relative_to(DATA_DIR)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(path), str(dest))

        if MEMORY_LIBRARY_PATH.exists():
            lib = self._read_library()
            keep = [e for e in lib["entries"] if not (isinstance(e, dict) and redline.hit(e.get("text")))]
            if len(keep) != len(lib["entries"]):
                archive(MEMORY_LIBRARY_PATH, "library.before-redline-%s.json" % stamp)
                counts["memory"] = len(lib["entries"]) - len(keep)
                lib["entries"] = keep
                self._write_library(lib)
        for path, what in ((EVENT_ARCHIVE_PATH, "event"), (INSIGHT_ARCHIVE_PATH, "insight")):
            if not path.exists():
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            kept = []
            for line in lines:
                try:
                    rec = json.loads(line)
                except Exception:
                    kept.append(line)
                    continue
                text = " ".join(str(rec.get(k) or "") for k in self._KEPT_TEXT_KEYS) if isinstance(rec, dict) else ""
                if not redline.hit(text):
                    kept.append(line)
            if len(kept) != len(lines):
                archive(path, "")
                tmp = path.with_suffix(".tmp")
                tmp.write_text("".join(x + "\n" for x in kept), encoding="utf-8")
                os.replace(str(tmp), str(path))
                counts[what] = len(lines) - len(kept)
        if isinstance(getattr(self, "self_model", None), dict):
            dropped = sum(1 for key in ("notebook", "narrative_items", "diary", "relationship_narratives")
                          for x in self.self_model.get(key) or [] if isinstance(x, dict) and redline.hit(x.get("text")))
            if dropped:
                if SELF_MODEL_PATH.exists():
                    archive(SELF_MODEL_PATH, "")
                self._save_self_model()  # its red-line check drops them
                counts["notes"] = dropped
        if counts:
            logger.info("[ams-life] red lines on: taken out of what she kept (copies archived first): %s", counts)
        return counts

    def _anonymized(self, text, names) -> str:
        """`text` without any name of the people in `names` (ids or names): each id brings
        every name that person is known by."""
        return discretion.anonymize(text, self._known_names(names))

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
                names = self._known_names(discretion.names_in(ev))
                ev = dict(ev)
                for key in _EVENT_TEXT_FIELDS:
                    if ev.get(key):
                        ev[key] = discretion.anonymize(ev[key], names)
            out.append(ev)
        return out

    # ------------------------------------------------------------------
    # Her self-description and the speaker's relationship record.
    # ------------------------------------------------------------------
    def _notebook_for(self, event) -> list:
        """Her notebook as she may bring it up here: each entry by its origin (private ones
        only in that private chat, others' public ones without names, her own anywhere)."""
        here = self._here(event)
        lines = []
        for item in (self.self_model or {}).get("notebook") or []:
            if not isinstance(item, dict):
                continue
            v = discretion.verdict(discretion.origin_of(item), here)
            if v == discretion.DROP:
                continue
            text = str(item.get("text") or "")
            if v == discretion.ANON:
                text = self._anonymized(text, discretion.origin_of(item)["people"] + list(item.get("names") or []))
            if text:
                lines.append(text)
        return lines

    def _self_model_for(self, event) -> dict:
        """Self model as seen from here: "narrative" is her notebook, only the entries
        allowed here (used for goal relevance)."""
        model = dict(self.self_model or {})
        model["narrative"] = "；".join(self._notebook_for(event))[:600]
        return model

    def _owner_rules(self) -> list:
        """The owner's rules, written in the panel; every chat's reply sees them."""
        try:
            if OWNER_RULES_PATH.exists():
                data = json.loads(OWNER_RULES_PATH.read_text(encoding="utf-8"))
                rules = data.get("rules") if isinstance(data, dict) else []
                return [str(x)[:OWNER_RULES_CHARS] for x in (rules or []) if str(x or "").strip()][:OWNER_RULES_MAX]
        except Exception as exc:
            logger.warning("[ams-life] owner rules read failed: %s", exc)
        return []

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
    def _forget(self, person: str = "", source_ids=None, entry_ids=None) -> dict:
        """Delete every memory, event, note and phone line that came from `person`
        (or from one of `source_ids`; or the memories `entry_ids`), and his relationship
        record. Deleting by message also takes what is written in the relationship
        records of the people those messages involve (sub-records from those messages,
        and any without a source; the numbers stay), the descriptions of pictures in
        what was deleted, and the dedupe log rows of deleted events.

        Returns counts per store (memories, events, insights, relationship, notes incl. her
        notebook, phone) and the places something was deleted from. Files moved aside by
        the one-her migration (per-session legacy/archive folders) and the archive
        copies of the library are not touched here. Every call is logged; the log
        length is the forget count (see _job_stale).
        """
        person = str(person or "").strip()
        ids = [str(x) for x in (source_ids or []) if str(x or "").strip()]
        entry_ids = {str(x) for x in (entry_ids or []) if str(x or "").strip()}
        if not person and not ids and not entry_ids:
            return {}
        if not isinstance(getattr(self, "_forget_log", None), list):
            self._forget_log = []
        his_names = [n for n in self._known_names([person]) if len(n) >= 2] if person else []
        if person and isinstance(getattr(self, "_name_index", None), dict):
            self._name_index.pop(person, None)
        self._forget_log.append((person, list(ids)))
        counts = {"memories": 0, "events": 0, "relationship": 0, "notes": 0, "phone": 0, "insights": 0}
        places, involved, pictures, gone_events = set(), set(), set(), set()

        def about(item):
            return discretion.is_about(discretion.origin_of(item), person, ids)

        def note(item):
            o = discretion.origin_of(item)
            if o["where"]:
                places.add(o["where"])
            involved.update(str(x) for x in o["people"])
            for a in item.get("attachments") or []:
                if isinstance(a, dict) and a.get("ref"):
                    pictures.add(str(a["ref"]))

        def entry_gone(e):
            return isinstance(e, dict) and (about(e) or (entry_ids and _memory_entry_id_of(e) in entry_ids))

        # 1) the memory library (and the person's private room)
        lib = self._read_library()
        gone = {str(e.get("id") or "") for e in lib["entries"] if entry_gone(e)}
        for e in lib["entries"]:
            if entry_gone(e):
                note(e)
        keep = [e for e in lib["entries"] if not entry_gone(e)]
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
        library_written = self._write_library(lib) if counts["memories"] or person else True

        # 2) the event archive and its per-place copies, and the insights drawn from events
        paths = [EVENT_ARCHIVE_PATH, INSIGHT_ARCHIVE_PATH]
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
                    note(rec)
                    if rec.get("id"):
                        gone_events.add(str(rec["id"]))
                    continue
                kept.append(line)
            if dropped:
                tmp = path.with_suffix(".tmp")
                tmp.write_text("".join(x + "\n" for x in kept), encoding="utf-8")
                os.replace(str(tmp), str(path))
                if path == EVENT_ARCHIVE_PATH:
                    counts["events"] += dropped
                elif path == INSIGHT_ARCHIVE_PATH:
                    counts["insights"] = dropped

        # 3) his relationship record
        if person:
            safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in person)[:60]
            upath = USER_DIR / (safe + ".json")
            if upath.exists():
                upath.unlink()
                counts["relationship"] = 1

        # 4) her notes about him (narrative lines, diary, relationship narratives)
        changed = False
        for key in ("narrative_items", "diary", "relationship_narratives", "notebook"):
            items = self.self_model.get(key)
            if not isinstance(items, list):
                continue
            kept_items = [x for x in items if not (isinstance(x, dict) and about(x))]
            for x in items:
                if isinstance(x, dict) and about(x):
                    note(x)
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
                for x in win[key]:
                    if isinstance(x, dict) and about(x):
                        note(x)
                kept_items = [x for x in win[key] if not (isinstance(x, dict) and about(x))]
                if len(kept_items) != len(win[key]):
                    counts["phone"] += len(win[key]) - len(kept_items)
                    win[key] = kept_items
                    changed = True
            if changed:
                self._write_window(place, win)
        if person and (counts["phone"] or counts["relationship"]):
            places.add("private:" + person)

        # 6) what the relationship records of the people involved say: by message, those of
        #    the people in what was deleted; a person, every record that names him (BioCore
        #    draws the topics and sources in a record from the whole chat)
        others = set(involved) - {person, "self", ""}
        if person and USER_DIR.exists():
            for upath in USER_DIR.glob("*.json"):
                try:
                    rec = json.loads(upath.read_text(encoding="utf-8"))
                except Exception:
                    continue
                if isinstance(rec, dict) and self._record_mentions(rec, person, his_names):
                    others.add(str(rec.get("sender_id") or upath.stem))
        if others:
            counts["relationship_text"] = self._forget_relationship_text(
                others - {person}, set(ids) | gone | gone_events)

        # 7) what she thinks of the people in each group: a person, in every group; by
        #    message, what the model wrote about its authors there (it may come from it)
        if hasattr(self, "_impression_store"):
            store = self._impression_store()
            if person:
                counts["impressions"] = store.forget_person(person)
            for place in places:
                if place.startswith("group:"):
                    for who in involved - {person, "self", ""}:
                        if (ids or entry_ids) and store.forget_message_by(place, who):
                            counts["impressions"] = counts.get("impressions", 0) + 1

        # 8) what else may hold their words: picture descriptions, the dedupe log, the
        #    in-process vector cache (texts as keys)
        counts["pictures"] = self._forget_pictures(pictures)
        self._forget_dedupe_rows(gone_events)
        EMBED_CACHE.clear()

        self._refresh_loop_pressure(self._core(None))
        counts["places"] = sorted(p for p in places if p)
        logger.info("[ams-life] forgot person=%s sources=%d entries=%d: %s", "yes" if person else "no",
                    len(ids), len(entry_ids), {k: v for k, v in counts.items() if k != "places"})
        if not library_written:
            # registered all the same: it goes the next time the library is written
            raise forget_registry.Unreadable("the forget registry could not be read: the memory library was not "
                                             "changed (everything else was deleted); try again")
        return counts

    def _forget_registered(self) -> dict:
        """After the data folder was restored from a backup (the registry itself never is:
        the one in use stays), delete again what the owner deleted in the panel -- the people
        (everywhere) and the messages -- so nobody deleted comes back with an older backup.
        Other rows (a person forgotten in one group, an optout someone ended, a cutoff) are
        narrower than a whole delete: they are left to the registry, as every write is."""
        reg = self._registry()
        rows = [r for r in reg.rows() if str(r["note"] or "").startswith("owner:")]
        people = sorted({r["qq"] for r in rows if r["kind"] == "qq" and r["place"] == forget_registry.EVERYWHERE
                         and r["qq"] != "*"})
        sources = sorted({r["source_id"] for r in rows if r["kind"] == "source" and r["source_id"]})
        for person in people:
            self._forget(person=person)
        if sources:
            self._forget(source_ids=sources)
        if hasattr(self, "_impression_store"):
            for qq in sorted({r["qq"] for r in rows if r["kind"] == "impression"}):
                self._impression_store().forget_impression(qq)
        if not self._write_library(self._read_library()):   # rows for everyone in a place
            raise forget_registry.Unreadable("the forget registry could not be read")
        return {"people": len(people), "messages": len(sources)}

    _REL_TEXT_LISTS = ("we_memory", "annotations", "milestones")
    _REL_TEXT_MAPS = ("transactive_map", "destination_map", "social_world")
    # names that are everyday words: a record "mentions" such a person only by his number or
    # in a name field, never because the word turns up in what was said
    _EVERYDAY_WORDS = {"哈哈", "哈哈哈", "嘿嘿", "嗯嗯", "好的", "可以", "你好", "什么", "这个", "那个", "大家",
                       "真的", "没有", "就是", "然后", "知道", "有人", "某人"}

    def _record_mentions(self, rec, person, names) -> bool:
        """Does someone else's relationship record draw from `person`? Only its name and text
        fields are looked at (never timestamps or counts): his number as a whole number, his
        names in name fields, and in text only names that are not everyday words."""
        rel = rec.get("relationship") if isinstance(rec.get("relationship"), dict) else {}
        texts, name_fields, ids = [], [], []

        def take(x):
            if isinstance(x, dict):
                texts.extend(str(x.get(k) or "") for k in ("text", "key", "title", "latest_text"))
                texts.extend(str(ev.get("text") or "") for ev in x.get("evidence") or [] if isinstance(ev, dict))
                name_fields.append(str(x.get("sender_name") or x.get("name") or ""))
                ids.append(str(x.get("sender_id") or x.get("qq") or ""))
            elif isinstance(x, str):
                texts.append(x)
        for key in self._REL_TEXT_LISTS + self._REL_TEXT_MAPS:
            value = rel.get(key)
            if isinstance(value, dict):
                for k, v in value.items():
                    texts.append(str(k))
                    take(v)
            elif isinstance(value, list):
                for v in value:
                    take(v)
        if person in ids or person in name_fields:
            return True
        number = re.compile(r"(?<![0-9])%s(?![0-9])" % re.escape(person))
        if any(number.search(t) for t in texts):
            return True
        names = [n for n in names if len(n) >= 2 and not n.isdigit()]
        if any(n in name_fields for n in names):
            return True
        return any(n in t for n in names if n not in self._EVERYDAY_WORDS for t in texts)

    def _forget_relationship_text(self, people, refs) -> int:
        """Relationship records of `people`: drop sub-records that came from `refs` (message,
        memory or event ids) and any that do not say where they came from; the words drawn
        from memories (topics, sources, people around him) go too and are rebuilt from what
        is left. The numbers (state, trajectory, counts) stay."""
        dropped = 0
        refs = {str(x) for x in refs if str(x or "")}
        for who in sorted(people):
            safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(who))[:60]
            path = USER_DIR / (safe + ".json")
            if not path.exists():
                continue
            try:
                d = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            rel = d.get("relationship") if isinstance(d, dict) else None
            if not isinstance(rel, dict):
                continue
            changed = False
            for key in self._REL_TEXT_LISTS:
                items = rel.get(key)
                if not isinstance(items, list):
                    continue
                kept = []
                for x in items:
                    own = set()
                    if isinstance(x, dict):
                        own = {str(r) for r in list(x.get("source_ids") or []) + list(x.get("evidence_refs") or [])}
                    if own and not (own & refs):
                        kept.append(x)
                if len(kept) != len(items):
                    dropped += len(items) - len(kept)
                    rel[key] = kept
                    changed = True
            for key in self._REL_TEXT_MAPS:
                if rel.get(key):
                    rel[key] = [] if isinstance(rel.get(key), list) else {}
                    changed = True
            if changed:
                path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        return dropped

    def _forget_pictures(self, refs) -> int:
        """Descriptions of the pictures that were in what was deleted."""
        if not refs or not IMAGE_CACHE_PATH.exists():
            return 0
        cache = self._load_image_cache()
        keys = {_sha256(r) for r in refs} | {k for k, v in cache.items()
                                             if isinstance(v, dict) and str(v.get("ref") or "") in refs}
        gone = [k for k in keys if k in cache]
        for k in gone:
            cache.pop(k, None)
        if gone:
            IMAGE_CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        return len(gone)

    def _forget_dedupe_rows(self, event_ids) -> None:
        """The one-time dedupe log keeps event titles: its rows about deleted events go."""
        path = EVENT_ARCHIVE_DIR / "dedupe_log.jsonl"
        if not event_ids or not path.exists():
            return
        kept = []
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except Exception:
                kept.append(line)
                continue
            if isinstance(row, dict) and {str(row.get("kept_id") or ""), str(row.get("dropped_id") or "")} & set(event_ids):
                continue
            kept.append(line)
        tmp = path.with_suffix(".tmp")
        tmp.write_text("".join(x + "\n" for x in kept), encoding="utf-8")
        os.replace(str(tmp), str(path))

    # ------------------------------------------------------------------
    # The owner's deletes (panel only; never from a chat).
    # ------------------------------------------------------------------
    def _owner_forget_person(self, person) -> dict:
        """Delete a person everywhere and register it, so nothing of his is kept again."""
        person = str(person or "").strip()
        if not person:
            return {}
        self._registry().owner_delete(person=person)
        return self._forget(person=person)

    def _owner_forget_memory(self, entry_id) -> dict:
        """Delete one memory: it, and everything else that came from the messages it came
        from (registered, so they are not kept again). None when there is no such memory."""
        entry_id = str(entry_id or "").strip()
        lib = self._read_library()
        target = next((e for e in lib["entries"] if isinstance(e, dict) and _memory_entry_id_of(e) == entry_id), None)
        if not entry_id or target is None:
            return None
        o = discretion.origin_of(target)
        if o["source_ids"]:
            self._registry().owner_delete(source_ids=o["source_ids"], place=o["where"] or forget_registry.EVERYWHERE)
        return self._forget(source_ids=o["source_ids"], entry_ids=[entry_id])

    def _place_umos(self) -> dict:
        """place -> AstrBot's id of that chat, as her phone last saw it."""
        out = {}
        for place in self._window_places():
            umo = str(self._read_window(place).get("umo") or "")
            if umo:
                out[place] = umo
        return out

    async def _forget_in_astrbot(self, person, umos) -> dict:
        """What AstrBot itself keeps of a deleted person, through its public interfaces:
        the conversation of his private chat, and his rows in the platform message
        history (off by default). `umos`: place -> AstrBot's chat id, taken before the
        phone was cleared. The group context buffer has no public interface and is not
        touched (it holds at most the last messages of each group, in memory)."""
        out = {"conversations": 0, "message_history": 0}
        person = str(person or "").strip()
        if not person:
            return out
        conv = getattr(self.context, "conversation_manager", None)
        for umo in [u for p, u in sorted(umos.items()) if p == "private:" + person]:
            try:
                if conv is not None:
                    await conv.delete_conversations_by_user_id(umo)
                    out["conversations"] += 1
            except Exception as exc:
                logger.warning("[ams-life] astrbot conversation delete failed: %s", exc)
        hist = getattr(self.context, "message_history_manager", None)
        if hist is not None:
            for _place, umo in sorted(umos.items()):
                platform_id = str(umo).split(":", 1)[0]
                try:
                    page = 1
                    while page <= 50:
                        rows = await hist.get(platform_id, umo, page=page, page_size=200)
                        if not rows:
                            break
                        mine = [row for row in rows if str(getattr(row, "sender_id", "") or "") == person]
                        for row in mine:
                            await hist.delete_by_id(getattr(row, "id"))
                            out["message_history"] += 1
                        if not mine:
                            page += 1  # what was deleted moved the later rows up a page
                except Exception as exc:
                    logger.warning("[ams-life] astrbot message history delete failed: %s", exc)
        return out
