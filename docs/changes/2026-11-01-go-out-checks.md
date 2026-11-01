# Outbound checks and web memory (card 1h)

Sixth repair of PR #180, based on head `e04dd47` and main `8e90f89`.

## Behavior

Search words, addresses and typed text use the current turn's forbidden items
regardless of `global_memory`. Checks run before cleaning and before sending.
A refusal says only `这个不能拿去搜。`. A trip has no forbidden items from a
reply, but uses the existing names wall. Owner and character names are exempt
from that trip wall. Query cleaning and URL admission remain in place.

All pages keep their `web:<url>` origin and public visibility. Only privately
supplied links add `origin.shared_in = private:<id>`. Group links, her own
searches and trips have no sharing boundary. `asked_in` still records who
asked her. Deduplication includes the origin and its private sharing boundary.
Existing public web memories are not migrated or rewritten.

The reply order is: account for browsing, check the registry, shape the reply,
run the send check, then keep the pages with their sharing boundaries. Pages are kept
before returning when the check holds the reply back. Silent and empty replies
also keep their pages. Page text never comes from her reply. A private now
state says only where she is and that she is chatting privately outside its
own chat. The doing and detail are omitted. Self and empty now origins keep
the existing rendering.

## Fifth repair: B1 and B2

The fourth repair incorrectly changed web origins into room/self origins.
That removed the web label and requester discretion. It also admitted pages
to room documents, where trimming, summarization and whole-room replacement
could affect them. The changed list order was a symptom of this mistake.

The fifth repair restores `web:<url>` and the original ordered wire assertion.
The room replacement algorithm is unchanged. Pages never
enter a room document. `origin_of` preserves `shared_in`; label, verdict and
recall permission enforce it. Merge retains the source boundaries. The actual
recall test covers both global-memory settings, private recall with the web
tag, denial elsewhere, requester-name protection and room save isolation.
Group pages again survive forgetting the requester with an `asked_in` marker.

## Sixth repair: K1 and follow-ups

The panel's forced consolidation enumerated `_library_places`, which included
web origins from entries and room metadata. It could treat two reads of one
URL as a room, then produce a summary or candidate fact without `shared_in`.
The only production-code change in this repair excludes `web:` places in that
enumerator. Ordinary places keep their existing order and consolidation path.
No summary, candidate, label or recall algorithm was changed.

`WebOrigin.test_panel_consolidation_leaves_private_web_pages_uncompressed`
stores two different private page texts at the same URL using `_remember_web`,
then calls the real `page_consolidate`. It includes an old web room key and
an ordinary group as a control. Only the group is visited with force enabled.
The web entries stay unchanged, no summary is created and group recall cannot
retrieve either private text.

`FetchLimits.test_fifth_simultaneous_fetch_is_rejected_by_real_admission_limit`
holds four fake fetches concurrently and keeps the production semaphore. The
fifth must abort before any of the first four finishes. The test does not
replace admission with a one-slot semaphore; changing the real limit to an
unlimited one would queue the fifth request and fail this test.

Tests now use `new_event_loop` with explicit task, async-generator and executor
cleanup instead of the Python-3.11-only runner. Polling still avoids a real
Windows loopback wake-up socket. Fake transports and real DNS/socket guards
remain. The TLS description below is corrected: the handshake is bounded by
the remaining socket timeout, not interrupted by the Timer.

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
outer timeout; response bodies use the existing two-MiB byte limit. Other
browser timeouts and screenshot limits are unchanged.

## Fifth repair: B3 and small items

Network fetches use a dedicated four-worker executor. A nonblocking admission
gate rejects work when all four slots are occupied. No browser fetch enters
the shared default executor or waits in an unbounded queue. Slots stay occupied
until the worker actually exits, including after coroutine cancellation.

Each redirect hop has a monotonic total deadline. Its watchdog shuts down and
closes the watched socket during connect, proxy CONNECT, HTTP headers and
chunked body reads. TLS wrapping detaches the raw socket during the handshake,
so the Timer does not interrupt that handshake. The remaining time is set as
the socket timeout before wrapping; that timeout bounds the TLS handshake.
The wrapped socket is watched after the handshake. Cancellation closes the
currently watched socket. Responses and
connections close on completion or failure. Address retries share that hop's
deadline and try only the original checked batch. Proxy connections also use
watched sockets. OS DNS work remains confined to the bounded browser executor.

Requests force `Accept-Encoding: identity`. Fulfilled responses remove
`Content-Encoding`; the bridge never decompresses a response. Fetched URL
comparisons ignore fragments. IPv4-compatible, 6to4 and the well-known NAT64
prefix reject embedded non-public IPv4 addresses; the local NAT64 /48 is also
rejected. The private now test starts at `_set_now` and requires the generic
private-chat line outside that chat.

## Proxies and remaining boundaries

HTTP system proxies are supported. HTTPS uses CONNECT to the target hostname;
HTTP uses an absolute request URL without its fragment. A local proxy address
is allowed and is not checked as a target page. Proxy credentials go only to
the proxy and are never logged. Unsupported proxy protocols refuse the read,
log only the protocol, and never fall back to a direct connection. Hosts in
the system bypass list connect directly through the checked-IP transport.
Chromium itself receives no proxy configuration in the read-only path because
the bridge performs every network request.

The proxy still resolves the target hostname again. That resolver is outside
the local checked-IP guarantee, as accepted in the card. This is a remaining
DNS rebinding risk at the proxy. pushState and relative paths after redirects
are deferred usability issues; this repair does not change them.

