"""Stage what an import bundle carries into a fresh data folder: the forget registry and what
people were called (step 1, installing on this computer).

    python -I tools/import_aliases.py --bundle <folder written by tools/import_old.py> --out <new empty folder>

The plugin does not read a bundle's aliases.jsonl by itself (only tools/replay.py loads it,
with impressions.from_bundle). This does the same, outside AstrBot, into a new empty folder;
the folder is then copied into the plugin's new, empty data folder before the new code
starts for the first time (the owner's decision, 10-29). It never writes into AstrBot's
data, a plugin_data folder or this repository (tools/_guard.py), and only reads the bundle.

Into --out:
    forget_registry.sqlite3  the bundle's registry, copied as it is (byte for byte)
    people/                  what people were called, through the plugin's own
                             impressions.from_bundle with that registry: whoever it rules out
                             is left out, and every name is checked again (check_alias)
    import_aliases.json      counts only: what from_bundle did, the registry's rows by kind,
                             its people and name hashes. No names, no numbers.
"""
import argparse
import json
import shutil
import sqlite3
import sys
import time
from contextlib import closing
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import forget_registry  # noqa: E402
import impressions  # noqa: E402
from tools import _guard  # noqa: E402

ALIASES = "aliases.jsonl"
REPORT = "import_aliases.json"


def stage(bundle, out, day="") -> dict:
    """Copy the registry, load the aliases with it into out/people/, write the counts."""
    bundle = Path(bundle).resolve()
    reg_src = bundle / forget_registry.FILE_NAME
    if not reg_src.is_file():
        raise SystemExit("no %s in %s: not an import bundle" % (forget_registry.FILE_NAME, bundle))
    for extra in ("-wal", "-journal"):
        if Path(str(reg_src) + extra).exists():   # left open by something: not copied half-written
            raise SystemExit("%s%s is there: the bundle's registry is still open somewhere" % (reg_src.name, extra))
    out = _guard.output_dir(out, "the staged data")
    day = day or time.strftime("%Y-%m-%d")
    reg_path = out / forget_registry.FILE_NAME
    shutil.copyfile(reg_src, reg_path)
    lines = (bundle / ALIASES).read_text("utf-8").splitlines() if (bundle / ALIASES).exists() else []
    people = [json.loads(x) for x in lines if x.strip()]
    with forget_registry.ForgetRegistry(reg_path) as reg:
        loaded = impressions.from_bundle(impressions.Store(out / "people"), people, registry=reg, day=day)
        rows = reg.stats()
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
    (out / REPORT).write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--bundle", required=True, help="the import bundle (tools/import_old.py), read only")
    ap.add_argument("--out", required=True, help="new or empty folder (not in AstrBot's data, not in the repo)")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(stage(args.bundle, args.out), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
