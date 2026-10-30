"""Her conversation history in its own SQLite file (history_store.py).

Every number here is made up, and every database lives in the test's own
temporary directory.
"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import history_store as hs  # noqa: E402


class HistoryStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "history.sqlite3"
        self.store = hs.HistoryStore(self.path)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    # ------------------------------------------------------------------
    def _count(self):
        return self.store._db.execute("SELECT COUNT(*) FROM history").fetchone()[0]

    def _field(self, row_id, name):
        return self.store._db.execute("SELECT %s FROM history WHERE id = ?" % name, (row_id,)).fetchone()[0]

    # ------------------------------------------------------------------
    def test_recent_oldest_first_and_places_separate(self):
        first = self.store.append("group:10001", "user", "早上好", sender_id="10001")
        second = self.store.append("group:10001", "assistant", "早上好呀")
        third = self.store.append("group:10001", "user", "你在干嘛", sender_id="10003")
        self.store.append("private:20002", "user", "悄悄话", sender_id="20002")
        self.assertEqual((first, second, third), (1, 2, 3))
        self.assertEqual(self.store.recent("group:10001"), [
            {"role": "user", "content": "早上好"},
            {"role": "assistant", "content": "早上好呀"},
            {"role": "user", "content": "你在干嘛"},
        ])
        self.assertEqual(self.store.recent("group:10001", limit=2), [
            {"role": "assistant", "content": "早上好呀"},
            {"role": "user", "content": "你在干嘛"},
        ])
        self.assertEqual(self.store.recent("group:10001", limit=0), [])
        self.assertEqual(self.store.recent("group:10001", limit=-1), [])
        self.assertEqual(self.store.recent("private:20002"),
                         [{"role": "user", "content": "悄悄话"}])
        self.assertEqual(self.store.recent("group:900001"), [])

    def test_not_written(self):
        self.assertEqual(self.store.append("group:10001", "system", "不是话"), 0)
        self.assertEqual(self.store.append("group:10001", "user", "　\n\t "), 0)
        self.assertEqual(self.store.append("group:10001", "user", ""), 0)
        self.assertEqual(self.store.append("", "user", "没有地点"), 0)
        self.assertEqual(self._count(), 0)
        self.assertEqual(self.store.recent("group:10001"), [])

    def test_about_gets_the_speaker_once(self):
        row_id = self.store.append("group:10001", "user", "你好", sender_id="10001",
                                   about=("10001", "10003", "", "10003"))
        self.assertEqual(json.loads(self._field(row_id, "about")), ["10001", "10003"])
        row_id = self.store.append("group:10001", "user", "又一句", sender_id="10003")
        self.assertEqual(json.loads(self._field(row_id, "about")), ["10003"])
        row_id = self.store.append("group:10001", "assistant", "她回谁", about=["10001"])
        self.assertEqual(json.loads(self._field(row_id, "about")), ["10001"])

    def test_gate_decides_and_sees_the_row(self):
        seen = []

        def gate(row):
            seen.append(row)
            return row["content"] != "不要"

        with hs.HistoryStore(Path(self.tmp.name) / "gated.sqlite3", gate=gate) as store:
            self.assertEqual(store.append("group:10001", "user", "不要", sender_id="10001",
                                          message_id="900001", about=["10003"],
                                          sources=["900002"]), 0)
            self.assertEqual(store.recent("group:10001"), [])
            row_id = store.append("group:10001", "user", "要", sender_id="10001",
                                  message_id="900001", about=["10003"], sources=["900002"])
            self.assertGreater(row_id, 0)
            self.assertEqual(len(store.recent("group:10001")), 1)
        for row in seen:
            for key in ("place", "role", "content", "sender_id", "sender_name",
                        "message_id", "about", "sources", "ts"):
                self.assertIn(key, row)
            self.assertEqual(row["place"], "group:10001")
            self.assertEqual(row["sender_id"], "10001")
            self.assertEqual(row["about"], ["10003", "10001"])
            self.assertEqual(row["sources"], ["900002"])
            self.assertEqual(row["message_id"], "900001")

    def test_keep_per_place_drops_the_oldest(self):
        with hs.HistoryStore(Path(self.tmp.name) / "trim.sqlite3", keep_per_place=12) as store:
            for i in range(12 + 5):
                store.append("group:10001", "user", "第%d句" % i, sender_id="10001")
            got = store.recent("group:10001", limit=100)
            self.assertEqual([g["content"] for g in got], ["第%d句" % i for i in range(5, 17)])
            self.assertEqual(store._db.execute("SELECT COUNT(*) FROM history").fetchone()[0], 12)

    def test_forget_person(self):
        he = self.store.append("group:10001", "user", "他说的", sender_id="10001")
        she_back = self.store.append("group:10001", "assistant", "她回他的", about=["10001"])
        other = self.store.append("group:10001", "user", "别人说的", sender_id="10003")
        she_other = self.store.append("group:10001", "assistant", "她回别人的", about=["10003"])
        in_private = self.store.append("private:20002", "user", "他在私聊", sender_id="10001")
        self.assertEqual(self.store.forget_person(""), 0)
        self.assertEqual(self._count(), 5)
        self.assertEqual(self.store.forget_person("10001"), 3)
        for row_id in (he, she_back, in_private):
            self.assertEqual(self.store._db.execute("SELECT COUNT(*) FROM history WHERE id = ?",
                                                    (row_id,)).fetchone()[0], 0)
        self.assertEqual([c["content"] for c in self.store.recent("group:10001")],
                         ["别人说的", "她回别人的"])
        self.assertEqual(self.store.recent("private:20002"), [])
        for row_id in (other, she_other):
            self.assertEqual(self.store._db.execute("SELECT COUNT(*) FROM history WHERE id = ?",
                                                    (row_id,)).fetchone()[0], 1)
        self.assertEqual(self.store.forget_person("10001"), 0)

    def test_forget_messages(self):
        one = self.store.append("group:10001", "user", "收到一条", sender_id="10001",
                                message_id="900001")
        from_one = self.store.append("group:10001", "assistant", "她回这条",
                                     sources=["900001", "900003"])
        other = self.store.append("group:10001", "user", "另一条", sender_id="10003",
                                  message_id="900002")
        from_other = self.store.append("group:10001", "assistant", "她回另一条", sources=["900002"])
        self.assertEqual(self.store.forget_messages(""), 0)
        self.assertEqual(self.store.forget_messages(()), 0)
        self.assertEqual(self._count(), 4)
        self.assertEqual(self.store.forget_messages(["900001"]), 2)
        self.assertEqual(self._count(), 2)
        self.assertEqual([c["content"] for c in self.store.recent("group:10001")],
                         ["另一条", "她回另一条"])
        for row_id in (one, from_one):
            self.assertEqual(self.store._db.execute("SELECT COUNT(*) FROM history WHERE id = ?",
                                                    (row_id,)).fetchone()[0], 0)
        for row_id in (other, from_other):
            self.assertEqual(self.store._db.execute("SELECT COUNT(*) FROM history WHERE id = ?",
                                                    (row_id,)).fetchone()[0], 1)
        self.assertEqual(self.store.forget_messages(["900001"]), 0)

    def test_deleted_words_are_gone_from_the_file(self):
        path = Path(self.tmp.name) / "gone.sqlite3"
        store = hs.HistoryStore(path)
        try:
            store.append("group:10001", "user", "紫色长颈鹿暗号", sender_id="10001")
            store.append("group:10001", "user", "普通一句", sender_id="10003")
            self.assertEqual(store._db.execute("PRAGMA secure_delete").fetchone()[0], 1)
            self.assertNotEqual(
                str(store._db.execute("PRAGMA journal_mode").fetchone()[0]).lower(), "wal")
            self.assertEqual(store.forget_person("10001"), 1)
        finally:
            store.close()
        data = path.read_bytes()
        self.assertNotIn("紫色长颈鹿暗号".encode("utf-8"), data)     # really overwritten
        self.assertIn("普通一句".encode("utf-8"), data)             # the scan would have found it
        self.assertFalse(Path(str(path) + "-wal").exists())

    def test_clear_place_and_places(self):
        self.store.append("group:10001", "user", "一", sender_id="10001")
        self.store.append("group:10001", "user", "二", sender_id="10001")
        self.store.append("private:20002", "user", "三", sender_id="20002")
        self.store.append("group:10003", "user", "四", sender_id="10003")
        self.assertEqual(self.store.places(), ["group:10001", "group:10003", "private:20002"])
        self.assertEqual(self.store.clear_place("group:10001"), 2)
        self.assertEqual(self.store.recent("group:10001"), [])
        self.assertEqual(self.store.places(), ["group:10003", "private:20002"])
        self.assertEqual([c["content"] for c in self.store.recent("private:20002")], ["三"])
        self.assertEqual([c["content"] for c in self.store.recent("group:10003")], ["四"])
        self.assertEqual(self.store.clear_place("group:10001"), 0)

    def test_data_survives_close_and_with(self):
        self.store.append("group:10001", "user", "留着的", sender_id="10001")
        self.store.close()
        with hs.HistoryStore(self.path) as again:
            self.assertEqual(again.recent("group:10001"), [{"role": "user", "content": "留着的"}])
            self.assertEqual(again.places(), ["group:10001"])
        self.store = hs.HistoryStore(self.path)
        self.assertEqual(self.store.recent("group:10001")[0]["content"], "留着的")

    def test_no_astrbot_and_no_mixin_imports(self):
        src = (HERE.parent / "history_store.py").read_text(encoding="utf-8")
        imports = re.findall(r"^\s*(?:from|import)\s+\S+", src, re.M)
        self.assertTrue(imports)
        for line in imports:
            self.assertNotIn("astrbot", line.lower(), line)
            self.assertNotIn("mixin_", line, line)


if __name__ == "__main__":
    unittest.main()
