# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Group members she knows: a basic impression of everyone who talks a lot in a group.

What she keeps of a person, per group: what he is called there, how he talks (one
line, at most 60 characters, no numbers, no judgement of who he is), what he often
talks about (a few words), and some counts. Never a whole sentence of his: of his
words only his pet phrases, 2-4 characters each, checked against the red lines
before they are stored, deleted with his messages, and never put in a prompt
(``view`` does not return them). Never message ids. One file per group,
``people/<group>-<hash>.json``, and ``people/names.json``: every name and alias each
person went by, for making things anonymous elsewhere -- only ever added to, and it
goes only when he is deleted (deleting his impression, or an alias pushed out of the
last MAX_ALIASES, leaves it there):

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
  own lines, each person a code (P1, P2...), and every name anyone in the group goes by
  (card, nickname, known aliases) replaced by a code too, long numbers masked, red-line lines
  left out. The answer is JSON per code; every style line and topic is checked
  (red lines, judgements, numbers, length) and whatever fails is not kept -- the
  counts are kept either way.
- what others call them: the same call is shown the lines others addressed to them
  (an @ or a reply) and may propose names; a name is kept only when the program
  finds it in the window: 2-6 Chinese characters, not an everyday form of address,
  not part of someone else's group card, used by others at least twice when talking
  to him (an @, a reply, or within 20 minutes of something he said); a name proposed
  for two people goes for both.

Where she may use it (``view``), after the discretion table, decided by the owner:
in that group, all of it; in another group where he is present, only what he is
called (so she knows it is the same person); in his own private chat, name and
style, and only the topics he brought up there himself; anywhere else, nothing.

Wiring into the plugin (the nightly loop, the reply prompt, the panel, deleting)
comes with step 1, part 3-2. Only the standard library; no AstrBot.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import time
from collections import Counter
from pathlib import Path

try:
    from . import atomic_file, discretion, interpretation, redline
except ImportError:
    import atomic_file
    import discretion
    import interpretation
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
MAX_ALIASES = 4
ALIAS_MIN_USES = 2      # others called him that at least this often...
ALIAS_NEAR = 20 * 60    # ...in an @, a reply, or this close to something he said
ADDRESSED_LINES = 40    # lines others addressed to the picked people, shown to the model

# what a person is, rather than how he talks: not hers to write down about anyone
JUDGEMENT = re.compile(r"性格|人品|脾气|情商|智商|善良|自私|小气|大方|靠谱|不靠谱|好人|坏人|内向|外向|自卑|自信"
                       r"|聪明|笨蛋|愚蠢|幼稚|成熟|渣男|渣女|有钱|很穷|漂亮|帅气|好看|丑|年纪|年龄|职业|工作是"
                       r"|学生|结婚|单身")
DIGITS = re.compile(r"[0-9０-９]")


def judged(text) -> str:
    """'judgement' when `text` says what a person is (JUDGEMENT), else ''. The plugin's
    red-line switch decides whether it is held back; on its own this module holds it back."""
    return "judgement" if JUDGEMENT.search(str(text or "")) else ""
LONG_NUMBER = re.compile(r"\d{5,}")
PART = re.compile(r"\[(图片|表情|语音|视频|文件|聊天记录|戳一戳|卡片|分享|位置|音乐|骰子|猜拳|名片|消息)\]")
HAN = re.compile(r"[一-鿿]+")
# how anyone is addressed: never kept as what someone in particular is called
GENERIC_ALIASES = {"大佬", "群主", "管理", "老师", "兄弟", "姐妹", "宝贝", "宝宝", "大家", "各位", "朋友", "群友",
                   "哥哥", "姐姐", "弟弟", "妹妹", "老哥", "老弟", "老妹", "大哥", "大姐", "同学", "亲爱的",
                   "小爱", "爱弥斯", "机器人", "主人"}
# what was masked: a topic like "有人的猫" says nothing about him
MASKED = re.compile(r"有人|某人|[PQ]\d")
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
        if registry is not None and hasattr(registry, "impression_allowed") and not registry.impression_allowed(qq, place):
            continue  # the owner deleted what she thinks of him
        picked.append({"qq": qq, "name": names.get(qq, ""), "count": len(own), "lines": own})
    picked.sort(key=lambda p: (-p["count"], p["qq"]))
    return picked[:MAX_PEOPLE]


