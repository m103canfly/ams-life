# Recall walls

The reply prompt now filters each recalled memory, event and notebook entry by
its origin before selecting it. Private material stays in its own private chat.
Public group material is anonymized in another group or a non-member's private
chat. Members of the originating group may see it in their private chat. Groups
listed together in `shared_groups` share recall as one place. Her own material
and web material remain available everywhere. Unknown origins are withheld.

The earlier strict cross-group proposal was superseded by the November 1
decision: public group material may travel without names or known identifying numbers.
With `global_memory` off, this is close to the previous behavior; with it on,
private text is no longer shown to the model under a warning label. Merged
summaries retain private origins and preserve restrictions from multiple groups.
The shared-group configuration defaults to an empty list and accepts numeric
strings only. The standalone path is the target; AstrBot parity is not required.

The legacy discretion tests were updated only where they expected private text
in prompts, names or known numbers in anonymous text, or anonymous recall for a group
member. The full suite was not run, as instructed. The standalone golden test is
reserved for the owner to run.

Anonymization removes known names and known numeric identifiers; it cannot identify
every descriptive detail that might identify a person.

Review revision: filtered private material selected by the previous recall
limits still enters the send check, without entering the reply prompt. Merged
origins take the strictest source decision, and a turn caches each person's
group sessions. Unknown numbers remain as before. The replay's private-canary
label assertion in `test_replay_tools` now expects zero, because the private
secret no longer enters another place's prompt. Its discretion-instruction
assertion and the three replay send-check assertions are unchanged. The offline
fake model now says the private canary on game probes to test the send check
without putting that canary in the model prompt.

The send check uses the existing recall thresholds and limits. If a private item
is not selected for its forbidden list, it cannot detect a fabricated secret
from that item. A probe forcing the canary on every kind of question exposed this
limit; the game probes exercise selected forbidden items.

Offline tests passed, one file at a time: recall walls 10, reply provenance 7,
discretion 84, send check 23, replay tools 57, body heart 41, golden 2, basics
11, keep-in-group audit 1, stage replay 18, no numbers 15, strong event place
4, impressions 28, and impressions wiring 17.
