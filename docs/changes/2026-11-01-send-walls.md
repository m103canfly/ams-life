# Send walls

The final reply check now runs with `global_memory` on or off. It collects
the forbidden entries recorded for this turn by the recall wall. With global
memory off, relevant cross-session memories, the selected events and dropped
notebook entries are recorded too. Private group entries contribute their words,
but not the names of their speakers. Public group and self-origin text is not
added to that list. Owner rule copying remains a separate check. The check may
retry the reply once and holds it if the retry still leaks or the check fails.

Names come from the people index and per-place profiles. A person's sessions
decide whether their names belong in this conversation, including shared groups
and people present. Names with unknown owners or no recorded sessions are not
blocked; only their count is logged. Short names and everyday words are ignored.
The name list is cached for the turn. Matching uses `send_check.mentions`,
without exempting names found in allowed text. No additional location table or
plugin method is added.

Only the system prompt and her earlier replies here are allowed text. The
current user's matching words are excluded from the text comparison, but an
additional admission can still be held. Punctuation and spaces are removed for
text matching; pinyin initials are not detected. Vector comparison is used only
when the configured embedding host is explicitly loopback; remote hosts receive
neither the forbidden text nor the reply from this check. Scanning private
the recalled entries adds work to a reply. Existing memory and event vectors
are reused; missing vectors are calculated locally and cached. The reply check
no longer scans the entire private library.

The `test_send_check` names-only case again expects no retry; the disabled
global-memory hint case expects a retry when relevant private recall is blocked.
The `test_discretion` disabled-check assertion now expects the check to run;
its private-group assertion and the recall wall tests are unchanged. The
attention fixture restores its temporary check replacement after the hold case.

Offline validation passed separately: test_send_walls (10), test_send_check
(23), test_owner_rules_copy (6), test_recall_walls (10), test_discretion (84),
test_notebook_private (4), test_impression_layers (6), test_golden (2),
test_basics (11), test_replay_tools (57), test_attention (38),
test_stickers_wire (29), test_browse_wire (20), test_selfie (46), and
test_voice_once (9). No full suite was run. The standalone golden test is run
outside the sandbox by the owner; existing golden files are unchanged. The
owner's November 1 instruction excludes AstrBot-specific changes. No pages or
settings were changed.
