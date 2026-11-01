# Heybox and owner

Add a disabled-by-default, read-only Heybox flow and owner-only proactive messages.
`heybox_enabled`, `heybox_write_enabled`, and `proactive_owner_enabled` default
to false. There are no Heybox write requests. The panel provides POST routes at
`/api/page/heybox/login`, `/api/page/heybox/status`, and `/api/page/heybox/logout`;
the page must render the returned `qr_url` and poll status. Existing panel host,
origin and token checks apply. QR polling runs in Python at three-second intervals
for at most the returned expiry, capped at three minutes. The credential bundle
is held in the existing DPAPI key store and removed on logout.

The read path uses the fixed API host, a ten-second timeout, a 512 KiB response
limit and no redirects. Captcha pauses requests for the day; login failures ask
for a new scan. A failure on the first signed browsing run stops further signed
requests for review; logout clears that review state. The feed supplies at most
20 unseen titles, a model may select up to two, and a second model call forms an
impression and optional owner message. It receives only title, post text and up
to 20 comment texts, not author fields. Seen identifiers expire after seven days;
at most six visits are attempted daily. A wake, the second meal of her
day, and a sleep choice are each tried once per day; the second meal is used as
the lunch approximation so this follows her activities without a fixed clock.
Her own menu can also request a visit. Each model call is charged as `heybox`.

Owner messages use the existing life call, check the owner's unanswered count,
private material, red lines, copied owner rules, budget and sleep; only the
owner's private place is addressed. The old autonomous templates are suppressed
when owner-only mode is enabled. The model identifies used sharing wishes by
their temporary positions, and only successfully used wishes are removed.

The ParseHub signer is copied from commit `0ba8ba5` with its MIT notice. Fixed
vectors were calculated with that signer and checked against an independent
implementation of its actual finite-field operations. The earlier interface
notes incorrectly described these operations as standard AES InvMixColumns;
the source is authoritative. The locally generated device token follows the
provided shape, but the remote service's acceptance of it, the signing constants,
and the response formats have not been tested against the real service. The
first real run should be reviewed using only interface names and status fields.

Tests are offline and use fake accounts, responses and an in-memory key store.
The full suite and standalone golden were not run as instructed; the separate
AstrBot-specific work was omitted under the 11-01 instruction. The panel pages
were not changed.
