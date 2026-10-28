"""Memory vectors out of library.json (vector_store.py), on a made-up library."""
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import vector_store as vs  # noqa: E402


def vec(seed, dims=8):
    return [((seed * 7919 + i * 104729) % 1000) / 997.0 - 0.5 for i in range(dims)]


def library(n=5):
    entries = [{"id": "m%d" % i, "text": "第 %d 条记忆" % i, "vector": vec(i), "origin": {"where": "group:900001"}}
               for i in range(n)]
    entries.append({"id": "m-empty", "text": "删掉的", "vector": []})
    entries.append({"text": "没有编号", "vector": vec(99)})
    return {"entries": entries, "rooms": {"group:900001": {"working_set": ["m1"]}}, "schema_version": 3}


class Store(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / vs.FILE_NAME
        self.store = vs.VectorStore(self.path)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_put_get_delete(self):
        self.store.put("a", vec(1))
        self.store.put_many({"b": vec(2), "c": vec(3), "": vec(4), "d": []})
        self.assertEqual(self.store.get("a"), vec(1))                 # exactly, not rounded
        self.assertIsNone(self.store.get("z"))
        self.assertEqual(self.store.get_many(["a", "c", "z"]), {"a": vec(1), "c": vec(3)})
        self.assertEqual(self.store.ids(), {"a", "b", "c"})
        self.assertTrue(self.store.delete("a"))
        self.assertFalse(self.store.delete("a"))
        self.assertEqual(self.store.delete_many(["b", "z"]), 1)
        self.assertEqual(len(self.store), 1)
        self.store.put("c", vec(5))
        self.assertEqual(self.store.get("c"), vec(5))                  # replaced

    def test_returned_vectors_are_copies(self):
        self.store.put("a", vec(1))
        got = self.store.get("a")
        got[0] = 42.0
        self.assertEqual(self.store.get("a"), vec(1))

    def test_keep_only(self):
        self.store.put_many({"a": vec(1), "b": vec(2), "c": vec(3)})
        self.assertEqual(self.store.keep_only(["a", "c", "x"]), 1)
        self.assertEqual(self.store.ids(), {"a", "c"})

    def test_the_copy_follows_other_writers(self):
        self.store.put("a", vec(1))
        self.assertEqual(self.store.ids(), {"a"})
        db = sqlite3.connect(str(self.path))                           # someone else writes the file
        db.execute("INSERT INTO vectors VALUES (?,?,?)", ("b", 8, vs._pack(vec(2))))
        db.execute("DELETE FROM vectors WHERE entry_id='a'")
        db.commit()
        db.close()
        self.assertEqual(self.store.ids(), {"b"})
        self.assertEqual(self.store.get("b"), vec(2))
        with vs.VectorStore(self.path) as again:                       # and it is on disk
            self.assertEqual(again.get("b"), vec(2))

    def test_unchanged_file_is_not_read_again(self):
        self.store.put("a", vec(1))
        first = self.store._vectors()
        self.assertIs(self.store._vectors(), first)

    def test_attach_and_detach(self):
        entries = library()["entries"]
        written = self.store.detach(entries)
        self.assertEqual(self.store.ids(), {"m0", "m1", "m2", "m3", "m4"})
        self.assertTrue(all("vector" not in e for e in written if e.get("id")))
        self.assertEqual(written[-1]["vector"], vec(99))               # no id: keeps its vector
        self.assertEqual(entries[0]["vector"], vec(0))                 # the caller's entries are not changed
        back = self.store.attach(written)
        self.assertEqual(back[2]["vector"], vec(2))
        self.assertNotIn("vector", back[5])                            # empty one: nothing stored, nothing back
        own = [{"id": "m1", "vector": vec(50)}]
        self.assertEqual(self.store.attach(own)[0]["vector"], vec(50))  # an entry's own vector wins

    def test_deleting_entries_takes_their_vectors(self):
        entries = library()["entries"]
        self.store.detach(entries)
        kept = [e for e in entries if e.get("id") not in ("m1", "m3")]   # forgotten / trimmed
        self.store.keep_only(e.get("id") for e in kept if e.get("id"))
        self.assertEqual(self.store.ids(), {"m0", "m2", "m4"})


class SharedIds(unittest.TestCase):
    """Ids are not unique yet: an id is a hash of the text, so the same words in two groups share
    one, and her replies have none. Such entries keep their vectors in the library."""

    def test_two_entries_one_id_keep_their_own_vectors(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            lib_path, store_path = tmp / "library.json", tmp / vs.FILE_NAME
            entries = [{"id": "same", "text": "早安", "vector": vec(1), "origin": {"where": "group:900001"}},
                       {"id": "same", "text": "早安", "vector": vec(2), "origin": {"where": "group:900002"}},
                       {"id": "m9", "text": "别的", "vector": vec(9)}]
            lib_path.write_text(json.dumps({"entries": entries}, ensure_ascii=False), encoding="utf-8")
            counts = vs.migrate_library(lib_path, store_path, tmp / "archive")
            self.assertEqual((counts["moved"], counts["shared_id"]), (1, 2))
            lib = json.loads(lib_path.read_text("utf-8"))
            with vs.VectorStore(store_path) as store:
                self.assertEqual(store.ids(), {"m9"})
                back = store.attach(lib["entries"])
                self.assertEqual([e["vector"] for e in back], [vec(1), vec(2), vec(9)])
                written = store.detach(back)                       # and again on the next save
                self.assertEqual([e.get("vector") for e in written], [vec(1), vec(2), None])

    def test_deleting_one_of_two_keeps_the_others_vector(self):
        with tempfile.TemporaryDirectory() as tmp:
            with vs.VectorStore(Path(tmp) / vs.FILE_NAME) as store:
                first = {"id": "same", "text": "早安", "vector": vec(1)}
                store.detach([first])                              # stored while it was the only one
                second = {"id": "same", "text": "早安", "vector": vec(2)}
                library = store.detach([{"id": "same", "text": "早安"}, second])
                self.assertEqual(library[1]["vector"], vec(2))     # shared now: stays in the library
                # the first is deleted: the id is still used by the second, so its vector stays
                self.assertEqual(store.delete_many(["same"], remaining=[library[1]]), 0)
                self.assertEqual(store.attach([{"id": "same"}])[0]["vector"], vec(1))
                # the second is deleted instead: the first still gets its own vector back
                self.assertEqual(store.delete_many(["same"], remaining=[library[0]]), 0)
                self.assertEqual(store.attach([dict(library[0])])[0]["vector"], vec(1))
                self.assertEqual(store.attach([dict(library[1])])[0]["vector"], vec(2))
                # both gone: now it goes
                self.assertEqual(store.delete_many(["same"], remaining=[]), 1)


class Migrate(unittest.TestCase):
    def test_move_once_archive_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            lib_path = tmp / "memory" / "library.json"
            lib_path.parent.mkdir()
            original = library()
            lib_path.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")
            before = lib_path.read_bytes()
            store_path, archive = tmp / "memory" / vs.FILE_NAME, tmp / "memory" / "archive"

            counts = vs.migrate_library(lib_path, store_path, archive)
            self.assertEqual({k: counts[k] for k in ("entries", "moved", "no_id", "empty", "already")},
                             {"entries": 7, "moved": 5, "no_id": 1, "empty": 1, "already": 0})
            archived = archive / counts["archived"]
            self.assertEqual(archived.read_bytes(), before)            # the old file, kept as it was
            lib = json.loads(lib_path.read_text("utf-8"))
            self.assertEqual(lib["rooms"], original["rooms"])
            self.assertEqual(lib["schema_version"], 3)
            self.assertEqual([e.get("text") for e in lib["entries"]], [e["text"] for e in original["entries"]])
            self.assertTrue(all("vector" not in e for e in lib["entries"][:5]))
            self.assertEqual(lib["entries"][5]["vector"], [])
            self.assertEqual(lib["entries"][6]["vector"], vec(99))
            with vs.VectorStore(store_path) as store:                  # every entry gets its vector back
                back = store.attach(lib["entries"])
                for i in range(5):
                    self.assertEqual(back[i]["vector"], vec(i))

            again = vs.migrate_library(lib_path, store_path, archive)  # nothing left to move
            self.assertEqual((again["moved"], again["already"], again["archived"]), (0, 5, ""))
            self.assertEqual(len(list(archive.iterdir())), 1)
            with vs.VectorStore(store_path) as store:
                self.assertEqual(len(store), 5)

    def test_interrupted_migration_finishes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            lib_path, store_path = tmp / "library.json", tmp / vs.FILE_NAME
            lib_path.write_text(json.dumps(library(), ensure_ascii=False), encoding="utf-8")
            with vs.VectorStore(store_path) as store:                  # vectors stored, library not yet rewritten
                store.put_many({"m0": vec(0), "m1": vec(1)})
            counts = vs.migrate_library(lib_path, store_path, tmp / "archive")
            self.assertEqual(counts["moved"], 5)
            with vs.VectorStore(store_path) as store:
                self.assertEqual(len(store), 5)
                self.assertEqual(store.get("m1"), vec(1))


if __name__ == "__main__":
    unittest.main()
