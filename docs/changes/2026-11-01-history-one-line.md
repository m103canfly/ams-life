# 2026-11-01: Assistant history on one line

## Why and what

Earlier multi-message replies can encourage the model to repeat that shape. During turn preparation, join ordinary assistant history lines with spaces, including text parts in list content. Keep newlines inside fenced code and list blocks. User history keeps its existing framing.

The `history_one_line` switch defaults to on. Turn it off to pass assistant history through unchanged; restart the new program after changing the setting.

The new program changes the model's copy only; HistoryStore keeps the original lines. AstrBot 4.29.3 internal.py writes back history at the end of the turn, so its saved assistant history also becomes one line, like the existing user history framing.

The configuration schema was also changed for the switch. The golden files and standalone golden table were not changed.

## Tests

The full suite and `test_golden_standalone` were not run, as instructed. Each targeted file passed separately:

- `tests.test_history_one_line`: 4 tests in the first pass; switch tests added afterwards.
- `tests.test_prepare_turn`: 5 tests.
- `tests.test_turn_runner`: 9 tests.
- `tests.test_attention`: 38 tests.
- `tests.test_golden`: 2 tests.
- `tests.test_basics`: 11 tests; the plugin method count remains 505.

After adding the switch, separate runs passed: `tests.test_history_one_line` (6), `tests.test_prepare_turn` (5), `tests.test_golden` (2), `tests.test_basics` (11), `tests.test_app_config` (22), `tests.test_migrate_config` (9), `tests.test_interactive_browser` (60), and `tests.test_real_browser` (56).
