# 2026-10-30 · stickers-page

"她的表情包", the owner's page of her stickers (step 2, part 丙, the card's 表情包页). Stacked on `stickers-wire`
(PR #38): it reads the same library. A page of its own, `pages/stickers/` (it sorts after `dashboard` and `starmap`,
so the sidebar still opens the panel; the console can open it straight away at
`.../plugin-view/astrbot_plugin_ams_life/stickers`); title "她的表情包" / "Her stickers".

- **The page** (`pages/stickers/index.html`, `stickers.css`, `stickers.js`), in the panel's look (月白 on clear glass,
  no glow around words; opaque without backdrop-filter or with less transparency; still with less motion), for
  computer screens: a top line (how many, how many the owner gave, kept today, going within three days), sort
  (newest kept, last used, most used, going soonest), filters (emotion, occasion, where from), a grid of pictures
  that loads more as it scrolls and fetches each picture only when it comes into view, one opened large with its
  labels, where from, how long kept, last used, how many times, days left.
- **Where from** is "群1" / "私聊1" (numbered by when the first sticker came from there), "旧小爱", "主人给的":
  never a number (`stickers.place_labels`, `source_label`).
- **Delete one**: asked to confirm first ("这张是你加的" for the owner's own gifts); cannot be undone; nothing goes
  into the forget registry.
- **Add some** ("加表情包", several at a time, one request each): pictures only (JPEG, PNG, GIF, WebP) by their
  first bytes, whatever the name or the browser says; at most 5 MB and 4096 a side; kept under a new name (their
  content's hash); marked "主人给的": never swept, not counted in the 300; labelled by the owner's line, else by one
  look when looking at pictures is on (its money in the day's, as "vision"), else "主人给的". The owner's number is
  kept as who sent it (local data only).
- **Routes** (`mixin_stickers.py`, registered in `mixin_pages.py`): `page/stickers` (GET, one page of 40, no
  numbers), `page/stickers/image` (GET, one picture by its id, as a data URL), `page/stickers/delete` (POST),
  `page/stickers/add` (POST). Behaviour seen by the plugin: four new routes; the golden traces were re-recorded for
  those four lines only.
- Opened without AstrBot (a preview), the page shows made-up drawings and says so; no picture is in this repository.
- Not here: a link from the panel to this page (how AstrBot routes between a plugin's pages from inside one is not
  checked yet), and the console's button (the console's card).

## Files

- `pages/stickers/index.html`, `pages/stickers/stickers.css`, `pages/stickers/stickers.js` (new)
- `stickers.py` (`place_labels`, `source_label`, `view`, `listing`, `decode_upload`; `Library.counts_of`)
- `mixin_stickers.py` (the four routes), `mixin_pages.py` (registered)
- `.astrbot-plugin/i18n/zh-CN.json`, `en-US.json` (the page's title), `tests/test_plugin_pages.py` (three pages)
- `tests/stickers_cases.py`, `tests/test_stickers_wire.py`, `tests/test_stickers.py`, `tests/test_basics.py` (+6),
  `tests/golden/basic.json`, `tests/golden/full.json` (the four routes)
