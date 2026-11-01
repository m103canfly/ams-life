# Life choices see the chat with him

Card 1c-5. She used to decide what to do next from her body, the moment and
today's activities only, so she could not tell what he had just said to her,
and asked him again and again. Now the material for that choice also holds the
recent private chat with him and the "things I want to do" lines of her
notebook. The card names this file; no golden fixture was re-recorded.

## What changed

- `life_loop.py` reads his private window for the last 24 hours, at most 200
  lines, both sides, with the time and who said it (`11-01 21:40 她：…` /
  `11-01 21:52 家人：…`). The phone already keeps 24 hours, others' lines at 300
  characters and hers at 80; they are shown as stored. "最近没聊" when empty.
  The same two materials (the chat and the notebook's "想做的" lines) are added
  to the material of the heybox call too. The notebook lines are filtered with
  the existing recall wall for his private chat, so an entry that may only be
  told in another private chat is left out; a public one enters anonymized.
- Writing a public line is its own call now (`post_materials` /
  `parse_post` / `write_post`). The choice prompt no longer asks for `post`. The
  second call sees today's activities, the weather, her body and the reason,
  never the chat and never the `此刻` line. So a private chat cannot reach a
  public line through this path.
- `detail`, `liked_last`, `look` and the heybox `thought` are checked against
  the chat lines shown this time before they go anywhere public, with the
  non-model layer of `send_check.check` (the same "forbidden" list `tell_owner`
  builds). A hit drops the field: `detail` and `liked_last` are empty, `doing`
  falls back to `do`, `look` is not set, `thought` is not stored.
  `send_check.check` compares four characters in a row; the review's example
  ("在担心明天去医院" against "明天去医院复查") shares "明天去医院", so it is
  caught. `says_private` uses only `send_check.check`: a shorter repeat of two
  pairs was tried in the first version and removed. Short two-character words
  ("今天", "一下", "有点") are everywhere in 200 lines, so her own words were
  dropped too. `send_check.py` itself is unchanged.
- The prompts no longer nag: the unanswered count and "想和…说什么就在 tell 写
  一句" are gone. The JSON asks for `tell` and one neutral line remains
  ("要是想跟…说点什么就写在 tell，不写也行") only when
  `proactive_owner_enabled` is on. With the switch off she is not asked for
  `tell` at all (in `materials` and in `heybox_ask_prompt`), because a `tell`
  would not be sent and she would think she had spoken. The parsers still accept
  `tell` and the older `tell_owner`; `tell_owner` itself checks the switch.
- `tell_owner` now writes what was actually sent into the reply history as well
  (`private:<him>`, role assistant, about him, no sources: she wrote it
  herself), through one small function `keep_sent` that later proactive sends
  (for example a shared song) can use too. The send checks, switches, the 8-yuan
  line and the "do not look for him while asleep" rule are untouched; no cap on
  how often she may write was added.

## Behaviour

The choice now sees the recent chat and her "want to do" list, so it can weigh
by itself whether to say something. Anything drawn from the shown chat is kept
out of the public outputs. The number of life calls can rise by one when she
chooses `发说说`; the daily 8-yuan line and the 48-thought cap are unchanged.
Goldens needed no change: `life_loop` is not part of the golden scenarios, and
`_keep_turn` is unchanged (the new history line is written only by `tell_owner`).

## Tests

New file `tests/test_life_context.py` (eleven tests: the seven card tests 1-6
and 8, plus the four the review asked for): the chat with time and speaker; the
JSON has `tell` and no `post`, and no nag; `发说说` as a second call without the
chat or the `此刻` line; a leaking `detail` dropped and an unrelated one kept;
a heybox `thought` repeating the chat not stored while a clean one is; only
"想做的" lines that may be told in his private chat; after `tell_owner` the
assistant line is in `history_store.recent(...)` and the next turn's model
history holds it; `tell` absent from `materials` with `proactive_owner_enabled`
off and present with it on; the same for `heybox_ask_prompt`; a line 25 hours
old dropped and a line 23 hours old kept; 250 lines in the window only the last
200 shown.

The leaking `detail` and `thought` examples repeat four characters in a row of
his line ("在担心明天去医院" against "明天去医院复查"), so
`send_check.check` alone catches them.

Old tests that asserted exactly the replaced prompt were updated in that
assertion only:

- `tests/test_tell_owner.py` (`test_materials_show_unanswered_count`): asserts
  the count line is absent and the neutral line is present.
- `tests/test_owner_name.py` (`test_default_name_everywhere_and_no_owner_word`,
  `test_the_setting_is_used_everywhere`): the count/nudge assertions became the
  neutral line, for the owner name and for its default.
- `tests/test_heybox.py` (`test_browse_limits_budget_and_excludes_names`): the
  count line is gone from the heybox prompt; it now carries the chat block.
- `tests/test_life_loop.py` (`test_anonymization_and_forget`): `related_users`
  no longer includes the people named only in `post`, because the public line is
  written in its own call and only for `发说说`.

Both prompt tests above keep `proactive_owner_enabled` on, so the neutral line
is still asked for.

## Test runs in this sandbox

Python cannot write under the session's temporary area here
(`PermissionError: [WinError 5]`), so every test that creates its own data
directory stops before it can assert anything. Attempted after the rework, one
file at a time:

- `python -m unittest tests.test_tell_owner` — Ran 7 tests, `OK` (it needs no
  data directory).
- `python -m unittest tests.test_life_context` — 11 tests, 22 errors (the setUp
  and its cleanup of each one), all PermissionError.
- `python -m unittest tests.test_life_loop` — 41 tests, 78 errors, all
  PermissionError on `TemporaryDirectory()`.
- `python -m unittest tests.test_heybox` — 29 tests, 39 errors, 1 skipped, all
  the errors PermissionError.
- `python -m unittest tests.test_owner_name` — 22 tests, 2 errors, both
  PermissionError in `HerStickers`; the other classes ran.
- `python -m unittest tests.test_qzone` — 6 tests, 12 errors, all
  PermissionError.
- `python -m unittest tests.test_send_walls` — 10 tests, 20 errors, all
  PermissionError.
- `python -m unittest tests.test_basics` — 11 tests, 2 errors, both
  PermissionError in `STATE_DIR.mkdir`.
- `python -m unittest tests.test_golden` — 2 tests, 2 errors, all
  PermissionError.
- `python -m unittest tests.test_golden_standalone` — 6 tests, 4 errors, all
  PermissionError.

No assertion failed anywhere: every error is the sandbox denying the data
directory. The full suite was not run. Pure in-memory checks (import and
helpers, no data directory) passed: a dropped leaking `detail` with the new
four-character example, the kept unrelated one, the short two-pair repeat kept
(so her own words are not dropped), `materials()` and `heybox_ask_prompt()` with
`proactive_owner_enabled` off and on, the 25-hour line dropped and the 23-hour
line kept, 250 lines cut to the last 200, and both parsers still reading `tell`.

## Unsure about

- The current notebook writer does not store a `section` field; only imported or
  older entries carry one. The "想做的" selection uses
  `her_days.notebook_sections` as the card says, so today it may find nothing
  until the notebook writes sections.
- Card line numbers had moved (`materials()` and the others are further down
  now); the work was done at the current place.

`owner_unanswered()` and the test that covers it are still there: the review
said either way is fine, and leaving them keeps the change small. `keep_sent()`
is the module function the review allowed.

No plugin methods, switches, dependencies, golden fixtures or other files were
added or changed. Nothing outside this folder was read; no commit.
