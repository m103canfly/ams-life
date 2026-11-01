# Outbound checks (card 1h)

Files: `mixin_browse.py`, `browse.py`, `mixin_turn.py`, `mixin_selfie.py`,
`real_browser.py`, the new `tests/test_go_out_checks.py`, and the old tests whose
assertions this card changes (`test_browse`, `test_browse_wire`, `test_selfie`,
`test_real_browser`). No plugin method was added (`test_basics` still counts 510).

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

## Where a web memory belongs

`browse.web_memory` now sets a page's origin by who had her look it up: her own
search or her own trip -> `self` (recalled anywhere); a link given in a group -> that
group, openly; a link given in a private chat -> that private chat, privately. The
address in the origin is no longer used for new pages; older web memories are not
migrated and keep their public origin. `asked_in` (this chat and who asked) is kept
exactly as before, and `_remember_web` takes the origin as an optional argument.

A page's origin carries no people and no message ids: someone deleted does not take
the page with them. `_browse_keep_reply` marks each page with where it came from
(`from: given | search`), which `_tool_read` records.

## Reply pages are kept after the last look

`mixin_turn._after_reply` now calls `_browse_keep_reply` after the send check instead
of before it, and still calls it when the check held the reply back. The pages she
read are her own reading, not the words of the reply, so they are kept either way;
nothing was sent. Because a group's web memory now belongs to that group's window,
the library order can differ from before (an assertion in `test_browse_wire` now
compares the set of kept pages).

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
A page may make at most 60 subrequests; more are aborted. The system-proxy path is
unchanged: the proxy resolves and the browser's request goes through it. The
interactive browser is not touched by this card (it still uses the old route fetch),
and neither is DeepSeek's own fetch (the page is read on DeepSeek's side, not on this
computer).

## Tests

New file `tests/test_go_out_checks.py` (offline, no files): forbidden words with
`global_memory` off; a trip's names wall; web-memory origins and recall permission;
pages kept after a held reply (with order check/keep/stop); "此刻" blurring; the launch
rule; one resolution and connecting the checked address (Host/SNI by name); blocked
subrequest hosts, `POST` and `ws://`; redirects followed per hop and stopped at the
sixth; the 61st subrequest aborted. 11 tests, all pass.

Old tests were updated only where the card changes their behaviour:
`test_browse` (a new web memory is `self` for a trip, a group for a group, a private
chat for a private chat), `test_browse_wire` (origins; kept pages compared as a set),
`test_selfie` (one now-line assertion: set in a private chat, shown in a group), and
`test_real_browser` (the request fixtures now go through our own fetch: launch args,
GET-only, redirects followed and counted, the redirect/permission checks).

Results inside this sandbox (no network, no playwright, temp dirs partly read-only):
`test_go_out_checks` 11/11 passed; `test_browse` had only the two `PermissionError`
teardown errors of its temporary directories; `test_real_browser` had no assertion
failures, only the `PermissionError` cases that write a screenshot or a temp directory;
`test_interactive_browser` 39 passed and 21 `PermissionError`s writing its ledger/temp
files. `test_browse_wire`, `test_browse_standalone`, `test_send_walls`,
`test_recall_walls`, `test_selfie`, `test_golden`, `test_golden_standalone` and
`test_basics` could not run here (temp subdirectories are not writable in the
sandbox); the `browse_cases.py` reply/leak/trip/trip_switch scripts were run directly
with a data folder inside the worktree and their results match the updated
expectations. The full suite was not run; the dispatcher runs it outside.
