# 2026-11-01 — move 5e15: stickers in segments

OneBot images lost QQ's sticker markers when converted to neutral segments, and
TurnEvent has no raw message for the sticker lookup. Keep `sub_type` and `summary`
as strings on image segments, including quoted images, and recognize stickers from
the current message's segments when no raw message is available. The raw-message
path remains in use when available. Ordinary images are not stickers; sticker
references still use URLs only. No switch or plugin method was added.

The AstrBot adapter and golden files are unchanged. The OneBot comparison test's
single segment-data assertion ignores the two new fields on images, including in
quoted chains, because AstrBot's neutral segments do not contain them.

Tests run separately in the sandbox: `test_stickers_segments` (4 passed),
`test_adapter_onebot` (35 passed), `test_stickers_wire` (29 passed),
`test_golden` (2 passed), and `test_basics` (11 passed). The full suite was
intentionally not run; `test_golden_standalone` is to be run outside the sandbox
by the owner. No files outside the card's allowed list were intentionally changed.
