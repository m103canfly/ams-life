# 2026-11-02 heybox inbox

One look at 小黑盒 now also sees the private messages and the notices. It reads one more
address, keeps only counts, a name and one line, and answers nothing.

## What changed

- `heybox.PATHS` gains `/bbs/app/user/message` and nothing else. Any address not in that
  set is still not sent, so there is still no reply, like or follow request.
- `heybox.inbox(result)` is a pure function. It keeps at most five conversations that
  have unread messages: the unread `count`, the other person's name, and `text_only` of
  the last line cut to 60 characters. Notices are the `header` items with `count > 0`
  (labelled by their `text`) and the positive numbers in `message_unread_num` (labelled
  by their own keys). A missing field or a value of the wrong type skips that row and
  raises nothing.
- `browse_heybox` reads `/bbs/app/user/message` with `list_type=2`, `offset=0`, once,
  before the front page, inside the same look and on the same daily count. A read that
  returns `None` means only "this time the private messages were not seen"; the front
  page is then read as usual.
- No new posts but unread messages or notices: she is still asked for a thought once,
  and the material holds only the private-message paragraph. That look's `HeyboxRead`
  keeps `read=0`.
- The material says, for the private part: this is what someone told you in private, it
  may only be said in front of that person, you cannot answer now and cannot see the
  whole conversation, only the last line. Then each name, its unread count and its last
  line. Notices are given as counts only, with "only the count, not the content". Nothing
  new says `私信和通知：没有新的`; a failed read says `这次没看到私信和通知`.
- Every private name and last line of the look joins the same forbidden list the chat
  uses: a thought holding one is not remembered, and a word to him holding one is not
  sent. A tell that only says someone wrote (`有人私信我`), with no name and no words of
  theirs, is not stopped.
- The private messages go into no memory, no day line and no file. The day line keeps
  E3's words and adds the counts at the end, without a name or anyone's words: for
  example `看了 1 篇；有 2 条私信、3 条通知`. When nothing new was posted but something
  came in, the line is `没有新帖子；有 4 条私信` (she did see something, so it is not
  written as "没看成"). With no messages the E3 lines are unchanged, including
  `想刷小黑盒，没看成：没有新帖子`.

## Name keys, and why they are tried in that order

The trial read showed a `user_a` object with an avatar and a nickname, but not its
contents, so which key holds the nickname is not known. `username`, `nickname` and `name`
are tried in that order (the usual account/login name first, then the display name), and
a value that is not a non-empty string is skipped. A conversation with none of them is
written as `有人`.

## Unknown, and risk

- Whether reading this address marks the private messages as read is **unknown**. The
  trial read returned no `Set-Cookie`, and nothing else shows it either. The messages are
  only read; nothing is sent, so nothing else can change them.
- The risk is the same kind as reading the front page: one more request to a service
  whose client is not documented. No guarantee can be given that this does not raise the
  ban risk.
- The whole conversation is not read: the trial read found no address for it.

## Test results

`tests.test_heybox_inbox` is new (15 tests). Run in this sandbox as-is, 9 pass; the other
6 need a writable temporary directory and fail with `PermissionError` because the sandbox
denies the platform temp area. With that directory placed inside the workspace all 15
pass, which was done once for verification and then removed.

Each acceptance file was run on its own, as-is. Those that create a temporary directory
failed with `PermissionError`; the same module was then run once more with that directory
placed inside the workspace (nothing outside it was written), and cleaned up afterwards:

- `tests.test_heybox_inbox`: as-is 9 pass, 6 `PermissionError`; with a workspace temp
  Ran 15 tests | OK
- `tests.test_heybox`: as-is `PermissionError`; with a workspace temp Ran 29 tests | OK
  (1 skipped: aiohttp is not installed)
- `tests.test_heybox_page`: Ran 12 tests | OK as-is
- `tests.test_honest_hands`: as-is `PermissionError`; with a workspace temp Ran 10 tests
  | OK
- `tests.test_life_loop`: as-is `PermissionError`; with a workspace temp Ran 41 tests | OK
- `tests.test_golden`: as-is `PermissionError`; with a workspace temp Ran 2 tests | OK
  (the golden traces are unchanged)
- `tests.test_golden_standalone`: as-is `PermissionError`; with a workspace temp 4 of 6
  fail with `ModuleNotFoundError: No module named 'aiohttp'` from the scenario
  subprocess (2 pass). This is a missing dependency in this Python, not a result of this
  change; the dispatcher runs it outside.

`tests.test_life_context` (11 | OK) and `tests.test_owner_name` (20 of 22 pass, the two
sticker tests failing on the same temp-area denial) also pass with a workspace temp; they
are the two other callers of `heybox_ask_prompt`.

The full suite was not run, as instructed. No file outside the card was changed.
