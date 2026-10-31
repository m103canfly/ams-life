# 2026-10-31 move-7d: rename the old session keys in the copied data folder

Her data now uses neutral place names (`group:900001`, `private:10001`: what
`discretion.place_of` gives), and 5j-1 and 5j-2 make the plugin store only those. Old records
still hold AstrBot's session strings (`default:GroupMessage:900001`). `tools/rename_places.py`
changes those old values once, in the copy `tools/migrate_data.py` (7c) made, so that a copied
folder reads the same under the new names. Her own data folder is never touched: `--data` is
refused when `tools/_guard.live_reason` says it looks like an AstrBot data folder, when it is
inside this repository, or when it does not exist (exit 2, nothing written).

Changed, and only these:

    archives/events.jsonl                    each record's session, provenance.session,
                                             provenance.sources[].session and
                                             source_check.source_items[].session
    archives/sessions/<folder>/events.jsonl  the same fields, then the folders are merged
    memory/library.json                      entries[].provenance.session and its sources
    users/*.json                             the sessions list: deduplicated keeping the last
                                             place (the newest is last), at most 20
    archives/dedupe_log.jsonl                session and dropped_sessions

Each value becomes exactly `discretion.place_of(old)`, so the tool and the plugin agree on
what a place is; an empty session stays empty. Not changed: the `umo` of a `phone/` window (it
is AstrBot's wiring for sending and for deleting a conversation's history, not a key), the old
archives (`memory/archive/`, `memory/per_session_legacy/`, `states/per_session_archive/`,
`before-forget-*`, `before-redline-*`), `archives/insights.jsonl`, and `people/` (the names and
aliases she keeps of people are not a program key).

The event folders are merged the way the owner decided (10-31). Every event of every
`archives/sessions/<folder>/events.jsonl` first has its session fields renamed; its target
folder is the renamed session through the plugin's own rule, copied into the tool from
`mixin_events._event_session_file` (`"".join(c if c.isalnum() or c in "-_" else "_" for c in
(session or "default"))[:80]`, so `group_900001` and `private_10001`, and an empty session is
`default`). Events of one target are gathered, deduplicated by `id` (two records equal as
`json.dumps(..., sort_keys=True)` are kept once; one `id` with two different contents stops
the run with exit 2 and nothing written, printing only the folder and the `id`; records with
no `id` are all kept) and sorted by `ts`, the same `ts` keeping its earlier order. The target
file is written with `atomic_file` (a temp file, then `os.replace`); only after it is in place
are the old folders that were merged into it removed, and only in the copy.

Everything is read and worked out before anything is written. Read first: every file the tool
may change (a file it cannot read as JSON stops the run with exit 2 and only its relative
path printed) and the platform prefix of every session-like value (an AstrBot platform name
before `GroupMessage` & co.; more than one prefix stops the run, printing each prefix and how
many distinct values carry it). Then the same check for an `id` seen twice with different
contents. Any of these means exit 2 with no file touched, which is why the tool never leaves a
half-renamed copy.

Printed: per store the number of values renamed and the count before and after; the event
folders before and after (how many, the first and the last five names), how many groups were
merged and how many identical events were dropped; `TempMessage` counted as private chats and
`GuildMessage` as groups. Only numbers, folder names and relative paths are printed, never a
record's words and never a key. Exit: 0 all done, 1 `--check` still finds a session string or
an event that does not belong to its folder, 2 not started (the guard, an unreadable file, two
prefixes, an `id` clash). `--check` only reads and judges the same files without writing:
no session string left in them, and each folder's events cleaning to the folder's own name.
`--check` cannot know the count from before the rename, so the real run's report carries the
before and after counts.

`tests/test_rename_places.py` uses only made-up folders inside its own temporary folder; the
numbers are `900001`, `10001`, `900002` and the platform is `default`. It covers one run over
a made-up copy (`test_one_run_renames_every_store_and_merges_the_places`: every session field
neutral, the two folders merged into `group_900001` with the identical event once and the
order by `ts`, the library's entries and sources, the users list deduplicated with the newest
last and at most 20, the dedupe log, the `phone/` window's `umo` and the `people/` names
untouched byte for byte, the same number of `events.jsonl` lines, and no record's words on the
screen); `--check` before the rename (exit 1) and after (exit 0, and `--check` writes
nothing) (`test_check_before_and_after`); one `id` with two contents stopping everything with
exit 2 and every file's hash unchanged (`test_one_id_with_two_contents_stops_everything`);
`default:` and `other:` stopping the same way (`test_two_platform_prefixes_stop_everything`); a
JSON that cannot be read (`test_a_json_that_cannot_be_read_stops_everything`); the guard
refusing a made up `astrbot/data/plugin_data/...` folder and the tool refusing a missing folder
and one inside the repository (`test_a_live_data_folder_is_refused`,
`test_a_folder_that_is_not_there_and_the_repository_are_refused`); the `TempMessage` and
`GuildMessage` counts in the report
(`test_temp_message_is_a_private_chat_and_guild_message_a_group`); and a source-level check
that the tool imports no AstrBot and no logging (`test_no_astrbot_and_no_logging`).

Nothing existing changed; the tool is not imported by the plugin, so behavior and golden traces
are unchanged. Only the names inside the copied data change, and each new value is what
`discretion.place_of` already turns the old one into when the plugin reads it, so the copy reads
as before. Files keep the plugin's own formats: JSONL lines as
`json.dumps(..., ensure_ascii=False)`, `memory/library.json` compact, `users/*.json` with
`indent=1` (as `mixin_discretion` and `mixin_people` write them).

Files: `tools/rename_places.py`, `tests/test_rename_places.py`, this note. No other file changed.

Tests: `tests.test_rename_places`, run by the dispatcher outside the sandbox (dsh's sandbox
cannot write its temporary folders): 9 tests pass with the test Python and with `venv-ams-life`. The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
