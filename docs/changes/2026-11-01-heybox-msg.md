# 2026-11-01 heybox failure messages

Failed XiaoHeiHe responses now include a sanitized top-level `msg`, or `message` when
`msg` is absent, on the status warning. Control characters are removed, URLs, long
identifier-like strings and long numbers are replaced, and the message is limited to
60 characters. Non-string messages use a fixed placeholder. Successful responses keep
their existing logging behavior.

The response body, result, cookies, device ID, request URL and parameters are not
logged. Requests, signing and login behavior are unchanged. There is no new setting.
The AstrBot-specific test item is omitted under the November 1 instruction.

Validation: `tests.test_heybox`, `tests.test_heybox_page`, `tests.test_golden` and
`tests.test_basics` passed in the sandbox. `tests.test_golden_standalone` is run
outside the sandbox by the owner. The full suite was not run, as instructed.
