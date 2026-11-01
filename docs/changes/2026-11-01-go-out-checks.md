# Outbound checks (card 1h) — rework

Files: `mixin_browse.py`, `browse.py`, `mixin_turn.py`, `mixin_selfie.py`,
`real_browser.py`, `discretion.py`, `mixin_memory.py`, the new
`tests/test_go_out_checks.py`, and the old tests whose assertions this card changes
(`test_browse`, `test_browse_wire`, `test_selfie`, `test_real_browser`). No plugin method was
added (`test_basics` still counts 510).

Her going out is checked on what leaves her, not on what she may read.

## The send check on what would go out

`BrowseMixin._may_go_out` no longer looks at `global_memory`. A search's words, an
address's words and the words she would type into a page always go through the send
check's own look for this turn (the forbidden list of a reply, pieces and names,
local vectors, no model). A word or name it finds is not sent; the tool answers the
existing line `这个不能搜。` and says no more. `clean_query` (names and long numbers
out) and the address rules are unchanged.

A trip has no message of its own: its forbidden list is empty, but the names wall is
checked as for a reply. The owner's name and her own names are not names to keep out
of a search; everyone else's name is, when it is known from another place. The names
wall is the one `mixin_send_check._name_walls` already keeps for replies, so no new
plugin method is added.

## A web memory is a page, not a room's memory (B1, B2)

`browse.web_memory` keeps `where` as `web:<url>` for every page, whoever had her look it up
(her own trip, her own search, a link given anywhere). A page is never her own memory
(`self` is not used for a page), so `discretion.label`/`tag` always say `网上看到的，只是资料`.

A link given in a private chat is recorded apart: `origin["shared_in"] = "private:<qq>"`.
`discretion.label`'s web branch then gives `may=NO` outside that chat, and the rest of the
wall follows: `may_recall` and `verdict` drop the page outside it too (so it is not put in a
prompt there), and `discretion.tag` says it may only be brought up there. `make_origin` and
`origin_of` carry `shared_in` unchanged. When the one who gave the page is forgotten
(`asked_in` is the `gone` mark, written by `mixin_discretion._forget`) the page does not
become public again: of the two ways the second review allowed, this takes the first -- the
page is kept, and kept only of that chat, so because that chat is nobody's the page is
dropped in every group and in every other private chat (the second way, deleting the page
with the person, is not taken: a page is not the person's own, and older pages carry no
`shared_in` to delete by). `tests/test_go_out_checks.py` checks that a group and another
private chat both get DROP after the forget.

`mixin_memory._load_memory` and `_save_memory` take a room's entries with `_in_room`: an entry
whose `where` starts with `web:` is never one of them. So a page given in a group or a private
chat is not trimmed with that room's window, not squashed into a room summary (which loses its
address) and not overwritten by a concurrent save. `_library_places` (the place list
`page_consolidate` walks) skips `web:` places: tidying memories does not take a page for a room.

Older web memories (made before this card) are not migrated: they keep `web:<url>` or the old
`self`, and are no longer counted as a room's either.

## Fetching a page on its own small pool (B3)

`real_browser` fetches pages on its own `ThreadPoolExecutor` of `FETCH_WORKERS` (4) threads,
never the default one that embeddings, pictures and voice use. Name resolution and the fetch
itself both go through it (`_pool_call`). Each hop has one total deadline (`HOP_SECONDS`, 20s)
covering name, connect, request and read: `_read_all`/`_read_head` set the socket's timeout to
what is left and read in chunks, so a server that dribbles bytes is cut at the deadline, and the
socket is closed on the way out. A slot is held until its thread really ends, even when the
waiting coroutine times out. When no slot is free the request is aborted (`FetchBusy`, the block
reason `busy`) instead of queued behind a slow page.

