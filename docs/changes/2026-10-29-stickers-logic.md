# 2026-10-29 · stickers-logic

`stickers.py`, her stickers' own logic (step 2, part 丙; not wired into the plugin yet), and `tools/import_stickers.py`, which stages the old companion's 118 stickers into a new folder (read only from the unpacked archive; sha256 and picture format checked; the old chats' numbers in 出现于 not taken). Pictures known by their first bytes, at most 5 MB and 4096 a side, fetched only from QQ's picture servers; QQ's sticker mark read from the message as NapCat sent it; one look at a picture answers what she keeps (only known fields, cut short; the program decides); the library (30 days unused, at most 300; what the owner gave neither expires nor counts; deleting a person takes what he sent); a few offered in a reply; sending one as a QQ sticker only to the chat of the message, only image, text and face; what a look leaves in the picture cache says who sent it.

## Files

- `stickers.py` (new)
- `tools/import_stickers.py` (new)
- `tests/test_stickers.py` (new)

## README's table of modules

| `stickers.py` `tools/import_stickers.py` | 她的表情包（第 2 步丙块）的纯逻辑：认图片格式和大小、只从 QQ 图片服务器取、认出 QQ 标成“表情”的图、看一眼图要回的那几样和存不存、她的表情包库（30 天不用就删、最多 300 张，主人给的不删不占数、删人连他发的图一起删）、回话时挑几张候选、发成 QQ 表情时只许发到这条消息的会话、看过的图的描述记上是谁发的；导入旧小爱 118 张的工具（写进暂存文件夹）；还没接进插件 |
