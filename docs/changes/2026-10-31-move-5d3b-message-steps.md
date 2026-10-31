# Move 5d-3b: message steps

Move message storage and reply decisions into platform-neutral turn steps, so a
new entry point can call them without an AstrBot reply request.

`TurnMixin._on_message` keeps the original message handler body. `_decision`
keeps the original decision body, returning `"reply"` at its two request sites.
`_decide` retains its request-returning interface, and `_decide_turn` exposes the
decision. The AstrBot hooks stay in `main.py` and preserve their exception and
yield behavior. No switches or behavior were changed; no files outside the card
were changed. The method count is now 502.

The new tests compare both bodies line by line with frozen source, and cover the
old decision interface, hook outcomes, and neutral turn events. The source checks
confirmed both moved bodies match, apart from the two specified return changes.

## Test results

Each file was run separately in the sandbox:

- `tests.test_message_steps`: Ran 6 tests in 0.012s | OK
- `tests.test_basics`: Ran 11 tests in 0.044s | OK
- `tests.test_golden`: Ran 2 tests in 3.453s | OK
- `tests.test_attention`: Ran 38 tests in 5.235s | OK
- `tests.test_mood_events`: Ran 26 tests in 0.073s | OK
- `tests.test_message_admission`: Ran 12 tests in 0.081s | OK
- `tests.test_stickers_wire`: Ran 29 tests in 8.729s | OK
- `tests.test_turn_event`: Ran 5 tests in 0.003s | OK
- `tests.test_event_reads`: Ran 5 tests in 0.023s | OK
- `tests.test_discretion`: Ran 84 tests in 29.920s | OK
- `tests.test_selfie`: Ran 46 tests in 1.812s | OK
- `tests.test_group_browse`: Ran 43 tests in 0.117s | OK

Outside the sandbox the same 12 modules pass one at a time with `venv-ams-life`; the golden
files are unchanged. A script compared both moved bodies with `1cf9e62` line for line
(`_on_message` = `main.py` 597-643, `_decision` = `mixin_attention.py` 242-318 with the two
`return "reply"` lines) and the card's short pieces word for word: all the same.
`test_message_steps` compares the two kept `Incoming`s without `ts`, the time each was built.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
