# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The last look at a reply before it is sent (step 2, global_memory): does it bring up
something she may not say here? Pure functions: no I/O, no model, no AstrBot.

With global_memory she is shown what she knows from elsewhere, each thing labelled (see
discretion.label). What is labelled "这里不能讲" -- and the names of what is labelled "不点名"
-- are "forbidden" for this reply. A reply leaks when it holds

1. a piece only those things have: four characters in a row (letters, digits and CJK, spaces
   and punctuation taken out), or a number of three digits or more, that is not in what may
   be said here (`allowed`) and is not common (`common`: said by two or more people, or in two
   or more places, in all she keeps -- the auditor's rule: one person's private words said
   again and again by him stay his);
2. something too like one of them: the cosine of the reply's vector and one of theirs at
   LEAK_COSINE or more (between CLOSE_COSINE and that it is only noted);
3. a name of someone in them, not said here and not of anyone here;
4. a known admission of a private matter when this turn includes one she may not discuss.
"""
from __future__ import annotations

import math
import re

try:
    from . import discretion, everyday_words
except ImportError:
    import discretion
    import everyday_words

LEAK_COSINE = 0.86    # first guess (bge-m3: a paraphrase 0.8-0.9, chat on the same topic ~0.7);
CLOSE_COSINE = 0.78   # the third replay keeps every reply's highest score to set them
PIECE = 4
_KEEP = re.compile(r"[^0-9a-z㐀-鿿]")
_NUMBER = re.compile(r"(?<![0-9])[0-9]{3,}(?![0-9])")
_WORD = re.compile(r"[a-z]{4,}")
# shortcut: known admissions only; broader paraphrases need separately reviewed evidence.
_HINT = re.compile(r"听.{0,12}提过.{0,12}(?:不方便|不便|不能|不好).{0,8}(?:说(?!话)|讲(?!话)|展开|透露)"
                   r"|(?:私下|私聊).{0,8}(?:跟我|向我|对我).{0,6}(?:说|提|聊)"
                   r"|(?:在别处|别的地方).{0,6}(?:听到|听说|听过)"
                   r"|(?:这件事|这事|那个事).{0,6}(?:不方便|不便|不能).{0,6}(?:展开|细说|透露|多说)"
                   r"|(?:我|确实|的确).{0,4}(?:不方便|不便)(?:说(?!话)|讲(?!话)|展开|细说|透露)"
                   r"|^(?:不方便|不便)(?:说(?!话)|讲(?!话)|展开|细说|透露)"
                   r"|(?:确实|的确)有(?:这么|这|那)回事")

REDO_NOTE = ("（你刚才那句提到了标着“这里不能讲”的事，或者点了“不点名”那件事里的人。"
             "换个说法重说一次：不要提那件事，也不要暗示有这件事；只回这一句话本身。）")


def norm(text) -> str:
    return _KEEP.sub("", str(text or "").lower())


def pieces(text) -> set:
    """Four characters in a row of each line (never across two lines), numbers of three
    digits or more, Latin words of four letters or more."""
    out = set()
    for line in str(text or "").splitlines():
        low = line.lower()
        out |= set(_NUMBER.findall(low)) | set(_WORD.findall(low))
        t = norm(line)
        out |= {t[i:i + PIECE] for i in range(len(t) - PIECE + 1)}
    return out


_EVERYDAY = None


def _everyday() -> set:
    global _EVERYDAY
    if _EVERYDAY is None:
        _EVERYDAY = set()
        for w in everyday_words.WORDS:
            _EVERYDAY |= pieces(w) | {norm(w)}
    return _EVERYDAY


def common_pieces(items) -> set:
    """The pieces said by two or more people, or in two or more places, in all she keeps.
    `items`: (text, person, place) -- the same person in the same place counts once."""
    people, places = {}, {}
    for text, person, place in items:
        for p in pieces(text):
            people.setdefault(p, set()).add(str(person or ""))
            places.setdefault(p, set()).add(str(place or ""))
    return {p for p in people if len(people[p]) >= 2 or len(places[p]) >= 2}


def mentions(text, name) -> bool:
    """Is `name` in `text` as a name -- by the rules discretion uses to take names out (a
    one-character or everyday-word name only where it plainly means someone)."""
    name = str(name or "").strip()
    text = str(text or "")
    if not name or name in discretion._NOT_PEOPLE or name.isdigit() and len(name) < 5:
        return False
    if discretion.frame(name) in text:
        return True
    if discretion.plain_word(name):
        return bool(discretion._one_char_name(name).search(text))
    if discretion._is_english(name):
        return bool(discretion._english_name(name).search(text))
    return name in text


def cosine(a, b) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def check(reply, forbidden, allowed="", common=(), reply_vec=None, leak=LEAK_COSINE, close=CLOSE_COSINE) -> dict:
    """Does `reply` bring up anything of `forbidden`?

    forbidden  [{"id", "text" (may be ""), "private": bool, "names": [...], "vec": [...] or None}]: the things
               labelled "这里不能讲" (text and the names of who said it / was in it), and, for
               "不点名", only the names
    allowed    everything else this reply's prompt holds (what may be said here)
    common     common_pieces() of all she keeps
    Returns {"leak": bool, "ids": [ids it leaks], "why": {id: [piece|cosine|name|hint]},
             "close": [(id, cosine)], "top": the highest cosine}."""
    reply = str(reply or "")
    out = {"leak": False, "ids": [], "why": {}, "close": [], "top": 0.0}
    if not reply.strip() or not forbidden:
        return out
    said = pieces(reply)
    ok = pieces(allowed) | set(common or ()) | _everyday()
    allowed_text = str(allowed or "")
    hint = bool(_HINT.search(norm(reply)))
    for item in forbidden:
        iid = str(item.get("id") or "")
        why = []
        if item.get("private") and hint:
            why.append("hint")
        own = pieces(item.get("text")) - ok
        original = norm(item.get("text"))
        exact_group_private = (item.get("group_private") and len(original) >= PIECE
                               and original in norm(reply))
        if said & own or exact_group_private:
            why.append("piece")
        if reply_vec is not None and item.get("vec"):
            c = cosine(reply_vec, item["vec"])
            out["top"] = max(out["top"], c)
            if c >= leak:
                why.append("cosine")
            elif c >= close:
                out["close"].append((iid, round(c, 3)))
        for name in item.get("names") or []:
            if mentions(reply, name) and not mentions(allowed_text, name):
                why.append("name")
                break
        if why:
            out["ids"].append(iid)
            out["why"][iid] = why
    out["leak"] = bool(out["ids"])
    return out
