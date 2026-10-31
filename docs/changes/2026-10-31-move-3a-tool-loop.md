# 2026-10-31 move-3a-tool-loop: her own tool loop, plain Python

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Section 1 asks for "a tool loop of our own, for a reply and for the background alike... only these
tools of hers, no command line, no files"; section 12 borrows OpenMinis's guard against endless
loops. Today the plugin has two hand-written loops: the trip out (`mixin_browse.
_interactive_trip_rounds`) and the clickable browser, while the loop of a reply lives inside
AstrBot. This card writes **one general loop** on top of 1c's `ModelClient`; it is not wired into
the plugin yet (pieces 3 and 5 will).

New files only; no existing file is changed, so behaviour is unchanged and the golden traces stay
the same:

* `tool_loop.py`: `MAX_ROUNDS`, `RESULT_CHARS`, `REPEAT_WARN`, `REPEAT_STOP`; `LoopTool` (a
  `model_client.Tool` and the handler that runs for it) and `LoopResult` (frozen dataclasses); and
  `run(client, *, system=None, messages=(), tools=(), max_rounds=MAX_ROUNDS, round_seconds=None)`.
  Only the standard library and `model_client`: no plugin framework, no file, no subprocess, no
  socket; the loop itself never goes out. The messages it is given are copied and never changed.
  Each round asks `client.chat(system=..., messages=..., tools=...)`, adds up `reply.usage`, and
  either ends with her words or adds the assistant turn (`tool_calls` as
  `{"id", "type": "function", "function": {"name", "arguments"}}`) and one `tool` turn per call,
  in order. A tool the loop does not know answers "没有这个工具。" and runs nothing; a handler only
  gets the arguments its schema's `properties` name; a handler's error becomes one short sentence
  with the error's class name and no error text; a result that is not a `str` becomes one, and is
  cut to `RESULT_CHARS`. `reason` is `"done"`, `"rounds"`, `"repeat"` or `"timeout"`: the last
  round is asked without tools and with `{"role": "user", "content": "该收尾了，直接说你要说的话。"}`
  after the messages, and a `round_seconds` timeout ends the loop with no words. An error the
  client raises passes through as it is.
* `tests/test_tool_loop.py`: a fake model client answers from a script and records every round's
  `system`, `messages` and `tools`; fake handlers record their arguments. Every name, id, number
  and line of text is made up.

Borrowed from OpenMinis: the guard against an endless loop. The same call (the tool's name plus
its arguments in sorted JSON) is counted; at `REPEAT_WARN` times the result carries a note to her,
and from `REPEAT_STOP` times on the call is not run at all (the result says she has done the same
thing too often) and the next round is the last one. On top of that, the loop has a hard cap of
`MAX_ROUNDS` model calls, whose last one has no tools and a closing note.

The same as `mixin_browse._interactive_trip_rounds` today: the assistant turn carries the tool
calls in the same shape, and the model's `reasoning` is given back as `reasoning_content` when it
is not empty (DeepSeek wants its thinking back within the turn); an unknown tool answers
"没有这个工具。"; a handler error is one sentence; a result is stringified and cut. Different on
purpose: the loop is general (tools come in as `LoopTool`s, not one browser action), a client
error is passed on instead of ending quietly, a whole-round timeout is `asyncio.wait_for` around
the model call only (not around every handler), and the repeat guard is shared by all tools.

Tests (16, `python -m unittest tests.test_tool_loop`): words only end the loop in one round; a call
then words, with the assistant and tool turns the next round receives; the `reasoning_content` key
appears with reasoning and not when it is empty; an unknown tool runs no handler; the schema drops
extra arguments; a handler error is one sentence with no error text and the loop goes on; a long
result is cut to `RESULT_CHARS` and a number becomes text; the last round has no tools and the
closing note (reason `"rounds"`); the same call is warned, then not run, and ends the loop as
`"repeat"` with the next round the last; another key order is the same call; a slow client is a
timeout and another error passes through unchanged; usage is added up; and the module is read to
check it mentions no AstrBot, `mixin_`, `os`, `subprocess` or `socket`.

New module line for README's table of modules (brought up to date later):

| `tool_loop.py` | 她自己的工具循环（纯 Python）：给模型一轮一轮地看，按顺序跑它要的工具，结果送回；最后一轮不给工具、加一句收尾；重复的调用先提醒、太多次就不跑；只认 `LoopTool`，不读写文件、不联网 |

Full suite: 1200 tests OK outside the sandbox (main dad87b5 had 1184; +16 in `tests/test_tool_loop.py`).
Golden traces unchanged. Inside dsh's sandbox the card's own file, `python -m unittest tests.test_tool_loop`,
ran 16 tests, all OK.

Written by dsh (DeepSeek Harness, headless, workspace-write), dispatched by the build window.
