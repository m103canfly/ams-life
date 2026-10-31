# Move 5e-10: standalone paths without AstrBot

Standalone reply browsing now uses the DeepSeek stand-in with the `deepseek` key from its key store. A missing or unavailable key leaves the existing unavailable response. The existing browsing checks, quotas and result parsing remain in place. Enable `browse_enabled` to use reply browsing.

Standalone skips AstrBot knowledge-base retrieval and returns an empty knowledge-base list; it has no knowledge base yet. It also goes straight to QQ voice transcription. AstrBot continues to use its existing tool, knowledge-base and speech-provider paths. No switches were changed.

The standalone golden comparison removes the 24 voice warnings and one knowledge-base warning. Its log paths now cover the 24 phone-tool warnings that remain on the AstrBot side. Golden files are unchanged.

Offline validation: `tests.test_standalone_no_astrbot`, `tests.test_browse_wire`, `tests.test_vision_channel`, `tests.test_prepare_turn`, `tests.test_golden`, and `tests.test_basics` passed individually. `tests.test_golden_standalone` requires aiohttp and is reserved for the owner to run outside the sandbox. The full suite was not run as instructed. No files outside the card's scope were intentionally changed.
