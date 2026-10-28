# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Memory vectors in their own SQLite file, out of memory/library.json.

A 1024-number vector written as JSON text is about nine tenths of every memory
entry, and the library is read and written whole several times a turn. Kept
here instead, one row per memory entry id, the numbers stored exactly (doubles),
so recall comes out the same.

- get / get_many, put / put_many, delete / delete_many, keep_only (drop vectors
  whose entries are gone);
- attach(entries) puts each entry's vector back on it for code that reads
  e["vector"]; detach(entries) takes them off into the store before the library
  is written;
- reads come from an in-memory copy, loaded again only when the file changed
  (another connection wrote it, or the file itself changed);
- migrate_library() moves the vectors of an existing library.json here, after
  copying the file into an archive folder (never deleted). Run again, it finds
  nothing to move and does nothing.

Ids are not unique yet: a new memory's id is a hash of its text, so the same words
said in two places share one, and her replies get none when they are written.
So only an entry whose id occurs once in the whole library has its vector here;
an entry without an id, or sharing its id, keeps its vector in the library as it
is. Deleting a vector likewise only happens once no entry uses that id any more.
Step 1, part 3-2 gives every memory its own id.

Wiring into the plugin (_load_memory / _save_memory, the trims, _forget) comes
with step 1, part 3-2: until then the plugin still reads vectors from the
library, so do not migrate a live data folder before that.

Only the standard library; no AstrBot.
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import time
from array import array
from collections import Counter
from pathlib import Path

FILE_NAME = "vectors.sqlite3"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS vectors (
    entry_id TEXT PRIMARY KEY,
    dims     INTEGER NOT NULL,
    data     BLOB NOT NULL
);
"""


def _pack(vector) -> bytes:
    return array("d", (float(x) for x in vector)).tobytes()


def _unpack(blob) -> list:
    a = array("d")
    a.frombytes(blob)
    return a.tolist()


def unique_ids(entries) -> set:
    """The ids that occur exactly once among `entries` (the whole library)."""
    count = Counter(str(e["id"]) for e in entries or [] if isinstance(e, dict) and e.get("id"))
    return {i for i, n in count.items() if n == 1}


def _used_ids(entries) -> set:
    return {str(e["id"]) for e in entries or [] if isinstance(e, dict) and e.get("id")}


class VectorStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(self.path))
        self._db.executescript(_SCHEMA)
        self._db.commit()
        self._cache = None
        self._stamp = None

    def close(self) -> None:
        self._db.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # ------------------------------------------------------------------
    # The in-memory copy
    # ------------------------------------------------------------------
    def _file_stamp(self):
        try:
            st = self.path.stat()
            file_part = (st.st_mtime_ns, st.st_size)
        except OSError:
            file_part = None
        version = self._db.execute("PRAGMA data_version").fetchone()[0]
        return file_part, version

    def _vectors(self) -> dict:
        stamp = self._file_stamp()
        if self._cache is None or stamp != self._stamp:
            self._cache = {eid: _unpack(blob) for eid, blob in self._db.execute("SELECT entry_id, data FROM vectors")}
            self._stamp = stamp
        return self._cache

    def _wrote(self) -> None:
        self._db.commit()
        self._stamp = self._file_stamp()  # our own write: the copy is already up to date

    # ------------------------------------------------------------------
    def get(self, entry_id):
        v = self._vectors().get(str(entry_id))
        return list(v) if v is not None else None

    def get_many(self, ids) -> dict:
        vectors = self._vectors()
        return {str(i): list(vectors[str(i)]) for i in ids if str(i) in vectors}

    def ids(self) -> set:
        return set(self._vectors())

    def __len__(self) -> int:
        return len(self._vectors())

    def put(self, entry_id, vector) -> None:
        self.put_many({entry_id: vector})

    def put_many(self, vectors) -> int:
        rows = [(str(k), len(v), _pack(v)) for k, v in dict(vectors).items() if str(k) and v]
        if not rows:
            return 0
        cache = self._vectors()
        self._db.executemany("INSERT OR REPLACE INTO vectors (entry_id, dims, data) VALUES (?,?,?)", rows)
        for eid, _dims, blob in rows:
            cache[eid] = _unpack(blob)
        self._wrote()
        return len(rows)

    def delete(self, entry_id, remaining=None) -> bool:
        return self.delete_many([entry_id], remaining) == 1

    def delete_many(self, ids, remaining=None) -> int:
        """Delete the vectors of `ids`. With `remaining` (the whole library after the deletion),
        an id some remaining entry still uses keeps its vector: ids are not unique yet."""
        cache = self._vectors()
        still = _used_ids(remaining) if remaining is not None else set()
        gone = [str(i) for i in ids if str(i) in cache and str(i) not in still]
        if not gone:
            return 0
        self._db.executemany("DELETE FROM vectors WHERE entry_id=?", [(i,) for i in gone])
        for i in gone:
            cache.pop(i, None)
        self._wrote()
        return len(gone)

    def keep_only(self, ids) -> int:
        """Delete every vector whose entry is not in `ids` (entries trimmed, merged or forgotten)."""
        keep = {str(i) for i in ids}
        return self.delete_many([i for i in self.ids() if i not in keep])

    # ------------------------------------------------------------------
    # For code that reads and writes e["vector"]
    # ------------------------------------------------------------------
    def attach(self, entries) -> list:
        """Put each entry's stored vector back on it (in place), unless it already carries one."""
        vectors = self._vectors()
        for e in entries or []:
            if isinstance(e, dict) and not e.get("vector") and str(e.get("id") or "") in vectors:
                e["vector"] = list(vectors[str(e["id"])])
        return entries

    def detach(self, entries) -> list:
        """Store the vectors and return copies of the entries without them, ready to be written.
        `entries` must be the whole library. Only new or changed vectors are written. An entry
        without an id, or whose id another entry also has, keeps its vector in the library."""
        stored = self._vectors()
        unique = unique_ids(entries)
        moving, out = {}, []
        for e in entries or []:
            if isinstance(e, dict) and str(e.get("id") or "") in unique and isinstance(e.get("vector"), list):
                eid = str(e["id"])
                if e["vector"] and stored.get(eid) != [float(x) for x in e["vector"]]:
                    moving[eid] = e["vector"]
                e = {k: v for k, v in e.items() if k != "vector"}
            out.append(e)
        self.put_many(moving)
        return out


