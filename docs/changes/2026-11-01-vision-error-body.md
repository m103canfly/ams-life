# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.

# Vision HTTP error body

Vision provider errors previously logged only the HTTP status, hiding the reason
for a rejection. The image API now reads up to 4096 response bytes, decodes UTF-8
with replacement, flattens line breaks and tabs, trims whitespace, and logs at
most 200 characters. A complete configured key in that excerpt is replaced with
`***`. Empty or unreadable bodies retain the status-only warning. The exception
remains `vision request failed`; the request body is not logged.

The key is replaced before the excerpt is cut, so no piece of a key is left at
the 200-character boundary. Provider responses can still contain other text.
There is no new switch or plugin method. No files outside the card were changed.
The full suite is deferred. Sandbox checks passed: error body 5, neutral 8,
channel 14, golden 2, and basics 11. Golden standalone requires aiohttp and is
reserved for the external run.
