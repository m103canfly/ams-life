# 2026-10-30 cx-clicky-browser: read article text with trafilatura

The interactive browser uses Playwright's built-in `aria_snapshot(mode="ai")` and `get_by_ref`;
the owner verified both in Playwright 1.64.1 and reported that playwright-mcp uses the same
approach. browser-use is not used: the owner reported that it no longer uses Playwright, has over
30 dependencies, and enables telemetry and cloud synchronization by default. Article extraction
uses optional trafilatura (owner sign-off board item 83).

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

Second round: `interactive_browser.BrowsingSession` provides bounded actions and snapshots.
The existing temporary browser
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
(new), `main.py`, `_conf_schema.json`. `test_shared_launch_closes_resources_when_setup_fails` covers shared setup cleanup, and
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

Third round: the read-only browser and interactive sessions wait at most `LOCK_WAIT_SECONDS=3`
for the shared lock; a busy read or screenshot returns failure to its existing accounting and
fallback. With all three browsing switches enabled, the trip adds `ams_browser_action` for open,
click, type, press, scroll, back, read and finish. Screenshot is intentionally absent from trips;
sharing screenshots remains in the reply flow. Search and read tools remain available. Open is
limited to search results, current snapshot links and addresses already allowed on the trip, with
the existing outbound check. Typing goes through `clean_query` and the outbound check. Each model
round performs at most one browser action; 30 session steps and 600 seconds end the action phase,
release the browser and prompt for the existing JSON conclusion. Every model response's usage is
charged to the browser ledger. Successful interactive reads join the trip's seen pages.

The ledger and dashboard add `interactive_steps`, `interactive_clicks`, `interactive_types` and
`interactive_blocked`. Steps count actions accepted by the session, clicks and types count their
attempted session actions, and blocked counts include blocked requests and rejected actions without
double counting a single rejected request. The new counters are optional in old ledger rows; default
disabled status retains the previous panel shape. No game content or unrelated feature was added.
Files additionally changed: `browse.py`, `mixin_browse.py`, `pages/dashboard/app.js`, and the
second-round browser and tests above. `tests/test_basics.py` method count is unchanged.

Third-round offline tests: `test_busy_session_limits_wait_for_read_screenshot_and_session`,
`test_busy_browser_keeps_deepseek_text_and_counts_failed_read`,
`test_snapshot_link_allowlist_tracks_current_snapshot`,
`test_trip_interactive_tools_typing_accounting_and_memory`,
`test_trip_opens_only_search_and_current_page_links`, `test_trip_link_open_also_passes_outbound_check`,
`test_trip_switch_off_keeps_old_two_tools`,
`test_trip_thirty_steps_forces_final_without_tools`, `test_trip_time_limit_closes_before_final`, and
`test_trip_only_executes_one_browser_action_per_model_round`. Existing reply tool tests still cover
the two-tool reply flow.

The owner reported three findings from a local Edge test. First, background POST requests could
make a successful GET navigation report that the action was blocked. All non-GET/HEAD requests
are still blocked and counted, but only a blocked main-frame navigation marks the action as blocked.
Second, a blocked form navigation could leave the page at a browser error URL. The session now
reloads the previous page through the checked redirect path, returns a fresh snapshot with the
blocked message, and closes if recovery fails. Third, Playwright's requests did not use the system
proxy on that machine. Shared browser context setup now uses the system HTTPS or HTTP proxy and its
bypass list when present; proxy addresses are not logged or passed to page checks.

Offline checks added: `test_background_post_is_counted_without_failing_action`,
`test_enter_navigation_survives_background_post`, `test_child_frame_post_is_blocked_without_failing_action`,
`test_blocked_main_post_restores_page_and_fresh_snapshot`, `test_enter_blocked_main_post_also_restores_page`,
`test_failed_navigation_recovery_ends_session`, `test_context_uses_system_https_proxy_and_bypass`,
`test_context_uses_http_proxy_or_omits_proxy`, `test_proxy_does_not_bypass_page_address_checks`,
`test_interactive_session_uses_shared_proxy_settings`, `test_popup_post_is_counted_and_not_replayed`,
`test_proxy_lookup_failure_keeps_browser_available`, and
`test_proxy_address_is_not_logged_on_browser_error`. The existing
`test_post_is_blocked_and_reported` now accepts the recovered snapshot after the blocked message.