The last look at a page's address after it was read (`_checked_free`, the second review's first
minor item) takes no fetch slot: a page that timed out may still hold every thread, and the
look failing must not lose a page that was read. An address this visit already checked is
answered from what it checked; one it never checked is resolved on the default thread.

## An HTTP proxy, by us (B4)

Only an HTTP proxy is spoken. `_proxy_for` reads the system proxy per address: a host in
`NO_PROXY` takes our own path (resolved and connected by the checked address); a proxy URL whose
scheme is not `http` (a SOCKS or `ALL_PROXY` setting) is refused and the request is aborted --
never taken for no proxy and dialled.

`_fetch_once_proxy` connects to the proxy itself and sends the request (absolute form for
`http`, `CONNECT` then TLS with the page's name for `https`), so the page has the same limits as
a direct fetch: `Accept-Encoding: identity`, `MAX_RESPONSE_BYTES` (2MB) cut, hop headers and
`Content-Encoding` removed before it is handed to the browser. Playwright's own
`context.request.get` is no longer used for a page. The pinned browser is launched with no
Playwright proxy at all (every request is fetched by us); the shared launch (the interactive
browser) still gets the system proxy but without a Playwright bypass list, so `NO_PROXY` is ours
to handle.

## Addresses (minor items)

`browse._bad_address` and `real_browser._public_address` now also refuse an IPv6 address that
carries an IPv4 address that is not public: IPv4-mapped, IPv4-compatible (`::127.0.0.1`),
IPv4-translated (`::ffff:0:7f00:1`), NAT64 (`64:ff9b::/96`, `64:ff9b:1::/48`), 6to4 and Teredo
(these read as global in 3.12, and some in 3.10). `_strict_url` uses the same rule.

Names are resolved once and their addresses tried IPv4 first (a home without IPv6 must not lose
a dual-stack site), and a hop whose address does not answer falls through to the next checked
address instead of failing (`_get_direct`). `_parse_response` drops `Content-Encoding` on every
path, proxy or not.

## The second review's smaller items

- A response is read only up to its `Content-Length` (`_read_response`/`_content_length`), not
  until the server closes or the deadline; `_read_all` now reads just the bytes still wanted.
  A chunked body, or one with no length, is still read until the close or the deadline, and the
  2MB cut stands. This goes for a direct fetch and for a proxied one.
- The TLS handshake is inside the connect's own budget, not a fresh one (`_connect` recomputes
  what the connect left), so one attempt cannot take twice the hop. `_get_direct` gives the
  whole hop one deadline, shared by the addresses it tries, and tries at most `MAX_ADDRESSES`
  (4) of them: a name that answers with many addresses cannot multiply the hop's time.
- An IPv6 address keeps its brackets in the `Host` header, in the proxy's absolute form and in
  the `CONNECT` line (`_host_in_url_form`).
- The slow-server test now bounds the whole exercise in `asyncio.wait_for(..., 2)`, so a
  deadline that is not watched fails there instead of hanging to the harness timeout; the new
  `Content-Length` test also asserts the read finishes in under a second.

## "此刻" set in a private chat

`mixin_selfie._now_line` keeps the old line when the state's `place` is empty, is
`self`, or is this same chat. If it was set in a private chat and is shown in another
place, only the rough where/doing is given, with `discretion.anonymize` over her known
names and without the original sentence, its start time or its duration. The state
format is unchanged.

## The browser resolves no name (R7, rewritten for Playwright)

