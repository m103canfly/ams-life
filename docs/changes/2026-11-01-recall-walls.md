# Recall walls

The reply prompt now filters each recalled memory, event and notebook entry by
its origin before selecting it. Private material stays in its own private chat.
Public group material is anonymized in another group or a non-member's private
chat. Members of the originating group may see it in their private chat. Groups
listed together in `shared_groups` share recall as one place. Her own material
and web material remain available everywhere. Unknown origins are withheld.

The earlier strict cross-group proposal was superseded by the November 1
decision: public group material may travel without names or identifying numbers.
With `global_memory` off, this is close to the previous behavior; with it on,
private text is no longer shown to the model under a warning label. Merged
summaries retain private origins and preserve restrictions from multiple groups.
The shared-group configuration defaults to an empty list and accepts numeric
strings only. The standalone path is the target; AstrBot parity is not required.

The legacy discretion tests were updated only where they expected private text
in prompts, names or numbers in anonymous text, or anonymous recall for a group
member. The full suite was not run, as instructed. Offline results: recall walls
5 passed, reply provenance 7 passed, discretion 84 passed, golden 2 passed, and
basics 11 passed. The standalone golden test is reserved for the owner to run.

Anonymization removes known names and numeric identifiers; it cannot identify
every descriptive detail that might identify a person.
