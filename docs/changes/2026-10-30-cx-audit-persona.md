# 2026-10-30 cx-audit-persona: audit persona and canary questions

## What

- The names check excludes the persona prefix from reply prompts, while still
  checking the plugin block and the message sent to the model. It compares all
  recorded reply prefixes (including redo prompts): when they differ, it removes
  none and reports `persona_boundary_ambiguous` in the names warnings. A reply
  without the boundary line is checked in full.
- The sent check excludes persona text and canary private questions from its
  private-word sources. Canary lines containing a recorded secret remain sources;
  normal chat and the other audit checks keep their existing rules.
- Offline replay-tool tests cover the persona, plugin block, asked text, canary
  questions, secret lines, and persona words in sent replies.

## Files and limits

`tools/audit_replay.py` and `tests/test_replay_tools.py`; no plugin changes or
new switches. The recorded prompt does not separately identify the persona:
the audit compares the prefixes before the first `[她现在]` line in replies
instead of comparing against an unavailable original persona. Identical prefixes
are not proof of the boundary: if that line appears in the persona, or the same
extra content precedes it in every reply, the inference can still be wrong.
No unrelated work or golden changes are included.
