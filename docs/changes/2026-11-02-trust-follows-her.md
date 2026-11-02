# 2026-11-02 K1: the trust in each person follows how she really felt while hearing them

Card K1, on branch `dsh-k1` cut from main `497f1be`. The files this change touches:

- `mixin_people.py` — only `_touch_user` and the constants at the top of the file;
- `mixin_turn.py` — only the few lines around `observe` in `_prepare_turn`, plus passing
  `reaction` into `_touch_user`;
- `tests/test_trust_follows_her.py` — new;
- `tests/test_owner_name.py` — one line: its stand-in `_touch_user` takes the new `reaction`
  keyword too, otherwise the real `_prepare_turn` it drives would raise `TypeError` (see below);
- `tests/golden/basic.json` and `tests/golden/full.json` — re-recorded, not edited (see below);
- this note.

`body.py` and `relationship_meta.py` are not touched. No new plugin method, so the method count
stays 512.

## What was wrong

`_touch_user` updated each person's `trust` from `float(getattr(core, "trust", 0.5))`. Her body
has no `trust` attribute — `body._trust()` says "no global trust": it only borrows the other
person's trust while one `observe()` runs, and clears it afterwards. So `_ct` was always 0.5,
and every message pulled that person's trust 30% of the way to 0.5 (`old + 0.30 * (0.5 - old)`).
Nothing about how the message actually landed on her went in, and an ordinary sentence moved the
number anyway.

Because `relationship_meta.relationship_state` computes `closeness`, `conflict`, `repair` and
`predictability` from that trust, those four only followed her `social` and `stress`.

## What changed

### 1. The change is measured around `observe` (`mixin_turn._prepare_turn`)

Before `core.observe(text, …)` the turn reads `core.v` and `core.stress`; after it, it computes
`_reaction = {'v': Δv, 'stress': Δstress}` and passes it to
`_touch_user(event, core, reaction=_reaction)`. With no text to observe (no words, e.g. a picture
only) `_reaction` stays `None`. Nothing about her body is written differently: the delta is only
read, not stored.

### 2. Trust follows that reaction (`mixin_people._touch_user`)

Evidence of this one exchange, in −1…1:

    e = clip(Δv / TRUST_V_SCALE, -1, 1) - clip(Δstress / TRUST_STRESS_SCALE, 0, 1) * TRUST_STRESS_WEIGHT

New trust (then clipped to `TRUST_MIN`…`TRUST_MAX`):

    e > 0:  old + rate * e * (1 - old)      # near 1 it is harder to gain trust
    e < 0:  old + rate * e * old            # near 0 it is harder to lose what is left

