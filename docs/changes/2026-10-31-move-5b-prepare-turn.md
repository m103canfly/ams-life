# 2026-10-31 move 5b: prepare turn

The fifth move separates turn preparation from AstrBot so another program can use
the same preparation. The preparation body moved from `main.py` to `TurnMixin`,
with only `req` renamed to `turn_request`. Switches and intended behavior are unchanged.

The 5a adapter now preserves a missing user-parts list as `None`, leaves an absent
tool field absent, and retains an unchanged empty tool set. It writes changed lists
in place and leaves unchanged fields alone. The two corresponding 5a test expectations
were corrected. The hook writes back even on errors and restores the AstrBot request
in the send-check note, so a retry sees images prepared after the hook.

Tool selection remains on AstrBot's request for this card; its existing tests use
that interface. No files outside the card or golden traces were changed.

Full suite: 1304 tests OK outside the sandbox with `venv-ams-life` (main 754dd0b had 1299; +5 in
`tests/test_prepare_turn.py`). Golden traces unchanged. A script checked that main.py lines 698-898 at
754dd0b, with `req` renamed to `turn_request`, are the body of `_prepare_turn` character for character
(mixin_turn.py lines 21-221; 14 lines renamed).
