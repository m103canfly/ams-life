# 2026-10-30 — cx-open-group

She can open a group herself and look at recent QQ stickers when she opens it.
The new `browse_groups_enabled` switch defaults off. With it off, an uncalled QQ
sticker is no longer looked at on arrival; the current message's pictures still
follow the existing reply path. `browse_groups_min_minutes` defaults to 5 and is
a safety net, not the schedule for a decision.

## When a person might pick up the phone

| Situation | Effect on the decision |
| --- | --- |
| Idle for a while | Raises the score; active recent conversation blocks it. |
| Awaiting a reply in a group | Raises that group's score for up to an hour. |
| Morning after waking or before bed | A small time-of-day signal; this does not prove she actually woke or is going to sleep. |
| Several unread messages and a familiar person | Raises the group's score, with unread capped so a busy group cannot dominate indefinitely. |
| A small group has waited a long time | Its waiting score grows, reducing starvation. |
| Night or no unread messages | No self-initiated group opening. |

Scores are bounded heuristics, not measurements of boredom or sleep. The first
version only rules out tiredness at night; a later change should use the mood
block's existing body state. The same five-minute loop can choose `group`, `web`,
or `none`. The web branch is a placeholder until #41's actual entry point is
verified. Opening a group itself invokes no model and sends no message.

Reply requests mark a group open, including the normal AstrBot wake path and a
request made after the attention gate. A completed response schedules a separate
task for the previous queued stickers; the reply's own images remain on the
existing reply path. A group queue is memory-only, capped at 100 and one hour,
and includes source identifiers to support forgetting. A person or source delete
clears queued items. The registry and deletion generation are rechecked before a
look and before its results are saved. At most three eligible looks are attempted
per opening, the daily hard limit is checked before each, and failed attempts are
not retried within the queue's lifetime. Cache identity is the URL hash while the
cache entry remains; a different URL for the same image can cost another look.
Each queued picture holds the vision lock for one look. A reply waiting for the
lock takes priority; the unattempted pictures stay queued for the next opening,
subject to the same expiry, capacity and forgetting rules.
Replies with no image to look at, including cached images and images with captioning
disabled, do not wait for the lock or interrupt the group look.
An individual call may cross the daily limit and failed calls may incur provider
charges that are unavailable in the response. Vision usage is recorded even when
`self_decide` is off.

The offline `tools/sim_open_groups.py` accepts a database path and per-look price,
opens the database read-only and prints only three aggregate estimates. It uses the
same observable signal weights and 5/15/30-minute safety nets. The old database
does not contain real mood, sleep or familiarity; interactions approximate the
latter and mood is neutral. Estimates are not actual bills or proof of behavior.
The immutable SQLite connection assumes a complete database snapshot; outstanding
WAL data may be absent from the estimate.

Files: `_conf_schema.json`, `main.py`, `mixin_group_browse.py`, `mixin_autonomy.py`,
`mixin_attention.py`, `mixin_media.py`, `mixin_stickers.py`, `mixin_discretion.py`,
`tools/sim_open_groups.py`, and corresponding offline tests. The discretion change
is one call on its existing shared deletion path. Candidate notes are checked for
five turns using AstrBot's existing non-saved-part harness. No unrelated changes
are intended, except that `_spending` now records vision use even when `self_decide`
is off. Goldens were not changed; the switch-off change can alter traces that
include uncalled stickers, and vision spending can change a trace with vision on
and `self_decide` off.
