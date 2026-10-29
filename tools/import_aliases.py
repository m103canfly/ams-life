"""Stage what an import bundle carries into a fresh data folder: the forget registry and what
people were called; with --replay, also what a replay run of the old chat log left her
(step 1, installing on this computer).

    python -I tools/import_aliases.py --bundle <folder written by tools/import_old.py> --out <new empty folder>
        [--replay <a tools/replay.py run folder>]

The plugin does not read a bundle's aliases.jsonl by itself (only tools/replay.py loads it,
with impressions.from_bundle). This does the same, outside AstrBot, into a new empty folder;
the folder is then copied into the plugin's new, empty data folder before the new code
starts for the first time (the owner's decision, 10-29). It never writes into AstrBot's
data, a plugin_data folder or this repository (tools/_guard.py), and only reads the bundle
and the run.

Into --out:
    forget_registry.sqlite3  the bundle's registry, copied as it is (byte for byte)
    people/                  what people were called, through the plugin's own
                             impressions.from_bundle with that registry: whoever it rules out
                             is left out, and every name is checked again (check_alias)
    import_aliases.json      counts only: what from_bundle did, the registry's rows by kind,
                             its people and name hashes; with --replay, what was merged and
                             what was left out, by kind and reason. No names, no numbers.

--replay <run> (the owner's decision, 10-29: "并") merges four things from <run>/data/:
    memories      memory/library.json entries, with their vectors (vector_store) -- only those
    events        archives/events.jsonl; each place's copy (archives/sessions/) written again
                  from the events merged, not copied
    impressions   people/<group> files and names.json, on top of the names loaded above (the
                  same person: the run's impression, the names of both, at most MAX_ALIASES)
    notebook      self_model.json's notebook only, written as {"notebook": [...]}; the plugin
                  fills in the rest when it starts
Not taken: her phone, brain_turns.json, states/, users/, api_config.json, the rest of
self_model.json, the run's own copy of the registry, the library's rooms.
Each item passes two gates or is left out whole: nothing of the run's made-up test data
(canaries.json: its people, its private chat, its secrets, its names, anywhere in the item),
and the registry copied above allows it (may_keep_all by its origin; impressions and names by
person, may_keep_untimed). Words are merged as the run wrote them: no numbers put back, no
「」 added; deleted people's names are the plugin's own sweep at its first start.
"""
import argparse
import json
import re
import shutil
import sqlite3
import sys
import tempfile
import time
from collections import Counter
from contextlib import closing
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import discretion  # noqa: E402
import forget_registry  # noqa: E402
import impressions  # noqa: E402
import vector_store  # noqa: E402
from tools import _guard  # noqa: E402

ALIASES = "aliases.jsonl"
REPORT = "import_aliases.json"
CANARIES = "canaries.json"


