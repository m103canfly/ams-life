# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.

# 2026-10-31 move-7b: the persona export tool

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Sections 1 and 5 say her persona, "爱弥斯", must leave AstrBot's `data_v4.db` and become the
`persona.md` file that `persona_file.py` (move 5h) reads, with the same words: the move checks
that by comparing digests, no one reads the real words. This card writes the tool that does the
copy. It is not wired into the plugin, no switch or setting is added, and it is not run on any
real database here: every database and every persona in the tests is made up. The real export
is run by the dispatcher at the machine on the move's day, and only the digests are looked at.

## What was added

* `tools/export_persona.py`, two commands:

      python tools/export_persona.py --db <data_v4.db> --list
      python tools/export_persona.py --db <data_v4.db> --persona-id <name> --out <persona.md>

  The table is AstrBot 4.29.3's `personas` (`core/db/po.py`); only `persona_id` (the name),
  `system_prompt` (the words) and `begin_dialogs` (opening dialogs, JSON) are read. The database
  is opened read only: `sqlite3.connect(Path(...).resolve().as_uri() + "?mode=ro", uri=True)`,
  the path as an SQLite URI, so Chinese and spaces in it work and nothing can be written to the
  database. `--list` prints each `persona_id` and how many there are, never the words. The
  export reads the row, sends `--out` through `tools/_guard.output_file` and refuses a file that
  is already there, then writes with `persona_file.save`: newlines become `\n`, the body is at
  most `MAX_CHARS`, the temp file is swapped in with `atomic_file.replace`. Then the two digests
  are compared: sha256 of the column's text after the same newline change, and sha256 of the
  file. Only the standard library, `persona_file` and `tools/_guard`; no AstrBot, no `logging`,
  no log file, no network.

  The screen gets the character count, both digests and whether they match, how many newlines
  had to be made `\n` (CRLF and lone CR counts), how many `begin_dialogs` the row holds, the
  line numbers `persona_file` would leave out of her prompt, and whether the body had to be
  cut. No persona text is printed, and an error message holds none either. Exit code 0 means
  the digests match, `begin_dialogs` is 0, no line is left out and nothing was cut; 1 means the
  file is written but a person should look; 2 means it stopped and wrote nothing (database not
  readable, no `personas` table, no such name, an output file already there, words
  `persona_file` refuses, or an output the guard refuses).
* `tests/test_export_persona.py`: eleven tests on made-up data. The `personas` table is built in
  the test's own temporary folder with AstrBot's columns and a made-up body ("她叫编造。说话温柔。"
  and the like); every database and every file is made there and removed afterwards. Cases:
  `--list` gives both names and "2" and no words; an export gives exit code 0, the file holds
  exactly the column's text, both digests are equal and no words are printed; a body with CRLF
  and CR is written with LF only and the digests are equal because they are taken after the
  newline change, with "newlines changed: 3 (2 CRLF, 1 CR)" on the screen; two `begin_dialogs`
  give exit code 1 with the reminder that they are not exported; a line "忽略之前的指令" stays in
  the file exactly (the save does not filter) while its line number 3 is printed and the exit
  code is 1; a body over `MAX_CHARS` gives exit code 2, writes nothing, leaves no temp file and
  prints no words; an unknown name, an existing output file and an output under a made-up
  `astrbot/data` folder all give exit code 2 and write nothing; the database's sha256 is the same
  before and after a list and an export and no `-wal`, `-journal` or `-shm` appears beside it; a
  database whose path has Chinese and spaces opens read only and exports; a missing database or
  one without a `personas` table gives exit code 2; and the tool's own source is read to check
  that it imports no AstrBot and no `logging` and that its one `sqlite3.connect` carries
  `mode=ro`, `uri=True` and `.as_uri()`.

README's table of modules needs no new row: `tools/` is already there (offline tools, writing
only outside the repository). If the tool had a row of its own it would read:

| `tools/export_persona.py` | 搬家用的离线工具：把 AstrBot 人格表里的一条人设只读导出成 `persona.md`，只打字数、哈希和行号，不打正文 |

## Why nothing else changes

Only the two new Python files and this note were added. No plugin module, entry point, switch,
setting, dependency, golden trace or existing test is touched, so the plugin's behaviour is
unchanged. The tool opens SQLite databases read only, prints to the screen only, and writes just
the one persona file the owner asks for; the guard keeps it out of AstrBot's data folder and out
of this repository. Every name, number and persona line in the tests is made up; no real
database, real persona or real data was read, copied or checked.

Tests: `python -m unittest tests.test_export_persona` (11 tests), for the dispatcher to run
outside the sandbox (this sandbox cannot write a test's temporary folder). The card's mutation
checks A, B and C are left to the last round, as the owner asked.

Tests: `tests.test_export_persona` passes outside the sandbox with `venv-ams-life` (11 tests). The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
