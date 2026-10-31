# 2026-10-31 move 7d-2: prefixes of one account

The same account can have both `ams-life` and `default` prefixes. The former is the
current AstrBot platform name; the latter comes from the group browse substitute event
and older records made when the platform name was `default`. Both can describe the same
place. The owner must approve merging these prefixes before the tool is run on the copy.

## What changed

- `--same-account ams-life,default` explicitly lists prefixes of one account. An observed
  prefix outside the list stops the run before writing. `--check` accepts the same option.
- Without the option, the existing multiple-prefix stop remains unchanged. The event merge,
  deduplication and conflict rules remain unchanged.
- With the option, an explicitly listed prefix that looks like a neutral place prefix, such
  as `other:GroupMessage:...`, is recognized as an old session and converted as well.
- Tests use invented data and temporary directories. No files outside this card were changed.

## Checked

- `tests.test_rename_places`: 13 tests passed.
- `tests.test_golden`: 2 tests passed; golden files unchanged.
- `tests.test_basics`: 11 tests passed; the 505 method count is unchanged.
- The full suite is deferred under the current testing rule.
