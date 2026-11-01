# Heybox login request signing

The QR login endpoint returned `hkey` missing. Sign both login paths with the
existing signer and offset, as already done for the other allowed paths.
Login requests still do not count as the first signed read and remain available
when review is required. No settings or request parameters were otherwise changed.

Offline tests cover both login signatures, failure and review state, and log
redaction. The existing signature vectors and page tests also pass. AstrBot-specific
work is omitted under the November 1 instruction.

Validation: `tests.test_heybox` (29 run, one skipped),
`tests.test_heybox_page` (12 passed), `tests.test_golden` (2 passed), and
`tests.test_basics` (11 passed). The standalone golden test is to be run outside
the sandbox. The full suite was not run as instructed.
