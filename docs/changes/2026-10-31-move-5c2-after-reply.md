# Move 5c-2: reply handling

Move the post-model reply into `TurnMixin._after_reply` so AstrBot and a neutral turn can use the same path. The AstrBot hook wraps its response; the neutral caller supplies a `TurnReply`. The send check, attention and browser accounting use the handle at the points that touch the response. Handle detection uses known types so mocks are wrapped as responses.

The AstrBot adapter retains the previous text, chain and usage behavior. The existing switches and defaults are unchanged. No files outside the card's scope were changed. The golden files were not updated.

The moved body was compared with `92febba` using Git's moved-line comparison; its remaining differences match the card's replacements. The four integration changes were checked against the baseline diff.

## Test results

Each module ran separately in the sandbox:

```text
tests.test_after_reply: Ran 6 tests in 1.192s | OK
tests.test_reply_handle: Ran 10 tests in 0.002s | OK
tests.test_golden: Ran 2 tests in 3.572s | OK
tests.test_send_check: Ran 23 tests in 7.872s | OK
tests.test_selfie: Ran 46 tests in 1.876s | OK
tests.test_stickers: Ran 22 tests in 2.791s | OK
tests.test_stickers_wire: Ran 29 tests in 9.055s | OK
tests.test_attention: Ran 38 tests in 5.287s | OK
tests.test_browse: Ran 20 tests in 0.013s | OK
tests.test_browse_wire: Ran 20 tests in 2.229s | OK
tests.test_discretion: Ran 84 tests in 30.179s | OK
tests.test_slang: Ran 14 tests in 0.292s | OK
tests.test_messenger: Ran 25 tests in 0.076s | OK
tests.test_ports: Ran 7 tests in 0.003s | OK
tests.test_turn: Ran 10 tests in 0.001s | OK
tests.test_basics: Ran 11 tests in 0.040s | OK
```

Outside the sandbox the same 16 modules pass one at a time with `venv-ams-life`, and the golden
files are unchanged. A script took `main.py` 730-886 at `92febba`, applied the card's table and
compared it with the body of `_after_reply`: all 145 lines are the same. Every global name the
moved body uses is defined in `mixin_turn`.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
