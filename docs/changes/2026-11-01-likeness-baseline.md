# L1: reply likeness baseline

## Purpose and changes

Keep a local baseline of replies for the owner to rate before the first phase changes her behavior. This records only the reply half of the design; days of her life are deferred. No model call or new dependency is added.

The standalone turn runner calls `_keep_likeness` only after the messenger reports a successful first send. `turn_runner.py` is changed because `_keep_turn` is called after both a successful send and a caught send failure; it cannot distinguish them. The existing history call and its behavior remain unchanged. The mixin uses the existing speaking and private-message checks, restricts private samples to the owner, and checks the forget registry for each speaker. It keeps at most five preceding user lines.

`likeness.py` stores weekly samples and selections under `DATA_DIR/likeness`, alongside standalone history. `app.prepare_data` sets `DATA_DIR` from the standalone data root before loading the mixins; the same root contains `history.sqlite3`. Each ISO week holds at most 300 randomly retained samples. The first panel read chooses up to 20 and persists the choice. Later reads of the current week fill any vacant positions from unselected samples while keeping existing choices and ratings; other weeks retain their first selection. Random choices use an independent generator. The panel excludes sender IDs and place IDs and masks runs of five or more digits in displayed names and words; stored words remain original.

Forgetting a person removes matching samples and selected entries. A past week's selection is not refilled; the current week can be refilled on its next read. If likeness deletion fails, the error type is logged and the remaining deletion continues, as for history deletion. The likeness files may still contain that person's data after such a failure and require a successful retry. Likeness logs do not include chat text.

The two routes use the existing panel security: GET checks Host; POST checks Host, Origin and the token. This follows the 11-01 review clarification. `tests/test_panel_api.py` updates its two route-count assertions from 28 to 30. The plugin method count changes from 505 to 508 for `_keep_likeness` and the two page handlers. No page files were changed.

## Golden differences

The owner approved intentional re-recording. For both `basic.json` and `full.json`, the only changes from `HEAD` are two additions to `routes`:

- `/astrbot_plugin_ams_life/page/likeness`
- `/astrbot_plugin_ams_life/page/likeness/rate`

A JSON comparison against `git show HEAD:tests/golden/<name>.json` verified that all other values are unchanged. The golden test passes after removing the update variable.

The standalone comparison allows the 24 sample rows and their individual context fields only in A to B0, using a strictly formatted `<week>` placeholder. Sample IDs use a deterministic SHA-256 digest of the timestamp, place, reply and context, with a collision sequence, so B0 to B has no random ID difference.

## Test results

Each module was run separately in the sandbox; no full suite was run.

- `tests.test_likeness`: 10 tests OK, 1 skipped (aiohttp unavailable).
- `tests.test_panel_api`: 20 tests OK, 17 skipped (aiohttp unavailable).
- `tests.test_forget_wiring`: 19 tests OK.
- `tests.test_forget_history`: 7 tests OK.
- `tests.test_keep_turn`: 8 tests OK.
- `tests.test_golden`: 2 tests OK after re-recording.
- `tests.test_basics`: 11 tests OK, including the 508-method assertion.

The aiohttp panel security test and `tests.test_golden_standalone` require the owner's outside environment.
