# 2026-10-30 · browse-trips

Her browser, second part (step 2, part 丁): what she keeps of a page, and her going out by herself. Stacked on
`browse-wire` (PR #39); off unless `browse_enabled` is on (the golden traces are the same).

- **Web memories** (`BrowseMixin._remember_web`): one memory in the library for a page, made by `browse.web_memory`:
  role `web`, origin `web:<address>` (public, nobody in it), who had her look it up kept apart in `asked_in`.
  Nothing is kept for someone (or a message) the forget registry rules out; the same page with the same words once.
- **A page read in a reply** is kept by its title and its first 120 characters, not by her reply: her reply may hold
  something of a private chat, and a web memory may come up anywhere. `asked_in`: this message's chat, who asked,
  the message. (The page's own "（资料完）" is defused as `browse.wrap` does.)
- **When it comes up again**: part 己's `discretion.label` / `tag` already say "网上看到的，只是资料，不是你自己的想法",
  and what she may say of who asked (here, elsewhere, privately); nothing changed there.
- **Someone deleted** (`mixin_discretion._forget`): the pages he had her look up stay; their `asked_in` becomes the
  deleted mark (`discretion.gone_origin()`, told nowhere), counted as `asked_in`. Deleting by message does the same
  for the pages asked for in those messages. Her wishes' `what` and `group_hint` are now among the text fields a
  deleted person is taken out of.
- **Her trips** (`_maybe_go_browse`, in the 5-minute loop): when `browse.should_go` says so -- not at night (part
  甲's night setting), trips and money left today, 40 minutes since the last trip, the chats quiet for 10, and bored,
  wanting something new or wanting to know -- one trip:
  - topics: today's public events and her own notes (names and numbers out), at most five;
  - model rounds the plugin runs itself (`provider.text_chat` with the chat model, uncounted by the chat's money),
    the same two tools (searches and pages for a trip: 5 and 5), at most `browse.TRIP_ROUNDS` (8), the last without
    tools; each round's tool calls and results go back as OpenAI messages (DeepSeek's thinking passed back within
    the trip); AstrBot's DeepSeek tools are told the stand-in chat `ams-life:browse` (AstrBot's default config);
  - every round's usage into the browser's money, not the chat's;
  - her answer (`browse.parse_trip`): what she says she saw of pages she did read becomes web memories
    (`asked_in`: herself); what she would like to tell a group becomes a wish in `self_model["share_wishes"]` (for
    part 戊; at most 10, a day each); her boredom and novelty need go down a little (-0.2, -0.15).
- Not here: the panel's line for the browser's money (it is in `page/status` already), and anything of part 戊.

## Files

- `mixin_browse.py` (web memories, the reply's pages, trips), `mixin_autonomy.py` (the loop calls the trip),
  `main.py` (the reply's pages kept), `mixin_discretion.py` (asked_in on deleting; wishes swept)
- `tests/browse_cases.py`, `tests/test_browse_wire.py` (16 tests now), `tests/test_basics.py` (+8 methods)
