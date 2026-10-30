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

First-round files: `real_browser.py`, `tests/test_real_browser.py`, this change note.

Offline tests added: `test_article_extraction_uses_html_and_preserves_title`,
`test_article_extraction_falls_back_for_empty_short_error_and_missing`,
`test_article_extraction_timeout_falls_back`, `test_article_html_is_limited_by_utf8_bytes`,
`test_article_extraction_only_on_read_not_screenshot`, and
`test_trafilatura_never_fetches_or_extracts_from_url`.

Second round: `interactive_browser.BrowsingSession` provides bounded actions and snapshots;
the trip and accounting integration is left for the next round. The existing temporary browser
launch, request route, redirect probing and screenshot code in `real_browser.py` are shared.
Both switches `browser_enabled` and `browser_interactive_enabled` must be on; the latter defaults
to false. Open addresses must be supplied in the caller's allowlist, and typing is refused unless
the caller supplies a check that returns the cleaned text. The game entry uses only files resolved
inside the supplied games directory, and its route rejects all other requests; opening a web address
after entering game mode requires a new session. The owner reported
testing real Edge file routing for local, outside-directory and HTTP resources.

The snapshot uses Playwright `aria_snapshot(mode="ai")` and `get_by_ref`, with refs replaced at
each snapshot. browser-use is not used: the owner reported that it uses CDP, has many dependencies,
and enables telemetry and cloud synchronization by default. playwright-mcp is not used; its
snapshot/ref approach informed the choice. Constants: `MAX_STEPS=30`, `MAX_SECONDS=600`,
`MAX_ELEMENTS=60`, `VISIBLE_CHARS=3000`, `SNAPSHOT_CHARS=10000`, `SNAPSHOT_DEPTH=20`,
and `ACTION_SECONDS=20`. Allowed roles, keys, actions and login-name markers are also constants.
`read` returns wrapped article text followed by the updated snapshot; `screenshot` returns a
mapping containing the image path and updated snapshot. Before sharing an image, the caller must
apply the existing image-description and send checks.

Files additionally changed: `interactive_browser.py` (new), `tests/test_interactive_browser.py`
(new), `main.py`, `_conf_schema.json`. No trip, ledger, game content, or unrelated feature was
added. `test_shared_launch_closes_resources_when_setup_fails` covers shared setup cleanup, and
`test_default_switch_is_off` checks the new default.

Interactive offline tests: `test_snapshot_refs_and_refresh_after_each_action`,
`test_snapshot_limits_elements_and_material`, `test_stale_reference_after_navigation_is_rejected`,
`test_only_allowed_actions_and_keys`,
`test_open_requires_supplied_address`, `test_typing_requires_check_and_uses_cleaned_text`,
`test_typing_rejects_password_login_and_non_text_roles`, `test_post_is_blocked_and_reported`,
`test_click_redirect_checked_per_hop_and_local_rejected`, `test_subresource_redirect_is_not_followed`,
`test_popup_closed_and_checked_before_opening`, `test_filechooser_and_dialog_are_handled`,
`test_shared_browser_security_and_websocket`, `test_popup_initial_navigation_is_aborted_before_network`,
`test_unsafe_response_stops_session_reads`,
`test_step_and_time_limits_only_allow_finish`, `test_read_material_and_screenshot_refresh_snapshot`,
`test_read_uses_article_extraction`, `test_game_allows_only_files_inside_games`,
`test_disabled_switches_do_not_start_browser`, `test_challenge_is_not_read_or_screenshot`,
`test_close_releases_browser_context_and_lock`, `test_no_file_upload_api`, and
`test_interactive_switch_defaults_off`.
