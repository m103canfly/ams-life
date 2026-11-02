# 2026-11-02 E2: a thing that matters comes in, and she weighs it herself

Card E2. Three marks she may write at the end of a reply and never sends: putting down what
is in her hands for something that matters more, looking him up later, answering him later.
A thing she put down calls her while she is busy; a due row does not wait for the quiet
gate; going on with what she had is on the menu while her hands are full; and the first
thinking after a sleep says what she missed.

Files: `attention.py`, `mixin_turn.py` (only `_after_reply` and the note in the material),
`mixin_selfie.py` (only `_now_line`), `life_loop.py`, the new `tests/test_put_down_marks.py`
and this note. Nothing was committed.

## The three marks (`attention.py`)

`PUT_DOWN`, `OWNER_LATER` and `OWNER_REPLY_LATER` sit beside `SILENT`. `take_marks(text,
private=False)` gives `(clean words, marks)`:

- `【放下手上的：为什么】` — a why of at most 40 characters;
- `【过会儿再找他：大概几分钟，为什么】` — minutes 1-1440, a why of at most 40 characters;
- `【过会儿再回：大概几分钟】` — minutes 1-1440.

The last two are read in his private chat only; anywhere else they are cut out as if she had
not written them. A mark written badly (no closing bracket, minutes out of range, a why too
long, a missing why) is cut out too and is not taken. Only the marks themselves are cut:
`【不说】` and `【下一条】` stay for the code that already reads them.

`MARKS_NOTE` (everywhere, after `CHOICES_NOTE`, inside the `self_decide` block) and
`MARKS_NOTE_OWNER` (his private chat only) say what she may write and that these are not
sent.

## The reply (`mixin_turn._after_reply`)

The marks are taken out right after `interpretation.strip_state_tags`, before the sticker,
before `【不说】` and before the look before sending. What is left is what is sent, kept in
her history and put in the window; the marks are in none of them. A reply that is only
marks (or `【不说】` plus marks) is silence: nothing is sent, and the marks are handed on
all the same. A look that holds the whole reply back does not take the marks with it
either: they are handed to `life_loop.note_mark` before the look.

`mixin_selfie._now_line` adds `打算到 HH:MM` after `已经 N 分钟`, for a thing she chose
that has an end (`source == "her"` and a length); the day's own schedule has no end of hers
and says nothing.

## What is kept (`life_loop.note_mark`)

Nothing is kept while the life loop is off. A why goes through `anonymized` (names of
others taken out) and the red lines (`redline.hit` and `plugin._red_line`); one that does
not pass drops the mark. A thing put down is kept as the newest one in `state['put_down']`
with its `id`, `why`, `ts` and `here`. The two later marks add a row to `state['due']`:
`{'id', 'ts': now + minutes * 60, 'kind': 'owner_later', 'why', 'set_at'}` or
`{'id', 'ts', 'kind': 'owner_reply_later', 'set_at'}`. The due table keeps at most 20 rows,
the oldest dropped first.

## When she is called, and in what order (`life_loop.tick`)

The reason is picked in this order: the end of a thing or a waking > a fresh start > a
thing she put down > her body crossing a line > a due row > a quiet stretch.

- A thing put down calls her with `聊天里有件事你觉得要紧：<why>。你手上在做：<doing>，打算到
  HH:MM。急不急你自己掂量。` The id is remembered once it has called her, so the same thing
  never calls her twice.
- A due row calls her in words of its own: `之前想过会儿再找他：<why>（HH:MM 那会儿想的）`
  or `他 HH:MM 找过你，你说过会儿再回`. Several rows that came due together are said
  together. Each row is taken out of the table when it has called her.
- While she sleeps (`state['sleep']` or a sleeping item not ended) nothing calls her. The
  put-down thing and the due rows stay where they are and are reckoned with after waking.

### The 600 seconds

A thing put down and a still-unhandled due row never wait for the quiet gate: like the end
of a thing and a fresh start, they call her whatever `last_think_ts` says. They still count
into the same 48 thinkings a day, and no other limit is added.

## He spoke first

When his last private line is still unanswered (or one of her `owner_reply_later` rows has
come due), the tell is asked for and given even with `proactive_owner_enabled` off: he
opened the conversation, so answering him is not speaking up on her own. Then the tell may
be 300 characters instead of 80 (`parse(..., tell_max=...)`). It goes out through the same
`tell_owner`, with the same money line, the same sleep check, the same leak check and the
same red lines; only the switch's refusal is lifted for this one.

## Waking up

The tick that wakes her remembers the sleep in `state['woke_sleep']`. The next thinking
says `你睡着的时候：HH:MM 到 HH:MM 在睡觉。`, marks his lines from those hours with
`（你睡着时）` in the chat block, and says any `owner_reply_later` that came due. Whether to
answer, and whom first, is hers. The group half of this (E2s) is not in this card.

## Going on with what she had

