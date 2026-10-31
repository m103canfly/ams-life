# Vision image preparation

Large images and animated GIFs can be rejected by image providers. The image API now
prepares each image with optional Pillow: it uses the first frame, limits the longest
side to 1280 pixels, and saves transparent images as PNG and other images as JPEG.
It reduces quality or dimensions until the result is at most 1 MiB. The initial
JPEG quality and resize method follow AstrBot 4.29.3; the size limit is conservative.

Without Pillow the original bytes are sent and a warning is logged once. Decoding
errors also return the original bytes and log only the error type. There is no new
switch. Cache digests still use the original bytes; selfie handling is unchanged.
The change is limited to the files named on the card, including the attribution in
NOTICE. The full suite is deferred until the combined acceptance round.

Initial sandbox validation: vision preparation ran 6 tests (5 skipped without Pillow),
vision channel 14 passed, standalone image context 3 passed, golden 2 passed, and
basics 11 passed. After the decoding fallback, vision preparation ran 7 tests
(6 skipped without Pillow) and vision channel passed 14. The Pillow-dependent tests
require validation in an environment with Pillow.
