"""Offline wish checks; all names and numbers below are invented."""
import asyncio
import importlib
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def setUpModule():
    global DATA, _temporary_data, _modules_before, discretion, wishes, interpretation, mixin_llm, mixin_browse, mixin_wishes, mixin_send_check, mixin_discretion, mixin_selfie
    _modules_before = set(sys.modules)
    _temporary_data = tempfile.TemporaryDirectory(prefix="wishes-test-")
    DATA = Path(_temporary_data.name)
    # The harness replaces global time and random.Random; these tests do not need it.
    with patch.dict("os.environ", {"AMS_LIFE_DATA_DIR": str(DATA)}), patch.object(
            sys, "path", [str(HERE / "stubs"), str(HERE.parent)] + sys.path):
        discretion = importlib.import_module("discretion")
        wishes = importlib.import_module("wishes")
        interpretation = importlib.import_module("interpretation")
        mixin_llm = importlib.import_module("mixin_llm")
        mixin_browse = importlib.import_module("mixin_browse")
        mixin_wishes = importlib.import_module("mixin_wishes")
        mixin_send_check = importlib.import_module("mixin_send_check")
        mixin_discretion = importlib.import_module("mixin_discretion")
        mixin_selfie = importlib.import_module("mixin_selfie")
    OwnerCheck._check_for_owner = mixin_send_check.SendCheckMixin._check_for_owner
    for name in ("_tool_wish", "_record_wish", "_forget_wishes", "_new_wishes_count", "_wish_materials",
                 "_wish_block", "page_wishes", "page_wishes_status"):
        setattr(Tool, name, getattr(mixin_wishes.WishesMixin, name))


def tearDownModule():
    _temporary_data.cleanup()
    root = os.path.normcase(os.path.abspath(str(HERE.parent))) + os.sep
    for name in set(sys.modules) - _modules_before:
        module = sys.modules.get(name)
        path = getattr(module, "__file__", None)
        if path and os.path.normcase(os.path.abspath(path)).startswith(root):
            sys.modules.pop(name, None)


class OwnerCheck:
    def __init__(self, entries=(), owner="10005"):
        self.config = {"owner_qq": owner}
        self.entries = list(entries)

    def _read_library(self, vectors=False):
        return {"entries": self.entries}

    def _names_index(self):
        return {"10006": {"阿梨"}, "10005": {"主人"}}

    def _known_names(self, people):
        return [n for p in people for n in self._names_index().get(p, set())]

    def _said_by(self, item):
        return str(item.get("sender_id") or "") if item.get("role") != "assistant" else ""

    def _common_pieces(self):
        return set()

    async def _embed_text(self, text):
        return None


def memory(where, text, sender="10006", visibility=None, deleted=False):
    return {"id": where, "text": text, "sender_id": sender, "deleted": deleted,
            "origin": discretion.make_origin(where, [sender], visibility=visibility)}


