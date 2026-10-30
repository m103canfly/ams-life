# 2026-10-31 move-1h: message lookups through Messenger

Quoted image and forwarded message lookups now use the plugin's Messenger port.
The AstrBot adapter calls the same actions with string IDs and normalizes non-dict
results to an empty dict. Existing result handling and exception handling are unchanged.
`MediaMixin` and `PhoneMixin` inherit `PortsMixin`; its messenger accepts a missing
context, so a standalone media mixin can use a bot without a plugin context.
No switch or dependency is added. No files outside the card are changed.

`tests/test_lookup_ports.py` covers both lookups, non-dict results, missing bots and
refusal of an action outside the allowlist. It also checks a standalone media mixin
without context and that the plugin MRO contains one `PortsMixin`.

Full suite: 1077 tests OK outside the sandbox (main 7e92514 had 1072; +5 in `tests/test_lookup_ports.py`).
In the sandbox the same run passes except `test_brain_panel.InTheShell`, which needs a real browser.
No existing tests or golden files were changed.
