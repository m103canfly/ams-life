# 2026-10-31 move-5es: hearing a voice through QQ's own speech-to-text

Before the switch, seeing pictures and hearing voices have to work without AstrBot (the owner,
10-31). Hearing a voice uses AstrBot's speech-to-text provider; the new program has no AstrBot,
so the voice is asked of QQ itself.

## What changed

- `messenger.py`: `ALLOWED_ACTIONS` gains `fetch_ptt_text`. It only reads: the words of one
  voice, found by `message_id`. `OneBotMessenger.call` passes it through with no other change.
- `mixin_media.py` (`_voice_context`): the switch and the AstrBot provider are tried as before.
  When a provider answers, the old body runs unchanged. When there is no provider (the method is
  missing, asking fails, or it answers `None`) and the message has a record segment, the
  message's id goes to `fetch_ptt_text` through the messenger, and the words are taken from the
  answer: a string as it is; a dict by `text`, then `content`, then `result`. The words are
  stripped and cut to 300 characters as before (600 for the whole sentence). No words, no
  message id, or any error (including `ActionFailed`) gives "" and one warning that names only
  the error kind; nothing is raised. A message with no voice is not asked about.
- `tests/fake_napcat.py`: `FakeNapCat` answers `fetch_ptt_text` with made-up words
  (`PTT_TEXT`), data `{"text": ...}`, which is NapCat's own shape for this action.
- `tests/test_voice_text.py`: a new test file. `WithAstrBot` keeps the old `_voice_context` from
  `d20f2fa` beside the new one and compares their words, with QQ never asked. `WithoutAstrBot`
  has no provider (a `None`, a missing method, a failing one) and checks one `fetch_ptt_text`
  call with this message's id. `TheWords` takes a string answer and a dict one. `NothingHeard`
  covers an empty answer and a failing call (no words, nothing raised). `NoVoiceToHear` covers
  no voice, the switch off, and no message id (nothing is called). `ThroughTheFakeNapCat` and
  `OverTheServer` run `fetch_ptt_text` through `OneBotMessenger` and the fake NapCat; the
  socket one is skipped without aiohttp.

## NapCat's shape

`fetch_ptt_text` takes `{"message_id": ...}` and answers with one string field, `text`: the
data is `{"text": "..."}`. The fake uses that shape and made-up words ("明天几点出门"). The real
effect is tried once on the moving day with a real voice.

## Why nothing else changes

On AstrBot the provider is there, so the old words and the old path are untouched and the golden
traces do not change (no scenario has a voice). No plugin method is added: `_voice_context` is
changed, not added, and the count in `tests/test_basics.py` stays 504. No new dependency, switch,
default, data file or service is touched. Only the files on the card were changed.

## Tests

Tests: run by the dispatcher outside the sandbox (dsh's sandbox cannot write temporary
folders), one file at a time with `venv-ams-life`: `tests.test_voice_text` (12, the server one
too), `test_basics`, `test_golden` (unchanged), `test_messenger`, `test_onebot_messenger`,
`test_fakes`, `test_model_ports_vision`, `test_lookup_ports`, and `test_segment_readers` (it
holds an old copy of `_voice_context`) all pass. The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).

In the sandbox: `test_voice_text` 12 tests OK (1 skipped, no aiohttp); `test_messenger` 25 OK;
`test_fakes` 15 OK (5 skipped, no aiohttp); `test_model_ports_vision` 4 OK; `test_lookup_ports`
5 OK. `test_basics`, `test_golden` and the file tests of `test_onebot_messenger` stop at writing
a temporary folder (`PermissionError`), as the dispatcher warned; `test_basics`' method count
test passes at 504 before that, and `test_onebot_messenger`'s action tests pass.
