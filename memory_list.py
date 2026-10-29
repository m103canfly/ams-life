# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What she keeps, as a list for the panel ("她记住了什么", page/memories), read only.

Built from the brain map's snapshot (brain_graph.build, made by mixin_brain), so it holds
exactly what the map may show: the forget registry was asked about every memory, event
and note, and about every impression, when the snapshot was made; the places carry the
same labels ("群1", "私聊1") within one run of the plugin; ids are the page's keyed ids.

Four kinds, newest first: memories, events (the nightly note of the day too), her
notebook, and what she thinks of people (one row per group and person). Every row says
where it came from, when, where it may be said and who it is about. Long numbers are
hidden ("[号码]"); the words as kept come only on a second call (number()), one row at
a time. Paged: at most PAGE_MAX rows a call, with a token for the next page.
"""
from __future__ import annotations

import time

try:
    from . import brain_graph
except ImportError:
    import brain_graph

PAGE_MAX = 50
KINDS = ("memory", "event", "note", "impression")
KIND_NAMES = {"memory": "记忆", "event": "事件", "note": "本子", "impression": "群友印象"}
VIS = ("public", "private", "self")


def _date_ts(day) -> float:
    try:
        return time.mktime(time.strptime(str(day or "")[:10], "%Y-%m-%d"))
    except ValueError:
        return 0.0


def _item_text(kind, item) -> str:
    if kind == "event":
        return "\n".join(str(item.get(k) or "") for k in ("title", "small_summary", "event") if item.get(k))
    return str(item.get("text") or "")


def _impression_text(rec) -> str:
    parts = []
    if rec.get("name"):
        parts.append("叫“%s”" % rec["name"])
    if rec.get("aliases"):
        parts.append("称呼：" + "、".join(str(a) for a in rec["aliases"]))
    if rec.get("style"):
        parts.append("说话：" + str(rec["style"]))
    if rec.get("topics"):
        parts.append("常聊：" + "、".join(str(t) for t in rec["topics"]))
    return "；".join(parts)


def rows(snap, impressions, ids) -> list:
    """Every row of the list, with its words as kept (`raw`, never sent as it is)."""
    out = []
    for pid, entry in snap.index.items():
        if pid.startswith("_"):
            continue
        kind, raw, info = entry
        if kind not in ("memory", "event", "note"):
            continue
        item, o = info["item"], info["origin"]
        place = snap.index["_windows"].get(brain_graph._window_place(o["where"]), "")
        out.append({"id": pid, "kind": kind, "place": place, "where": brain_graph._where_text(snap, o["where"]),
                    "ts": brain_graph._num(item.get("ts")), "vis": o["visibility"],
                    "who": [brain_graph._person_name(snap, q) for q in o["people"] if q in snap.index["_people"]],
                    "raw": _item_text(kind, item), "entry": raw if kind == "memory" else ""})
    for where, recs in (impressions or {}).items():
        place = snap.index["_windows"].get(brain_graph._window_place(where))
        if not place:
            continue
        for qq, rec in (recs or {}).items():
            # only people the map may show: the registry was asked about each (keep_person),
            # besides whether what she thinks of him was stopped (keep_impression)
            if not isinstance(rec, dict) or str(qq) not in snap.index["_people"]:
                continue
            out.append({"id": ids("i", "%s|%s" % (where, qq)), "kind": "impression", "place": place,
                        "where": brain_graph._label(snap, place), "ts": _date_ts(rec.get("updated") or rec.get("since")),
                        "vis": "public", "who": [str(rec.get("name") or "") or brain_graph._person_name(snap, str(qq))],
                        "raw": _impression_text(rec), "entry": ""})
    return out


def places(snap) -> list:
    """The places for the filter: [{id, label}], groups first."""
    out = [{"id": pid, "label": brain_graph._label(snap, pid), "sub": snap.index[pid][2].get("sub", "")}
           for _place, pid in snap.index["_windows"].items()]
    return sorted(out, key=lambda x: (x["sub"] != "group", len(x["label"]), x["label"]))


def _shown(row) -> dict:
    text = brain_graph._words(row["raw"])
    return {"id": row["id"], "kind": row["kind"], "kind_name": KIND_NAMES[row["kind"]], "place": row["place"],
            "where": row["where"], "ts": round(row["ts"]), "date": brain_graph._date(row["ts"]), "vis": row["vis"],
            "may": brain_graph._MAY.get(row["vis"], brain_graph._MAY["private"]), "who": [w for w in row["who"] if w],
            "text": text, "has_number": text != row["raw"], "entry": row["entry"]}


def _when(x, end=False) -> float:
    """A date (YYYY-MM-DD, the whole day) or seconds; 0 when not given."""
    x = str(x or "").strip()
    if not x:
        return 0.0
    if x.replace(".", "", 1).isdigit():
        return float(x)
    t = _date_ts(x)
    return t + 86400 - 0.001 if t and end else t


def select(all_rows, kind="", place="", vis="", start="", end="", q="") -> list:
    """The rows that match, newest first. `q` is looked for in the words as shown (numbers
    hidden) and the names, never in a hidden number."""
    lo, hi, q = _when(start), _when(end, True), str(q or "").strip()[:50]
    out = []
    for r in all_rows:
        if kind and r["kind"] != kind or place and r["place"] != place or vis and r["vis"] != vis:
            continue
        if lo and r["ts"] < lo or hi and r["ts"] > hi:
            continue
        if q and q not in brain_graph._words(r["raw"]) and not any(q in w for w in r["who"]):
            continue
        out.append(r)
    return sorted(out, key=lambda r: (-r["ts"], r["id"]))


def page(selected, after="", limit=PAGE_MAX) -> dict:
    """One page of `selected` (as select() sorts it) after the token `after`."""
    try:
        limit = max(1, min(PAGE_MAX, int(limit or PAGE_MAX)))
    except ValueError:
        limit = PAGE_MAX
    start = 0
    if after:
        ts, _, pid = str(after).partition("~")
        try:
            key = (-float(ts), pid)
        except ValueError:
            key = None
        if key is not None:
            start = next((i for i, r in enumerate(selected) if (-r["ts"], r["id"]) > key), len(selected))
    chunk = selected[start:start + limit]
    more = start + limit < len(selected)
    return {"items": [_shown(r) for r in chunk], "total": len(selected),
            "next": ("%r~%s" % (chunk[-1]["ts"], chunk[-1]["id"])) if more and chunk else ""}


def number(all_rows, pid):
    """The words of one row as kept (the second click), or None."""
    for r in all_rows:
        if r["id"] == pid:
            return {"id": pid, "text": r["raw"]}
    return None
