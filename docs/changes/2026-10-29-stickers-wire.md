# 2026-10-29 · stickers-wire

Her stickers wired into the plugin (step 2, part 丙; the logic is `stickers.py`, PR #32). Off unless
`stickers_enabled` is on, and looking at pictures (`image_caption`) has to be on too; off, nothing changes
(the golden traces are the same).

- One look at a picture (`stickers.LOOK_PROMPT`, the vision provider, deepseek-flash) answers what it shows and
  whether she keeps it; the program decides (`stickers.should_keep`). At reply time it is the look
  `_image_context` already made (no second call), and the QQ stickers of the message are looked at wherever it
  was sent. A QQ sticker in a chat she was not called in gets a look of its own, a task started from
  `on_message` after the message is kept; not for anyone the forget registry rules out. At most three pictures
  a message, each looked at once (image_cache.json); the money goes into the day's as "vision", once.
- Every look is kept in image_cache.json with who sent it and where (`stickers.cache_entry`).
- What she keeps is fetched from QQ's picture servers only (`stickers.fetch_picture`: a redirect elsewhere is
  not followed, at most 5 MB), checked by its first bytes, and added to one library (`<data dir>/stickers/`),
  one add at a time; the library is swept (30 days unused, at most 300) after each add.
- A reply's prompt offers up to five (`stickers.pick_candidates`: the talk by local vectors, her mood; none sent
  in the last 30 minutes). She names one as `[表情包:n]`. Not `[表情:n]`: `[表情:名字]` is 甲's QQ face and stays
  one. Only an offered number counts; the mark never reaches QQ.
- The one she named is checked like her words (the send check, when global_memory is on), then sent after her
  words (甲's queue: after her last message, a short pause) as a QQ sticker through the adapter's own client,
  `event.bot.call_action`: only `send_group_msg` / `send_private_msg`, only to this message's chat, only an image
  with sub_type 1 (`stickers.send_params` / `allowed`). If NapCat says no, or there is no client, once as a
  plain picture through AstrBot; else not sent, and a line in the log. A sticker alone (no words): AstrBot sends
  nothing, the plugin sends the sticker.
- What she sent is kept as `[表情包：标签]` in her phone and in AstrBot's history (on_agent_done settles it), and
  counts in the group's hour (`_note_sent`).
- Deleting a person deletes the looks at the pictures he sent and the stickers he sent (never what the owner
  gave); old cache entries that do not say who sent them go after 30 days on the next deletion.
- Not here yet: the stickers page (`pages/stickers/`) with the owner's delete and add, a PR of its own on the
  new look (#37).

## Files

- `mixin_stickers.py`, `tests/stickers_cases.py`, `tests/test_stickers_wire.py` (new)
- `main.py` (the mixin, `stickers_enabled`, on_message, on_llm_request, on_llm_response, on_agent_done)
- `mixin_media.py` (`_image_context`: the sticker look in the same call), `mixin_attention.py` (`_send_rest`
  takes something to send after the words; `_after_words`), `mixin_discretion.py` (deleting a person)
- `stickers.py` (`fetch_picture`, `QQOnlyRedirect`; the mark is `[表情包:n]`, kept as `[表情包：标签]`)
- `_conf_schema.json` (`stickers_enabled`, off), `tests/test_basics.py` (+15 methods), `tests/test_stickers.py`,
  `tests/stubs/astrbot/api/message_components.py` (`Image.fromBase64`)

## README's table of modules

| `mixin_stickers.py` | 她的表情包接进插件（第 2 步丙块）：看一眼图顺带判断存不存（回话时那一次，没叫她时 QQ 表情另看一次）、从 QQ 图片服务器取图存进库、回话时给几张候选、她写 `[表情包:n]` 就在话后面发成 QQ 表情（只发到这条消息的会话，不行就发普通图片）、手机和历史记成 `[表情包：标签]`、删人连他发的图一起删；开关 `stickers_enabled` 默认关 |
