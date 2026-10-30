# 2026-10-30 cx-clicky-browser: read article text with trafilatura

The owner approved the recommendation on sign-off board item 83; trafilatura 2.3.1 was
reported installed. Browser page reads now try to extract the article from the already loaded
HTML, without comments and with tables, favoring precision. The title and the existing material
wrapping and length limit stay the same. DeepSeek reads and screenshots are unchanged.

The optional package is imported only when used; there is no new switch or requirements entry.
If it is missing, extraction fails or times out, or the result is below 200 characters or one
quarter of visible text, the browser uses the original visible text. `HTML_MAX_BYTES` limits
parser input to 2 MiB of UTF-8; `EXTRACT_SECONDS` limits the content and extraction wait to
5 seconds. A timed-out worker thread cannot be forcibly stopped. No trafilatura network
fetch is used.

Files: `real_browser.py`, `tests/test_real_browser.py`, this change note. No work outside the
article extraction part of the card was included.

Offline tests added: `test_article_extraction_uses_html_and_preserves_title`,
`test_article_extraction_falls_back_for_empty_short_error_and_missing`,
`test_article_extraction_timeout_falls_back`, `test_article_html_is_limited_by_utf8_bytes`,
`test_article_extraction_only_on_read_not_screenshot`, and
`test_trafilatura_never_fetches_or_extracts_from_url`.
