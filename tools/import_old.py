"""Read the old companion plugin's data and write an import bundle (step 1, part 3).

    python -I tools/import_old.py --old <folder holding plugin_data/snow_companion> --out <new empty folder>
        [--skip-archive-place group:<id> ...] [--old-forgets keep-out|let-in] [--replay-registries]

The old stores are opened read-only. Nothing is written into ams-life's data folder:
the bundle is a neutral set of JSON-lines files, every record with its origin, which the
plugin's own loader turns into memories, events and impressions later. Bundle:

    forget_registry.sqlite3  who and what must not be kept (forget_registry.py): what the old companion
                             was asked to forget stays forgotten (the owner's decision; --old-forgets
                             let-in leaves the registry empty and keeps nothing out)
    events.jsonl             what happened in a group each day / week     (old archive: day_line, day_headline, week)
    memories.jsonl           running jokes, notebook facts, one-to-one memories
    groups.jsonl             what each group is like                       (old group profile)
    people.jsonl             group members: name, how people call them, a one-line style, numbers
    skipped.json             what was left out, counted by reason
    manifest.json            inputs (sha256), options, counts

What is left out on purpose (decided in the step-1 investigation):
- the old archive's member updates, open threads and her own sayings: they hold people's
  words verbatim, and words verbatim only ever live 24 hours in her phone;
- the old notebook's "herself" layer and the old diary/style notes: her heart is written by her;
- anything expired, superseded, quarantined, a candidate, forgotten or merged;
- anything that crosses a red line (redline.py), comes from a forgotten person or message,
  or whose place cannot be worked out;
- the archive of every place given with --skip-archive-place (the test group). Its group
  profile and member cards are still imported.

Record shape (events, memories):

    {"id": "old:<store>:<id>", "kind": "...", "text": "...", "time": <unix>, "date": "YYYY-MM-DD",
     "names": ["..."], "origin": {"where", "people", "source_ids", "visibility"}}
"""
import argparse
import hashlib
import json
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import discretion  # noqa: E402
import forget_registry  # noqa: E402
import redline  # noqa: E402
from tools import _guard  # noqa: E402

ARCHIVE_BOOKS = {"day_line": "events", "day_headline": "events", "week": "events", "lore": "memories"}
NOTEBOOK_LAYERS = ("fact", "master", "topic", "lesson")
PERSON_TOKEN = "⟦person:"


def ro(path):
    return sqlite3.connect("file:" + Path(path).resolve().as_posix() + "?mode=ro&immutable=1", uri=True)


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def loads(text, default):
    try:
        v = json.loads(text) if text else default
        return v if isinstance(v, type(default)) else default
    except (TypeError, ValueError):
        return default


def day_of(ts) -> str:
    return time.strftime("%Y-%m-%d", time.localtime(float(ts or 0)))


class Bundle:
    def __init__(self, out, registry):
        self.out, self.reg = out, registry
        self.files = {}
        self.skipped = Counter()
        self.kept = Counter()

    def write(self, name, record):
        f = self.files.get(name)
        if f is None:
            f = self.files[name] = open(self.out / name, "w", encoding="utf-8")
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        self.kept[name] += 1

    def skip(self, what, reason):
        self.skipped[what + ":" + reason] += 1

    def close(self):
        for f in self.files.values():
            f.close()

    def blocked(self, people, place, source_ids, at) -> bool:
        return not self.reg.may_keep_all(people, place, at, source_ids)


