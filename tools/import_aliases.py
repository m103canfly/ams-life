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


class Gates:
    """The two gates every merged item passes: the run's made-up test data, the registry."""

    def __init__(self, canaries, reg):
        self.reg = reg
        people = canaries.get("people") or {}
        self.people = {str(v) for v in (people.values() if isinstance(people, dict) else people) if str(v)}
        secrets = canaries.get("secrets") or {}
        self.secrets = [str(v) for v in (secrets.values() if isinstance(secrets, dict) else secrets) if str(v)]
        rows = canaries.get("rows") or []
        self.places = {str(r.get("place")) for r in rows if str(r.get("place") or "").startswith("private:")}
        self.places |= {"private:" + p for p in self.people}
        self.names = {str(r.get("name")) for r in rows if len(str(r.get("name") or "")) >= 2}
        self.numbers = re.compile(r"(?<![0-9])(?:%s)(?![0-9])" % "|".join(map(re.escape, sorted(self.people)))) \
            if self.people else None

    def made_up(self, item, people=(), where="", sender="") -> str:
        """Why `item` is the run's made-up test data, or ''."""
        if set(map(str, people)) & self.people:
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


def merge_replay(run, out, reg, canaries) -> dict:
    """Merge the four things of <run>/data into `out` through the gates. Counts only."""
    data = run / "data"
    gates = Gates(canaries, reg)
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
        lines, by_session = [], {}
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
        (out / "self_model.json").write_text(json.dumps({"notebook": notebook}, ensure_ascii=False, indent=1),
                                             encoding="utf-8")
    return {k: dict(sorted(v.items())) for k, v in sorted(counts.items())}


def stage(bundle, out, day="", replay=None) -> dict:
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
    out = _guard.output_dir(out, "the staged data")
    day = day or time.strftime("%Y-%m-%d")
    reg_path = out / forget_registry.FILE_NAME
    shutil.copyfile(reg_src, reg_path)
    lines = (bundle / ALIASES).read_text("utf-8").splitlines() if (bundle / ALIASES).exists() else []
    people = [json.loads(x) for x in lines if x.strip()]
    with forget_registry.ForgetRegistry(reg_path) as reg:
        loaded = impressions.from_bundle(impressions.Store(out / "people"), people, registry=reg, day=day)
        rows = reg.stats()
        merged = merge_replay(run, out, reg, canaries) if run else None
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
        summary["replay"] = {"made_up_test_data": bool(canaries), "merged": merged}
    (out / REPORT).write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--bundle", required=True, help="the import bundle (tools/import_old.py), read only")
    ap.add_argument("--out", required=True, help="new or empty folder (not in AstrBot's data, not in the repo)")
    ap.add_argument("--replay", help="a tools/replay.py run folder (read only): merge what it left her")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(stage(args.bundle, args.out, replay=args.replay), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
