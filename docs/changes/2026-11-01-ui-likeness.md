# 2026-11-01 L1/L2 web: 像不像, her week to rate in the panel

L1 keeps 20 of her replies a week for the owner to rate; L2 (Python half #177) adds 2 of her days.
Neither had a page yet, so this is both web halves: a new view 像不像 in the panel. Only
`pages/dashboard/` and a new page test; no Python, no new route.

## What changed

- A view 像不像 in the side list, before 设置 (`index.html`, `likeness.js`, a few `.lk-*` styles).
- At the top: ← 上一周 / the week (`2026-W44（10-26 起）`) / 下一周 → (not past this week), how many
  replies and days, and how many are rated.
- 她的回话: each of the week's replies, with where (群里 / 私聊), when, what was said before it, and
  her reply.
- 她的两天, under the replies: each day, one line per thing she did, by time:
  `几点 做了什么（多久）——她的心里话` (`do` and `detail` joined by "：", the minutes only when
  there are some, the line after —— only when she had one).
- Each reply and each day: 像 / 不像 / 说不准, and 一句为什么 with 存理由. A pick saves at once with
  the line typed so far; 存理由 saves the line with the pick already made (and asks for a pick
  first if there is none). The pick shows in the panel's own primary look.
- Only `page/likeness` (`?week=`; replies in `data`, days in `days`) and `page/likeness/rate`
  (`{week, id, rating, reason}`). The week is worked out in the page the way `likeness.week_of`
  does it (ISO week, local time). Numbers come hidden from the plugin as `[number]`; the page
  shows that as `[号码]`, like the rest of the panel.
- Without a bridge (a static preview) it shows an invented week, saying so, and saves nothing.
- `app.js?v=20261101-3`, `styles.css?v=20261101-2`, `likeness.js?v=20261101-1`.

Before #177 is merged, `page/likeness` has no `days` and the page says 这一周还没有她过日子的记录。

## How it was checked

- Our own server: `app.py` at #177's commit with these page files, on a made-up data folder and a
  test port. 29 made-up replies over two weeks written through `likeness.Store.add`, and three
  made-up days in `her_days/` (one detail with a made-up long number). In a headless Edge:
  - 20 replies and 2 days; the days one line per thing, by time; no long number on the page;
  - 像 with a line on a reply, 不像 then 存理由 on a day: three POSTs with the token, and both
    ratings are in `week-2026-W44.json`; 存理由 with no pick posted nothing;
  - ← 上一周 read 2026-W43 (5 replies, no days), and 下一周 was enabled again.
- AstrBot side: the scratch AstrBot stand-in. The view read `page/likeness?week=…` and 说不准 on
  the day went out as `api:post page/likeness/rate`.
- Tests, one file at a time: the new `test_likeness_page` 8 (the ISO weeks, the answer's shapes
  and an error answer, a day's lines, escaping, rating only through the rate route),
  `test_memory_list_page` 9, `test_look` 15, `test_plugin_pages` 3, `test_panel_api` 20,
  `test_likeness` 14, `test_golden` 2, `test_golden_standalone` 6. All pass.
