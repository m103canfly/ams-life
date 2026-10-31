# 2026-10-31 - move 5c-1 reply handle

Prepare reply processing for a platform-neutral turn without changing the current callers.
AstrBot's handle preserves the existing text, chain shaping, and spending rules; the neutral
handle works on `TurnReply`. The browser accepts its own normalized usage format so a second
normalization keeps the input counts. Other usage formats retain their existing behavior.

- `adapter_astrbot_turn.py`: add the AstrBot reply handle and chain builder.
- `turn.py`: add the neutral handle and the optional first message.
- `browse.py`: recognize dictionaries with exactly the three normalized usage keys.
- `tests/test_reply_handle.py`: compare the handles with the existing implementation and
  cover normalized usage, chain components, and platform independence.

There is no new switch. No callers, plugin methods, existing tests, or files outside the card
were changed. Existing AstrBot behavior is preserved by using the same operations; the new
normalized usage input now retains its input counts. Golden traces were not run or changed.

## Tests

`tests.test_reply_handle`, `tests.test_turn`, `tests.test_browse`, and `tests.test_browse_wire`:
`Ran 60 tests in 2.252s | OK`.

The same four pass outside the sandbox, in both orders, with the test Python and with
`venv-ams-life`. The blocks the card says to copy as they are were checked line for line
against main c209cf5. The full suite and the card's spot checks run once blocks 5 and 6 are
written (the owner's rule, 10-31).
