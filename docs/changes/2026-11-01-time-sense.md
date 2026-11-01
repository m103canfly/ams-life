# Time sense, part 1b

The owner can now have dates remembered in private. The `remember_day` tool is
offered only in that conversation, and checks the same boundary when called.
Dates and their private origin are stored in `states/our_days.json`. The turn
shows the owner's dates after calendar material, or says none have been saved;
dates within seven days come first. Month-day and year-month-day dates recur
annually, starting no earlier than a specified year. Deleting a person removes
their related dates; a failure is logged without blocking the other deletions.
There are no new switches or dependencies. AstrBot-specific tests are omitted
under the owner's November 1 instruction.

The authorized golden update adds only `\n你们之间记下的日子：还没有。` to
the following values in each of `basic.json` and `full.json`:

| File | Changed JSON values |
| --- | --- |
| basic | `turns[0].inject[0]`, `turns[1].inject[0]`, `turns[7].inject[0]`, `turns[8].inject[0]`, `turns[9].inject[0]`, `turns[16].inject[0]`, `turns[17].inject[0]`, `turns[18].inject[0]`, `turns[19].inject[0]`, `turns[20].inject[0]` |
| full | `turns[0].inject[0]`, `turns[1].inject[0]`, `turns[7].inject[0]`, `turns[8].inject[0]`, `turns[9].inject[0]`, `turns[16].inject[0]`, `turns[17].inject[0]`, `turns[18].inject[0]`, `turns[19].inject[0]`, `turns[20].inject[0]` |

The complete diff was checked line by line: removing the insertion from each
new line yields its old line. Both reconstructed JSON documents parse and
the paths above identify every changed value. The tool list did not change in
these scenarios. `test_selfie` updates its explicitly authorized tool-set
assertion; `test_basics` counts the new stable handler. No other old tests were
changed.

Validation: `test_our_days` 4, `test_time_sense` 2, `test_selfie` 46,
`test_turn_tools` 10, `test_forget_wiring` 19, `test_prepare_turn` 5,
`test_golden` 2 and `test_basics` 11 passed separately. The full suite was not
run; `test_golden_standalone` is reserved for the owner outside the sandbox.
No pages or files outside the authorized scope were changed.

# Time sense, part 1

Add calendar material and elapsed days to the turn. There are no new switches or
dependencies. Anniversary storage and tools are deferred. The AstrBot-specific
work is omitted under the owner's November 1 instruction.

The existing approximate solar-term table is shared with `look`; only 立冬
changes, from November 8 to November 7. This also advances the winter season
in the outfit line by one day. On the same day, solar terms take precedence,
then solar festivals, then lunar festivals; within each table the first match
wins. Only festivals are announced in advance, up to seven days. Unsupported
lunar years produce one warning per process and omit lunar dates.

The lunar table uses Gregorian dates in this order: 除夕, 春节, 元宵, 端午,
七夕, 中秋, 重阳.

| Year | Dates |
| --- | --- |
| 2026 | 02-16, 02-17, 03-03, 06-19, 08-19, 09-25, 10-18 |
| 2027 | 02-05, 02-06, 02-20, 06-09, 08-08, 09-15, 10-08 |
| 2028 | 01-25, 01-26, 02-09, 05-28, 08-26, 10-03, 10-26 |
| 2029 | 02-12, 02-13, 02-27, 06-16, 08-16, 09-22, 10-16 |
| 2030 | 02-02, 02-03, 02-17, 06-05, 08-05, 09-12, 10-05 |

These dates need independent review: network access is prohibited, and the
local calendar API could not be constructed in the sandbox's PowerShell
language mode. The card supplies the 2026 and 2027 examples, not the full table.

Private turns add elapsed days before the existing continuity summary; group
turns add a separate elapsed-days line and retain the existing summary. The
original summary, loops and relationship data still go to feedback; a
days-only turn does not create a feedback record.

The authorized golden update changes exactly these JSON values. The excerpts
are truncated around the insertion; all omitted text is identical:

| File and JSON path | Old excerpt | New excerpt |
| --- | --- | --- |
| basic `turns[12].inject[0]` | `…认识\n此刻：…` | `…认识\n[上次聊到] 好久没见他了（3 天）\n此刻：…` |
| basic `turns[21].inject[0]` | `…\n此刻：…` | `…\n[上次聊到] 好久没见他了（3 天）\n此刻：…` |
| full `turns[12].inject[0]` | `…认识\n此刻：…` | `…认识\n[上次聊到] 好久没见他了（3 天）\n此刻：…` |
| full `turns[21].inject[0]` | `…\n此刻：…` | `…\n[上次聊到] 好久没见他了（3 天）\n此刻：…` |

An independent recursive comparison against `git show HEAD:tests/golden/...`
verified that removing those insertions restores every old JSON value. The
golden update was followed by a passing golden test.

Validation: `test_calendar_cn` 4, `test_time_sense` 2, `test_her_look` 5,
`test_prepare_turn` 5, `test_reply_provenance` 7, `test_golden` 2 and
`test_basics` 11 all passed. The full suite was not run as instructed;
`test_golden_standalone` is reserved for the owner outside the sandbox. No
pages or other out-of-scope files were edited.

审核用香港天文台公历农历对照表逐年核了 2026–2030，改正一处：2028 年重阳是 10-26（原表 10-27）。
