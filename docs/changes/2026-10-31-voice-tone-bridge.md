# 2026-10-31 - Voice tone bridge

The bridge now selects a reference from `tones` using the request's `voice`.
It tries entries in order, falls back to the calm tone, then to the existing
top-level reference. Unknown voices use the calm tone. Existing configurations
without `tones` keep using the top-level reference. The selected text and audio
are sent together; the multipart filename stays fixed. No new switch or
dependency is needed, and no files outside this card changed.

Full suite: 1226 tests OK outside the sandbox (main aee4e7a had 1220; +6 in `tests/test_breeze_openai_tts.py`);
after merging main 32662f1 (1240 tests), 1246 tests OK with venv-ams-life, run on its own. Golden traces unchanged. The machine's tone table lives in breeze.json,
outside the repository.
