# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Group members she knows: a basic impression of everyone who talks a lot in a group.

What she keeps of a person, per group: what he is called there, how he talks (one
line, at most 60 characters, no numbers, no judgement of who he is), what he often
talks about (a few words), and some counts. Never his words verbatim, never message
ids. One file per group, ``people/<group>-<hash>.json``:

    {"place": "group:1", "tried": "2026-10-28",
     "group":  {"text": "...", "stats": {...}, "origin": {...}},          # what the group is like
     "people": {"10001": {"qq", "name", "aliases", "style", "topics", "stats",
                          "since", "updated", "origin"}}}

Every night, from that group's phone window (the last 24 hours):
- who: everyone with at least DAILY_MIN lines that day, or at least NEW_MIN and no
  impression yet; at most MAX_PEOPLE, the most talkative first; nobody the forget
  registry rules out;
- counts and pet phrases are worked out by the program;
- one model call for the whole group, at most once a day (marked as tried before
  the call, so a failure or a restart does not call again): only those people's
  own lines, each person a code (P1, P2...), long numbers masked, red-line lines
  left out. The answer is JSON per code; every style line and topic is checked
  (red lines, judgements, numbers, length) and whatever fails is not kept -- the
  counts are kept either way.

Where she may use it (``view``), after the discretion table, decided by the owner:
in that group, all of it; in another group where he is present, only what he is
called (so she knows it is the same person); in his own private chat, name and
style, and only the topics he brought up there himself; anywhere else, nothing.

Wiring into the plugin (the nightly loop, the reply prompt, the panel, deleting)
comes with step 1, part 3-2. Only the standard library; no AstrBot.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from collections import Counter
from pathlib import Path

try:
    from . import discretion, redline
except ImportError:
    import discretion
    import redline

DAILY_MIN = 10          # lines in one day that make someone "talks a lot today"
NEW_MIN = 5             # ... or this many, for someone she has no impression of yet
MAX_PEOPLE = 12         # people per group per night (one model call)
LINES_PER_PERSON = 30   # his most recent lines that go to the model
LINE_CHARS = 60         # each cut to this
STYLE_CHARS = 60
TOPIC_CHARS = (2, 8)
MAX_TOPICS = 3
MAX_PHRASES = 3

# what a person is, rather than how he talks: not hers to write down about anyone
JUDGEMENT = re.compile(r"性格|人品|脾气|情商|智商|善良|自私|小气|大方|靠谱|不靠谱|好人|坏人|内向|外向|自卑|自信"
                       r"|聪明|笨蛋|愚蠢|幼稚|成熟|渣男|渣女|有钱|很穷|漂亮|帅气|好看|丑|年纪|年龄|职业|工作是"
                       r"|学生|结婚|单身")
DIGITS = re.compile(r"[0-9０-９]")
LONG_NUMBER = re.compile(r"\d{5,}")
PART = re.compile(r"\[(图片|表情|语音|视频|文件|聊天记录|戳一戳|卡片|分享|位置|音乐|骰子|猜拳|名片|消息)\]")
HAN = re.compile(r"[一-鿿]+")
GENERIC = {"哈哈", "哈哈哈", "哈哈哈哈", "什么", "这个", "那个", "我们", "你们", "他们", "就是", "还是", "可以", "没有",
           "不是", "感觉", "然后", "一个", "小爱", "知道", "现在", "今天", "怎么", "为什么", "真的", "好像", "已经",
           "是不是", "有没有", "不知道", "我也", "我是", "你是", "他是", "这么", "那么", "因为", "所以"}


def _day(ts) -> str:
    return time.strftime("%Y-%m-%d", time.localtime(float(ts or 0)))


