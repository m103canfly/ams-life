# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What happened today in each chat window: she goes over her phone at night (the owner, 10-28).

She only keeps an event when something moves her enough; what the groups talked about
otherwise is gone from her phone after 24 hours. So every night, each window that had
messages today -- every group, and the busiest PRIVATE_MAX private chats -- gets one model
call, at most once a day (marked as tried before the call, so a failure or a restart does
not call again), and what it answers becomes events of that window:

- material: the day's lines of that window, everyone's (hers as "她"), the most recent
  MAX_LINES, each numbered, each cut to LINE_CHARS; nothing the forget registry rules out
  (person or message); everyone who spoke a code P1, P2..., every other name anyone in
  the window goes by a code Q1, Q2..., long numbers '#', other @s '@某人' -- as in the
  group impressions (impressions.masker); red-line lines left out (the plugin's switch);
- answer: at most MAX_EVENTS things that happened, each a title, what happened, who it
  is about (codes) and the lines it is drawn from; only what happened, nothing she
  thinks or feels. Every item is checked: its codes are known ones, no long numbers,
  lengths, red lines and judgements of a person (the switch); whatever fails is dropped;
- origin (the plugin): that window, public for a group and private for a private chat;
  its people and message ids from the lines it names; if it names no line or a line
  that is not there, every person who spoke today and every message of the day -- wider
  rather than something left out that could then not be forgotten.

Only the standard library; no AstrBot.
"""
from __future__ import annotations

import json
import re
import time

try:
    from . import impressions, redline
except ImportError:
    import impressions
    import redline

MAX_EVENTS = 5
MAX_LINES = 150         # the most recent lines of the day that go to the model
LINE_CHARS = 80
TITLE_CHARS = 24
WHAT_CHARS = 120
PRIVATE_MAX = 3         # private chats per night, the busiest
HER = "她"
CODE = re.compile(r"[PQ]\d+")
LONG_NUMBER = re.compile(r"\d{5,}")


def _day(ts) -> str:
    return time.strftime("%Y-%m-%d", time.localtime(float(ts or 0)))


def day_lines(lines, day, place="", registry=None) -> list:
    """The window's lines of `day` she may use: not from anyone or any message the forget
    registry rules out; her own lines by their own origin (whom she answered, and what)."""
    out = []
    for ln in lines or ():
        if not isinstance(ln, dict) or _day(ln.get("ts")) != day or not str(ln.get("text") or "").strip():
            continue
        if registry is not None:
            if ln.get("role") == "assistant":
                o = ln.get("origin") if isinstance(ln.get("origin"), dict) else {}
                if not registry.may_keep_all(_people(o), place, ln.get("ts"), o.get("source_ids") or ()):
                    continue
            elif not registry.may_keep(str(ln.get("sender_id") or ""), place, ln.get("ts"),
                                       str(ln.get("msg_id") or "")):
                continue
        out.append(ln)
    return out


def _people(origin) -> list:
    return [str(p) for p in (origin.get("people") or []) if str(p or "") not in ("", "self", HER)]


def speakers(lines) -> list:
    """Everyone who spoke, in the order they first did (not her)."""
    out = []
    for ln in lines:
        qq = str(ln.get("sender_id") or "")
        if ln.get("role") != "assistant" and qq and qq not in out:
            out.append(qq)
    return out


def material(lines, names=None, red=redline.hit) -> tuple:
    """(text for the model, {code: qq}, [the lines shown, line n is shown[n-1]]).
    `names` ({qq: names}): every name anyone in this window goes by."""
    shown = [ln for ln in lines if not red(str(ln.get("text") or ""))][-MAX_LINES:]
    code_of = {qq: "P%d" % (i + 1) for i, qq in enumerate(speakers(shown))}
    names = {str(q): {str(n) for n in ns if n and not str(n).isdigit()} for q, ns in (names or {}).items()}
    for ln in shown:
        if ln.get("role") != "assistant" and ln.get("sender_name") and ln.get("sender_id"):
            names.setdefault(str(ln["sender_id"]), set()).add(str(ln["sender_name"]))
    n_p = len(code_of)
    for qq in sorted(q for q in names if q not in code_of):
        code_of[qq] = "Q%d" % (len(code_of) - n_p + 1)
    mask = impressions.masker(code_of, {q: ns for q, ns in names.items() if q in code_of})
    rows = []
    for i, ln in enumerate(shown):
        who = HER if ln.get("role") == "assistant" else code_of.get(str(ln.get("sender_id") or ""), "有人")
        rows.append("%d %s：%s" % (i + 1, who, mask(str(ln.get("text") or ""))[:LINE_CHARS]))
    return "\n".join(rows), {c: qq for qq, c in code_of.items()}, shown


PROMPT = """下面是一个%s今天的聊天记录。每行开头是行号；说话的人用代号表示（P1、P2……；话里提到的其他人是 Q1、Q2……），“她”是小爱自己。代号只是为了区分人。
请写出今天在这里发生的几件事，最多 %d 件，挑有来龙去脉的；打招呼、刷表情、几句闲聊不算。每件写：
- title：一句标题，不超过 %d 个字；
- what：经过，一两句话，不超过 %d 个字；
- who：跟谁有关，写代号；
- lines：用到了哪几行，写行号。
只写发生了什么。不要评价人，不要写小爱的感受和看法；不要写号码；人一律用代号。没有值得记的就输出空列表。
只输出一个 JSON，不要别的文字，格式：{"events": [{"title": "...", "what": "...", "who": ["P1"], "lines": [1, 2]}]}

"""


def prompt_for(text, private=False) -> str:
    return PROMPT % ("私聊" if private else "群", MAX_EVENTS, TITLE_CHARS, WHAT_CHARS) + text


def _clean(text, limit) -> str:
    t = re.sub(r"\s+", " ", str(text or "")).strip()
    return t if 2 <= len(t) <= limit else ""


def parse_answer(text, codes, n_lines, red=redline.hit, judge=impressions.judged) -> list:
    """The items that pass: [{"title", "what", "who": [codes], "lines": [line numbers],
    "who_ok", "lines_ok"}]. An item with a code that is not one of `codes`, a long number,
    a red line or a judgement of a person (as the switch has them) is dropped; "who_ok" /
    "lines_ok" say whether it named only real codes / only lines that are there."""
    raw = str(text or "")
    start, end = raw.find("{"), raw.rfind("}")
    try:
        data = json.loads(raw[start:end + 1]) if start >= 0 and end > start else {}
    except ValueError:
        data = {}
    items = data.get("events") if isinstance(data, dict) else None
    out = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        title, what = _clean(item.get("title"), TITLE_CHARS), _clean(item.get("what"), WHAT_CHARS)
        both = "%s %s" % (title, what)
        if not (title and what) or LONG_NUMBER.search(both) or red(both) or judge(both):
            continue
        if any(c not in codes for c in CODE.findall(both)):
            continue
        who = item.get("who") if isinstance(item.get("who"), list) else []
        nums = item.get("lines") if isinstance(item.get("lines"), list) else []
        ok_who = [str(c) for c in who if str(c) in codes]
        ok_lines = [n for n in nums if isinstance(n, int) and not isinstance(n, bool) and 1 <= n <= n_lines]
        out.append({"title": title, "what": what, "who": list(dict.fromkeys(ok_who)),
                    "lines": list(dict.fromkeys(ok_lines)),
                    "who_ok": bool(who) and len(ok_who) == len(who),
                    "lines_ok": bool(nums) and len(ok_lines) == len(nums)})
        if len(out) >= MAX_EVENTS:
            break
    return out


def named(text, codes, names) -> str:
    """The codes in what the model wrote back to the names (`names`: {qq: name})."""
    return CODE.sub(lambda m: names.get(codes.get(m.group(0), ""), "") or "某人", str(text or ""))


def sources(item, codes, shown, day_all) -> tuple:
    """(people, message ids) of one item: from the lines it names (her own by their origin:
    whom she answered, and what), the people it names and the codes in its text; when it
    names no line or a wrong one, every line of the day; when it names a wrong person,
    everyone who spoke too."""
    coded = {codes[c] for c in item["who"] + CODE.findall(item["title"] + " " + item["what"]) if c in codes}
    if item["lines_ok"]:
        used = [shown[n - 1] for n in item["lines"]]
    else:
        used = day_all
    people = set(speakers(used)) | coded
    if not item["who_ok"] or not item["lines_ok"]:
        people |= set(speakers(day_all))
    ids = [str(ln.get("msg_id")) for ln in used if ln.get("msg_id")]
    for ln in used:   # her own lines: whom she answered there, and what
        if ln.get("role") == "assistant" and isinstance(ln.get("origin"), dict):
            people |= set(_people(ln["origin"]))
            ids += [str(s) for s in ln["origin"].get("source_ids") or [] if str(s or "")]
    return sorted(people), list(dict.fromkeys(ids))


# ----------------------------------------------------------------------
# Where its events are used (the discussion window, 10-28)
# ----------------------------------------------------------------------
PER_REPLY = 2           # of these events in "[最近的事]", at most
RELEVANT_MIN = 2        # pairs of characters a message must share with one of them


def is_digest(e) -> bool:
    return isinstance(e, dict) and e.get("kind") == "daily_digest"


def _pairs(text) -> set:
    t = re.sub(r"[^0-9a-z一-鿿]", "", str(text or "").lower())
    return {t[i:i + 2] for i in range(len(t) - 1)}


def relevance(message, e) -> int:
    """How much one of these events has to do with a message: the pairs of characters in a
    row (letters, digits, Chinese) they share."""
    return len(_pairs(message) & _pairs("%s %s" % (e.get("title") or "", e.get("event") or "")))


def for_reply(message, events, here) -> list:
    """Which of these events a reply here may bring up: only this window's, only those that
    have to do with the message (RELEVANT_MIN), the most to do with it first, at most PER_REPLY."""
    scored = [(relevance(message, e), i, e) for i, e in enumerate(events)
              if is_digest(e) and (e.get("origin") or {}).get("where") == here]
    return [e for n, _i, e in sorted(scored, key=lambda x: (-x[0], x[1])) if n >= RELEVANT_MIN][:PER_REPLY]


def weight(e) -> tuple:
    """How much an event matters, for picking: a strong event (not one of these) first, then
    the more people it is about, then its importance, then the newer."""
    o = e.get("origin") if isinstance(e.get("origin"), dict) else {}
    return (0 if is_digest(e) else 1, len(o.get("people") or []), float(e.get("importance", 0) or 0),
            float(e.get("ts", 0) or 0))


def pick_fairly(events, n) -> list:
    """At most `n` of `events`, fairly between windows: each window's weightiest first (the
    windows by that one), then the weightiest of the rest. In their order in `events`."""
    order = sorted(range(len(events)), key=lambda i: weight(events[i]), reverse=True)
    picked, windows = [], set()
    for i in order:
        where = (events[i].get("origin") or {}).get("where", "")
        if where not in windows:
            windows.add(where)
            picked.append(i)
    picked = picked[:n]
    for i in order:
        if len(picked) >= n:
            break
        if i not in picked:
            picked.append(i)
    return [events[i] for i in sorted(picked)]
