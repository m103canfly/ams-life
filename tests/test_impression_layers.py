# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks of relationship text selected for model prompts."""
import asyncio
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import discretion
import her
import impressions
import interpretation
import mixin_discretion
import test_forget_history
import turn


def event(place, sender="10001"):
    return turn.TurnEvent(SimpleNamespace(place=place, sender_id=sender, sender_name="Alice"))


class ImpressionLayers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.users = self.root / "users"
        self.users.mkdir()
        self.user_patch = patch.object(mixin_discretion, "USER_DIR", self.users)
        self.user_patch.start()
        self.addCleanup(self.user_patch.stop)
        self.events_patch = patch.object(mixin_discretion, "EVENT_ARCHIVE_PATH", self.root / "events.jsonl")
        self.events_patch.start()
        self.addCleanup(self.events_patch.stop)
        self.p = her.Her.__new__(her.Her)
        self.p.config = {}
        self.p._read_library = lambda **kw: {"entries": []}
        self.p._window_places = lambda: []
        self.p._event_archive = lambda count: []
        self.p._read_window = lambda place: {"recent": []}
        self.p._people_store = impressions.Store(self.root / "people")
        self.p._owner_aliases = lambda: {}

    def prompt(self, ev, record):
        view = self.p._user_view(ev, record)
        private = ev.incoming.place == "private:" + ev.incoming.sender_id
        return interpretation.render_compact(None, user=view, private_with_him=private,
                                             people=self.p._people_lines(ev)), view

    def test_group_and_other_private_remove_all_relationship_text(self):
        fields = mixin_discretion._RELATIONSHIP_PRIVATE_FIELDS
        record = {"sender_id": "10001", "interactions": 25,
                  "relationship": {key: [{"text": "secret_" + key}] for key in fields}}
        for ev in (event("group:900001"), event("private:10003", "10003")):
            prompt, view = self.prompt(ev, record)
            self.assertIn("挺熟", prompt)
            for key in fields:
                self.assertNotIn(key, view["relationship"])
                self.assertNotIn("secret_" + key, prompt)
        self.assertIn("milestones", record["relationship"])

    def test_own_private_filters_known_sources_and_keeps_legacy(self):
        sources = [
            {"id": "own", "origin": discretion.make_origin("private:10001", ["10001"], ["m-own"])},
            {"id": "other", "origin": discretion.make_origin("private:10003", ["10003"])},
            {"id": "group", "origin": discretion.make_origin("group:900002", ["10003"])},
        ]
        self.p._read_library = lambda **kw: {"entries": sources[:2]}
        (self.root / "events.jsonl").write_text(json.dumps(sources[2]) + "\n", encoding="utf-8")
        rel = {"we_memory": [{"text": "owncode", "source_ids": ["m-own"]},
                             {"text": "othercode", "evidence_refs": ["other"]},
                             {"text": "groupcode", "evidence_refs": ["group"]},
                             {"text": "legacycode", "evidence_refs": ["missing"]}]}
        record = {"sender_id": "10001", "interactions": 25, "relationship": rel}
        prompt, view = self.prompt(event("private:10001"), record)
        self.assertIn("owncode", prompt)
        self.assertEqual([x["text"] for x in view["relationship"]["we_memory"]], ["owncode", "legacycode"])
        record["relationship"]["we_memory"] = view["relationship"]["we_memory"][1:]
        self.assertIn("legacycode", self.prompt(event("private:10001"), record)[0])
        for key in mixin_discretion._RELATIONSHIP_PRIVATE_FIELDS:
            bad = {"text": "blocked", "source_ids": ["other"]}
            value = {"item": bad} if key.endswith("_map") else [bad]
            view = self.p._user_view(event("private:10001"), {"sender_id": "10001", "relationship": {key: value}})
            self.assertFalse(view["relationship"][key], key)
        mixed = {"we_memory": [{"text": "mixed", "evidence_refs": ["own", "other"]}]}
        self.assertEqual(self.p._user_view(event("private:10001"), {"relationship": mixed})
                         ["relationship"]["we_memory"], [])

    def test_group_private_source_keeps_existing_guard(self):
        source = {"id": "private_group", "origin": discretion.make_origin(
            "group:900001", ["10001"], visibility=discretion.PRIVATE)}
        self.p._read_library = lambda **kw: {"entries": [source]}
        record = {"sender_id": "10001", "relationship": {"transactive_map": {"topic": 1},
                  "we_memory": [{"text": "owncode"}], "annotations": [{"text": "legacy"}]}}
        rel = self.p._user_view(event("private:10001"), record)["relationship"]
        self.assertEqual(rel["transactive_map"], {})
        self.assertEqual(rel["we_memory"], [])
        self.assertEqual(rel["annotations"][0]["text"], "legacy")

    def test_group_cards_keep_existing_views(self):
        store = self.p._people_store
        store.save("group:900001", {"people": {"10001": {
            "qq": "10001", "name": "Alice", "aliases": [], "style": "gentlestyle",
            "topics": ["topiccode"], "origin": discretion.make_origin("group:900001", ["10001"])}}})
        record = {"sender_id": "10001", "interactions": 4}
        a = self.prompt(event("group:900001"), record)[0]
        b = self.prompt(event("group:900002"), record)[0]
        private = self.prompt(event("private:10001"), record)[0]
        self.assertIn("gentlestyle", a)
        self.assertIn("topiccode", a)
        self.assertIn("Alice", b)
        self.assertNotIn("gentlestyle", b)
        self.assertNotIn("topiccode", b)
        self.assertIn("gentlestyle", private)
        self.assertNotIn("topiccode", private)

    def test_narrative_model_receives_only_allowed_milestones(self):
        p = self.p
        p._llm_allowed = lambda kind: True
        p._llm_v2_cooldown_ok = lambda kind: True
        p._user_record = lambda ev: {"sender_id": "10001", "relationship": {"milestones": [
            {"key": "ownmark", "source_ids": ["own"]},
            {"key": "othermark", "source_ids": ["other"]},
            {"key": "oldmark"}]}}
        p._read_library = lambda **kw: {"entries": [
            {"id": "own", "origin": discretion.make_origin("private:10001")},
            {"id": "other", "origin": discretion.make_origin("private:10003")} ]}
        calls = []
        async def capture(kind, prompt, parser, ev):
            calls.append(prompt)
            return None
        p._llm_v2_call = capture
        asyncio.run(p._maybe_relationship_narrative(event("group:900001"), None))
        self.assertEqual(calls, [])
        asyncio.run(p._maybe_relationship_narrative(event("private:10001"), None))
        self.assertIn("ownmark", calls[0])
        self.assertIn("oldmark", calls[0])
        self.assertNotIn("othermark", calls[0])

    def test_forget_person_removes_both_layers(self):
        p = test_forget_history.Plugin()
        self.addCleanup(p._forget_reg.close)
        store = impressions.Store(self.root / "people")
        p._impression_store = lambda: store
        store.save("group:900001", {"people": {"10001": {"qq": "10001"}}})
        path = self.users / "10001.json"
        path.write_text(json.dumps({"sender_id": "10001", "relationship": {"we_memory": []}}), encoding="utf-8")
        paths = {name: self.root / name for name in ("EVENT_ARCHIVE_PATH", "INSIGHT_ARCHIVE_PATH", "EVENT_SESSION_DIR")}
        with patch.multiple(mixin_discretion, **paths):
            p._forget(person="10001")
        self.assertFalse(path.exists())
        self.assertNotIn("10001", store.load("group:900001")["people"])