`CONTINUE_WORDS` (`接着做刚才的`) is on the menu only while something of her own is in her
hands and has not run its time (dazing is not work). Choosing it writes nothing new: no
`_set_now`, no line in her day, the same thing and the same end. `handled_item` is still
taken out, so its own end calls her again with `刚才那件事到时候了`. `tell`, `wish` and
`liked_last` are kept as before. Choosing anything else is putting it down, which E3 will
write as `做了 N 分钟就放下了`.

## What one more thinking costs

One more `life` model call, the same price as any thinking: the material is under a
thousand tokens and the answer is a small JSON, so about **0.01-0.02 yuan** a call at
`DEFAULT_PRICES`. A day of them stays inside the unchanged money line (8 yuan: his private
chat only; 10 yuan: nothing), and the 48 a day cap is unchanged.

## Tests

New file `tests/test_put_down_marks.py`, 19 tests, a fake plugin, a fake clock and a fake
model, no network: the mark in a reply is not sent, not kept in the window and kept in
`state['put_down']`; `【不说】` plus a mark sends nothing and keeps the mark; both marks
about him in a group are cut out and stored nowhere, in his private chat they fill the due
table with the right `ts` and `kind`; a name in the why is taken out and a red line drops
the mark; a thing put down calls her while busy and inside the 600 seconds, and never twice;
while asleep nothing calls her and the mark waits, the waking says `你睡着的时候：` and the
next minute brings it; going on keeps the thing, writes no day line, and its end calls her;
going on is offered only while it lasts; an `owner_later` row calls her at 29 no and 30
minutes yes, once; an `owner_reply_later` row comes due, the tell is given with the switch
off, up to 300 characters, and goes out through `tell_owner`; the tell is there when he
spoke first and gone when she has answered; his lines from the sleep are marked and his
line from before it is not; the now line says `打算到` for her own thing and not for the
schedule; with the loop off the marks are still cut out and nothing is kept; a mark with no
closing bracket is cut out and nothing is sent.

## Test runs in this sandbox

Run one file at a time. In this worktree Python may create one directory in the temp area
but not write inside it, so every test that keeps its data in a temp folder stops with
`PermissionError` before running:

- `python -m unittest tests.test_put_down_marks` — Ran 19 tests, 34 errors, every one
  `PermissionError`; no test body runs.
- `python -m unittest tests.test_life_loop` — Ran 41 tests, 78 errors, all `PermissionError`.
- `python -m unittest tests.test_basics` — Ran 11 tests, 2 errors, both `PermissionError`.
- `python -m unittest tests.test_golden_standalone` — Ran 6 tests, 4 errors (`PermissionError`
  in the temp area); the two placeholder tests pass.

The other named files were run only through the local-root runner below; their temp folders
are created the same way and would stop the same way.

To check the code rather than the sandbox, the same files were run again with
`tempfile.TemporaryDirectory` pointing inside the workspace (a local substitution in the
runner only; no file of the repository and no `TEMP`/`TMP` was changed):

- `tests.test_put_down_marks` — Ran 19 tests, **OK**.
- `tests.test_life_loop` — Ran 41 tests, **OK**.
- `tests.test_life_context` — Ran 11 tests, **OK**.
- `tests.test_attention` — Ran 41 tests, **OK**.
- `tests.test_sleep_when_sleepy` — Ran 18 tests, **OK**.
- `tests.test_selfie` — Ran 46 tests, **OK**.
- `tests.test_basics` — Ran 11 tests, **OK**.
- `tests.test_golden` — Ran 2 tests, **OK**.
- `tests.test_golden_standalone` — Ran 6 tests, 4 failures: the scenario process stops with
  `ModuleNotFoundError: No module named 'aiohttp'` (`scenario_standalone.py` imports
  `panel_api`). That is a missing third-party package in this sandbox, not a difference of
  the traces; the two placeholder tests pass.

Golden traces: unchanged, and none was rewritten. `tests/scenario.py` runs with
`self_decide` off, so neither the new note lines nor `打算到` reach its material (its now
line is the schedule's, and no life-loop tick writes `now.json` there).
`tests/scenario_standalone.py` does turn `self_decide` on, but `GOLDEN_A` already allows
the whole `turns[*].inject[0]` text to differ, so the note line it gains is covered. It
could not be run here for the missing `aiohttp`; the identical `A -> B0` and `B0 -> B`
comparisons are on both sides of the same code, so only `golden -> A` looks at this line at
all.

## Unsure about

- The card's test 6 talks about "the material of the waking thinking (or of the next
  minute)". The waking thinking's reason is the waking itself, so the thing put down is
  named in the material of the next minute (it is not consumed meanwhile, and it does not
  wait 600 seconds). That is what the test checks.
- A due row is still taken out of the table by any thinking, as before this card (the tick
  has always done that). So if a row comes due in the very minute a thing of hers also
  ends, the row's own words are not in that material. Changing that seemed outside the
  card.
- `note_mark` takes minutes only for the two due marks; a put-down row carries `minutes: 0`
  from `take_marks` and none in the state.
- `【过会儿再找他：30 分钟，为什么】` (a word after the number) is read as a badly written
  mark: it is cut out and not taken.
- No plugin method, setting, dependency or golden file was added or changed. Nothing
  outside this folder was read; nothing was committed.
