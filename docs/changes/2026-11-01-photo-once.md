# Photo once

Overlapping turns could queue two photos at the same place and repeat the reply as a caption.
Track an in-progress photo per place, expire stale reservations, and release only the matching
reservation when preparation or sending ends. Drop captions already contained in the sent reply
after removing whitespace and punctuation. Log photo delivery and bounded failure reasons
without photo descriptions or captions.

The existing photo switch is unchanged. Voice and screenshots are unchanged. No plugin methods
were added. The selfie test double supplies the existing event-local send-check note interface.

Offline tests passed: photo_once (4), photo_wait (6), selfie (46), selfie_ports (10),
turn_tools (10), golden (2), and basics (11). The full suite was not run as instructed;
golden_standalone is reserved for the external run. No golden files were changed.