# ----------------------------------------------------------------------
# Old archive (ledger state.sqlite3)
# ----------------------------------------------------------------------
def import_archive(b, path, skip_places):
    db = ro(path)
    names = {}
    for scope, qq, name in db.execute("SELECT scope, qq, name FROM actors"):
        names[(discretion.place_of(scope), str(qq))] = str(name or "")
    sources = {}
    for scope, sid, qq, received, revoked in db.execute("SELECT scope, id, qq, received, revoked FROM sources"):
        sources[(str(scope), str(sid))] = (str(qq or ""), float(received or 0), bool(revoked))
    links = {}
    for entry_id, scope, sid in db.execute("SELECT entry_id, scope, source_id FROM entry_sources"):
        links.setdefault(entry_id, []).append((str(scope), str(sid)))
    for entry_id, book, group_scope, origins, visibility, payload, event_at, created, state in db.execute(
            "SELECT id, book, group_scope, origins, visibility, payload, event_at, created, state FROM entries"):
        if book not in ARCHIVE_BOOKS:
            b.skip("archive." + str(book), "not_imported")
            continue
        if state != "active":
            b.skip("archive." + book, "state_" + str(state))
            continue
        scopes = set(loads(origins, [])) | ({group_scope} if group_scope else set())
        places = {discretion.place_of(s) for s in scopes}
        if visibility != "scoped" or len(places) != 1 or not next(iter(places)).startswith("group:"):
            b.skip("archive." + book, "no_single_group")
            continue
        place = places.pop()
        if place in skip_places:
            b.skip("archive." + book, "skipped_place")
            continue
        body = loads(payload, {})
        text = str(body.get("text") or "") if book != "lore" else \
            "%s：%s" % (str(body.get("term") or "").strip(), str(body.get("meaning") or "").strip())
        text, people, said = _names(text, place, names)
        if not text.strip("：").strip():
            b.skip("archive." + book, "empty")
            continue
        ids, bad = [], False
        for scope, sid in links.get(entry_id, []):
            qq, received, revoked = sources.get((scope, sid), ("", 0.0, False))
            if revoked or b.blocked([qq] if qq else [], place, [sid], received):
                bad = True
                break
            ids.append(sid)
            if qq:
                people.append(qq)
        if bad:
            b.skip("archive." + book, "forgotten_or_revoked")
            continue
        if redline.hit(text):
            b.skip("archive." + book, "redline")
            continue
        when = float(event_at or created or 0)
        b.write(ARCHIVE_BOOKS[book] + ".jsonl", {
            "id": "old:archive:%s" % entry_id, "kind": book, "text": text, "time": when, "date": day_of(when),
            "names": said, "origin": discretion.make_origin(place, people, ids)})
    db.close()


def _names(text, place, names):
    """⟦person:<qq>⟧ -> that person's name in that group; returns (text, people, names used)."""
    people, said = [], []
    out, rest = [], str(text or "")
    while PERSON_TOKEN in rest:
        before, _, after = rest.partition(PERSON_TOKEN)
        qq, close, rest = after.partition("⟧")
        if not close:
            rest = after
            break
        name = names.get((place, qq)) or "有人"
        out.extend([before, name])
        people.append(qq)
        if name != "有人":
            said.append(name)
    out.append(rest)
    return "".join(out), people, said


# ----------------------------------------------------------------------
# Old notebook (notebook.sqlite3)
# ----------------------------------------------------------------------
def import_notebook(b, path):
    db = ro(path)
    for row in db.execute("SELECT id, layer, scope, content, state, origin, origin_qq, about_qq, source_ids, created "
                          "FROM entries"):
        entry_id, layer, scope, content, state, origin, origin_qq, about_qq, source_ids, created = row
        what = "notebook." + str(layer)
        if layer == "rule":
            # the owner's rules: none is active in the old data; an active one would go to owner_rules.json
            b.skip(what, "rule_not_imported" if state == "active" else "state_" + str(state))
            continue
        if layer not in NOTEBOOK_LAYERS:
            b.skip(what, "not_imported")
            continue
        if state != "active":
            b.skip(what, "state_" + str(state))
            continue
        place = forget_registry._legacy_place(scope)
        if place == forget_registry.EVERYWHERE or not place.startswith(("group:", "private:")):
            b.skip(what, "no_place")
            continue
        people = [str(q) for q in (origin_qq, about_qq) if str(q or "").strip()]
        ids = [str(s) for s in loads(source_ids, []) if str(s or "").strip()]
        if b.blocked(people, place, ids, float(created or 0)):
            b.skip(what, "forgotten")
            continue
        if redline.hit(content):
            b.skip(what, "redline")
            continue
        b.write("memories.jsonl", {
            "id": "old:notebook:%s" % entry_id, "kind": "notebook_" + layer, "text": str(content or ""),
            "time": float(created or 0), "date": day_of(created), "names": [],
            "origin": discretion.make_origin(place, people, ids)})
    db.close()


