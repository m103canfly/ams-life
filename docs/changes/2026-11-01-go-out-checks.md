# Outbound checks and web memory (card 1h)

## Behavior

Search words, addresses and typed text use the current turn's forbidden items
regardless of `global_memory`. Checks run before cleaning and before sending.
A refusal says only `这个不能拿去搜。`. A trip has no forbidden items from a
reply, but uses the existing names wall. Owner and character names are exempt
from that trip wall. Query cleaning and URL admission remain in place.

A link supplied in a private chat produces a private memory from that chat.
A group-supplied link produces a public memory from that group. Her own search
and trip pages have a self origin. `asked_in` still records who asked her.
Deduplication includes the origin so separate private sources cannot collide.
Existing public web memories are not migrated or rewritten.

The reply order is: account for browsing, check the registry, shape the reply,
run the send check, then keep the pages by their own origins. Pages are kept
before returning when the check holds the reply back. Silent and empty replies
also keep their pages. Page text never comes from her reply. A private now
state is generalized outside its own chat; doing is anonymized and extra detail
is omitted. Self and empty now origins keep the existing rendering.

## Memory list order

The remaining wire-test failure concerned list position. `_save_memory` in
`mixin_memory.py` regroups entries by room when it saves that room. A newly
group-scoped web memory therefore moves relative to a self-scoped page on the
next room save. The list has no chronological contract here.

The approved assertion option was chosen: `assertCountEqual` checks that both
URLs remain exactly once. The origin, text and requester assertions remain.
`mixin_memory.py` is unchanged. This avoids changing other memory behavior just
to preserve incidental positions. Older origin and forgetting assertions now
expect chat/self origins; forgetting the supplier removes the supplied page,
while a self-sourced search page remains with a forgotten-requester marker.

## Browser requests and proxies

The read-only browser launches with `--host-resolver-rules=MAP * ~NOTFOUND`.
`context.route("**/*")` owns HTTP requests. Only GET is allowed. Other network
schemes are aborted; data and blob URLs remain browser-local. WebSockets,
service workers and WebRTC retain their existing protections.

Each request and redirect resolves once, rejects non-public addresses and
connects a socket to the checked numeric address. Host and TLS SNI/certificate
verification use the original hostname. The bridge follows at most five
redirects and fulfills the final response. It reports the final fetched URL.
Cross-host redirects drop cookie and authorization request headers. A page
allows one document and sixty subrequests. Requests retain the twenty-second
timeout; response bodies use the existing two-MiB byte limit. Other browser
timeouts and screenshot limits are unchanged.

HTTP system proxies are supported. HTTPS uses CONNECT to the target hostname;
HTTP uses an absolute request URL without its fragment. A local proxy address
is allowed and is not checked as a target page. Proxy credentials go only to
the proxy and are never logged. Unsupported proxy protocols refuse the read,
log only the protocol, and never fall back to a direct connection. Hosts in
the system bypass list connect directly through the checked-IP transport.
Chromium itself receives no proxy configuration in the read-only path because
the bridge performs every network request.

DeepSeek's remote page fetch resolves and connects on DeepSeek's own machines;
that path is outside this change. Interactive browsing keeps its existing
launch and routing helpers. AstrBot-specific behavior is not maintained under
the owner's November 1 instruction. No plugin methods or switches were added.
The merged main already expects 511 methods; `test_basics` is unchanged.

## Offline test changes

`test_go_out_checks` adds fourteen tests for the off-switch send check, blocked
searches, trip names and exemptions, memory origins, blocked-reply save order,
private now rendering, DNS pinning, Host/SNI, methods, redirects, request count
and proxy tunneling.

The new test names are:

```text
PinnedBrowser.test_launch_disables_browser_dns
PinnedBrowser.test_connection_uses_checked_address_and_original_host
PinnedBrowser.test_transport_preserves_host_and_tls_name
PinnedBrowser.test_proxy_connects_to_proxy_and_tunnels_original_host
PinnedBrowser.test_local_and_non_get_requests_abort
PinnedBrowser.test_redirects_are_checked_and_bounded
PinnedBrowser.test_sixty_first_subrequest_aborts
WebOrigin.test_private_group_and_self_recall
Outbound.test_forbidden_words_checked_when_global_memory_off
Outbound.test_search_does_not_send_forbidden_words
Outbound.test_blocked_reply_keeps_pages_after_check
Outbound.test_link_origin_and_search_origin_are_distinct
Outbound.test_trip_uses_name_wall_with_no_forbidden_items
NowLine.test_private_now_is_anonymized_elsewhere
```

The shared `test_real_browser` fake now intercepts our resolver and IP
transport. Playwright fetch/get are forbidden. Real `getaddrinfo`, socket
connect/connect_ex and create_connection throw and must remain unused.
Windows asyncio's wake-up socketpair and thread dispatch are also replaced in
these tests so its internal loopback channel never reaches a real socket.
Two initial fixture runs exposed that wake-up setup; the corrected fixture
passed all 61 tests with the network guards untouched.

Existing test intentions are retained. The changed cases are:

- `test_context_uses_system_https_proxy_and_bypass` and
  `test_context_uses_http_proxy_or_omits_proxy` assert the bridge's selected
  proxy rather than a Chromium proxy option.
- `test_article_extraction_timeout_falls_back` lets the new fetch helper run
  while timing out only extraction.
- `test_launch_and_context_are_temporary_and_sandboxed` adds the DNS rule.
- `test_request_method_and_public_addresses` now rejects HEAD as required.
- The five fetch/fulfill/abort error tests inject errors at `transfer`, the
  new fake transport seam. Error containment, counts and redacted logs remain.
- The main redirect, redirect-loop, response-redirect and screenshot refusal
  cases now exercise intercepted requests. They retain private-target refusal,
  per-hop checks, the hop bound, final URL reporting and partial-file cleanup.
  Navigation starts at the original URL; the bridge follows redirects.
- `test_route_fetch_aborts_redirects_and_fulfills_other_responses` and
  `test_main_route_redirect_after_preflight_is_aborted` keep rejecting redirects
  without a location and assert that Playwright fetch was not used.
- `test_route_source_never_continues_unchecked` now exercises routes: only
  data/blob continue; network schemes must be fetched or aborted.
- `test_one_page_at_a_time` uses the new transport fake and retains its
  concurrency assertion.

New browser tests cover HTTP proxy CONNECT/absolute URLs and credentials,
unsupported-protocol refusal without credential logging, bypass to a checked
IP, numeric socket connections with Host/SNI, TLS failure cleanup and response
size cleanup. The shared fake interfaces used by interactive tests remain.
Their added names are `test_unsupported_proxy_logs_only_protocol_and_never_connects`,
`test_no_proxy_uses_checked_ip_without_proxy`,
`test_http_proxy_connect_and_absolute_request`,
`test_direct_connection_uses_numeric_socket_host_and_tls_name` and
`test_tls_failure_and_oversize_response_close_connection`.

## Validation (2026-11-01)

The designated sandbox runner ran one file at a time. Final summaries:

```text
tests.test_browse_wire: Ran 20 tests in 2.654s | OK
tests.test_go_out_checks: Ran 14 tests in 0.049s | OK
tests.test_real_browser: Ran 61 tests in 1.027s | OK
tests.test_interactive_browser: Ran 60 tests in 0.697s | OK
tests.test_browse: Ran 20 tests in 0.016s | OK
tests.test_turn_tools: Ran 10 tests in 0.016s | OK
tests.test_selfie: Ran 46 tests in 1.841s | OK
tests.test_golden: Ran 2 tests in 3.838s | OK
tests.test_basics: Ran 11 tests in 0.040s | OK
```

The golden fixtures are unchanged. The full suite was not run.
`test_golden_standalone` remains assigned to the owner outside the sandbox.
No pages, live data, dependencies or service settings were changed. No network
requests, commits, permission changes or elevated commands were used.
Added-line scans found only the fictional long numbers 10001, 10003, 20002
and 900001, no username paths and no token/private-key literal patterns.
`git diff --check` passed. Both new files have exactly one final newline.
