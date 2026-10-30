# 2026-10-31 move-1j: vision calls through ModelClient

Image captions and sticker looks now use the model port over the same vision
provider. The adapter sends the same prompt and image list and returns the same
completion text. Existing parsing, exception handling and provider accounting
remain in place. `StickersMixin` inherits `PortsMixin` for standalone use.
No switch or dependency is added. No files outside the card are changed.

`tests/test_model_ports_vision.py` covers provider arguments, captions, looks,
provider errors and the plugin MRO. Existing tests and golden files are unchanged.

Full suite: 1155 tests OK outside the sandbox (main bf4bbc3 had 1151; +4 in `tests/test_model_ports_vision.py`).
In the sandbox the same run passes except `test_brain_panel.InTheShell`, which needs a real browser.
Golden traces unchanged.
