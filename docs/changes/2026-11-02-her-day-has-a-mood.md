# 2026-11-02 M1: her own day has her mood in it

Card M1. The material she picks a thing to do from, the material a song or a reading
note is written from, and the material a public line is written from used to hold only
three bodily needs (sleepy, hungry, tired). Now each of them says how she feels as well.
Only `life_loop.py`, the new `tests/test_life_mood.py` and this note. `interpretation.py`
and `body.py` are not touched.

## What changed

`life_loop.mood_line(core)` gives `心情：` plus `interpretation.body_brief(core)`; it is
`''` when the brief says nothing. The brief is called as it is: no second mood writer,
no change to it.

The line is added once in each of the three materials, just after the feel lines:

- `materials` — choosing what to do at this moment;
- `own_lines` — what a song or a reading note is written from (`song_materials` and
  `review_materials` build on it, so they have it too);
- `post_materials` — what a public line is written from.

Nothing else changes. There is no new model call, no new money, and no line telling her
what to do or not do with the mood: she weighs it herself. The brief carries no numbers
and no names, so neither does the line.

The brief and `bodily.feel_lines` may both mention being sleepy ("有点困了" / "有点困。");
they are not de-duplicated. The card asks for the brief's own words, and the two are
different views of the same body.

Honesty: the line is read from the same `core` the tick already decayed
(`plugin._core(None)` then `_decay_to_now()`), at the moment the material is built.
Nothing is stored, and nothing is invented.

## Tests

`tests/test_life_mood.py` — five tests, a fake plugin and a fake model, no network, no
file written: `DATA_DIR` and `STATE_DIR` point at a path that is never created (a missing
day file reads as empty), and the fake model is never called.

1. `core.v = -0.5` → `心情：心里有点沉` in `materials`; `core.v = 0.5` → `心情：心情不错`
   and no `心里有点沉`.
2. The same line is in `own_lines` (写歌), `song_materials` and `post_materials` (写说说).
3. `body_brief` returning `''` or `None` → no `心情：` line in any of the three.
4. A `woken` mood event one minute old → `刚被吵醒` in all three.
5. Numbers changed between two builds → the second line follows them (not remembered),
   and a fresh mood event shows up at once.

## Test runs in this sandbox

Run one file at a time:

- `python -m unittest tests.test_life_mood` — Ran 5 tests, **OK**.
- `python -m unittest tests.test_life_loop` — Ran 41 tests, 78 errors, every one
  `PermissionError: [WinError 5]` in `TemporaryDirectory` (`states` mkdir and cleanup).
  No test body runs, so `Ran` counts them, but no assertion ran.
- `python -m unittest tests.test_life_context` — Ran 11 tests, 22 errors, all
  PermissionError.
- `python -m unittest tests.test_real_things` — Ran 21 tests, 27 errors, all
  PermissionError.
- `python -m unittest tests.test_golden` — Ran 2 tests, 2 errors, both PermissionError.
- `python -m unittest tests.test_golden_standalone` — Ran 6 tests, 4 errors, all
  PermissionError; the other two passed.

No assertion failed anywhere: every error is the sandbox denying the data directory
(Python may create the temp directory but cannot write or remove inside it). The card's
list should be run outside this sandbox.

The golden traces are not expected to change: they go through the reply path, which uses
`interpretation.body_brief` as before, and `life_loop` is not part of the golden scenarios.

## Unsure about

- The prefix repeats the mood word: the line reads `心情：心情平平。…` or
  `心情：刚被吵醒，还有点迷糊，有点起床气。心情平平。…`. The card asks for exactly
  `心情：<body_brief(core)>`, so the brief's own first word is kept.
- `body_brief` ages a mood event from the real wall clock (`time.time()` inside it), not
  from the `now` the caller passes. The line is therefore honest about "the last hour"
  in real time even when a test passes a fixed clock. `interpretation.py` was left as is.
- No plugin method, switch, dependency, golden fixture or other file was added or changed.
  Nothing outside this folder was read; nothing was committed.
