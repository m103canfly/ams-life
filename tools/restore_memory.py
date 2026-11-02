# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Put memories that fell out of her library back from copies of it. Dry run by default.

    python tools/restore_memory.py --data <her data folder> --backup <a copy's memory folder> [...]
    python tools/restore_memory.py --data <her data folder> --backup <...> [...] --apply

Until 11-02 the plugin cut a place's memories down to its last 80 (or its last 200
unsummarized ones while compression was on), and the vectors of the cut ones went with
them. The copies of her data folder made before that still hold many of those memories
and their vectors.sqlite3 files.

Only a memory whose id the library does not have now is put back, exactly as the copy
kept it: its id, time, origin, provenance, importance, how it felt. A vector comes from
that copy's own vectors.sqlite3; when the copy has none, or the dimensions do not match
the library's, it is worked out again by the local bge-m3 service (only a loopback
address, through the plugin's own _embed_text). A memory whose vector cannot be had is
not put back and is counted instead.

Every memory goes in through the plugin's _write_library, so the forget registry is
asked first (what was forgotten never comes back) and the red line is held.

Reading is all a run does unless --apply is given. --apply copies her memory folder to
memory-备份-补回前-<time>/ beside it first, and only writes when that copy is complete.
Stop her, and start the vector service, before really writing.

Printed: per copy, how many can be put back, how many the registry keeps out, how many
the red line keeps out, and how many have no vector. Never a memory's words, a number or
a place. Exit: 0 done, 2 not started.
"""
import argparse
import asyncio
import copy
import glob
import json
import os
import shutil
import sqlite3
import sys
import time
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from tools import _guard  # noqa: E402  (only paths; the plugin's modules come after the data folder is set)

OK, REFUSED = 0, 2
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
RED_LINE_WHAT = "memory"
COPY_PREFIX = "memory-备份-补回前-"


class Problem(Exception):
    """Nothing is written: a copy cannot be read, or the copy before writing failed."""


# ---------------------------------------------------------------------------
# The plugin methods this tool needs, over her data folder
# ---------------------------------------------------------------------------
def make_host(redline=False):
    """A small stand-in for the plugin: the memory and discretion methods, nothing else.

    It keeps memory_meta's own rules (through _write_library and _origin_kept) and the
    red line's, and it reads the embedding settings from her api_config.json. `redline`
    is the redline_filter switch as her config has it.
    """
    import common
    import forget_registry
    import mixin_discretion
    import mixin_memory
    import mixin_phone

    class Host(mixin_memory.MemoryMixin, mixin_discretion.DiscretionMixin, mixin_phone.PhoneMixin):
        def __init__(self):
            self.redline_filter = bool(redline)
            self._forget_reg = None
            self._known_memory_ids = None
            self._known_memory_texts = None
            self.api_config = {}
            try:
                if common.API_CONFIG_PATH.exists():
                    loaded = json.loads(common.API_CONFIG_PATH.read_text(encoding="utf-8"))
                    if isinstance(loaded, dict):
                        self.api_config = loaded
            except Exception:
                self.api_config = {}

        def _registry(self):
            """The forget registry: hers when there is one, else an empty one in memory (a
            dry run must not create a file)."""
            reg = getattr(self, "_forget_reg", None)
            if reg is None:
                path = Path(common.FORGET_REGISTRY_PATH)
                reg = forget_registry.ForgetRegistry(path if path.exists() else None)
                self._forget_reg = reg
            return reg

        def _embedding_runtime_config(self):
            """The embedding endpoint saved in the panel (there is no AstrBot here)."""
            saved = self.api_config.get("embedding") if isinstance(self.api_config.get("embedding"), dict) else {}
            if not saved.get("base_url"):
                return None
            return {"base_url": saved.get("base_url"), "api_key": saved.get("api_key", ""),
                    "model": saved.get("model", "")}

    return Host()


def close_host(host) -> None:
    """Close the databases a host opened, so Windows may move or remove the folder."""
    for name in ("_forget_reg", "_vectors_db"):
        store = getattr(host, name, None)
        close = getattr(store, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass
        try:
            setattr(host, name, None)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Reading one copy
# ---------------------------------------------------------------------------
def read_backup(folder):
    """The memory entries of one copy of the data folder (its library.json)."""
    folder = Path(folder)
    lib_path = folder / "library.json"
    if not lib_path.is_file():
        raise Problem("这份备份里没有 library.json：%s" % folder.name)
    try:
        lib = json.loads(lib_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Problem("这份备份的 library.json 读不了：%s" % folder.name) from exc
    entries = lib.get("entries") if isinstance(lib, dict) else None
    return [e for e in entries if isinstance(e, dict)] if isinstance(entries, list) else []


def read_vectors(folder) -> dict:
    """entry id -> vector, from a folder's vectors.sqlite3 (read only); {} when there is none."""
    import vector_store
    path = Path(folder) / vector_store.FILE_NAME
    if not path.is_file():
        return {}
    out = {}
    try:
        db = sqlite3.connect("file:" + path.resolve().as_posix() + "?mode=ro&immutable=1", uri=True)
        try:
            for eid, blob in db.execute("SELECT entry_id, data FROM vectors"):
                try:
                    out[str(eid)] = vector_store._unpack(blob)
                except Exception:
                    continue
        finally:
            db.close()
    except Exception:
        return {}
    return out


