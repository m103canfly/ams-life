# Standalone LLM settings from the panel

The standalone app uses the panel's custom LLM model and address when both are
present and the address passes the existing DeepSeek URL check. Otherwise it
uses the command-line model and default address. A rejected address is not logged.
The DeepSeek key still comes from the key store. Changes to the panel settings
take effect after restarting the standalone app.

Standalone LLM model listing checks the address before reading the key or making
a request. It uses the stored key, ignores the page key, and does not follow
redirects. AstrBot and other model listing kinds retain their existing behavior.
The URL check was extracted without changing the DeepSeek client's acceptance
rules. There is no new switch. Changes are limited to the files on the card.

The full suite is deferred to the combined acceptance round. The standalone
golden test is to be run outside the sandbox.

Sandbox validation: panel LLM 10 passed; app 16 ran with 10 skipped; panel API
20 ran with 17 skipped; DeepSeek client 9 ran with 1 skipped; golden 2 passed;
basics 11 passed. Skipped tests require dependencies unavailable in the sandbox.
