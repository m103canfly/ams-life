# Impression storage and reply paths

Read-only investigation, 2026-11-01, at `bcd3bbd` (which includes 3a-1).
No code or behavior was changed. The second-stage design is pending review.

## Facts

- Group cards: `impressions.py:382` and `:390` store one `people` map per
  group in `people/<sanitized-place>-<hash>.json`. A record holds `name`,
  `aliases`, `style`, `topics`, `stats`, dates and `origin`; `names.json`
  separately retains aliases. `mixin_impressions.py:222` reads each group
  window for the nightly job. `impressions.py:529` excludes group-private
  text from model input and text-derived statistics, checks the forget
  registry, and saves the card. Imports can also populate cards
  (`impressions.py:630`).
- Group cards in replies: `mixin_impressions.py:90` selects the speaker and
  recent participants, then `impressions.py:593` selects a view. The same
  group gets the full descriptive card; another group gets names and aliases
  only when the person is present; the person's own private chat gets style
  and names, with topics limited to those mentioned in that private window.
  A card marked private is blocked outside its source group. The result enters
  `render_compact` through `people` (`mixin_turn.py:320`).
- Person record: `mixin_people.py:123` keys `users/<speaker>.json` by speaker,
  not by place. `_touch_user` (`:153`) updates names, sessions, interactions,
  last seen, trust and relationship state for both group and private turns.
  Its relationship record contains numerical state and trajectory, repair,
  absence, attachment, commitment and investment, alongside text-bearing
  `transactive_map`, `destination_map`, `social_world`, `milestones`,
  `we_memory` and `annotations` (`relationship_meta.py:700`). The maps and
  candidates derive from current-place memory (`mixin_memory.py:426`); group
  items marked private are excluded before building them. Milestones come from
  visible archived events and retain source IDs. Existing merged fields can
  survive later turns from another place. Optional `we_memory` candidates
  derive from memory text (`mixin_people.py:128`), and the switch defaults off.
- Relationship impressions: `mixin_llm.py:369` uses visible archived events
  with sufficient importance and IDs, then either calls the enabled model or
  uses a deterministic numeric-state template. `relationship_meta.py:477`
  merges bounded `traits` and `relation_events` into `annotations`, and valid
  candidates into `we_memory`, with evidence references but no per-item place.
  It saves the same speaker record. Thus the inputs may come from either kind
  of place, subject to event visibility; this job is not inherently nightly.
- Relationship narratives: `mixin_llm.py:626` uses the speaker record's
  milestones when the optional function is enabled. It saves `text`,
  `evidence_refs` and an `origin` in `self_model.relationship_narratives`
  (`mixin_people.py:98` persists the self model). The origin uses the current
  place and speaker, with source IDs and private visibility if a found source
  was private. Source lookup may not find every old source. No direct read of
  this list in the normal `render_compact` reply path was found; the normal
  notebook path reads `notebook` instead (`mixin_discretion.py:678`). The list
  is also inspected for red lines and deletion (`mixin_impressions.py:175`,
  `mixin_discretion.py:1019`).
- Person record in replies: `mixin_turn.py:238` updates the current speaker,
  then passes `_user_view` to `render_compact` at `:304`. Outside that person's
  own private chat `_user_view` removes `we_memory`; in their private chat it
  also removes `we_memory` and `transactive_map` if retained group-private
  source material involving them is found (`mixin_discretion.py:848`).
  Independently, `interpretation.py:200` emits only an interaction-count
  familiarity description in group replies. In the person's private chat it
  may also render closeness, repair/conflict, absence, transactive topics and
  the first `we_memory` item. It does not directly render `annotations`,
  `milestones`, `destination_map` or `social_world` there.
- Deletion: `mixin_discretion.py:1272` registers a person deletion and calls
  `_forget`; this removes their person record, applicable self-model entries,
  group cards and aliases, and examines other relationship records for related
  text (`mixin_discretion.py:1019`, `:1060`, `:1076`, `:1136`). Deleting only
  an impression (`mixin_impressions.py:276`) instead removes group cards and
  blocks their recreation while retaining names and other memories.

## Inference and review risks

- `public_impression` and `private_bond` do not exist as storage layers in the
  inspected Python paths. A shared person record can merge material from
  different places; the present reply guards reduce exposure but do not assign
  reliable provenance to old text. Evidence IDs are not themselves a place.
- The requested boundary for another group needs an explicit decision for
  existing public cards: current code can supply cross-group names and aliases
  for a present person, while the same-group card supplies more detail. Old
  records without recoverable origins need a conservative migration rule.
- Review the indirect model calls and deletion paths as well as the reply
  prompt when designing the second stage. Narrative origins based on found
  milestone sources and group-private visibility need particular attention.
  Numeric relationship aggregates currently combine interactions across places.
  Their intended use is allowed by the card, but must not silently carry text.
- The card's external report path conflicts with the workspace-only rule, so
  this report uses the specified repository fallback. AstrBot was not checked,
  per the 11-01 instruction. No live data, network or services were accessed.
