# 2026-10-31 move-5f: forget conversation history

Wire her own history into forgetting before the new program creates the store. When `_history` exists, forgetting a person or source messages removes matching history rows and reports the total. Entry-only deletes leave history alone. A history deletion error is logged and does not stop the other deletes. Without a store, the existing counts and behavior stay unchanged.

`_history_gate` checks each row's people, place, time, sources and message ID against the forget registry. An unreadable registry refuses the write. The new program will pass this gate when creating the store; this change adds no switch and does not create a store.

`tests/test_forget_history.py` covers the old counts, person and message deletes, entry-only deletes, registry checks, an unreadable registry, and a failed history delete. The method count in `tests/test_basics.py` is updated from 492 to 494 for the two new methods. Golden files and other existing tests are unchanged.

Full suite: 1283 tests OK outside the sandbox with `venv-ams-life` (main e39fb76 had 1276; +7 in
`tests/test_forget_history.py`). `tests/test_basics.py` counts the two new methods (492 -> 494: `_history_store`,
`_history_gate`), the one old test changed, as review agreed. Golden traces unchanged.