# ----------------------------------------------------------------------
# One-to-one memories (social.sqlite3, experience.sqlite3)
# ----------------------------------------------------------------------
def import_items(b, path, store):
    db = ro(path)
    cols = {r[1] for r in db.execute("PRAGMA table_info(items)")}
    evidence = {}
    for item_id, sid in db.execute("SELECT item_id, source_id FROM evidence"):
        evidence.setdefault(item_id, []).append(str(sid))
    cur = db.execute("SELECT * FROM items")
    keys = [d[0] for d in cur.description]
    for row in cur.fetchall():
        item = dict(zip(keys, row))
        what = store + "." + str(item.get("kind") or "item")
        if item.get("revoked") or ("active" in cols and not item.get("active")) or \
                str(item.get("state") or "active") not in ("active", ""):
            b.skip(what, "inactive")
            continue
        place = forget_registry._legacy_place(item.get("scope"))
        if not place.startswith(("group:", "private:")):
            b.skip(what, "no_place")
            continue
        people = [str(item.get("qq"))] if item.get("qq") else []
        ids = evidence.get(item.get("id"), [])
        if b.blocked(people, place, ids, float(item.get("created") or 0)):
            b.skip(what, "forgotten")
            continue
        if redline.hit(item.get("text")):
            b.skip(what, "redline")
            continue
        b.write("memories.jsonl", {
            "id": "old:%s:%s" % (store, item.get("id")), "kind": store, "text": str(item.get("text") or ""),
            "time": float(item.get("created") or 0), "date": day_of(item.get("created")), "names": [],
            "origin": discretion.make_origin(place, people, ids)})
    db.close()


# ----------------------------------------------------------------------
# Group profiles, member cards, how people are called (group_cognition.sqlite3)
# ----------------------------------------------------------------------
def _clean_stats(stats):
    """Numbers stay; a pet phrase that crosses a red line goes."""
    out = dict(stats) if isinstance(stats, dict) else {}
    for key, value in list(out.items()):
        if isinstance(value, list):
            out[key] = [v for v in value if not (isinstance(v, str) and redline.hit(v))]
        elif isinstance(value, str) and redline.hit(value):
            out[key] = ""
    return out


def import_cognition(b, path):
    db = ro(path)
    now = time.time()
    for scope, content, stats, src_from, src_to, state in db.execute(
            "SELECT scope, content, stats, src_from, src_to, state FROM profile"):
        place = forget_registry._legacy_place(scope)
        if state != "active" or not place.startswith("group:"):
            b.skip("cognition.profile", "inactive_or_no_place")
            continue
        text = str(content or "")
        if redline.hit(text):
            b.skip("cognition.profile_text", "redline")
            text = ""
        b.write("groups.jsonl", {"place": place, "text": text, "stats": _clean_stats(loads(stats, {})),
                                 "from": src_from, "to": src_to,
                                 "origin": discretion.make_origin(place, [], [])})
    people = {}
    for scope, qq, name, content, stats, src_from, src_to, state in db.execute(
            "SELECT scope, qq, name, content, stats, src_from, src_to, state FROM card"):
        place = forget_registry._legacy_place(scope)
        if state != "active" or not place.startswith("group:"):
            b.skip("cognition.card", "inactive_or_no_place")
            continue
        if b.blocked([str(qq)], place, [], now):
            b.skip("cognition.card", "forgotten")
            continue
        style = str(content or "")
        if redline.hit(style):
            b.skip("cognition.card_style", "redline")
            style = ""
        people[(place, str(qq))] = {"place": place, "qq": str(qq), "name": str(name or ""), "aliases": [],
                                    "style": style, "stats": _clean_stats(loads(stats, {})),
                                    "from": src_from, "to": src_to}
    for scope, qq, card, aliases in db.execute("SELECT scope, qq, card, aliases FROM alias"):
        place = forget_registry._legacy_place(scope)
        if not place.startswith("group:") or b.blocked([str(qq)], place, [], now):
            b.skip("cognition.alias", "forgotten_or_no_place")
            continue
        rec = people.setdefault((place, str(qq)), {"place": place, "qq": str(qq), "name": str(card or ""),
                                                   "aliases": [], "style": "", "stats": {}, "from": None, "to": None})
        rec["aliases"].extend(a for a in loads(aliases, []) if isinstance(a, str) and a and not redline.hit(a))
    for key in sorted(people):
        rec = people[key]
        rec["origin"] = discretion.make_origin(rec["place"], [rec["qq"]], [])
        b.write("people.jsonl", rec)
    db.close()


