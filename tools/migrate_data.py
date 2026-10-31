# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Copy the plugin's data folder into ams-life's own data folder, and check the copy.

    python tools/migrate_data.py --src <plugin data folder> --dst <new data folder>
    python tools/migrate_data.py --src <plugin data folder> --dst <new data folder> --verify

Every file and every (also empty) folder is copied as it is (shutil.copy2), except the keys
in api_config.json: they are left empty in the copy, to be filled again in the panel. The
source is only read, never written. A copy is refused while AstrBot is still writing (a
non-empty *-wal file in the source), when the source holds a symbolic link, or when the
source's api_config.json cannot be read as JSON. --verify only compares and writes nothing.
Printed: counts and relative paths only, never a file's content and never a key. Exit: 0 all
equal, 1 something differs, 2 not started.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from tools import _guard  # noqa: E402

API_CONFIG = "api_config.json"
WAL = "-wal"
OK, DIFFERS, NOT_STARTED = 0, 1, 2


class Blocked(Exception):
    """Nothing is copied: the source is still being written, or it holds a link."""


def read_config(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def keys_in(config) -> list:
    """[(kind, key)] for each top-level dict with a non-empty api_key."""
    if not isinstance(config, dict):
        return []
    found = []
    for kind, entry in config.items():
        if isinstance(entry, dict) and entry.get("api_key"):
            found.append((str(kind), str(entry.get("api_key"))))
    return found


def sha256(path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def scan(root) -> dict:
    """Relative posix path -> file, for every file under root (a link is not followed)."""
    root = Path(root)
    if not root.is_dir():
        return {}
    return {path.relative_to(root).as_posix(): path for path in sorted(root.rglob("*")) if path.is_file()}


def walk(root):
    """Every entry under root in order; a symbolic link is listed, not followed."""
    root = Path(root)
    for base, folders, names in os.walk(root, followlinks=False):
        here = Path(base)
        for name in sorted(folders) + sorted(names):
            yield here / name


def quiet_reason(src) -> str:
    """Why ams-life may not copy this folder yet, or '' when it may."""
    wal, links = [], []
    for path in walk(src):
        rel = path.relative_to(src).as_posix()
        if path.is_symlink():
            links.append(rel)
        elif path.name.endswith(WAL) and path.is_file() and path.stat().st_size:
            wal.append(rel)
    if wal:
        return "先停 AstrBot：数据目录里还有没写完的 WAL 文件（%s）" % "、".join(wal)
    if links:
        return "不跟符号链接：%s" % "、".join(links)
    # A config we cannot read keeps its keys in the copy: read it now, copy nothing.
    config = Path(src) / API_CONFIG
    if config.is_file():
        try:
            read_config(config)
        except (OSError, ValueError):
            return "api_config.json 不是有效的 JSON（%s）：清不掉 Key，不复制" % API_CONFIG
    return ""


def copy_folder(src, dst) -> None:
    """Copy every file and every (also empty) folder of src into dst, one at a time."""
    dst.mkdir(parents=True, exist_ok=True)
    for base, folders, names in os.walk(src, followlinks=False):
        here = Path(base)
        rel = here.relative_to(src)
        for name in sorted(folders) + sorted(names):
            path = here / name
            if path.is_symlink():
                raise Blocked("不跟符号链接：%s" % path.relative_to(src).as_posix())
            target = dst / rel / name
            if path.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)


def clear_keys(path):
    """Write api_config.json again with every top-level dict's api_key empty (the same format).
    Returns the kinds cleared, [] when none was set, None when the file cannot be read."""
    try:
        config = read_config(path)
    except (OSError, ValueError):
        return None
    kinds = [kind for kind, _key in keys_in(config)]
    if not kinds:
        return []
    for kind in kinds:
        config[kind]["api_key"] = ""
    Path(path).write_text(json.dumps(config, ensure_ascii=False, indent=1), encoding="utf-8")
    return kinds


def verify(src, dst) -> dict:
    """Compare the copy with the source. Read only. Returns counts, problems and key finds."""
    src_files, dst_files = scan(src), scan(dst)
    problems = []
    for name in sorted(set(src_files) - set(dst_files)):
        problems.append((name, "少了"))
    for name in sorted(set(dst_files) - set(src_files)):
        problems.append((name, "多了"))
    for name in sorted(set(src_files) & set(dst_files)):
        if name == API_CONFIG:
            continue
        if src_files[name].stat().st_size != dst_files[name].stat().st_size:
            problems.append((name, "大小不一样"))
        elif sha256(src_files[name]) != sha256(dst_files[name]):
            problems.append((name, "哈希不一样"))
    plain = []
    if API_CONFIG in src_files and API_CONFIG in dst_files:
        try:
            want = read_config(src_files[API_CONFIG])
            got = read_config(dst_files[API_CONFIG])
        except (OSError, ValueError):
            problems.append((API_CONFIG, "读不了"))
        else:
            pairs = keys_in(want)
            plain = [key for _kind, key in pairs]
            for kind, _key in pairs:
                want[kind]["api_key"] = ""
            if want != got:
                problems.append((API_CONFIG, "清掉 Key 以后不一样"))
            if keys_in(got):
                problems.append((API_CONFIG, "还有 Key"))
    found = []
    needles = list(dict.fromkeys(key.encode("utf-8") for key in plain))
    if needles:
        for name in sorted(dst_files):
            raw = dst_files[name].read_bytes()
            if any(needle in raw for needle in needles):
                found.append(name)
    return {"files": len(src_files), "bytes": sum(path.stat().st_size for path in src_files.values()),
            "problems": problems, "found": found}


def print_counts(files, total) -> None:
    print("文件数：%d，总字节数：%d" % (files, total))


def print_problems(report) -> None:
    for name, why in report["problems"]:
        print("对不上：%s（%s）" % (name, why))
    for name in report["found"]:
        print("含 Key 明文：%s" % name)
    if not report["problems"] and not report["found"]:
        print("都对上了。")


def _utf8() -> None:
    """Chinese names print on a Windows console too; a redirected stream is already text."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def main(argv=None) -> int:
    _utf8()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--src", required=True, help="the plugin's data folder (read only)")
    parser.add_argument("--dst", required=True,
                        help="the new data folder (new or empty; not in AstrBot's data, not in the repo)")
    parser.add_argument("--verify", action="store_true", help="only compare --src and --dst; write nothing")
    args = parser.parse_args(argv)
    src = Path(args.src).resolve()
    if not src.is_dir():
        print("源目录不存在：%s" % src, file=sys.stderr)
        return NOT_STARTED
    if args.verify:
        report = verify(src, Path(args.dst).resolve())
        print_counts(report["files"], report["bytes"])
        print_problems(report)
        return OK if not report["problems"] and not report["found"] else DIFFERS
    try:
        # Check first and make nothing, so a busy source leaves no folder behind.
        _guard.output_dir(args.dst, "data", make=False)
        why = quiet_reason(src)
        if why:
            print(why, file=sys.stderr)
            return NOT_STARTED
        out = _guard.output_dir(args.dst, "data")
        copy_folder(src, out)
    except _guard.Refused as exc:
        print(exc, file=sys.stderr)
        return NOT_STARTED
    except Blocked as exc:
        print(exc, file=sys.stderr)
        return NOT_STARTED
    config_path = out / API_CONFIG
    if config_path.is_file():
        cleared = clear_keys(config_path)
        if cleared is None:
            key_line = "api_config.json 读不了，没有清 Key。"
        elif cleared:
            key_line = "清了 Key 的类别：" + "、".join(cleared)
        else:
            key_line = "没有非空的 Key。"
    else:
        key_line = "没有 Key 文件"
    report = verify(src, out)
    print_counts(report["files"], report["bytes"])
    print(key_line)
    print_problems(report)
    return OK if not report["problems"] and not report["found"] else DIFFERS


if __name__ == "__main__":
    raise SystemExit(main())
