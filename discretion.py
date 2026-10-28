# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Where a memory came from, and where she may bring it up again.

Every memory, event and note carries an ``origin``:

    {"where": "group:<id>" | "private:<qq>" | "web:<url>" | "self",
     "people": [qq, ...],          # who it is about / whose messages it came from
     "source_ids": [msg id, ...],  # the messages it was distilled from (forgetting deletes by these)
     "visibility": "public" | "private" | "self"}

and ``verdict(origin, here)`` applies the discretion table of the plan:

    came from            | same place | another group / a private chat
    ---------------------|------------|-----------------------------------------------
    said openly in group | full       | anon: may be mentioned, never "X said ..."
    told in private      | full       | drop (only ever in that private chat)
    her own / web page   | full       | full

Anything whose origin cannot be worked out is treated as private to an unknown
place, so it is never shown anywhere.  Pure functions only: no I/O, no AstrBot.
"""
from __future__ import annotations

import re

try:
    from . import everyday_words
except ImportError:
    import everyday_words

PUBLIC, PRIVATE, SELF = "public", "private", "self"
FULL, ANON, DROP = "full", "anon", "drop"
SOMEONE = "有人"
SOMEBODY = "某人"   # someone deleted, or an @ with no name: in what she keeps
NUMBER = "[号码]"   # a number she knows to be someone's or some chat's
_NOT_PEOPLE = {"", "self", "summary", "unknown", "她"}
_KIND = re.compile(r"(FriendMessage|GroupMessage|GuildMessage|TempMessage|OtherMessage)")


def place_of(session) -> str:
    """'default:GroupMessage:42' or 'default_GroupMessage_42' -> 'group:42'; private chats -> 'private:<qq>'."""
    text = str(session or "").strip()
    if not text:
        return ""
    if text == SELF or text.startswith(("group:", "private:", "web:", "other:")):
        return text
    match = _KIND.search(text)
    if not match:
        return "other:" + text
    ident = text[match.end():].strip(":_")
    kind = match.group(1)
    if kind in ("GroupMessage", "GuildMessage"):
        return "group:" + ident
    if kind in ("FriendMessage", "TempMessage"):
        return "private:" + ident
    return "other:" + ident


def visibility_of(where: str) -> str:
    where = str(where or "")
    if where.startswith(("group:", "web:")):
        return PUBLIC
    if where == SELF:
        return SELF
    return PRIVATE


def make_origin(where, people=(), source_ids=(), visibility=None) -> dict:
    where = place_of(where)
    seen_people = [str(p) for p in (people or []) if str(p or "") not in _NOT_PEOPLE]
    seen_ids = [str(s) for s in (source_ids or []) if str(s or "")]
    # no cap: whoever or whatever is left out could not be forgotten
    return {"where": where,
            "people": list(dict.fromkeys(seen_people)),
            "source_ids": list(dict.fromkeys(seen_ids)),
            "visibility": visibility if visibility in (PUBLIC, PRIVATE, SELF) else visibility_of(where)}


def origin_of(item, fallback_where="") -> dict:
    """The item's stored origin, or one worked out from its provenance (older records)."""
    if not isinstance(item, dict):
        return make_origin("")
    stored = item.get("origin")
    if isinstance(stored, dict) and "where" in stored:
        return make_origin(stored.get("where"), stored.get("people"), stored.get("source_ids"),
                           stored.get("visibility"))
    prov = item.get("provenance") if isinstance(item.get("provenance"), dict) else {}
    where = place_of(prov.get("session") or item.get("session") or fallback_where)
    people, refs = [], []
    for src in [prov] + [s for s in (prov.get("sources") or []) if isinstance(s, dict)]:
        people.append(src.get("sender_id"))
        refs.extend(src.get("message_refs") or [])
    people.extend(prov.get("senders") or [])
    people.append(item.get("sender_id"))
    if where.startswith("private:"):
        people.append(where.split(":", 1)[1])
    return make_origin(where, people, refs)


def merge(origins) -> dict:
    """Origin of something distilled from several items: as narrow as its narrowest source."""
    origins = [o for o in (origins or []) if isinstance(o, dict)]
    if not origins:
        return make_origin("")
    people, refs = [], []
    for o in origins:
        people.extend(o.get("people") or [])
        refs.extend(o.get("source_ids") or [])
    places = {str(o.get("where") or "") for o in origins}
    vis = {str(o.get("visibility") or PRIVATE) for o in origins}
    where = places.pop() if len(places) == 1 else ""
    if PRIVATE in vis:
        visibility = PRIVATE
    elif PUBLIC in vis:
        visibility = PUBLIC
    else:
        visibility = SELF
    return make_origin(where, people, refs, visibility)


def verdict(origin, here) -> str:
    """full / anon / drop for bringing an item with `origin` up in place `here`."""
    o = origin if isinstance(origin, dict) else {}
    where = str(o.get("where") or "")
    vis = str(o.get("visibility") or PRIVATE)
    if vis == SELF or where == SELF or where.startswith("web:"):
        return FULL
    if where and where == place_of(here):
        return FULL
    if vis == PUBLIC:
        return ANON  # said openly (one place, or several merged): without names
    return DROP


