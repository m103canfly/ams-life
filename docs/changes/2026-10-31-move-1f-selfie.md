# 2026-10-31 move-1f-selfie: phone media through Messenger

Phone media now uses the Messenger port, so another transport can send the same segments.
The AstrBot adapter can use the current event's send method for its own place;
other places still use the context. The event route is opt-in. Photo and screenshot captions
remain plain text, and whitespace-only captions are omitted. Voice and fallback screenshot
text retain their original component types. No settings or switches were added.

`tests/test_selfie_ports.py` covers event routing, errors, opt-in, and the media components.
No existing tests or golden files were changed. Only the five files named on the card changed.


The event route also accepts an empty place when the event's place is empty. Previously the
media code called the event's send method even when the event had no session origin, so this
preserves that behavior. An empty destination does not match a nonempty event place.

Full suite: 1161 tests OK outside the sandbox (main bf4bbc3 had 1151; +10 in `tests/test_selfie_ports.py`).
In the sandbox the same run passes except `test_brain_panel.InTheShell`, which needs a real browser.
Golden traces unchanged.
