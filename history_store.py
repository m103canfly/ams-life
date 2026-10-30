# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her side of the conversation, in its own SQLite file, one row per line.

A row says where it was said (`place`), who said it (`role`, `sender_id`,
`sender_name`, `message_id`), who it is about (`about`), which messages it came
from (`sources`) and when (`ts`). So a person can be forgotten line by line, and
so can a message; nothing has to be cleared whole.

- `append` writes one line, and keeps at most `keep_per_place` lines per place,
  dropping the oldest;
- `recent` gives the last lines of a place, oldest first, ready to be a model's
  `messages`;
- `forget_person` / `forget_messages` / `clear_place` delete for good:
  `PRAGMA secure_delete = ON` overwrites what is deleted, and the default journal
  leaves no copy in a WAL file;
- `gate`, when given, is asked before a line is written (the forget registry,
  once it is wired in, will refuse people and messages already forgotten);
- every change is committed, and an error (a broken file, a full disk) is raised
  as it is, never swallowed.

Wiring into the reply flow comes with step 1, part 5. Only the standard library;
no AstrBot and no plugin mixin.
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

KEEP_PER_PLACE = 200     # rows kept per place; the oldest go first
RECENT_DEFAULT = 20      # rows recent() gives when not told
ROLES = ("user", "assistant")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    place       TEXT NOT NULL,
    role        TEXT NOT NULL,
    content     TEXT NOT NULL,
    sender_id   TEXT NOT NULL DEFAULT '',
    sender_name TEXT NOT NULL DEFAULT '',
    message_id  TEXT NOT NULL DEFAULT '',
    about       TEXT NOT NULL DEFAULT '[]',
    sources     TEXT NOT NULL DEFAULT '[]',
    ts          REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS history_place ON history (place, id);
"""


def _text(value) -> str:
    """A trimmed string; None is empty."""
    return "" if value is None else str(value).strip()


def _ids(value) -> list:
    """Strings from a string or an iterable: trimmed, without empties or repeats."""
    if isinstance(value, str):
        value = (value,)
    out, seen = [], set()
    for item in value or ():
        text = str(item).strip()
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def _loads(value) -> list:
    """The list stored as JSON text; anything else is empty."""
    try:
        data = json.loads(value or "[]")
    except (TypeError, ValueError):
        return []
    return [str(x) for x in data] if isinstance(data, list) else []


class HistoryStore:
    def __init__(self, path, *, keep_per_place=KEEP_PER_PLACE, gate=None):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.keep_per_place = max(0, int(keep_per_place))
        self.gate = gate
        self._db = sqlite3.connect(str(self.path))
        # Deleted content is overwritten with zeros in the file, not just marked free.
        self._db.execute("PRAGMA secure_delete = ON")
        # The journal mode stays SQLite's default: a WAL file can keep what was deleted.
        self._db.executescript(_SCHEMA)
        self._db.commit()

    def close(self) -> None:
        self._db.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # ------------------------------------------------------------------
    def _trim(self, place) -> None:
        """Keep only the newest `keep_per_place` rows of one place."""
        self._db.execute(
            "DELETE FROM history WHERE place = ? AND id NOT IN"
            " (SELECT id FROM history WHERE place = ? ORDER BY id DESC LIMIT ?)",
            (place, place, self.keep_per_place))

    def _delete_ids(self, ids) -> int:
        ids = list(ids)
        for start in range(0, len(ids), 500):
            chunk = ids[start:start + 500]
            self._db.executemany("DELETE FROM history WHERE id = ?", [(i,) for i in chunk])
        if ids:
            self._db.commit()
        return len(ids)

    # ------------------------------------------------------------------
    def append(self, place, role, content, *, sender_id="", sender_name="", message_id="",
               about=(), sources=(), ts=None) -> int:
        """Write one line and return its id, or 0 when it is not written."""
        place = _text(place)
        role = _text(role)
        text = "" if content is None else str(content)
        if role not in ROLES or not place or not text.strip():
            return 0
        sender_id = _text(sender_id)
        people = _ids(about)
        if sender_id and sender_id not in people:
            people.append(sender_id)
        row = {
            "place": place,
            "role": role,
            "content": text,
            "sender_id": sender_id,
            "sender_name": "" if sender_name is None else str(sender_name),
            "message_id": _text(message_id),
            "about": people,
            "sources": _ids(sources),
            "ts": float(time.time() if ts is None else ts),
        }
        if self.gate is not None and not self.gate(row):
            return 0
        cur = self._db.execute(
            "INSERT INTO history (place, role, content, sender_id, sender_name,"
            " message_id, about, sources, ts) VALUES (?,?,?,?,?,?,?,?,?)",
            (row["place"], row["role"], row["content"], row["sender_id"], row["sender_name"],
             row["message_id"], json.dumps(row["about"], ensure_ascii=False),
             json.dumps(row["sources"], ensure_ascii=False), row["ts"]))
        row_id = int(cur.lastrowid)
        self._trim(place)
        self._db.commit()
        return row_id

    def recent(self, place, limit=RECENT_DEFAULT) -> list:
        """The last `limit` lines of a place, oldest first, as {"role", "content"}."""
        place = _text(place)
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            return []
        if not place or limit <= 0:
            return []
        rows = self._db.execute(
            "SELECT role, content FROM history WHERE place = ? ORDER BY id DESC LIMIT ?",
            (place, limit)).fetchall()
        return [{"role": role, "content": content} for role, content in reversed(rows)]

    def forget_person(self, person) -> int:
        """Delete every line a person said or is about (her replies to them too)."""
        person = _text(person)
        if not person:
            return 0
        gone = []
        for row_id, sender_id, about in self._db.execute("SELECT id, sender_id, about FROM history"):
            if sender_id == person or person in _loads(about):
                gone.append(int(row_id))
        return self._delete_ids(gone)

    def forget_messages(self, message_ids) -> int:
        """Delete every line that is one of these messages, or came from one of them."""
        wanted = set(_ids(message_ids))
        if not wanted:
            return 0
        gone = []
        for row_id, message_id, sources in self._db.execute("SELECT id, message_id, sources FROM history"):
            if message_id in wanted or wanted.intersection(_loads(sources)):
                gone.append(int(row_id))
        return self._delete_ids(gone)

    def clear_place(self, place) -> int:
        """Delete every line of one place; return how many."""
        cur = self._db.execute("DELETE FROM history WHERE place = ?", (_text(place),))
        self._db.commit()
        return int(cur.rowcount or 0)

    def places(self) -> list:
        """Every place with lines, sorted."""
        return sorted(place for (place,) in self._db.execute("SELECT DISTINCT place FROM history"))