def _plain(text) -> str:
    return PART.sub("", str(text or ""))


def pet_phrases(own_lines, other_lines=(), red=redline.hit) -> list:
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
          if n >= 3 and p not in GENERIC and len(set(p)) > 1 and not red(p) and theirs.get(p, 0) <= n]
    ok.sort(key=lambda x: (-x[1], -len(x[0]), x[0]))
    out = []
    for p, _n in ok:
        if any(p in q or q in p for q in out):
            continue
        out.append(p)
        if len(out) == MAX_PHRASES:
            break
    return out


def day_stats(own_lines, other_lines=(), red=redline.hit) -> dict:
    texts = [str(ln.get("text") or "") for ln in own_lines]
    hours = Counter(time.localtime(float(ln.get("ts") or 0)).tm_hour for ln in own_lines)
    return {
        "msgs": len(texts),
        "avg_chars": round(sum(len(_plain(t)) for t in texts) / max(1, len(texts)), 1),
        "image_ratio": round(sum(1 for t in texts if "[图片]" in t) / max(1, len(texts)), 2),
        "hours": [h for h, _n in hours.most_common(2)],
        "phrases": pet_phrases(own_lines, other_lines, red),
    }


# ----------------------------------------------------------------------
# What the model sees, and what is kept of its answer
# ----------------------------------------------------------------------
def group_names(lines=(), people=None) -> dict:
    """{qq: {every name he goes by here}}: group card / nickname from the window lines, and the
    name and aliases already kept in this group's impressions."""
    out = {}
    for ln in lines or ():
        if isinstance(ln, dict) and ln.get("sender_id") and ln.get("sender_name"):
            out.setdefault(str(ln["sender_id"]), set()).add(str(ln["sender_name"]))
    for qq, rec in (people or {}).items():
        names = out.setdefault(str(qq), set())
        names.update(str(n) for n in [rec.get("name")] + list(rec.get("aliases") or []) if n)
    return out


def addressed(lines, picked, day, self_id=""):
    """Lines others said to the picked people today: an @ of their name, or a reply to one
    of their messages. (What the model looks at for what they are called.)"""
    names = {p["qq"]: [n for n in [p.get("name")] if n and len(n) >= 2] for p in picked}
    mine = {str(ln.get("msg_id") or ""): p["qq"] for p in picked for ln in p["lines"] if ln.get("msg_id")}
    out = []
    for ln in lines or []:
        who = str(ln.get("sender_id") or "")
        if not isinstance(ln, dict) or ln.get("role") == "assistant" or who == str(self_id) or _day(ln.get("ts")) != day:
            continue
        text = str(ln.get("text") or "")
        to = mine.get(str(ln.get("reply_to") or ""))
        if not to:
            to = next((q for q, ns in names.items() if any("@" + n in text for n in ns)), None)
        if to and to != who:
            out.append(ln)
    return out[-ADDRESSED_LINES:]


def masker(code_of, names):
    """text -> text as the model may see it: every QQ number in `code_of` ({qq: code}) and
    every name in `names` ({qq: names}, each qq in code_of) its code, long numbers '#',
    pictures and the like '[图]', any other @ '@某人'."""
    swaps = sorted(((n, code_of[q]) for q, ns in names.items() for n in ns
                    if len(n) >= 2 and not discretion.plain_word(n)), key=lambda x: -len(x[0]))
    # a one-character name, or one that is an everyday word, only where it plainly names
    # someone (as discretion.anonymize does)
    singles = [(discretion._one_char_name(n), code_of[q]) for q, ns in sorted(names.items()) for n in sorted(ns)
               if n and not n.isdigit() and discretion.plain_word(n)]
    qqs = sorted(code_of.items(), key=lambda x: -len(x[0]))

    def mask(text):
        for qq, c in qqs:
            text = text.replace(qq, c)
        for name, c in swaps:
            if discretion._is_english(name):
                text = discretion._english_name(name).sub(c, text)
            else:
                text = text.replace(name, c)
        for pattern, c in singles:
            text = pattern.sub(lambda m, c=c: ("@" if m.group(0).startswith("@") else "") + c, text)
        text = PART.sub("[图]", LONG_NUMBER.sub("#", text))
        return re.sub(r"@(?![PQ]\d)\S{1,20}", "@某人", text)
    return mask


