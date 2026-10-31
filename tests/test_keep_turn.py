# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Keeping one turn in her own history, for the new program (AstrBot keeps its own)."""
import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import test_basics  # noqa: E402,F401

import adapter_astrbot  # noqa: E402
import forget_registry  # noqa: E402
import harness  # noqa: E402
import history_store  # noqa: E402
import main  # noqa: E402
import mixin_turn  # noqa: E402
import turn  # noqa: E402


class KeepTurnTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.plugin = test_basics.make_plugin(harness.FakeContext())
        self.plugin._forget_reg = forget_registry.ForgetRegistry()   # in memory, closed below
        self.addCleanup(self._close_registry)
        self.store = history_store.HistoryStore(Path(self.tmp.name) / "history.sqlite3",
                                                gate=self.plugin._history_gate)
        self.addCleanup(self.store.close)
        self.plugin._history = self.store
        fake = harness.FakeEvent("hello", sender="10001", name="柠檬", group="900001")
        self.event = turn.TurnEvent(adapter_astrbot.from_astrbot(fake))
        self.place = "group:900001"
        self.request = turn.TurnRequest(prompt="谁说的(10001): hello")
        self.reply = turn.TurnReply(text="model words")

    def _close_registry(self):
        registry = getattr(self.plugin, "_forget_reg", None)
        self.plugin._forget_reg = None
        if registry is not None:
            registry.close()

    def rows(self):
        cur = self.store._db.execute(
            "SELECT role, content, sender_id, sender_name, message_id, about, sources"
            " FROM history WHERE place = ? ORDER BY id", (self.place,))
        out = []
        for role, content, sender_id, sender_name, message_id, about, sources in cur.fetchall():
            out.append({"role": role, "content": content, "sender_id": sender_id,
                        "sender_name": sender_name, "message_id": message_id,
                        "about": json.loads(about), "sources": json.loads(sources)})
        return out

    # ------------------------------------------------------------------
    def test_normal_turn_writes_two_lines(self):
        sent = "分条以后的话"
        self.plugin._check_note(self.event)["sent"] = sent
        self.plugin._keep_turn(self.event, self.request, self.reply)
        self.assertEqual(self.store.recent(self.place), [
            {"role": "user", "content": self.request.prompt},
            {"role": "assistant", "content": sent},
        ])
        user, hers = self.rows()
        self.assertEqual(user["content"], self.request.prompt)
        self.assertEqual(user["sender_id"], "10001")
        self.assertEqual(user["message_id"], "mhello")
        self.assertEqual(user["sources"], ["mhello"])
        self.assertEqual(hers["about"], ["10001"])
        self.assertEqual(hers["sources"], ["mhello"])

    def test_no_sent_uses_the_reply_text(self):
        self.plugin._keep_turn(self.event, self.request, self.reply)
        self.assertEqual(self.store.recent(self.place), [
            {"role": "user", "content": self.request.prompt},
            {"role": "assistant", "content": "model words"},
        ])

    def test_stopped_event_writes_nothing(self):
        self.plugin._check_note(self.event)["sent"] = "写了也不算"
        self.event.stop_event()
        self.plugin._keep_turn(self.event, self.request, self.reply)
        self.assertEqual(self.store.recent(self.place), [])
        self.assertEqual(self.rows(), [])

    def test_empty_words_write_nothing(self):
        self.plugin._check_note(self.event)["sent"] = ""
        self.plugin._keep_turn(self.event, self.request, self.reply)
        self.assertEqual(self.rows(), [])
        self.plugin._check_note(self.event)["sent"] = None
        self.reply.set_text("\n\t ")
        self.plugin._keep_turn(self.event, self.request, self.reply)
        self.assertEqual(self.rows(), [])

    def test_forgotten_person_writes_nothing(self):
        self.plugin._forget_reg.forget_person("10001")
        self.plugin._check_note(self.event)["sent"] = "还是不说"
        self.plugin._keep_turn(self.event, self.request, self.reply)
        self.assertEqual(self.store.recent(self.place), [])
        self.assertEqual(self.rows(), [])

    def test_without_a_store_does_nothing(self):
        self.plugin._history = None
        self.plugin._check_note(self.event)["sent"] = "写了也没处放"
        before = len(mixin_turn.logger.records)
        self.plugin._keep_turn(self.event, self.request, self.reply)
        self.assertEqual(mixin_turn.logger.records[before:], [])
        self.assertEqual(self.store.recent(self.place), [])

    def test_append_error_is_logged_not_raised(self):
        class Broken:
            def append(self, *args, **kwargs):
                raise OSError("history unavailable")

        self.plugin._history = Broken()
        self.plugin._check_note(self.event)["sent"] = "话"
        before = len(mixin_turn.logger.records)
        self.plugin._keep_turn(self.event, self.request, self.reply)
        new = mixin_turn.logger.records[before:]
        self.assertEqual(len(new), 1)
        self.assertEqual(new[0][0], "warning")
        self.assertIn("OSError", new[0][1])
        self.assertEqual(self.store.recent(self.place), [])

    def test_not_called_on_astrbot(self):
        main_source = (ROOT / "main.py").read_text(encoding="utf-8")
        self.assertNotIn("_keep_turn", main_source)
        source = (ROOT / "mixin_turn.py").read_text(encoding="utf-8")
        node = next(node for node in ast.walk(ast.parse(source))
                    if isinstance(node, ast.AsyncFunctionDef) and node.name == "_after_reply")
        self.assertNotIn("_keep_turn", ast.get_source_segment(source, node))
        self.assertTrue(callable(main.BioCorePlugin._keep_turn))


if __name__ == "__main__":
    unittest.main()
