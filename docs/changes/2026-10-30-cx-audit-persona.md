# 2026-10-30 cx-audit-persona: audit persona and canary questions

## What

- The names check excludes the persona prefix from reply prompts, while still
  checking the plugin block and the message sent to the model.
- The sent check excludes persona text and canary private questions from its
  private-word sources. Canary lines containing a recorded secret remain sources;
  normal chat and the other audit checks keep their existing rules.
- Offline replay-tool tests cover the persona, plugin block, asked text, canary
  questions, secret lines, and persona words in sent replies.

## Files and limits

`tools/audit_replay.py` and `tests/test_replay_tools.py`; no plugin changes or
new switches. The recorded prompt does not separately identify the persona:
the audit infers its end from the first `[她现在]` line in a regular reply.
If that line is missing or appears in the persona, the boundary is ambiguous.
No unrelated work or golden changes are included.
