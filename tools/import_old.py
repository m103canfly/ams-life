"""Read the old companion plugin's data and write an import bundle (step 1, part 3).

    python -I tools/import_old.py --old <folder holding plugin_data/snow_companion> --out <new empty folder>
        [--old-forgets keep-out|let-in] [--replay-registries]

Only two things are carried over (the owner's decision, 10-28): what the old companion was
asked to forget, and what it found people were called. Its archive, member cards, group
profiles and notebook are not: what she thinks of each group and each person grows from
the replay of the chat logs and from her own nights.

The old stores are opened read-only. Nothing is written into ams-life's data folder. Bundle:

    forget_registry.sqlite3  who and what must not be kept (forget_registry.py): what the old companion
                             was asked to forget stays forgotten (--old-forgets let-in leaves it empty)
    aliases.jsonl            {"place", "qq", "name", "aliases", "origin"}: what people were called in a
                             group, each name checked again (impressions.check_alias); loaded with
                             impressions.from_bundle; the owner's own names (setting member_aliases)
                             come first in the plugin
    skipped.json             what was left out, counted by reason
    manifest.json            inputs (sha256), options, counts
"""
import argparse
import hashlib
import json
import sqlite3
import sys
import time
from collections import Counter
from contextlib import closing
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import discretion  # noqa: E402
import forget_registry  # noqa: E402
import impressions  # noqa: E402
from tools import _guard  # noqa: E402


def ro(path):
    return sqlite3.connect("file:" + Path(path).resolve().as_posix() + "?mode=ro&immutable=1", uri=True)


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def import_aliases(out, reg, path) -> tuple:
    """group_cognition.sqlite3, table alias(scope, qq, card, aliases): what people were called."""
    kept, skipped = 0, Counter()
    with closing(ro(path)) as db, open(out / "aliases.jsonl", "w", encoding="utf-8") as f:
        for scope, qq, card, raw in db.execute("SELECT scope, qq, card, aliases FROM alias ORDER BY scope, qq"):
            place, qq = forget_registry._legacy_place(scope), str(qq or "")
            if not place.startswith("group:") or not qq:
                skipped["no_place"] += 1
                continue
            if not reg.may_keep_untimed(qq, place):   # the old names carry no time
                skipped["forgotten"] += 1
                continue
            try:
                names = json.loads(raw or "[]")
            except ValueError:
                names = []
            aliases = [a for a in (impressions.check_alias(x) for x in names if isinstance(x, str)) if a]
            if not aliases:
                skipped["no_alias_left"] += 1
                continue
            f.write(json.dumps({"place": place, "qq": qq, "name": str(card or ""), "aliases": aliases,
                                "origin": discretion.make_origin(place, [qq], [])}, ensure_ascii=False) + "\n")
            kept += 1
    return kept, skipped


def build(old, out, replay_registries=False, old_forgets="keep-out") -> dict:
    """Read the old data under `old` (the folder holding plugin_data/), write the bundle into `out`."""
    out = _guard.output_dir(out, "the import bundle")
    snow = Path(old) / "plugin_data" / "snow_companion"
    inputs = {
        "notebook_forget": snow / "notebook-forget.sqlite3",
        "ledger_registry": snow / "ledger" / "forget-registry.sqlite3",
        "cognition": snow / "group_cognition.sqlite3",
    }
    replay = sorted((Path(old) / "extra").rglob("notebook-forget.sqlite3")) if (Path(old) / "extra").exists() else []
    reg = forget_registry.ForgetRegistry(out / forget_registry.FILE_NAME)
    registry_counts = {}
    # the forget registry first: the names are checked against it
    keep_out = old_forgets == "keep-out"
    if keep_out and inputs["notebook_forget"].exists():
        registry_counts["notebook_forget"] = forget_registry.import_notebook_tombstones(reg, inputs["notebook_forget"])
    if keep_out and inputs["ledger_registry"].exists():
        registry_counts["ledger_registry"] = forget_registry.import_ledger_registry(reg, inputs["ledger_registry"])
    for i, path in enumerate(replay, 1):
        if keep_out and replay_registries:
            registry_counts["replay_%d" % i] = forget_registry.import_notebook_tombstones(
                reg, path, note="legacy:replay-test")
    kept, skipped = (0, Counter())
    if inputs["cognition"].exists():
        kept, skipped = import_aliases(out, reg, inputs["cognition"])
    summary = {
        "made": time.strftime("%Y-%m-%d %H:%M:%S"),
        "options": {"old_forgets": old_forgets, "replay_registries": bool(replay_registries),
                    "forget_me": forget_registry.FORGET_ME},
        "inputs": {k: {"sha256": sha256(p), "bytes": p.stat().st_size} for k, p in inputs.items() if p.exists()},
        "replay_registries_found": len(replay),
        "registry": {"imported": registry_counts, "rows": reg.stats()},
        "written": {"aliases.jsonl": kept},
    }
    reg.close()
    (out / "skipped.json").write_text(json.dumps(dict(sorted(skipped.items())), ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    summary["skipped"] = dict(skipped)
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--old", required=True, help="folder that holds plugin_data/snow_companion (read only)")
    ap.add_argument("--out", required=True, help="new or empty folder for the bundle (not in AstrBot's data, not in the repo)")
    ap.add_argument("--old-forgets", choices=("keep-out", "let-in"), default="keep-out",
                    help="keep out what the old companion was asked to forget (default) or import without it")
    ap.add_argument("--replay-registries", action="store_true",
                    help="also count the forget registries left by old replay tests under extra/ (default: no)")
    args = ap.parse_args(argv)
    summary = build(args.old, args.out, args.replay_registries, args.old_forgets)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("registry", "written", "skipped")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
