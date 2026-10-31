# 2026-10-31 move 5e8 photo key

Photo requests use the same image service as vision. The new program now reads
the vision credential from its key store for both selfies and snapshots. A
missing or unreadable credential becomes an empty string. Without a key store,
AstrBot continues to use the image configuration credential. Voice is unchanged.

The shared lookup is a module function, so the plugin method count remains 505.
There is no new switch. The key page label can be updated in a later UI change.
Only the files named on the card were changed; golden files were not changed.

Test results (sandbox, one file at a time):

- `tests.test_selfie_key`: Ran 4 tests in 0.022s | OK
- `tests.test_selfie`: Ran 46 tests in 2.004s | OK
- `tests.test_golden`: Ran 2 tests in 4.939s | OK
- `tests.test_basics`: Ran 11 tests in 0.041s | OK

The full suite and standalone golden test were not run; they are scheduled for
the later review and outside-sandbox run respectively.
