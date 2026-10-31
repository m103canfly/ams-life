# Neutral message destinations

The new entry point supplies a messenger that sends to neutral places and produces turns
without an AstrBot session string. Prefer that messenger, use the incoming place for later
messages and media, and preserve an existing window session when the new turn has none.
AstrBot events retain their existing destinations and session storage. No switch was added.
Only the files on the card were changed.
The 10-31 review amended the card to use `incoming_of(event).place` in
`mixin_selfie.py` at line 470, following the 5d-1 rule for mixin-only test doubles.

## Test results

Each file was run separately in the sandbox.

- `tests.test_send_neutral`: Ran 6 tests in 0.076s | OK
- `tests.test_basics`: Ran 11 tests in 0.040s | OK
- `tests.test_golden`: Ran 2 tests in 3.551s | OK
- `tests.test_attention`: Ran 38 tests in 5.644s | OK
- `tests.test_selfie`: Ran 46 tests in 1.803s | OK
- `tests.test_selfie_ports`: Ran 10 tests in 0.029s | OK
- `tests.test_autonomy_ports`: Ran 5 tests in 0.194s | OK
- `tests.test_ports`: Ran 7 tests in 0.003s | OK
- `tests.test_messenger`: Ran 25 tests in 0.076s | OK
- `tests.test_stickers_wire`: Ran 29 tests in 8.953s | OK
- `tests.test_forget_wiring`: Ran 19 tests in 7.765s | OK

Outside the sandbox the same 11 modules pass one at a time with `venv-ams-life`; the golden
files are unchanged and no old test was changed.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
