# 2026-11-02 记1: keep every memory; the hot/cold tier works; lost ones come back from a copy

Card 记1 (the urgent one). Only `mixin_memory.py`, the new `tools/restore_memory.py`, the
new `tests/test_keep_memory.py` and this note. `memory_meta.py`, `body.py` and `life_loop.py`
are not touched; `memory_meta.memory_tier` and `select_top` are used as they are.

## Why nothing is cut for room any more

`_trim_memory` cut a place's memories to its last 80 entries, or to its last 200
unsummarized ones while compression was on. It was called after every stored message, her
reply and consolidation, and `_save_memory` then wrote the cut list as that place's whole
list; `_write_library`'s `store.keep_only(...)` dropped the vectors of the entries that
went. A cut memory was gone, vector and all, with nothing left to restore it from.

Now both cuts are gone: `_trim_memory` keeps its place in the flow and only settles the
order by time. There is no new cap. A memory is kept until the owner deletes it or the
forget registry rules it out.

## Why the hot/cold tier did nothing, and how it is worked out now

`memory_tier` was written once, as `"hot"`, when a memory was stored; only the merge path
of a duplicate worked it out again, and `_load_memory` filled `"warm"` for entries that
had none. Nothing recomputed it, so a memory stored a year ago was still "hot", and
`select_top`'s cold budget (2 reads) had nothing cold to keep in check.

Now, just before `select_top` in `_memory_recall`, every entry's tier is worked out again
with `memory_meta.memory_tier(entry, now)`; the stored value is not trusted. The doc is
written after the recall, so the worked-out tier is persisted and the panel shows the true
one. The rules are the base module's own (nothing new): importance >= 0.75, a day old or
less, or recalled >= 3 times is hot; importance >= 0.45 or two weeks old or less is warm;
anything else is cold. The plan's "高光永留" (importance 0.65, recalled twice) lands in warm
by that same rule, so no second rule set was written for it.

## Nothing is lost on save

