# T2 old tests and fixes

Update old test fixtures for recent images, route registration, vision and sticker sharing. Restore retrying atomic replacements during backup restoration, avoid direct raw event reads in recent image tracking, and keep the autonomy loop running when weather ticks fail. Weather codes 85 and 86 now describe snow showers.

The recent image assertions follow 5e-34: an unnamed sender is shown as someone, images from another sender in the same group are considered, and the two newest images are checked. Images from another group remain isolated. The vision test expects the fetched image data and its fingerprint, as required by the current look behavior. No plugin methods or switches were added. The AstrBot-specific raw event path is omitted as instructed.

The segment reader fixture explicitly sets its neutral model to None for the AstrBot voice comparison, avoiding a synthetic MagicMock attribute. The turn image check also relies on normalized sticker segments instead of AstrBot raw messages. The recent-image sticker test uses a normalized segment to check that stickers are not remembered as pictures.

The unseen-image sticker test also uses a normalized segment and still checks that no unseen-image note is added.

Validation: group browse, her, model ports vision, segment readers, sticker ports, atomic file, event reads, recent images any sender, unseen image, stickers wire, golden, basics, panel backup, weather and autonomy ports passed (panel backup skipped two tests). After the main update, unseen image, recent images any sender, event reads, golden and basics passed again. The full suite was not run; standalone golden is reserved for the owner.
