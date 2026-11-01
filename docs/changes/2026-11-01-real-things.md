# Every thing on the menu makes something real

Her owner's words: "做的每件事都是真正的事"; "我希望小爱诚实，尊重事实，不去编造事实".
A choice that needs a model must leave something she can show, or the day must
say it was not done. This card (1c-6a) adds her works (a song, a reading note),
renames dazing, gives the notebook its own menu entry, and adds her wish list
to the notebook she already keeps.

## Her works (`works.py`, `DATA_DIR/works.jsonl`)

One work per line:

```
{"id", "ts", "kind": "song" | "review", "title", "text", "url", "origin"}
```

`url` is set for a reading note (the page she read) and empty for a song; the
origin is her own (`self`). A work is only written after the call came back and
its words passed the hard red lines (`redline.hit`) and the red-line switch, and
after every name she knows was taken out, his too (`life_loop.without_names`).
A title is 80 characters, the text 1000: only a guard against a model running
away, not a limit on how long she writes.

Her works hold no one else's name by construction, so forgetting someone has
nothing to do here: there is no `forget` wiring in `works.py`, and the work's
origin is `self`.

Each made work also adds one memory of her own to the library
(`memory_source: "self"`, origin `self`): "我写了首歌《…》：头两句…" or
"我读了《…》，觉得…". A missed attempt adds no memory.

## The menu (`life_loop.menu`, `life_loop.apply_choice`)

| Choice | What it does | What is left |
| --- | --- | --- |
| 写歌 (new) | one call of its own: her day, the weather, her body; never the chat; `{"title","lyrics"}` | one work and one memory |
| 读篇文章写读后感 (new, browser on) | the pages she read that may be said anywhere (no `shared_in`), newest first; she picks one (a call), then writes the note (another call) | one work with its `url` and one memory |
| 发呆 (was 什么都不干) | no call; no detail; "此刻" is 发呆 | nothing |
| 回看聊天、整理本子 | the existing notebook writing, once | the notebook |
| the rest | as before | as before |

Both writing calls keep the chat out: they are given `own_lines`, which is the
time, the weather, her body and today's activities. The reading note's page list
is filtered with `discretion.origin_of(entry).get("shared_in")`, so a page she
only saw because someone gave it to her in a private chat is never offered.

When it did not work out (no model answer, a red line, no page to read) nothing
is kept, the day's row says what she tried ("想写歌，没写出来" / "想写读后感，
没有能读的文章"), and "此刻" says the same. Her own `detail` is used only when
the work was really made. With no page to read, she asks for the same trip
"刷手机" asks for (`pending.go_browse`).

The old name is still understood: `parse` reads `什么都不干` as 发呆, and `tick`
treats either name as dazing in old data (`DAZE_TOO`).

## Dazing

`detail` is not written for 发呆 and `doing` is 发呆, so "此刻：在家里，正在发呆".
`BASE_MENU` is `('吃饭', '睡觉', '休息', '发呆', '写歌')`.

## The notebook entry in the menu

"回看聊天、整理本子" is offered while the existing notebook machinery would
really write (`notebook_due`: not written for today, the model switch on, the
budget fine). It is therefore absent once today's notebook is written, and also
absent outside the notebook's own window (03:00-18:00, or after a chosen sleep)
where `_maybe_write_notebook` would do nothing. Gating it on `notebook_due`
keeps the card's rule "当天写过本子就不出现" and its headline rule that every
menu entry really does something.

## Her wish list (the notebook's "想做的")

The life loop's JSON answer has one more nullable field, `wish` (at most 100
characters), and the prompt has one neutral line about it ("有想做但现在做不了
的事，可以写在 wish（最多100字）。"), no nudge. `life_loop.keep_wish` takes the
names out, refuses a red line, and appends it to `self_model["notebook"]` with
`section: "想做的"` and origin `self`; the same line twice is not kept again.
The menu never offers what she cannot do, and this list is not a menu.

## The public line

`life_loop.post_materials` shows the last three works (title and the first two
lines) before the model writes the public sentence: she may write about them or
not.

## The day's row

`her_days.Store.add` keeps one more field, `work` (the made work's id, empty
when nothing was made), so the day and the work stay tied together. The card
names this ("her_days 那一行带上作品的 id"), so `her_days.py` changes by that
one field.

## Old tests changed

`tests/test_life_loop.py`, one test only:
`test_detail_forty_characters_cleaning_and_now_line` used the old dazing answer
and checked that a long detail is cut to 40 characters. Dazing writes no detail
any more (this card), so the test now chooses 休息 for the same check. No other
assertion was touched; the old dazing answer still parses as 发呆, so the other
tests of that file keep their expectations.

## Golden traces

Not re-recorded: `tests/scenario.py` and `tests/scenario_standalone.py` do not
run the life loop, so no trace includes the menu, the wish or a work.

## Files

- `works.py` (new): the work store and the one-line memory of a work.
- `life_loop.py`: the menu, `parse`, `apply_choice`, the dazing name,
  `own_lines`, `song_materials`, `write_song`, `readable_pages`,
  `pick_materials`, `write_review`, `remember_work`, `keep_wish`, the `wish`
  line in `materials`, the recent works in `post_materials`, `dazing` in `tick`.
- `her_days.py`: the `work` field of a day's row.
- `tests/test_real_things.py` (new): the card's tests 1-7, plus the words
  (`WorkWords`) and the work store (`WorkStore`).
- `tests/test_life_loop.py`: the one dazing test described above.

## Validation

In the sandbox only tests that write no files can run: the new
`WorkWords` (7 tests) passes, `tests.test_life_loop.ParserTests` passes, and
`tests.test_basics.Split.test_all_methods_reachable` passes (512 methods: no
plugin method was added). Every file-based test fails here with
`PermissionError` on the first write inside the platform temp area, so
`test_life_loop`, `test_her_days`, `test_qzone`, `test_basics` (its two
plugin-making tests), `test_golden` and `test_golden_standalone` could not be
checked here. The new file's own file-based tests could not run either.

What was checked instead, with in-memory stand-ins for the files
(`read_state`/`save_state`, `her_days.Store`, `works.add`):

- a 写歌 choice through `tick` keeps one song, writes one `self` memory, puts
  the work id on the day's row, and the song call's prompt has no chat in it
  while the picking call's prompt does;
- a song over a red line keeps nothing and the day says "想写歌，没写出来";
- names, his too, are taken out of a song and it is still kept;
- a reading note picks only the page without `shared_in`; with no page it makes
  one call, sets `pending.go_browse` and says "想写读后感，没有能读的文章";
- 发呆 makes no second call, writes no detail and "此刻" is 发呆;
- a wish is written once and not twice, and a wish over a red line is not kept;
- the public line's prompt carries the recent work's title and first lines.
