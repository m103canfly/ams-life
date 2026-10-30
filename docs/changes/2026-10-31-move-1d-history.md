# 2026-10-31 move-1d-history: her conversation history, apart from AstrBot

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Step 1 is "split the layers, fix the interfaces", and this is its fourth interface: the conversation
history. What the model is given as "what was said before" is today AstrBot's per-session copy: it
does not say who said which line, and deleting a person can only clear it whole. After the move the
history is ours: one SQLite file, one row per line, with where it was said, who said it, its message
id, who it is about and which messages it came from, so a person or a message can be deleted row by
row.

New files only; no existing file is changed, so behaviour and the golden traces stay the same. The
plugin does not use the store yet; step 1, part 5 connects it to the reply flow and to
`mixin_discretion._forget`.

* `history_store.py`: `HistoryStore` (`append`, `recent`, `forget_person`, `forget_messages`,
  `clear_place`, `places`) over one `history` table. Standard library only (`sqlite3`, `json`,
  `time`); no AstrBot and no plugin mixin.
* `tests/test_history_store.py`: made-up numbers only, one database per test in
  `tempfile.TemporaryDirectory()`; checks the reads, the per-place trim, deleting by person and by
  message, `clear_place` / `places`, closing and reopening, the import rule, and that a forgotten
  line's words are really gone from the file's bytes.

`PRAGMA secure_delete = ON` is set on the connection: deleted lines are overwritten with zeros in
the file, not merely marked free, so forgetting a person really removes what they said. The journal
mode is SQLite's default; WAL is not used, because a WAL file can keep what was deleted. Every
change is committed, and an error is raised as it is, never swallowed.

New module line for README's table of modules (brought up to date later):

| `history_store.py` | 她自己的对话历史：一个 SQLite 文件，每行带地点、谁说的、消息号、跟谁有关，按人按消息删 |

Full suite: not run here. dsh's Windows sandbox cannot write the temporary files SQLite needs, so
even the new test file cannot run inside it. The dispatcher runs `python -m unittest discover -s
tests` outside; this change adds 11 tests to the 954 on main.

Written by dsh (DeepSeek Harness, headless, workspace-write), dispatched and checked by the build
window.

Full suite, run outside dsh's sandbox by the dispatcher: 981 tests, all OK (the file-backed tests that cannot run in the sandbox pass here); the golden traces did not change. Spot checks: turning `secure_delete` off fails item 8 (`test_deleted_words_are_gone_from_the_file`); a `forget_person` that looks only at `sender_id` fails item 6 (`test_forget_person`).

