# 2026-10-31 move-3b: DeepSeek model client

The move needs a second `ModelClient` for DeepSeek chat completions and tool calls.
`deepseek_client.py` adds that client without wiring it into the plugin. The caller passes
the key; a later caller can obtain it from 4a's `KeyStore`. The SDK is imported only when
the caller does not provide a client. The base URL must use HTTPS and the exact DeepSeek
host, so a lookalike host cannot receive the key. Images are rejected because the plugin
uses its own vision channel.

Messages are copied before system and prompt turns are added. Tool schemas and replies use
the shared model interface; SDK errors pass through. Reasoning is read from the message or
its SDK `model_extra`, and the tool loop sends it back in the assistant turn. Usage is
normalized by `browse.usage_of`, including DeepSeek cache hit and miss tokens.

`tests/test_deepseek_client.py` uses an offline fake client to check requests, responses,
errors, the tool loop, and imports. SDK construction is tested when `openai` is installed,
without a request. There is no new dependency or switch, and no existing behavior or golden
trace is changed because the client is not connected to the plugin.

Full suite: 1229 tests OK outside the sandbox with `venv-ams-life` (aiohttp 3.14.5, openai 3.41.0; main aee4e7a
had 1220; +9 in `tests/test_deepseek_client.py`), the real `AsyncOpenAI` construction included. With the
owner's Python (no openai) also 1229 OK, that one test skipped. Golden traces unchanged.