def material(picked, names=None, said_to=(), red=redline.hit) -> tuple:
    """(text for the model, {code: qq}). Each picked person a code P1, P2...; everyone else in
    the group the model only sees mentioned gets Q1, Q2... -- every name anyone in the group
    goes by (`names`, from group_names) and every @ becomes a code, long numbers '#', pictures
    and the like '[图]'; red-line lines are left out."""
    codes = {"P%d" % (i + 1): p["qq"] for i, p in enumerate(picked)}
    code_of = {qq: c for c, qq in codes.items()}
    names = {str(q): set(v) for q, v in (names or {}).items()}
    for p in picked:
        if p.get("name"):
            names.setdefault(p["qq"], set()).add(p["name"])
    for qq in sorted(q for q in names if q not in code_of):
        code_of[qq] = "Q%d" % (len(code_of) - len(codes) + 1)
    mask = masker(code_of, names)
    out = []
    for code, p in zip(codes, picked):
        out.append("%s：今天说了 %d 句" % (code, p["count"]))
        for ln in p["lines"][-LINES_PER_PERSON:]:
            text = str(ln.get("text") or "")
            if red(text):
                continue
            out.append("- " + mask(text)[:LINE_CHARS])
    shown = []
    for ln in said_to or ():
        text = str(ln.get("text") or "")
        if red(text):
            continue
        shown.append("- " + mask(text)[:LINE_CHARS])
    if shown:
        out.append("别人对他们说的话：")
        out.extend(shown)
    return "\n".join(out), codes


PROMPT = """下面是一个群里几位群友今天说的话，每个人用代号表示（P1、P2……；话里提到的其他群友是 Q1、Q2……），代号只是为了区分人。
请给每个代号写两样东西：
- style：他说话的样子，一句话，不超过 60 个字。只写语气、用词、节奏、爱用的表达，比如“说话很快，爱用语气词，常接别人的梗”。
- topics：他今天常聊的话题，最多 3 个，每个 2 到 8 个字。
- aliases：别人在聊天里怎么叫他（外号、昵称，2 到 6 个字），只写真的有人这样叫他的；没有就留空。
不要写数字；不要评价这个人是什么样的人（性格、人品、聪明不聪明）；不要写健康、钱、感情、家里的事、长相、工作学业；看不出来就留空。
只输出一个 JSON，不要别的文字，格式：{"P1": {"style": "...", "topics": ["...", "..."], "aliases": ["..."]}}

"""


def prompt_for(picked, names=None, said_to=(), red=redline.hit) -> tuple:
    text, codes = material(picked, names, said_to, red)
    return PROMPT + text, codes


def check_style(text, red=redline.hit, judge=judged) -> str:
    """The style line if it may be kept, else ''."""
    t = str(text or "").strip().strip("。")
    if not t or len(t) > STYLE_CHARS or DIGITS.search(t) or judge(t) or red(t):
        return ""
    return t


def check_topic(text, red=redline.hit, judge=judged) -> str:
    t = str(text or "").strip()
    lo, hi = TOPIC_CHARS
    if not (lo <= len(t) <= hi) or DIGITS.search(t) or judge(t) or red(t) or MASKED.search(t):
        return ""
    return t


def check_alias(text, red=redline.hit, judge=judged, owner_name="") -> str:
    """2-6 Chinese characters or 2-10 plain letters/digits, not over a red line, not how
    anyone is addressed. `owner_name`: what she calls him, never kept as an alias."""
    t = str(text or "").strip()
    ok = re.fullmatch(r"[一-鿿]{2,6}", t) or re.fullmatch(r"[A-Za-z0-9_]{2,10}", t)
    generic = GENERIC_ALIASES | {interpretation.owner_display_name(owner_name)}
    return t if ok and t not in generic and not red(t) and not judge(t) else ""


