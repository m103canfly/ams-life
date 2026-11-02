# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Step 2 (甲, setting self_decide): she decides herself whether to answer. Pure functions:
no I/O, no model, no AstrBot. The plugin keeps the state (mixin_attention.py).

- Called (the owner, 10-29): an @ of her, a quote of her, her name; every message of a private
  chat; and someone taking up what she just said (she spoke in this window a moment ago, to him).
  Called: the model is always asked (unless the two safety nets or the night say no).
- Not called (groups only): the plugin scores the last message of a stretch (topic, people she
  knows, how much she said here lately, how long she has been quiet here) and asks the
  model only over the threshold of the level the owner picks (less / normal / more).
- Night (01:00-08:25 by default): called once she does not answer; called NIGHT_WAKE_CALLS times
  within NIGHT_WAKE_MINUTES she is woken, and answers until nobody called her for
  NIGHT_SLEEP_AGAIN_MINUTES. Never speaks up herself at night.
- Two safety nets, no fixed limits otherwise: about 30 messages an hour in one group; money a
  day (10 yuan; near it only the owner's private chat; over it nothing).
- What she sends is hers to pick (the owner, 10-29: 6): 【不说】 (nothing), a QQ face, a short line,
  or a real answer; several messages split by 【下一条】 (at most MAX_MESSAGES, the owner's 27; 10 since 11-01).
"""
from __future__ import annotations

import math
import re
import time

LEVELS = {"less": 0.55, "normal": 0.45, "more": 0.35}   # thresholds of the three levels
CONTINUE_SECONDS = 180          # someone takes up what she said: within 3 minutes
NIGHT_WAKE_CALLS = 3
NIGHT_WAKE_MINUTES = 10
NIGHT_SLEEP_AGAIN_MINUTES = 20
GROUP_HOUR_MAX = 30
MAX_MESSAGES = 10
SILENT = "【不说】"
NEXT = "【下一条】"
# the three marks she may write for herself at the end of a reply: never sent, never kept
# as words of hers; what they say goes to her own loop (life_loop.note_mark)
PUT_DOWN = "放下手上的"
OWNER_LATER = "过会儿再找他"
OWNER_REPLY_LATER = "过会儿再回"
MARK_NAMES = (PUT_DOWN, OWNER_LATER, OWNER_REPLY_LATER)
MARK_PUT_DOWN = "put_down"                 # what she put down for something that matters more
MARK_OWNER_LATER = "owner_later"           # she means to look him up herself, in a while
MARK_OWNER_REPLY_LATER = "owner_reply_later"   # she means to answer him, in a while
MARK_WHY_MAX = 40
MARK_MINUTES_MAX = 1440

# QQ's own small faces she may use, by name (the ids are QQ's: to be checked after install)
FACES = {"惊讶": 0, "撇嘴": 1, "色": 2, "发呆": 3, "得意": 4, "流泪": 5, "害羞": 6, "睡": 8, "大哭": 9,
         "尴尬": 10, "发怒": 11, "调皮": 12, "呲牙": 13, "微笑": 14, "难过": 15, "酷": 16, "偷笑": 20,
         "可爱": 21, "白眼": 22, "疑问": 32, "嘘": 33, "晕": 34, "再见": 39, "爱心": 66, "赞": 76,
         "鼓掌": 99, "坏笑": 101, "委屈": 106}
_FACE = re.compile(r"\[表情[:：]([^\]\s]{1,6})\]")
HER_NAMES = ("小爱",)
# her name as a call: at the start or after a space or a stop, and followed by a stop, a space,
# "你" or the end -- "小爱乱撞" is no call
_STOPS = r"\s，,。.！!？?：:、~～"

# what she is told she may pick (one line of the reply block; it describes, it does not order)
CHOICES_NOTE = ("你可以自己挑怎么回：不想回就只写%s；可以只回一个QQ小表情（写成[表情:名字]，名字有：%s）；"
                "可以一句短的；也可以正经回一段。"
                % (SILENT, "、".join(FACES)))
# the three marks, in the words she is given (never sent: they are hers, not his)
MARKS_NOTE = "这件事要是比你手上在做的要紧，可以在最后写【%s：为什么】。" % PUT_DOWN
MARKS_NOTE_OWNER = ("手上有事、不想马上回，可以先回一句、也可以什么都不回，写【%s：大概几分钟】；"
                    "想过会儿再找他，写【%s：大概几分钟，为什么】。这些不会发出去，不需要就别写。"
                    % (OWNER_REPLY_LATER, OWNER_LATER))
UNSEEN_IMAGE_NOTE = "这条消息里有图，但这次你没看清图里是什么：照实说没看清，别猜，也别当成之前那张。"


# ------------------------------------------------------------------
# called or not
# ------------------------------------------------------------------
def called(addresses_her, private, sender, last_reply_ts=0.0, last_reply_to=(), now=None) -> str:
    """Why she is called ("at" / "private" / "continue"), or "" when she is not."""
    now = time.time() if now is None else now
    if private:
        return "private"
    if addresses_her:
        return "at"
    if last_reply_ts and now - float(last_reply_ts) <= CONTINUE_SECONDS and str(sender) in {
            str(x) for x in (last_reply_to or ())}:
        return "continue"
    return ""


def names_her(text, names=HER_NAMES) -> bool:
    """Someone calls her by name ("小爱，在吗" / "小爱 你看" / "...吧 小爱")."""
    text = str(text or "")
    for name in names or ():
        name = str(name or "").strip()
        if name and re.search(r"(?:^|[%s@])%s(?=[%s]|你|$)" % (_STOPS, re.escape(name), _STOPS), text):
            return True
    return False


# ------------------------------------------------------------------
# night
# ------------------------------------------------------------------
def _minutes(hhmm) -> int:
    h, _, m = str(hhmm).partition(":")
    return int(h) * 60 + int(m or 0)


def is_night(now=None, start="01:00", end="08:25") -> bool:
    t = time.localtime(time.time() if now is None else now)
    m, a, b = t.tm_hour * 60 + t.tm_min, _minutes(start), _minutes(end)
    return a <= m < b if a <= b else (m >= a or m < b)


def night_gate(calls, now, awake_until=0.0, wake_calls=NIGHT_WAKE_CALLS, wake_minutes=NIGHT_WAKE_MINUTES,
               sleep_again=NIGHT_SLEEP_AGAIN_MINUTES) -> tuple:
    """At night: (answer?, woken just now?, awake until). `calls`: the times she was called
    at night lately (this one included). Awake, every call keeps her awake a while more."""
    now = float(now)
    if awake_until and now < float(awake_until):
        return True, False, now + sleep_again * 60
    recent = [t for t in calls if now - float(t) <= wake_minutes * 60]
    if len(recent) >= wake_calls:
        return True, True, now + sleep_again * 60
    return False, False, 0.0


# ------------------------------------------------------------------
# people she knows (the owner, 10-29: by the dealings; he himself the closest)
# ------------------------------------------------------------------
def familiarity(tie, now=None, owner=False) -> float:
    """0..1 from the dealings with someone: days they talked (the last 30 weigh most), times he
    called her, a private chat. The owner is always 1."""
    if owner:
        return 1.0
    now = time.time() if now is None else now
    tie = tie if isinstance(tie, dict) else {}
    today = int(now // 86400)
    days = [int(d) for d in tie.get("days") or [] if str(d).lstrip("-").isdigit()]
    recent = sum(1 for d in days if today - d < 30)
    older = sum(1 for d in days if 30 <= today - d < 90)
    calls = sum(int(n) for d, n in (tie.get("calls") or {}).items()
                if str(d).lstrip("-").isdigit() and today - int(d) < 30)
    x = 0.12 * recent + 0.04 * older + 0.04 * min(calls, 50)
    f = 1.0 - math.exp(-x) + (0.15 if tie.get("private") else 0.0)
    return round(max(0.0, min(1.0, f)), 3)


def note_tie(tie, now=None, called_her=False, private=False) -> dict:
    """The dealings, one more message: the day, a call of her, a private chat. Kept small."""
    now = time.time() if now is None else now
    tie = dict(tie) if isinstance(tie, dict) else {}
    day = int(now // 86400)
    days = [int(d) for d in tie.get("days") or [] if str(d).lstrip("-").isdigit() and day - int(d) < 90]
    if day not in days:
        days.append(day)
    tie["days"] = sorted(days)[-90:]
    calls = {k: int(v) for k, v in (tie.get("calls") or {}).items() if str(k).lstrip("-").isdigit()
             and day - int(k) < 30}
    if called_her:
        calls[str(day)] = calls.get(str(day), 0) + 1
    tie["calls"] = calls
    tie["private"] = bool(tie.get("private")) or bool(private)
    tie["last"] = now
    return tie


# ------------------------------------------------------------------
# not called: a score and a threshold
# ------------------------------------------------------------------
def score(topic=0.0, known=0.0, her_recent=0, quiet_minutes=0.0) -> float:
    """How much the last message of a stretch draws her in (no model). topic: how close it is to
    what she keeps (cosine, 0..1); known: the most familiar of who spoke (0..1); her_recent: her
    lines here in the last 10 minutes; quiet_minutes: since she last spoke here."""
    s = 0.45 * max(0.0, min(1.0, float(topic))) + 0.25 * max(0.0, min(1.0, float(known)))
    s += 0.15 * min(1.0, max(0.0, float(quiet_minutes)) / 120.0)
    s -= 0.20 * min(1.0, max(0, int(her_recent)) / 3.0)
    return round(s, 4)


def threshold(level="normal") -> float:
    return LEVELS.get(str(level or "normal"), LEVELS["normal"])


def mood_threshold(level, valence, energy) -> float:
    """Adjust the uncalled-message threshold by bounded mood and energy."""
    v = max(-1.0, min(1.0, float(valence)))
    e = max(0.0, min(1.0, float(energy)))
    adjustment = -0.10 * v + 0.10 * max(0.0, 0.5 - e)
    return max(0.20, min(0.75, threshold(level) + adjustment))


def mood_wait(seconds, valence, energy) -> float:
    """A bounded pause before deciding; this never changes the safety gates."""
    v = max(-1.0, min(1.0, float(valence)))
    e = max(0.0, min(1.0, float(energy)))
    return max(1.0, min(10.0, float(seconds) - 2.0 * v + 4.0 * max(0.0, 0.5 - e)))


# ------------------------------------------------------------------
# the two safety nets
# ------------------------------------------------------------------
def hour_ok(sent_times, now=None, most=GROUP_HOUR_MAX) -> bool:
    """Fewer than `most` messages of hers in this group in the last hour."""
    now = time.time() if now is None else now
    return sum(1 for t in sent_times or () if now - float(t) < 3600) < int(most)


def cost(usage, prices) -> float:
    """Yuan of one model call. usage: {input_miss, input_hit, output} tokens; prices: yuan a
    million tokens for each."""
    u, p = usage or {}, prices or {}
    return round(sum(float(u.get(k, 0) or 0) * float(p.get(k, 0) or 0) for k in ("input_miss", "input_hit", "output"))
                 / 1e6, 6)


def budget(spent, soft=8.0, hard=10.0) -> str:
    """"ok", "soft" (only the owner's private chat), "hard" (nothing at all)."""
    spent = float(spent or 0)
    return "hard" if spent >= float(hard) else "soft" if spent >= float(soft) else "ok"


# ------------------------------------------------------------------
# the three marks she writes for herself
# ------------------------------------------------------------------
_MARK_HEAD = re.compile("【\\s*(?:%s)" % "|".join(MARK_NAMES))
_MARK_BODY = re.compile(r"^\s*(%s)\s*[:：]\s*(.*?)\s*$" % "|".join(MARK_NAMES), re.S)
_MARK_MINUTES = re.compile(r"^\s*(\d{1,4})\s*$")


def _mark_of(inner):
    """One mark from what is between its brackets: {kind, why, minutes}, or None when miswritten."""
    match = _MARK_BODY.match(str(inner or ""))
    if not match:
        return None
    name, rest = match.group(1), match.group(2)
    if name == PUT_DOWN:
        why = " ".join(rest.split())
        if not why or len(why) > MARK_WHY_MAX:
            return None
        return {"kind": MARK_PUT_DOWN, "why": why, "minutes": 0}
    count, _, why = rest.partition("，") if "，" in rest else rest.partition(",")
    minutes = _MARK_MINUTES.match(count)
    if not minutes or not 1 <= int(minutes.group(1)) <= MARK_MINUTES_MAX:
        return None
    why = " ".join(why.split())
    if name == OWNER_REPLY_LATER:
        if why:      # this one carries no why: miswritten, so not taken
            return None
        return {"kind": MARK_OWNER_REPLY_LATER, "why": "", "minutes": int(minutes.group(1))}
    if not why or len(why) > MARK_WHY_MAX:
        return None
    return {"kind": MARK_OWNER_LATER, "why": why, "minutes": int(minutes.group(1))}


def take_marks(text, private=False):
    """Cut the marks she wrote for herself out of her words: (clean words, marks).

    The marks are never sent and never kept as words of hers. One written badly (no
    closing bracket, minutes outside 1-1440, too long a why) is cut out too, and is not
    taken. 【过会儿再找他】 and 【过会儿再回】 count only in his private chat: anywhere else
    they are cut out as if she had not written them."""
    text = str(text or "")
    pieces, marks, at = [], [], 0
    for head in _MARK_HEAD.finditer(text):
        if head.start() < at:
            continue
        close = text.find("】", head.end())
        if close < 0:
            # never closed: the rest is cut out, and nothing of it is taken
            end, mark = len(text), None
        else:
            end, mark = close + 1, _mark_of(text[head.start() + 1:close])
        pieces.append(text[at:head.start()])
        if mark is not None and (private or mark["kind"] == MARK_PUT_DOWN):
            marks.append(mark)
        at = end
    pieces.append(text[at:])
    return "".join(pieces), marks


# ------------------------------------------------------------------
# what she sends
# ------------------------------------------------------------------
def silent(text) -> bool:
    """She chose to say nothing: the reply is 【不说】 alone (or nothing at all)."""
    t = str(text or "").strip()
    return not t or t.replace(SILENT, "").strip() == "" and SILENT in t


PIECES_NOTE = "绝大多数时候只写一段（发一条）。只有在确有必要时才可以分段（最多不超过 10段）。一段里别换行。"


def split(text, most=MAX_MESSAGES) -> list:
    """Split ordinary lines, preserving fenced code and consecutive list lines."""
    parts, block, kind = [], [], None

    def flush():
        if block:
            parts.append("\n".join(block).strip())
            block.clear()

    for line in str(text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if kind == "code":
            block.append(line)
            if line.lstrip().startswith("```"):
                flush()
                kind = None
            continue
        if line.lstrip().startswith("```"):
            flush()
            block.append(line)
            if line.count("```") >= 2:
                flush()
                kind = None
            else:
                kind = "code"
            continue
        if re.match(r"^\s*(?:[-·] |\d+\.\s*)", line):
            block.append(line)
            kind = "list"
            continue
        flush()
        kind = None
        parts.extend(p.strip() for p in line.split(NEXT) if p.strip())
    flush()
    parts = [p for p in parts if p]
    if len(parts) > most:
        parts = parts[:most - 1] + [" ".join(parts[most - 1:])]
    return parts


def pieces(text) -> list:
    """One message as ("text", words) and ("face", id) in order; an unknown face name stays text."""
    out, at = [], 0
    for m in _FACE.finditer(str(text or "")):
        if m.group(1) not in FACES:
            continue
        if m.start() > at and str(text)[at:m.start()].strip():
            out.append(("text", str(text)[at:m.start()].strip()))
        out.append(("face", FACES[m.group(1)]))
        at = m.end()
    rest = str(text or "")[at:].strip()
    if rest:
        out.append(("text", rest))
    return out


def typing_seconds(text) -> float:
    """A pause before the next message, as if typing it: 1 to 3 seconds by its length."""
    return round(min(3.0, 1.0 + len(str(text or "")) / 30.0), 2)