# ----------------------------------------------------------------------
# Who, and what the program can count
# ----------------------------------------------------------------------
def pick_people(lines, day, known=(), place="", registry=None, self_id=""):
    """Today's talkative people in one window. `lines` are phone lines ({ts, role, sender_id,
    sender_name, text}); `known` the qqs she already has an impression of here.
    Returns [{"qq", "name", "count", "lines": [their lines today]}], most lines first."""
    known = {str(q) for q in known}
    by_person, names = {}, {}
    for ln in lines or []:
        if not isinstance(ln, dict) or ln.get("role") == "assistant" or _day(ln.get("ts")) != day:
            continue
        qq = str(ln.get("sender_id") or "")
        if not qq or qq == str(self_id):
            continue
        by_person.setdefault(qq, []).append(ln)
        if ln.get("sender_name"):
            names[qq] = str(ln["sender_name"])
    picked = []
    for qq, own in by_person.items():
        if len(own) < DAILY_MIN and not (len(own) >= NEW_MIN and qq not in known):
            continue
        if registry is not None and not all(registry.may_keep(qq, place, ln.get("ts")) for ln in own):
            continue
        picked.append({"qq": qq, "name": names.get(qq, ""), "count": len(own), "lines": own})
    picked.sort(key=lambda p: (-p["count"], p["qq"]))
    return picked[:MAX_PEOPLE]


def _plain(text) -> str:
    return PART.sub("", str(text or ""))


def pet_phrases(own_lines, other_lines=()) -> list:
    """2-4 Chinese characters he says on at least 3 lines, not everyday words, not over a
    red line, and that the others in the group do not say more than he does. At most 3."""
    def per_line(lines):
        count = Counter()
        for ln in lines:
            seen = set()
            for run in HAN.findall(_plain(ln.get("text") if isinstance(ln, dict) else ln)):
                for n in (2, 3, 4):
                    seen.update(run[i:i + n] for i in range(len(run) - n + 1))
            count.update(seen)
        return count
    mine, theirs = per_line(own_lines), per_line(other_lines)
    ok = [(p, n) for p, n in mine.items()
          if n >= 3 and p not in GENERIC and len(set(p)) > 1 and not redline.hit(p) and theirs.get(p, 0) <= n]
    ok.sort(key=lambda x: (-x[1], -len(x[0]), x[0]))
    out = []
    for p, _n in ok:
        if any(p in q or q in p for q in out):
            continue
        out.append(p)
        if len(out) == MAX_PHRASES:
            break
    return out


def day_stats(own_lines, other_lines=()) -> dict:
    texts = [str(ln.get("text") or "") for ln in own_lines]
    hours = Counter(time.localtime(float(ln.get("ts") or 0)).tm_hour for ln in own_lines)
    return {
        "msgs": len(texts),
        "avg_chars": round(sum(len(_plain(t)) for t in texts) / max(1, len(texts)), 1),
        "image_ratio": round(sum(1 for t in texts if "[图片]" in t) / max(1, len(texts)), 2),
        "hours": [h for h, _n in hours.most_common(2)],
        "phrases": pet_phrases(own_lines, other_lines),
    }


# ----------------------------------------------------------------------
# What the model sees, and what is kept of its answer
# ----------------------------------------------------------------------
def material(picked) -> tuple:
    """(text for the model, {code: qq}). Each person a code; their names and @s become the
    code, long numbers '#', pictures and the like '[图]'; red-line lines are left out."""
    codes = {"P%d" % (i + 1): p["qq"] for i, p in enumerate(picked)}
    names = sorted(((p["name"], "P%d" % (i + 1)) for i, p in enumerate(picked) if len(p["name"]) >= 2),
                   key=lambda x: -len(x[0]))
    qqs = [(p["qq"], "P%d" % (i + 1)) for i, p in enumerate(picked)]
    out = []
    for code, p in zip(codes, picked):
        out.append("%s：今天说了 %d 句" % (code, p["count"]))
        for ln in p["lines"][-LINES_PER_PERSON:]:
            text = str(ln.get("text") or "")
            if redline.hit(text):
                continue
            for qq, c in qqs:
                text = text.replace(qq, c)
            for name, c in names:
                text = text.replace(name, c)
            text = PART.sub("[图]", LONG_NUMBER.sub("#", text))
            text = re.sub(r"@(?!P\d)\S{1,20}", "@某人", text)
            out.append("- " + text[:LINE_CHARS])
    return "\n".join(out), codes


