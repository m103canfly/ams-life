# 2026-10-30 media-asis: her camera and her voice, as the owner wired them in

The night of 10-30 the owner wired a photo of herself and a voice note into the installed plugin
by hand. This brings exactly that into the repository, so installing a newer version no longer
wipes it out. The way it works is kept as it was (keywords in the message, a daily cap); the next
change turns both into tools she decides to use herself.

What it does:

- After she answers (end of `on_llm_response`, after the last look and her 【不说】, so a reply
  held back or not said is never said aloud or pictured), `_media_after_reply` looks at the
  message for the keywords in `<data>/media_settings.json` (or the defaults) and, when one is
  there, sends a voice note of her reply and/or a photo of her doing what she said.
- The photo: the image API of the panel's API settings (`api_config["image"]`, `/images/edits`),
  with two reference pictures in `<data>/selfie/refs/` (`face.png`, `ornament.png`). The pictures
  are the owner's and stay on his machine; they are not in this repository.
- The voice: the TTS API of the panel's API settings (`api_config["tts"]`, an OpenAI-compatible
  `/audio/speech`). `tools/gsv_openai_tts.py` is that API in front of a local GPT-SoVITS
  (`api_v2.py` on 127.0.0.1:9880; the bridge listens on 127.0.0.1:9881). It is copied into the
  GPT-SoVITS folder and run there; it is not imported by the plugin.
  Its reference clip and the clip's words are read from `voices.json` next to it (the owner's,
  not in this repository); the copy running on the owner's machine still has them written in.
- Off by default here (`selfie_enabled`, `voice_enabled` false). The owner's
  `<data>/media_settings.json` turns them on on his machine; installing does not touch it.
- A cap per day (`*_daily_limit`, 0 = none, the owner's choice of 10-30), counted in
  `<data>/selfie/counters.json`. The files sent stay in `<data>/selfie/`.
- Anything that fails sends nothing and leaves one line in the log. The log has no chat words.
- Where the services are and their keys are only in the panel's API settings, never in code.

Also from that night:

- `_fetch_models` (the panel's "读取模型") asks through the Windows system proxy: AstrBot sets
  `no_proxy` on start, and with it Python's `getproxies()` reports no proxy at all, so outside
  model lists timed out. Local addresses never go through a proxy.
- The panel says what reading the models is doing next to the block that asked, and gives up
  after 25 seconds instead of waiting for ever.

`tts.py` (what of a reply is said out loud) comes along from the voice work of that night; it is
not used yet. The next change (her two tools) speaks through it.

Files: `mixin_selfie.py` (new), `main.py`, `mixin_pages.py`, `pages/dashboard/app.js`, `tts.py`
(new), `tools/gsv_openai_tts.py` (new), `tests/test_selfie.py`, `tests/media_cases.py`,
`tests/test_tts.py`, `tests/test_basics.py` (+9 methods), `tests/stubs` (`Record.fromFileSystem`).

README's table of modules would get:

| `mixin_selfie.py` | her camera and her voice after a reply (keywords, a daily cap; off by default) |
| `tts.py` | what of a reply is said out loud, and the body asked of GPT-SoVITS |