def vector_dims(entries, folder=None) -> int:
    """The library's vector length: from an entry that still carries one, else its store."""
    for e in entries or []:
        if not isinstance(e, dict):
            continue
        vec = e.get("vector")
        if isinstance(vec, list) and vec:
            return len(vec)
    if folder is not None:
        for vec in read_vectors(folder).values():
            if vec:
                return len(vec)
    return 0


def embedding_is_local(host) -> bool:
    """Whether the embedding service the panel saves is on this computer."""
    try:
        conf = host._embedding_runtime_config() or {}
        parts = urllib.parse.urlsplit(str(conf.get("base_url") or ""))
        return parts.hostname in LOCAL_HOSTS
    except Exception:
        return False


def embed_text(host, text):
    """One vector from the local bge-m3 service, through the plugin's own _embed_text."""
    if not embedding_is_local(host):
        return None
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(host._embed_text(text))
    finally:
        loop.close()


# ---------------------------------------------------------------------------
# What a run would do (reads only), and what --apply does
# ---------------------------------------------------------------------------
def scan(host, backups) -> dict:
    """The entries each copy can put back, and the counts. Reads; writes nothing.

    Only a memory whose id the library does not have now is a candidate. It must pass
    the forget registry and the red line, and it must end up with a vector.
    """
    lib = host._read_library(vectors=False)
    have = {str(e.get("id")) for e in lib.get("entries") or []
            if isinstance(e, dict) and e.get("id")}
    dims = vector_dims(lib.get("entries") or [], memory_dir())
    local = embedding_is_local(host)
    report = {"backups": [], "restorable": 0, "registry": 0, "redline": 0, "no_vector": 0,
              "already": 0, "recomputed": 0, "entries": []}
    planned = set()
    for folder in backups:
        entries = read_backup(folder)
        vectors = read_vectors(folder)
        row = {"name": Path(folder).name, "restorable": 0, "registry": 0,
               "redline": 0, "no_vector": 0}
        for entry in entries:
            eid = str(entry.get("id") or "")
            if not eid:
                continue
            if eid in have or eid in planned:
                report["already"] += 1
                continue
            # the same gates _write_library keeps, counted here for the dry run too
            if not host._origin_kept(entry):
                row["registry"] += 1
                continue
            text = str(entry.get("text") or "")
            if host._red_line(text, RED_LINE_WHAT):
                row["redline"] += 1
                continue
            vec = vectors.get(eid)
            if not isinstance(vec, list) or not vec or (dims and len(vec) != dims):
                vec = None
            if vec is None:
                # no vector in the copy, or the dimensions are not the library's: ask
                # this computer's own bge-m3, never a service somewhere else
                if not local:
                    row["no_vector"] += 1
                    continue
                report["recomputed"] += 1
                try:
                    vec = embed_text(host, text)
                except Exception:
                    vec = None
                if not vec:
                    row["no_vector"] += 1
                    continue
            new = copy.deepcopy(entry)
            new["vector"] = [float(x) for x in vec]
            report["entries"].append(new)
            planned.add(eid)
            row["restorable"] += 1
        report["backups"].append(row)
        for key in ("restorable", "registry", "redline", "no_vector"):
            report[key] += row[key]
    return report


def memory_dir() -> Path:
    """Her memory folder, as the plugin's own common module has it."""
    import common
    return Path(common.MEMORY_DIR)


