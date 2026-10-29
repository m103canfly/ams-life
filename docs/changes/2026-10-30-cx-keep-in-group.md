# 2026-10-30 cx-keep-in-group: keep requested group messages in their group

A group message asking for confidentiality and up to three preceding messages by the
same person in the same group within 120 seconds are private to that group. Phrases and
explicit negative phrases are in `discretion.py`. The rule applies to future messages;
existing historical records are not migrated. A future follow-up can narrow the records
already made from the preceding messages in its two-minute window.

`mixin_phone.py` detects the request, preserves the message IDs, and marks current and
preceding window lines. `mixin_discretion.py` narrows matching library entries, event
archive and session copies, insights, self-model notes, window lines and open loops; it
also narrows relevant impressions. Work still waiting for a model is marked stale so it
cannot overwrite a narrowed record with an older copy.

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
- `impressions.py` attaches the day's group-private source origins conservatively to each
  impression, because the shared model call can use one person's words for another;
  days without those sources leave the existing origins unchanged.
  Display outside a private impression's group is dropped, and cross-group alias
  collection excludes private records. For older impressions without IDs, a follow-up
  narrows each such record in the group rather than guessing which fields came from it.
- `discretion.py` provides the existing default, fallback, merge and table rules;
  `visibility_of` is called by `make_origin`. `tools/import_old.py` imports old data
  and is outside the future-message rule.

`mixin_send_check.py` includes retained group-private originals from windows and the
memory library as private forbidden items even when not recalled; `main.py` runs the
check with `global_memory` on or off, without changing its default. These additional
window items use literal and existing hint checks without fetching embeddings for each
line. An exact repeat of a group-private original is blocked even if it is quoted in the
request; otherwise existing allowed/common-piece exclusions and paraphrase limits apply.
Phone lines hold at most 300 characters and expire after 24 hours; if a message was not
also retained in memory, its expired or truncated original cannot be checked. This
does not add a permanent copy or change existing retention and forgetting rules.
Relationship evidence that has lost all of its source IDs cannot be traced back after
its source window and memory have expired.

`tools/audit_replay.py` classifies requests and their preceding messages as private;
when the group canary occurs in one, an anonymous mention elsewhere is also a leak.
Its normal piece-size and paraphrase limits still apply. `tools/replay.py`'s fake
reply in the owner's own private chat answers his private canary without also echoing
the unrelated group-private canary; deliberately leaked group secrets remain checked.

Offline tests exercise real `on_message` handling, current and preceding visibility,
time, person and group boundaries, negations, derived stores, digest, impression,
send check and replay canary. No model or network is needed. The full suite passes
(572 tests); `tests/golden/` is unchanged, since neither golden conversation has a
keep-in-group request.

Files: `discretion.py`, `digest.py`, `impressions.py`, `main.py`, `mixin_phone.py`,
`mixin_discretion.py`, `mixin_memory.py`, `mixin_events.py`, `mixin_llm.py`, `mixin_people.py`,
`mixin_digest.py`, `mixin_impressions.py`, `mixin_send_check.py`, `send_check.py`,
`tools/audit_replay.py`, `tools/replay.py`, `tests/discretion_cases.py`,
`tests/test_discretion.py`, `tests/test_replay_tools.py`, `tests/test_keep_in_group_audit.py`,
`tests/test_basics.py` (+2 plugin methods).
