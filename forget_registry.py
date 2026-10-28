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

One SQLite table, append-only, read in order (and two small ones, see below):

    kind      place               qq      source_id   stamp
    'qq'      'group:1' or '*'    10001   -           t    a person: all of his up to t is gone
    'source'  'group:1' or '*'    -       m123        t    one message
    'optout'  ...                 10001   -           t    nothing of his from t on
    'optin'   ...                 10001   -           t    ends an optout

``place`` is a place as discretion.place_of() writes it; '*' means everywhere.
A 'qq' row with qq '*' forgets everyone in that place up to t. The old companion
also let people opt out and back in themselves; those kinds are kept so its
registries convert as they are, but nothing new writes them. An 'impression' row
(the owner deleted what she thinks of someone, not the person) only stops her
writing an impression of him again; it does not touch anything else.

What a 'qq' row means for what the person says *later* is a way of reading the
rows, not part of them:

    FORGET_ME_OPTOUT (default): it also keeps everything after it out, until an 'optin';
    FORGET_ME_CUTOFF:           only what came before is gone (the old companion).

What a person deleted from the panel was called (the discussion window, 10-29): when the
owner deletes someone, every name she knew him by then goes in as a salted hash with his
number (``names``; the salt is in ``meta``, next to it), never the name itself. Someone
else saying one of those names later is found by names_in(): every stretch of a text of a
stored length is hashed and looked up. So what she keeps and what the nightly jobs show a
model never has the name of someone deleted, after a restart too -- the same intent as his
number in the rows above: remembering whom she no longer keeps.

Only the standard library; no AstrBot.
"""
from __future__ import annotations

import hashlib
import re
import secrets
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


KINDS = ("qq", "source", "optout", "optin", "impression")
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
CREATE TABLE IF NOT EXISTS names (
    qq     TEXT NOT NULL,
    digest TEXT NOT NULL,
    size   INTEGER NOT NULL,
    stamp  REAL NOT NULL,
    PRIMARY KEY (qq, digest)
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
"""
NAME_MIN, NAME_MAX = 2, 24
_ASCII_WORD = re.compile(r"[0-9A-Za-z]")


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

    @classmethod
    def copy_of(cls, rows):
        """A registry in memory holding these rows (as rows() gives them). SQLite lets a
        registry be read only in the thread that opened it; work in another thread makes
        its own copy there."""
        reg = cls(None)
        reg._db.executemany("INSERT INTO forget (seq, kind, place, qq, source_id, stamp, note) VALUES (?,?,?,?,?,?,?)",
                            [(r["seq"], r["kind"], r["place"], r["qq"], r["source_id"], r["stamp"], r["note"])
                             for r in rows])
        reg._db.commit()
        return reg

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

    def stop_impression(self, qq, place=EVERYWHERE, stamp=None, note="owner:panel") -> int:
        """No impression of `qq` (in `place`) from now on: the owner deleted it in the panel."""
        return self.add("impression", place, qq=qq, stamp=stamp, note=note)

    def impression_allowed(self, qq, place="") -> bool:
        place = "" if not place else norm_place(place)
        return not any(_covers(row_place, place) for (row_place,) in self._db.execute(
            "SELECT place FROM forget WHERE kind='impression' AND qq=?", (str(qq or "").strip(),)))

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

    def may_keep_untimed(self, qq, place="") -> bool:
        """For something of his with no time (an old name): only when no reading of the rows
        and no time rules him out here -- anyone with a row is left out."""
        return self.may_keep(qq, place, forget_me=FORGET_ME_OPTOUT) and self.may_keep(qq, place, at=0)

    def may_keep_all(self, people=(), place="", at=None, source_ids=(), forget_me=None) -> bool:
        """For something made from several messages: every person and every message must be allowed."""
        if any(self.why_not(source_id=s, place=place, at=at, forget_me=forget_me) for s in (source_ids or ())):
            return False
        return not any(self.why_not(qq=p, place=place, at=at, forget_me=forget_me) for p in (people or ()))

    # ------------------------------------------------------------------
    # What a person deleted from the panel was called (hashes only)
    # ------------------------------------------------------------------
    def _salt(self) -> str:
        row = self._db.execute("SELECT value FROM meta WHERE key='name_salt'").fetchone()
        if row:
            return str(row[0])
        salt = secrets.token_hex(16)
        self._db.execute("INSERT INTO meta (key, value) VALUES ('name_salt', ?)", (salt,))
        self._db.commit()
        return salt

    @staticmethod
    def _digest(salt, name) -> str:
        return hashlib.sha256(("%s|%s" % (salt, name)).encode("utf-8")).hexdigest()[:32]

    def remember_names(self, qq, names, stamp=None) -> int:
        """The names `qq` went by, as salted hashes (2 to 24 characters, not all digits, not his
        number; lower case, so "Tom" is "tom" too). Returns how many were new."""
        qq = str(qq or "").strip()
        names = {str(n).strip().lower() for n in names or () if str(n or "").strip()}
        names = {n for n in names if NAME_MIN <= len(n) <= NAME_MAX and not n.isdigit() and n != qq}
        if not qq or not names:
            return 0
        salt, stamp = self._salt(), float(time.time() if stamp is None else stamp)
        before = self._db.total_changes
        self._db.executemany("INSERT OR IGNORE INTO names (qq, digest, size, stamp) VALUES (?,?,?,?)",
                             [(qq, self._digest(salt, n), len(n), stamp) for n in sorted(names)])
        self._db.commit()
        self._names_cache = None
        return self._db.total_changes - before

    def _name_table(self) -> tuple:
        """(salt, {size: {digest: qq}}), reread when the table grows."""
        count = int(self._db.execute("SELECT COUNT(*) FROM names").fetchone()[0])
        cache = getattr(self, "_names_cache", None)
        if cache and cache[0] == count:
            return cache[1], cache[2]
        table = {}
        for qq, digest, size in self._db.execute("SELECT qq, digest, size FROM names"):
            table.setdefault(int(size), {})[str(digest)] = str(qq)
        salt = self._salt() if table else ""
        self._names_cache = (count, salt, table)
        return salt, table

    def names_in(self, text) -> dict:
        """{name: qq} for every stretch of `text` that is a stored name (a name of letters and
        digits only where it stands as a word of its own; one that is an everyday word only
        where it plainly means someone, see discretion.plain_word)."""
        text = str(text or "")
        salt, table = self._name_table()
        out = {}
        for size, digests in table.items():
            for i in range(len(text) - size + 1):
                part = text[i:i + size]
                qq = digests.get(self._digest(salt, part.lower()))
                if not qq:
                    continue
                if part.isascii() and ((i and _ASCII_WORD.match(text[i - 1]))
                                       or (i + size < len(text) and _ASCII_WORD.match(text[i + size]))):
                    continue
                if discretion.plain_word(part) and not discretion._one_char_name(part).search(text):
                    continue   # an everyday word: only where it plainly means someone
                out[part] = qq
        return out

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
