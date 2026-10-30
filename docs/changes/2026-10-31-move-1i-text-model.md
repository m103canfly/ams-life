# 2026-10-31 move-1i: text model calls through ModelClient

Move the simple text-only model calls behind the model port. The four mixins now
inherit `PortsMixin` and call `self._model(provider).chat`; they read `reply.text`.
The calls cover LLM v2, persona compilation, memory summaries, event summaries,
insights and group impressions.

The adapter forwards the same supplied provider arguments and converts the same
completion text. Existing parsing, error handling and provider accounting stay in
place. No switches or files outside this card were changed.

`tests/test_model_ports_text.py` checks provider arguments, parsed replies and
errors at each call site, and the plugin's `PortsMixin` MRO. Its eight tests passed
in the sandbox. Existing tests and golden files were not edited.

Full suite: 1159 tests OK outside the sandbox (main bf4bbc3 had 1151; +8 in `tests/test_model_ports_text.py`).
In the sandbox the same run passes except `test_brain_panel.InTheShell`, which needs a real browser.
Golden traces unchanged.
