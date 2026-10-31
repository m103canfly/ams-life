# Move 5e-5a: one neutral turn

## Why

The new program needs the turn sequence that AstrBot currently provides.

## Changes

Add a neutral turn runner and offline tests. It gates messages through her decision,
prepares the request and tools, calls the neutral model, shapes and sends the reply,
and keeps history. Reply usage is counted once by her existing after-reply hook.
The runner adds no switches and does not change the plugin or golden files.

## Test results

Each module ran separately in the sandbox:

- tests.test_turn_runner: Ran 9 tests in 6.464s | OK
- tests.test_basics: Ran 11 tests in 0.040s | OK
- tests.test_golden: Ran 2 tests in 3.508s | OK
- tests.test_her: Ran 5 tests in 0.152s | OK
- tests.test_fakes: Ran 15 tests in 0.005s | OK (skipped=5)
- tests.test_tool_loop: Ran 16 tests in 0.029s | OK
- tests.test_keep_turn: Ran 8 tests in 0.216s | OK
- tests.test_send_neutral: Ran 6 tests in 0.074s | OK

The five FakeNapCat server tests skipped because aiohttp is not installed. The new
turn tests use the fake DeepSeek client without the OpenAI SDK and do not skip.

Outside the sandbox the same 8 modules pass one at a time with `venv-ams-life` (`test_fakes`
in full: 15 tests); the golden files are unchanged.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
