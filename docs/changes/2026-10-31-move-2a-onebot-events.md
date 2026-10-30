# 2026-10-31 move-2a-onebot-events: NapCat's raw message becomes an Incoming

The owner is moving the plugin out of AstrBot. Step 2 is the QQ layer: our own connection to
NapCat (OneBot 11), with no AstrBot in between. This is its smallest piece: one pure function
that turns one message NapCat pushes as JSON into the `events.Incoming` of step 1a.

New files only; no existing file is changed, so no behaviour changes and the golden traces stay
the same:

* `adapter_onebot.py`: `from_onebot(payload, *, quoted=None, names=None) -> Incoming | None`.
  Pure: no I/O, no logging, no AstrBot, and it never raises. Anything that is not one message
  event gives None (not a dict, another `post_type`, another `message_type`, a string `message`,
  as AstrBot does not read the string format either). A part it cannot read is left out.
* `tests/test_adapter_onebot.py`: one case per field and per part, payloads that are not message
  events, broken parts, and a check that the same message gives the same Incoming through
  `from_onebot` and through `from_astrbot` on an event built by hand the way AstrBot 4.29.3
  builds it.

The split follows AstrBot 4.29.3 (`aiocqhttp_platform_adapter.py`, 198-425), so moving over does
not change what she hears:

* a row of `text` parts becomes one text, and the joined words are stripped ("@小爱 你好" gives
  "你好"); a row that is empty once stripped adds no text;
* an `at` keeps the number and the name; `all` is "全体成员";
* a `reply` keeps the quoted id and the quoted message's sender; `reply_to` is the first reply's
  id, cut to 80 characters;
* `image` and `record` keep url and file, `face` and `forward` keep the id, `markdown` is one
  piece of text as it is (not stripped, not joined with the text beside it);
* `mface` (the shop sticker) is skipped, and so is a part AstrBot does not know;
* `video`, `file`, `rps`, `dice`, `shake`, `share`, `contact`, `location`, `music`, `poke`,
  `node`, `nodes` and `json` are "other", with AstrBot's class name in `kind`;
* `place` is "group:<id>" or "private:<sender>", the private session AstrBot uses.

The three small differences (for step 5 to look at again):

* a name AstrBot does not have is `""` for us, not `"N/A"`;
* AstrBot looks up an `@`'s name and the quoted message's sender itself; our caller looks them
  up and passes `names` and `quoted`;
* AstrBot drops messages from QQ's butler account. We do not; a later gate (step 5) does that by
  configuration, and that number is not written into the repository.

New module line for README's table of modules (brought up to date later):

| `adapter_onebot.py` | NapCat（OneBot 11）推来的一条消息，变成 `events.Incoming`，跟 AstrBot 的拆法对得上 |

Tests: `tests/test_adapter_onebot.py` adds 34 tests; only this file was run in the sandbox, with
`python -m unittest tests.test_adapter_onebot` (34 tests, all OK).

Full suite: 1065 tests OK (main a85d118 had 1031; +34 in `tests/test_adapter_onebot.py`). Golden traces unchanged.

Written by dsh (DeepSeek Harness, headless, workspace-write), dispatched and checked by the build
window.
