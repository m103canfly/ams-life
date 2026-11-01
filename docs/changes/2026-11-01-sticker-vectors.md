# Sticker vectors

Sticker semantic text now includes meaning, tags, image text, emotion, scene, reply target and caption. Embeddings are stored separately in `vectors.json`, keyed by model and semantic text hash; deletion removes the corresponding vector.

When stickers are enabled, one background worker fills missing vectors and retries embedding failures after five minutes. New stickers are prioritized. Replies compare their existing query vector with saved vectors and fall back to mood for missing vectors. Changing the embedding model or sticker text invalidates the old vector.

The existing sticker and embedding switches apply. No new dependency or plugin method is added. The existing wire test seeds fake vectors and disables the worker in its scripted cases; its assertions are unchanged.

Targeted tests passed: sticker vectors (6), sticker look v2 (5), sticker wire (29), golden (2), and basics (11). The full suite was not run, as requested. The standalone golden test is run outside the sandbox.
