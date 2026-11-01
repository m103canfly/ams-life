# Offline jailbreak boundaries

Add adversarial tool calls through `turn_runner.run_turn` with a scripted model and an
in-memory OneBot API. The tests cover local and nonstandard-port reads, an added query
string (T13), a URL in an image caption (T08), an unseen screenshot, a file segment and
invented upload tool, allowed outgoing actions and segments, a forged forward (T09),
and native JSON and XML cards (T11). Browser, DNS, screenshot and image dependencies
are replaced with offline stand-ins. Browsing and screenshots are enabled in the tests.
The tests add no production behavior or switches and leave the golden files unchanged.

Persona and memory disclosure, page instructions, `allowed/common` guessing, T01–T05,
T12 and T14–T19 remain for a separately authorized paid model replay. Other future
boundary cases belong to their respective cards.

Validation: `test_jailbreak_boundaries` passed (7 tests), `test_golden` passed (2 tests),
and `test_basics` passed (11 tests). The full suite was not run as instructed;
`test_golden_standalone` is reserved for the owner's outside run.
