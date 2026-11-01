# Sleep when sleepy

She was getting sleepy too fast while awake and recovering far too fast while
asleep, so a night's sleep could not last more than about three hours and she
reported her own minutes. Now sleepiness moves slowly enough for a 24-hour day,
the length of a sleep comes from how sleepy she is, and a chat going quiet no
longer interrupts something she is busy with.

## Sleepiness rates (`body.py`)

The three rates are module constants together with a comment that shows the
arithmetic: `SLEEPINESS_RISE_DAY = 0.035`, `SLEEPINESS_RISE_NIGHT = 0.06`,
`SLEEPINESS_FALL_SLEEP = 0.066`. Awake in the day is 07:00-23:00, at night is
23:00-07:00 (the old split at 06:00 moves to 07:00). Hunger and physical
fatigue keep their old rates.

With the life loop on, only an interval she chose counts as sleep. The
`daily.schedule` rule that treats the 00:00-07:00 stretch as sleep is used only
when the life loop is off, so a stretch she chose to stay awake is no longer
counted as sleep by the schedule.

## Sleep length (`life_loop.py`)

`apply_choice` ignores her `minutes` for sleeping. It computes
`(sleepiness - waking line) / 0.066` hours in `sleep_minutes`, within limits: a
sleep begun in 20:00-05:59 is the night's and runs to 0.15, at most 10 hours;
any other sleep is a nap and runs to 0.45, at most 90 minutes; 20 minutes is the
floor. The computed length is written to `states/now.json` and to the sleep
state, so the wake time is the same for both, and the day record keeps it too.
`_set_now` keeps a chosen sleeping item at an hour or more, so the short item is
written once more with the computed length.

The prompt's JSON example no longer shows `"minutes":30`; it now says
`"minutes":"睡觉不用写，别的事写大概多久"`. Falling asleep at night still writes
the notebook as before.

## Interrupting her (`life_loop.tick`)

If a chosen activity has not ended and is not `什么都不干`, `reason` only
accepts the body crossing a line, a due plan, or a fresh start. "跟人聊完了，
那个地方静下来了" now reaches her only while she is idle (her thing has ended or
she is dazing). The body crossing and due checks move ahead of the quiet one;
the reason text itself is unchanged.

## Examples

| Case | Sleepiness | Length | Wake |
| --- | --- | --- | --- |
| Wakes at 07:00 at 0.15 | reaches 0.7 at about 22:45 | 500 min | 07:05 |
| Sleeps at 22:45 | 0.7 | 500 min (8 h 20 m) | 07:05 |
| Afternoon nap at 14:00 | 0.55 | 90 min (cap) | 15:30 |
| Afternoon nap at 14:00 | 0.30 | 20 min (floor) | 14:20 |
| Late night at 01:00 | 0.82 | 600 min (cap) | 11:00 |

## Files

- `body.py`: the three rate constants, `slept`, `_advance_needs`,
  `_chosen_needs` (a nap may be 20 minutes), `_sleeps_by_choice`.
- `life_loop.py`: `sleep_minutes` and its constants, `apply_choice`, the prompt
  line in `materials`, the `busy` gate in `tick`.
- `tests/test_sleep_when_sleepy.py`: the card's tests 1-7.
- `tests/test_life_loop.py`, `tests/test_body_needs.py`: old expectations.
- `tests/golden/basic.json`, `tests/golden/full.json`: re-recorded.

## Golden update

The sleepiness rate change is meant to change the body numbers, and exactly two
values per trace differ; every other value is byte-identical. They were
re-recorded after checking the list.

| File | Path | Old | New |
| --- | --- | --- | --- |
| basic | `files/states/her.json.sleepiness` | 0.802 | 0.8424 |
| basic | `page_status.data.cores[0].snapshot.sleepiness` | 0.862 | 0.8774 |
| full | `files/states/her.json.sleepiness` | 0.802 | 0.8424 |
| full | `page_status.data.cores[0].snapshot.sleepiness` | 0.877 | 0.8861 |

## Old tests changed

`test_body_needs` changes only the expected numbers (day rate, night rate,
asleep rate, `slept`). In `test_life_loop`:

- the three quiet tests now start from `什么都不干` (dazing), because a chosen
  rest is no longer interrupted by quiet;
- the eight-hour sleep test starts at 22:45 with 0.678 so the night sleep really
  is eight hours;
- the recovery, restart, expired-sleep and wake-settling tests use the computed
  lengths (a 90-minute nap at 10:00 with 0.9, a 20-minute nap with 0.1) and the
  new rates; one test is renamed from eight hours to a twenty-minute nap;
- no other assertion was touched.

## Validation

What could run in the sandbox: `tests.test_sleep_when_sleepy.Rates` and
`.Lengths` (9 tests) passed; `tests.test_life_loop.ParserTests` (2) passed;
`tests.test_body_needs.BodyNeedsTests` passed 8 of 9 - the ninth builds a real
plugin and stops at `PermissionError` creating `states/` in the platform temp
area.

The file-based tests cannot run here: the sandbox denies `mkdir` inside the
platform temp area (`PermissionError`), which hits `test_life_loop`,
`test_body_heart`, the async classes of `test_sleep_when_sleepy`, and both
golden tests. The goldens were therefore re-recorded by running
`tests/scenario.py` in a fresh interpreter with `PYTHONHASHSEED=0` and without
`AMS_LIFE_DATA_DIR`, using a data folder inside the worktree; a second run was
byte-identical. The full suite was not run, as instructed.