def migrate_library(library_path, store_path, archive_dir) -> dict:
    """Move the vectors of library.json into the store at `store_path`.

    The library file is first copied into `archive_dir` (never deleted); then the vectors are
    stored, and only then is the library written again without them (a crash in between leaves
    them in both places, and running again finishes the job). Nothing to move: nothing is
    archived or written. Entries without an id, sharing their id with another entry, or with an
    empty vector, are left as they are."""
    library_path = Path(library_path)
    lib = json.loads(library_path.read_text(encoding="utf-8"))
    entries = lib.get("entries") if isinstance(lib, dict) else None
    entries = entries if isinstance(entries, list) else []
    unique = unique_ids(entries)
    moving = [e for e in entries if isinstance(e, dict) and str(e.get("id") or "") in unique
              and isinstance(e.get("vector"), list) and e["vector"]]
    counts = {"entries": len(entries), "moved": len(moving), "archived": "",
              "no_id": sum(1 for e in entries if isinstance(e, dict) and not e.get("id") and e.get("vector")),
              "shared_id": sum(1 for e in entries if isinstance(e, dict) and e.get("id")
                               and str(e["id"]) not in unique and e.get("vector")),
              "empty": sum(1 for e in entries if isinstance(e, dict) and e.get("vector") == [])}
    with VectorStore(store_path) as store:
        counts["already"] = sum(1 for e in entries if isinstance(e, dict) and str(e.get("id") or "") in store.ids()
                                and not e.get("vector"))
        if not moving:
            return counts
        archive_dir = Path(archive_dir)
        archive_dir.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        target = archive_dir / ("library.before-vectors-%s.json" % stamp)
        n = 1
        while target.exists():
            n += 1
            target = archive_dir / ("library.before-vectors-%s-%d.json" % (stamp, n))
        shutil.copy2(str(library_path), str(target))
        counts["archived"] = target.name
        store.put_many({str(e["id"]): e["vector"] for e in moving})
    for e in moving:
        e.pop("vector", None)
    tmp = library_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(lib, ensure_ascii=False), encoding="utf-8")
    os.replace(str(tmp), str(library_path))
    return counts
