# 2026-10-31 - Close test databases before deleting temporary data

Windows cannot remove an open SQLite file. Other tests import `test_basics` for its
setup and can create plugins in its data directory after module cleanup. A single
registered `atexit` callback now collects garbage, closes databases on surviving
plugins, and removes the registered directories. Module cleanup still runs earlier.
Test behavior and golden files are unchanged. There is no switch or plugin code change.

| Test module | Cleanup before directory removal |
| --- | --- |
| `test_basics.py` | At module cleanup, close tracked plugins; at exit, close surviving plugins' forget registries and vector stores before removing the directory. |
| `test_body_heart.py` | Remove its directory at module cleanup and again at exit if recreated. |

The two `atexit` subprocess scripts in `test_stage_replay.py` use pure helpers and
do not open these databases. `CloseBeforeDelete.test_close_plugin_databases_before_removing_directory`
checks close order, missing stores, and cleared references.
`CloseBeforeDelete.test_exit_cleanup_handles_database_opened_after_module_cleanup`
checks a reopened directory and databases as well as one-time exit registration.

## Tests

Full suite: 1242 tests OK outside the sandbox (main 32662f1 had 1240; +2 in `tests/test_close_before_delete.py`),
with the owner's Python and with `venv-ams-life`. With TEMP pointed at an empty folder, each run leaves
nothing behind; so does running `test_basics` or `test_body_heart` alone. Golden traces unchanged.
