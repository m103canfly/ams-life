# Fix one old test that still expected `her._history`

2026-11-01. The test changed; product code is untouched.

`tests/test_life_context.py`'s `test_sent_words_are_in_the_history_a_reply_reads` uses a
fake plugin (`Person`) that only carried `_history`. Since C1 a turn reads the history
through `mixin_phone.PhoneMixin._reply_context`, so the test failed with
`AttributeError: 'Person' object has no attribute '_reply_context'`. Both sides passed on
their own before; they broke once they met.

## What changed

- `Person` now takes the real `_reply_context` (and its static `_message_id`) from
  `mixin_phone.PhoneMixin` instead of a fake. `_here`, `_read_window` and `_history_store`
  were already on `Person`, and `_history_store` already returns the test's store.
- The turn runs with `time.time` patched to the test's fake clock, because `_reply_context`
  keeps only the rows of the last 24 hours. `tell_owner` writes its row at that same clock,
  so the row is inside the window whatever the real date is.
- The assertion is unchanged: the messages the model gets are her own words
  `你今天在做什么呀` first, then `在干嘛`.

## Files

- `tests/test_life_context.py`

## Tests

Run one at a time, in this sandbox:

- `tests.test_life_context`: 11 tests, every one an error in `asyncSetUp` —
  `PermissionError` on `(self.root / 'states').mkdir()` (the temp area takes one new folder
  but allows no writes inside it).
- `tests.test_basics`: 9 of 11 pass; the 2 errors are `PermissionError` on
  `STATE_DIR.mkdir` while building a plugin.
- `tests.test_golden`: 2 tests, both an error — `PermissionError` in `tempfile`.
- `tests.test_reply_context`: did not finish. It printed the first test's name and then made
  no progress for 90 s. Its setup makes a folder inside `test_basics`' own temp folder
  (`TemporaryDirectory(dir=test_basics.DATA)`), and in this sandbox that call never returns
  (a probe confirmed: a folder inside the temp folder blocks, a file there raises
  `PermissionError`).

Because of that, the fixed test was checked directly in memory (same steps, the history
store opened as `:memory:`, no file written): the store keeps
`[{'role': 'assistant', 'content': '你今天在做什么呀'}]` and the model gets
`['你今天在做什么呀', '在干嘛']`. The dispatcher runs the four files outside the sandbox.
