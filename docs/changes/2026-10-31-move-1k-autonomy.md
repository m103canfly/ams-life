# 2026-10-31 move-1k: autonomy and screenshot ports

Proactive sends now use the messenger port for the event's own place. The
adapter still calls the event's send method and keeps the text in one Plain,
including face markers. Screenshot captions now use the model port, which
passes the same prompt and image path to the provider and returns its text.
The module-level `model_for` selects the client for both screenshot captions
and `PortsMixin._model`, so the choice has one place to change.
No switch or dependency is added. No files outside the card are changed.

`tests/test_autonomy_ports.py` covers event and background sends, face markers,
screenshot provider arguments and missing providers, the model factory, and
the plugin MRO.
Existing tests and golden files are unchanged.

Full suite: 1189 tests OK outside the sandbox (main dad87b5 had 1184; +5 in `tests/test_autonomy_ports.py`).
In the sandbox the same run passes except `test_brain_panel.InTheShell`, which needs a real browser.
Golden traces unchanged.
