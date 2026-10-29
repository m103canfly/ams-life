# 2026-10-30 stickers-link: "她的表情包" from the panel

Stacked on `stickers-page` (her stickers' own page).

## What changed

- The panel's side list has a new item, "她的表情包". It opens her stickers' page inside the panel's own
  frame, with a "← 回到面板" button that brings back the view the owner left, in the theme the page is in.
- Why a copy: AstrBot 4.29.3 shows a plugin page in a frame sandboxed with
  `allow-scripts allow-forms allow-downloads` only (no top navigation, no pop-ups), its page bridge has no
  "go to another page" call, and a page's address carries a token good for that one page only. So the panel
  cannot send AstrBot to `plugin-view/astrbot_plugin_ams_life/stickers`; it can only change what its own frame
  shows, from its own folder. `pages/dashboard/stickers/` is `pages/stickers/` copied byte for byte (a test
  checks), and the panel goes there with `?from=panel&back=<view>&theme=<theme>`.
- The page's own address in AstrBot (`.../plugin-view/astrbot_plugin_ams_life/stickers`, for the console's
  button) stays as it was; opened that way it shows no "回到面板".
- `back` is taken only as a short lower-case word (else `overview`), and the panel switches to `?view=` only
  when that view exists.
- No new route; no change to what the page reads or writes.

## Files

- `pages/stickers/index.html`, `stickers.css`, `stickers.js`: the "回到面板" link, shown only with
  `from=panel`; `[hidden]` always hides.
- `pages/dashboard/stickers/` (new): the same three files.
- `pages/dashboard/index.html`, `app.js`, `styles.css`: the side list item; only items with a view switch
  views; `?view=` only for a view that exists.
- `tests/test_stickers_wire.py`: the copy is the page; the panel's link opens it in the frame; the way back
  only from the panel (run in Node with a stand-in page).