class WishOwnerCheck(unittest.TestCase):
    def test_import_does_not_replace_clock_or_random(self):
        code = ("import importlib.util, random, sys, time; "
                "clock, rng = time.time, random.Random; "
                "spec = importlib.util.spec_from_file_location('wishes_import_test', sys.argv[1]); "
                "module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); "
                "assert time.time is clock and random.Random is rng")
        proc = subprocess.run([sys.executable, "-c", code, str(Path(__file__))],
                              capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def check(self, plugin, text):
        with patch.object(mixin_send_check, "MEMORY_LIBRARY_PATH", DATA / "absent-library.json"):
            return asyncio.run(plugin._check_for_owner(text))["leak"]

    def test_owner_allowed_sources(self):
        for where, sender in (("self", ""), ("web:example", "10006"),
                              ("private:10005", "10005"), ("group:900001", "10005")):
            with self.subTest(where=where):
                self.assertFalse(self.check(OwnerCheck([memory(where, "今晚一起去看星星", sender)]), "今晚一起去看星星"))

    def test_other_private_words_are_rejected(self):
        plugin = OwnerCheck([memory("private:10006", "我的秘密是下周要搬去海边")])
        self.assertTrue(self.check(plugin, "我的秘密是下周要搬去海边"))

    def test_group_name_is_anonymous(self):
        plugin = OwnerCheck([memory("group:900001", "今天去看星星")])
        self.assertTrue(self.check(plugin, "阿梨今天去看星星"))
        self.assertFalse(self.check(plugin, "今天去看星星"))

    def test_unreadable_library_is_held_back(self):
        path = DATA / "invalid-wish-library.json"
        path.write_text("{", encoding="utf-8")
        try:
            with patch.object(mixin_send_check, "MEMORY_LIBRARY_PATH", path):
                result = asyncio.run(OwnerCheck()._check_for_owner("普通文字"))
            self.assertTrue(result["leak"])
        finally:
            path.unlink()

    def test_no_owner_or_deleted_memory(self):
        self.assertTrue(self.check(OwnerCheck(owner=""), "一条普通的话"))
        self.assertFalse(self.check(OwnerCheck([memory("private:10006", "秘密是要去海边", deleted=True)]), "秘密是要去海边"))

    def test_cache_refreshes_on_same_timestamp_edit(self):
        plugin = OwnerCheck([memory("private:10006", "蓝鲸在海边唱歌")])
        self.assertFalse(self.check(plugin, "松鼠在森林跳舞"))
        plugin.entries[0]["text"] = "松鼠在森林跳舞"
        self.assertTrue(self.check(plugin, "松鼠在森林跳舞"))


class Tool(OwnerCheck):
    enabled = wishes_enabled = True

    def _without_gone(self, text, event=None):
        return text.replace("旧名字", "某人")

    def _known_numbers(self):
        return {"10006"}

    def _speaker(self, event):
        return ("10006", "阿梨")

    def _source_ids(self, event):
        return ["msg-1"]

    def _here(self, event):
        return "private:10006"

    def _may_keep(self, *args, **kwargs):
        return True

    def _wish_local(self):
        return True

    async def _page_body(self, body):
        return body or {}


class WishStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "wishes.json"
        self.now = datetime(2026, 10, 30, 12)

    def test_tool_records_clean_self_and_only_one_file(self):
        plugin = Tool()
        with patch.object(mixin_wishes, "WISHES_PATH", self.path), patch.object(
                mixin_send_check, "MEMORY_LIBRARY_PATH", Path(self.tmp.name) / "missing"):
            result = asyncio.run(plugin._tool_wish(object(), "希望有一个能整理每日生活记录的工具和提醒功能10006", "为了回顾"))
        self.assertEqual(result, "记下了")
        row = wishes.read(self.path)["items"][0]
        self.assertNotIn("10006", row["what"])
        self.assertEqual(row["origin"]["visibility"], discretion.SELF)
        self.assertEqual((row["status"], row["source_ids"], row["speaker"]), ("新", ["msg-1"], "10006"))
        self.assertEqual([x.name for x in self.path.parent.iterdir()], ["wishes.json"])

    def test_tool_rejects_private_content(self):
        plugin = Tool([memory("private:10006", "我的秘密是下周要搬去海边")])
        with patch.object(mixin_wishes, "WISHES_PATH", self.path), patch.object(
                mixin_send_check, "MEMORY_LIBRARY_PATH", Path(self.tmp.name) / "missing"):
            result = asyncio.run(plugin._tool_wish(object(), "希望我的秘密是下周要搬去海边能够被好好记录下来", ""))
        self.assertEqual(result, "这条里有别人的私事，换个说法")
        self.assertFalse(self.path.exists())

    def test_length_daily_duplicate_and_open_limit(self):
        self.assertEqual(wishes.add(self.path, "短", "", "reply", now=self.now), "字数不合适")
        self.assertEqual(wishes.add(self.path, "甲" * 61, "", "reply", now=self.now), "字数不合适")
        self.assertEqual(wishes.add(self.path, "甲" * 20, "乙" * 101, "reply", now=self.now), "字数不合适")
        text = "希望能够拥有一个方便整理生活的小工具" + "甲乙丙丁戊己庚辛壬癸"
        self.assertEqual(wishes.add(self.path, text, "", "reply", now=self.now), "记下了")
        self.assertEqual(wishes.add(self.path, text, "", "reply", now=self.now), "这条已经记过了")
        data = wishes.read(self.path)
        data["daily"][self.now.date().isoformat()] = 5
        wishes.write(self.path, data)
        self.assertEqual(wishes.add(self.path, "希望可以在不同的日子使用完全不同的绘画工具", "", "reply", now=self.now), "今天记满了，明天再记")
        data["items"] = [dict(data["items"][0], id=i, what=str(i)) for i in range(30)]
        wishes.write(self.path, data)
        self.assertEqual(wishes.add(self.path, text, "", "reply", now=self.now + timedelta(days=1)), "满了，先挑一条合并或撤掉")

    def test_forget_person_and_source_and_status(self):
        text = "希望能够拥有一个方便整理生活的小工具以及提醒功能"
        wishes.add(self.path, text, "", "reply", ["10006"], ["msg-1"], now=self.now)
        self.assertTrue(wishes.set_status(self.path, 1, "好", self.now))
        self.assertEqual(wishes.read(self.path)["items"][0]["status"], "好")
        self.assertEqual(wishes.forget(self.path, "10006"), 1)
        wishes.add(self.path, text, "", "reply", [], ["msg-2"], now=self.now)
        self.assertEqual(wishes.forget(self.path, source_ids=["msg-2"]), 1)

    def test_all_owner_statuses_and_count(self):
        text = "希望能够拥有一个方便整理生活的小工具以及提醒功能"
        wishes.add(self.path, text, "", "reply", now=self.now)
        for status in ("好", "先放着", "不要"):
            self.assertTrue(wishes.set_status(self.path, 1, status, self.now))
            row = wishes.read(self.path)["items"][0]
            self.assertEqual((row["status"], row["marked_at"]), (status, self.now.isoformat()))
        plugin = Tool()
        with patch.object(mixin_wishes, "WISHES_PATH", self.path):
            self.assertEqual(plugin._new_wishes_count(), 0)

    def test_forget_calls_wish_cleanup(self):
        class Called(Exception):
            pass
        class Fake:
            def _group_forget_queue(self, *args): pass
            def _forget_recent_images(self, *args): pass
            def _forget_wishes(self, person, ids):
                self.seen = (person, ids)
                raise Called()
        obj = Fake()
        with self.assertRaises(Called):
            mixin_discretion.DiscretionMixin._forget(obj, "10006", ["msg-1"])
        self.assertEqual(obj.seen, ("10006", ["msg-1"]))

    def test_switch_off(self):
        plugin = Tool()
        plugin.wishes_enabled = False
        with patch.object(mixin_wishes, "WISHES_PATH", self.path):
            self.assertEqual(asyncio.run(plugin._tool_wish(object(), "希望能够拥有一个方便整理生活的小工具以及提醒功能", "")), "没开")
        self.assertFalse(self.path.exists())

    def test_tool_is_only_offered_when_enabled(self):
        class FunctionTool:
            def __init__(self, **kwargs):
                self.name = kwargs["name"]
        class ToolSet:
            def __init__(self, tools): self.tools = tools
        class Phone(mixin_selfie.SelfieMixin):
            enabled = True
            config = {}
            def _phone_context(self, event): return ""
            async def _tool_wish(self, event, what="", why=""): pass
        module = types.ModuleType("astrbot.core.agent.tool")
        module.FunctionTool, module.ToolSet = FunctionTool, ToolSet
        p = Phone()
        with patch.dict(sys.modules, {"astrbot.core.agent.tool": module}):
            for enabled in (False, True):
                p.wishes_enabled = enabled
                req = types.SimpleNamespace(func_tool=None)
                p._give_phone_tools(req, object())
                self.assertEqual("wish" in [x.name for x in req.func_tool.tools], enabled)

    def test_atomic_write_cleans_temporary_file_on_failure(self):
        wishes.write(self.path, {"items": [], "next_id": 1})
        before = self.path.read_bytes()
        with patch.object(wishes.os, "replace", side_effect=OSError("failure")):
            with self.assertRaises(OSError):
                wishes.write(self.path, {"items": [{"what": "new"}]})
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual([p.name for p in self.path.parent.iterdir()], ["wishes.json"])

    def test_page_status_materials_and_disabled(self):
        text = "希望能够拥有一个方便整理生活的小工具以及提醒功能"
        wishes.add(self.path, text, "可以回顾", "reply", now=self.now)
        plugin = Tool()
        with patch.object(mixin_wishes, "WISHES_PATH", self.path):
            for status in ("好", "先放着", "不要"):
                result = asyncio.run(plugin.page_wishes_status({"id": 1, "status": status}))
                self.assertEqual(result["status"], "ok")
                self.assertIn(status, " ".join(plugin._wish_materials(self.now.timestamp())))
                page = asyncio.run(plugin.page_wishes())
                self.assertEqual(page["data"]["items"][0]["status"], status)
                self.assertNotIn("speaker", page["data"]["items"][0])
            plugin.wishes_enabled = False
            self.assertFalse(asyncio.run(plugin.page_wishes())["data"]["on"])

    def test_block_counts_only_category_and_recent_dates(self):
        wishes.count_block(self.path, "看不到图", self.now)
        wishes.count_block(self.path, "网址不能读", self.now)
        wishes.count_block(self.path, "不属于列表的原话", self.now)
        content = self.path.read_text(encoding="utf-8")
        self.assertNotIn("不属于列表的原话", content)
        self.assertIn("看不到图 1 次", " ".join(wishes.materials(self.path, self.now)))
        self.assertEqual(wishes.materials(self.path, self.now + timedelta(days=8)), [])

    def test_unavailable_search_tool_records_category(self):
        class Browser(Tool):
            _tool_search = mixin_browse.BrowseMixin._tool_search
            def _browse_ledger(self): return types.SimpleNamespace(money_left=lambda: True)
            def _browse_quota(self, event): return types.SimpleNamespace(take=lambda name: True)
            def _browse_names(self): return []
            async def _may_go_out(self, event, text): return True
            def _builtin_web_tool(self, name): return None
        p = Browser()
        with patch.object(mixin_wishes, "WISHES_PATH", self.path):
            asyncio.run(p._tool_search(object(), "四季天空的颜色"))
        rows = wishes.read(self.path)["blocks"]
        self.assertEqual(sum(row.get("工具没有", 0) for row in rows.values()), 1)

    def test_remote_page_request_is_rejected(self):
        p = Tool()
        p._wish_local = lambda: False
        self.assertEqual(asyncio.run(p.page_wishes())["status"], "error")
        self.assertEqual(asyncio.run(p.page_wishes_status({"id": 1, "status": "好"}))["status"], "error")

    def test_local_request_requires_local_host_and_no_proxy_headers(self):
        fake_quart = types.ModuleType("quart")
        fake_quart.request = types.SimpleNamespace(remote_addr="127.0.0.1", host="localhost", headers={})
        with patch.dict(sys.modules, {"quart": fake_quart}):
            self.assertTrue(mixin_wishes.WishesMixin._wish_local())
            fake_quart.request.remote_addr = "192.0.2.1"
            self.assertFalse(mixin_wishes.WishesMixin._wish_local())
            fake_quart.request.remote_addr = "127.0.0.1"
            fake_quart.request.host = "example.test"
            self.assertFalse(mixin_wishes.WishesMixin._wish_local())
            fake_quart.request.host = "localhost"
            fake_quart.request.headers = {"X-Forwarded-For": "192.0.2.1"}
            self.assertFalse(mixin_wishes.WishesMixin._wish_local())

    def test_notebook_wish_checked_and_at_most_two(self):
        class Notebook(Tool):
            _maybe_write_notebook = mixin_llm.LLMMixin._maybe_write_notebook
            def __init__(self):
                super().__init__()
                self.self_model = {"notebook": []}
                self.night = {"tried": [], "changes": 0}
            def _notebook_time_reached(self, now): return True
            def _notebook_night(self, now): return self.night
            def _core(self, event): return None
            async def _persona_text(self, event): return ""
            def _notebook_sittings(self, now): return ["group"]
            def _save_self_model(self): pass
            def _notebook_shown(self, entries, sitting): return []
            def _notebook_materials(self, core, sitting, now): return []
            async def _llm_v2_call(self, kind, prompt, parser, default, **kwargs):
                self.prompt = prompt
                rows = [{"op": "wish", "what": x, "why": "为了方便"} for x in (
                    "希望能够拥有一个方便整理生活的小工具以及提醒功能",
                    "希望可以用新的绘画功能制作不同颜色的风景图片",
                    "希望将收集的音乐按时间顺序排列并进行分类整理")]
                return parser(json.dumps({"changes": rows}, ensure_ascii=False))
            def _job_stale(self): return False
            def _sitting_origin(self, sitting, materials): return discretion.make_origin(discretion.SELF)
        p = Notebook()
        with patch.object(mixin_wishes, "WISHES_PATH", self.path), patch.object(
                mixin_send_check, "MEMORY_LIBRARY_PATH", self.path.parent / "missing"):
            self.assertTrue(asyncio.run(p._maybe_write_notebook(self.now.timestamp())))
        rows = wishes.read(self.path)["items"]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["where"] == "notebook" for r in rows))
        self.assertIn('"op":"wish"', p.prompt)

    def test_notebook_wish_rejects_private_material(self):
        p = Tool([memory("private:10006", "我的秘密是下周要搬去海边")])
        with patch.object(mixin_wishes, "WISHES_PATH", self.path), patch.object(
                mixin_send_check, "MEMORY_LIBRARY_PATH", self.path.parent / "missing"):
            result = asyncio.run(p._record_wish(None, "希望我的秘密是下周要搬去海边能够被好好记录下来", "", "notebook"))
        self.assertEqual(result, "这条里有别人的私事，换个说法")
        self.assertFalse(self.path.exists())
