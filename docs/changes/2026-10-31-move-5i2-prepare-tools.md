# Move 5i-2: prepare tools on the turn

Tool preparation now works on `TurnRequest` so a platform-neutral caller can use it.
The AstrBot hook converts the request, prepares tools and the turn, and writes back.
The existing phone, browser, and reply tool methods remain available. The same
switches and warnings apply. No files outside the card were changed (`tests/reply_tools_cases.py`
was added to the card on 10-31).

Changed tool lists are written into an existing ToolSet; unchanged lists and their
ToolSet are left alone. If the old route emptied a ToolSet and then added phone
tools, it made a new ToolSet; the new route keeps the original. For a permitted
disabled tool with the same name as one of her tools, AstrBot's active preference
and `TurnRequest.add_tool` can choose differently. The card accepts these differences.

If reading or writing the tool set fails, the hook gives no tools and logs the
same warning, preserving the PR #27 rule. On 10-31 review authorized changing the
Broken test tool set to fail when its tools are written back; the neutral route no
longer calls its `remove_tool`.

## Test results

Each file was run separately in the sandbox:

- `tests.test_prepare_tools`: Ran 6 tests in 0.019s | OK
- `tests.test_turn_tools`: Ran 10 tests in 0.012s | OK
- `tests.test_turn`: Ran 10 tests in 0.001s | OK
- `tests.test_prepare_turn`: Ran 5 tests in 0.052s | OK
- `tests.test_basics`: Ran 11 tests in 0.040s | OK
- `tests.test_golden`: Ran 2 tests in 3.459s | OK
- `tests.test_selfie`: Ran 46 tests in 1.785s | OK
- `tests.test_browse_wire`: Ran 20 tests in 2.200s | OK
- `tests.test_reply_tools`: Ran 6 tests in 1.422s | OK
- `tests.test_message_steps`: Ran 6 tests in 0.012s | OK
- `tests.test_after_reply`: Ran 6 tests in 1.112s | OK

Outside the sandbox the same 11 modules pass one at a time with `venv-ams-life`; the golden
files are unchanged. A script checked the hook: it starts with `main.py` 624-628 as they were,
the read and the write of tools each fall back to no tools with the old warning, and it no
longer calls `_give_phone_tools`, `_give_browse_tools` or `_reply_tools_off`. The
`_prepare_tools` docstring is the card's, and its three warnings are the old ones word for word.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).
