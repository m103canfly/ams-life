# 2026-11-01: unseen image note

When this message or its quote contains a picture but image recognition provides no description,
the turn now asks her to say she could not see it and not guess from a previous picture. This also
applies when image recognition is disabled. QQ stickers do not count as pictures for this note.
The note precedes the choices line when self-decide is enabled and is also present when it is off.

`attention.py` holds the note; `mixin_turn.py` detects pictures and adds it to the turn. Offline
checks in `tests/test_unseen_image.py` cover both event types, quotes, stickers and seen pictures.
No settings or files outside the card are changed. Existing image descriptions and turns without
images are unchanged. AstrBot drops sticker marks from quoted image components, so a quoted
sticker without those marks cannot be distinguished from a picture on that path.

Individual offline tests passed: unseen image (8), prepare turn (5), standalone image context (3),
vision channel (14), golden (2), and basics (11). The full suite was not run as instructed; the
standalone golden test requires aiohttp and is to be run outside the sandbox.
