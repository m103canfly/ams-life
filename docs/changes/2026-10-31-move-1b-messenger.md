# 2026-10-31 move-1b-messenger: what she sends, and the platform actions

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Step 1 is "split the layers, fix the interfaces". Step 1a fixed what one received message looks
like; this piece fixes the other direction: everything she sends, and every NapCat action she asks
for, goes through one `Messenger`. The plugin's four ways of sending today
(`context.send_message`, `event.send`, `event.bot.api.call_action`, `bot.call_action`) become
callers of that one interface in the cards from 1e on.

New files only; no old plugin file is changed, so no behaviour changes and the golden traces stay
the same:

* `messenger.py`: the interface and the rules. `ALLOWED_ACTIONS`, `SEND_TYPES`, `ActionRefused`,
  `Sent`, `Messenger`, `check_segments` and `text_segments`. A message is a tuple of
  `events.Segment`; text, face, image (exactly one of path, base64, url) and record are sendable,
  anything else is a `ValueError`. Imports the standard library, `attention` and `events`, never
  AstrBot.
* `adapter_astrbot_messenger.py`: `AstrBotMessenger(context, umo_of, bot_of)` over AstrBot.
  `send` builds the very components the plugin builds today (`mixin_attention._chain_of`,
  `mixin_selfie`, `mixin_stickers`) and hands the chain to `context.send_message`; an empty umo or
  a refused segment sends nothing. `call` allows only `ALLOWED_ACTIONS`, asks
  `bot.api.call_action` when there is one and `bot.call_action` otherwise.
* `tests/test_messenger.py`: the splits against `attention.pieces`, the segment table, the
  components against the plugin's own chain, the three kinds of message, the answers of
  `context.send_message`, the four actions and the refused ones, and that `messenger.py` never
  mentions AstrBot.
* `tests/test_adapter_astrbot.py`: one test added only. The 1a review found that an image with
  both a url and a file was not covered; the url is the reference, and an event like that is
  checked against the plugin too.

Full suite, run outside dsh's sandbox by the dispatcher (`python -m unittest discover -s tests`):
996 tests, all OK; the golden traces did not change. Spot checks: adding `delete_msg` to
`ALLOWED_ACTIONS` fails item 8, letting `reply` through `check_segments` fails item 2.
inside, dsh ran only the two files this card names. `python -m unittest tests.test_messenger
tests.test_adapter_astrbot` ran 42 tests, all OK.

Written by dsh (DeepSeek Harness, headless, workspace-write, its web tools off), dispatched and
checked by the build window: its tools touched only paths inside the worktree.
