# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Rename the AstrBot session keys in a copy of her data folder to neutral place names.

    python tools/rename_places.py --data <a copy of her data folder>
    python tools/rename_places.py --data <the same folder> --check

Old records keep AstrBot's chat ids ("default:GroupMessage:900001"); the plugin now stores
neutral place names ("group:900001", what discretion.place_of gives). This tool changes the
old values once, in a copy made by tools/migrate_data.py -- never in her own data folder.

Changed, and only these:
    archives/events.jsonl                    session, provenance.session,
                                             provenance.sources[].session,
                                             source_check.source_items[].session
    archives/sessions/<folder>/events.jsonl  the same fields; the folders are then merged by
                                             the folder name the new session gives (the
                                             plugin's own rule, mixin_events)
    memory/library.json                      entries[].provenance.session and .sources[].session
    users/*.json                             sessions (the last place kept, at most 20)
    archives/dedupe_log.jsonl                session, dropped_sessions
Not changed: phone/ windows (their umo is AstrBot's wiring, not a key), the old archives,
insights, and people/ (the names and aliases she keeps of people).

Everything is read and worked out before anything is written: a file that cannot be read, two
unapproved platform prefixes, or two events with one id and different content stops the run with exit 2,
and no file is written. Events of one place are deduplicated by id (an identical record is
kept once) and sorted by ts before they are written, then the folders merged into it are
removed. Printed: counts, folder names and relative paths only, never a record's words.
Exit: 0 all done, 1 --check found something left, 2 not started.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import atomic_file  # noqa: E402
import discretion  # noqa: E402
from tools import _guard  # noqa: E402

OK, LEFT, NOT_STARTED = 0, 1, 2
FOLDERS_SHOWN = 5
USERS_MAX = 20
KIND = re.compile(r"(FriendMessage|GroupMessage|GuildMessage|TempMessage|OtherMessage)")
EVENTS = ("archives", "events.jsonl")
SESSIONS = ("archives", "sessions")
LIBRARY = ("memory", "library.json")
USERS = ("users",)
DEDUPE = ("archives", "dedupe_log.jsonl")


class Problem(Exception):
    """Nothing is written: the copy is not in a state this tool may change."""


# ---------------------------------------------------------------------------
# Names: what a session becomes, and the folder the plugin keeps its events in.
# ---------------------------------------------------------------------------
def session_ish(value) -> bool:
    """Whether a value is an AstrBot session string (a chat kind somewhere in it)."""
    return isinstance(value, str) and bool(KIND.search(value))


def prefix_of(value) -> str:
    """The platform prefix of an AstrBot session string ("default:GroupMessage:42" -> "default")."""
    match = KIND.search(value)
    return value[:match.start()].strip(":_") if match else ""


def folder_of(session) -> str:
    """The folder the plugin keeps a place's events in (mixin_events._event_session_file)."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in str(session or "default"))[:80]


def keep_last(items) -> list:
    """The items with a repeat kept only where it was last (the newest one is last), at most 20."""
    last = {}
    for index, item in enumerate(items):
        last[_key(item)] = index
    kept = [item for index, item in enumerate(items) if last[_key(item)] == index]
    return kept[-USERS_MAX:]


def _key(item) -> str:
    """A hashable, order-independent key for one item of a sessions list."""
    try:
        return json.dumps(item, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return repr(item)


def _ts(row) -> float:
    """The record's own time, for sorting; anything else sorts as 0."""
    obj = row[1] if isinstance(row, tuple) else row
    if not isinstance(obj, dict):
        return 0.0
    try:
        return float(obj.get("ts") or 0)
    except (TypeError, ValueError):
        return 0.0


# ---------------------------------------------------------------------------
# Where a session sits in a record.
# ---------------------------------------------------------------------------
def event_holders(rec) -> list:
    """The dicts of one event that hold a session: the record, its provenance, each of the
    provenance's sources, and each of source_check's items."""
    holders = [rec]
    prov = rec.get("provenance")
    if isinstance(prov, dict):
        holders.append(prov)
        holders.extend(x for x in (prov.get("sources") or []) if isinstance(x, dict))
    check = rec.get("source_check")
    if isinstance(check, dict):
        holders.extend(x for x in (check.get("source_items") or []) if isinstance(x, dict))
    return holders


def memory_holders(entry) -> list:
    """The dicts of one memory entry that hold a session: its provenance and their sources."""
    holders = []
    prov = entry.get("provenance")
    if isinstance(prov, dict):
        holders.append(prov)
        holders.extend(x for x in (prov.get("sources") or []) if isinstance(x, dict))
    return holders


def _rename_field(holder, changed, place=discretion.place_of) -> bool:
    """Set holder["session"] to discretion.place_of; True when it changed. A value that is not
    a string is left alone (an empty one stays empty)."""
    value = holder.get("session")
    if not isinstance(value, str):
        return False
    new = place(value)
    if new == value:
        return False
    holder["session"] = new
    changed.append((value, new))
    return True


def event_values(rows) -> list:
    """Every session value of one events.jsonl's rows, as they are now."""
    out = []
    for _line, obj in rows:
        if isinstance(obj, dict):
            for holder in event_holders(obj):
                if isinstance(holder.get("session"), str):
                    out.append(holder["session"])
    return out


def memory_values(doc) -> list:
    """Every session value of the library's entries, as they are now."""
    out = []
    if isinstance(doc, dict):
        for entry in doc.get("entries") or []:
            if isinstance(entry, dict):
                for holder in memory_holders(entry):
                    if isinstance(holder.get("session"), str):
                        out.append(holder["session"])
    return out


def sessions_of(doc) -> list:
    """The sessions list of one users/*.json file, as it is now."""
    if isinstance(doc, dict) and isinstance(doc.get("sessions"), list):
        return [x for x in doc["sessions"] if isinstance(x, str)]
    return []


def dedupe_values(rows) -> list:
    """Every session value of one dedupe_log.jsonl's rows, as they are now."""
    out = []
    for _line, obj in rows:
        if not isinstance(obj, dict):
            continue
        if isinstance(obj.get("session"), str):
            out.append(obj["session"])
        for value in obj.get("dropped_sessions") or []:
            if isinstance(value, str):
                out.append(value)
    return out


def _entries(doc) -> int:
    if isinstance(doc, dict) and isinstance(doc.get("entries"), list):
        return len(doc["entries"])
    return 0


# ---------------------------------------------------------------------------
# Reading, and writing a line back.
# ---------------------------------------------------------------------------
def _rel(data, path) -> str:
    """A path as the report prints it: relative to the data folder, posix separators."""
    try:
        return Path(path).relative_to(data).as_posix()
    except ValueError:
        return Path(path).name


def read_jsonl(path, data):
    """(text, [(raw line, object)]) for one JSONL file. A line that is not JSON stops the run
    with the relative path only: its words are not printed."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, ValueError):
        raise Problem("读不了：%s" % _rel(data, path))
    rows = []
    for line in text.splitlines():
        if not line.strip():
            rows.append((line, None))
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            raise Problem("读不了：%s" % _rel(data, path))
        rows.append((line, obj))
    return text, rows


def read_json(path, data):
    """(text, object) for one JSON file. A file that cannot be read stops the run."""
    try:
        text = Path(path).read_text(encoding="utf-8")
        doc = json.loads(text)
    except (OSError, ValueError):
        raise Problem("读不了：%s" % _rel(data, path))
    return text, doc


def render(rows) -> str:
    """The text of a JSONL file: a line kept as it was, or written again from its object."""
    parts = []
    for line, obj in rows:
        parts.append(line if line is not None else json.dumps(obj, ensure_ascii=False))
    return "".join(part + "\n" for part in parts)


def _write(path, text) -> None:
    """Write a temp file beside the target and put it in place (atomic_file)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    atomic_file.replace(tmp, path)


# ---------------------------------------------------------------------------
# Renaming one store, in memory.
# ---------------------------------------------------------------------------
def renamed_events(rows, place=discretion.place_of):
    """(rows, changed) with the session fields of one events.jsonl renamed."""
    out, changed = [], []
    for line, obj in rows:
        if not isinstance(obj, dict):
            out.append((line, obj))
            continue
        mine = []
        for holder in event_holders(obj):
            _rename_field(holder, mine, place)
        changed.extend(mine)
        out.append((line if not mine else None, obj))
    return out, changed


def renamed_memory(doc, place=discretion.place_of) -> list:
    """The session fields of the library's entries renamed in place; returns the changes."""
    changed = []
    if isinstance(doc, dict):
        for entry in doc.get("entries") or []:
            if isinstance(entry, dict):
                for holder in memory_holders(entry):
                    _rename_field(holder, changed, place)
    return changed


def renamed_sessions(doc, place=discretion.place_of):
    """A users/*.json file's sessions renamed in place, the last place kept, at most 20.
    Returns (changes, whether the list changed at all): a place kept once is one change, a
    repeat dropped or a list cut to 20 is no rename, but the file is still written."""
    if not isinstance(doc, dict) or not isinstance(doc.get("sessions"), list):
        return [], False
    old = list(doc["sessions"])
    changed = []
    new = []
    for value in old:
        if isinstance(value, str):
            placed = place(value)
            if placed != value:
                changed.append((value, placed))
            new.append(placed)
        else:
            new.append(value)
    new = keep_last(new)
    if new != old:
        doc["sessions"] = new
    return changed, new != old


def renamed_dedupe(rows, place=discretion.place_of):
    """(rows, changed) with the session fields of one dedupe_log.jsonl renamed."""
    out, changed = [], []
    for line, obj in rows:
        if not isinstance(obj, dict):
            out.append((line, obj))
            continue
        mine = []
        _rename_field(obj, mine, place)
        values = obj.get("dropped_sessions")
        if isinstance(values, list):
            new = [place(x) if isinstance(x, str) else x for x in values]
            for before, after in zip(values, new):
                if before != after:
                    mine.append((before, after))
            if new != values:
                obj["dropped_sessions"] = new
        changed.extend(mine)
        out.append((line if not mine else None, obj))
    return out, changed


# ---------------------------------------------------------------------------
# The copy of her data folder.
# ---------------------------------------------------------------------------
class Copy:
    """Read once, worked out in memory, then written: nothing is written before every check."""

    def __init__(self, data):
        self.data = Path(data)
        self.events = None
        self.folders = {}
        self.library = None
        self.users = {}
        self.dedupe = None
        self.changed = {"events": [], "sessions": [], "library": [], "users": [], "dedupe": []}
        self.user_modified = {}
        self.prefixes = {}
        self.private = 0
        self.as_group = 0
        self.left = []
        self.mismatched = []
        self.groups = {}
        self.sources = {}
        self.dropped = 0
        self.merged_groups = 0
        self.before = {}
        self.after = {}

    # -- reading ---------------------------------------------------------
    def read(self) -> None:
        """Read every file this tool may change. A file that cannot be read stops the run."""
        data = self.data
        path = data.joinpath(*EVENTS)
        if path.is_file():
            self.events = read_jsonl(path, data)
            self.before["events"] = len(self.events[1])
        sessions = data.joinpath(*SESSIONS)
        if sessions.is_dir():
            for folder in sorted(p for p in sessions.iterdir() if p.is_dir()):
                file = folder / "events.jsonl"
                if file.is_file():
                    self.folders[folder.name] = read_jsonl(file, data)
        self.before["sessions"] = sum(len(rows) for _text, rows in self.folders.values())
        path = data.joinpath(*LIBRARY)
        if path.is_file():
            self.library = read_json(path, data)
            self.before["library"] = _entries(self.library[1])
        users = data.joinpath(*USERS)
        if users.is_dir():
            for file in sorted(p for p in users.glob("*.json") if p.is_file()):
                self.users[file] = read_json(file, data)
        self.before["users_files"] = len(self.users)
        self.before["users"] = sum(len(sessions_of(doc)) for _text, doc in self.users.values())
        path = data.joinpath(*DEDUPE)
        if path.is_file():
            self.dedupe = read_jsonl(path, data)
            self.before["dedupe"] = len(self.dedupe[1])

    def _every_value(self):
        """(relative path, every session value) for each store, as it is now."""
        if self.events is not None:
            yield _rel(self.data, self.data.joinpath(*EVENTS)), event_values(self.events[1])
        root = self.data.joinpath(*SESSIONS)
        for name, (_text, rows) in self.folders.items():
            yield _rel(self.data, root / name / "events.jsonl"), event_values(rows)
        if self.library is not None:
            yield _rel(self.data, self.data.joinpath(*LIBRARY)), memory_values(self.library[1])
        for path, (_text, doc) in self.users.items():
            yield _rel(self.data, path), sessions_of(doc)
        if self.dedupe is not None:
            yield _rel(self.data, self.data.joinpath(*DEDUPE)), dedupe_values(self.dedupe[1])

    # -- the checks done before anything is written ----------------------
    def scan(self, same_account=None) -> None:
        """Collect every session string first: check platform prefixes, and (for --check)
        what is still a session and each folder's own events."""
        like = set()
        for label, values in self._every_value():
            found = [value for value in values if session_ish(value)]
            self.left.append((label, len(found)))
            like.update(found)
        for value in sorted(like):
            prefix = prefix_of(value)
            self.prefixes[prefix] = self.prefixes.get(prefix, 0) + 1
            kind = KIND.search(value).group(1)
            if kind == "TempMessage":
                self.private += 1
            elif kind == "GuildMessage":
                self.as_group += 1
        if (same_account is None and len(self.prefixes) > 1 or
                same_account is not None and set(self.prefixes) - same_account):
            reason = "平台前缀不止一种" if same_account is None else "平台前缀不在同账号名单中"
            raise Problem("%s：%s" % (reason, "、".join(
                "%s（%d 个）" % (prefix or "（没有前缀）", count)
                for prefix, count in sorted(self.prefixes.items()))))
        root = self.data.joinpath(*SESSIONS)
        for name, (_text, rows) in sorted(self.folders.items()):
            wrong = 0
            for _line, obj in rows:
                session = obj.get("session") if isinstance(obj, dict) else ""
                if folder_of(session if isinstance(session, str) else "") != name:
                    wrong += 1
            self.mismatched.append((_rel(self.data, root / name), wrong))

    # -- renaming, in memory --------------------------------------------
    def rename(self, same_account=None) -> None:
        """Rename every session field of everything read. Nothing is written here."""
        def place(value):
            match = KIND.search(value)
            if (same_account is not None and match and prefix_of(value) in same_account
                    and value[:match.start()] == prefix_of(value) + ":"):
                return discretion.place_of(value[match.start():])
            return discretion.place_of(value)

        if self.events is not None:
            rows, changed = renamed_events(self.events[1], place)
            self.events = (self.events[0], rows)
            self.changed["events"] = changed
        for name, (text, rows) in list(self.folders.items()):
            rows, changed = renamed_events(rows, place)
            self.folders[name] = (text, rows)
            self.changed["sessions"].extend(changed)
        if self.library is not None:
            self.changed["library"] = renamed_memory(self.library[1], place)
        for path, (text, doc) in list(self.users.items()):
            changed, self.user_modified[path] = renamed_sessions(doc, place)
            self.changed["users"].extend(changed)
        if self.dedupe is not None:
            rows, changed = renamed_dedupe(self.dedupe[1], place)
            self.dedupe = (self.dedupe[0], rows)
            self.changed["dedupe"] = changed

    # -- the events of one place ----------------------------------------
    def merge(self) -> None:
        """Put every folder's events where the renamed session says: by id (an identical
        record once, one id with two contents stops the run), sorted by ts."""
        gathered, sources = {}, {}
        for name in sorted(self.folders):
            _text, rows = self.folders[name]
            for row in rows:
                obj = row[1]
                session = obj.get("session") if isinstance(obj, dict) else ""
                target = folder_of(session if isinstance(session, str) else "")
                gathered.setdefault(target, []).append(row)
                sources.setdefault(target, [])
                if name not in sources[target]:
                    sources[target].append(name)
        for target in sorted(gathered):
            rows, dropped = self._dedupe(gathered[target], target)
            self.dropped += dropped
            rows.sort(key=_ts)
            self.groups[target] = rows
        self.sources = sources
        self.merged_groups = sum(1 for names in sources.values() if len(names) > 1)

    def _dedupe(self, rows, target):
        """(rows, dropped) with one id kept once. The same id twice with different content
        stops the run: the target folder and the id are printed, never the words."""
        kept, seen, dropped = [], {}, 0
        for row in rows:
            obj = row[1]
            ident = str(obj.get("id") or "") if isinstance(obj, dict) else ""
            if not ident:
                kept.append(row)
                continue
            canon = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
            if ident in seen:
                if seen[ident] != canon:
                    raise Problem("同一个 id 的内容不一样：%s（id %s）" % (
                        _rel(self.data, self.data.joinpath(*SESSIONS) / target), ident))
                dropped += 1
                continue
            seen[ident] = canon
            kept.append(row)
        return kept, dropped

    # -- writing ---------------------------------------------------------
    def write(self) -> None:
        """Write what changed; a folder merged into another one is removed after its events
        are written, and only in this copy."""
        data = self.data
        if self.events is not None and self.changed["events"]:
            _write(data.joinpath(*EVENTS), render(self.events[1]))
        root = data.joinpath(*SESSIONS)
        for target in sorted(self.groups):
            rows = self.groups[target]
            text = self.folders[target][0] if target in self.folders else ""
            new = render(rows)
            if new != text:
                _write(root / target / "events.jsonl", new)
        for name, target in sorted((name, target) for target, names in self.sources.items()
                                   for name in names):
            if name == target or name in self.groups:
                continue
            if not (root / target / "events.jsonl").is_file():
                continue
            old = root / name / "events.jsonl"
            if old.is_file():
                old.unlink()
            try:
                (root / name).rmdir()
            except OSError:
                pass
        if self.library is not None and self.changed["library"]:
            _write(data.joinpath(*LIBRARY), json.dumps(self.library[1], ensure_ascii=False))
        for path, (_text, doc) in sorted(self.users.items()):
            if self.user_modified.get(path):
                _write(path, json.dumps(doc, ensure_ascii=False, indent=1))
        if self.dedupe is not None and self.changed["dedupe"]:
            _write(data.joinpath(*DEDUPE), render(self.dedupe[1]))

    # -- the report ------------------------------------------------------
    def counts_after(self) -> None:
        """The counts after the rename, for the report's "before -> after"."""
        self.after["events"] = len(self.events[1]) if self.events is not None else 0
        self.after["sessions"] = sum(len(rows) for rows in self.groups.values())
        self.after["library"] = _entries(self.library[1]) if self.library is not None else 0
        self.after["users_files"] = len(self.users)
        self.after["users"] = sum(len(sessions_of(doc)) for _text, doc in self.users.values())
        self.after["dedupe"] = len(self.dedupe[1]) if self.dedupe is not None else 0

    def report(self) -> None:
        """Counts, folder names and relative paths: no record's words, no key."""
        self.counts_after()
        before_folders = sorted(self.folders)
        after_folders = sorted(self.groups)
        print("事件存档 archives/events.jsonl：改了 %d 个值，%d 条 -> %d 条" % (
            len(self.changed["events"]), self.before.get("events", 0), self.after["events"]))
        print("事件文件夹：改前 %d 个（%s）" % (len(before_folders), _few(before_folders)))
        print("事件文件夹：改后 %d 个（%s）" % (len(after_folders), _few(after_folders)))
        print("合并了 %d 组，去掉 %d 条一模一样的事件；改了 %d 个值，%d 条 -> %d 条" % (
            self.merged_groups, self.dropped, len(self.changed["sessions"]),
            self.before.get("sessions", 0), self.after["sessions"]))
        print("记忆 memory/library.json：改了 %d 个值，%d 条 -> %d 条" % (
            len(self.changed["library"]), self.before.get("library", 0), self.after["library"]))
        print("用户 users：%d 个文件，改了 %d 个会话，%d 个 -> %d 个" % (
            self.after["users_files"], len(self.changed["users"]),
            self.before.get("users", 0), self.after["users"]))
        print("去重日志 archives/dedupe_log.jsonl：改了 %d 个值，%d 条 -> %d 条" % (
            len(self.changed["dedupe"]), self.before.get("dedupe", 0), self.after["dedupe"]))
        print("TempMessage 算成私聊：%d 个；GuildMessage 算成群：%d 个" % (
            self.private, self.as_group))
        print("改完了。")

    # -- --check ---------------------------------------------------------
    def check(self) -> bool:
        """Read only: is any session string left, and is every event in its own folder?"""
        ok = True
        for label, count in self.left:
            if count:
                ok = False
                print("还有没改的会话串：%s（%d 个）" % (label, count))
        for folder, count in self.mismatched:
            if count:
                ok = False
                print("文件夹里的事件不在自己的地方：%s（%d 条）" % (folder, count))
        if ok:
            print("都对上了：没有会话串，事件都在自己的文件夹里。")
        return ok


def _few(names) -> str:
    """The first and the last few folder names, for the report."""
    names = list(names)
    if not names:
        return "（没有）"
    if len(names) <= 2 * FOLDERS_SHOWN:
        return "、".join(names)
    return "前 %d 个：%s；后 %d 个：%s" % (
        FOLDERS_SHOWN, "、".join(names[:FOLDERS_SHOWN]),
        FOLDERS_SHOWN, "、".join(names[-FOLDERS_SHOWN:]))


def checked_path(path) -> Path:
    """The data folder this tool may work on: it exists, is not in the repository, and is not
    (part of) a live AstrBot data folder. It only ever runs on the copy 7c made of her data."""
    data = Path(path).resolve()
    why = _guard.live_reason(data)
    if why:
        raise Problem("不能用这个目录：%s" % why)
    if _inside(data, _guard.ROOT):
        raise Problem("不能用这个目录：它在仓库里")
    if not data.exists():
        raise Problem("不能用这个目录：它不存在")
    if not data.is_dir():
        raise Problem("不能用这个目录：它不是文件夹")
    return data


def _inside(path, parent) -> bool:
    """Whether `path` is `parent` or below it (both already resolved)."""
    try:
        Path(path).relative_to(parent)
        return True
    except ValueError:
        return False


def _utf8() -> None:
    """Chinese names print on a Windows console too; a redirected stream is already text."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def main(argv=None) -> int:
    _utf8()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--data", required=True,
                        help="a copy of her data folder (tools/migrate_data.py made it)")
    parser.add_argument("--check", action="store_true",
                        help="only look: no session string left, and every event in its folder")
    parser.add_argument("--same-account", help="comma-separated prefixes of the same account")
    args = parser.parse_args(argv)
    try:
        data = checked_path(args.data)
        copy = Copy(data)
        copy.read()
        same_account = set(args.same_account.split(",")) if args.same_account is not None else None
        copy.scan(same_account)
        copy.rename(same_account)
        copy.merge()
        if args.check:
            return OK if copy.check() else LEFT
        copy.write()
        copy.report()
    except Problem as exc:
        print(exc, file=sys.stderr)
        return NOT_STARTED
    return OK


if __name__ == "__main__":
    raise SystemExit(main())
