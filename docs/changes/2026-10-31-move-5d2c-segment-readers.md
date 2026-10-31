# Move 5d-2c: segment readers

The twelve message-part readers now use `Incoming.segments`, so they also accept a
`TurnEvent` where the rest of the method does not need AstrBot event methods.
`events.image_ref` reads image url, file, then path. Record attachments still
ignore path, while transcription still accepts it. Quote text and message_str,
quote image privacy checks, ordering and deduplication are preserved.

The adapter comparison freezes the old reply reader. The new offline tests compare
all twelve readers with the code at 82b5412, including effects and six TurnEvent
readers. No feature switch or unrelated source file was changed.

AstrBot `Nodes` has no id and `Node.id` defaults to zero. A received Node with a
nonzero id previously triggered a forward fetch; it no longer does. Received chat
records use Forward segments. This is the card's accepted behavior change.

## Test results

Each module ran separately in the sandbox:

- tests.test_segment_readers: Ran 3 tests in 0.015s | OK
- tests.test_adapter_astrbot: Ran 17 tests in 0.099s | OK
- tests.test_turn_event: Ran 5 tests in 0.003s | OK
- tests.test_incoming_text: Ran 4 tests in 0.001s | OK
- tests.test_segments_full: Ran 3 tests in 0.000s | OK
- tests.test_golden: Ran 2 tests in 3.432s | OK
- tests.test_basics: Ran 11 tests in 0.040s | OK
- tests.test_lookup_ports: Ran 5 tests in 0.005s | OK
- tests.test_message_admission: Ran 12 tests in 0.081s | OK
- tests.test_group_browse: Ran 43 tests in 0.119s | OK
- tests.test_model_ports_vision: Ran 4 tests in 0.003s | OK
- tests.test_forget_wiring: Ran 19 tests in 8.035s | OK
- tests.test_turn: Ran 10 tests in 0.001s | OK
- tests.test_selfie: Ran 46 tests in 1.866s | OK
- tests.test_browse_wire: Ran 20 tests in 2.227s | OK
- tests.test_no_numbers: Ran 15 tests in 4.225s | OK
- tests.test_stickers_wire: Ran 29 tests in 9.223s | OK
- tests.test_reply_tools: Ran 6 tests in 1.484s | OK

Outside the sandbox the same 18 modules pass one at a time with `venv-ams-life`; the golden
files and `tests/stubs` are unchanged. The new test also passes loaded together with
`test_basics` in one discover run.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
