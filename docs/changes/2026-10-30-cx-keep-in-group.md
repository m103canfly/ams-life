# 2026-10-30 cx-keep-in-group: keep requested group messages in their group

A group message asking for confidentiality and up to three preceding messages by the
same person in the same group within 120 seconds are private to that group. Phrases and
explicit negative phrases are in `discretion.py`. The rule applies to future messages;
existing historical records are not migrated. A future follow-up can narrow the records
already made from the preceding messages in its two-minute window.

`mixin_phone.py` detects the request, preserves the message IDs, and marks current and
preceding window lines. `mixin_discretion.py` narrows matching library entries, event
archive and session copies, insights, self-model notes, window lines and open loops; it
also narrows impressions that actually carry matching source IDs. A pending per-group job
is made stale only when its own group is narrowed. Jobs with no single place retain a
conservative snapshot of all groups.

Origin call-site inventory from `make_origin(` and `visibility_of(`:

- `mixin_phone.py` `_event_origin` uses the message request or the saved window origin;
  updated and resolved loops merge the source when the incoming group message is private.
- `mixin_memory.py` new user and assistant records use the event origin; duplicate and
  reconsolidated records merge or narrow the old origin. Consolidation at 909 and 962
  already passes merged visibility. The legacy migration preserves stored visibility;
  the missing-origin fallback retains its existing inference for old records.
- `mixin_events.py` the strong-event origin now retains merged visibility. The merge
  helper at 25 and consolidation at 2218 already pass merged visibility.
- `mixin_llm.py` relationship narratives use the visibility of matching evidence in the
  phone, memory library and event archive. Body/self and notebook origins at 452, 499, 501 and 592
  already use self or merged material. The notebook excludes private group material
  from its group sitting.
- `mixin_people.py` excludes group-private memories from relationship maps without
  per-item origins; the private-chat view suppresses existing shared text when retained
  group-private material from that person is present.
- `mixin_digest.py` checks the selected source lines for private visibility; `digest.py`
  also collects fallback IDs for group-private lines without a platform message ID.
- `impressions.py` excludes group-private lines from the model's material and alias
  verification, and keeps counts and hours. Impression origins stay as before; a record
  carrying source IDs that match a follow-up is narrowed, but an older record without
  such IDs is not. Names and aliases are still saved for anonymization. When a follow-up
  arrives while this group's impression model call is waiting, the answer is discarded
  because the model may have seen the newly narrowed lines. Counts saved before the call
  still stand; text-derived phrase statistics from that in-flight call cannot currently
  be traced back to individual messages.
- `discretion.py` provides the existing default, fallback, merge and table rules;
  `visibility_of` is called by `make_origin`. `tools/import_old.py` imports old data
  and is outside the future-message rule.

`main.py` runs the send check only with `global_memory` on, as before. A recalled
group-private memory, event or note labelled NO is forbidden by its text, without
forbidding the speaker's name; the existing private hint checks still apply. The check
does not scan unrecalled material or handle a prompt built before the follow-up narrowed
its sources. Phone lines hold at most 300 characters and expire after 24 hours; once
expired or truncated, a line not retained in memory cannot be recalled or checked.
This does not add a permanent copy or change existing retention and forgetting rules.
Relationship evidence that has lost all of its source IDs cannot be traced back after
its source window and memory have expired.

`tools/audit_replay.py` classifies requests and their preceding messages as private;
when the group canary occurs in one, an anonymous mention elsewhere is also a leak.
Its normal piece-size and paraphrase limits still apply. `tools/replay.py`'s fake
reply in the owner's own private chat answers his private canary without also echoing
the unrelated group-private canary; deliberately leaked group secrets remain checked.

Offline tests exercise real `on_message` handling, current and preceding visibility,
time, person and group boundaries, negations, derived stores, digest, impression,
send check and replay canary. No model or network is needed. The 584-test result in the
review predates this revision; the revision has not been run here. `tests/golden/` is unchanged.

Files: `discretion.py`, `digest.py`, `impressions.py`, `main.py`, `mixin_phone.py`,
`mixin_discretion.py`, `mixin_memory.py`, `mixin_events.py`, `mixin_llm.py`, `mixin_people.py`,
`mixin_digest.py`, `mixin_impressions.py`, `mixin_send_check.py`, `send_check.py`,
`tools/audit_replay.py`, `tools/replay.py`, `tests/discretion_cases.py`,
`tests/test_discretion.py`, `tests/test_impressions.py`, `tests/test_replay_tools.py`,
`tests/test_keep_in_group_audit.py`, `tests/test_basics.py` (+1 plugin method).
