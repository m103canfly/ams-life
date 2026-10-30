# 2026-10-31 move-1c-model-client: one place to call the chat model

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Step 1 is "split the layers, fix the interfaces", and this is its third piece: **she calls a chat
model (tools included) through one `ModelClient`**. Today the plugin makes more than twenty
`provider.text_chat(...)` calls with differently shaped arguments, and reads the replies field by
field; the DeepSeek client of step 3 only has to implement the one interface.

New files only; no existing file is changed, so behaviour is unchanged and the golden traces stay
the same:

* `model_client.py`: `Tool`, `ToolCall` and `ModelReply` (frozen dataclasses), `ModelClient.chat`
  (subclasses override it) and `arguments_of` (a dict as is, a JSON object string parsed, anything
  else `{}`). Only the standard library and `browse.usage_of`; no AstrBot.
* `adapter_astrbot_model.py`: `AstrBotModel(provider, toolset_of=None)`. It passes on only the
  arguments it was given -- `prompt`, `system_prompt`, `contexts`, `image_urls`, and `func_tool`
  for a non-empty tool list (one `ToolSet` of `FunctionTool`, made by the given `toolset_of`; the
  default one makes AstrBot-style tools whose handler raises, since the plugin runs its own tools).
  The reply becomes a `ModelReply`; a field that cannot be read gives its empty value; an error
  `text_chat` raises passes through as it is.
* `tests/test_model_client.py`: a fake provider checks the exact `text_chat` arguments, the order
  of the tools, the ToolSet the default makes, the reply's fields (tool calls, unreadable
  arguments, missing ids, empty names, both usage shapes, reasoning) and the errors passing
  through; the interface file is read to check it does not mention AstrBot.

New module line for README's table of modules (brought up to date later):

| `model_client.py` `adapter_astrbot_model.py` | 调聊天模型的唯一接口（`Tool`、`ToolCall`、`ModelReply`、`ModelClient.chat`，参数照插件现在的调法），以及它在 AstrBot provider 上的实现 |

Full suite: not run inside dsh's sandbox -- the sandboxed Python may not write temporary files, and
the card says the dispatcher runs it outside. Run outside dsh, `python -m unittest discover -s
tests` is expected to cover main's 954 tests plus this card's 24 in `tests/test_model_client.py`.
Inside dsh's sandbox the card's own file, `python -m unittest tests.test_model_client`, ran 24
tests, all OK.

Written by dsh (DeepSeek Harness, headless, workspace-write), dispatched by the build window.

Full suite, run outside dsh's sandbox by the dispatcher: 994 tests, all OK; the golden traces did not change. Spot checks: sending `system_prompt=None` when `system` is `None` fails item 1 (4 tests); returning a list argument as is fails item 4 (2 tests).

