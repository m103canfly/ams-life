# 2026-10-31 move-7a: the configuration migration tool

Move design section 5: the switches, lists and prices in AstrBot's plugin configuration
(`astrbot\data\config\astrbot_plugin_ams_life_config.json`) become her own `config.json`,
compared item by item. 5g added the reading, writing and comparing (`app_config.py`); this
card adds the small tool that is run once, by hand, on the moving day.

## What was added

`tools/migrate_config.py` (new):

    python tools/migrate_config.py --astrbot <AstrBot's plugin config> --out <new config.json>
    python tools/migrate_config.py --astrbot <AstrBot's plugin config> --check <existing config.json>

- `--out`: `app_config.load_schema()`, then `app_config.load(astrbot, schema)`. The problem
  `unreadable` stops it with exit code 2 and nothing written. `_guard.output_file` keeps the
  new file out of the repository and out of any AstrBot data folder, and an existing
  `config.json` is never written over (exit code 2). Then `app_config.save`, and the new file
  is read back with `app_config.load` and compared item by item with AstrBot's copy, which is
  read again with `json` as `utf-8-sig` (AstrBot writes a byte-order mark).
- `--check`: that comparison only, for the last look on the moving day. It writes nothing.
- Printed: the number of settings, the problems (`unreadable`, `unknown: <key>`,
  `type: <key>`) and the keys that differ, plus the path written. A value is never printed,
  and there is no log file, only the screen.
- Exit codes: 0 everything agrees; 1 the file was written (or compared) but a person should
  look, because of a `type:` problem or a key that differs; 2 stopped before writing.
- AstrBot's copy is only read, never written. A `--astrbot` path that is not a file also
  stops with exit code 2, instead of quietly writing a `config.json` of defaults.

`tests/test_migrate_config.py` (new) has nine tests covering the card's eight checks (the
`--check` pair is two tests). Every file is built in the test's own temporary folder and
removed afterwards; every value is made up; the repository's real `_conf_schema.json` is
used as it is:

1. a BOM-carrying AstrBot-style file gives exit 0; the new file has no BOM; read back it is
   the same; `compare` is empty;
2. a `bool` setting given a string gives exit 1; the key is on the screen and the value is
   not; the file is written with the default there;
3. bad JSON gives exit 2 and nothing is written;
4. an existing `config.json` gives exit 2 and its bytes are unchanged;
5. an output path under `astrbot\data\...` is refused by `_guard`, nothing is written;
6. `--check`: equal gives 0, one setting changed gives 1 with the key only; both files are
   unchanged (compared by hash);
7. no made-up value reaches the screen in any of the runs;
8. the source imports neither `astrbot` nor `logging`.

## Behavior

Unchanged for the plugin: nothing imports the tool, there is no switch, and no golden trace
moves. The tool is run only by hand on the moving day; until then it is tried against made-up
data only. The files added are `tools/migrate_config.py`, `tests/test_migrate_config.py` and
this note; nothing else changed.

## Tests

Only `tests/test_migrate_config.py` was run (the owner's rule of 10-31: each card runs only
the test file it adds or changes). In the sandbox Python could not write inside a freshly
made temporary folder, so the file stopped in its fixtures with `PermissionError`; the
dispatcher runs it outside.

Tests: `tests.test_migrate_config` passes outside the sandbox with `venv-ams-life` (9 tests). The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
