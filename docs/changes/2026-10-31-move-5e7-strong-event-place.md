# Move 5e-7: strong-event cooldown by place

The strong-event summary hook used the AstrBot session string as its in-memory cooldown key. Neutral turns leave that string empty, so a summary in one place suppressed another place for 600 seconds.

The hook now uses `self._here(event)`, which obtains the neutral place through `adapter_astrbot_turn.incoming_of`. AstrBot group and private sessions continue to have separate cooldowns by place. Session strings that map to the same place now share a cooldown. The cooldown duration and the summary path are unchanged; there is no new switch or persisted data.

The new offline tests exercise neutral and AstrBot events, the cooldown interval, and the source boundary. No other plugin code, old tests, or golden files were changed.

## Tests

- `tests.test_strong_event_place`: Ran 4 tests in 0.016s | OK
- `tests.test_golden`: Ran 2 tests in 4.734s | OK
- `tests.test_basics`: Ran 11 tests in 0.054s | OK; the expected method count remains 505.
- `tests.test_turn_runner`: Ran 9 tests in 6.531s | OK
- `tests.test_after_reply`: Ran 6 tests in 1.577s | OK
- `tests.test_attention`: Ran 38 tests in 6.698s | OK
- `tests.test_brain_data`: Ran 27 tests in 12.998s | OK
- `tests.test_browse_wire`: Ran 20 tests in 2.989s | OK
- `tests.test_digest`: Ran 27 tests in 4.923s | OK
- `tests.test_discretion`: Ran 84 tests in 39.957s | OK
- `tests.test_forget_wiring`: Ran 19 tests in 10.149s | OK
- `tests.test_impressions_wiring`: Ran 17 tests in 4.444s | OK
- `tests.test_ignore_senders`: Ran 5 tests in 1.130s | OK
- `tests.test_no_numbers`: Ran 15 tests in 5.632s | OK
- `tests.test_reply_tools`: Ran 6 tests in 1.934s | OK
- `tests.test_send_check`: Ran 23 tests in 10.545s | OK
- `tests.test_stickers_wire`: Ran 29 tests in 12.408s | OK
- `tests.test_reply_provenance`: Ran 7 tests in 0.077s | OK
- `tests.test_selfie`: Ran 46 tests in 2.096s | OK
- `tests.test_body_heart`: Ran 41 tests in 10.187s | OK

The additional old files exercise the request hook directly or through their offline case scripts. Tests that replace `_prepare_turn` with a stub do not reach this hook.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).

## Session-string audit

The 23 occurrences below are the pre-change matches in plugin Python files, excluding AstrBot adapters, `main.py`, and tests. Some construct or declare a field rather than read it. After this change 22 remain.

- `common.py:729`: AstrBot stand-in stores the session for sending.
- `common.py:744`: AstrBot stand-in sends through the AstrBot context.
- `mixin_attention.py:386`: AstrBot conversation lookup; neutral turns use their own runner.
- `mixin_attention.py:461`: Split replies fall back to the neutral place when the session is empty.
- `mixin_autonomy.py:28`: The AstrBot group guard is followed by the neutral incoming privacy check.
- `mixin_autonomy.py:169`: Still used as a key for autonomous private sessions; empty neutral sessions are not registered, so autonomous ticks miss them when enabled.
- `mixin_browse.py:621`: AstrBot tool stand-in supplies a trip session.
- `mixin_events.py:189`: Stand-in passes a stored place or session to core lookup; the adapter accepts both forms.
- `mixin_events.py:2436`: Cooldown key fixed by this card to use the place.
- `mixin_group_browse.py:18`: Group-event stand-in constructs an AstrBot-shaped session from a place.
- `mixin_llm.py:82`: AstrBot persona manager lookup; the neutral persona path precedes it.
- `mixin_llm.py:147`: AstrBot provider lookup; the neutral model path precedes it.
- `mixin_llm.py:704`: AstrBot vision provider fallback; the neutral model path precedes it.
- `mixin_media.py:271`: AstrBot speech-to-text provider lookup; absence falls back to received text.
- `mixin_pages.py:629`: Memory consolidation stand-in carries a library place, accepted by the adapter.
- `mixin_pages.py:648`: Working-set stand-in carries a place, accepted by the adapter.
- `mixin_pages.py:896`: Insight stand-in carries a core key, accepted by the adapter.
- `mixin_phone.py:394`: Saves an AstrBot session for deletion in AstrBot; neutral storage is keyed by place.
- `mixin_ports.py:30`: AstrBot session lookup for a given place; neutral messenger uses the place directly.
- `mixin_ports.py:46`: AstrBot messenger event-send routing; neutral messenger returns earlier.
- `mixin_send_check.py:131`: AstrBot provider fallback; neutral model is selected first.
- `mixin_stickers.py:240`: Passes the session along with the place; sticker sending uses the place.
- `turn.py:18`: Declares the optional AstrBot session field; neutral turns leave it empty.
