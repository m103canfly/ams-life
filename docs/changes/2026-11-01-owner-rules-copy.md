# 2026-11-01: Hold copied owner rules

## Why and what

Owner rules remain in every reply prompt, with an instruction to follow them without reciting or listing them. Empty rules still produce no prompt line.

The module-level check in `mixin_turn.py` holds a reply when any twelve consecutive characters match one rule after whitespace and punctuation are removed. It checks the final text after the optional global memory look, clears the phone queue, stops the event, and records only `rule_copy` and a generic log message. It runs whether global memory is on or off. Rule storage and the panel are unchanged; there is no new switch or plugin method.

## Tests

Separate runs passed: `tests.test_owner_rules_copy` (6), `tests.test_send_check` (23), `tests.test_prepare_turn` (5), `tests.test_golden` (2), and `tests.test_basics` (11). The plugin method count remains 508. The golden files were unchanged. The full suite was not run; the standalone golden test is reserved for the owner.
