# 2026-10-29 send-check: the last look at a reply before it is sent

Step 2 (己, part 2). Only with the setting `global_memory` (off by default; off, nothing changes).

## What

- While the reply prompt is built, the items labelled "这里不能讲" are noted on the event: their words, their vector, and the names of who they are about (not of whoever is talking to her or is here). For "不点名" items only the names are noted, and for a web page someone asked about in private, the asker's names. Everything else in the prompt counts as what may be said here; that includes the block in the system prompt, with only its sayable items counted.
- `send_check.check` (pure). A reply leaks when it holds one of these:
  - a piece only those items have: four characters in a row, a number of three digits or more, or a Latin word of four letters or more. The piece must not be in what may be said here, not an everyday word, and not common. Common means said by two or more people, or in two or more places, in all she keeps.
  - a cosine with one of them of 0.86 or more. 0.78 to 0.86 is only noted.
  - a name from them that is not said here.
- `on_llm_response`:
  - First leak: the chat model is asked once more, with the same request (block, message, history, system prompt, pictures), one line more and no tools. The call is counted.
  - Still a leak: `stop_event()`. AstrBot neither sends nor saves it, and the plugin keeps nothing of it.
  - The look itself failing is held back the same way.
  - The log has ids only.
- `on_agent_done` (new hook; AstrBot saves the turn after it):
  - the last assistant message of `run_context.messages` becomes exactly the words sent, without the model's thinking (`ThinkPart`);
  - the event's `_llm_reasoning_content` is cleared.
- Counts per day go in `states/send_check.json` (redone, held, close, failed, redo calls and tokens). The panel shows today's counts next to the red-line note.

## New modules (for the README's table)

| File | What |
| --- | --- |
| `send_check.py` `mixin_send_check.py` | 第 2 步（`global_memory` 打开时）：回话发出去以前再查一道——说了标着“这里不能讲”的事（特有的字、意思很像、名字）就请模型重说一次，还漏就不发，检查本身出错也不发；AstrBot 存的对话里只留发出去的话，不留模型“想”的部分；面板上能看今天挡了几次 |

## Files

`send_check.py` (new), `mixin_send_check.py` (new), `main.py` (`SendCheckMixin`, `on_llm_response`, `on_agent_done`), `mixin_memory.py`, `mixin_events.py`, `mixin_discretion.py` (noting what may not be said), `mixin_pages.py`, `pages/dashboard/index.html`, `pages/dashboard/app.js` (the panel line), `tests/test_send_check.py`, `tests/send_check_cases.py` (new), `tests/test_basics.py` (method count).
