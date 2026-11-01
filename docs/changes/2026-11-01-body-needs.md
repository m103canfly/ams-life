# Body needs

Add bounded sleepiness, hunger and physical fatigue to the body snapshot, with
timestamps and schedule-based fallback transitions. The panel already returns
that snapshot. Event helpers and optional feeling descriptions are available for
later work; they are not connected to prompts. The existing mood derivation and
daily schedule remain unchanged. No switch or new dependency is needed.

The basic and full golden traces were re-recorded. Each has exactly these
added paths, compared recursively with the respective HEAD JSON:

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

No existing values or other paths changed. The targeted body, daily, turn,
panel, golden and basics tests passed; the panel test skipped 17 cases without
aiohttp. The full suite was not run as instructed. No files outside the card
were changed.
