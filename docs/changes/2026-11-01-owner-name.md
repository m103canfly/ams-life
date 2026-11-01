# What she calls him: the `owner_name` setting

Status on 2026-11-01: card P2 (审核 v5) is implemented on `dsh-move-p2`, cut from main
`4e27138`. No commit. The goldens are unchanged. The full suite is not run here; the
dispatcher runs it outside.

## Why

On 11-01 evening the owner said that he and she stand as equals, family and friends, and
that she is to call him by his name rather than "主人". A public repository cannot hold his
real name or nickname, so the code keeps one setting and one neutral default; the real name
is written into the run folder's `config.json` on the day it is set up.

## The setting

- `_conf_schema.json` adds `owner_name`: a string, description "她怎么称呼你", default
  "家人".
- It is read like the other settings, from the plugin's configuration: a setting that is
  missing, empty, only whitespace, or longer than 12 characters gives the default.
- `interpretation.owner_name(config)` reads it; `interpretation.owner_display_name(value)`
  cleans one value (one line, at most 12 characters, else "家人"). Every other module uses
  those two functions, so there is one default and one rule.
- Install day (Codex调度): back up the run folder's `config.json`, then write `owner_name`
  into it (the discussion gives the wording); `persona.md`'s "主人" is changed by the
  discussion's plan, with a backup first.

## What changed

- `interpretation.py`: the two helpers above; `render_compact` takes `owner_name` and
  writes "[<name>定的规矩]" instead of "[主人定的规矩]".
- `life_loop.py`: the life-choice prompt and the Heybox prompt say "<name>还没回的有 N 条"
  and "想和<name>说什么"; the JSON key she is asked for is `tell` (no more `tell_owner`
  written as an English key in a Chinese prompt). Both keys are parsed, new first, old
  second, in `parse()` and `heybox_impression()`. The internal Python name `tell_owner`
  stays (a variable name, not shown to her). The Heybox prompt moved into
  `heybox_ask_prompt(plugin, readings)` so it can be checked without a network call; that
  is a module function, not a plugin method.
- `mixin_phone.py`: the phone line labels the owner with "（<name>）" and everyone else
  with "（别人）". The old-label regex in `_history_original` accepts the old "（主人）" /
  "（非主人）" records, "（别人）", and any short label (1–16 characters), because the new
  label carries a name that is config-dependent and this function has no config.
- `mixin_selfie.py`: "这里只能在和<name>的私聊里记。" and the `remember_day` tool
  description "记下你和<name>之间重要的日子。".
- `stickers.py`: `Library.add` takes `owner_name`; when the owner gives a picture with no
  note and no look caption, the new caption is "<name>给的". `OWNER_LABEL` stays
  "主人给的" for the page's "from" column, and captions already stored as "主人给的" are
  not migrated (this card does not migrate data).
- `mixin_stickers.py`: the owner's page-add passes "<name>给的" as the note when he wrote
  none.
- `impressions.py`: "主人" stays in `GENERIC_ALIASES`; `check_alias` takes `owner_name`
  and blocks the setting's value as a name, too (the default name "家人" is blocked by
  default).

## Behaviour that stays the same

- The panels (`pages/`) keep their 5 "主人" places; the card leaves them for a separate UI
  card.
- `owner_qq`, the variables and function names with "owner", the English comments and the
  persona file are not touched.
- The goldens: `tests/golden/` has no "主人", no "tell_owner" and no rules line, and this
  change writes none of those into a prompt that a golden records. `git status` shows no
  change under `tests/golden/`.

## Two callers outside this card's file list

`render_compact` and `check_alias` take the name as an argument (`owner_name=`). Their
production callers are `mixin_turn.py` (one keyword at the `render_compact` call) and
`mixin_impressions.py` (pass the setting into `nightly`). Those two files are not in the
card's list, so they were not changed. Until a follow-up card adds that one call each, those
two places show the default "家人" and never "主人"; the rest of the places read the setting.
This is flagged for review.

## Old tests updated (only the assertions with the changed wording)

- `tests/test_owner_rules_copy.py`: "[主人定的规矩]" → "[家人定的规矩]" (2 lines).
- `tests/test_body_heart.py`: the rules line assertion → "[家人定的规矩]".
- `tests/test_tell_owner.py`: "主人还没回的有 3 条" → "家人还没回的有 3 条".
- `tests/test_heybox.py`: the same prompt assertion → "家人还没回的有 3 条".
- `tests/test_jailbreak_boundaries.py`: "Alice（非主人）" → "Alice（别人）"; and the
  negative case "主人（主人）" → "主人（家人）".
- `tests/test_reply_provenance.py`: the phone labels in the expected prompts
  ("（非主人）" → "（别人）", "（主人）" → "（家人）"); a "（主人）" inside a user's own
  text stays as the user wrote it.

No other old test was changed.

## New test file

`tests/test_owner_name.py` (16 tests), offline, every name and number in it made up
("阿柚", 家人, 10001, 10003). It checks: the schema entry and the default; a blank, a
whitespace-only and a too-long setting giving the default; every place she sees (rules
line, life materials, Heybox prompt, the private-chat answer and tool description, the
phone labels, the sticker caption) with the setting empty and set, and that none of them
says "主人"; the old and new phone-record labels being recognised; `tell` and `tell_owner`
both parsed; the sticker page passing "<name>给的"; old "主人给的" captions kept; and the
setting's name being a stopword.

## Tests run here, one file at a time

The sandbox this was built in cannot write files below the OS temp directory
(`PermissionError`, WinError 5), so only tests that do not write can finish here. No
assertion about the changed wording failed; every error below is that `PermissionError`,
and the few `test_selfie` failures are tests whose setup could not write its temp data.

- `python -m unittest tests.test_owner_name`: Ran 16, 14 passed. The 2 sticker-caption
  tests error on the temp write; the same two were run with the file writes stubbed out
  (probe only, nothing added) and both passed. One earlier revision had more write-bound
  tests; those were rewritten to use fakes, so 14 of 16 now run here.
- `python -m unittest tests.test_tell_owner`: OK (7 tests).
- `python -m unittest tests.test_message_steps` and `tests.test_incoming_text` (the
  phone-window files): OK, no errors.
- `python -m unittest tests.test_basics`: 11 tests, 2 errors (plugin creation writes
  `states/`); the method count (511) and the schema checks pass.
- `python -m unittest tests.test_life_loop`: 41 tests, 78 errors, all `PermissionError`.
- `python -m unittest tests.test_selfie`: 46 tests, 67 errors and 9 failures, all from the
  unwritable temp data dir (`_tool_set_now` returning "不能更新此刻" and the like).
- `python -m unittest tests.test_stickers`: 22 tests, 11 errors, all `PermissionError`.
- `python -m unittest tests.test_impressions`: 28 tests, 13 errors, all `PermissionError`.
- `python -m unittest tests.test_app_config`: the schema classes pass (`RealSchema`,
  `Defaults`); the temp-file classes cannot finish here (the sandbox blocks temp writes,
  and the run does not terminate).
- `python -m unittest tests.test_owner_rules_copy`, `tests.test_reply_provenance`,
  `tests.test_jailbreak_boundaries`, `tests.test_body_heart`: errors only, all
  `PermissionError`.
- `python -m unittest tests.test_golden` and `tests.test_golden_standalone`: cannot run
  here (temp writes); the goldens were not touched.

The dispatcher runs the full suite and the golden files outside.
