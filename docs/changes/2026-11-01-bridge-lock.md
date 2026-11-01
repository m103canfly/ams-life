# Shared image bridge lock

Vision and photo requests share a plugin lock so that the image service handles one request at a time. Vision waits up to 150 seconds for the lock and retries a 429 twice, waiting 10 seconds between attempts. Photo requests keep their existing retry and request timeout behavior. A cancelled caller leaves the lock held until its request finishes.

The supplied log finding is that the incident was a 429 rate limit caused by overlapping vision and photo requests. The only recorded 400 was older and its response body was unavailable, so its cause is unknown.

There is no new switch or plugin method. The existing vision gate and golden files are unchanged. Only the new program is in scope; the AstrBot-specific portion was omitted as directed on November 1.

Offline tests: `test_bridge_lock`, `test_vision_channel`, `test_vision_neutral`, `test_selfie`, `test_photo_wait`, `test_sticker_relook`, `test_golden`, and `test_basics` passed. The standalone golden test is run outside the sandbox by the owner. The full suite was not run as directed.
