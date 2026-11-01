# Impression layers at load time

The shared person record can contain relationship text from multiple places.
Keep its existing storage and select its text when it is loaded for a reply.

- Outside the subject's private chat, remove all six text-bearing relationship
  fields from the view. Counts, names and numerical relationship state remain.
- In that private chat, match `source_ids` and `evidence_refs` against memory
  and the complete event archive. Keep a sourced item only when every matched
  source passes `recall_permission` as `SAY`; keep old items without a matched
  source. The existing group-private guard still clears `we_memory` and
  `transactive_map`. The archive scan is read-only and does not deduplicate.
- The background relationship narrative previously used unfiltered milestones.
  It now uses the same view before forming its model prompt. The relationship
  impression job already filters its event inputs through `_visible_events`,
  and its relationship input renders only numerical state.
- Group cards and existing deletion behavior are unchanged. No stored records
  are migrated, no switch or plugin method is added, and no other card scope
  is changed. AstrBot was not checked, per the 11-01 instruction.

Unmatched references are retained as requested, so missing, unreadable or
already-deleted sources cannot establish a restriction. Existing aggregate map
entries without references likewise remain in the subject's private chat.

Validation in the sandbox, one module at a time:

```text
tests.test_impression_layers: Ran 6 tests in 0.016s | OK
tests.test_golden: Ran 2 tests in 3.793s | OK
tests.test_basics: Ran 11 tests in 0.040s | OK
```

The full suite and `test_golden_standalone` were not run, as instructed.
