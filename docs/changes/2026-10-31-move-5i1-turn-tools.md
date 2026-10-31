# 2026-10-31 move 5i-1: the neutral tool lists

The tool section of `main.py` (672-695) still makes AstrBot's `FunctionTool`s by hand on the
request. 5e needs one tool table of her own (`turn.TurnTool`), so the two steps are split: this
card adds the neutral builders in the three mixins and keeps the old methods as thin AstrBot
shells; 5i-2 (after 5d) moves `main.py` onto the neutral methods. `main.py` and
`adapter_astrbot_turn.py` are not touched here, and the plugin still calls the old methods, so
nothing it does changes.

New file `adapter_astrbot_tools.py` (standard library only):

* `available()`: whether `astrbot.core.agent.tool` can be imported.
* `function_tool(tool)`: one `FunctionTool` from one `TurnTool` (name, description, parameters,
  handler).
* `add_to_request(req, tools)`: as the plugin did — no tool set yet makes
  `req.func_tool = ToolSet([...])`, an existing one gets `add_tool` for each, in order.

`FunctionTool` and `ToolSet` are imported inside the functions, as before.

The three mixins:

* `mixin_selfie.py`: new `_phone_tools(event) -> list` holds the old 204-230 lines, with
  `FunctionTool` changed to `turn.TurnTool`; descriptions, switches and order are unchanged, and
  it returns `[]` while the plugin is off. `_give_phone_tools(req, event)` is now the shell, in
  the old order: off -> return; tool classes not importable -> one warning and return (before any
  tool is made, as before: `_phone_context` is not called then); otherwise add the list.
* `mixin_browse.py`: new `_browse_tools(event) -> list` returns `[]` while browsing is off or
  today's money is gone, else the search and read tools as `turn.TurnTool` (same descriptions,
  parameters and handlers), records this message's quota and addresses, and returns them.
  `_give_browse_tools(req, event)` is the shell: off or no money -> `False`; tool classes not
  importable -> `False` silently (as before: no quota, no addresses); else add and return `True`.
* `mixin_settings.py`: new `_tools_not_allowed(names) -> list` (the old 189-191 lines: the
  setting `allowed_tools` as a list or one name a line, blanks stripped) and new
  `_turn_tools_off(turn_request) -> list` for 5i-2 (it takes the names out of a `TurnRequest`,
  one `remove_tool` each, and logs one line with the same words as before). `_reply_tools_off`
  only replaces its three lines with `gone = self._tools_not_allowed(names)`.

One order changed in `_give_browse_tools`: the quota and the message's addresses are now recorded
before the tools go in, not after. Nothing looks at the quota or the addresses in between, so the
result is the same; the old import-failure path still records neither.

`tests/test_basics.py`: the method count of `test_all_methods_reachable` goes +4, for
`_phone_tools`, `_browse_tools`, `_tools_not_allowed` and `_turn_tools_off`, with one comment
line.

`tests/test_turn_tools.py` (10 tests; AstrBot's tool classes are stand-ins put into `sys.modules`
for one test and taken out again, and no file is written):

* `test_both_routes_make_the_same_tools`: with all switches on, all off and one on, each route
  gives exactly the expected names (`set_now`, `take_photo`, `share_screenshot`, `say_aloud` /
  `set_now` / `set_now` and `say_aloud`), and the `TurnTool`s of `_phone_tools` and the
  `FunctionTool`s `_give_phone_tools` puts into the request have the same names, descriptions,
  parameters and handlers, in the same order.
* `test_switched_off_no_tools_and_no_tool_set`: `_phone_tools` is `[]` and the request still has
  no `func_tool`.
* `test_missing_tool_classes_warned_before_the_tools_are_made`: without the tool classes the
  phone shell logs `[ams-life] phone tools unavailable`, `_phone_context` is never called (a
  counting stand-in), and the request has no tool set.
* `test_missing_tool_classes_no_browse_tools_no_quota_no_addresses`: the browse shell returns
  `False` and records neither the quota nor the message's addresses.
* `test_off_or_no_money_no_tools_and_no_quota`: browse off or no money left -> `[]`, no quota.
* `test_on_gives_search_and_read_and_keeps_the_messages_addresses`: `[search, read]` with
  `_tool_search` / `_tool_read`, quota set, the message's address kept.
* `test_allowed_tools_as_list_as_text_and_empty`: `allowed_tools` as a list, as a multi-line
  text and as nothing gives the right names, in their order.
* `test_turn_request_keeps_order_and_logs_one_line`: `_turn_tools_off` takes the names out of a
  `TurnRequest`, keeps the order, and logs one line with the same words.
* `test_turn_request_nothing_to_take_out_no_line`: nothing to take out -> `[]`, no log line.
* `test_the_four_methods_do_not_name_astrbot`: reading the source with `ast`, the bodies of
  `_phone_tools`, `_browse_tools`, `_tools_not_allowed` and `_turn_tools_off` name no `astrbot`,
  `FunctionTool` or `ToolSet`.

Tests: `tests.test_turn_tools` and `tests.test_basics` pass outside the sandbox with `venv-ams-life` (21 tests).
`tests/test_basics.py` counts the four new methods (494 -> 498). The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
