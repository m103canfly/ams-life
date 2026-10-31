# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Export one persona from AstrBot's data_v4.db into a persona.md file (move card 7b).

    python tools/export_persona.py --db <data_v4.db> --list
    python tools/export_persona.py --db <data_v4.db> --persona-id <name> --out <persona.md>

The table is AstrBot 4.29.3's ``personas`` (core/db/po.py): ``persona_id`` is the name,
``system_prompt`` the words she is given, ``begin_dialogs`` the opening dialogs as JSON; the
other columns are not read. The database is opened read only, as SQLite's ``mode=ro`` URI
(``Path(...).resolve().as_uri()``), so a Chinese or space-bearing path works and nothing can
be written to it. No journal, no wal, no log file: only what is printed on the screen.

The move asks for the persona's words to be the same in the file as in the column, byte for
byte. The words go through ``persona_file.save`` (newlines become ``\\n``, the body is at most
``MAX_CHARS``, an existing file is never overwritten), then the sha256 of the column's text
after the same newline change is compared with the sha256 of the file: they must match.

No persona text is printed. The screen gets the character count, the two digests and whether
they match, how many newlines had to be made ``\\n``, how many opening dialogs the row holds,
the line numbers ``persona_file`` would leave out of her prompt, and whether the body had to
be cut.

Exit codes: 0 everything matched and nothing was left behind; 1 the file is written but a
person should look (the digests differ, opening dialogs are not exported, a line is left out
of her prompt, or the body was cut); 2 stopped and wrote nothing (no database, no personas
table, no such name, a file that is already there, words persona_file refuses, an output the
guard refuses).

Only the standard library, ``persona_file`` and ``tools/_guard``; no framework, no log.
"""
import argparse
import hashlib
import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import persona_file  # noqa: E402
from tools import _guard  # noqa: E402


def _fail(message, code=2) -> int:
    """One line on the screen, and the exit code to stop with."""
    print(message, file=sys.stderr)
    return code


def _utf8() -> None:
    """Chinese names print on a Windows console too; a redirected stream is already text."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def read_only(path) -> sqlite3.Connection:
    """The database as SQLite's URI, opened so that nothing may be written to it."""
    return sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True)


def open_personas(path) -> sqlite3.Connection:
    """The database, read only, with a personas table; otherwise sqlite3.Error."""
    db = read_only(path)
    try:
        db.execute("SELECT 1 FROM personas LIMIT 1").close()
    except sqlite3.Error:
        db.close()
        raise
    return db


def newlines(text) -> tuple:
    """How many CRLF and lone CR the newline change has to make: (CRLF, CR)."""
    crlf = text.count("\r\n")
    return crlf, text.count("\r") - crlf


def dialog_count(raw) -> int:
    """How many opening dialogs the column holds (0 when it holds nothing)."""
    if raw is None:
        return 0
    text = raw if isinstance(raw, str) else str(raw)
    if not text.strip():
        return 0
    try:
        value = json.loads(text)
    except ValueError:
        return 1          # something is there but it cannot be counted: say there is one
    if value is None:
        return 0
    if isinstance(value, list):
        return len(value)
    return 1


def list_personas(path) -> int:
    """Every persona_id and how many there are; never the words."""
    try:
        with closing(open_personas(path)) as db:
            names = [row[0] for row in db.execute("SELECT persona_id FROM personas ORDER BY persona_id")]
    except sqlite3.Error as error:
        return _fail("cannot read the database: %s" % error)
    for name in names:
        print("" if name is None else name)
    print("personas: %d" % len(names))
    return 0


def export(path, persona_id, out_path) -> int:
    """Write one persona to out_path, check its digest, and report. Nothing here prints words."""
    try:
        with closing(open_personas(path)) as db:
            row = db.execute("SELECT system_prompt, begin_dialogs FROM personas WHERE persona_id = ?",
                             (persona_id,)).fetchone()
    except sqlite3.Error as error:
        return _fail("cannot read the database: %s" % error)
    if row is None:
        return _fail("no persona named %r in the database" % persona_id)
    text, dialogs = row
    try:
        out = _guard.output_file(out_path, "persona")
    except _guard.Refused as refused:
        return _fail(str(refused))
    if out.exists():
        return _fail("refusing to write the persona to %s: it is already there" % out)
    try:
        persona = persona_file.save(out, text)
    except persona_file.PersonaError as error:
        return _fail(str(error))
    except OSError as error:
        return _fail("cannot write the persona file: %s" % error)

    # save changes the newlines and nothing else, so the two digests must be the same
    body = text.replace("\r\n", "\n").replace("\r", "\n")
    in_database = hashlib.sha256(body.encode("utf-8")).hexdigest()
    written = hashlib.sha256(out.read_bytes()).hexdigest()
    same = in_database == written
    crlf, cr = newlines(text)
    dialogs_left = dialog_count(dialogs)

    print("chars: %d" % len(body))
    print("sha256 in the database: %s" % in_database)
    print("sha256 of the file: %s" % written)
    print("equal: %s" % ("yes" if same else "no"))
    print("newlines changed: %d (%d CRLF, %d CR)" % (crlf + cr, crlf, cr))
    print("begin_dialogs: %d" % dialogs_left)
    if dialogs_left:
        print("the opening dialogs are not exported")
    print("lines left out: %s" % (", ".join(str(number) for number in persona.removed) or "none"))
    print("truncated: %s" % ("yes" if persona.truncated else "no"))
    if same and not dialogs_left and not persona.removed and not persona.truncated:
        return 0
    print("the file is written, but a person should look at it")
    return 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--db", required=True, help="AstrBot's data_v4.db (opened read only)")
    parser.add_argument("--list", action="store_true",
                        help="print every persona_id and how many there are, never the words")
    parser.add_argument("--persona-id", help="the persona to export, by its name in the table")
    parser.add_argument("--out",
                        help="the persona.md to write (a new file, outside AstrBot's data and this repository)")
    args = parser.parse_args(argv)
    _utf8()
    if args.list:
        if args.persona_id or args.out:
            parser.error("--list does not take --persona-id or --out")
        return list_personas(args.db)
    if not args.persona_id:
        parser.error("give --list, or --persona-id and --out")
    if not args.out:
        parser.error("--out is needed with --persona-id")
    return export(args.db, args.persona_id, args.out)


if __name__ == "__main__":
    sys.exit(main())
