# 2026-10-31 move-1g: sticker sends through Messenger

Sticker sends now go through the Messenger port. The sticker action still uses the existing
parameter and destination checks, and the no-bot path still falls back without a warning.
The picture fallback sends the same base64 image component to the event's session.
The adapter prefers `bot.api.call_action` when available, then `bot.call_action`.
No switch or dependency is added.

For an empty or unresolved session, the adapter does not send the fallback picture; the caller
still marks it sent when the adapter returns without raising. Normal event sessions resolve to
the same destination as before.

`tests/test_stickers_ports.py` covers the sticker action, failure fallback, missing bot and
speech admission. No files outside this card are changed. Golden files are unchanged.

Full suite: 1076 tests OK outside the sandbox (main 7e92514 had 1072; +4 in `tests/test_stickers_ports.py`).
In the sandbox the same run passes except the six `test_brain_panel.InTheShell` tests, which need a real browser.
