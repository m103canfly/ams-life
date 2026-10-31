# 2026-10-31 — move 5d-2b full segments

The next migration needs quoted components and words, plus attachment paths, in
neutral segments. AstrBot and OneBot adapters now retain those fields. OneBot
quoted words keep their trailing space, and nested quotes are not fetched again.
Existing consumers and message text are unchanged. There is no switch, and no
files outside this card were changed.

Tests added: `test_astrbot_quote_and_paths`, `test_astrbot_unreadable_chain`,
`test_onebot_quote_and_paths`, and `test_quote_with_content_and_nested_reply`.
The cross-adapter comparison also checks segment data.

The reviewer authorized adding `path` to the two record assertions on 10-31.

Tests in the sandbox, one file at a time:

- `tests.test_segments_full`: `Ran 3 tests in 0.000s | OK`
- `tests.test_adapter_astrbot`: `Ran 17 tests in 0.100s | OK`
- `tests.test_adapter_onebot`: `Ran 35 tests in 0.002s | OK`
- `tests.test_turn`: `Ran 10 tests in 0.001s | OK`
- `tests.test_turn_event`: `Ran 5 tests in 0.004s | OK`
- `tests.test_incoming_text`: `Ran 4 tests in 0.001s | OK`
- `tests.test_golden`: `Ran 2 tests in 3.404s | OK`
- `tests.test_basics`: `Ran 11 tests in 0.039s | OK`
- `tests.test_prepare_turn`: `Ran 5 tests in 0.049s | OK`
- `tests.test_reply_handle`: `Ran 10 tests in 0.002s | OK`
- `tests.test_after_reply`: `Ran 6 tests in 1.113s | OK`
- `tests.test_messenger`: `Ran 25 tests in 0.075s | OK`
- `tests.test_onebot_messenger`: `Ran 40 tests in 0.160s | OK`

Outside the sandbox the same 13 modules pass one at a time with `venv-ams-life`; the golden
files are unchanged and no mixin or `main.py` is touched.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