`rate` is `TRUST_RATE` normally, and `memory_meta.nassar_alpha(e)` when `bio_learning` is on (the
same adaptive alpha as before, now fed this exchange's evidence). `reaction` is `None`, or
`|e| < TRUST_DEADBAND` (an ordinary sentence), leaves the trust exactly where it was.

The constants sit together at the top of `mixin_people.py`, with a comment saying what they are:
the rise and fall inside one exchange with this person, not a global number.

| constant | value | meaning |
| --- | --- | --- |
| `TRUST_V_SCALE` | 0.25 | a v change this big is full evidence in that direction |
| `TRUST_STRESS_SCALE` | 0.25 | the same for a rise in stress |
| `TRUST_STRESS_WEIGHT` | 0.6 | how much a rise in stress counts as bad evidence |
| `TRUST_DEADBAND` | 0.12 | below this the sentence was ordinary: no change |
| `TRUST_RATE` | 0.30 | how much of the evidence is taken in |
| `TRUST_MIN` / `TRUST_MAX` | 0.05 / 0.95 | the two limits |

Her own reaction is the truth here, so a warm line can still cost a little when her v dips (for
example a repeated line, which her body habituates to). That is the point of the card: the number
follows what really happened in her, not what the words look like.

## What is deliberately not in this card

- Keeping promises and repairing (`promises_kept`, `repair_state`) are still recorded where they
  already were; this card does not feed them into the trust. Whether they should count later is a
  separate question, to be taken up on its own.
- `closeness` still carries a little of her `social` and `stress`
  (`0.55*trust + 0.30*social + 0.15*(1-stress)`) — that is the existing formula and this card
  leaves it as it is.
- Part of `Δv` comes from `body._lexicon_deltas` (the emotion word lists). This card only connects
  the reaction the core already computes; that word-list layer is not this card.

## Old data

Trust that was already pulled towards 0.5 is not recomputed backwards. From this change on it
grows and shrinks by the real reaction, from wherever each person's number happens to be.

## Tests

`tests/test_trust_follows_her.py` — a fake plugin, a fake core and each person's record kept in a
dict, so no file is written and nothing of hers is touched. Nine tests, as the card lists them:

1. a line that lifts her v raises that person's trust;
2. a line that sinks her v and raises her stress lowers it;
3. an ordinary sentence does not move it, and twenty ordinary sentences in a row leave it at 0.38
   (the old code would have walked it to 0.5);
4. 0.9 with a good line stays ≤ `TRUST_MAX`, 0.1 with a bad line stays ≥ `TRUST_MIN`;
5. the same good line lifts the person at 0.2 more than the person at 0.9;
6. `reaction` is `None` → no change;
7. a changed trust changes `relationship.state.closeness` with the same `social` and `stress`;
8. with `bio_learning` on, the fake `nassar_alpha` is called once, with `e`, and its rate is the
   one taken in (0.5 → 0.655);
9. A is lifted and B is lowered in the same exchange, each in their own record.

## The goldens

`AMS_UPDATE_GOLDEN=1 python -m unittest tests.test_golden` cannot run in this sandbox: it makes its
data directory with `tempfile`, and the sandbox refuses it. So the command the golden test runs
(`PYTHONHASHSEED=0 python tests/scenario.py <data> <trace> basic|full`) was run with the data
directory inside this folder, twice, and both runs were byte-identical (sha256). The traces were
then copied over `tests/golden/basic.json` and `tests/golden/full.json`. No absolute path of this
machine is in them.

The diff is exactly 315 changed lines in `basic.json` (267213 → 267404 bytes) and 317 in
`full.json` (323912 → 324106 bytes): one line per changed value, no added or removed structure.
Everything that changed is one of these, all read from the person's trust:

- `users/<qq>.json` → `trust`, and `relationship.state` (`trust`, `closeness`, `conflict`,
  `repair`, `predictability`), `relationship.trajectory.*`, `relationship.attachment.*`,
  `relationship.repair_state.evidence.*`;
- `page_status.data.relationships.*` — the same fields per person, and the same trajectory;
- `states/her.json` → `proactive_autonomy.sources.{trust,closeness,closeness_effective}`, which
  read the closest person's record;
- the rest is her own numbers moving in the last digits, through the existing (unchanged) line in
  `_touch_user` that passes the relationship delta to L1:
  `core.integrate_noise('relationship', social=0.004*(closeness-0.5), valence=0.004*(trust-0.5))`.
  With trust frozen at 0.5 that valence term was always 0; now it moves a little, so
  `homeostasis`, `learning…sum_pe`, `reflection`, `ripple`, `spiking`, `proactive_autonomy` and
  memory `importance` differ in the last digits (for example `importance` 0.4636273877543944 →
  0.4636273762957345, `homeostasis.L_int` 0.0214 → 0.0209). Her final `v` and `stress` in the
  trace are unchanged.

Nothing else differs: `routes`, `turns` (prompts included), `provider_prompts`, `log`,
`autonomy_ticks`, `api_config`, the self model, the archives and the phone files are identical.

The final trust in the traces, from 0.5 before: basic — 10001 0.36, 10002 0.486, 10003 0.502,
10004 0.473, 10005 0.506; full — 10001 0.335, 10002 0.518, 10003 0.524, 10004 0.468, 10005 0.5.

`tests.test_golden_standalone` also reads these two files. It needs `aiohttp`, which is not
installed here, so its own comparison was replayed by hand: the three paths
(`scenario_standalone.py --path astrbot|nohistory|standalone`) were run for both modes with a
throwaway `aiohttp` stand-in on `PYTHONPATH` (deleted afterwards), and `test_golden_standalone`'s
own `differences()` / `matches()` and its allowed-path tables were applied to them. No extra path
and no missing path in any of the three comparisons (golden → A: 85 differing paths in basic and
132 in full, all allowed; A → B0: 431; B0 → B: 480), and the log rows still match (24 warnings at
A, none at B0).

## Test runs in this sandbox

One file at a time. The sandbox refuses every file write outside this folder, and on this Windows
Python `tempfile.TMP_MAX` is 2147483647, so a `tempfile.mkdtemp` under the refused OS temp folder
retries practically forever instead of failing. Those files were therefore run with
`tempfile.TMP_MAX` set to 20 first — the same tests, only the refused retry loop is cut short — and
what comes out is the refusal, not an assertion.

- `python -m unittest tests.test_trust_follows_her` — Ran 9 tests, **OK**.
- `tests.test_people_sessions` — Ran 4, 4 errors: every one at `setUp`,
  `tempfile.TemporaryDirectory(dir=test_basics.DATA)`, `FileExistsError: no usable temporary
  directory name` (the sandbox refuses the nested folder). No test body ran.
- `tests.test_body_heart` — Ran 41, 27 errors, all `PermissionError`; the other 14 passed. No
  assertion failed.
- `tests.test_forget_wiring` — Ran 19, 19 errors, all `PermissionError` at `setUp`. No assertion ran.
- `tests.test_forget_registry` — Ran 17, 3 errors (the temporary folder cannot be made or removed:
  `FileNotFoundError` / `PermissionError`); 14 passed.
- `tests.test_stage_replay` — Ran 7, 6 errors (the temporary run folder cannot be made:
  `FileNotFoundError`/`PermissionError`); 1 passed.
- `tests.test_discretion` — Ran 84, 62 errors, all `PermissionError`; 22 passed.
- `tests.test_golden` — Ran 2, 2 errors, both `PermissionError` when the scenario's data folder is
  made. The re-recorded traces are the ones described above.
- `tests.test_golden_standalone` — Ran 6, 4 errors (`PermissionError`), 2 passed.
- `tests.test_basics` — Ran 11, 2 errors (`PermissionError` on the plugin's `states/`), 9 passed —
  including the method count (512).
- `tests.test_owner_name` — Ran 22, 2 errors (`PermissionError` / `FileNotFoundError` on its
  temporary folders), 20 passed. Its `FakeTurn` drives the real `_prepare_turn` with a stand-in
  `_touch_user`; that stand-in now takes `reaction=None` as well (one line in that test file,
  nothing else there). Before that line, the two `ReplyPrompt` tests raised
  `TypeError: FakeTurn._touch_user() got an unexpected keyword argument 'reaction'` — a stand-in
  out of step with the call, not a behaviour of the change.

No assertion failed anywhere. Every error is the sandbox denying a file under the OS temp folder.

## Unsure about

- The re-recorded goldens carry her own numbers in the last digits, through the existing
  `integrate_noise('relationship', …)` line, not only the trust fields. The card asks for "only
  trust and the few things computed from it"; this is trust reaching L1 through a line that was
  already there, and it was left alone. If that ripple is not wanted, the line in `_touch_user`
  would have to change, which is not this card.
- The trust values move with `Δstress` as well as `Δv`, so a happy message that also raises her
  stress a little can end slightly lower. That is the formula the card gives.
- `tests.test_golden_standalone` could not be run for real (no `aiohttp`); it was replayed as
  described above, so its pass is a replay, not a run.
- No file outside the list above was changed, except the one line in `tests/test_owner_name.py`
  that keeps its stand-in `_touch_user` in step with the new keyword; nothing was committed.
