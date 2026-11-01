# 2026-11-01 move 5e-28 web: 下载备份 is a POST, and the panel says the keys are not in it

5e-28 makes `page/backup` a POST (so it goes through the panel's write token and Origin check like
the other writes) and leaves the keys out of the backup. The Python half is #148. This is the web
half; it has to land together with #148, or 下载备份 breaks (a GET to a POST-only route). Only
`pages/dashboard/` is touched; no Python.

## What changed

- 下载备份 calls `bridge.apiPost("page/backup", {})` instead of `apiGet`. On our own server the
  bridge adds `X-AMS-Token`; inside AstrBot it goes out as the bridge's `api:post`.
- Under the button a new line, `#backupKeysNote`: 备份里不含钥匙，恢复后要在“钥匙”里重填。
  Inside AstrBot (no 钥匙 tab there; the keys live in the API tab) it reads
  备份里不含 API Key，恢复后要在“API”里重填。
- The section's hint was 含记忆/人设/API KEY; it is now 含记忆/人设，不含钥匙. The line under it was
  备份包含 API Key…不要外发; it is now 备份里有记忆、人设和聊天记录，不要外发。 (the backup still holds
  her memories and chats, so it is still not for sharing).
- `index.html`: `app.js?v=20261101-2`.

## Where this differs from the card

- The card asked for the same note inside AstrBot. There it would point to a 钥匙 tab that does not
  exist, so inside AstrBot the note names the API tab instead.

## How it was checked

- Our own server: `app.py` from #148's commit with these two page files, on a made-up data folder
  and a test port (no keys, so only the panel runs). `GET /api/page/backup` → 404, a POST without
  the token → 403. In a headless Edge, 下载备份 sent one POST with `X-AMS-Token`, the zip landed,
  and the status line said 下载已开始. In the zip: no `keys.dat`, no `logs/`, every `api_key` in
  `api_config.json` empty, the made-up key values nowhere in it.
- AstrBot side: the scratch AstrBot stand-in in a headless Edge. 下载备份 sent one `api:post
  page/backup` and no `api:get`; the note names the API tab.
- Tests, one file at a time (the card's own plus the goldens): `test_panel_api` 20,
  `test_golden` 2, `test_golden_standalone` 6. All pass.
