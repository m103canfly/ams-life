# 2026-10-31 move 5d-1: incoming gates

The identity and addressing gates now read an `Incoming`, so they also accept a neutral
`TurnEvent`. The AstrBot adapter strips sender ID and name as the original plugin did.
`incoming_of` recognizes `TurnEvent` by type and otherwise converts the AstrBot event.
No event caching or new setting was added; message content and event actions stay in place.

For readable events the frozen old code checks the same fields and gates. An unreadable
place or self ID now becomes empty instead of raising. The plugin method count remains 499.
Only the files on the card were changed; golden files were not changed.

## Tests

Each module ran separately in the sandbox. The first `test_turn_event` run failed to import
`test_basics`; its test path setup was corrected before the successful run below.

```text
tests.test_turn_event: Ran 5 tests in 0.003s | OK
tests.test_adapter_astrbot: Ran 17 tests in 0.100s | OK
tests.test_turn: Ran 10 tests in 0.001s | OK
tests.test_ports: Ran 7 tests in 0.003s | OK
tests.test_golden: Ran 2 tests in 3.471s | OK
tests.test_basics: Ran 11 tests in 0.040s | OK
tests.test_message_admission: Ran 12 tests in 0.084s | OK
tests.test_mood_events: Ran 26 tests in 0.078s | OK
tests.test_attention: Ran 38 tests in 5.148s | OK
tests.test_discretion: Ran 84 tests in 29.208s | OK
tests.test_send_check: Ran 23 tests in 7.773s | OK
tests.test_slang: Ran 14 tests in 0.268s | OK
tests.test_group_browse: Ran 43 tests in 0.117s | OK
tests.test_selfie: Ran 46 tests in 1.841s | OK
tests.test_stage_replay: Ran 18 tests in 2.215s | OK
tests.test_vision_channel: Ran 14 tests in 0.067s | FAILED (failures=2, errors=2)
```

In `test_vision_channel`, `test_existing_daily_count_is_carried_into_ledger` and
`test_zero_price_counts_calls_without_increasing_spending` could not find `spend.json`.
`test_browse_source_is_available_to_future_callers` and
`test_thirty_first_and_hundredth_picture_call_model` saw zero calls instead of the expected
counts. The cause was not established; testing stopped as instructed on an old test failure.

The dispatcher could not make it fail again. Run alone in the same sandbox afterwards,
`test_vision_channel` passes (14 tests) on this branch and on the old code (main `6568a29`);
outside the sandbox it passes with the test Python (six runs) and with `venv-ams-life`.
The failing run took 0.067s where a passing one takes about 0.74s. It is noted for the
final round.

Outside the sandbox the 16 modules pass one at a time with `venv-ams-life`, and the golden
files are unchanged. A script took each changed file at `6568a29`, made the card's changes
and compared it with the new file: apart from the new import lines, all eight are the same.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
