# 2026-10-31 move-2c-onebot-messenger: what she sends, over NapCat (OneBot 11)

The owner is moving the plugin out of AstrBot. Step 2 is the QQ layer: our own connection to
NapCat (OneBot 11), with no AstrBot in between. Step 1b fixed the `Messenger` interface; its
only implementation so far is the AstrBot one. This is the implementation we use with NapCat
directly: it turns the segments into OneBot 11 message segments and calls `send_group_msg` /
`send_private_msg`, and asks for the other allowed actions through the same one `call_api`.

New files only; no existing file is changed, so no behaviour changes and the golden traces stay
the same:

* `adapter_onebot_messenger.py`: `MAX_FILE_BYTES` (20 MiB), `ActionFailed`, `to_onebot` and
  `OneBotMessenger(call_api, *, roots=())`. It imports the standard library and `messenger`
  only, never AstrBot and never aiohttp.
* `tests/test_onebot_messenger.py`: the segment table, her folders, sending and the answers,
  the four actions and the refused ones, a comparison with AstrBot's own sending, and a source
  check that the module imports neither AstrBot nor aiohttp. Every file it needs is written in
  a `tempfile.TemporaryDirectory()` of the test's own.
* this note.

What NapCat receives is what AstrBot 4.29.3 sends today. The rules followed, from
`astrbot/core/platform/sources/aiocqhttp/aiocqhttp_message_event.py` (36-125):

* a local picture or voice is read from its file and sent as base64 (`base64://...`), never as
  a local path;
* a picture given as base64 keeps one `base64://` prefix; a picture given as a url sends the
  url;
* words are sent as they are, and a face sends its id as a string;
* words that are only whitespace are not sent, and a message with no segments at all calls no
  action;
* a group message goes to `group_id`, a private one to `user_id`, both as numbers.

One check AstrBot does not have is added: a local file is only read when it is a file inside
`roots`, her own folders (later her data folder). The path is resolved first and then compared
with `os.path.normcase` and `os.path.relpath`, as `interactive_browser._file_in_games` does, so
a `..` that leaves the folders, another drive, or a folder itself is refused. With no roots no
local path is accepted at all. This is on purpose: if some caller passes a wrong path, she
still cannot send another file of the computer. A refused file is a `ValueError` and the whole
message is not sent.

`call` is the same as aiocqhttp's `call_action`: it allows only `messenger.ALLOWED_ACTIONS`,
answers the frame's `data`, and raises `ActionFailed(action, retcode)` when the status is not
`ok`; `send` returns `Sent(True, message_id)` for `ok` and `Sent(False, "")` otherwise, and a
place that is not `group:<digits>` or `private:<digits>` calls nothing.

Tests: `tests/test_onebot_messenger.py` adds 40 tests. Inside dsh's sandbox
`python -m unittest tests.test_onebot_messenger` collects all 40; the 35 that need a temporary
folder stop with `PermissionError` because the sandbox does not allow temporary files, so the
file has to be run outside. The 5 tests that need no files passed (the four `call` cases and
the import check), and the rest of the module was walked through in memory (the segment table,
a real file read as base64, a file outside her folders, a `..` escape, a folder, sending,
failed answers and a raised error), all as expected.

Full suite: 1112 tests OK (main 7e92514 had 1072; +40 in `tests/test_onebot_messenger.py`). Golden traces unchanged.

Written by dsh (DeepSeek Harness, headless, workspace-write), dispatched and checked by the
build window.
