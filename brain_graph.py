# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The brain map's data (pages/brain, docs/brain-viz.md): what she keeps, as stars
and lines, read only.

- build(): what the plugin keeps -> the page's format (ams-life.brain/1). The graph
  carries no words, names or numbers: the ids are made up for the page (a keyed
  hash, so the same person gets the same id while the key lasts), labels are
  "群1 / 私聊1 / 人1" and categories.
- detail(): what one star holds, only when the owner opens it; a QQ number only
  on a second click (reveal_qq).
- search(): the ids whose words match, never the words.
- Whatever the forget registry rules out never appears: `keep` is asked about
  every item and every person, and when it raises (the registry cannot be read)
  build() raises too and nothing is returned.
- TurnLog: what each reply recalled and what the discretion table held back, as
  ids only (no words), the last TURNS_MAX turns.

Only the standard library; no AstrBot.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from pathlib import Path

try:
    from . import atomic_file, discretion
except ImportError:
    import atomic_file
    import discretion

SCHEMA = "ams-life.brain/1"
TURNS_MAX = 200
TURN_IDS_MAX = 12          # recalled / held ids kept per turn
PART_NODES = 2000          # one answer of page/brain carries at most this many stars ...
PART_EDGES = 4000          # ... and lines; the rest comes in further parts
SEARCH_MAX = 200
DETAIL_TEXT_MAX = 600
BODY_KEYS = ("social", "curiosity", "boredom", "seen", "talked", "stress", "valence")

_EMOTION = {"joy": "开心", "happy": "开心", "happiness": "开心", "excitement": "兴奋", "love": "喜欢",
            "gratitude": "感激", "pride": "得意", "relief": "松口气", "calm": "平静", "neutral": "平常",
            "curiosity": "好奇", "surprise": "惊讶", "sadness": "难过", "sad": "难过", "loneliness": "寂寞",
            "anger": "生气", "frustration": "烦", "fear": "害怕", "anxiety": "担心", "worry": "担心",
            "shame": "不好意思", "guilt": "愧疚", "disgust": "讨厌", "boredom": "无聊", "confusion": "困惑"}


def _num(x, default=0.0) -> float:
    try:
        v = float(x)
        return default if v != v else v
    except (TypeError, ValueError):
        return default


def _clip01(x) -> float:
    return round(max(0.0, min(1.0, _num(x))), 3)


def _date(ts) -> str:
    ts = _num(ts)
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts)) if ts > 0 else ""


def _window_place(where) -> str:
    where = str(where or "")
    return where if where.startswith(("group:", "private:")) else ""


class PageIds:
    """Ids for the page: kind + a keyed hash of what the plugin calls it. Without the key
    (it never leaves the plugin) nobody can work a QQ number or group number back out."""

    def __init__(self, key: bytes):
        self.key = bytes(key)

    def __call__(self, kind, raw) -> str:
        digest = hmac.new(self.key, ("%s|%s" % (kind, raw)).encode("utf-8"), hashlib.sha256).hexdigest()
        return "%s:%s" % (kind, digest[:10])


def body_of(snapshot) -> dict:
    """Her body's seven numbers from a BioCore snapshot."""
    s = snapshot if isinstance(snapshot, dict) else {}
    drives = ((s.get("homeostasis") or {}).get("drives") or {}) if isinstance(s.get("homeostasis"), dict) else {}
    out = {"social": s.get("social"), "curiosity": drives.get("curiosity", s.get("novelty_need")),
           "boredom": s.get("boredom"), "seen": s.get("seen_need"), "talked": s.get("talked"),
           "stress": s.get("stress")}
    out = {k: _clip01(v) for k, v in out.items()}
    out["valence"] = round(max(-1.0, min(1.0, _num(s.get("v")))), 3)
    return out


