# 2026-10-31 move-1e: port entry points and split replies

The plugin needs one place to obtain its ports as AstrBot calls move behind interfaces.
`mixin_ports.py` provides `_messenger(event)`, `_model(provider)`, and `_incoming(event)`;
`_umo_of(place, event)` resolves the current event's session or the saved window session.
Each call creates a fresh adapter. No new switch or dependency is added.

`main.py` adds `PortsMixin`. `mixin_attention.py` sends the second and later parts of a reply
through `Messenger.send`. The adapter builds the same text and face components and uses the
same session for the current event; pauses, sent notes, stickers and error handling stay in place.
The first part still uses the existing AstrBot reply flow.

`tests/test_ports.py` checks the entry points, component equivalence and send failures.
`tests/test_basics.py` updates the inherited method count. No other files are changed.

README module line: `mixin_ports.py` | Plugin entry points for the AstrBot port adapters.

Full suite: 1038 tests OK (main a85d118 had 1031; +7 in `tests/test_ports.py`). Golden traces unchanged.
