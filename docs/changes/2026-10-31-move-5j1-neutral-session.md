# Move 5j-1: neutral event sessions

The owner decided on October 31 that stored chat identities should use neutral places.
Event sessions and provenance now use `group:` or `private:` places. Canonical
comparison also recognizes older AstrBot session strings. Event lookup, duplicate
detection, deletion propagation, and daily digests use the neutral place. AstrBot
API connections and window `umo` remain unchanged. No plugin methods were added.

The two golden traces were regenerated once with `AMS_UPDATE_GOLDEN=1` for the
intentional session-field change. The owner will compare the old and new traces.
No feature switch was added. No files outside the card's scope were changed.

**Installation must run migration 7d before starting the new code.** Otherwise the
new code cannot find events in the old session folders.

## Test results

Each module ran separately in the sandbox with the prescribed test runner.

- `tests.test_neutral_session`: Ran 7 tests in 0.070s | OK
- `tests.test_golden` (update): Ran 2 tests in 3.609s | OK (skipped=2)
- `tests.test_golden` (normal): Ran 2 tests in 3.472s | OK
- `tests.test_basics`: Ran 11 tests in 0.049s | OK
- `tests.test_digest`: Ran 27 tests in 3.707s | OK
- `tests.test_discretion`: Ran 84 tests in 31.139s | OK
- `tests.test_forget_wiring`: Ran 19 tests in 8.141s | OK
- `tests.test_forget_history`: Ran 7 tests in 0.152s | OK
- `tests.test_brain_data`: Ran 27 tests in 10.005s | OK
- `tests.test_brain_panel`: Ran 14 tests in 6.338s | FAILED (errors=1). `InTheShell.setUpClass` requires the real browser environment; its subprocess produced no output in the sandbox.
- `tests.test_message_admission`: Ran 12 tests in 0.087s | OK
- `tests.test_event_reads`: Ran 5 tests in 0.026s | OK
- `tests.test_reply_tools`: Ran 6 tests in 1.522s | OK

Golden traces, re-recorded once with `AMS_UPDATE_GOLDEN=1` (the owner's decision, 10-31: all her
data uses neutral names). Compared with `dd9eb31` outside the sandbox:
- every changed `session` value is `discretion.place_of` of the old one (basic.json 94, full.json
  134): `default:FriendMessage:10001` -> `private:10001`, `default:GroupMessage:900001` ->
  `group:900001`, `default:GroupMessage:900002` -> `group:900002`;
- the two event folders are renamed with them (`default_FriendMessage_10001` -> `private_10001`,
  `default_GroupMessage_900001` -> `group_900001`); inside them only `session` and the
  `coverage` below differ;
- in full.json, `source_check.coverage` of three events moves (0.197 -> 0.2, 0.23 -> 0.237,
  0.172 -> 0.179, and the same three in `page_status`). `_source_check` is given
  `str(entry)` of each source entry (mixin_events 2172), and the entry's
  `provenance.session` is part of that text: the shorter neutral name leaves fewer source
  characters. overlap, novelty, length_ratio and status are unchanged;
- nothing else differs.

Outside the sandbox the same 12 modules pass one at a time with `venv-ams-life` (the browser
tests of `test_brain_panel` too).

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
