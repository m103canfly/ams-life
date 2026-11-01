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

- An exchange counts when someone called her in that place, that is when
  `called[here]` is newer than `quiet_seen[here]`.
- An exchange also counts when the other side spoke in the window and she has
  her own line there too, both newer than `quiet_seen[here]`. Her own lines
  alone never count, so a group where others chat, nobody calls her and she
  never answers stays quiet.
- The exchange marker is the later of her last reply and `called[here]`. That
  keeps the old rule that one exchange counts once, so a consumed line cannot
  trigger again.
- The 600-second silence check, the cooldown, `tell_owner()`, the prompts and
  the other window rules are unchanged. The wait still runs from the last
  message in the window.

## Behaviour

Before: a proactive message from her with no reply counted as a finished chat,
so the loop could repeat roughly every ten minutes. Group talk that was not
addressed to her counted as well.

After: her own message alone is not a conversation, and group chatter that
never calls her and never gets an answer is not one either. A chat where
someone called her, or where the other side spoke and she answered, counts
once, after 600 quiet seconds.

## Tests

The offline test file `tests/test_quiet_needs_them.py` uses a fake clock,
in-memory state and a fake model. Its tests:

- `test_her_own_message_alone_is_not_quiet`
- `test_their_message_and_her_reply_are_quiet_once`
- `test_called_exchange_is_quiet_once`
- `test_unaddressed_group_chatter_is_not_quiet`
- `test_her_own_line_after_a_seen_exchange_is_not_quiet`
- `test_private_exchange_is_quiet_once`
- `test_tell_owner_does_not_make_quiet_after_ten_minutes`

Result in this workspace sandbox: `Ran 7 tests in 0.016s | OK`.

Spot check: dropping the "the other side spoke" condition (the old rule, where
her last line or a call is enough) makes
`test_her_own_message_alone_is_not_quiet`,
`test_her_own_line_after_a_seen_exchange_is_not_quiet` and
`test_tell_owner_does_not_make_quiet_after_ten_minutes` fail. Letting the last
user line alone count makes `test_unaddressed_group_chatter_is_not_quiet` fail.

Other named files:

- `tests.test_tell_owner`: `Ran 7 tests in 0.071s | OK`.
- `tests.test_basics`: 9 tests passed. `test_routes_use_new_name` and
  `test_group_browsing_defaults_off` failed with `PermissionError` while
  creating their temporary data directory.
- `tests.test_life_loop` and `tests.test_golden`: they create temporary
  directories, and the sandbox denied writes inside them with `PermissionError`.
  They need the owner's outside run. The two windows tests that this card had
  broken, `test_called_group_and_only_that_places_silence` and
  `test_unaddressed_group_never_triggers`, and the private windows test
  `test_private_quiet_once_and_later_messages_delay_it` were checked by calling
  `quiet_chats` with the same fake windows and clock; all three answer as the
  tests expect.

The golden fixtures were not touched or rerecorded. No plugin method, switch,
dependency or data file changed. No commit was made. AstrBot-specific work was
left out under the owner's November 1 instruction.