def verify_aliases(proposed, lines, cards, day) -> dict:
    """{qq: [names]} kept from what the model proposed: each found in the window as said by
    others to him -- an @, a reply to him, or within ALIAS_NEAR of a line of his -- at
    least ALIAS_MIN_USES times; not part of anyone else's group card (`cards`: {qq: names});
    a name proposed for two people goes for both."""
    today = [ln for ln in lines or [] if isinstance(ln, dict) and ln.get("role") != "assistant"
             and _day(ln.get("ts")) == day]
    owner_of = {}
    for qq, names in proposed.items():
        for n in names:
            owner_of.setdefault(n, set()).add(qq)
    out = {}
    for qq, names in proposed.items():
        his = [ln for ln in today if str(ln.get("sender_id") or "") == qq]
        his_ids = {str(ln.get("msg_id") or "") for ln in his if ln.get("msg_id")}
        his_times = [float(ln.get("ts") or 0) for ln in his]
        his_cards = [c for c in cards.get(qq, ()) if c]
        kept = []
        for n in names:
            if len(owner_of.get(n, ())) > 1:
                continue
            if any(n in c or c in n for other, cs in cards.items() if other != qq for c in cs if len(c) >= 2):
                continue
            uses = 0
            for ln in today:
                if str(ln.get("sender_id") or "") == qq or n not in str(ln.get("text") or ""):
                    continue
                t = float(ln.get("ts") or 0)
                to_him = str(ln.get("reply_to") or "") in his_ids or any("@" + c in str(ln.get("text") or "")
                                                                        for c in his_cards)
                if to_him or any(abs(t - h) <= ALIAS_NEAR for h in his_times):
                    uses += 1
            if uses >= ALIAS_MIN_USES:
                kept.append(n)
        if kept:
            out[qq] = kept
    return out


def parse_answer(text, codes, red=redline.hit, judge=judged) -> dict:
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
        style = check_style(item.get("style"), red, judge)
        topics = [t for t in (check_topic(x, red, judge) for x in (item.get("topics") or [])[:MAX_TOPICS * 2])
                  if t][:MAX_TOPICS]
        aliases = [a for a in (check_alias(x, red, judge) for x in (item.get("aliases") or [])[:MAX_ALIASES * 2])
                   if a][:MAX_ALIASES]
        if style or topics or aliases:
            out[qq] = {"style": style, "topics": topics, "aliases": aliases}
    return out


# ----------------------------------------------------------------------
# On disk
# ----------------------------------------------------------------------
def _record(place, qq):
    return {"qq": str(qq), "name": "", "aliases": [], "style": "", "topics": [], "stats": {},
            "since": "", "updated": "", "origin": discretion.make_origin(place, [str(qq)], [])}


NAMES_FILE = "names.json"


