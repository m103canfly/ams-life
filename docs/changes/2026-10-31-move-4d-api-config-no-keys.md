# 2026-10-31 move-4d: do not save submitted API keys in standalone

The standalone panel stores keys separately, but a direct API configuration request could
still write a submitted key into the plain configuration file.

## What changed

- `page_api_config` keeps the previously saved key when `_key_store` is present and is not
  `None`. A nonempty submitted key is ignored and logged by configuration kind only.
- Other fields are saved as before. AstrBot, which has no `_key_store`, keeps its existing
  key handling. The model lookup endpoint is unchanged.
- Added four offline tests for the standalone and AstrBot paths, including the saved file and
  the log. No files outside the card are changed.

## Test results

- `tests.test_api_config_keys`: Ran 4 tests in 0.034s | OK
- `tests.test_panel_api`: Ran 20 tests in 0.004s | OK (skipped=17)
- `tests.test_golden`: Ran 2 tests in 4.734s | OK
- `tests.test_basics`: Ran 11 tests in 0.055s | OK
- `tests.test_golden_standalone`: to be run by the owner outside the sandbox; aiohttp is needed.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
