# 2026-11-01 send roots

Local media sends now read only the selfie and browser screenshot folders. Raw OneBot send
actions accept only text, face and base64 media segments. These restrictions prevent other
data files from being sent; ordinary media sends keep their existing format.

No switch was added. The existing OneBot messenger tests provide valid messages for send
actions and check that missing messages are refused. The full suite and standalone golden
test are left to the owner as requested.

Checks: `test_send_roots` (4), `test_onebot_messenger` (41), `test_send_neutral` (6),
`test_app` (16, 10 skipped), `test_golden` (2), and `test_basics` (11) passed.

## 2026-11-01 security follow-up

OneBot URL images are refused. Base64 images must decode to a recognized image within the
sticker size limit, including raw send actions. Vision reads local files only from the selfie,
browser screenshots and sticker image folders. A quoted message is used only when its source
matches the current group or private chat. URL image tests now expect refusal; new offline tests
cover image validation, local vision paths and quote isolation.

The owner authorized replacing the old OneBot tests' non-image base64 fixture with a PNG
signature and moving the vision tests' local files into a temporary screenshot folder. Their
assertions are unchanged. The first runs exposed these fixture conflicts; both passed after
the fixture updates.

Follow-up checks passed: `test_send_roots` (7), `test_onebot_messenger` (41),
`test_send_neutral` (6), `test_vision_neutral` (8), `test_vision_channel` (14),
`test_app` (16, 10 skipped), `test_golden` (2), and `test_basics` (11).
