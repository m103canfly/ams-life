# Outbound checks and web memory

Outbound searches, addresses and typed text use the current turn's send checks
regardless of the global memory switch. A trip also uses the names wall.

Web memories retain the chat origin for a link supplied in that chat. Pages
found by her own search or trip have a self origin. Existing memories are not
rewritten. Pages read in a reply are kept after the send check even if the
reply is held. A private now state is generalized outside its own chat.

The read-only browser disables Chromium hostname resolution and fetches routed
requests through checked addresses. Each redirect is checked separately. The
DeepSeek remote fetch resolves and connects on DeepSeek's own machines and is
outside this change. Interactive browsing is outside this change. HTTP proxies
are supported; other proxy schemes currently fail closed and need follow-up.

The older browse tests' origin and forgetting assertions now reflect the new
origin rules. AstrBot-specific behavior is not maintained under the owner's
November 1 instruction.

Validation is recorded in the final work report. The full suite was not run.
