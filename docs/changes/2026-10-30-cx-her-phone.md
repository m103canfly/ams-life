# 2026-10-30 cx-her-phone: her phone

Her reply can use three request-local tools, each off by default: `photo_enabled`,
`screenshot_enabled`, and `say_aloud_enabled`. The existing `allowed_tools` behavior
continues for other tools. Old media keyword and daily-limit settings in the installed
`media_settings.json` are no longer used; installing does not edit that file.

Tools only queue work on the event. The reply must pass the existing last look and not
be silent or stopped; each outgoing description, caption or spoken sentence is checked
again before a service or send. A short delay after the reply hook approximately
preserves text-before-media ordering. The webpage sharing tool currently accepts no
pages until the browser supplies the pages she actually saw; it sends title, address
and caption rather than making a screenshot file.

Photos use the configured image API, `codex-image` and 1080x1440. Selfies use one
local `selfie/refs/` reference (`selfie_reference`, default `her_base.png`); snaps
use the generations endpoint without it. A single generation runs at a time, with
three waiting places and up to three attempts on 429. Voice uses the configured TTS
bridge and `tts.speakable`. Generated photo and voice files are retained separately
(`phone_photo_retention` and `phone_voice_retention`, each default 50). Only files
matching the phone's own names are removed.

Counts and configured per-call prices are stored with the existing spend data and
shown on the panel. `phone_photo_price` and `phone_voice_price` default to zero:
set the actual service prices before using a paid service; zero is not evidence that
a remote service is free. Screenshot sharing makes no remote service call here.
No fixed daily media limit is imposed.

The changes are within the card: phone wiring, settings, panel, TTS marker cleanup,
offline tests and this document. No golden files or prohibited modules were changed.
Tests have not been run in this environment. The `test_phone_check_blocks_private_photo_voice_and_caption_before_services`
and `test_real_send_check_blocks_private_media_text` tests exercise the check before
service calls; removing that gate would make them fail.

The phone tests reuse the existing harness setup instead of replacing the shared
clock during discovery. Their fake tool modules are installed only for each test
and restored afterward.