class Store:
    """The people/ folder: one file per group, and NAMES_FILE ({qq: [names]})."""

    def __init__(self, root):
        self.root = Path(root)
        self._cache = {}   # path -> ((mtime, size), content): a file is read again only when it changed

    def _read(self, path) -> dict:
        """A file's content (a copy: the caller may change it), read again only when it changed."""
        try:
            st = path.stat()
        except OSError:
            self._cache.pop(path, None)
            return {}
        key = (st.st_mtime_ns, st.st_size)
        hit = self._cache.get(path)
        if not hit or hit[0] != key:
            try:
                content = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                content = {}
            hit = self._cache[path] = (key, content if isinstance(content, dict) else {})
        return copy.deepcopy(hit[1])

    def _write(self, path, content) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
        atomic_file.replace(tmp, path)
        st = path.stat()
        self._cache[path] = ((st.st_mtime_ns, st.st_size), copy.deepcopy(content))

    def path(self, place) -> Path:
        place = str(place)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in place)[:60]
        return self.root / ("%s-%s.json" % (safe, hashlib.sha1(place.encode("utf-8")).hexdigest()[:12]))

    def load(self, place) -> dict:
        data = self._read(self.path(place))
        if not isinstance(data, dict) or str(data.get("place") or "") != str(place):
            data = {}  # not this group's file: start empty rather than read another group
        data["place"] = str(place)
        if not isinstance(data.get("people"), dict):
            data["people"] = {}
        return data

    def save(self, place, data) -> None:
        data["place"] = str(place)
        self._write(self.path(place), data)

    def places(self) -> list:
        out = []
        for path in sorted(self.root.glob("*.json")) if self.root.exists() else []:
            if path.name != NAMES_FILE:
                out.append(str(self._read(path).get("place") or ""))
        return [p for p in out if p]

    def names_of(self, qq) -> list:
        """Every name and alias he went by (NAMES_FILE)."""
        return [str(n) for n in self._read(self.root / NAMES_FILE).get(str(qq)) or []]

    def keep_names(self, qq, names) -> None:
        """Add names he goes by to NAMES_FILE (never removes any)."""
        path = self.root / NAMES_FILE
        content = self._read(path)
        old = [str(n) for n in content.get(str(qq)) or []]
        new = list(dict.fromkeys(old + [str(n).strip() for n in names or () if str(n or "").strip()]))
        if new != old:
            content[str(qq)] = new
            self._write(path, content)

    def forget_impression(self, qq) -> int:
        """The owner deleted what she thinks of him: his impression in every group goes; the
        names he went by stay in NAMES_FILE, so what she remembers of him is still made
        anonymous elsewhere."""
        n = 0
        for place in self.places():
            data = self.load(place)
            rec = data["people"].pop(str(qq), None)
            if rec is not None:
                self.keep_names(qq, [rec.get("name")] + list(rec.get("aliases") or []))
                self.save(place, data)
                n += 1
        return n

    def forget_person(self, qq) -> int:
        """He is deleted (by the owner): his impression in every group, and every name he went by."""
        n = self.forget_impression(qq)
        path = self.root / NAMES_FILE
        content = self._read(path)
        if content.pop(str(qq), None) is not None:
            self._write(path, content)
        return n

    def forget_message_by(self, place, qq) -> bool:
        """A message of his here was deleted: what the model wrote about him here goes, and so do
        his pet phrases (either may have come from that message); the counts stay. They are
        worked out again another night."""
        data = self.load(place)
        rec = data["people"].get(str(qq))
        stats = (rec or {}).get("stats") or {}
        if not rec or not (rec.get("style") or rec.get("topics") or stats.get("phrases")):
            return False
        rec["style"], rec["topics"] = "", []
        if isinstance(rec.get("stats"), dict):
            rec["stats"]["phrases"] = []
        self.save(place, data)
        return True


def clean_phrases(phrases, red=redline.hit, judge=judged) -> list:
    """Pet phrases as they may be stored: 2-4 characters, no red line, no judgement, at most 3."""
    out = []
    for p in phrases or []:
        p = str(p or "").strip()
        if 2 <= len(p) <= 4 and not red(p) and not judge(p) and not DIGITS.search(p) \
                and p not in out:
            out.append(p)
    return out[:MAX_PHRASES]


def add_day(rec, name, stats, day, red=redline.hit, judge=judged) -> None:
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
        "phrases": clean_phrases(stats.get("phrases") or old.get("phrases") or [], red, judge),
    }
    rec["since"] = rec.get("since") or day
    rec["updated"] = day


