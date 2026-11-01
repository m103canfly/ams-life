# What one reply sees: this place's last day, at most 200 lines

Her replies used to look at the last 20 stored turns only. The history store keeps the
turns she answered, so in a group everything other people said without her answering was
invisible. Now a reply sees the place's last 24 hours, at most 200 lines, in time order.

## One ruler

`history_store.py` holds the only two numbers, so every caller shares them:

- `CONTEXT_SECONDS = 24 * 3600`
- `CONTEXT_ROWS = 200`

`app.py` uses them for `--history` (now 200) and the new `--history-hours` (now 24), and
passes both to `turn_runner.run_turn`, which passes them to the reply. The history store's
own cap (`KEEP_PER_PLACE`) and the phone window's cap (`WINDOW_SECONDS`) are unchanged.

## How the two sources join

`history_store.recent` accepts `since`: only rows at or after that time. A call without
`since` returns exactly what it did before (`{"role", "content"}`). With `since`, each row
also carries `ts` and `message_id`, which the phone side needs to merge and de-duplicate.

`PhoneMixin._reply_context(event)` builds the reply's history:

- her history store's rows for this place within the day (the turns she answered, her
  words in full);
- the window's `user` lines whose `msg_id` is not among those history rows' `message_id`
  and is not this message: others' lines she did not answer, each as one separate `user`
  line framed by `_phone_line` (time, name, `（原文）`). One message is one line, so
  `_history_original` marks each by its own start;
- her own window lines are not used, because the window keeps only 80 characters of them.

The merged list is sorted by time and cut to the newest `limit` rows. `_window_lines(event,
6)` and the other small callers are unchanged: the reply already sees the whole window, so
they are not given it twice.

## Forgetting

Nothing new is kept: forgetting still deletes rows from the store and lines from the
window. A wider history does not bring deleted lines back. The tests check that after
`_forget(person=...)` neither source has anything left and the next reply sees none of it.

## Cost

Prices are `mixin_attention.DEFAULT_PRICES` (deepseek-flash, peak, rounded up): 2.2 yuan
per million input tokens without a cache hit, 0.05 with one, 8.7 for output. A line is
about 30 tokens (the time and name part about 13, an ordinary sentence about 12).

- 200 lines ≈ 6000 tokens, against about 600 before: 5400 more. The system prompt changes
  every turn and the history follows it, so the first round counts as a cache miss: about
  **0.012 yuan more per reply**. Tool rounds in the same reply reuse the prefix, so they
  are nearly free.
- 100 replies a day ≈ **1.2 yuan more**; 300 ≈ 3.6 yuan.
- Worst case (200 lines of 300 characters) ≈ 39k tokens: about **0.085 yuan more per
  reply**, 8.5 yuan for 100 replies. That can reach the daily line (8 yuan: owner's
  private chat only; 10 yuan: stop), which is unchanged.
- In the owner's private chat there are a few dozen lines a day, so a reply costs under
  0.01 yuan more and a day a few tenths of a yuan.

## Behaviour and tests

Every reply now includes the last 24 hours' unanswered lines of its place, so it can
answer what was said around it; nothing else about a turn changes. AstrBot's old path
(`main.py`) is unchanged, as agreed on 11-01.

New file `tests/test_reply_context.py` covers: answered turns plus unanswered window lines
in time order with the current message not repeated; the 24-hour edge (25 hours out, 23
hours in); 250 lines cut to the newest 200; her long reply in full once (the window's 80
characters are not repeated); forgetting leaving nothing visible; private and group places
staying apart; and `recent` unchanged without `since`. The method count in
`tests/test_basics.py` moves from 511 to 512 for `_reply_context`.

Sandbox note: in this worktree Python can create one directory in the temp area but not
write inside it, so every test that keeps its data in a temp folder fails with
`PermissionError` before running (this includes test_basics' two plugin-construction
tests, test_history_store, test_turn_runner's file-based cases, and the golden tests).
The dispatcher runs them outside. The parts that need no files were checked directly:
`test_basics` counts 512 methods and passes 9 of 11 (2 errors from the temp-folder
`PermissionError`), `test_turn_runner.Helpers` passes 4 of 4, and the reply-context merge,
the `since` filter, the 200-line cut and `_phone_line` were exercised in memory. Golden
traces are expected to be unchanged: AstrBot's path does not use this, and the standalone
scenario does not record the model's messages.
