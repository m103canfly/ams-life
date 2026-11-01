# 2026-11-01 move 5e-27 web: the stickers page shows where each one may be sent, and the owner can publish hers

5e-27 (Python half #151, merged) gives every sticker a share scope: old 小爱's and the owner's go
everywhere; the ones she kept herself are sent only where she kept them, until the owner publishes
them. This is the web half. Only `pages/stickers/` and its copy `pages/dashboard/stickers/` are
touched (the two stay byte for byte the same); no Python.

## What changed

- Every card has a tag: 只在存下的地方用 or 所有地方都能用 (from the list's `scope`, `"here"` / `"all"`).
  No group or number is shown; the page never gets one.
- The detail has a row 能在哪用, and for the ones she kept herself a button: 发到所有地方 when it is
  `here`, 收回 when it is `all`. Old 小爱's (from 旧小爱) and the owner's get no button; they are
  everywhere anyway.
- The button posts `page/sticker_scope` `{id, scope: "all" | "here"}` through the same `post()` as
  删掉这张 (the panel token on our own server, the bridge's `api:post` inside AstrBot). On success the
  detail and the card change in place.
- 发到所有地方 first asks (the page's own confirm, like 删掉这张): 发到所有地方以后，她在别的群、别的
  私聊里也可能发这张。确定吗？ 收回 does not ask.
- The footer says the rule in one line. The made-up preview (no bridge) has scopes too.
- `stickers.css?v=20261101-1`, `stickers.js?v=20261101-1`.

## Where this differs from the card

- The card did not ask for the question before publishing. Publishing can take a picture from a
  private chat into groups, so it asks once, as deleting does.
- The list says `from` and `owner` but not the source itself, so "old 小爱's" is told by its
  label 旧小爱 (`stickers.OLD_LABEL`).

## How it was checked

- Our own server: `app.py` from this branch on a made-up data folder and a test port, with a
  made-up library written through `stickers.Library` (kept in a group, kept in a private chat, kept
  and published, old 小爱's, the owner's). In a headless Edge, with `window.confirm` replaced in the
  page (no real dialog):
  - the five cards show the right tag; no group number, number, `group:` or `private:` on the page;
    the list's fields have `scope` and no `from_where`;
  - old 小爱's and the owner's: no button; the published one: 收回; the group one: 发到所有地方;
  - 发到所有地方 asked once, posted `{id, scope: "all"}` with the token, the server then says `all`;
    收回 posted `here`, the server says `here`; saying no to the question posted nothing.
- AstrBot side: the scratch AstrBot stand-in. The panel opens the stickers page in its frame; 发到
  所有地方 went out as `api:post page/sticker_scope` with `scope: "all"`, and the card changed.
- Tests, one file at a time: `test_stickers_wire` 29, `test_sticker_scope` 5, `test_panel_api` 20,
  `test_golden` 2, `test_golden_standalone` 6 pass. `test_stickers` has 1 failure
  (`InAReply.test_a_few_offered_by_topic_and_mood_none_just_sent`: `pick_candidates` without a
  place now returns nothing); it fails the same on main without this change, so it comes from the
  Python half, not from this page.
