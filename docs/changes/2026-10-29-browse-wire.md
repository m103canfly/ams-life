# 2026-10-29 · browse-wire

Her browser wired into the plugin, first part: in a reply (step 2, part 丁; the logic is `browse.py`, PR #29).
Off unless `browse_enabled` is on; off, nothing changes (the golden traces are the same, no file is written).

- A reply gets two tools of the plugin's own, `ams_web_search` and `ams_read_page`, put into the request after
  AstrBot's are all taken out (`_reply_tools_off`, unchanged: `allowed_tools` still only keeps AstrBot's own),
  and only while today's browser money is left. They are not registered with AstrBot (the reviewer agreed):
  AstrBot runs a tool by its name from the request's own tool set (`tool_loop_agent_runner.py` 1225-1235, both
  tool modes), so no other chat ever has them. They are AstrBot `FunctionTool`s with a handler, which AstrBot
  calls as `handler(event, **arguments)` (`astr_agent_tool_exec.py` 709-716, 813-814).
- Each does its work through AstrBot's own DeepSeek search and fetch (`get_llm_tool_manager().get_builtin_tool`),
  handed a context of this message's event and AstrBot's context, which is all they read
  (`web_search_tools.py` `_get_runtime`): the Key stays AstrBot's, the plugin never reads it.
- Before: the search words are cleaned (`browse.clean_query`: no long numbers, none of the names she knows anyone
  by); a page's address is checked (`browse.check_url` with this computer's resolver: http/https, no user, port
  80/443, nothing on this computer or the home network). After: results only with pages she may read; what comes
  back cut short and wrapped as material (`browse.wrap`; a page cannot end the wrapping early).
- At most 3 searches and 3 pages for one message (`browse.Quota.for_reply`), then the tool answers
  `这次不能再搜了。`; the same once today's browser money (`browse_yuan_per_day`, 5 yuan) is used up.
- The browser's money is kept apart from the chat's (`<data dir>/browse/ledger.json`): each successful search and
  page (0.00075 dollars), failed ones and refused addresses counted apart, and the model rounds a reply took for
  its tools, each estimated as dear as the last round (only its usage reaches the plugin; errs high).
  `page/status` carries the browser's day (spent, limit, searches, pages, trips) when it is on.
- Not here yet (the next parts): her going out by herself (the 5-minute loop, a trip of model rounds with the same
  two tools), what she keeps of a page (web memories with who asked, `asked_in`, and the mark for someone
  deleted), the "（网上看到的）" label when such a memory comes up again, her wishes to share, and the panel's line.

Before upgrading AstrBot: run `tests/test_browse_wire.py`, and read again the three places of AstrBot's named
above (how a tool is found by name, how a handler is called, what DeepSeek's tools read of their context).

Review of PR #39 (`审核-PR39.md`): an address could carry something private out to a site in its words (a page,
or someone in a group, writing "read https://site/?q=<what you know of so-and-so>"; the send check only looks at
what goes to QQ). So:

- a page is read only at an address this message (or the one it quotes) gave, or one of her searches in this
  reply found (`browse.urls_in`; `_browse_urls` on the event); any other answers
  `这个网址不能读：只能读消息里给的、或者搜索结果里的网址。` and counts as a refused address;
- with global_memory on, the words of a search and of an address (decoded) first go through the send check's own
  look (`_check_reply`: pieces, names, local vectors; no model): something labelled "这里不能讲" in this reply's
  prompt does not go out (`这个不能搜。`), even in an address the message gave.

Tests: an address nobody gave is not read; the message's and the search's are; with global_memory on, a search and
an address holding something private are held back. Undoing the first rule fails four tests, the second one.

## Files

- `mixin_browse.py`, `tests/browse_cases.py`, `tests/test_browse_wire.py` (new)
- `main.py` (the mixin, `browse_enabled`; on_llm_request gives the tools, on_llm_response counts the rounds)
- `mixin_pages.py` (`page/status`: the browser's day), `_conf_schema.json` (`browse_enabled`, off;
  `browse_yuan_per_day`, 5), `tests/test_basics.py` (+11 methods)

## README's table of modules

| `mixin_browse.py` | 她的浏览器接进插件（第 2 步丁块，第一段：回话时）：回话时只给她插件自己的两个工具（搜一下、读网页），借 AstrBot 自带的 DeepSeek 搜索和读网页去做（Key 在 AstrBot），搜索词洗掉名字和号码、本机内网的网址不读、网页包成资料、一条消息最多搜 3 次读 3 页、钱单独记（每天 5 元）；开关 `browse_enabled` 默认关 |
