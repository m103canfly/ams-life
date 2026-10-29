"""Stage the old companion's stickers for her library (step 2, part 丙; the owner, 10-29: "全部都存进来").

    python -I tools/import_stickers.py --src <the unpacked folder: 表情清单.csv and stickers/> --out <new empty folder>

The owner brought the old companion's stickers over from the server (a tar.gz, unpacked on
this computer). They are someone else's files: read only, never run, never changed. This puts
them into a new empty folder, in the library's own shape (stickers.Library), to be copied into
the plugin's data folder when installing; it never writes into AstrBot's data, a plugin_data
folder or this repository (tools/_guard.py).

From 表情清单.csv (文件名, 描述, 匹配文字, 情绪, 场景, 使用次数合计, 出现于, 字节, sha256), each row:
- the file is looked for by its name in stickers/ (a bare name only), its sha256 is worked out
  again and must be the row's, and it must be a picture by its first bytes (JPEG, PNG, GIF,
  WebP), at most stickers.MAX_BYTES and stickers.MAX_SIDE a side; otherwise it is left out;
- kept as the old companion's (source "old", from "old"): 描述 -> caption, 情绪 -> emotion,
  场景 -> scene (left empty where the row has none: no model looks at them, the owner's
  decision); saved and last used today, used 0 times, so they go after DAYS unused like hers;
- not taken: 出现于 (the old companion's groups and private chats, real numbers), 使用次数合计,
  匹配文字 (empty).

Into --out: stickers/index.json, stickers/img/<sha256>.<format>, and import_stickers.json with
counts only (no names, no numbers).
"""
import argparse
import csv
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import stickers  # noqa: E402
from tools import _guard  # noqa: E402

CSV_NAME = "表情清单.csv"


def stage(src, out, now=None) -> dict:
    src, now = Path(src), float(time.time() if now is None else now)
    out = _guard.output_dir(out, "the staged stickers")
    lib = stickers.Library(out / "stickers")
    counts = Counter()
    with open(src / CSV_NAME, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        counts["rows"] += 1
        name = str(row.get("文件名") or "").strip()
        if not name or Path(name).name != name or name in (".", ".."):
            counts["left out: not a bare file name"] += 1
            continue
        path = src / "stickers" / name
        if not path.is_file():
            counts["left out: no such file"] += 1
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != str(row.get("sha256") or "").strip().lower():
            counts["left out: sha256 differs"] += 1
            continue
        look = {"caption": row.get("描述") or "", "emotion": row.get("情绪") or "", "scene": row.get("场景") or ""}
        sid, why = lib.add(data, now, source="old", from_where="old", look=look)
        if why:
            counts["left out: " + why] += 1
            continue
        counts["kept"] += 1
        if not look["emotion"].strip():
            counts["kept without an emotion"] += 1
    summary = dict(sorted(counts.items()))
    summary["in the library"] = len(lib.rows)
    (out / "import_stickers.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), "utf-8")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--src", required=True, help="the unpacked folder (表情清单.csv, stickers/), read only")
    ap.add_argument("--out", required=True, help="new or empty folder (not in AstrBot's data, not in the repo)")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(stage(args.src, args.out), ensure_ascii=False))


if __name__ == "__main__":
    main()
