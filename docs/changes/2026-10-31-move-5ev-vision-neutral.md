# 2026-10-31 — move 5e-v vision

The neutral program has no AstrBot provider to ask and stores vision credentials separately.
When `_neutral_model` is present, vision routing uses `ImageAPI` and still requires a configured
vision model. When `_key_store` is present, `ImageAPI` reads its `vision` key; a store error sends
an empty key and preserves the existing request failure handling. The slang image model uses the
same adapter. Without these attributes, AstrBot routing and configuration keys are unchanged.
There is no new configuration switch.

## Files

- `mixin_llm.py`, `vision.py`: routing and key selection.
- `tests/test_vision_neutral.py`: offline routing, key, slang model and import checks.
- `docs/changes/2026-10-31-move-5ev-vision-neutral.md`: this note.

No files outside the card were changed.

## Test results

Each file ran separately in the sandbox:

- `tests.test_vision_neutral`: Ran 8 tests in 0.010s | OK
- `tests.test_basics`: Ran 11 tests in 0.041s | OK
- `tests.test_golden`: Ran 2 tests in 3.609s | OK
- `tests.test_vision_channel`: Ran 14 tests in 0.745s | OK
- `tests.test_vision_provider`: Ran 6 tests in 0.000s | OK
- `tests.test_model_ports_vision`: Ran 4 tests in 0.003s | OK
- `tests.test_slang`: Ran 14 tests in 0.269s | OK
- `tests.test_group_browse`: Ran 43 tests in 0.118s | OK

Outside the sandbox the same 8 modules pass one at a time with `venv-ams-life`; the golden
files are unchanged.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