def session_dir(session) -> str:
    """The folder of a place's copy of its events, as the plugin names it
    (mixin_events._event_session_file; a test keeps the two the same)."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in str(session or "default"))[:80]


def _whole_numbers(numbers):
    return re.compile(r"(?<![0-9])(?:%s)(?![0-9])" % "|".join(map(re.escape, sorted(numbers)))) if numbers else None


class Gates:
    """The two gates every merged item passes: the run's made-up test data (and the people on
    the --exclude-people list, left out the same way), the registry."""

    def __init__(self, canaries, reg, excluded=()):
        self.reg = reg
        people = canaries.get("people") or {}
        self.people = {str(v) for v in (people.values() if isinstance(people, dict) else people) if str(v)}
        secrets = canaries.get("secrets") or {}
        self.secrets = [str(v) for v in (secrets.values() if isinstance(secrets, dict) else secrets) if str(v)]
        rows = canaries.get("rows") or []
        self.places = {str(r.get("place")) for r in rows if str(r.get("place") or "").startswith("private:")}
        self.places |= {"private:" + p for p in self.people}
        self.names = {str(r.get("name")) for r in rows if len(str(r.get("name") or "")) >= 2}
        self.numbers = _whole_numbers(self.people)
        self.excluded = {str(x) for x in excluded} - self.people
        self.excluded_numbers = _whole_numbers(self.excluded)

    def made_up(self, item, people=(), where="", sender="") -> str:
        """Why `item` is the run's made-up test data, or someone on the list's; or ''."""
        people = set(map(str, people))
        if people & self.people:
            return "made_up_person"
        if str(where) in self.places:
            return "made_up_chat"
        if str(sender) in self.people:
            return "made_up_sender"
        text = json.dumps(item, ensure_ascii=False)
        if any(s in text for s in self.secrets):
            return "made_up_secret"
        if self.numbers and self.numbers.search(text):
            return "made_up_number"
        if any(n in text for n in self.names):
            return "made_up_name"
        if people & self.excluded or str(sender) in self.excluded or str(where) in {"private:" + p for p in self.excluded} \
                or (self.excluded_numbers and self.excluded_numbers.search(text)):
            return "excluded_person"
        return ""

    def why_not(self, item) -> str:
        """A memory, an event or a note: '' when it may be merged."""
        o = discretion.origin_of(item)
        why = self.made_up(item, o["people"], o["where"], item.get("sender_id") or "")
        if why:
            return why
        if not self.reg.may_keep_all(o["people"], o["where"], item.get("ts"), o["source_ids"]):
            return "forgotten"
        return ""

    def why_not_person(self, qq, place, item) -> str:
        """An impression of `qq` in `place`, or his names (place '')."""
        why = self.made_up(item, [qq], place)
        if why:
            return why
        return "" if self.reg.may_keep_untimed(qq, place) else "forgotten"


def _read_canaries(run) -> dict:
    path = run / CANARIES
    if not path.is_file():
        raise SystemExit("no %s in %s: what is made up there cannot be told apart, nothing merged" % (CANARIES, run))
    try:
        canaries = json.loads(path.read_text("utf-8"))
        if not isinstance(canaries, dict):
            raise ValueError("not an object")
        if canaries.get("enabled") and not (isinstance(canaries.get("people"), dict) and canaries.get("secrets")):
            raise ValueError("enabled, but no people or secrets")
    except ValueError as exc:
        raise SystemExit("%s in %s cannot be read (%s): nothing merged" % (CANARIES, run, exc))
    return canaries if canaries.get("enabled") else {}


def _linked(entry, kept_ids) -> dict:
    """A memory's links and associations to memories merged too, none to one left out."""
    out = dict(entry)
    if isinstance(out.get("links"), list):
        out["links"] = [x for x in out["links"] if not isinstance(x, dict) or str(x.get("id") or "") in kept_ids]
    if isinstance(out.get("assoc"), dict):
        out["assoc"] = {k: v for k, v in out["assoc"].items() if str(k) in kept_ids}
    return out


# Relationship records (users/<qq>.json), as the plugin reads and cleans them when someone is
# deleted (mixin_discretion._record_mentions, _forget_relationship_text; a test keeps the two the same).
REL_TEXT_LISTS = ("we_memory", "annotations", "milestones")
REL_TEXT_MAPS = ("transactive_map", "destination_map", "social_world")
EVERYDAY_WORDS = {"哈哈", "哈哈哈", "嘿嘿", "嗯嗯", "好的", "可以", "你好", "什么", "这个", "那个", "大家",
                  "真的", "没有", "就是", "然后", "知道", "有人", "某人"}


