# 2026-10-30 cx-her-phone: her phone

Her reply can use three request-local tools, each off by default: `photo_enabled`,
`screenshot_enabled`, and `say_aloud_enabled`. The existing `allowed_tools` behavior
continues for other tools. Old media keyword and daily-limit settings in the installed
`media_settings.json` are no longer used; installing does not edit that file.

Tools only queue work on the event. The reply must pass the existing last look and not
be silent or stopped; each outgoing description, caption or spoken sentence is checked
again before a service or send. A short delay after the reply hook approximately
preserves text-before-media ordering. With the browser enabled, webpage sharing accepts
only search results and pages successfully read in this reply. It sends the browser's
title, address and caption rather than making a screenshot file. Pages from earlier
turns will be connected when web memory is available.

Photos use the configured image API, `codex-image` and 1080x1440. Selfies use one
local `selfie/refs/` reference (`selfie_reference`, default `her_base.png`); snaps
use the generations endpoint without it. Before either request, the description is
cleaned with the browser's name, alias and number rules; an empty result is discarded.
A known one-character name is also removed from photo descriptions.
A single generation runs at a time, with
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
The review reports 625 passing tests on the original PR head. The
`test_phone_check_blocks_private_photo_voice_and_caption_before_services` and
`test_real_send_check_blocks_private_media_text` tests exercise the check before
service calls; removing that gate would make them fail.

The phone tests reuse the existing harness setup instead of replacing the shared
clock during discovery. Their fake tool modules are installed only for each test
and restored afterward.

Installation: the current approved reference is `her_base_v2.png`. Set
`selfie_reference` to that filename, or place a copy under the default name
`her_base.png` in `selfie/refs/`; the reference is local data, not shipped here.
The phone window does not yet record sent media, and media are not counted in the
group's hourly message total. The delayed send only approximates text-first order.
