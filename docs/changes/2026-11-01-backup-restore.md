# Panel backup and restore

The backup endpoint now uses POST so panel write protection applies. Backups omit
keys, logs, restore backups, likeness data and temporary files; API configuration
has every `api_key` value cleared. The backup notice asks the owner to refill keys.
Plugin source remains included. ZIP paths use forward slashes on every platform.

Restore validates the entire archive, its sizes, compression ratios, entry types
and resolved data paths before extracting into a temporary sibling directory.
Keys, logs and the forget registry are not restored. Files are staged before
replacement, with rollback on replacement failure. The existing safety backup and
forget-registry replay remain in place. No feature switch was added.

Only the Python half of the card is included; the panel UI needs its separate POST
change. The standalone golden test and full suite are to be run outside the sandbox.
The targeted tests passed; aiohttp and directory symlink checks were skipped in
this environment. The golden traces were unchanged and the existing plugin method
count remains 508, rather than the card's stated 505. No files outside the card
were intentionally changed.