def user_file(qq) -> str:
    """users/ file name of `qq`, as the plugin names it (mixin_people._user_path)."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in str(qq or "unknown"))[:60] + ".json"


def record_mentions(rec, person, names) -> bool:
    """Does a relationship record draw from `person`? (mixin_discretion._record_mentions)"""
    rel = rec.get("relationship") if isinstance(rec.get("relationship"), dict) else {}
    texts, name_fields, ids = [], [], []

    def take(x):
        if isinstance(x, dict):
            texts.extend(str(x.get(k) or "") for k in ("text", "key", "title", "latest_text"))
            texts.extend(str(ev.get("text") or "") for ev in x.get("evidence") or [] if isinstance(ev, dict))
            name_fields.append(str(x.get("sender_name") or x.get("name") or ""))
            ids.append(str(x.get("sender_id") or x.get("qq") or ""))
        elif isinstance(x, str):
            texts.append(x)
    for key in REL_TEXT_LISTS + REL_TEXT_MAPS:
        value = rel.get(key)
        if isinstance(value, dict):
            for k, v in value.items():
                texts.append(str(k))
                take(v)
        elif isinstance(value, list):
            for v in value:
                take(v)
    if person in ids or person in name_fields:
        return True
    number = re.compile(r"(?<![0-9])%s(?![0-9])" % re.escape(person))
    if any(number.search(t) for t in texts):
        return True
    names = [n for n in names if len(n) >= 2 and not n.isdigit()]
    if any(n in name_fields for n in names):
        return True
    return any(n in t for n in names if n not in EVERYDAY_WORDS for t in texts)


def _clean_record(rec, says_bad) -> None:
    """As the plugin does to someone else's record when a person is deleted
    (_forget_relationship_text): sub-records that draw from them, or do not say where they
    came from, go; the three word maps are emptied (rebuilt later); the numbers stay."""
    rel = rec.get("relationship")
    if not isinstance(rel, dict):
        return
    for key in REL_TEXT_LISTS:
        if isinstance(rel.get(key), list):
            rel[key] = [x for x in rel[key] if isinstance(x, dict)
                        and (list(x.get("source_ids") or []) + list(x.get("evidence_refs") or []))
                        and not says_bad({"relationship": {key: [x]}})]
    for key in REL_TEXT_MAPS:
        if rel.get(key):
            rel[key] = [] if isinstance(rel.get(key), list) else {}


def merge_replay(run, out, reg, canaries, excluded=()) -> dict:
    """Merge the four things of <run>/data (and users/) into `out` through the gates. Counts only."""
    data = run / "data"
    gates = Gates(canaries, reg, excluded)
    counts = {}

    def tally(kind, why):
        counts.setdefault(kind, Counter())[why or "merged"] += 1

    # memories, and only their vectors
    lib_path = data / "memory" / "library.json"
    if lib_path.is_file():
        lib = json.loads(lib_path.read_text("utf-8"))
        kept = []
        for e in lib.get("entries") or []:
            if not isinstance(e, dict):
                continue
            why = gates.why_not(e)
            tally("memory", why)
            if not why:
                kept.append(e)
        ids = {str(e.get("id") or "") for e in kept}
        kept = [_linked(e, ids) for e in kept]
        vectors = data / "memory" / vector_store.FILE_NAME
        if vectors.is_file():
            # the run's store is read from a copy: opening one writes to it
            with tempfile.TemporaryDirectory() as tmp:
                shutil.copyfile(vectors, Path(tmp) / vector_store.FILE_NAME)
                with vector_store.VectorStore(Path(tmp) / vector_store.FILE_NAME) as source:
                    source.attach(kept)
        (out / "memory").mkdir(parents=True, exist_ok=True)
        with vector_store.VectorStore(out / "memory" / vector_store.FILE_NAME) as store:
            entries = store.detach(kept)
            counts["memory_vectors"] = Counter(stored=len(store))
        merged = {"schema_version": lib.get("schema_version"), "rooms": {}, "entries": entries}
        (out / "memory" / "library.json").write_text(json.dumps(merged, ensure_ascii=False), encoding="utf-8")

    # events, and each place's copy written again from them
    ev_path = data / "archives" / "events.jsonl"
    if ev_path.is_file():
        kept_events = []
        for line in ev_path.read_text("utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                tally("event", "unreadable")
                continue
            why = gates.why_not(rec) if isinstance(rec, dict) else "unreadable"
            tally("event", why)
            if not why:
                kept_events.append((line, rec))
        event_ids = {str(rec.get("id") or "") for _line, rec in kept_events}
        lines, by_session = [], {}
        for line, rec in kept_events:
            linked = {k: [x for x in rec[k] if not isinstance(x, dict) or str(x.get("id") or "") in event_ids]
                      for k in ("links", "chain_links") if isinstance(rec.get(k), list)}
            if any(len(v) != len(rec[k]) for k, v in linked.items()):   # none to an event left out
                line = json.dumps(dict(rec, **linked), ensure_ascii=False)
            lines.append(line)
            by_session.setdefault(session_dir(rec.get("session")), []).append(line)
        (out / "archives").mkdir(parents=True, exist_ok=True)
        (out / "archives" / "events.jsonl").write_text("".join(x + "\n" for x in lines), encoding="utf-8")
        for name, own in by_session.items():
            folder = out / "archives" / "sessions" / name
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "events.jsonl").write_text("".join(x + "\n" for x in own), encoding="utf-8")
        counts["event_copies"] = Counter(places=len(by_session))

    # impressions and names, on top of the names loaded from the bundle
    if (data / "people").is_dir():
        theirs, ours = impressions.Store(data / "people"), impressions.Store(out / "people")
        for place in theirs.places():
            here = ours.load(place)
            for qq, rec in (theirs.load(place).get("people") or {}).items():
                why = gates.why_not_person(qq, place, rec) if isinstance(rec, dict) else "unreadable"
                tally("impression", why)
                if why:
                    continue
                rec = dict(rec)
                had = (here["people"].get(str(qq)) or {}).get("aliases") or []
                rec["aliases"] = list(dict.fromkeys(list(had) + list(rec.get("aliases") or [])))[-impressions.MAX_ALIASES:]
                here["people"][str(qq)] = rec
            if here["people"]:
                ours.save(place, here)
        names_path = data / "people" / impressions.NAMES_FILE
        names = json.loads(names_path.read_text("utf-8")) if names_path.is_file() else {}
        for qq, ns in (names or {}).items():
            why = gates.why_not_person(qq, "", ns)
            tally("names", why)
            if not why:
                ours.keep_names(qq, ns)

    # her notebook: that list only
    sm_path = data / "self_model.json"
    if sm_path.is_file():
        notebook = []
        for x in (json.loads(sm_path.read_text("utf-8")).get("notebook") or []):
            why = gates.why_not(x) if isinstance(x, dict) else "unreadable"
            tally("notebook", why)
            if not why:
                notebook.append(x)
        # "heart": 1, or at its first start the plugin would keep a copy of this file
        # (self_model.before_heart.json) that no later delete reaches
        (out / "self_model.json").write_text(json.dumps({"notebook": notebook, "heart": 1}, ensure_ascii=False,
                                                        indent=1), encoding="utf-8")

    # relationship records: whoever may not be kept, his own file goes; anyone else's that
    # draws from such a person is cleaned as the plugin does when someone is deleted
    if (data / "users").is_dir():
        bad = gates.people | gates.excluded | {q for q in reg.people() if not reg.may_keep_untimed(q, "")}
        known = {}
        for r in canaries.get("rows") or []:
            known.setdefault(str(r.get("user_id") or ""), set()).add(str(r.get("name") or ""))
        names_path = data / "people" / impressions.NAMES_FILE
        for qq, ns in (json.loads(names_path.read_text("utf-8")) if names_path.is_file() else {}).items():
            known.setdefault(str(qq), set()).update(str(n) for n in ns or [])

        def says_bad(rec):
            return bool(gates.made_up(rec)) or any(record_mentions(rec, b, sorted(known.get(b, ()))) for b in bad)
        for path in sorted((data / "users").glob("*.json")):
            try:
                rec = json.loads(path.read_text("utf-8"))
            except ValueError:
                tally("users", "unreadable")
                continue
            who = str(rec.get("sender_id") or path.stem) if isinstance(rec, dict) else ""
            why = gates.why_not_person(who, "", {}) if who else "unreadable"
            if why:
                tally("users", why)
                continue
            (out / "users").mkdir(parents=True, exist_ok=True)
            if not says_bad(rec):
                shutil.copyfile(path, out / "users" / user_file(who))
                tally("users", "")
                continue
            _clean_record(rec, says_bad)
            if says_bad(rec):
                tally("users", "still_draws_from_someone_left_out")
                continue
            (out / "users" / user_file(who)).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            tally("users", "cleaned")
    return {k: dict(sorted(v.items())) for k, v in sorted(counts.items())}


def stage(bundle, out, day="", replay=None, exclude=None) -> dict:
    """Copy the registry, load the aliases with it into out/people/, merge a replay run if
    given, write the counts."""
    bundle = Path(bundle).resolve()
    reg_src = bundle / forget_registry.FILE_NAME
    if not reg_src.is_file():
        raise SystemExit("no %s in %s: not an import bundle" % (forget_registry.FILE_NAME, bundle))
    for extra in ("-wal", "-journal"):
        if Path(str(reg_src) + extra).exists():   # left open by something: not copied half-written
            raise SystemExit("%s%s is there: the bundle's registry is still open somewhere" % (reg_src.name, extra))
    run = canaries = None
    if replay:   # everything about the run is checked before anything is made
        run = Path(replay).resolve()
        if not (run / "data").is_dir():
            raise SystemExit("no data/ in %s: not a replay run" % run)
        canaries = _read_canaries(run)
    excluded = []
    if exclude:
        if not replay:
            raise SystemExit("--exclude-people goes with --replay")
        ex = Path(exclude)
        if not ex.is_file():
            raise SystemExit("no list at %s: nothing merged" % ex)
        excluded = [x.strip() for x in ex.read_text("utf-8-sig").splitlines() if x.strip() and not x.strip().startswith("#")]
        if not all(x.isdigit() for x in excluded):
            raise SystemExit("%s: one number a line: nothing merged" % ex)
    out = _guard.output_dir(out, "the staged data")
    day = day or time.strftime("%Y-%m-%d")
    reg_path = out / forget_registry.FILE_NAME
    shutil.copyfile(reg_src, reg_path)
    lines = (bundle / ALIASES).read_text("utf-8").splitlines() if (bundle / ALIASES).exists() else []
    people = [json.loads(x) for x in lines if x.strip()]
    with forget_registry.ForgetRegistry(reg_path) as reg:
        loaded = impressions.from_bundle(impressions.Store(out / "people"), people, registry=reg, day=day)
        rows = reg.stats()
        merged = merge_replay(run, out, reg, canaries, excluded) if run else None
    with closing(sqlite3.connect("file:" + reg_path.as_posix() + "?mode=ro", uri=True)) as db:
        names = {"people": db.execute("SELECT COUNT(DISTINCT qq) FROM names").fetchone()[0],
                 "name_hashes": db.execute("SELECT COUNT(*) FROM names").fetchone()[0]}
    summary = {
        "made": time.strftime("%Y-%m-%d %H:%M:%S"),
        "day": day,
        "bundle_manifest": (bundle / "manifest.json").is_file(),
        "aliases_lines": len(people),
        "aliases": dict(sorted(loaded.items())),
        "registry": {"rows": rows, "names": names},
    }
    if run:
        summary["replay"] = {"made_up_test_data": bool(canaries), "excluded_people": len(set(excluded)), "merged": merged}
    (out / REPORT).write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--bundle", required=True, help="the import bundle (tools/import_old.py), read only")
    ap.add_argument("--out", required=True, help="new or empty folder (not in AstrBot's data, not in the repo)")
    ap.add_argument("--replay", help="a tools/replay.py run folder (read only): merge what it left her")
    ap.add_argument("--exclude-people", help="with --replay: a list on this computer (not in the repository), one "
                                             "number a line, of people left out like the run's made-up ones")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(stage(args.bundle, args.out, replay=args.replay, exclude=args.exclude_people), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
