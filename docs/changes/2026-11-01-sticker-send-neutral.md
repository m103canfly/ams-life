# Neutral sticker sending

The new program's events have no bot, so stickers were sent as ordinary images.
The neutral messenger now uses the existing sticker action and checks, with the
same single image fallback on failure. AstrBot behavior is unchanged. There is no
new switch or plugin method. Changes are limited to the files on the card.

Sandbox validation passed: sticker send neutral 6 tests, stickers wire 29,
stickers segments 4, send neutral 6, golden 2, and basics 11. The full suite is
deferred. The standalone golden test runs outside the sandbox.
