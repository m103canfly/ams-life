# 2026-10-30 cx-vision-sol: configurable vision channel

Stacked on the reviewed branch that also changes `mixin_llm.py`.

## What changed

- Image caption can select `image_api` in the model functions panel. `vision_image_api_model` supplies its model name (empty disables the channel). Each request reads the image API address and key from the plugin's existing API configuration. Other provider choices retain their order.
- `vision_price_per_call` is empty by default, retaining token pricing. Set it to `0` for zero monetary cost. The reply, passing-sticker and owner-upload paths record picture counts in the same daily spending ledger, shown on the dashboard only after a picture is looked at that day, including when self-decision is off. There is no daily or per-group hourly picture-count limit here. Failed attempts count; cached captions do not. If an older daily counter exists, its count is carried into the ledger on the next request.
- The panel splits vision counts by `reply`, `browse`, and `owner_add`. A sticker looked at in passing is counted as `browse`; a sticker looked at while preparing a reply is `reply`. The future group-reading caller can select `source="browse"` through `_vision_provider_for`. Older totals without source data are shown as unattributed; they are not guessed. The source ledger contains only counts and the latest time. The existing phone counts remain separate.
- Content fingerprints use downloaded image bytes when available, otherwise the address. Captions are scoped to place, with senders recorded for deletion, expire after 24 hours, and share the bounded image cache with the existing address entries. Deleting the sender removes their entries. A cached sticker caption does not recreate the original keep decision.
- No selfie, voice, face or sticker logic was changed. Existing address cache entries and normal chat pricing remain in place.

## Files

- `vision.py`, `mixin_llm.py`, `mixin_attention.py`, `mixin_media.py`, `mixin_stickers.py`, `mixin_discretion.py`, `mixin_pages.py`: adapter, accounting, cache, deletion and panel data.
- `_conf_schema.json`, `pages/dashboard/app.js`: settings, provider selection and daily count display.
- `tests/test_vision_channel.py`, `tests/test_vision_provider.py`, `tests/stickers_cases.py`, `tests/test_stickers_wire.py`: offline coverage and address-cache expectations.

## Validation

Offline tests cover the 31st and 100th picture, source counts and the phone selfie count, the three paths and both provider types, zero price, cache, deletion and legacy count migration. Python tests and the mutation check require an environment able to run Python. The endpoint and model have not been checked here; the owner performs those steps.
