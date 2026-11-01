# Standalone file logging

The standalone app can run without a visible console. The optional `--log` path
adds a UTF-8 rotating file handler at INFO, with 2 MiB files and five backups.
Existing startup messages also go to the file. The handler is removed and closed
when the app stops, including after a refused data directory. Without the option,
file logging remains disabled and console output is unchanged. The change is
limited to the files named on the card.

Sandbox validation: test_app ran 15 tests (10 skipped without aiohttp), test_golden
passed 2, and test_basics passed 11. The aiohttp-dependent tests and
test_golden_standalone require external validation. The full suite was not run.
