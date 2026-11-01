# Event source check text

Event source checks previously converted entire memory entry dictionaries to strings.
Metadata could therefore supply characters that were absent from the source text.
The event archive now uses each dictionary's `text`, defaulting to an empty string,
and retains string conversion for non-dictionary entries. The other source check
continues to receive its existing text list. No plugin methods were added.

The check's `overlap` measures the fraction of event characters found in sources;
removing metadata can lower it and can change confidence. `coverage` instead
measures the fraction of source characters found in the event, so it can rise.
In the recorded scenarios below it rose, and confidence did not change.

The golden files were deliberately regenerated with `AMS_UPDATE_GOLDEN=1`.
`basic.json` did not change. The complete changes in `full.json` are:

| JSON path prefix | coverage | length_ratio |
| --- | --- | --- |
| `files.archives/events.jsonl[1].source_check` | 0.2 → 1.0 | 0.007 → 1.05 |
| `files.archives/events.jsonl[3].source_check` | 0.237 → 1.0 | 0.01 → 1.0 |
| `files.archives/events.jsonl[4].source_check` | 0.179 → 1.0 | 0.006 → 1.0 |
| `files.archives/sessions/group_900001/events.jsonl[1].source_check` | 0.237 → 1.0 | 0.01 → 1.0 |
| `files.archives/sessions/group_900001/events.jsonl[2].source_check` | 0.179 → 1.0 | 0.006 → 1.0 |
| `files.archives/sessions/private_10001/events.jsonl[1].source_check` | 0.2 → 1.0 | 0.007 → 1.05 |
| `page_status.data.events[0].source_check` | 0.179 → 1.0 | 0.006 → 1.0 |
| `page_status.data.events[1].source_check` | 0.237 → 1.0 | 0.01 → 1.0 |
| `page_status.data.events[3].source_check` | 0.2 → 1.0 | 0.007 → 1.05 |

Validation: `tests.test_source_check_text`, `tests.test_model_ports_text`, and
`tests.test_basics` passed. `tests.test_golden` initially failed for `full`,
then passed after regeneration; the regeneration run skipped both cases as
designed. The full suite and `tests.test_golden_standalone` were not run, as
directed. No files outside the requested change set were intentionally edited.
