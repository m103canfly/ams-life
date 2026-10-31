# 2026-10-31 move-5g: her own config.json

Move 5 takes AstrBot's plugin configuration out of the plugin: the switches, lists and
prices become her own `config.json`, compared item by item with AstrBot's copy on the
moving day. This card adds the reading and writing side only. It is not connected to the
plugin, and it does not read the owner's real configuration; the converting script is a
later card (block 7).

## Why, and what was added

`app_config.py` (new) reads the repository's `_conf_schema.json` (118 flat entries of five
types: bool, int, float, string, list), works out the defaults, loads a `config.json`,
saves it, and compares it with an AstrBot configuration dict. `tests/test_app_config.py`
(new) covers all of it, with its files built in the test's own temporary folder.

- `load_schema`: the schema as AstrBot shaped it, a dict of settings.
- `defaults`: the setting's own `default`; one without a `default` gets `False`, `""`,
  `0`, `0.0` or `[]` by its type. A list default is copied, so a caller cannot change
  the schema through it.
- `load`: `(config, problems)`. A missing file is all defaults and no problem. Bad JSON,
  or JSON that is not an object, is the defaults plus one problem `unreadable`, not an
  exception: a half-written file must not stop her from starting.
- `save`: UTF-8 JSON, two-space indents, schema order first and unknown keys last, swapped
  in from a temp file in the same folder through `atomic_file.replace`.
- `compare`: the schema keys whose two values differ. A key AstrBot's copy lacks counts as
  its default (AstrBot fills defaults the same way). Float settings compare as floats, so
  `1` and `1.0` are the same value.

## The type rules

bool takes only `true`/`false`; int takes whole numbers but not a bool; float takes whole
numbers and decimals but not a bool, and is read as a float; string and list as they are.
A value of the wrong type leaves the setting at its default and adds one problem
`type: <key>` — the file is not trusted to guess what was meant, and a price must not
silently become a string. `save` applies the same rules before writing: a wrong type
raises `ConfigError` and nothing is written, so a broken value cannot replace a good file.

## Why a key outside the schema is kept

A later version of her may add settings, and someone may edit `config.json` by hand. Both
leave keys this version does not know. Dropping them would quietly undo her settings on
the next save, so they are kept as they are (and written back, after the schema keys) and
only noted as `unknown: <key>`.

## Why a problem never holds a value

Lists and prices are the least public part of her configuration, and a problem ends up in
a log or in a panel message. A problem therefore has the key name and one word — `unreadable`,
`unknown: <key>` or `type: <key>` — and never the offending value. The same holds for
`ConfigError`, whose message names the key only.

## Behavior

Unchanged for the plugin: nothing imports `app_config` yet, so no switch, no panel page
and no golden trace moves. There is no feature switch either; the new module is inert
until a later card connects it. The files added are `app_config.py`,
`tests/test_app_config.py` and this note; nothing else changed.

## Full suite

1297 tests OK outside the sandbox with `venv-ams-life` (main e39fb76 had 1276; +21 in `tests/test_app_config.py`), the
file tests included. Golden traces unchanged.