# a one-character name ("鹿") is only a name where it plainly means someone: after an @, or
# as the one who says something ("鹿说", "鹿：") -- never inside other words ("小鹿乱撞");
# so is a name that is an everyday word ("周末": "周末说" is him, "周末一起玩" is not)
_HAN = "一-鿿"


def plain_word(name) -> bool:
    """A name only taken for one where it plainly means someone (see _one_char_name)."""
    name = str(name or "")
    return (len(name) < 2 and not name.isdigit()) or name in everyday_words.WORDS
_SAYS = "说|讲|问|答|觉得|认为|提到|：|:"


def _one_char_name(name):
    n = re.escape(name)
    word = _HAN + ("A-Za-z0-9_" if name.isascii() else "")   # "A" is not a name inside "@Alice"
    return re.compile(r"@%s(?![%s])|(?<![%s@])%s(?=%s)" % (n, word, word, n, _SAYS))


def _is_english(name) -> bool:
    return name.isascii() and not name.isdigit()


def _english_name(name):
    """An English name is a whole word: "Al" is not a name inside "Alice"."""
    return re.compile(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(name))


def anonymize(text, names, to=SOMEONE) -> str:
    """Replace the names and QQ numbers of the people involved with "有人" (or `to`)."""
    out = str(text or "")
    for name in sorted({str(n).strip() for n in (names or []) if str(n or "").strip()}, key=len, reverse=True):
        if name in _NOT_PEOPLE:
            continue
        if plain_word(name):
            out = _one_char_name(name).sub(lambda m: ("@" if m.group(0).startswith("@") else "") + to, out)
            continue
        if _is_english(name):
            out = _english_name(name).sub(to, out)
            continue
        out = out.replace(name, to)
    return out


# an @ as AstrBot writes it into the text, " @昵称(号码) " -- a group card may hold spaces and
# brackets, so the name is anything up to the brackets that hold a number -- and a bare "@号码"
_AT_NAMED = re.compile(r"@([^@\n]{0,40}?)\s*[(（](\d{5,})[)）]")
_AT_NUMBER = re.compile(r"@(\d{5,})(?![0-9])")


def at_names(text) -> list:
    """(name, number) of every "@昵称(号码)" in `text`."""
    return [(m.group(1).strip(), m.group(2)) for m in _AT_NAMED.finditer(str(text or ""))]


def strip_numbers(text, numbers=(), her=(), her_name="", gone=(), ats=()) -> str:
    """A message as she keeps it: an @ keeps the name only ("@昵称"; "@某人" with no name or
    for someone deleted; her own name for an @ of her), and every number in `numbers` (whole
    numbers only) becomes NUMBER. Other long numbers are left alone. `ats`: (name, number) of
    the message's own @ parts, replaced exactly first ("@名字(号码)", whatever the name holds)."""
    her, gone = {str(x) for x in her}, {str(x) for x in gone}

    def at(name, qq):
        if qq in her:
            return "@" + (her_name or SOMEBODY)
        if qq in gone:
            return "@" + SOMEBODY
        return "@" + (name.strip() or SOMEBODY)
    out = str(text or "")
    for name, qq in sorted(ats, key=lambda x: -len(str(x[0]))):
        if name and qq:
            out = out.replace("@%s(%s)" % (name, qq), at(name, str(qq)))
    out = _AT_NAMED.sub(lambda m: at(m.group(1), m.group(2)), out)
    out = _AT_NUMBER.sub(lambda m: at("", m.group(1)), out)
    nums = sorted({str(n) for n in numbers if len(str(n)) >= 5 and str(n).isdigit()}, key=len, reverse=True)
    if nums:
        out = re.sub(r"(?<![0-9])(?:%s)(?![0-9])" % "|".join(nums), NUMBER, out)
    return out


def names_in(item) -> list:
    """Every name and id an item carries about the people involved."""
    if not isinstance(item, dict):
        return []
    out = [item.get("sender_name"), item.get("sender_id")]
    prov = item.get("provenance") if isinstance(item.get("provenance"), dict) else {}
    for src in [prov] + [s for s in (prov.get("sources") or []) if isinstance(s, dict)]:
        out.extend([src.get("sender_name"), src.get("sender_id")])
    out.extend(prov.get("senders") or [])
    out.extend(origin_of(item).get("people") or [])
    return [str(x) for x in out if str(x or "").strip()]


def is_about(origin, person=None, source_ids=None) -> bool:
    """For forgetting: does this item come from / concern `person`, or from one of `source_ids`?"""
    o = origin if isinstance(origin, dict) else {}
    if person and str(person) in {str(p) for p in (o.get("people") or [])}:
        return True
    if source_ids:
        wanted = {str(s) for s in source_ids if str(s or "")}
        if wanted & {str(s) for s in (o.get("source_ids") or [])}:
            return True
    return False