# ----------------------------------------------------------------------
def build(old, out, skip_places=(), replay_registries=False, ledger="snapshot", old_forgets="keep-out") -> dict:
    """Read the old data under `old` (the folder holding plugin_data/), write the bundle into `out`."""
    out = _guard.output_dir(out, "the import bundle")
    snow = Path(old) / "plugin_data" / "snow_companion"
    inputs = {
        "notebook_forget": snow / "notebook-forget.sqlite3",
        "ledger_registry": snow / "ledger" / "forget-registry.sqlite3",
        "archive": snow / "ledger" / ledger / "state.sqlite3",
        "notebook": snow / "notebook.sqlite3",
        "social": snow / "social.sqlite3",
        "experience": snow / "experience.sqlite3",
        "cognition": snow / "group_cognition.sqlite3",
    }
    replay = sorted((Path(old) / "extra").rglob("notebook-forget.sqlite3")) if (Path(old) / "extra").exists() else []
    reg = forget_registry.ForgetRegistry(out / forget_registry.FILE_NAME)
    registry_counts = {}
    # the forget registry first: everything after is checked against it
    keep_out = old_forgets == "keep-out"
    if keep_out and inputs["notebook_forget"].exists():
        registry_counts["notebook_forget"] = forget_registry.import_notebook_tombstones(reg, inputs["notebook_forget"])
    if keep_out and inputs["ledger_registry"].exists():
        registry_counts["ledger_registry"] = forget_registry.import_ledger_registry(reg, inputs["ledger_registry"])
    for i, path in enumerate(replay, 1):
        if keep_out and replay_registries:
            registry_counts["replay_%d" % i] = forget_registry.import_notebook_tombstones(
                reg, path, note="legacy:replay-test")
    b = Bundle(out, reg)
    try:
        if inputs["archive"].exists():
            import_archive(b, inputs["archive"], {forget_registry.norm_place(p) for p in skip_places})
        if inputs["notebook"].exists():
            import_notebook(b, inputs["notebook"])
        for store in ("social", "experience"):
            if inputs[store].exists():
                import_items(b, inputs[store], store)
        if inputs["cognition"].exists():
            import_cognition(b, inputs["cognition"])
    finally:
        b.close()
    summary = {
        "made": time.strftime("%Y-%m-%d %H:%M:%S"),
        "options": {"skip_archive_places": len(skip_places), "old_forgets": old_forgets,
                    "replay_registries": bool(replay_registries),
                    "ledger": ledger, "forget_me": forget_registry.FORGET_ME},
        "inputs": {k: {"sha256": sha256(p), "bytes": p.stat().st_size} for k, p in inputs.items() if p.exists()},
        "replay_registries_found": len(replay),
        "registry": {"imported": registry_counts, "rows": reg.stats()},
        "written": dict(b.kept),
    }
    reg.close()
    (out / "skipped.json").write_text(json.dumps(dict(sorted(b.skipped.items())), ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    summary["skipped"] = dict(b.skipped)
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--old", required=True, help="folder that holds plugin_data/snow_companion (read only)")
    ap.add_argument("--out", required=True, help="new or empty folder for the bundle (not in AstrBot's data, not in the repo)")
    ap.add_argument("--skip-archive-place", action="append", default=[], metavar="PLACE",
                    help="do not import the old archive of this place, e.g. group:<id> (repeatable)")
    ap.add_argument("--old-forgets", choices=("keep-out", "let-in"), default="keep-out",
                    help="keep out what the old companion was asked to forget (default) or import without it")
    ap.add_argument("--replay-registries", action="store_true",
                    help="also count the forget registries left by old replay tests under extra/ (default: no)")
    ap.add_argument("--ledger", choices=("snapshot", "work"), default="snapshot")
    args = ap.parse_args(argv)
    summary = build(args.old, args.out, args.skip_archive_place, args.replay_registries, args.ledger,
                    args.old_forgets)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("registry", "written", "skipped")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
