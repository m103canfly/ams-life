# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check the text supplied as event evidence."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import mixin_events


class SourceCheckTextTest(unittest.TestCase):
    def test_metadata_does_not_supply_event_characters(self):
        entries = [
            {"text": "今天抽卡又歪了", "provenance": {"session": "group:900001", "sender_id": "10003"}},
            {"text": "我也歪了", "provenance": {"session": "group:900001", "sender_id": "10003"}},
        ]
        body = "群里有人抽卡歪了，还有 10003"
        check = mixin_events.EventsMixin._source_check
        actual = check(body, [mixin_events._source_text(item) for item in entries])
        old = check(body, [str(item) for item in entries])
        self.assertEqual(actual, check(body, [item["text"] for item in entries]))
        self.assertLess(actual["overlap"], old["overlap"])
        self.assertNotEqual(actual["coverage"], old["coverage"])

    def test_non_dict_and_missing_text(self):
        self.assertEqual(mixin_events._source_text("今天抽卡又歪了"), "今天抽卡又歪了")
        self.assertEqual(mixin_events._source_text({}), "")
        check = mixin_events.EventsMixin._source_check
        self.assertEqual(check("抽卡歪了", [mixin_events._source_text("今天抽卡又歪了")]),
                         check("抽卡歪了", ["今天抽卡又歪了"]))

    def test_event_source_uses_text_helper(self):
        source = (Path(__file__).resolve().parents[1] / "mixin_events.py").read_text("utf-8")
        self.assertIn("self._source_check(body, [_source_text(t) for t in seg_entries]", source)
        self.assertNotIn("self._source_check(body, [str(t) for t in seg_entries]", source)
