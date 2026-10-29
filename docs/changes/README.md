# docs/changes: what each pull request changed

From 2026-10-30 every pull request describes its change in a file of its own here, instead of
adding a row to the table in `NOTICE.md` (the table keeps the changes before that date). One pull
request, one new file; nobody edits another's, so pull requests no longer collide over one line.

## Name

`<date>-<branch>.md`, the date the pull request was opened, e.g. `2026-10-30-send-check.md`.

## What goes in

- the date, and what changed: what someone reading the code later needs to know (English or 中文);
- the files it touched;
- a new module: the line it would have in README's table of modules (README's table is brought up
  to date now and then by a small pull request of its own, not by every pull request).

## Why this still meets the AGPL

AGPL-3.0 section 5(a) asks a modified work to carry prominent notices that it was changed, with a
relevant date. `NOTICE.md` still says from the top that ams-life is a modified version of BioCore
v1.2.99 and that every later change is in the git history; every modified or new source file still
starts with a line pointing to `NOTICE.md`; each change has its dated description here.