def copy_before(stamp) -> Path:
    """Copy her whole memory folder beside itself; return the copy. Nothing is written
    until this has finished and its library.json is there."""
    src = memory_dir()
    if not src.is_dir():
        raise Problem("没有 memory 文件夹，无法先复制一份：不补。")
    base = "%s%s" % (COPY_PREFIX, stamp)
    target = src.parent / base
    n = 1
    while target.exists():
        n += 1
        target = src.parent / ("%s-%d" % (base, n))
    _guard.output_dir(target, "the copy before restoring", make=False)   # may refuse: then nothing is copied
    try:
        shutil.copytree(src, target)
    except Exception as exc:
        raise Problem("复制 memory 文件夹失败，没有写入：%s" % exc) from exc
    if not (target / "library.json").is_file():
        raise Problem("复制出来的文件夹里没有 library.json：没有写入。")
    return target


def restore(host, backups, now=None) -> dict:
    """Plan, copy her memory folder, then write the plan through _write_library."""
    report = scan(host, backups)
    report["written"] = 0
    report["copy"] = None
    if not report["entries"]:
        return report
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time() if now is None else float(now)))
    target = copy_before(stamp)
    lib = host._read_library()
    lib["entries"] = list(lib.get("entries") or []) + report["entries"]
    if not host._write_library(lib):
        raise Problem("忘记的登记读不了，没有写入。")
    report["written"] = len(report["entries"])
    report["copy"] = target
    return report


# ---------------------------------------------------------------------------
# The screen
# ---------------------------------------------------------------------------
def print_report(report, applied=False) -> None:
    """Per copy and in all: the four counts. No memory's words, no number, no place."""
    for i, row in enumerate(report.get("backups") or [], start=1):
        print("备份 %d（%s）：能补 %d 条，登记挡了 %d 条，红线挡了 %d 条，没向量 %d 条"
              % (i, row["name"], row["restorable"], row["registry"],
                 row["redline"], row["no_vector"]))
    print("合计：能补 %d 条，登记挡了 %d 条，红线挡了 %d 条，没向量 %d 条"
          % (report["restorable"], report["registry"], report["redline"], report["no_vector"]))
    if applied:
        print("补回了 %d 条。" % report.get("written", 0))
        if report.get("copy") is not None:
            print("补前的那一份在：%s" % Path(report["copy"]).name)
    else:
        print("只是试跑，没有写入。加 --apply 才真写。")


def _utf8() -> None:
    """Chinese names print on a Windows console too; a redirected stream is already text."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def main(argv=None) -> int:
    _utf8()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--data", required=True, help="her data folder (her-data); it holds memory/")
    parser.add_argument("--backup", action="append", default=[], required=True,
                        help="a copy's memory folder (repeatable; a * in it is expanded)")
    parser.add_argument("--apply", action="store_true", help="really write (her memory folder is copied first)")
    parser.add_argument("--redline", action="store_true",
                        help="the redline_filter switch is on in her config (off by default)")
    args = parser.parse_args(argv)
    data = Path(args.data).resolve()
    if not (data / "memory").is_dir():
        print("她的数据目录里没有 memory 文件夹：%s" % data, file=sys.stderr)
        return REFUSED
    folders = []
    for pattern in args.backup:
        found = sorted(glob.glob(str(pattern))) or [str(pattern)]
        folders.extend(Path(name) for name in found)
    for folder in folders:
        if not (folder / "library.json").is_file():
            print("这份备份里没有 library.json：%s" % folder.name, file=sys.stderr)
            return REFUSED
    os.environ["AMS_LIFE_DATA_DIR"] = str(data)
    import common
    import forget_registry
    if Path(common.DATA_DIR).resolve() != data:
        print("这个进程已经读过另一个数据目录，没有动手。", file=sys.stderr)
        return REFUSED
    host = make_host(args.redline)
    try:
        if args.apply:
            print_report(restore(host, folders), applied=True)
        else:
            print_report(scan(host, folders), applied=False)
        return OK
    except _guard.Refused as exc:
        print(exc, file=sys.stderr)
        return REFUSED
    except forget_registry.Unreadable as exc:
        print("忘记的登记读不了，没有动手：%s" % exc, file=sys.stderr)
        return REFUSED
    except Problem as exc:
        print(exc, file=sys.stderr)
        return REFUSED
    finally:
        close_host(host)


if __name__ == "__main__":
    raise SystemExit(main())
