# A quiet chat needs the other side

## Why

`tell_owner` writes her proactive message into the owner's window as an
assistant line. `quiet_chats` took the last assistant time as the start of an
exchange, so 600 seconds after a message she sent herself the window already
looked "quiet". The life loop thought again for that reason, `tell_owner` sent
another line, and the new line started the same cycle. The 600-second cooldown
could not stop it, and her own 20–60 minute choices were cut short about every
ten minutes.

## What changed

Only `quiet_chats` in `life_loop.py` changed.

- A new exchange needs the other side to have spoken. The latest `role ==
  'user'` line in the window, or `called[here]`, must be newer than
  `quiet_seen[here]`. Her own assistant lines alone never count.
- The exchange marker written by the existing tick now covers the latest of her
  last reply, `called[here]` and the other side's last message. That keeps the
  old rule that one exchange counts once, so a consumed line cannot trigger
  again.
- The 600-second silence check, the cooldown, `tell_owner()`, the prompts and
  the other window rules are unchanged. The wait still runs from the last
  message in the window.

## Behaviour

Before: a proactive message from her with no reply counted as a finished chat,
so the loop could repeat roughly every ten minutes.

After: that message alone is not a conversation. A chat where the other side
spoke still counts once, after 600 quiet seconds, as before.

## Tests

New offline test file `tests/test_quiet_needs_them.py`, fake clock, in-memory
state and fake model:

- `test_her_own_message_alone_is_not_quiet`
- `test_their_message_and_her_reply_are_quiet_once`
- `test_called_exchange_is_quiet_once`
- `test_tell_owner_does_not_make_quiet_after_ten_minutes`

Result in this workspace sandbox: `Ran 4 tests in 0.020s | OK`.

Spot check: removing the "other side spoke" condition makes the first and the
fourth test fail; the other two keep passing.

Other named files:

- `tests.test_tell_owner`: `Ran 7 tests in 0.075s | OK`.
- `tests.test_basics`: 9 tests passed. `test_routes_use_new_name` and
  `test_group_browsing_defaults_off` failed with `PermissionError` while
  creating their temporary data directory. The method count stayed 511.
- `tests.test_life_loop`, `tests.test_golden` and
  `tests.test_golden_standalone`: they create temporary directories, and the
  sandbox denied those writes with `PermissionError`. They need the owner's
  outside run.

The golden fixtures were not touched or rerecorded. No plugin method, switch,
dependency or data file changed. No commit was made. AstrBot-specific work was
left out under the owner's November 1 instruction.