DeepSeek's remote page fetch resolves and connects on DeepSeek's own machines;
that path is outside this change. Interactive browsing keeps its existing
launch and routing helpers. AstrBot-specific behavior is not maintained under
the owner's November 1 instruction. No plugin methods or switches were added.
The merged main already expects 511 methods; `test_basics` is unchanged.

## Offline test changes

`test_go_out_checks` has nineteen tests for the off-switch send check, blocked
searches, trip names and exemptions, memory origins, blocked-reply save order,
private now rendering, actual recall, room isolation, DNS pinning, Host/SNI,
embedded addresses, methods, redirects, request count and proxy tunneling.

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
WebOrigin.test_real_recall_keeps_private_pages_outside_rooms
WebOrigin.test_shared_origin_survives_origin_copy_and_merge
WebOrigin.test_panel_consolidation_leaves_private_web_pages_uncompressed
Outbound.test_forbidden_words_checked_when_global_memory_off
Outbound.test_search_does_not_send_forbidden_words
Outbound.test_blocked_reply_keeps_pages_after_check
Outbound.test_link_origin_and_search_origin_are_distinct
Outbound.test_trip_uses_name_wall_with_no_forbidden_items
NowLine.test_private_now_from_set_now_is_generic_elsewhere
EmbeddedAddresses.test_embedded_private_ipv4_is_refused
EmbeddedAddresses.test_public_nat64_is_allowed
```

The shared `test_real_browser` fake now intercepts our resolver and IP
transport. Playwright fetch/get are forbidden. Real `getaddrinfo`, socket
connect/connect_ex and create_connection throw and must remain unused.
Windows asyncio's wake-up socketpair and thread dispatch are also replaced in
these tests so its internal loopback channel never reaches a real socket.
Most browser tests run the fake bridge inline. The executor regression test
uses real dedicated/default worker threads with in-process fake sockets and a
timer pulse instead of a Windows loopback wake-up pipe. It proves that slow
bytes expire, the socket closes, the default executor works, excess work aborts
and the browser worker slot is released. All 67 tests pass with the real network
guards untouched.
Both test executors have one worker, so using the default executor for the slow
fetch would prevent its other job from completing. The second request must be
rejected while the first is still active, rather than after waiting in a queue.

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

Fifth-repair browser tests add:

```text
Browser.test_fragment_does_not_hide_fetched_document
Browser.test_response_encoding_is_removed_before_fulfill
Transport.test_other_checked_addresses_are_tried_without_resolving_again
Transport.test_deadline_closes_socket_during_slow_headers
FetchLimits.test_slow_body_expires_without_using_default_pool_or_queuing
FetchLimits.test_fifth_simultaneous_fetch_is_rejected_by_real_admission_limit
```

## Fifth-repair validation (2026-11-01)

The designated sandbox runner ran one file at a time. Final summaries:

```text
tests.test_browse_wire: Ran 20 tests in 2.640s | OK
tests.test_go_out_checks: Ran 18 tests in 0.085s | OK
tests.test_real_browser: Ran 66 tests in 1.623s | OK
tests.test_interactive_browser: Ran 60 tests in 0.741s | OK
tests.test_browse: Ran 20 tests in 0.016s | OK
tests.test_turn_tools: Ran 10 tests in 0.017s | OK
tests.test_selfie: Ran 46 tests in 1.942s | OK
tests.test_send_walls: Ran 10 tests in 0.081s | OK
tests.test_recall_walls: Ran 10 tests in 0.064s | OK
tests.test_browse_standalone: Ran 6 tests in 0.105s | OK
tests.test_golden: Ran 2 tests in 4.026s | OK
tests.test_golden_standalone: Ran 6 tests in 0.371s | FAILED (failures=4)
tests.test_basics: Ran 11 tests in 0.041s | OK
```

The standalone golden file was attempted as requested for this repair. Its
basic/full scenarios in both runners failed at `panel_api` import because the
designated Python lacks `aiohttp`. All four failures have the same missing
dependency; they did not reach golden comparison. Two other tests passed.
No dependency was installed, no fixture was changed and no retry was made.
The reviewer subsequently reported all six standalone golden tests passing
and a full run of 1923 tests passing on `e04dd47`. Those are reviewer results
for the fifth repair, not a full-suite run of the sixth repair here.
The other twelve files passed. The golden fixtures are unchanged and
`test_golden` passed. The full suite remains assigned to the reviewer.
No pages, live data, dependencies or service settings were changed. No network
requests, commits, permission changes or elevated commands were used.
Added-line scans check fictional identities, username paths and token/private-key
literal patterns. No real credentials or identifiers are used in the fixtures.
`git diff --check` passed. The test and change-note files end in one newline.

## Sixth-repair validation

Each requested file ran separately through the designated sandbox runner.
`test_discretion` is the existing consolidation/forgetting regression file.

```text
tests.test_go_out_checks: Ran 19 tests in 0.096s | OK
tests.test_real_browser: Ran 67 tests in 1.648s | OK
tests.test_browse_wire: Ran 20 tests in 2.583s | OK
tests.test_browse: Ran 20 tests in 0.017s | OK
tests.test_send_walls: Ran 10 tests in 0.085s | OK
tests.test_recall_walls: Ran 10 tests in 0.063s | OK
tests.test_discretion: Ran 84 tests in 33.959s | OK
tests.test_golden: Ran 2 tests in 3.914s | OK
tests.test_basics: Ran 11 tests in 0.041s | OK
```

All nine files passed (243 tests). No full suite or mutations were run here.
The golden fixtures and plugin method count are unchanged. The repair touches
only `_library_places`, the two test files and this note. No network, real
local port, dependency installation, permission change or commit was used.
