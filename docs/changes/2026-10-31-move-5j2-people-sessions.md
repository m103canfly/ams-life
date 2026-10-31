# Move 5j-2: neutral people sessions

People records now store the current neutral place in `sessions`. When a person
speaks again, older spellings of that same place are removed before it is added
at the end. The existing limit of 20 entries remains. Dashboard relationship rows
normalize older session strings and deduplicate them in first-seen order.
Other stored entries are left as they are until their place is visited again.

The two golden traces were regenerated once for the intentional `sessions`
change. The test diff showed only session values changing before the update.
The owner will compare the old and new traces. No feature switch or plugin
method was added. No files outside the authorized scope were changed.

## Test results

Each module ran separately in the sandbox with the prescribed test runner.

- `tests.test_people_sessions`: Ran 4 tests in 0.056s | OK
- `tests.test_basics`: Ran 11 tests in 0.049s | OK
- `tests.test_golden` (update): Ran 2 tests in 3.644s | OK (skipped=2)
- `tests.test_golden` (normal): Ran 2 tests in 3.668s | OK
- `tests.test_group_browse`: Ran 43 tests in 0.126s | OK
- `tests.test_migrate_data`: Ran 12 tests in 0.213s | OK
- `tests.test_neutral_session`: Ran 7 tests in 0.072s | OK
- `tests.test_no_numbers`: Ran 15 tests in 4.496s | OK
- `tests.test_stage_replay`: Ran 18 tests in 2.359s | OK

Golden traces, re-recorded once with `AMS_UPDATE_GOLDEN=1`. Compared with `269cd7a` outside the
sandbox: only `sessions` lists differ (10 in basic.json, 10 in full.json: the five `users/*.json`
files and the panel's `relationships` rows), and every new list is the old one with each item
made `discretion.place_of` (`default:GroupMessage:900001` -> `group:900001`,
`default:FriendMessage:10001` -> `private:10001`). Nothing else differs. Outside the sandbox
the same 8 modules pass one at a time with `venv-ams-life`.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
