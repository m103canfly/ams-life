# Heybox research report (2026-11-01)

## Evidence and scope

The requested upstream repository is not available in this worktree. Network
access is prohibited for this task, so its source, license and current service
behavior could not be inspected. The card identifies `huandu/heybox-url` as MIT;
that attribution is an unverified input, not an independently checked license.
No implementation decision should rely on the unknowns below.

At commit `1f30495`, a repository search outside `pages/` found no `heybox`,
`小黑盒`, `huandu`, or `xiaoheihe` references. `life_loop.py`, named in the
second-step outline, is absent. The requested 1c and 1h prerequisites therefore
cannot be established from that filename or the old card numbers alone.

## Upstream questions for review

1. Request construction, endpoint paths, parameter names, signatures,
   timestamps, device identifiers, and source locations: unknown. Anonymous
   access to the home feed, popular feed, category lists, and full post bodies
   is unverified. Do not implement login-dependent requests.
2. Reusable code, its dependencies, and whether it can be copied intact: unknown.
   Review the actual source and dependency manifests before proposing a port;
   any new package requires the owner's approval.
3. Response fields and their names: unknown. The proposed minimum is post ID,
   title, and text; image URLs only if required by the reviewed design. Do not
   retain author nicknames. Verify that these fields are actually available
   without login before specifying storage or prompts.
4. Published limits, enforcement, and blocking risk: unknown. Three or four
   daily feed reads cannot be assumed sufficient or safe; selecting up to two
   posts also adds requests. Verify current service terms and limits, account
   for retries and failures, and agree a conservative request budget.
5. License: inspect the upstream license and copyright notices first. If the
   copied material is confirmed MIT, preserve its copyright and permission
   notice in `NOTICE.md` as required by that license. The exact attribution and
   text cannot be supplied without the source; this step does not edit NOTICE.

## Local observations and implications

`mixin_autonomy.py:56`, `:89`, `:132`, and `:281` contain the template, gate,
send, and tick described by the card. The tick iterates remembered private
sessions, rather than selecting the owner; registration retains at most 20 and
the tick skips entries older than one day. The gate uses a deterministic template
and has no spend check. `_conf_schema.json:77` and `:83` describe the two
default-off switches and the existing quiet time, cooldown, and daily cap.
Changing this behavior is outside the first step.

The local search found no `share_wishes` reference outside `pages/` and golden
fixtures, so its stated expiration and usage cannot be confirmed here. No
unanswered-owner count was found by the searched terms; this is not proof that
no equivalent mechanism exists under another name.

`weather.py:17` and `:24` provide a local example of a 64 KiB response limit,
five-second timeout, and disabled redirects. This does not establish suitable
limits or URL validation for the unknown upstream API. A fixed destination,
redirect handling, response bounds, data minimization, spend accounting and
owner-only sending still need review in the later implementation card.

## Validation

This step changes documentation only; no code, tests, switches, or golden files
are intentionally changed. Upstream verification and the second-step design
remain blocked on an available source and review.