PROMPT = """下面是一个群里几位群友今天说的话，每个人用代号表示（P1、P2……），代号只是为了区分人。
请给每个代号写两样东西：
- style：他说话的样子，一句话，不超过 60 个字。只写语气、用词、节奏、爱用的表达，比如“说话很快，爱用语气词，常接别人的梗”。
- topics：他今天常聊的话题，最多 3 个，每个 2 到 8 个字。
不要写数字；不要评价这个人是什么样的人（性格、人品、聪明不聪明）；不要写健康、钱、感情、家里的事、长相、工作学业；看不出来就留空。
只输出一个 JSON，不要别的文字，格式：{"P1": {"style": "...", "topics": ["...", "..."]}}

"""


def prompt_for(picked) -> tuple:
    text, codes = material(picked)
    return PROMPT + text, codes


def check_style(text) -> str:
    """The style line if it may be kept, else ''."""
    t = str(text or "").strip().strip("。")
    if not t or len(t) > STYLE_CHARS or DIGITS.search(t) or JUDGEMENT.search(t) or redline.hit(t):
        return ""
    return t


def check_topic(text) -> str:
    t = str(text or "").strip()
    lo, hi = TOPIC_CHARS
    if not (lo <= len(t) <= hi) or DIGITS.search(t) or JUDGEMENT.search(t) or redline.hit(t):
        return ""
    return t


def check_alias(text) -> str:
    """2-6 Chinese characters or 2-10 plain letters/digits, not over a red line."""
    t = str(text or "").strip()
    ok = re.fullmatch(r"[一-鿿]{2,6}", t) or re.fullmatch(r"[A-Za-z0-9_]{2,10}", t)
    return t if ok and not redline.hit(t) and not JUDGEMENT.search(t) else ""


def parse_answer(text, codes) -> dict:
    """{qq: {"style", "topics"}} for every code whose answer passed; codes that failed are left out."""
    raw = str(text or "")
    start, end = raw.find("{"), raw.rfind("}")
    try:
        data = json.loads(raw[start:end + 1]) if start >= 0 and end > start else {}
    except ValueError:
        data = {}
    out = {}
    for code, qq in codes.items():
        item = data.get(code) if isinstance(data, dict) else None
        if not isinstance(item, dict):
            continue
        style = check_style(item.get("style"))
        topics = [t for t in (check_topic(x) for x in (item.get("topics") or [])[:MAX_TOPICS * 2]) if t][:MAX_TOPICS]
        if style or topics:
            out[qq] = {"style": style, "topics": topics}
    return out


# ----------------------------------------------------------------------
# On disk
# ----------------------------------------------------------------------
def _record(place, qq):
    return {"qq": str(qq), "name": "", "aliases": [], "style": "", "topics": [], "stats": {},
            "since": "", "updated": "", "origin": discretion.make_origin(place, [str(qq)], [])}


