# 2026-10-31 move-5e4b: the new program keeps each turn in her own history

On AstrBot the conversation history is AstrBot's own: at the end of a turn its
`_save_to_history` writes that turn's messages, leaving out the system prompt and every part
marked `_no_save`, and before that the plugin's `_settle_history` (`mixin_send_check` 203 at
ec39fd7) replaces her last message with the words actually sent, without the model's thinking.
A stopped event (she chose to say nothing, or the look before sending held the reply back) sends
nothing and saves nothing. The new program has no AstrBot, so move 1d's `HistoryStore` had no
writer. This card adds the one method the new program (5e-5) calls after each turn is sent.

## What changed

`mixin_turn.TurnMixin._keep_turn(event, turn_request, reply)`:

* it returns at once when there is no store (`_history_store`, move 5f) or when the event was
  stopped;
* her line is `_check_note(event).get("sent")` when the send check set it (the pieces and the
  sticker after them are already in it), else `reply.text`; nothing is written when that is
  empty;
* the person's line stores `turn_request.prompt`: the message as the plugin gave it to the
  model, labels and all, which is the shape `_prepare_turn` reads back through
  `_history_original`; the request-only blocks marked `_no_save` (the now line, the body, the
  recalled memories) were never part of it;
* the place is `_here(event)`; `adapter_astrbot_turn.incoming_of(event)` gives the sender id,
  sender name and message id; `_source_ids(event)` gives what forgetting by message looks for;
* her line carries `about=(sender_id,)` and the same sources, so forgetting a person or a
  message also deletes her answer;
* the store's `gate` (`_history_gate`, move 5f) is asked before any line is written, like every
  other write;
* a failure is logged as a warning with the error's type only and is not raised: the reply has
  already been sent.

## Difference from AstrBot

* AstrBot also saves this turn's tool calls and tool results; the new program does not keep
  them.
* The new program keeps only these two lines per turn.

## Behavior

Unchanged on AstrBot: nothing there calls `_keep_turn` (`main.py` does not mention it and
`_after_reply` does not call it), and without a `_history` the method stops before writing
anything. No golden trace moves and nothing is wired in yet. One plugin method is added, so the
method count in `tests/test_basics.py` goes from 504 to 505, with the comment
`# move 5e-4b: +1 (_keep_turn)` above the line; nothing else changes there.

## Tests

Tests: run by the dispatcher outside the sandbox (dsh's sandbox cannot write temporary
folders), one file at a time with `venv-ams-life`: `tests.test_keep_turn` (8), `test_basics`
(505), `test_golden` (unchanged), `test_history_store`, `test_forget_history`, `test_her`,
`test_message_steps` and `test_after_reply` all pass. The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).

`tests/test_keep_turn.py` (new, eight tests) covers a normal turn (both lines, the person's
`sender_id` and `message_id`, her sent words, and `recent()` in order), her line from
`reply.text` when there is no `sent`, a stopped event, empty words, someone in the forget
registry (the gate blocks both lines), no store, a failing `store.append` (one warning, no
raise), and the source (`_keep_turn` is not called in `main.py` or in `_after_reply`). The
three spot checks stay for the last round: A, writing even when stopped, must fail test 3;
B, her line without `about`, must fail test 5; C, using `reply.text` instead of `sent`, must
fail test 1.

In the sandbox here Python could not write temporary files (PermissionError at the test's own
temporary folder), so the test file was not run inside it; the dispatcher runs it outside.
