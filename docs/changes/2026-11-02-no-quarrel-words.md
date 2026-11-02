# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.

# 2026-11-02 no quarrel words in the score

In a group where nobody called her, the score used to look the words up in the
emotion lexicon. A hit that lowered `v` by more than 0.15 and raised `a` by more
than 0.05 (a fight between the others) took 0.20 off the score, so she was asked
less while people were quarrelling. That is a keyword rule, and the owner does
not want it. The words are not a reliable sign of what a stretch is about.

## What changed

- `attention.py`: `score` takes four numbers now: `topic`, `known`,
  `her_recent`, `quiet_minutes`. The `quarrel` argument and its 0.20 are gone,
  and the module docstring no longer lists a quarrel among the things the score
  weighs.
- `mixin_attention.py`, only `_score`: it no longer calls `_lexicon_deltas` and
  calls `attention.score(topic, known, her, quiet)`. Nothing else in the plugin
  changed.
- `_conf_schema.json`, only the hint of `reply_other_groups_when_called`: it now
  says that with the switch on, a call of her in a group outside the list shows
  her the message and she decides herself whether to answer (she may say
  nothing); without a call she only looks and does not speak. The old line
  about "只在测试群和主人私聊开口" was out of date and is dropped. The default
  stays off; the owner sets it on the panel.

## Where the behavior differs

During a quarrel in a group where nobody called her, she is no longer asked
one time less: the same stretch scores the same with or without the words. The
level thresholds, the safety nets, the called cases, and the night are
unchanged.

## Not here

- `body.py`'s `mood_kinds` still has its own `quarrel` (a mood event, from
  `MOOD_QUARREL_WORDS`). It is a different rule and is left for later.
- "她瞄一眼" (looking at the groups she is in) is G1b.

## Tests

- `tests/attention_cases.py`: the new `no_quarrel` case scores one message with
  the words and one without in the same stretch, with the same embedding.
  `tests/test_attention.py` asserts the two scores are equal, and that
  `attention.score` refuses the old fifth argument.
- The old score tests (topic, people she knows, her recent lines, quiet here)
  are kept and pass. No `quarrel=` call is left.
- In the work sandbox Python cannot write files, so the plugin-level cases that
  need a data directory stopped with `PermissionError`; the pure-function tests
  of `test_attention` pass (21). `test_message_admission` stopped in its setup
  for the same reason. The other acceptance files (`test_turn_event`,
  `test_golden`, `test_golden_standalone`) were not run; they are to run outside
  the sandbox.
- The golden files were not changed.
