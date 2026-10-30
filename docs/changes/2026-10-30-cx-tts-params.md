# 2026-10-30 cx-tts-params: sampling parameters for the voice bridge

The OpenAI-compatible TTS bridge forwards optional `temperature` and `top_k` settings
to GPT-SoVITS. Each request can override the setting in `voices.json`; values are converted
to float and int respectively. Missing or invalid values are omitted, so api_v2 keeps its
defaults. An invalid request override is omitted rather than falling back to the setting.

Files: `tools/gsv_openai_tts.py`, `tests/test_gsv_openai_tts.py`.