`_load_memory` drops the entries whose text `_usable_memory_text` refuses (empty, an old
system prompt) from the view it hands back, and `_save_memory` then used to write the view
as the place's whole list, so those entries disappeared. Now the load keeps them aside on
the view (`_unusable_entries`, never written into `rooms`) and the save puts them back
exactly as they were. Deliberate removals are unchanged: the forget registry
(`_write_library`'s `_origin_kept`), a panel delete, a duplicate merge and a summary mark
all still remove or mark their entry.

## 5000 memories: how long one recall takes

Counted, not measured here. This sandbox cannot create the test's data folder
(`PermissionError` on the temporary folder), so the card's test 12 could not run. The
`Speed` test in `tests/test_keep_memory.py` builds 5000 made-up memories and prints the
time of one `_memory_recall`; it has no assertion on the time, and no cap was added. Run
it outside this sandbox and read the number; if it is slow enough to need a limit, that
goes back to review first.

## Putting lost memories back: `tools/restore_memory.py`

    python tools/restore_memory.py --data <her data folder> --backup <copy>/memory [--backup ...]
    python tools/restore_memory.py --data <her data folder> --backup <copy>/memory [...] --apply

Reads the copies of `memory/` made before 11-02 (each holds `library.json` and usually
`vectors.sqlite3`): the pre-表情包 copy, the old plugin's `plugin_data` copy, the
`memory-记1前` copy and the three installation copies. A `*` in `--backup` is expanded.
`history.sqlite3` is not used: it starts at the move and overlaps the library.

- Only a memory whose id the library does not have now is a candidate; its id, time,
  `origin`, `provenance`, importance, encoding emotion and the rest are copied as they
  were.
- Vector: the copy's own `vectors.sqlite3` first. When it is missing, or its length is not
  the library's, the vector is worked out again by the local bge-m3 service through the
  plugin's own `_embed_text`, and only when the saved embedding address is loopback
  (127.0.0.1 / localhost / ::1). If no vector can be had, the memory is not put back and is
  counted.
- Every memory goes in through `_write_library`, so the forget registry (`_origin_kept`)
  and the red line are asked first: what was forgotten, or crosses a red line with the
  switch on, never comes back.
- A run is a dry run unless `--apply` is given: it prints, per copy, how many can be put
  back, how many the registry keeps out, how many the red line keeps out and how many have
  no vector. No memory's words, no number, no place key.
- `--apply` copies `memory/` to `memory-备份-补回前-<time>/` beside it first, and writes
  only when that copy is complete.
- `--redline` says the `redline_filter` switch is on in her config (off by default, as in
  the plugin; there is no AstrBot here to read it from).
- Really running `--apply` needs the owner: stop her first, start the vector service, run
  it, then start her again. This card only used made-up data in tests and never pointed the
  tool at `her-data`; in this sandbox the tests could not create their data folder either.

## Tests

`tests/test_keep_memory.py` — 16 tests, each in a fresh interpreter on a made-up data
folder (`_case`), no network, no model, no real data:

1. 120 memories in one place: 120 in the library and 120 vectors.
2. compression on, 250 memories: all 250 kept.
3. an old, unimportant memory stored as `"hot"` is cold when recalled, and the saved tier
   becomes `"cold"` after the recall.
4. an old memory with importance 0.8 stays hot and is still recalled.
5. a summary mark still keeps its entry out of recall, and the entry itself stays.
6. an entry whose text is not usable is set aside by the load and is still in the library
   after a new memory is saved.
7. a forgotten person's memory does not come back when a new one is stored; duplicates
   still merge (one entry, hits 2); a panel delete stays deleted after the next store.
8. dry run over two fake copies: 3 restorable (1 already in the library); the library is
   unchanged; the output holds no words, no number, no place key.
9. `--apply`: 3 restored with the same id, ts, origin, provenance and importance; the
   vectors come from the copy's store; `memory-备份-补回前-…/` exists and its
   `library.json` is the memory folder as it was.
10. a memory of a forgotten person is counted as registry-blocked and is not restored.
11. with the red line on, a memory that crosses one is not restored.
12. a copy vector of other dimensions, or none, is worked out again with a fake
    `_embed_text`; a failed recompute is counted and not restored.
13. 5000 made-up memories: the time of one recall is printed, with no upper bound.

## Test runs in this sandbox

Run one file at a time; every error below is the sandbox refusing the test's temporary data
folder, not an assertion:

- `python -m unittest tests.test_keep_memory` — 16 tests, 16 errors, all `PermissionError`
  in `TemporaryDirectory` (`data.mkdir`). No test body could run.
- `tests.test_go_out_checks` — 19 run, 3 errors (`PermissionError`), 16 passed.
- `tests.test_model_ports_text` — 8 tests, OK (it replaces `_load_memory`, so it says
  nothing about this card).
- `tests.test_recall_walls` — 10 run, 20 errors, all `PermissionError`.
- `tests.test_send_walls` — 10 run, 20 errors, all `PermissionError`.
- `tests.test_basics` — 11 run, 2 errors, all `PermissionError`.
- `tests.test_golden` — 2 run, 2 errors, both `PermissionError`.
- `tests.test_golden_standalone` — 6 run, 4 errors; the other 2 passed.
- `tests.test_discretion` — 84 run, 62 errors, all `PermissionError`.
- `tests.test_forget_wiring` — 19 run, 19 errors, all `PermissionError`.

The golden traces were not re-recorded. They are expected to change in one way only: the
tier is now worked out at recall and written back, so `memory_tier` values change
(hot↔warm) for the older memories of the scripted conversation. A read-only count against
the recorded traces suggests roughly half of each trace's entries would change that value.
No entry in either scenario is more than a few days old, so none becomes cold, and the
memories a reply recalls should be the same. This cannot be confirmed here because the
golden test cannot run in this sandbox: the dispatcher should confirm the diff is only
`memory_tier` values before re-recording outside.

## Unsure about

- The tier is worked out for the whole view of the place doing the recall; another place's
  entries get theirs worked out when its own recall runs.
- `_load_memory`'s aside list is per view: a doc loaded before a concurrent write is
  merged by `_merge_memory_doc`, which does not merge a second load's aside list (the same
  limit the old code had, where those entries were lost outright).
- The restore tool asks for `--backup` explicitly instead of baking the owner's absolute
  paths into the repository; the change note lists which copies to pass.
- No memory content, number or place key is printed by the tool or written in this note.
