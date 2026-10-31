# 2026-10-31 move-4c web: the panel pages call our own server when there is no AstrBot

The panel pages reached the plugin only through the bridge AstrBot injects
(`window.AstrBotPluginView` / `AstrBotPluginPage`, `ready()`, `apiGet()`, `apiPost()`), and
`app.js` threw `"direct-open"` when a bridge was there but the page was not framed. Card 4c
serves the same routes from our own panel server (`/api/page/...`) and puts
`<meta name="ams-token">` into every `.html` it serves; writes need that token in
`X-AMS-Token`. This change only swaps how the pages talk to the back end. Nothing looks
different, and inside AstrBot nothing changes.

## What changed

- New `ams-bridge.js`, the same file in `pages/dashboard/`, `pages/stickers/` and
  `pages/dashboard/stickers/`. AstrBot serves a page only from its own folder, so the file is
  copied instead of shared under `pages/`. It does something only when the page has the
  `ams-token` meta line and there is no AstrBot bridge (the three names, on `window` and on
  `window.parent`). Then it defines `window.AstrBotPluginPage` with:
  - `standalone: true` and `ready()` (resolves at once);
  - `apiGet(path, params)` → `fetch('/api/' + path + query)`, where values that are
    `undefined` or `null` are left out;
  - `apiPost(path, body)` → POST JSON with `X-AMS-Token`;
  - a non-2xx answer throws `HTTP <status>` and nothing else; otherwise the answer is the
    handler's own dict, as AstrBot's bridge gives it.
  
  The token is never stored and never printed. Inside AstrBot no page has the meta line, so
  the script returns at once. AstrBot adds its own bridge script at the end of `<body>`,
  after this one, which is why the meta line is what decides.
- `pages/dashboard/index.html`, `pages/stickers/index.html` and
  `pages/dashboard/stickers/index.html` load `./ams-bridge.js` before their own scripts.
  `app.js?v=` is bumped so a cached copy is not used.
- `app.js`:
  - A bridge with `standalone` is used even when the page is not framed. All other cases are
    as before, including `"direct-open"` for AstrBot's bridge outside a frame.
  - The tombstone click handler, which called `page/memory/restore/...`, is removed. Step 1-3
    removed that route, and no tombstone row has drawn the restore button since.
  - `runMemOp` now calls only `page/memory/delete/...`. Any other `op` says “已经没有这个功能”.
    The rollback route is gone; the row draws only the delete button.
- `stickers.js` (both copies) and the stickers `index.html` comments now mention the new path.
  This is comments only.

## Not as the card said, and why

- **The panel's sticker copy loads `./ams-bridge.js`, not `../ams-bridge.js`.** `pages/dashboard/stickers/` has its own copy.
  `tests/test_stickers_wire.py` (`test_the_panels_copy_is_the_page`) requires the two sticker
  folders to hold the same files, byte for byte. Changing that test would have meant changing
  Python, which this card does not touch.
- **`page/memory/<op>/...` (old line 1048) is not removed outright.** The only `op` the list draws is `delete`, and
  `mixin_pages.py` still registers `page/memory/delete/<path:session>/<entry_id>` (the owner's
  delete, step 1-3). Removing the call would break a working button, so only the delete path is
  kept.
- **`pages/starmap` is not changed.**
  - Its `index.html` and `brain.bundle.js` are generated from `tools/brain/src/` by
    `tools/brain/build.mjs`, and `tests/test_brain_page.py` checks that.
  - The bundle uses a bridge only when it is framed.
  - On our own server, `/static/starmap/` opened by itself still shows the made-up sample. The
    panel's “她的脑子” view does work: it is a srcdoc frame that asks the panel, and the panel
    asks through this bridge.
  - Opening the single page by itself would need `tools/brain/src/brain.js` changed and the map
    rebuilt. That is left for a card that may touch `tools/`.

## Checked

- **Without AstrBot:** 4c's `PanelServer` (root `pages/`, `start_page='dashboard/'`) on
  127.0.0.1. A local script outside the repository gave it made-up handlers for `page/status`,
  `page/owner_rules`, `page/memories`, `page/stickers` and `page/stickers/image`. In the
  built-in browser:
  - `/` redirects to the panel, which shows 已连接 and the status;
  - “她记住了什么” lists the made-up rows;
  - “她的表情包” (the panel's copy) and `/static/stickers/` show the made-up pictures, with no
    sample badge, and “回到面板” goes back;
  - “保存规矩” sends a POST. The handler saw the token header, and it matched; the log records
    only that it matched, never the token. The Origin was `http://127.0.0.1:<port>`.
- **In AstrBot's place:** a scratch copy of `tests/panel_shell` stood in for AstrBot. It serves
  this branch's `pages/dashboard/`, adds a stand-in bridge script, and answers the same routes
  with made-up data. The copy also maps a page folder to its `index.html`; the shell in the
  repository does not, so the sticker link 404s there. Headless Edge was driven over 127.0.0.1
  the way `drive.mjs` does it:
  - the page has no token meta, `ams-bridge.js` defined nothing, and the panel ran on the
    stand-in bridge;
  - the status, the memory list, the owner-rules write and the sticker page (with its own
    stand-in bridge) all worked;
  - the host's log shows every call going through the stand-in.
- **The real AstrBot was not started**, by the rule that only the owner starts it. The
  installed plugin is also not this branch.
- **Tests:** only `tests.test_stickers_wire.FromThePanel`, the copy check on the files changed
  here. It ran with `venv-ams-life`: 3 tests, OK. By the owner's rule of 10-31, the full suite
  runs once everything is written.
- `node --check` passes on `app.js` and `ams-bridge.js`.