class Store:
    """The people/ folder: one file per group."""

    def __init__(self, root):
        self.root = Path(root)

    def path(self, place) -> Path:
        place = str(place)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in place)[:60]
        return self.root / ("%s-%s.json" % (safe, hashlib.sha1(place.encode("utf-8")).hexdigest()[:12]))

    def load(self, place) -> dict:
        data = {}
        try:
            path = self.path(place)
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
        if not isinstance(data, dict) or str(data.get("place") or "") != str(place):
            data = {}  # not this group's file: start empty rather than read another group
        data["place"] = str(place)
        if not isinstance(data.get("people"), dict):
            data["people"] = {}
        return data

    def save(self, place, data) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        data["place"] = str(place)
        path = self.path(place)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(str(tmp), str(path))

    def places(self) -> list:
        out = []
        for path in sorted(self.root.glob("*.json")) if self.root.exists() else []:
            try:
                out.append(str(json.loads(path.read_text(encoding="utf-8")).get("place") or ""))
            except (OSError, ValueError):
                continue
        return [p for p in out if p]

    def forget_person(self, qq) -> int:
        """He is deleted (by the owner): his impression and how he is called, in every group."""
        n = 0
        for place in self.places():
            data = self.load(place)
            if str(qq) in data["people"]:
                del data["people"][str(qq)]
                self.save(place, data)
                n += 1
        return n

    def forget_message_by(self, place, qq) -> bool:
        """A message of his here was deleted: what the model wrote about him here goes (it may
        have come from that message); the counts stay. It is written again another night."""
        data = self.load(place)
        rec = data["people"].get(str(qq))
        if not rec or not (rec.get("style") or rec.get("topics")):
            return False
        rec["style"], rec["topics"] = "", []
        self.save(place, data)
        return True


def add_day(rec, name, stats, day) -> None:
    """Fold one day's counts into a record."""
    old = rec.get("stats") or {}
    if name:
        rec["name"] = name
    days = int(old.get("days", 0) or 0) + (0 if old.get("last_day") == day else 1)
    msgs = int(old.get("msgs", 0) or 0) + int(stats.get("msgs", 0))
    rec["stats"] = {
        "msgs": msgs, "days": days, "last_day": day,
        "avg_chars": stats.get("avg_chars", old.get("avg_chars", 0)),
        "image_ratio": stats.get("image_ratio", old.get("image_ratio", 0)),
        "hours": stats.get("hours") or old.get("hours") or [],
        "phrases": stats.get("phrases") or old.get("phrases") or [],
    }
    rec["since"] = rec.get("since") or day
    rec["updated"] = day


async def nightly(store, place, lines, ask, day, registry=None, self_id="") -> dict:
    """One group, one night. `ask` is an async callable(prompt) -> answer text (the model).
    At most one call per group per day; marked as tried before the call."""
    data = store.load(place)
    if data.get("tried") == day:
        return {"skipped": "tried today"}
    picked = pick_people(lines, day, data["people"], place, registry, self_id)
    if not picked:
        return {"skipped": "nobody"}
    picked_qq = {p["qq"] for p in picked}
    for p in picked:
        others = [ln for ln in lines if str(ln.get("sender_id") or "") not in (p["qq"], str(self_id))
                  and ln.get("role") != "assistant" and _day(ln.get("ts")) == day]
        rec = data["people"].setdefault(p["qq"], _record(place, p["qq"]))
        add_day(rec, p["name"], day_stats(p["lines"], others), day)
    data["tried"] = day
    store.save(place, data)
    prompt, codes = prompt_for(picked)
    try:
        answer = await ask(prompt)
    except Exception as exc:  # counted as the day's call all the same
        return {"called": 1, "picked": len(picked), "written": 0, "error": type(exc).__name__}
    got = parse_answer(answer, codes)
    data = store.load(place)
    for qq, item in got.items():
        rec = data["people"].get(qq)
        if rec is None or qq not in picked_qq:
            continue
        if registry is not None and not registry.may_keep(qq, place):
            continue  # deleted while the model was answering
        rec["style"] = item["style"] or rec.get("style", "")
        rec["topics"] = item["topics"] or rec.get("topics", [])
        rec["updated"] = day
    store.save(place, data)
    return {"called": 1, "picked": len(picked), "written": len(got), "rejected": len(codes) - len(got)}


