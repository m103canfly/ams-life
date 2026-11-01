# What she calls him: the `owner_name` setting

Status on 2026-11-01: card P2 (审核 v5), rework round 1 after the first review. Implemented
on `dsh-move-p2`, cut from main `4e27138`. No commit. The goldens are unchanged. Two files
outside the card's list got one change each (allowed by the review: the two callers below).
The full suite is not run here; the dispatcher runs it outside.

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
  with "（别人）". The old-label regex in `_history_original` is narrowed (review, round 1):
  it accepts only the old "（主人）" / "（非主人）" records, "（别人）" and the setting's own
  name, escaped with `re.escape`. Nothing wider, so a message from outside that only looks
  like one of our framed records is marked "（历史消息，发言人和时间未核实）" as before.
  That check is called without the config, so `_phone_line` (which has it) keeps the
  setting's name in a module-level variable, and `_history_original` uses it when no name is
  given; the function also takes `owner_name` explicitly. The phone line runs before the
  history is framed in the same turn (`_prepare_turn`), so the name is the current setting's.
- `impressions.py`: "主人" stays in `GENERIC_ALIASES`; `check_alias` takes `owner_name`
  and blocks the setting's value as a name, too (the default name "家人" is blocked by
  default). `nightly` and `parse_answer` take `owner_name` and hand it to `check_alias`, so
  the night's answer never keeps the setting's name as somebody's alias.
- `mixin_selfie.py`: "这里只能在和<name>的私聊里记。" and the `remember_day` tool
  description "记下你和<name>之间重要的日子。".
- `stickers.py`: `Library.add` takes `owner_name`; when the owner gives a picture with no
  note and no look caption, the new caption is "<name>给的". `OWNER_LABEL` stays
  "主人给的" for the page's "from" column, and captions already stored as "主人给的" are
  not migrated (this card does not migrate data).
- `mixin_stickers.py`: the owner's page-add passes "<name>给的" as the note when he wrote
  none.

## Behaviour that stays the same

- The panels (`pages/`) keep their 5 "主人" places; the card leaves them for a separate UI
  card.
- `owner_qq`, the variables and function names with "owner", the English comments and the
  persona file are not touched.
- The goldens: `tests/golden/` has no "主人", no "tell_owner" and no rules line, and this
  change writes none of those into a prompt that a golden records. `git status` shows no
  change under `tests/golden/`.

## The two callers the first review named (one change each)

`render_compact` and `check_alias` take the name as an argument (`owner_name=`). Their
production callers were missing it; the review allowed one change in each of those two files,
and those are the only changes there:

- `mixin_turn.py`: the `render_compact` call passes
  `interpretation.owner_name(self.config)`, so the block every reply carries says
  "[<name>定的规矩]" instead of "[家人定的规矩]".
- `mixin_impressions.py`: the `impressions.nightly` call passes the same, and `nightly` hands
  it to `parse_answer` and on to `check_alias`; the setting's name is a stopword at night.

`impressions.py` is a file of the card, so `nightly`/`parse_answer` there take the new
keyword (`""` keeps the old behaviour for every other caller).

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

`tests/test_owner_name.py` (22 tests), offline, every name and number in it made up
("阿柚", 家人, 10001, 10003). It checks: the schema entry and the default; a blank, a
whitespace-only and a too-long setting giving the default; every place she sees (rules
line, life materials, Heybox prompt, the private-chat answer and tool description, the
phone labels, the sticker caption) with the setting empty and set, and that none of them
says "主人"; `tell` and `tell_owner` both parsed; the sticker page passing "<name>给的";
old "主人给的" captions kept; and the setting's name being a stopword.

For rework round 1 it also checks the production callers, without writing a file:

- `_prepare_turn` itself (the real `mixin_turn`, on a stand-in for the plugin whose other
  methods answer "nothing") puts "[阿柚定的规矩]" into the block a reply is built from, and
  "[家人定的规矩]" when the setting is empty;
- `_maybe_update_impressions` gives the setting to `impressions.nightly`;
- the night's answer does not keep "阿柚" as anyone's alias (a made-up store in memory);
- the framed-record check keeps （主人）/（非主人）/（别人）/（<the setting's name>） and does
  not keep （随便谁）; a name that is not the setting's is not a label either; and the phone
  line keeps the setting's name for that check.

## Tests run here, one file at a time (rework round 1)

The sandbox cannot create the plugin (its first write is `states/` under the OS temp
directory) and cannot write temp files at all (`PermissionError`, WinError 5). So the
files that build a plugin or a temp directory cannot finish here; that is the sandbox, not
the change. No assertion failed in any file that could run. Only the files the review named
were run.

- `python -m unittest tests.test_owner_name`: Ran 22, 20 passed. The 2 sticker-caption
  tests error on the temp write (the same two as last round). The new tests all pass,
  including `_prepare_turn` through the real `mixin_turn` and the night's aliases.
- `python -m unittest tests.test_turn_tools`: OK (10 tests).
- `python -m unittest tests.test_basics`: Ran 11, 2 errors (plugin creation writes
  `states/`); the method count (511) and the schema checks pass.
- `python -m unittest tests.test_impressions`: Ran 28, 15 passed, 13 errors, all
  `PermissionError` from `tempfile` (the same 13 as last round; the `parse_answer` checks
  pass).
- `python -m unittest tests.test_owner_rules_copy`: Ran 6, 6 errors, all `PermissionError`
  (the plugin cannot be created).
- `python -m unittest tests.test_reply_provenance`: Ran 7, 7 errors, all `PermissionError`
  (the plugin cannot be created).
- `python -m unittest tests.test_jailbreak_boundaries`: Ran 7, 14 errors (set-up and
  tear-down), all `PermissionError`.
- `python -m unittest tests.test_golden`: Ran 2, 2 errors (the temp directory cannot be
  made); the goldens were not touched.

The dispatcher runs the full suite and the golden files outside.
