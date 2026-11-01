# Standalone browsing trips

Standalone trips previously tried to obtain an AstrBot provider and could not
run. They now use the neutral model and the existing search and read handlers,
with trip quotas and only search results allowed as read addresses. Notes and
sharing wishes are kept only for pages read on the trip. Each model call is
counted in both the browser ledger and the daily spending account. A hard daily
budget or an exhausted browser budget stops further model calls.

Both browse_enabled and browse_trips_enabled remain off by default. The
interactive browser switch does not enable interactive trips in standalone;
the ordinary trip is used and an informational message is logged. Do not enable
trips on the live installation until the next card's pre-browsing work is done.
The AstrBot trip branch is unchanged, and AstrBot-specific new tests are omitted
under the November 1 instruction. No files outside this card were changed.

Validation: test_browse_standalone (6), test_browse (20), test_browse_wire (20),
test_interactive_browser (60), test_standalone_no_astrbot (4), test_golden (2),
and test_basics (11) passed separately in the sandbox. The owner runs
test_golden_standalone outside the sandbox. The golden files were not changed.
No full suite was run, per the instruction.
