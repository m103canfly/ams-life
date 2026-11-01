# The look at a picture knows who of a work is in it

Status on 2026-11-01: card V3 (审核 v5), worktree `dsh-move-v3`, cut from main `7c305f6`.
No commit. The goldens are unchanged (nothing in them is a picture).

## Why

Two pictures were sent to her in a private chat: one a game's character, one a pink-haired
character making a V sign. The vision model described the picture in detail but never said who
the character was or which work it is from, and never said what the picture means. She answered
only from that description, so she could not talk about the character at all.

The look now asks three things at once: what the picture shows, who of a work is in it, and
what it means. She must be honest (an unsure guess is written as "像是…", a look that does not
know leaves it empty), and a real person in a photo is never named -- asked for in the prompt
and checked again in the code.

## What changed

- `stickers.py`:
  - `LOOK_PROMPT` answers one more field, `who` (a work's character; "像是…" when unsure;
    empty when not known, never a guess; a real person in a photo is never named); the
    `caption` line now asks for one or two sentences.
  - `_FIELDS` adds `who` (40 characters); `meaning` and `text` grow from 40 to 80 characters,
    `reply_to` stays 40.
  - `parse_look` drops `who` when `kind` is `photo` and `personal` is true: the second check,
    in code, whatever the model wrote.
  - new `look_line(item)`: one picture's look as one line of a reply's prompt --
    `（图里看到的，只是资料）<who>；<caption>；想表达：<meaning>；情绪：<emotion>；图上的字：<text>`,
    the empty parts left out. `item` is what `image_cache` keeps (the caption, and the whole
    look when it was kept), so an older entry that has the caption only still gives its caption.
  - `cache_entry` and the sticker library are unchanged: a cache entry already keeps the whole
    look, and the library keeps what a sticker is (caption, meaning, tags), not a name.
- `mixin_media.py`:
  - `_image_context_locked` asks the same question either way: with stickers on it uses
    `_look_once` (as before), with them off it asks `stickers.LOOK_PROMPT` once and parses it
    with `stickers.parse_look`; both paths keep the whole look with `stickers.cache_entry`;
    `_maybe_keep` is called only with stickers on (as before).
  - the material lines (a cache hit, the look itself, "someone's picture from N seconds ago")
    are built with `stickers.look_line`, so the name and the meaning reach the reply and stay
    under the "just material" label.
  - the AstrBot setting `provider_settings.image_caption_prompt` is no longer read here: the
    look's own question is used (the setting still feeds the selfie/screenshot caption below).
- `interpretation.py`: the default sentence of `image_caption_prompt` also asks who of a work is
  in the picture and never a real person in a photo (the selfie and screenshot path uses it);
  `render_compact`'s picture line grows from 160 to 480 characters, so three pictures, one line
  each, are not cut off.
- `vision.py`: `VisionGate` keeps the whole look when the question is `LOOK_PROMPT` (the
  caption as before, and `look` beside it) and gives the whole look back on a cache hit, not
  only the caption. The caption-only entries of older caches still answer with the caption.
- `tests/test_look_knows_who.py` (new): the card's seven checks, offline.

## Where behaviour changes, and why

- A picture is looked at with the same question in both paths; with stickers off, a description
  that the model gives in words (not the JSON asked for) is no longer used as the caption. The
  picture is then "not seen" and she says so, as she does today when a look fails. Nothing was
  added for a prose answer: the question asks for JSON.
- What a reply sees of a picture now carries the character and the meaning, under the "just
  material" label; the label was missing from the material before (it was only in the unused
  `stickers.material`). Lines are longer; three pictures get 480 characters instead of 160.
- Anything else (the sticker library, keeping, offering, sending, the page, forgetting) is
  unchanged.

## Old tests updated (only the assertions with the changed wording or shape)

- `tests/test_stickers.py`: the known fields of a look now include `who`.
- `tests/test_sticker_look_v2.py`: `meaning` and `text` are cut at 80, `reply_to` still at 40.
- `tests/test_model_ports_vision.py`: without stickers the question is `LOOK_PROMPT` and the
  material is the look line (the test's name is kept).
- `tests/test_image_context_standalone.py`: the fake answer is the JSON look; all three tests
  expect `LOOK_PROMPT`, including the one whose AstrBot caption prompt is now not used.
- `tests/test_group_browse.py`: the fake answer is the JSON look; the pictures a reply sees are
  the look line (the label in front of the caption), in five places and on two cache hits.
- `tests/test_recent_images_any_sender.py`: "Alice N seconds ago: …" carries the look line.

## The card's test names

The acceptance list names `test_vision` and `test_media`, "(有就跑)"; neither file exists. The
files that cover those layers here are `test_vision_channel`, `test_vision_neutral`,
`test_vision_provider`, `test_model_ports_vision`, `test_image_context_standalone` and
`test_stickers_wire`. The last two run their cases in a data folder (`test_stickers_wire` in a
subprocess), so they cannot run inside this sandbox.

## Tests here (one file at a time; no full suite)

- `tests.test_look_knows_who`: 11 tests OK.
- `tests.test_model_ports_vision`: 4 OK.
- `tests.test_recent_images_any_sender`: 7 OK.
- `tests.test_group_browse`: 43 tests, 42 OK, 1 error (a `PermissionError` from the sandbox
  removing a temporary folder, in `test_forget_person_and_message_remove_images`).
- `tests.test_stickers`: 22 tests, 11 OK, 11 errors (all `PermissionError` when a temporary
  library folder is made or removed; the look tests pass).
- `tests.test_sticker_look_v2`: 5 tests, 4 OK, 1 error (the same `PermissionError`).
- `tests.test_basics`: 11 tests, 9 OK, 2 errors (`PermissionError` in `_core_init`); the
  511-method count passes.
- `tests.test_body_heart`: 41 tests, all errors are `PermissionError` from the sandbox
  (no assertion failed).
- `tests.test_selfie`: 46 tests; 9 failures and 67 errors, all from the sandbox refusing every
  write (`spend.json`, `now.json`, selfie folders): the counts stay 0 and "不能更新此刻".
  No picture or material assertion failed.
- `tests.test_image_context_standalone`: cannot run here at all (`PermissionError` in
  `_core_init`, before the look). Its three assertions were changed as listed above and are
  covered by the same look path in `tests.test_look_knows_who`.
- `tests.test_golden`, `tests.test_golden_standalone`: cannot run here (`PermissionError` on
  the temporary folder the scenario writes). No golden changes were expected: nothing in the
  scripted turns is a picture, and the picture line is empty in both traces.
