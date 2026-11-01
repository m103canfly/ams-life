# 2026-11-01 1d web fix: 小黑盒 in a panel opened straight on 设置

Audit v5 found it after #182 (B1). A panel opened with `?view=settings` (the way back from
她的表情包 to 设置) switches to 设置 while the page loads, before `app.js` has its bridge. `heybox.js`
decided its mode on that first visit and kept it, so the real panel kept the invented code
(示例（编造）), sent nothing on a click, and a reload did the same.

## What changed

- `heybox.js`: the mode is worked out again each time 设置 or the 钥匙 tab is opened (`enter()`).
  From the invented code to our own server: the 示例 line and the code are put away and the state is
  asked once. Inside AstrBot: the block is hidden again, and so are the 钥匙 parts it showed for the
  preview.
- `qrcodegen.js`: the header no longer says "copied unchanged" next to "turned into plain JavaScript"
  (audit v5, m2). The code is the same.
- `test_heybox_page`: a new case: no bridge on the first 设置, then the bridge; through another view
  and back, and through the 钥匙 tab: not the invented code, status asked once, 已登录, and 退出登录
  sends `logout`; an AstrBot bridge that comes late hides the block. The Node part now ends itself
  after writing its answer (m1), so a timer left running fails at once instead of after 120 seconds.
- `heybox.js?v=20261101-2`.

## How it was checked

- The new case fails on the code from #182 and passes now.
- A stand-in panel server on a test port with made-up answers, opened at `/?view=settings` in a
  headless Edge: the first 设置 has the invented code (no bridge yet); 钥匙 then shows 没登录 with no
  示例 line, and 登录 → the code → 已登录 → 退出登录 works as in #182, with the code's address
  nowhere on the page or the console.
- Tests, one file at a time: `test_heybox_page` 12, `test_plugin_pages` 3, `test_golden` 2,
  `test_golden_standalone` 6. All pass.
