# Send walls

The final reply check now runs with `global_memory` on or off. It collects
private memories, events and notebook entries denied by the recall wall,
including cross-session memories, without adding public group or self-origin
text to that list. Owner rule copying remains a separate check. The check may
retry the reply once and holds it if the retry still leaks or the check fails.

Names come from the people index and per-place profiles. A person's sessions
decide whether their names belong in this conversation, including shared groups
and people present. Names with unknown owners or no recorded sessions are not
blocked; only their count is logged. Short names and everyday words are ignored.
No additional location table or plugin method is added.

Only the system prompt and her earlier replies here are allowed text. The
current user's matching words are excluded from the text comparison, but an
additional admission can still be held. Punctuation and spaces are removed for
text matching; pinyin initials are not detected. Vector comparison is used only
when the configured embedding host is explicitly loopback; remote hosts receive
neither the forbidden text nor the reply from this check. Scanning private
records and, for a local embedding service, embedding their text adds work to
each reply; vectors are cached for the process lifetime.

The old `test_send_check` assertions for a disabled check and for a cleared
temporary forbidden list now reflect the always-on check. The recall wall test
is unchanged. Offline validation passed separately: test_send_walls (6),
test_send_check (23), test_owner_rules_copy (6), test_recall_walls (10),
test_golden (2), test_basics (11), and test_replay_tools (57). No full suite
was run. The standalone golden test is run outside the sandbox by the owner;
the existing golden files are unchanged. AstrBot-specific items were omitted
under the owner's November 1 instruction. No pages or settings were changed.
