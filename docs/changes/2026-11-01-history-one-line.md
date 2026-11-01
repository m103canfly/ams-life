# 2026-11-01: Assistant history on one line

## Why and what

Earlier multi-message replies can encourage the model to repeat that shape. During turn preparation, join ordinary assistant history lines with spaces, including text parts in list content. Keep newlines inside fenced code and list blocks. User history keeps its existing framing. This has no new setting.

The new program changes the model's copy only; HistoryStore keeps the original lines. AstrBot 4.29.3 internal.py writes back history at the end of the turn, so its saved assistant history also becomes one line, like the existing user history framing.

Only the files named on the card changed. The golden files and standalone golden table were not changed.

## Tests

The full suite and `test_golden_standalone` were not run, as instructed. Each targeted file passed separately:

- `tests.test_history_one_line`: 4 tests.
- `tests.test_prepare_turn`: 5 tests.
- `tests.test_turn_runner`: 9 tests.
- `tests.test_attention`: 38 tests.
- `tests.test_golden`: 2 tests.
- `tests.test_basics`: 11 tests; the plugin method count remains 505.
