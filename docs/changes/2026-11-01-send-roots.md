# 2026-11-01 send roots

Local media sends now read only the selfie and browser screenshot folders. Raw OneBot send
actions accept only text, face and base64 media segments. Image URLs pass the existing public
URL check and require every resolved address to be public. Unresolved names are refused.
These restrictions prevent other data files and local addresses from being sent; ordinary
media sends keep their existing format.

No switch was added. The existing OneBot messenger tests now use a fake resolver, provide
valid messages for send actions, and check that missing messages are refused. The full suite
and standalone golden test are left to the owner as requested.

Checks: `test_send_roots` (4), `test_onebot_messenger` (41), `test_send_neutral` (6),
`test_app` (16, 10 skipped), `test_golden` (2), and `test_basics` (11) passed.