class Snapshot:
    """One build: the graph (in parts), and what the detail and search look up."""

    def __init__(self, graph, index, token):
        self.graph, self.index, self.token = graph, index, token
        self.made = time.time()
        n, e = graph["nodes"], graph["edges"]
        self.parts = max(1, -(-len(n) // PART_NODES), -(-len(e) // PART_EDGES))

    def part(self, k) -> dict:
        k = int(k)
        nodes = self.graph["nodes"][k * PART_NODES:(k + 1) * PART_NODES]
        edges = self.graph["edges"][k * PART_EDGES:(k + 1) * PART_EDGES]
        out = {"part": k, "parts": self.parts, "snap": self.token, "nodes": nodes, "edges": edges}
        if k == 0:
            out.update({key: v for key, v in self.graph.items() if key not in ("nodes", "edges")})
        return out


def build(src, ids, keep_item, keep_person, keep_impression=None) -> Snapshot:
    """src: what the plugin read (see BrainMixin._brain_sources):
        now, memories, events, notes, records {qq: {names, ts}}, impressions {place: {qq: rec}},
        windows {place: {lines24, last, names {qq: name}}}, body, turns (TurnLog rows).
    ids: PageIds. keep_item(item) / keep_person(qq, at) / keep_impression(qq, place): may it be
    shown? They raise when the forget registry cannot be read, and so does build()."""
    now = _num(src.get("now"), time.time())
    nodes, edges, index = {}, [], {}
    about, first_seen, last_seen, names = {}, {}, {}, {}
    person_ok = {}

    def seen(qq, ts):
        ts = _num(ts) or now
        first_seen[qq] = min(first_seen.get(qq, ts), ts)
        last_seen[qq] = max(last_seen.get(qq, 0.0), ts)

    def name(qq, n):
        n = str(n or "").strip()
        if qq and n and n not in names.setdefault(qq, []):
            names[qq].append(n)

    def person_shown(qq):
        if qq not in person_ok:
            person_ok[qq] = bool(keep_person(qq, last_seen.get(qq) or None)) and bool(keep_person(qq, None))
        return person_ok[qq]

    # ---------------------------------------------------------------- who is known by what
    for qq, rec in (src.get("records") or {}).items():
        qq = str(qq)
        seen(qq, rec.get("ts"))
        for n in rec.get("names") or []:
            name(qq, n)
    for place, people in (src.get("impressions") or {}).items():
        for qq, rec in (people or {}).items():
            qq = str(qq)
            first_seen.setdefault(qq, now)
            last_seen.setdefault(qq, 0.0)
            name(qq, rec.get("name"))
    for place, win in (src.get("windows") or {}).items():
        for qq, n in (win.get("names") or {}).items():
            name(str(qq), n)

    # ---------------------------------------------------------------- memories, events, notes
    items = []   # (kind, raw id, item, origin)
    for e in src.get("memories") or []:
        if not isinstance(e, dict) or not e.get("id") or e.get("deleted") or e.get("summarized"):
            continue
        items.append(("m", str(e["id"]), e, discretion.origin_of(e)))
    for ev in src.get("events") or []:
        if isinstance(ev, dict) and ev.get("id"):
            items.append(("e", str(ev["id"]), ev, discretion.origin_of(ev)))
    for x in src.get("notes") or []:
        if isinstance(x, dict) and x.get("id"):
            items.append(("n", str(x["id"]), x, discretion.origin_of(x)))
    partner_ok = {}

    def partner_shown(where):   # a private chat's things go with its partner
        p = _window_place(where)
        if not p.startswith("private:"):
            return True
        qq = p.split(":", 1)[1]
        if qq not in partner_ok:
            partner_ok[qq] = bool(keep_person(qq, None))
        return partner_ok[qq]

    kept = []
    for kind, raw, item, o in items:
        if not keep_item(item) or not partner_shown(o["where"]):
            continue
        kept.append((kind, raw, item, o))
        for qq in o["people"]:
            seen(qq, item.get("ts"))
        if kind == "m":
            name(str(item.get("sender_id") or ""), item.get("sender_name"))

    # ---------------------------------------------------------------- windows
    places = {}
    for kind, raw, item, o in kept:
        p = _window_place(o["where"])
        if p:
            places[p] = min(places.get(p, now), _num(item.get("ts")) or now)
    for p, win in (src.get("windows") or {}).items():
        if _window_place(p):
            places.setdefault(p, _num(win.get("first")) or _num(win.get("last")) or now)
    for p in src.get("impressions") or {}:
        if _window_place(p):
            places.setdefault(p, now)
    windows = {}
    counts = {}
    for kind, raw, item, o in kept:
        counts[o["where"]] = counts.get(o["where"], 0) + 1
    order = {"group": 0, "private": 0}
    for p in sorted(places, key=lambda x: (places[x], x)):
        sub = "group" if p.startswith("group:") else "private"
        if sub == "private" and not person_shown(p.split(":", 1)[1]):
            continue
        order[sub] += 1
        pid = ids("w", p)
        windows[p] = pid
        label = ("群%d" if sub == "group" else "私聊%d") % order[sub]
        index[pid] = ("window", p, {"label": label, "sub": sub})
        nodes[pid] = {"id": pid, "kind": "window", "sub": sub, "label": label}
    busiest = max([int((src.get("windows") or {}).get(p, {}).get("lines24", 0) or 0) for p in windows] + [1])
    most = max([counts.get(p, 0) for p in windows] + [1])
    for p, pid in windows.items():
        lines24 = int((src.get("windows") or {}).get(p, {}).get("lines24", 0) or 0)
        nodes[pid]["w"] = round(max(0.15, 0.6 * lines24 / busiest + 0.4 * counts.get(p, 0) / most), 3)

    # ---------------------------------------------------------------- people
    people = {}
    candidates = set(first_seen)   # a name seen in a window alone does not make a star
    for p in windows:
        if p.startswith("private:"):
            candidates.add(p.split(":", 1)[1])
    n_person = 0
    for qq in sorted((q for q in candidates if q and q != "self"), key=lambda q: (first_seen.get(q, now), q)):
        if not person_shown(qq):
            continue
        n_person += 1
        pid = ids("p", qq)
        people[qq] = pid
        label = "人%d" % n_person
        index[pid] = ("person", qq, {"label": label})
        nodes[pid] = {"id": pid, "kind": "person", "label": label}

    # ---------------------------------------------------------------- stars of what she keeps
    raw_to_pid = {}
    for kind, raw, item, o in kept:
        pid = ids(kind, raw)
        raw_to_pid[(kind, raw)] = pid
        where = windows.get(_window_place(o["where"]))
        vis = o["visibility"]
        if kind == "m":
            role = str(item.get("role") or "user")
            cat = "总结" if role == "summary" else "她说的" if role == "assistant" else "私下" if vis == "private" else "听来的"
            w = _clip01(item.get("importance", 0.5))
        elif kind == "e":
            cat = _EMOTION.get(str(item.get("emotion") or "").lower(), "事件")
            w = _clip01(item.get("importance", 0.5))
        else:
            cat = "她自己那一页" if vis == "self" else "私下那一页" if vis == "private" else "群里那一页"
            w = 0.6
        node = {"id": pid, "kind": {"m": "memory", "e": "event", "n": "note"}[kind], "cat": cat,
                "label": cat if kind != "n" else "本子", "where": where, "ts": round(_num(item.get("ts"))),
                "w": max(0.05, w), "vis": vis}
        if kind == "n":
            node["self"] = vis == "self"
        nodes[pid] = node
        index[pid] = ({"m": "memory", "e": "event", "n": "note"}[kind], raw, {"item": item, "origin": o, "cat": cat})
        if where:
            edges.append({"s": pid, "t": where, "kind": "origin"})
        for qq in o["people"]:
            if qq in people:
                edges.append({"s": pid, "t": people[qq], "kind": "about"})
                about[qq] = about.get(qq, 0) + 1
    # associations: two memories recalled together (entry["links"]), each pair once
    pairs = {}
    for kind, raw, item, o in kept:
        if kind != "m":
            continue
        for link in item.get("links") or []:
            other = raw_to_pid.get(("m", str((link or {}).get("id") or "")))
            if not other or other == raw_to_pid[("m", raw)]:
                continue
            a, b = sorted((raw_to_pid[("m", raw)], other))
            w, ts = _num(link.get("weight"), 1.0), _num(link.get("ts"))
            old = pairs.get((a, b))
            if not old or w > old[0]:
                pairs[(a, b)] = (w, ts)
    for (a, b), (w, ts) in sorted(pairs.items()):
        edges.append({"s": a, "t": b, "kind": "link", "w": round(w, 2), "ts": round(ts)})
    # what she thinks of people, per group
    for place, recs in sorted((src.get("impressions") or {}).items()):
        if place not in windows:
            continue
        msgs = {str(qq): int(((rec or {}).get("stats") or {}).get("msgs", 0) or 0) for qq, rec in (recs or {}).items()}
        top = max(list(msgs.values()) + [1])
        for qq in sorted(msgs):
            if qq in people and (keep_impression is None or keep_impression(qq, place)):
                edges.append({"s": people[qq], "t": windows[place], "kind": "impression",
                              "w": round(max(0.1, msgs[qq] / top), 3)})
    most_about = max(list(about.values()) + [1])
    for qq, pid in people.items():
        nodes[pid]["w"] = round(max(0.15, about.get(qq, 0) / most_about), 3)

    # ---------------------------------------------------------------- turns
    mem_pid = {raw: pid for (kind, raw), pid in raw_to_pid.items() if kind == "m"}
    turns = []
    for t in src.get("turns") or []:
        if not isinstance(t, dict):
            continue
        rec = [mem_pid[x] for x in t.get("recalled") or [] if x in mem_pid]
        held = [mem_pid[x] for x in t.get("held") or [] if x in mem_pid]
        if not rec and not held:
            continue
        path = [[mem_pid[a], mem_pid[b]] for a, b in (t.get("path") or []) if a in mem_pid and b in mem_pid]
        row = {"id": "t%d" % (len(turns) + 1), "ts": round(_num(t.get("ts"))),
               "where": windows.get(_window_place(t.get("where"))), "recalled": rec, "held": held, "path": path}
        if isinstance(t.get("body"), dict):
            row["body"] = {k: round(_num(v), 3) for k, v in t["body"].items() if k in BODY_KEYS}
        turns.append(row)

    index["_names"] = names
    index["_people"] = people
    index["_windows"] = windows
    index["_about"] = about
    index["_counts"] = counts
    graph = {"schema": SCHEMA, "sample": False, "now": round(now),
             "body": dict(src.get("body") or {}),
             "nodes": list(nodes.values()), "edges": edges, "turns": turns[-TURNS_MAX:]}
    token = hashlib.sha256(("%s|%s|%s" % (now, len(nodes), len(edges))).encode("utf-8") + os.urandom(8)).hexdigest()[:16]
    return Snapshot(graph, index, token)


# ---------------------------------------------------------------------- opening one star
def _label(snap, pid) -> str:
    entry = snap.index.get(pid)
    return entry[2].get("label", "") if entry and entry[0] in ("window", "person") else ""


def _person_name(snap, qq) -> str:
    ns = snap.index["_names"].get(qq) or []
    return ns[0] if ns else _label(snap, snap.index["_people"].get(qq, ""))


def _where_text(snap, where) -> str:
    where = str(where or "")
    if where == discretion.SELF:
        return "她自己"
    if where.startswith("web:"):
        return "网页"
    pid = snap.index["_windows"].get(_window_place(where))
    return _label(snap, pid) if pid else "好几个地方"


_MAY = {"public": "公开：哪里都能说，别处不带名字", "private": "私下：只在那个私聊里", "self": "她自己的：哪里都能说"}


def detail(snap, pid, impressions=None, reveal_qq=False):
    """What one star holds, or None. A person's QQ number only with reveal_qq (and then
    only that). `impressions`: {place: {qq: rec}} for what she thinks of a person (only
    the ones keep_impression allowed)."""
    entry = snap.index.get(str(pid or ""))
    if not entry or str(pid).startswith("_"):
        return None
    kind, raw, info = entry
    if reveal_qq:
        return {"qq": raw} if kind == "person" else None
    if kind in ("memory", "event", "note"):
        item, o = info["item"], info["origin"]
        who = "、".join(_person_name(snap, q) for q in o["people"] if q in snap.index["_people"])
        lines = [["出处", _where_text(snap, o["where"])], ["能在哪说", _MAY.get(o["visibility"], "私下：只在那个私聊里")]]
        if who:
            lines.append(["跟谁有关", who])
        if kind == "memory":
            text = str(item.get("text") or "")
            lines.append(["记下的时间", _date(item.get("ts"))])
            if int(_num(item.get("recall_count"))):
                lines.append(["想起过", "%d 次" % int(_num(item.get("recall_count")))])
            return {"title": info["cat"] + "的记忆", "text": text[:DETAIL_TEXT_MAX], "lines": lines}
        if kind == "event":
            text = "\n".join(str(item.get(k) or "") for k in ("title", "small_summary", "event") if item.get(k))
            lines.append(["什么时候", _date(item.get("ts"))])
            return {"title": "事件 · " + info["cat"], "text": text[:DETAIL_TEXT_MAX], "lines": lines}
        lines.append(["写于", _date(item.get("ts"))])
        return {"title": "本子 · " + info["cat"], "text": str(item.get("text") or "")[:DETAIL_TEXT_MAX], "lines": lines}
    if kind == "window":
        n = snap.index["_counts"].get(raw, 0)
        if info["sub"] == "private":
            qq = raw.split(":", 1)[1]
            return {"title": "跟%s的私聊" % _person_name(snap, qq),
                    "lines": [["类型", "私聊"], ["从这里来的", "%d 条" % n]]}
        return {"title": info["label"], "lines": [["类型", "群聊"], ["从这里来的", "%d 条" % n]]}
    if kind == "person":
        lines = []
        ns = snap.index["_names"].get(raw) or []
        if len(ns) > 1:
            lines.append(["也叫", "、".join(ns[1:6])])
        for place, recs in sorted((impressions or {}).items()):
            rec = (recs or {}).get(raw)
            if not isinstance(rec, dict) or place not in snap.index["_windows"]:
                continue
            said = "，".join(x for x in [str(rec.get("style") or ""),
                                          ("常聊" + "、".join(str(t) for t in (rec.get("topics") or [])[:4]))
                                          if rec.get("topics") else ""] if x)
            if said:
                lines.append(["她在%s的印象" % _where_text(snap, place), said])
        seen_in = [_label(snap, w) for p, w in sorted(snap.index["_windows"].items())
                   if (p == "private:" + raw) or (raw in ((impressions or {}).get(p) or {}))]
        if seen_in:
            lines.append(["在哪见过", "、".join(seen_in)])
        lines.append(["跟这个人有关的", "%d 条" % snap.index["_about"].get(raw, 0)])
        return {"title": _person_name(snap, raw), "lines": lines, "has_qq": True}
    return None


def search(snap, q, impressions=None) -> list:
    """Ids of the stars whose words (or a person's names) contain q; never the words."""
    q = str(q or "").strip()[:50]
    if not q:
        return []
    out = []
    for pid, entry in snap.index.items():
        if pid.startswith("_"):
            continue
        kind, raw, info = entry
        if kind in ("memory", "event", "note"):
            item = info["item"]
            hay = " ".join(str(item.get(k) or "") for k in ("text", "title", "event", "small_summary", "big_summary"))
        elif kind == "person":
            hay = " ".join(snap.index["_names"].get(raw) or [])
        else:
            continue
        if q in hay:
            out.append(pid)
            if len(out) >= SEARCH_MAX:
                break
    return out


# ---------------------------------------------------------------------- what each reply recalled
class TurnLog:
    """A small JSON file: the last TURNS_MAX turns, each {ts, where, recalled, held, path,
    body}. Only ids (memory ids, the place) and her body's numbers; never words."""

    def __init__(self, path):
        self.path = Path(path)

    def read(self) -> list:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            turns = data.get("turns") if isinstance(data, dict) else None
            return [t for t in turns if isinstance(t, dict)] if isinstance(turns, list) else []
        except Exception:
            return []

    def _write(self, turns) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"turns": turns[-TURNS_MAX:]}, ensure_ascii=False), encoding="utf-8")
        atomic_file.replace(tmp, self.path)

    @staticmethod
    def clean(turn) -> dict:
        def id_list(xs):
            return list(dict.fromkeys(str(x)[:40] for x in (xs or []) if str(x or "").strip()))[:TURN_IDS_MAX]
        rec, held = id_list(turn.get("recalled")), id_list(turn.get("held"))
        known = set(rec) | set(held)
        path = [[str(a)[:40], str(b)[:40]] for a, b in (turn.get("path") or [])
                if str(a)[:40] in known and str(b)[:40] in known and a != b][:2 * TURN_IDS_MAX]
        out = {"ts": round(_num(turn.get("ts"), time.time()), 3), "where": discretion.place_of(turn.get("where")),
               "recalled": rec, "held": [x for x in held if x not in rec], "path": path}
        if isinstance(turn.get("body"), dict):
            out["body"] = {k: round(_num(v), 3) for k, v in turn["body"].items() if k in BODY_KEYS}
        return out

    def add(self, turn) -> dict:
        row = self.clean(turn)
        if not row["recalled"] and not row["held"]:
            return {}
        self._write(self.read() + [row])
        return row

    def prune(self, gone_ids=(), gone_places=(), keep_ids=None) -> int:
        """Drop deleted memories (gone_ids, or every id not in keep_ids) and whole turns in
        gone_places; a turn left with nothing goes. Returns how many turns changed or went."""
        gone, places = {str(x) for x in gone_ids or ()}, {str(x) for x in gone_places or ()}
        keep = None if keep_ids is None else {str(x) for x in keep_ids}

        def ok(x):
            return x not in gone and (keep is None or x in keep)
        turns, out, changed = self.read(), [], 0
        if not turns:
            return 0
        for t in turns:
            if str(t.get("where") or "") in places:
                changed += 1
                continue
            row = dict(t, recalled=[x for x in t.get("recalled") or [] if ok(x)],
                       held=[x for x in t.get("held") or [] if ok(x)],
                       path=[p for p in t.get("path") or [] if len(p) == 2 and ok(p[0]) and ok(p[1])])
            if row != t:
                changed += 1
            if row["recalled"] or row["held"]:
                out.append(row)
        if changed:
            self._write(out)
        return changed
