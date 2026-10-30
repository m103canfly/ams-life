# 2026-10-31 move-1a-events: one received message, apart from AstrBot

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Step 1 is "split the layers, fix the interfaces", and this is its smallest piece: what one
received message looks like. The future QQ layer will build the same object from NapCat's raw
message; this piece builds it from an AstrBot event, so the two can be checked item by item.

New files only; no existing file is changed, so no behaviour changes and the golden traces stay
the same:

* `events.py`: `Segment` and `Incoming` (frozen dataclasses) and `plain_text`.
* `adapter_astrbot.py`: `from_astrbot(event) -> Incoming`. Pure: it does not change the event,
  writes nothing, logs nothing and calls no plugin method (`_message_text` has side effects, so
  it is not used). A field that cannot be read becomes "" / False / an empty tuple.
* `tests/test_adapter_astrbot.py`: the fields one by one, events whose fields cannot be read, and
  a check that `place`, `at_me`, `reply_to`, `message_id` and `image_refs` equal what
  `MemoryMixin._here`, `PhoneMixin._addresses_her`, `PhoneMixin._reply_to`,
  `PhoneMixin._message_id` and `MediaMixin._image_ref` give for the same events.

New module line for README's table of modules (brought up to date later):

| `events.py` `adapter_astrbot.py` | 收到的一条消息长什么样（`Segment`、`Incoming`），以及从 AstrBot 的事件造出来 |

Full suite: run outside dsh's sandbox, `python -m unittest discover -s tests` ran 893 tests
(16 of them new), all OK; the golden traces did not change. Inside dsh's Windows sandbox the
suite cannot pass, because the sandboxed Python may not write temporary files.

Written by dsh (DeepSeek Harness, headless, workspace-write, its web tools off), dispatched and
checked by the build window: its tools touched only paths inside the worktree.