# ----------------------------------------------------------------------
# Where she may use it
# ----------------------------------------------------------------------
def view(rec, rec_place, here, present_here=False, private_text="") -> dict:
    """What of an impression formed in `rec_place` she may use in `here` (None: nothing).

    same group                 -> name, aliases, style, topics
    another group, he is there -> name, aliases (to know it is the same person)
    his own private chat       -> name, aliases, style; topics only those he brought up there himself
    anywhere else              -> nothing
    """
    if not isinstance(rec, dict):
        return None
    here = discretion.place_of(here) or str(here or "")
    full = {"name": rec.get("name", ""), "aliases": list(rec.get("aliases") or []),
            "style": rec.get("style", ""), "topics": list(rec.get("topics") or [])}
    if here == str(rec_place):
        return full
    if here.startswith("group:"):
        return {"name": full["name"], "aliases": full["aliases"]} if present_here else None
    if here == "private:" + str(rec.get("qq") or ""):
        said = str(private_text or "")
        return dict(full, topics=[t for t in full["topics"] if t and t in said])
    return None


def describe(v) -> str:
    """One line for a prompt: '柠檬（大家叫她 柠柠）：说话很快；常聊 抽卡、副本'. Descriptions only."""
    if not v:
        return ""
    head = v.get("name") or "有人"
    if v.get("aliases"):
        head += "（大家叫 %s）" % "、".join(v["aliases"])
    parts = [p for p in (v.get("style"), "常聊 " + "、".join(v["topics"]) if v.get("topics") else "") if p]
    return head + ("：" + "；".join(parts) if parts else "")


# ----------------------------------------------------------------------
# From the old companion (tools/import_old.py bundle: people.jsonl, groups.jsonl)
# ----------------------------------------------------------------------
_OLD_STATS = {"口头禅": "phrases", "在本群的消息条数": "msgs", "带图比例": "image_ratio", "常在的时段": "hours",
              "平均字数": "avg_chars"}


def from_bundle(store, people=(), groups=(), registry=None, day="") -> dict:
    """Old member cards, how people were called and group profiles -> people/ files.
    Everything is checked again (style line, aliases, red lines); 'something he said
    recently' is not carried over (it may be his words)."""
    counts = Counter()
    day = day or time.strftime("%Y-%m-%d")
    for g in groups or ():
        place = str(g.get("place") or "")
        if not place.startswith("group:"):
            counts["group_no_place"] += 1
            continue
        data = store.load(place)
        text = str(g.get("text") or "")
        data["group"] = {"text": "" if redline.hit(text) or JUDGEMENT.search(text) else text,
                         "stats": dict(g.get("stats") or {}), "from": g.get("from"), "to": g.get("to"),
                         "origin": discretion.make_origin(place, [], []), "updated": day}
        store.save(place, data)
        counts["groups"] += 1
    for p in people or ():
        place, qq = str(p.get("place") or ""), str(p.get("qq") or "")
        if not place.startswith("group:") or not qq:
            counts["person_no_place"] += 1
            continue
        if registry is not None and not registry.may_keep(qq, place):
            counts["person_forgotten"] += 1
            continue
        data = store.load(place)
        rec = data["people"].setdefault(qq, _record(place, qq))
        rec["name"] = str(p.get("name") or rec.get("name") or "")
        rec["aliases"] = [a for a in (check_alias(x) for x in p.get("aliases") or []) if a]
        rec["style"] = check_style(p.get("style"))
        old = p.get("stats") or {}
        stats = {new: old[key] for key, new in _OLD_STATS.items() if key in old}
        if "phrases" in stats:
            stats["phrases"] = [x for x in stats["phrases"] if isinstance(x, str) and not redline.hit(x)][:MAX_PHRASES]
        rec["stats"] = dict(rec.get("stats") or {}, **stats)
        rec["since"] = rec.get("since") or str(p.get("from") or day)
        rec["updated"] = day
        store.save(place, data)
        counts["people"] += 1
        counts["people_style_dropped"] += 0 if rec["style"] or not p.get("style") else 1
    return dict(counts)
