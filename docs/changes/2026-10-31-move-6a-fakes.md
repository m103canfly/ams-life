# 2026-10-31 move-6a: the two shared test fakes

The move's design, section 4, gives the new QQ layer, model layer and panel their own tests: a
fake NapCat (a local WebSocket client that speaks OneBot 11) and a fake DeepSeek (answers shaped
like the openai SDK). The 2d and 3b tests each had a small stand-in of their own; these two are
the shared ones that 5e and 6b use, so a test does not write one again.

## What was added

- `tests/fake_napcat.py`: `FakeNapCat` connects to `OneBotServer` on this machine with
  `Authorization: Bearer`, `X-Self-ID` and `X-Client-Role: Universal`. A background task answers
  every `{action, params, echo}` frame with that same `echo`. Every call is kept in `calls`;
  `send_group_msg` and `send_private_msg` are also kept in `sent` and get message ids from 1 up;
  `get_msg` finds a message the fake sent out (an event from `send_event`, or a message it was
  asked to send); `get_forward_msg` and any other action answer `failed`. `answer` scripts the
  answers to one action; a scripted answer is used once, in order. `group_message` and
  `private_message` build array-format events (at, reply, text, images); a message id is made up
  when none is given. The url must be `127.0.0.1`, else `ValueError`. aiohttp is imported only
  when the connection opens, so the message builders work without it.
- `tests/fake_deepseek.py`: `FakeDeepSeek` stands in for `openai.AsyncOpenAI`: `.chat` and
  `.chat.completions` are there, `create()` keeps its kwargs (`messages` copied) and gives back
  the next reply scripted by `say` or `call_tools`. A reply is shaped like the SDK's
  `ChatCompletion`: `choices[0].message` has `content`, `tool_calls` (arguments as a JSON
  string, ids `call_1`, `call_2`, ...) and the reasoning in `model_extra`, which is where the SDK
  keeps a field it does not know; `usage` has the four token attributes and `model_dump()`.
  Tool calls are `(name, arguments dict)`. A call with no scripted reply left is a mistake in the
  test and raises `AssertionError("no scripted reply")` at once, so an extra call is visible.
  Only the standard library; no SDK, no network.
- `tests/test_fakes.py`: both fakes checked against the real modules. `FakeDeepSeek` is given to
  `DeepSeekModel` (words, two tool calls, reasoning, usage) and to `tool_loop.run` (a tool round
  then words; the second request carries the thinking and the tool result; one call more than
  scripted raises). `FakeNapCat` connects to `OneBotServer` on an OS-chosen port (skipped
  without aiohttp): the handshake, an event arriving as an `Incoming` through `from_onebot`,
  a message sent through the messenger with a numeric group id, `get_msg` finding both what it
  sent and what she sent, and a scripted failure reaching `OneBotMessenger.call` as
  `ActionFailed`. The non-local url is refused. Two small cases need no socket: the messages
  the fake builds (a group one with at, reply and images, and a private one read by
  `from_onebot`), and the fake sources, which must import neither AstrBot nor an SDK.

## Why nothing else changes

Only new files under `tests/` and this note were added; no plugin module, entry point, switch,
setting, dependency or golden trace is touched. The suite's number of tests grows by the new
file's tests; no existing test is changed. The fakes build no temporary folder, so the
temporary-cleanup guard is unaffected. Every number, name, link and message in the tests is made
up (20002, 10001, 900001); nothing connects to a real account, and the only socket is a loopback
one opened by the test itself on a port the operating system picks.

Full suite: 1291 tests OK outside the sandbox with `venv-ams-life` (main e39fb76 had 1276; +15 in `tests/test_fakes.py`), the
fake NapCat over the real server included; with the owner's Python (no aiohttp) also 1291 OK, those skipped.
Golden traces unchanged.
