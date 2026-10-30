# 2026-10-31 - Test temporary directory cleanup

Test runs left temporary directories behind. Module-level and subprocess directories now
register removal at process exit. The named test fixtures register cleanup immediately
after creation, including when setup fails. Test behavior and golden files are unchanged;
there is no switch and no plugin change.

`TempCleanup.test_mkdtemp_files_mention_cleanup` checks test sources for a cleanup word
in files using `mkdtemp`. This is a coarse file-level check, not proof of cleanup for
each directory.

## Temporary directory inventory

| Location | Cleanup |
| --- | --- |
| `test_basics.py`, `test_body_heart.py` | `atexit` removes each module directory. |
| `test_stage_replay.py` (two subprocess scripts) | `atexit` removes each subprocess directory. |
| `test_look.py`, `test_stickers.py` (`OwnerDeleted`) | `addCleanup` removes each method directory. |
| `test_messenger.py`, `test_adapter_astrbot.py` | `addClassCleanup` removes each optional class directory. |
| `test_brain_panel.py` (`InTheShell`) | `addClassCleanup` removes the browser profile and redirected TEMP/TMP directory, ignoring cleanup errors. |
| `TemporaryDirectory` calls | Context managers, explicit fixture cleanup, or registered cleanup; the object also has a finalizer. |
| `NamedTemporaryFile(delete=False` | No matches. |

The source scan found eight actual `mkdtemp` calls and 130 lines using
`TemporaryDirectory`. Cleanup in other fixtures can depend on finalization when setup
fails; browser profile cleanup can also fail while a browser holds files. The guard
cannot detect a second uncleaned call in a file that already mentions cleanup.

The browser driver inherits TEMP and TMP pointing to its test directory. An outside
run found that Edge otherwise leaves a log and an importer directory in the shared
temporary folder. Cleanup can still leave files behind if the browser holds them.

## Tests

Full suite: 1152 tests OK outside the sandbox (main bf4bbc3 had 1151; +1 in `tests/test_temp_cleanup.py`).
With TEMP and TMP pointed at an empty folder, the run left nothing in it (0 files, 0 folders).
In the sandbox the same run passes except `test_brain_panel.InTheShell`, which needs a real browser.
Golden traces unchanged.
