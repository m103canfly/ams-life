# 2026-10-31 - Move 5e-2 model port

The new program needs its own model client where the plugin previously selected
an AstrBot provider. `model_for` now accepts a `ModelClient` directly, and
`_provider_for` selects `_neutral_model` when present. In the new program this
one model is used for every function; AstrBot provider IDs configured per
function are ignored. AstrBot without `_neutral_model` keeps its existing route.

`_SpendingModel` counts normalized model usage once under the existing spending
conditions. The retry uses the model port and the same spending wrapper. AstrBot
still counts the original provider response, including raw cache usage. The
adapter preserves the retry arguments and response text. Retry tokens are the
sum of normalized usage and are recorded only when nonzero. An AstrBot response
with a usage object containing three zero values formerly recorded zero; it now
records no token count. AstrBot 4.29.3 `core/provider/entities.py` lines 331–333
define `TokenUsage.total` as `self.input_other + self.input_cached + self.output`.

No new switch or dependency was added. Vision and browsing remain outside this
card. No files outside the card changed.

Tests in the sandbox, one file at a time:

- `tests.test_model_port`: Ran 8 tests in 0.009s | OK
- `tests.test_basics`: Ran 11 tests in 0.041s | OK
- `tests.test_golden`: Ran 2 tests in 3.553s | OK
- `tests.test_send_check`: Ran 23 tests in 8.236s | OK
- `tests.test_attention`: Ran 38 tests in 5.444s | OK
- `tests.test_model_ports_text`: Ran 8 tests in 0.011s | OK
- `tests.test_model_ports_vision`: Ran 4 tests in 0.003s | OK
- `tests.test_autonomy_ports`: Ran 5 tests in 0.210s | OK
- `tests.test_slang`: Ran 14 tests in 0.308s | OK
- `tests.test_discretion`: Ran 84 tests in 30.903s | OK

Outside the sandbox the same 10 modules pass one at a time with `venv-ams-life`; the golden
files are unchanged.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