async def nightly(store, place, lines, ask, day, registry=None, self_id="", extra_names=None, red=redline.hit,
                  judge=judged, still_current=None) -> dict:
    """One group, one night. `ask` is an async callable(prompt) -> answer text (the model).
    At most one call per group per day; marked as tried before the call. `extra_names`
    ({qq: names}): more names that become codes in what the model sees -- the owner's, and
    those people go by elsewhere. `red`: text -> the red line it may not cross, or '' (the
    plugin's switch; default: the red lines themselves); `judge` the same for a judgement of
    a person in what is written down (default: judged)."""
    data = store.load(place)
    if data.get("tried") == day:
        return {"skipped": "tried today"}
    picked = pick_people(lines, day, data["people"], place, registry, self_id)
    if not picked:
        return {"skipped": "nobody"}
    picked_qq = {p["qq"] for p in picked}
    safe_lines = [ln for ln in lines if isinstance(ln, dict) and not (
        discretion.origin_of(ln, place)["where"].startswith("group:")
        and discretion.origin_of(ln, place)["visibility"] == discretion.PRIVATE)]
    safe_ids = {id(ln) for ln in safe_lines}
    safe_picked = [dict(p, lines=[ln for ln in p["lines"] if id(ln) in safe_ids]) for p in picked]
    for p in picked:
        others = [ln for ln in lines if str(ln.get("sender_id") or "") not in (p["qq"], str(self_id))
                  and ln.get("role") != "assistant" and _day(ln.get("ts")) == day]
        rec = data["people"].setdefault(p["qq"], _record(place, p["qq"]))
        own_stats = [ln if id(ln) in safe_ids else dict(ln, text="") for ln in p["lines"]]
        other_stats = [ln for ln in others if id(ln) in safe_ids]
        add_day(rec, p["name"], day_stats(own_stats, other_stats, red), day, red, judge)
        store.keep_names(p["qq"], [p["name"]])
    data["tried"] = day
    store.save(place, data)
    cards = group_names(lines, data["people"])
    for qq, ns in (extra_names or {}).items():
        cards.setdefault(str(qq), set()).update(str(n) for n in ns if n and not str(n).isdigit())
    prompt, codes = prompt_for(safe_picked, cards, addressed(safe_lines, safe_picked, day, self_id), red)
    try:
        answer = await ask(prompt)
    except Exception as exc:  # counted as the day's call all the same
        return {"called": 1, "picked": len(picked), "written": 0, "error": type(exc).__name__}
    if still_current is not None and not still_current():
        return {"called": 1, "picked": len(picked), "written": 0, "skipped": "sources narrowed"}
    got = parse_answer(answer, codes, red, judge)
    names_seen = verify_aliases({qq: item["aliases"] for qq, item in got.items() if item.get("aliases")},
                                safe_lines, {q: [n for n in ns if n] for q, ns in group_names(safe_lines).items()}, day)
    data = store.load(place)
    for qq, item in got.items():
        rec = data["people"].get(qq)
        if rec is None or qq not in picked_qq:
            continue
        if registry is not None and not registry.may_keep(qq, place):
            continue  # deleted while the model was answering
        rec["style"] = item["style"] or rec.get("style", "")
        rec["topics"] = item["topics"] or rec.get("topics", [])
        if names_seen.get(qq):
            merged = list(dict.fromkeys(list(rec.get("aliases") or []) + names_seen[qq]))
            store.keep_names(qq, merged)
            rec["aliases"] = merged[-MAX_ALIASES:]
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
    if discretion.origin_of(rec, rec_place)["visibility"] == discretion.PRIVATE:
        return None
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
def from_bundle(store, people=(), registry=None, day="") -> dict:
    """What the old companion found people were called (tools/import_old.py: aliases.jsonl)
    -> people/ files: name and aliases only, each alias checked again. Nothing else of the
    old companion is carried over (the owner's decision): what she thinks of each group and
    each person grows from the replay and from her own nights."""
    counts = Counter()
    day = day or time.strftime("%Y-%m-%d")
    for p in people or ():
        place, qq = str(p.get("place") or ""), str(p.get("qq") or "")
        if not place.startswith("group:") or not qq:
            counts["person_no_place"] += 1
            continue
        if registry is not None and not registry.may_keep_untimed(qq, place):
            counts["person_forgotten"] += 1
            continue
        aliases = [a for a in (check_alias(x) for x in p.get("aliases") or []) if a]
        if not aliases:
            counts["no_alias_left"] += 1
            continue
        data = store.load(place)
        rec = data["people"].setdefault(qq, _record(place, qq))
        rec["name"] = rec.get("name") or str(p.get("name") or "")
        merged = list(dict.fromkeys(list(rec.get("aliases") or []) + aliases))
        store.keep_names(qq, [rec["name"]] + merged)
        rec["aliases"] = merged[-MAX_ALIASES:]
        rec["since"] = rec.get("since") or day
        rec["updated"] = day
        store.save(place, data)
        counts["people"] += 1
    return dict(counts)
