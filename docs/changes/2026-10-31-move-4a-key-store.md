# 2026-10-31 move-4a: DPAPI key store

The owner chose an encrypted file for keys (sign-off item 95). `key_store.py` adds a
standalone store using Windows DPAPI with fixed optional entropy and the UI-forbidden flag.
The JSON file holds base64-encoded ciphertext, and writes use `atomic_file.replace`.
The Windows account on this computer can decrypt it; a backup moved to another computer
cannot be expected to decrypt. `status()` exposes only names and booleans for a future
settings page; `get()` is for the program, not the page.

`tests/test_key_store.py` covers validation, corrupt files, status, ciphertext, reopening,
tampering, entropy and safe errors. The module is not connected to the panel or plugin;
existing behavior and golden traces are unchanged. There is no feature switch and no
change outside this card.

Full suite: 1199 tests OK outside the sandbox (main dad87b5 had 1184; +15 in `tests/test_key_store.py`,
two of them skipped on Windows because they cover the non-Windows path). Golden traces unchanged.
In the build sandbox DPAPI cannot encrypt at all (its account has no user keys, even a bare
`CryptProtectData` call fails), so the Windows tests run outside it, under the owner's account.
