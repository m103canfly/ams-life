# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The forget registry: who and what she must not keep, from now on.

No one can make her forget by saying so in a chat (the owner's decision). What
goes in here:
- what the old companion was asked to forget: it stays forgotten, so the import
  of its data and the replay of old chat logs leave it out;
- what the owner deletes from the panel (a person, or one memory): the panel
  calls owner_delete(), and the plugin deletes with ``_forget``. This file
  remembers *that* it was deleted, so nothing comes back later: a message that
  arrives afterwards, a replay, an import.

One SQLite table, append-only, read in order:

    kind      place               qq      source_id   stamp
    'qq'      'group:1' or '*'    10001   -           t    a person: all of his up to t is gone
    'source'  'group:1' or '*'    -       m123        t    one message
    'optout'  ...                 10001   -           t    nothing of his from t on
    'optin'   ...                 10001   -           t    ends an optout

``place`` is a place as discretion.place_of() writes it; '*' means everywhere.
A 'qq' row with qq '*' forgets everyone in that place up to t. The old companion
also let people opt out and back in themselves; those kinds are kept so its
registries convert as they are, but nothing new writes them.

What a 'qq' row means for what the person says *later* is a way of reading the
rows, not part of them:

    FORGET_ME_OPTOUT (default): it also keeps everything after it out, until an 'optin';
    FORGET_ME_CUTOFF:           only what came before is gone (the old companion).

Only the standard library; no AstrBot.
"""
from __future__ import annotations

import sqlite3
import time
from contextlib import closing
from pathlib import Path

try:
    from . import discretion
except ImportError:
    import discretion

FILE_NAME = "forget_registry.sqlite3"


class Unreadable(Exception):
    """The registry could not be read (locked, damaged, ...). Whatever was about to be written
    is not written; nothing already kept is dropped because of it."""

KINDS = ("qq", "source", "optout", "optin")
EVERYWHERE = "*"
FORGET_ME_OPTOUT, FORGET_ME_CUTOFF = "optout", "cutoff"
FORGET_ME = FORGET_ME_OPTOUT

_SCHEMA = """
CREATE TABLE IF NOT EXISTS forget (
    seq       INTEGER PRIMARY KEY AUTOINCREMENT,
    kind      TEXT NOT NULL,
    place     TEXT NOT NULL DEFAULT '*',
    qq        TEXT NOT NULL DEFAULT '',
    source_id TEXT NOT NULL DEFAULT '',
    stamp     REAL NOT NULL,
    note      TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS forget_qq ON forget (qq);
CREATE INDEX IF NOT EXISTS forget_source ON forget (source_id);
"""


def norm_place(place) -> str:
    """'*' stays '*'; anything else goes through discretion.place_of ('default:GroupMessage:1' -> 'group:1')."""
    text = str(place or "").strip()
    if not text or text == EVERYWHERE:
        return EVERYWHERE
    return discretion.place_of(text) or text


def _covers(row_place, place) -> bool:
    return row_place == EVERYWHERE or not place or row_place == place


class ForgetRegistry:
    """Open (or create) the registry at `path`; path None keeps it in memory (tests)."""

    def __init__(self, path=None):
        self.path = Path(path) if path else None
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(self.path) if self.path else ":memory:")
        self._db.executescript(_SCHEMA)
        self._db.commit()

    def close(self) -> None:
        self._db.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------
    def add(self, kind, place=EVERYWHERE, qq="", source_id="", stamp=None, note="") -> int:
        """Append one row; returns its seq, or 0 when the same row is already there."""
        if kind not in KINDS:
            raise ValueError("unknown kind: %r" % (kind,))
        place, qq, source_id = norm_place(place), str(qq or "").strip(), str(source_id or "").strip()
        if kind == "source" and not source_id:
            raise ValueError("a 'source' row needs a source_id")
        if kind != "source" and not qq:
            raise ValueError("a %r row needs a qq" % (kind,))
        stamp = float(time.time() if stamp is None else stamp)
        if kind == "source":
            # forgetting the same message twice changes nothing
            dup = self._db.execute("SELECT 1 FROM forget WHERE kind='source' AND place=? AND source_id=?",
                                   (place, source_id)).fetchone()
        else:
            dup = self._db.execute("SELECT 1 FROM forget WHERE kind=? AND place=? AND qq=? AND stamp=?",
                                   (kind, place, qq, stamp)).fetchone()
        if dup:
            return 0
        cur = self._db.execute("INSERT INTO forget (kind, place, qq, source_id, stamp, note) VALUES (?,?,?,?,?,?)",
                               (kind, place, qq, source_id, stamp, str(note or "")))
        self._db.commit()
        return int(cur.lastrowid)

    def owner_delete(self, person="", source_ids=(), place=EVERYWHERE, stamp=None) -> list:
        """The owner deleted a person (everywhere) or one memory (the messages it came from)
        from the panel. Returns the seqs written (0 for a row that was already there)."""
        seqs = []
        if str(person or "").strip():
            seqs.append(self.forget_person(person, EVERYWHERE, stamp=stamp, note="owner:panel"))
        for sid in source_ids or ():
            if str(sid or "").strip():
                seqs.append(self.forget_message(sid, place, stamp=stamp, note="owner:panel"))
        return seqs

    def forget_person(self, qq, place=EVERYWHERE, stamp=None, note="") -> int:
        return self.add("qq", place, qq=qq, stamp=stamp, note=note)

    def forget_message(self, source_id, place=EVERYWHERE, stamp=None, note="") -> int:
        return self.add("source", place, source_id=source_id, stamp=stamp, note=note)

    def opt_out(self, qq, place=EVERYWHERE, stamp=None, note="") -> int:
        return self.add("optout", place, qq=qq, stamp=stamp, note=note)

    def opt_in(self, qq, place=EVERYWHERE, stamp=None, note="") -> int:
        return self.add("optin", place, qq=qq, stamp=stamp, note=note)

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------
    def rows(self, since=0) -> list:
        cur = self._db.execute("SELECT seq, kind, place, qq, source_id, stamp, note FROM forget WHERE seq>? ORDER BY seq",
                               (int(since),))
        keys = ("seq", "kind", "place", "qq", "source_id", "stamp", "note")
        return [dict(zip(keys, r)) for r in cur.fetchall()]

    def last_seq(self) -> int:
        return int(self._db.execute("SELECT COALESCE(MAX(seq), 0) FROM forget").fetchone()[0])

    def people(self) -> set:
        """Everyone with a 'qq' or 'optout' row anywhere (whatever came after)."""
        return {r[0] for r in self._db.execute("SELECT DISTINCT qq FROM forget WHERE kind IN ('qq','optout') AND qq<>'*'")}

    def why_not(self, qq="", place="", at=None, source_id="", forget_me=None) -> str:
        """Why something by `qq` (and/or message `source_id`), said in `place` at time `at`,
        may not be kept: 'source', 'forgotten', 'optout' -- or '' when it may.

        `place` '' matches every row (the strictest reading). `at` None means now.
        """
        mode = forget_me or FORGET_ME
        place = "" if not place else norm_place(place)
        at = float(time.time() if at is None else at)
        source_id, qq = str(source_id or "").strip(), str(qq or "").strip()
        if source_id:
            for (row_place,) in self._db.execute("SELECT place FROM forget WHERE kind='source' AND source_id=?",
                                                 (source_id,)):
                if _covers(row_place, place):
                    return "source"
        if not qq:
            return ""
        rows = [r for r in self._db.execute(
            "SELECT seq, kind, place, stamp, qq FROM forget WHERE kind<>'source' AND (qq=? OR (qq='*' AND kind='qq')) "
            "ORDER BY stamp, seq", (qq,)) if _covers(r[2], place)]
        # everything up to a 'qq' row is gone, whatever came later
        if any(kind == "qq" and at <= stamp for _seq, kind, _p, stamp, _q in rows):
            return "forgotten"
        # after that: the latest switch at or before `at` decides
        state = ""
        for _seq, kind, _p, stamp, who in rows:
            if stamp > at:
                break
            # "everyone here up to t" (old cutoffs) never reaches past t
            if kind == "optout" or (kind == "qq" and who != "*" and mode == FORGET_ME_OPTOUT):
                state = "optout"
            elif kind == "optin":
                state = ""
        return state

    def may_keep(self, qq="", place="", at=None, source_id="", forget_me=None) -> bool:
        """May she keep something by this person / from this message, said here at this time?"""
        return not self.why_not(qq, place, at, source_id, forget_me)

    def may_keep_all(self, people=(), place="", at=None, source_ids=(), forget_me=None) -> bool:
        """For something made from several messages: every person and every message must be allowed."""
        if any(self.why_not(source_id=s, place=place, at=at, forget_me=forget_me) for s in (source_ids or ())):
            return False
        return not any(self.why_not(qq=p, place=place, at=at, forget_me=forget_me) for p in (people or ()))

    def stats(self) -> dict:
        out = {k: 0 for k in KINDS}
        for kind, n in self._db.execute("SELECT kind, COUNT(*) FROM forget GROUP BY kind"):
            out[kind] = int(n)
        out["people"] = len(self.people())
        return out


# ----------------------------------------------------------------------
# The old companion plugin's registries (read only)
# ----------------------------------------------------------------------
def _read_only(path):
    return sqlite3.connect("file:" + Path(path).resolve().as_posix() + "?mode=ro&immutable=1", uri=True)


def _legacy_place(scope) -> str:
    """Old scopes: 'group:<id>' and 'default:GroupMessage:<id>' -> 'group:<id>';
    the notebook's 'private' (the owner's chat, no id) and '*' -> everywhere."""
    text = str(scope or "").strip()
    if not text or text in ("*", "private"):
        return EVERYWHERE
    if text.startswith("group:"):
        return text
    return norm_place(text)


def import_notebook_tombstones(reg, path, note="legacy:notebook") -> dict:
    """notebook-forget.sqlite3, table tombstones(seq, kind, scope, qq, source_id, ...).
    kind is 'qq' / 'source' / 'optout' / 'optin'; entry_id and fingerprint were never written."""
    counts = {"rows": 0, "added": 0, "already": 0, "skipped": 0}
    with closing(_read_only(path)) as db:
        for kind, scope, qq, source_id, stamp in db.execute(
                "SELECT kind, scope, qq, source_id, stamp FROM tombstones ORDER BY seq"):
            counts["rows"] += 1
            kind = str(kind or "")
            ok = (kind == "source" and source_id) or (kind in ("qq", "optout", "optin") and qq)
            if not ok:
                counts["skipped"] += 1
                continue
            seq = reg.add(kind, _legacy_place(scope), qq=qq or "", source_id=source_id or "",
                          stamp=float(stamp or 0), note=note)
            counts["added" if seq else "already"] += 1
    return counts


def import_ledger_registry(reg, path, note="legacy:ledger") -> dict:
    """forget-registry.sqlite3: forgotten(seq, scope, source_id, entry_id, stamp, store_uuid) and
    forget_cutoffs(seq, scope, qq, cutoff). A cutoff forgets that qq in that place up to the cutoff
    (qq '' = everyone there). Rows naming only an old archive entry, and the bare sequence markers
    the old plugin wrote next to each cutoff, have nothing to carry over."""
    counts = {"rows": 0, "added": 0, "already": 0, "skipped": 0, "entry_rows": 0}
    with closing(_read_only(path)) as db:
        for scope, source_id, entry_id, stamp in db.execute(
                "SELECT scope, source_id, entry_id, stamp FROM forgotten ORDER BY seq"):
            counts["rows"] += 1
            if source_id:
                seq = reg.add("source", _legacy_place(scope), source_id=source_id, stamp=float(stamp or 0), note=note)
                counts["added" if seq else "already"] += 1
            else:
                counts["entry_rows" if entry_id else "skipped"] += 1
        for scope, qq, cutoff in db.execute("SELECT scope, qq, cutoff FROM forget_cutoffs ORDER BY seq"):
            counts["rows"] += 1
            seq = reg.add("qq", _legacy_place(scope), qq=str(qq or "") or "*", stamp=float(cutoff or 0), note=note)
            counts["added" if seq else "already"] += 1
    return counts
