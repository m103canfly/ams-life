# Sticker scope for group saves

The owner's principle is to protect other people's private matters and the system
itself, not to restrict her own use. Stickers she likes belong to her; images
posted publicly in groups are public.

| Source | Default sharing scope |
| --- | --- |
| Old Xiaoai's stickers and owner additions | Everywhere |
| Stickers she saved in a group | Everywhere |
| Stickers she saved in a private chat | That private chat until the owner publishes them everywhere |

New group saves and legacy rows without a saved scope now default to everywhere.
Existing saved scopes remain authoritative, including group stickers the owner
restricted to their origin. The owner can still restrict or publish a sticker
through the existing scope control. Rows without an origin remain unavailable
unless their source or an explicit scope permits sharing. No migration or new
plugin method is needed; there is no new switch.

Offline checks: `tests.test_sticker_scope`, `tests.test_golden`, and
`tests.test_basics` passed individually. The full suite was not run as instructed;
`tests.test_golden_standalone` is run outside the sandbox by the owner. Golden
fixtures were not changed. Per the owner's November 1 instruction, AstrBot
coverage for this change was not added. No files outside the Python half of the
card and this change note were intentionally modified.
