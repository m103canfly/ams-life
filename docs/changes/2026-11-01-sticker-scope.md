# Sticker sharing scope

Self-kept stickers are offered and sent only in their original place until the owner publishes them. Old and owner-provided stickers default to all places. Missing origins and unknown sources are held back. The owner can publish or restore the original scope through the new POST route; the listing exposes only `all` or `here`.

The look must explicitly say both privacy flags are false. A single fetched picture is used for the look and the saved file, with a digest check before saving. Transient picture bytes are excluded from the image cache. The existing sticker and vision switches remain unchanged.

The plugin has one additional method (508 to 509) and one route (30 to 31). The route uses the existing panel write protection. No pages were changed.

Existing tests were updated for the intentional behavior: `test_sticker_look_v2.py` checks missing flags and supplies old sources in its offer fixture; `test_sticker_send_neutral.py` supplies an old source; `test_stickers_wire.py` expects one fetch. The new `test_sticker_scope.py` covers scope, publication, listing, look flags, and the single fetch.

Both golden JSON files were intentionally regenerated. Each differs from its previous version only by the `/astrbot_plugin_ams_life/page/sticker_scope` route. The first golden run failed on that route; regeneration skipped both cases as expected, and the next run passed.

Validation: sticker scope 5 passed; sticker look 5 passed; neutral send 6 passed; sticker wire 29 passed; panel API 3 passed and 17 skipped (aiohttp unavailable); golden 2 passed; basics 11 passed. The standalone golden test is reserved for the owner outside the sandbox. The full suite was not run as instructed. The skipped panel tests include the live write-authentication checks.
