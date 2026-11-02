# 2026-11-02 E3: what her hands and eyes can see, said as it is; a miss or a half-done thing, said too

Card E3, the first of the honest-series cards (E3 → E2 → E1 → G1b). Only `life_loop.py`,
`her_days.py`, the new `tests/test_honest_hands.py` and this note. `heybox.py` and its requests are
not touched: no private message, no notice is read.

## What changed

### 1. One table of what each menu item can and cannot show her (`life_loop.SEES`)

The table sits next to `BASE_MENU`. `materials()` writes one more line under `菜单：`, and only for the
items that are on this menu:

    这些事能做到什么：刷小黑盒：能看首页动态里的帖子，点进去看正文和评论；私信、通知看不到。 …

Each sentence is what the code does, and where it comes from:

| item | sentence | the code it is read from |
| --- | --- | --- |
| 刷小黑盒 | 能看首页动态里的帖子，点进去看正文和评论；私信、通知看不到。 | `life_loop.browse_heybox` reads `/bbs/app/feeds` (the front page's posts, `heybox.feed_items`) and `/bbs/app/link/tree` (`owner_only=1` for the post's text, `is_first=1` for its comments). No other path of `heybox.PATHS` is used: `/account/get_qrcode_url/` and `/account/qr_state/` are the sign-in only. |
| 去测试群看看 | 能看群里新发的图，看中的收成表情包；大家在群里聊的字她不看。 | `mixin_group_browse._group_queue_sticker` queues only the pictures of a group's messages (`_sticker_refs`), `_group_open` takes them, `_group_look_pending` looks at up to three of them and `_maybe_keep` keeps the ones `stickers.should_keep` accepts. No text of the group is read anywhere on this path (it clears `unread` and forgets `people`). |
| 刷手机 | 能上网搜几样东西、读几个网页，看到的记下来；没有人回她的话。 | `mixin_browse._browse_trip`: model rounds with only the two browse tools (search, read), `browse.parse_trip` after them; what she saw becomes web memories (`_remember_web`), and a wish to tell someone may be kept (`add_wish`). Nothing on a trip is answered by anyone. |
| 发说说 | 能发一条说说，一天最多两条，只有他一个人看得到；别人的说说和评论她看不到。 | `qzone.post`: two a day (`if data['days'].get(day, 0) >= 2`), sent as `{'ugc_right': 16, 'target_uins': [owner]}` — the owner-only post the module is named for. Nothing in `qzone.py` reads a post of anyone else or a comment. |
| 拍照 | 能按她写的描述生成一张照片存下来，可以配到今天的说说上；照片拍成什么样她看不到。 | `mixin_selfie._make_photo('photo', …)` writes one picture from her description through the image service; `life_loop.photo` keeps its path and date in `state['last_photo']`; `apply_choice` gives that picture to today's 发说说. Nothing looks at the picture after it is made (no vision call on it). |

吃饭、睡觉、休息、发呆、写歌、读后感、整理本子 are not in the table (the card says they do not need it).

### 2. A 小黑盒 look that did not happen is written in the day

`life_loop.HeyboxRead` (`read`, `why`; falsey when `read` is 0) is what `browse_heybox` returns now,
instead of `True`/`False`. The reasons are the five the card names:

- `没有新帖子` — no unseen post on the front page;
- `今天刷够了` — six looks are already counted for today;
- `没登录上` — no saved credential, or the account can no longer be used (`heybox_ready`);
- `今天的钱到线了` — the day's money is used up (`budget`/`_spent_today`);
- `没挑到想看的` — the model picked nothing, or none of the picks had a text to read.

`tick` then rewrites the day's own line for her own 刷小黑盒 choice (`life_loop.day_heybox_line`):
`看了 N 篇` when she read N posts (no title, so nothing from outside comes into the day), or
`想刷小黑盒，没看成：<why>`. When a look does not even get that far and there is no true reason among
the five (the 小黑盒 function switched off, or she is asleep), it says only
`想刷小黑盒，没看成` rather than name a cause that is not so. The automatic looks on waking, at lunch
and before sleep (`automatic_heybox`) write no day line, as before.

### 3. A thing put down halfway is written in the day

`life_loop.put_down_after(item, now)` gives the minutes she gave a thing of her own that another
choice took the place of. It is `None` unless: the item is hers (`source == 'her'`), was chosen from the
menu (it has a `kind`), is not 发呆/什么都不干, is not 睡觉, and has not reached its end (`now < end`).
`apply_choice` records it with `her_days.Store.set_stopped` on the day row it is leaving (`state['last_item_id']`,
the same id `set_liked` uses), before the new row is added.

The new field is `stopped_after` (minutes). `minutes` is still the plan she wrote. `materials`,
`post_materials` and `own_lines` show that row as `打算 X 分钟，做了 N 分钟就放下了` through `length_shown`
(the card names the materials line; the other two read the same "今天已经做过" rows, so they say the same).

### 4. `her_days.Store` can correct a row

`set_liked` is unchanged in behaviour; it and the two new ones go through `_set_field`, which finds the
row by id and writes only then (a missing id returns `False` and touches no file):

- `set_detail(id, text)` — what she actually did, at most 40 characters;
- `set_stopped(id, minutes)` — the `stopped_after` field, an int of at least 0.

## How it was checked

The nine things the card asks for are in `tests/test_honest_hands.py`: the SEES line follows the menu
(with and without 刷小黑盒); a look with no new post, with six looks already today, and one that read a
post (counted, no title); a song put down after 20 of its 60 minutes (`stopped_after` 20, `minutes`
still 60, and the materials saying so); a song that ran its whole 60 minutes (no `stopped_after`); 发呆
and 睡觉 replaced halfway (no `stopped_after`); the automatic look writing no day row and calling no
model; and the two new store methods on a missing id (false, file bytes unchanged).

**The tests could not be run in this sandbox.** Python here cannot create a directory in the platform
temp area (it is outside the worktree): even the existing files stop at
`PermissionError: [WinError 5]` in `tempfile.mkdtemp` / `Path.mkdir`, before any test body runs. So no
test file could be run, and `test_golden` was not re-recorded. `life_loop` is not part of
`tests/scenario.py`, and no test data of hers is in `tests/golden/`, so the traces are not expected to
change; the dispatcher should run the card's list outside.

What could be checked here was checked read-only, in a plain interpreter (nothing written to disk):
the SEES line appears only for the items on the menu and carries `私信、通知看不到` only with 刷小黑盒;
`put_down_after` gives 20 for a 60-minute song after 20 minutes, and `None` at its end, for 发呆, for
睡觉, for a schedule item and for an item set by a chat tool; `length_shown` reads back
`打算 60 分钟，做了 20 分钟就放下了`; `HeyboxRead` is falsey with 0 posts and true with 1; a store with no
id returns `False` without creating anything; and `day_heybox_line` does nothing without a day row.
