# Photo once

Overlapping turns could queue two photos at the same place and repeat the reply as a caption.
Track an in-progress photo per place, expire stale reservations, and release only the matching
reservation when preparation or sending ends. Drop captions already contained in the sent reply
after removing whitespace and punctuation. Log photo delivery and bounded failure reasons
without photo descriptions or captions.

The voice tool now tells the model not to repeat the spoken meaning in text. On the neutral turn
route, compare each reply piece with the queued voice, dropping matching pieces while retaining
the voice and unrelated text. Compare normalized containment first, then local embedding cosine,
then character-bigram Jaccard when embeddings are unavailable. Embeddings are only requested
when the configured service hostname is localhost, 127.0.0.1, or ::1; otherwise use bigrams.
The AstrBot-specific route and its additional test were excluded by request.

The existing photo and voice switches are unchanged. Screenshots are unchanged. No plugin methods
were added. The selfie test double supplies the existing event-local send-check note interface,
and its voice tool assertion expects the new instruction.

Offline tests passed: photo_once (4), photo_wait (6), selfie (46), selfie_ports (10),
turn_tools (10), voice_once (7), voice_tone (6), send_neutral (6), golden (2), and basics (11).
The full suite was not run as instructed;
golden_standalone is reserved for the external run. No golden files were changed.
