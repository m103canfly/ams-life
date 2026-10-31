# 2026-10-31 move 5j-3 web: the panel knows the neutral place

The owner decided on 10-31 that her data is keyed by the neutral place, `group:<群号>` /
`private:<QQ号>`, not by AstrBot's session string. Since 5j-1, new events and memory origins
already use it; 5j-2 does the same for a person's `sessions`, and 7d renames the old data on
moving day. The panel (`pages/dashboard/app.js`) only understood session strings. A key like
`group:900001` was read as "no type", so its label, the dropdowns and the merging of variants
were wrong.

This change only touches `pages/dashboard/app.js` and the `app.js?v=` tag in
`pages/dashboard/index.html`. Nothing looks different.

## What changed

- `parseSessionKey(key)` reads the neutral place first:
  - `group:X` → `{platform:"", type:"GroupMessage", id:X}`;
  - `private:X` → `{platform:"", type:"FriendMessage", id:X}`;
  - `web:…`, `other:…` and `self` → `{type:""}`, with the key itself as `id`.

  Anything else goes through the old session-string split, unchanged. Old keys still come from
  data not yet renamed and from old backups.
- `canonicalSessionKey(key)` now returns the neutral place, worked out exactly as Python's
  `canonical_session_key` (`discretion.place_of` since 5j-1):
  - `…GroupMessage…` / `…GuildMessage…` → `group:<id>`;
  - `…FriendMessage…` / `…TempMessage…` → `private:<id>`;
  - a neutral place (`group:`, `private:`, `web:`, `other:`, `self`) is kept as it is, and an
    empty key gives `""`;
  - `…OtherMessage…` → `other:<id>`, and a key with no kind at all → `other:` + the key.

  As in Python, the kind is searched anywhere in the key, and `:` / `_` are trimmed from both
  ends of what follows it. So the `:` form, the `_` form and the neutral place of one chat
  become one dropdown item, and a person no longer appears twice.
- The places that use these two functions are unchanged:
  - `_relationshipSessionKeys`, `collectSessionVariants`, `_sessionHasEvent` and `_sessionHasMemory`;
  - the event cards, the summary and memory filters, the session list and the event chains;
  - `_coreSnapshot` and the related events of a person.

  None of them compares `ev.session` with a session string directly. The memory row's delete
  still sends the row's own stored session, not the canonical one.
- `orb.js` hashes `ev.session` for the layout. A neutral place hashes fine, and only the position
  differs from the old form, so it is not changed.
- `app.js?v=` is bumped to `20261031-2`.

## Side effects worth knowing

- A `TempMessage` chat is now listed as `私聊 · <名字>` and a `GuildMessage` chat as
  `群聊 · <号>`, the same as the Python side. Before, they were `临时会话` and `频道`.
- The sample that shows when the panel is not connected uses the key `demo:session`. It is now
  `会话 · other:demo:session` instead of `会话 · demo_session`.
- An event under a neutral place now finds its live core, so its card shows the message window.
  Before, such a card said “旧事件没有逐条消息窗口”.

## Checked

- **The JS rule against Python.** A scratch script ran `canonicalSessionKey` from this `app.js`
  and `discretion.place_of` on the same 27 made-up keys. They agreed on all 27. The keys were:
  - the `:` and `_` forms of Group, Friend, Temp, Guild and Other keys;
  - neutral places, `self` and `web:…`;
  - an empty key, spaces, and odd keys such as `default:GroupMessage:` and `x_GroupMessage__900001__`.
- **On the panel.** 4c's `PanelServer` on 127.0.0.1 served this branch's `pages/`, and also a
  copy with main's `app.js` for comparison. Made-up handlers sent made-up data:
  - events under `default:GroupMessage:900001`, `group:900001`, `private:10001` and
    `default_FriendMessage_10001`;
  - memory under `default_GroupMessage_900001`, `group:900001` and `private:10001`;
  - two people whose `sessions` mix `:` strings, `_` strings and neutral places.

  Headless Edge drove the 活动会话 view.
  - This branch:
    - the session list and both dropdowns show `群聊 · 900001`, `私聊 · 编的小明` and
      `私聊 · 编的小红`, each once;
    - picking the group shows both group events (old form and neutral), and picking 小明 shows
      both of his;
    - the memory list merges the two group keys (“合并 2 个原始 key”);
    - no script errors.
  - Main: five items, including `会话 · group_900001` and `会话 · private_10001` next to the old
    forms, and each pick shows only one form.
- **The real AstrBot was not started.**
- **Tests:** `test_look`, `test_brain_panel`, `test_plugin_pages`, `test_memory_list_page` and
  `test_repo_link`, the tests that read the panel pages, all passed. There is no node test for
  `parseSessionKey`. By the owner's rule of 10-31, the full suite runs once everything is written.
- `node --check` passes on `app.js`.
