# 2026-10-31 move 4d web: the API tab takes no keys on our own panel server

After the move, her keys live in 4a's encrypted file and the owner fills them in under 设置 → 钥匙
(#121). But the old "API" tab (BioCore's API overrides) still showed five "API Key" boxes
(`llmKey`, `embedKey`, `rerankKey`, `ttsKey`, `imageKey`). A key typed there would be saved in
plain text in `api_config.json`, past the encrypted file. This change closes that on the page.
Only `pages/dashboard/` is touched; no Python.

## What changed

Everything below happens only with our own server's bridge (`ams-bridge.js`, `standalone`), the
same test `keys.js` uses. Inside AstrBot the tab is exactly as before.

- **The five API Key boxes are hidden** (the label gets `hidden`, the box is emptied and
  `disabled`). They are never read: `saveApiConfig` sends `api_key: ""` for every block, and
  `loadModels` (获取模型) sends `api_key: ""`. The back end already takes `""` as "keep what is
  saved". A value put into a hidden box (say, by a browser's autofill) is still not sent.
- **A line at the top of the tab**: 新程序里，聊天模型和看图的 Key 在“钥匙”里填；这里只管地址和模型。
  With a 去钥匙 button that clicks the 钥匙 tab.
- **The LLM / 对话 block** gets the line 新程序的聊天模型用“钥匙”里的聊天模型，这一块不用。 and its
  fields are greyed (opacity). They still work and are still saved; nothing is removed.
- The "no provider found" note under each block no longer says "API Key" there:
  填写 API Base / 模型。 (Inside AstrBot it still says 填写 API Base / API Key / 模型。)
- `index.html`: `app.js?v=20261031-4`, `styles.css?v=20261031-2`.

## Where this differs from the card

- The card did not mention the per-block "no provider found" note. It named the hidden API Key
  box, so on our own server it now leaves that word out.
- The 去钥匙 button does not carry `fb-skip`: it makes no call of its own, so `feedback.js` has
  nothing to show for it.

## Not in this change

- The back end still accepts an `api_key` sent from our own server (Python; with the next 4d card).
- 备份's "含 API KEY" wording.

## How it was checked

- Our own server: 4c's `PanelServer` on 127.0.0.1 with a `KeyStore` on a made-up test file (never
  her real key file) and made-up `page/status`, `page/api_config` and `page/models` routes that log
  only whether each `api_key` is empty. In the built-in browser:
  - the five key boxes are `display: none` and disabled; the top line, the 去钥匙 button and the
    LLM line show; the LLM block is greyed;
  - with a made-up value put into each hidden box, 保存 API 接入 sent all five `api_key` as `""`,
    and 获取模型 (embedding, image, llm) sent `api_key` as `""` each time (seen both in a wrapped
    `fetch` and in the server's log);
  - 去钥匙 switches to the 钥匙 tab.
- AstrBot side: the scratch AstrBot stand-in (`tests/panel_shell` copy) in a headless Edge. The
  five boxes are there and usable; the new lines are hidden; with made-up values, 保存 and 获取模型
  sent each `api_key` with its value, as before.
- Tests (only the page-reading ones, one file at a time, as the owner set on 10-31):
  `test_look` 15, `test_plugin_pages` 3, `test_panel_server` 11 (1 skipped: this account cannot
  make symlinks), `test_panel_api` 20, `test_memory_list_page` 9, `test_repo_link` 5,
  `test_brain_panel` 20. All pass. `node --check app.js` passes.
