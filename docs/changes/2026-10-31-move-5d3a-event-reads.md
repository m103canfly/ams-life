# Move 5d-3a: event reads

The remaining private-chat and message identity reads now use Incoming. TurnEvent carries
the original session string so stored sessions and window lookup keep the same key.
There is no new switch. No files outside the card were changed.

For AstrBot events with matching session strings and message types, these reads agree with
the previous ones. An event without a session string is no longer treated as private even
if its `is_private_chat()` says it is. All four reads change: `_image_refs`, `_image_context`,
`_phone_context`, and `_is_private_event`. The group and guild guard remains in place.

Tests compare frozen reads with AstrBot events and TurnEvent, including identity, image
and session lookup behavior. The adapter test compares message IDs with the frozen read.
The session string added to `test_group_browse`'s `ev()` was approved in the card on 10-31.

## Test results

- tests.test_event_reads: Ran 5 tests in 0.023s | OK
- tests.test_adapter_astrbot: Ran 17 tests in 0.096s | OK
- tests.test_turn_event: Ran 5 tests in 0.004s | OK
- tests.test_segment_readers: Ran 3 tests in 0.014s | OK
- tests.test_golden: Ran 2 tests in 3.465s | OK
- tests.test_basics: Ran 11 tests in 0.040s | OK
- tests.test_group_browse: Ran 43 tests in 0.120s | OK
- tests.test_lookup_ports: Ran 5 tests in 0.004s | OK
- tests.test_model_ports_vision: Ran 4 tests in 0.003s | OK
- tests.test_message_admission: Ran 12 tests in 0.081s | OK
- tests.test_forget_history: Ran 7 tests in 0.155s | OK
- tests.test_onebot_messenger: Ran 40 tests in 0.158s | OK
- tests.test_turn_tools: Ran 10 tests in 0.012s | OK
- tests.test_ports: Ran 7 tests in 0.003s | OK
- tests.test_browse_wire: Ran 20 tests in 2.208s | OK
- tests.test_selfie: Ran 46 tests in 1.798s | OK
- tests.test_stickers_wire: Ran 29 tests in 8.577s | OK

Outside the sandbox the same 17 modules pass one at a time with `venv-ams-life`; the golden
files and `tests/stubs` are unchanged. A script took each changed mixin at `8763a44`, made the
card's changes and compared it with the new file: apart from the new import lines, all are the
same (`_message_id` keeps its try/except, as the reviewer allowed).

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
