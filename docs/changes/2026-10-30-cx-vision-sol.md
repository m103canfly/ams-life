# 2026-10-30 cx-vision-sol: configurable vision channel

## What changed

- Image caption can select `image_api` in the model functions panel. `vision_image_api_model` supplies its model name (empty disables the channel). Each request reads the image API address and key from the plugin's existing API configuration. Other provider choices retain their order.
- `vision_price_per_call` is empty by default, retaining token pricing. Set it to `0` for zero monetary cost. The reply, group-opening and owner-upload paths record picture counts in the same daily spending ledger, shown on the dashboard only after a picture is looked at that day, including when self-decision is off. There is no daily or per-group hourly picture-count limit here. Failed attempts count; cached captions do not. If an older daily counter exists, its count is carried into the ledger on the next request.
- The panel splits vision counts by `reply`, `browse`, and `owner_add`. A queued group sticker looked at when a group is opened is `browse`; a sticker looked at while preparing a reply is `reply`. The group-opening path selects `source="browse"` through `_vision_provider_for`. Older totals without source data are shown as unattributed; they are not guessed. The source ledger contains only counts and the latest time. The existing phone counts remain separate.
- Content fingerprints use image bytes. QQ picture URLs are downloaded only from allowed QQ picture hosts and sent to the provider as data URLs; unavailable or non-image inputs are not sent. Local files are read only after their header identifies a JPEG, PNG, GIF or WebP image. Captions are scoped to place, with senders recorded for deletion, expire after 24 hours, and share the bounded image cache with the existing address entries. Deleting the sender removes their entries. A cached sticker caption does not recreate the original keep decision.
- No selfie, voice, face or sticker logic was changed. Existing address cache entries and normal chat pricing remain in place.

## Files

- `vision.py`, `mixin_llm.py`, `mixin_attention.py`, `mixin_media.py`, `mixin_group_browse.py`, `mixin_stickers.py`, `mixin_discretion.py`, `mixin_pages.py`: adapter, accounting, cache, deletion and panel data.
- `_conf_schema.json`, `pages/dashboard/app.js`: settings, provider selection and daily count display.
- `tests/test_vision_channel.py`, `tests/test_vision_provider.py`, `tests/stickers_cases.py`, `tests/test_stickers_wire.py`: offline coverage and address-cache expectations.

## Validation

Offline tests cover the 31st and 100th picture, source counts and the phone selfie count, the three paths and both provider types, zero price, cache, deletion and legacy count migration. The full suite passes (729 tests on main 85c609b); the zero-price and image-header mutation checks fail as they should. The endpoint and model are checked on the computer at install time.
