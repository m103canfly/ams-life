# Wait when the image service is busy

The image service behind api_config's "image" takes one request at a time, and the owner's other programs use it too. On 11-01 she missed three pictures because the service answered 429, and our old retries gave up after about twenty seconds. Now her own requests queue on the shared bridge lock, and a 429 waits longer: 5, 10, 20, 40 and 60 seconds, with the lock released while she waits so her other requests can go first. The whole retry budget is three minutes. Vision and photo generation share the same waits: `vision.BUSY_WAITS`, `vision.BUSY_TOTAL_SECONDS` and `vision.wait_when_busy`.

The log line says the service was busy: `vision service busy (429), retry in Ns` before each rest, and `vision service busy (429), gave up after Ns` when the budget is spent. It names no picture content and no key.

When vision gives up the picture stays unseen, so nothing else changes: no caption is cached, and her material keeps `attention.UNSEEN_IMAGE_NOTE`, so she says she did not see it instead of pretending. A photo that gives up is still not sent, and the words go alone.

The card asked to wait for the vision card (V3) before starting. Its change is already here (the shared bridge lock in `vision.py`), so there was nothing to wait for.

## Requests to this service (card item 1)

- `vision.ImageAPI.text_chat` posts to `<image base_url>/chat/completions`. It takes the plugin's bridge lock before the request and holds it until the request ends. Every vision call comes through it: `_vision_provider_for` (reply, browse, owner_add, screenshot), `mixin_slang`, and the screenshot caption.
- `mixin_selfie._post_selfie` posts to `<image base_url>/images/edits`. Only `_make_photo` calls it, and only after the bridge lock is taken.
- `mixin_selfie._post_json` posts to `<image base_url>/images/generations`, in the same place under the same lock.
- `_post_json` also sends voice to the `tts` base_url (`/audio/speech`). That is a different service, so it takes no bridge lock.
- The panel's model-list fetch (`mixin_pages._fetch_models`, kind "image") sends one GET to `<image base_url>/v1/models` when the owner asks in the panel; it is not a picture request and stays as it is.
- `tools/replay.py` posts to the AstrBot chat provider address, not this image service.

So no request to this service was missing the lock, and nothing had to be added; card item 5 (a test for a site that had none) has no site to cover. In its place, the new test file checks that vision and both photo requests hold the lock while the request is sent.

## Changes

- `vision.py`: added `BUSY_WAITS`, `BUSY_TOTAL_SECONDS` and `wait_when_busy()`. `ImageAPI.text_chat` now retries a 429 with those waits and gives up when the budget is spent, instead of three tries ten seconds apart.
- `vision.py`: the rest inside `wait_when_busy()` goes through a small `_rest(seconds)` helper. It is the one place this card's wait calls `asyncio.sleep`, so tests patch `vision._rest` and never the global `asyncio.sleep`.
- `mixin_selfie.py`: `_make_photo` uses the same waits instead of `2 ** attempt`. The `PHOTO_RETRIES` constant is gone because the wait list now decides how many tries there are.
- `tests/test_busy_service.py`: new offline tests (fake service, fake `vision._rest` waits, no network, no real waiting).

What stays: the shared lock order (a photo is finished before a vision request is sent), the 150 second wait for the lock, both request timeouts, the give-up paths, the `phone photo cancelled: service` line, and the unseen-image note.

What changed: a 429 is now tried up to six times instead of three, with longer rests; a photo may rest 135 seconds in all instead of 3. The outer photo wait (`PHOTO_WAIT_SECONDS`, 150 seconds) still bounds a photo overall, so a slow success can end as "timeout" before the busy budget is spent; that constant is not part of the card and was left alone.

## Tests

- `tests/test_bridge_lock.py`, `test_vision_429_retries_and_releases_lock_during_sleep` asserted the old waits (10 seconds, three tries). Only that assertion changed: it now expects 5, 10, 20, 40, 60 and six tries.
- `tests/test_selfie.py`, `test_429_retries_then_cancels` asserted the old photo retry (three tries, 1 and 2 seconds). Only that assertion changed: it now expects six tries and 5, 10, 20, 40, 60.
- `tests/test_busy_service.py` (new): 429 twice then success for vision (5 and 10 seconds slept, success); always 429 gives up after 135 seconds and her material keeps the unseen-image note; a photo with 429 twice then success is made; vision and both photo requests take the lock before sending.

## Fake waits in tests

The busy waits are faked through `vision._rest`, which `wait_when_busy()` calls: the three vision waits and the photo wait in `tests/test_busy_service.py`, the lock check in `tests/test_bridge_lock.py`, and the two 429 tests in `tests/test_selfie.py` patch `vision._rest`. The tests no longer patch the global `asyncio.sleep`. Patching that replaced the sleep of the whole plugin, so a test that runs real plugin code waited forever on an `await asyncio.sleep(...)` yield that had become an immediate return. The `slept()` helper reads the same delays from the `vision._rest` mock.

## Results in this sandbox

File writes are refused here, so these are the owner's to run outside. `tests.test_busy_service` ran six tests: the three vision tests passed; the unseen-note test stopped on `PermissionError` at `STATE_DIR.mkdir`; the photo lock test stopped at `REF_DIR.mkdir` and the photo waits test could not write its photo (the same `PermissionError` shows as a `None` path). `tests.test_bridge_lock` ran five tests: four bodies passed; the photo test stops on the refused photo write (`assertIsNotNone` sees the same `PermissionError`), and every test also reports an error in `TemporaryDirectory` cleanup (`PermissionError`). `tests.test_selfie` (9 failures, 67 errors) all trace back to the refused file writes, for example the photo path and the temporary directories; the two changed 429 tests pass their bodies and only fail on cleanup. `tests.test_golden` (2 errors), `tests.test_golden_standalone` (4 errors), `tests.test_stickers` (11 errors) and `tests.test_basics` (2 errors) cannot run here: `PermissionError` when creating their temporary `data`, `states`, `src/stickers` and `img` folders. `tests.test_look_knows_who` passed all 11 tests. The full suite was not run.
