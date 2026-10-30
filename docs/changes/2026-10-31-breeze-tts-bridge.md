# 2026-10-31 - Breeze TTS bridge

The owner requested: “语音改用BreezeTTS2”. The standalone bridge keeps the plugin's
OpenAI speech endpoint and forwards requests to a local Breeze service. It wraps the
returned mono 16-bit PCM as WAV, or uses the configured ffmpeg for other formats.
The plugin and its configuration do not change. Run only one bridge on the shared port.

Place `breeze.json` beside the deployed bridge, outside this repository. Set
`breeze_url`, `ref_audio`, `ref_text`, and optionally `seed`, `cfg_scale`, and
`ffmpeg`. The bridge accepts only HTTP loopback hosts, disables proxy and redirects,
and checks the reference file before sending it, to keep reference data local.
`BREEZE_OPENAI_PORT` changes the listening port. No other files or switches change.

Full suite: 1161 tests OK outside the sandbox (main bf4bbc3 had 1151; +10 in `tests/test_breeze_openai_tts.py`). Golden traces unchanged.
The test double for fastapi.FastAPI was fixed by the dispatcher outside the sandbox (Codex could not write the file there): its route decorators now hand the function back, so the tests can call the routes.
