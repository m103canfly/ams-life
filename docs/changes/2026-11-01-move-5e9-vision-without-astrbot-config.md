# 2026-11-01 - move 5e9: vision without AstrBot config

The standalone context does not provide AstrBot's `get_config`, so reading the
caption prompt stopped image recognition before the vision provider was called.
If the prompt cannot be read, use the default prompt and continue. AstrBot's
configured prompt still takes precedence when available. No switches changed.

Added offline tests for standalone captioning and caching, the AstrBot prompt,
and a failing config lookup. No files outside the card were changed.

Tests, one file at a time: `test_image_context_standalone` (3),
`test_vision_channel` (14), `test_event_reads` (5), `test_group_browse` (43),
`test_model_ports_vision` (4), `test_stickers_wire` (29; exercises
`stickers_cases`), `test_golden` (2), and `test_basics` (11) passed.
The full suite was not run as instructed. `test_golden_standalone` is reserved
for the external run.
