# 2026-10-30 cx-forget-astrbot: clear group conversation history on owner deletion

When the owner deletes a person, the panel now reports how many group contexts were
cleared alongside the existing AstrBot private-conversation and message-history counts.
The plugin saves phone window origins before local deletion, selects groups containing
the person's recent messages or identified by deleted local records, and also selects
windows whose speakers cannot be determined. It leaves groups with only identifiable
other speakers alone unless deleted records link them to the person. Window lines expire
and are capped, so groups whose evidence has already disappeared cannot all be identified.

Using the supplied AstrBot 4.29.3 interface, `get_curr_conversation_id(umo)` finds the
current conversation and `update_conversation(umo, id, history=[])` clears its history.
This retains the current conversation and its other fields, and does not create a new
conversation when none is current. Missing interfaces and errors produce one generic
warning for the group-clearing pass and do not prevent local deletion. Concurrent writes
to the same conversation may race with this update; there is no synchronization here.

AstrBot's `astrbot.log` can contain chat text; it rotates at 50 MB with three old files
retained. Deletion does not modify these logs. AstrBot's per-group recent-message buffer
in memory has no public interface and disappears on restart.

No new switch; the behavior applies to owner person deletion. No changes outside the
card. Offline tests cover a matching and an unrelated group, a missing update interface,
and an update error. The full suite passes (713 tests on main 85c609b) and removing the
clear fails three of them. `tests/golden/` is unchanged.

Files: `mixin_discretion.py`, `mixin_pages.py`, `pages/dashboard/app.js`,
`tests/forget_cases.py`, `tests/test_forget_wiring.py`.
