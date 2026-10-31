# 2026-10-31 voice tone plugin

The voice bridge can select a reference recording by tone. The `say_aloud` tool
now accepts an optional tone; when omitted, the current body's mood selects one
after decay. Unreadable mood values or an unavailable body fall back to calm.
The request's `voice` field now carries the selected tone instead of the
configured voice. Voice remains controlled by the existing switch.

`tests/test_voice_tone.py` covers thresholds, invalid values, tool schema,
queueing, request bodies and dispatch compatibility. Existing tests and golden
files were not changed. No files outside the card were changed.

Full suite: 1226 tests OK outside the sandbox (main aee4e7a had 1220; +6 in `tests/test_voice_tone.py`);
after merging main 32662f1 (1240 tests), 1246 tests OK with venv-ams-life. Golden traces unchanged.
Check B1 of the card was changed with the review's agreement: with "happy" moved to the very front
(the happy and sad ranges do not overlap, so only swapping those two changes nothing).
