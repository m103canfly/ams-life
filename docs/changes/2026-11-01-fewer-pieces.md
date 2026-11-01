# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.

# Fewer reply pieces

The owner asked for mostly one message, with at most 10 pieces:

> 绝大多数时候只写一段（发一条）。只有在确有必要时才可以分段（最多不超过 10段）。一段里别换行。

The previous guidance encouraged splitting. The new guidance favors one piece and
keeps each piece on one line. `MAX_MESSAGES` is now 10; extra pieces still merge
into the last piece. `reply_in_pieces` and the group hourly limit are unchanged.
The separate persona text is outside this change.

The existing attention assertions for seven pieces, six lines, and the note were
updated. Offline tests cover the exact note, 10 and 12 pieces, and the prepared
turn prompt. No plugin methods were added.

Both golden files were intentionally regenerated. The only changes are the
`PIECES_NOTE` text in these JSON paths:

- `basic.turns[0].inject[0]`
- `basic.turns[1].inject[0]`
- `basic.turns[2].inject[0]`
- `basic.turns[3].inject[0]`
- `basic.turns[4].inject[0]`
- `basic.turns[5].inject[0]`
- `basic.turns[6].inject[0]`
- `basic.turns[7].inject[0]`
- `basic.turns[8].inject[0]`
- `basic.turns[9].inject[0]`
- `basic.turns[10].inject[0]`
- `basic.turns[11].inject[0]`
- `basic.turns[12].inject[0]`
- `basic.turns[13].inject[0]`
- `basic.turns[14].inject[0]`
- `basic.turns[15].inject[0]`
- `basic.turns[16].inject[0]`
- `basic.turns[17].inject[0]`
- `basic.turns[18].inject[0]`
- `basic.turns[19].inject[0]`
- `basic.turns[20].inject[0]`
- `basic.turns[21].inject[0]`
- `basic.turns[22].inject[0]`
- `basic.turns[23].inject[0]`
- `full.turns[0].inject[0]`
- `full.turns[1].inject[0]`
- `full.turns[2].inject[0]`
- `full.turns[3].inject[0]`
- `full.turns[4].inject[0]`
- `full.turns[5].inject[0]`
- `full.turns[6].inject[0]`
- `full.turns[7].inject[0]`
- `full.turns[8].inject[0]`
- `full.turns[9].inject[0]`
- `full.turns[10].inject[0]`
- `full.turns[11].inject[0]`
- `full.turns[12].inject[0]`
- `full.turns[13].inject[0]`
- `full.turns[14].inject[0]`
- `full.turns[15].inject[0]`
- `full.turns[16].inject[0]`
- `full.turns[17].inject[0]`
- `full.turns[18].inject[0]`
- `full.turns[19].inject[0]`
- `full.turns[20].inject[0]`
- `full.turns[21].inject[0]`
- `full.turns[22].inject[0]`
- `full.turns[23].inject[0]`

Validation: the first golden run failed for the changed prompt; regeneration
skipped both tests as expected, and the subsequent golden run passed. Individual
runs passed: `test_attention` (38), `test_fewer_pieces` (3),
`test_prepare_turn` (5), `test_golden` (2), and `test_basics` (11). The full
suite was not run as requested. `test_golden_standalone` was left for the owner
to run outside the sandbox; its table was not changed.

