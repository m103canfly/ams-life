# 2026-10-31 move 5e-6 web: the owner fills in her keys in the panel

After the move, her keys are no longer filled in AstrBot's back end. They are kept in 4a's
encrypted file (`key_store.py`: on Windows, encrypted with this computer's account), and 7c clears
the old config's keys when it moves the data. So the owner fills them in again, in person and
not through Claude:
- `deepseek`, the chat model;
- `vision`, the small channel for pictures;
- `napcat`, the token NapCat connects with.

4b's panel server already has `GET /api/keys` (whether each key is there, never the key, plus
`"damaged": true` when the file cannot be read), `POST /api/keys` and `DELETE /api/keys/{name}`.
Both writes need `X-AMS-Token`. This change adds the page for them. Only `pages/dashboard/` is
touched; no Python.

## What changed

- **New `pages/dashboard/keys.js`** (`window.BioKeys`, also loadable by node's `require()`):
  - It does something only when the page has our own server's bridge (`ams-bridge.js`,
    `standalone`). Inside AstrBot it returns at once: the keys are still filled in AstrBot's back
    end there.
  - One row each for `deepseek` 聊天模型, `vision` 看图 and `napcat` NapCat 口令. Each row has:
    - its state, 已填 or 没填, from `GET /api/keys`;
    - a password box (`type="password"`, `autocomplete="off"`, `spellcheck="false"`);
    - 保存 (also Enter in the box) and 清掉.
  - **保存** sends `POST /api/keys` with `{name, value}` through the bridge's `apiPost`, which
    adds the page's token. The value is trimmed at both ends first, and an empty box is not sent.
    After a success the box is emptied at once and the states are read again. After a failure the
    typed value stays in the box, so the owner can correct it.
  - **清掉** asks first (`window.confirm`, as the memory list's delete does). Then the page sends
    `DELETE /api/keys/<name>` with `fetch`, reading the token from the page's
    `meta[name="ams-token"]` for that one request only.
  - When the answer says `damaged`, a red line above the rows reads “钥匙文件读不了，请重新填”.
    Saving a key writes a fresh file, and the line goes away.
  - An error says only “没存上（HTTP 400）” / “没清掉（HTTP 403）”, or “（连不上）” when no
    answer came. No other part of an error is shown.
  - A key is never kept anywhere else: not in localStorage, not on the console, not in an
    address, not in any other request.
  - The boxes stay in the page and are never re-drawn. A browser can take a password box that
    disappears after a request as a sign-in and offer to keep the "password".
  - A name the server does not take (absent from `GET /api/keys`) reads “这边还不能填”, and its
    row is disabled.
- **`pages/dashboard/index.html`:**
  - a 钥匙 tab after API in 设置, with its title and panel, all `hidden` until `keys.js` shows
    them;
  - `keys.js` is loaded after `memories.js`;
  - `app.js?v=20261031-3` and `styles.css?v=20261031-1`.
- **`pages/dashboard/app.js`:** one line attaches `BioKeys`, next to the memory list.
- **`pages/dashboard/styles.css`:** a few rules for the rows and the red line, on the panel's own
  colour variables. They also keep a `hidden` settings tab and its title hidden. At phone width the
  row stacks.

## Choices worth knowing

- **It is a tab in 设置, not a page of its own.** A new folder under `pages/` would become another
  AstrBot plugin page, and `tests/test_plugin_pages.py` fixes the page list.
- **`keys.js` calls our own bridge directly**, not the copy `feedback.js` wraps. Its rows say
  “正在存…/存上了/没存上（HTTP …）” themselves, and the buttons carry `fb-skip`.
- **The napcat row needs the server to take it.** `PanelServer`'s default `key_names` is only
  `('deepseek', 'vision')`. For the third row to work, whatever starts the server (5e-5b's
  `app.py`) has to pass `key_names=('deepseek', 'vision', 'napcat')`. Until then that row reads
  “这边还不能填”.

## Checked

- **On our own server.**
  - Setup:
    - 4c's `PanelServer` on 127.0.0.1;
    - `key_names` set to the three of the card;
    - `keys` set to a `KeyStore` on a made-up test file in a scratch folder outside the
      repository, as `tests/test_panel_server.py` does. Her real key file was not touched.
    - A small subclass logged each `set` with the name and the value's length only.
    - `page/status` answered made-up data.
  - In the built-in browser:
    - all three rows read 没填;
    - typing a made-up value shows only dots;
    - 保存 turned the row to 已填, emptied the box and showed 存上了 (Enter does the same);
    - 清掉 sent nothing when cancelled; when confirmed, it sent the DELETE and the row went back
      to 没填;
    - with the test file overwritten by `broken`, the red line showed, and saving a key cleared
      it.
  - Errors:
    - a 5000-character made-up value got “没存上（HTTP 400）”, and the value stayed in the box;
    - a DELETE with the page's token changed on purpose (test only) got “没清掉（HTTP 403）”.
  - The phone width (375 px) stacks the rows, with no sideways scroll.
- **Where the value goes.**
  - Over this test, `fetch` was wrapped in the page to record, for each request, its address and
    method, and whether the value was in the address, the headers or the body.
  - The value was only in the body of the one `POST /api/keys`, which carried the token. Every
    `GET /api/keys` answer held only true/false.
  - The value was not in localStorage, sessionStorage, the address, the page's HTML or the
    resource list.
  - The console had only the test server's 404 for `page/look`.
  - The server log has names and lengths only.
- **In AstrBot's place.** The scratch copy of `tests/panel_shell` served this branch, driven by
  headless Edge over 127.0.0.1:
  - the page has no token meta, and the bridge is AstrBot's stand-in;
  - 设置 shows API, 记忆, 球体, 版本 and 备份, with no 钥匙;
  - the tab, title and panel stay hidden, no row is drawn, and no `/api/keys` request was made.
- **The real AstrBot was not started.**
- **Tests:** `test_look`, `test_plugin_pages`, `test_panel_server`, `test_brain_panel`,
  `test_memory_list_page` and `test_repo_link` all passed. `test_panel_server` skipped its
  symlink test, because this account cannot make symlinks. By the owner's rule of 10-31, the full
  suite runs once everything is written.
- `node --check` passes on `app.js` and `keys.js`.
