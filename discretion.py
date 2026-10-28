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

PUBLIC, PRIVATE, SELF = "public", "private", "self"
FULL, ANON, DROP = "full", "anon", "drop"
SOMEONE = "有人"
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


def anonymize(text, names) -> str:
    """Replace the names and QQ numbers of the people involved with "有人"."""
    out = str(text or "")
    for name in sorted({str(n).strip() for n in (names or []) if str(n or "").strip()}, key=len, reverse=True):
        if name in _NOT_PEOPLE or (len(name) < 2 and not name.isdigit()):
            continue
        out = out.replace(name, SOMEONE)
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