`real_browser` now starts Chromium with `--host-resolver-rules=MAP * ~NOTFOUND`, so
the browser itself can resolve nothing. Every request is taken by
`context.route("**/*", ...)`: only `GET` is served, `data:` / `blob:` are passed back
to the browser, every other scheme is aborted. For each hop the host is resolved once,
every address is checked as public (the same rules as `browse.check_url`), and the
connection is made to the checked address with the original hostname in the `Host`
header and in TLS's SNI and certificate check. Redirects are followed by us, not by
the browser (at most five), and each hop is resolved, checked and connected again.
A page may make at most 60 subrequests; more are aborted. The interactive browser is
not touched by this card (it still uses the old route fetch), and neither is DeepSeek's
own fetch (the page is read on DeepSeek's side, not on this computer).

## Tests

New file `tests/test_go_out_checks.py` (offline, no files, and sealed: the real resolver, the
real sockets and the real TLS context are booby traps, and the system proxy is empty unless a
test sets it). 30 tests: forbidden words with `global_memory` off; a trip's names wall; web
memory origins (`web:<url>`, `shared_in`), label/tag and the real recall wall for a page given
in a private chat, a group and her own search; a page given in a private chat is DROP in a
group and in another private chat after the one who gave it is forgotten (`origin_of` keeps
`shared_in`); `_load_memory`/`_save_memory` never count a page
as a room's memory and `_library_places` skips `web:`; pages kept after a held reply (with
order check/keep/stop); "此刻" blurring; the launch rule; `_connect` itself connecting the
checked address with the name only for TLS (C2), and closing on a TLS failure; one resolution,
next address after a failed one, IPv4 first; embedded-IPv4 addresses blocked; blocked
subrequest hosts, `POST` and `ws://`; redirects followed per hop and stopped at the sixth; the
61st subrequest aborted; the 2MB cut and `Content-Encoding` removal; a body read only up to its
`Content-Length` (a server that keeps the connection open is not waited for); an IPv6 address
bracketed in the `Host` header, in the proxy's absolute form and in `CONNECT`; HTTP-only proxies
(SOCKS and `ALL_PROXY` refused, never direct); a `NO_PROXY` host on our checked-address path; a
proxied page fetched by us with `identity` (absolute form and `CONNECT`); the pinned browser
getting no Playwright proxy and the shared launch keeping the proxy without a bypass; a slow
server cut at the hop deadline while the default pool keeps working (the whole exercise bounded
by `asyncio.wait_for(..., 2)`); the fifth page at once refused; a route with no free thread
aborted; the final look at a page's address taking no fetch thread (with every slot taken,
`_checked` raises `FetchBusy` while `_checked_free` answers from the address the visit already
checked, and resolves one it did not off the pool).

Old tests were updated only where the card changes their behaviour: `test_browse` (a page is
`web:<url>`, `shared_in` for a private chat), `test_browse_wire` (origins; the trip page is
`web:<url>`), `test_selfie` (the "group" event of the now test really is a group: its
`unified_msg_origin` is a group's, so the test checks the private-to-group blurring it means to),
and `test_real_browser` (the pinned browser gets no Playwright proxy; the shared launch keeps
the proxy without a bypass list; a proxied private name is refused before any proxy fetch; the
extraction-timeout fake lets `_check_url` through, since the final look now runs off the pool).

Results inside this sandbox (Python 3.12, no network, temp dirs not writable, each file run on
its own): `test_go_out_checks` 30/30 passed. `test_real_browser` 56 tests: no assertion
failures; 15 `PermissionError` cases that write a screenshot or a ledger (the four
`AssertionError`s seen are those writes failing). `test_browse` 20 tests: no failures, 2
`PermissionError` teardown errors of its temporary directory. `test_basics` 11 tests: the
method count is still 510 and every other test passed; 2 `PermissionError`s writing its
temporary data folder. `test_discretion` 84 tests: 22 pass, no assertion failures; the other 62
are `PermissionError` errors from temporary directories. `test_selfie`
46 tests: 9 failures and 67 errors, all because its temporary folder cannot be written here
(`test_now_shared_expiry_and_failure` is one of them; with the data folder inside the worktree
its 9 pass). `test_browse_wire`, `test_send_walls`, `test_recall_walls` and `test_golden` could
not run here: every case stops at `TemporaryDirectory` with a `PermissionError`, so nothing of
them is checked on this machine. The full suite was not run; the dispatcher runs it outside.
