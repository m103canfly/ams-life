# 2026-11-01 move 5e-13 web: the LLM block is filled in again on our own panel server

5e-13 lets the new program read its chat model's address and model name from the API tab's
LLM / 对话 block (the Python half is a separate PR). #123 had greyed that block on our own server
and said it was not used. This is the web half: the block can be filled in again there. The key
still comes only from 钥匙 (`deepseek`). Only `pages/dashboard/` is touched; no Python.

## What changed (only with our own server's bridge, `standalone`)

- The LLM block is no longer greyed, and the line "这一块不用" is gone.
- In its place: Key 在“钥匙”里填（聊天模型）；改了要重启新程序才生效。
- The block's 来源 select keeps only 自定义 API (the new program has no AstrBot to follow).
  A saved `source: "astrbot"` is shown and saved as `custom`, so API Base and the model are never
  read-only there.
- The block's head says 新程序 · 自定义 API, and its note says 填 API Base，点“获取模型”选模型。
- API Base, 模型 and 获取模型 work as in the other blocks. The API Key box stays hidden and every
  `api_key` sent is still `""` (#123).
- `index.html`: `app.js?v=20261101-1`, `styles.css?v=20261101-1`.

Inside AstrBot nothing changes.

## Where this differs from the card

- The card did not say what the block's head and note should read. They named AstrBot
  ("未检测到 AstrBot provider…"), which does not fit the new program, so they now say what to do.

## How it was checked

- Our own server: 4c's `PanelServer` on 127.0.0.1 with a `KeyStore` on a made-up test file and
  made-up routes that log only whether each `api_key` is empty. The made-up status had
  `api_config.llm.source = "astrbot"` and a made-up AstrBot provider, the hardest case. In the
  built-in browser:
  - 来源 has only `custom` and shows it; API Base is not read-only; the block is not greyed; the
    key line shows; the API Key box is `display: none`;
  - with a made-up value put into the hidden key box, 获取模型 sent `kind=llm`, `source=custom`, the
    typed base and `api_key: ""`; 保存 API 接入 sent `llm.source=custom`, the base, the chosen
    model, and all five `api_key` as `""`.
- AstrBot side: the scratch AstrBot stand-in in a headless Edge. 来源 still has both options, the
  key line is hidden, the five boxes are there, and 保存 / 获取模型 still send the typed values.
- Tests, one file at a time (the owner's 11-01 rule: the card's own tests plus the goldens):
  `test_look` 15, `test_plugin_pages` 3, `test_panel_server` 11 (1 skipped: this account cannot
  make symlinks), `test_panel_api` 20, `test_memory_list_page` 9, `test_repo_link` 5,
  `test_brain_panel` 20, `test_golden` 2, `test_golden_standalone` 5. All pass.
  `node --check app.js` passes.
