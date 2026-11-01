# Body needs

Add bounded sleepiness, hunger and physical fatigue to the body snapshot, with
timestamps and schedule-based fallback transitions. The panel already returns
that snapshot. Event helpers and optional feeling descriptions are available for
later work; they are not connected to prompts. The existing mood derivation and
daily schedule remain unchanged. No switch or new dependency is needed.

Review fix: the whole midnight schedule period counts as sleep, including its
"preparing to sleep" option. The evening option still counts as awake.

The basic and full golden traces were re-recorded after the review fix. Each
has exactly these added paths, compared recursively with the respective JSON
from the merged main parent:

- `files.states/her.json.hunger`
- `files.states/her.json.last_meal`
- `files.states/her.json.last_rest`
- `files.states/her.json.last_sleep_end`
- `files.states/her.json.physical_fatigue`
- `files.states/her.json.sleepiness`
- `page_status.data.cores[0].snapshot.hunger`
- `page_status.data.cores[0].snapshot.last_meal`
- `page_status.data.cores[0].snapshot.last_rest`
- `page_status.data.cores[0].snapshot.last_sleep_end`
- `page_status.data.cores[0].snapshot.physical_fatigue`
- `page_status.data.cores[0].snapshot.sleepiness`

No existing values or other paths changed against that parent. Against the
previous branch traces, only sleepiness, physical fatigue and last sleep end
changed in the state file and panel snapshot, as expected from the fix. The
targeted body (9), daily (3), turn (5), panel (20), golden (2) and basics (11)
tests passed; the panel test skipped 17 cases without aiohttp. The full suite
was not run as instructed. No files outside the card were changed.
