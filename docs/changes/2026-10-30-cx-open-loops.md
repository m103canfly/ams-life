# 2026-10-30 cx-open-loops: open loops follow their speaker

## What

`memory_meta.py` excludes marked questions and common unmarked questions about
remembering or knowing, as well as common first- or third-person future plans.
Reminders with no date expire after three days; the existing soon, tomorrow and
later windows remain unchanged. A legacy loop without a creation time starts its
expiry clock the first time it is updated, since its original age is unknown.
Cue matching is still heuristic and cannot understand every phrasing.

`mixin_phone.py` retains the event origin on new loops and combines source IDs
when the same person's similar requests merge. In groups, different people's
requests do not merge or settle one another. Expiry still applies to all loops.
`main.py` passes only loops attributed to the current speaker into the group
compact prompt; a group loop with missing or ambiguous people is omitted. Private
windows retain their existing behavior. Existing deletion and confidentiality
handling continues to use the origin. The continuity line and her notebook are
unchanged.

## Switches and scope

There is no new switch; the behavior applies to existing open loops. No work
outside the card is included. Offline tests cover detection, expiry, attribution,
group isolation, independent merging and cancellation, and legacy windows.
The owner ran the full suite: 714 tests, with three failures in the previous
revision (the prompt-shape expectation and the two golden traces). The old
prompt-shape test expected one person's group reminder while another person was
speaking; its assertion now checks the reminder for its speaker and its absence
for the other person. This revision and the requested filter-removal mutation
have not been run because Python cannot be started in this sandbox.

The files in `tests/golden/` were not changed. In the supplied diffs, the
unpunctuated remembering question is no longer stored or shown in private prompts;
group prompts no longer show the calculation request to other speakers. The
calculation request has no due date: created at 1793000790, it expires on the
first group update after three days, at 1793271380. The old trace instead marked
it fulfilled at 1793276520 when a different person reported handing in a report.
That message did not say the calculation was done: the old shared-bigram match
mistook the common address for a match. The new three-day expiry happens before
that message, and restricting group settlement to the requester also prevents
such a later cross-person settlement. Both changes follow the card's expiry and
person boundaries. The supplied full diff ends partway through, and the golden
test itself limits its diff to 120 lines, so unseen changes cannot be verified
from this output.

Files: `memory_meta.py`, `mixin_phone.py`, `main.py`,
`tests/discretion_cases.py`, `tests/test_discretion.py`, `tests/test_body_heart.py`,
and this note.
