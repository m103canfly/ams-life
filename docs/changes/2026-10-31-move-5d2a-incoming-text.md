# 2026-10-31 move 5d-2a: incoming text

`Incoming` carries the platform's words so message readers also accept `TurnEvent`.
The AstrBot adapter reads `message_str` afresh and returns empty text when unreadable.
The OneBot adapter joins text, mentions and markdown using the AstrBot 4.29.3 rules.
The 12 reads in the card's table now use `incoming_of(event).text` (the card's 13 counts
`mixin_attention.py` 367 too, which stays for 5d-3); segment reads remain for 5d-2c.
No setting was added, the method count stays 499, and golden files were not changed.
Only the card's files were changed: `events.py`, both adapters, `main.py`, the attention,
browse, events, phone, slang and turn mixins, the named adapter test, the new incoming
text test and this note.

For readable AstrBot events the words match the old read, including wake-check changes.
The OneBot path does not remove a leading wake prefix such as `/`, while AstrBot does.
AstrBot can drop an @ when its private-chat group-member lookup fails; OneBot keeps it.
These differences matter during shadow runs and are outside this card.

## Tests

Each module ran separately in the sandbox:

```text
tests.test_incoming_text: Ran 4 tests in 0.001s | OK
tests.test_adapter_astrbot: Ran 17 tests in 0.101s | OK
tests.test_adapter_onebot: Ran 34 tests in 0.002s | OK
tests.test_turn_event: Ran 5 tests in 0.003s | OK
tests.test_golden: Ran 2 tests in 3.549s | OK
tests.test_basics: Ran 11 tests in 0.040s | OK
tests.test_attention: Ran 38 tests in 5.232s | OK
tests.test_mood_events: Ran 26 tests in 0.072s | OK
tests.test_browse_wire: Ran 20 tests in 2.255s | OK
tests.test_digest: Ran 27 tests in 3.725s | OK
tests.test_slang: Ran 14 tests in 0.273s | OK
tests.test_prepare_turn: Ran 5 tests in 0.054s | OK
tests.test_discretion: Ran 84 tests in 30.052s | OK
tests.test_message_admission: Ran 12 tests in 0.080s | OK
```

Outside the sandbox the 14 modules pass one at a time with `venv-ams-life`, and the golden
files are unchanged. A script took each of the seven files at `2255b7f`, replaced only the
`message_str` read on the 12 lines and compared it with the new file: apart from the new
import lines, all are the same; `mixin_attention.py` 367 and `mixin_browse.py` 338 are as
they were.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
