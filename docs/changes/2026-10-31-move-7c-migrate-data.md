# 2026-10-31 move-7c: copy the data folder and check the copy

`tools/migrate_data.py` copies her whole data folder (`astrbot\data\plugin_data\astrbot_plugin_ams_life\`)
into ams-life's own new data folder, format unchanged, then checks the copy: the same relative
file list, the same size and sha256 for every file, and the same `api_config.json` once every
top-level `api_key` is set to `""`. The keys are not carried over: they are left empty in the
copy and filled again in the panel (the encrypted file of 4a). The original file's format is
kept (`json.dumps(..., ensure_ascii=False, indent=1)`, UTF-8: `mixin_settings.py` line 146).
The tool also searches the copy for the source's non-empty key strings (UTF-8 bytes) and
prints only the relative path of a file that holds one; it never prints a key.

Nothing is copied while AstrBot is still writing (a non-empty `*-wal` file in `--src`) or when
a symbolic link is found; then nothing is made and the exit code is 2. A `--src` whose
`api_config.json` cannot be read as JSON stops the copy the same way, before anything is made:
its keys could not be cleared in the copy, so they would stay in plain text there. The
destination goes through `tools/_guard.output_dir`: new or empty, not in the repository, not in
an AstrBot data folder. The source is only read, byte for byte. `--verify` only reads and writes
nothing; it does not require the destination to be empty, since it runs on the finished copy.
Printed: file count, total bytes, the kinds of key cleared, the files that differ (relative path
and reason: missing, extra, size, hash) and the files that hold a key's plaintext. Exit: 0 all
equal, 1 something differs, 2 not started. No file content is printed.

`tests/test_migrate_data.py` uses only made-up folders inside its own temporary folder. It
covers a source with nested folders, an empty folder, a binary file, two set keys and one
empty (`test_copy_clears_the_keys_and_keeps_everything_else`); the source left unchanged
(`test_the_source_is_not_changed`); `--verify` after the copy, after a one-byte change, after
a deleted file and after an extra file (`test_verify_passes_after_a_copy`,
`test_verify_catches_one_changed_byte`, `test_verify_catches_a_missing_file`,
`test_verify_catches_an_extra_file`); a key left in another file, path printed and key not
(`test_a_key_in_another_file_is_found_and_only_its_path_is_printed`); a live WAL stopping the
copy and an empty one not (`test_a_wal_still_being_written_stops_everything`); the guard
refusing a full folder and an `astrbot\data` path
(`test_the_guard_refuses_a_full_folder_and_a_live_data_folder`); a source with no
`api_config.json` (`test_no_api_config_still_copies`); and a source-level check that the tool
imports no AstrBot or logging and prints no read content
(`test_no_astrbot_or_logging_and_no_read_content_is_printed`). Symbolic links are not tested:
making one needs a permission on Windows.

Nothing existing changed; the tool is not imported by the plugin, so behavior and golden
traces are unchanged. The real copy is run by the dispatcher on the switch day, with AstrBot
stopped; this change and its tests only use made-up folders.

Files: `tools/migrate_data.py`, `tests/test_migrate_data.py`, this note. No other file changed.

Tests: `tests.test_migrate_data` passes outside the sandbox with `venv-ams-life` (12 tests). The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
