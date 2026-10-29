"""Made-up offline examples for the group-browsing estimate."""
import contextlib
import io
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch

from tools import sim_open_groups as sim


def ts(hour, minute=0, day=1):
    return datetime(2026, 1, day, hour, minute, tzinfo=timezone(timedelta(hours=8))).timestamp()


def sticker(ref):
    return "[CQ:image,subType=1,url=" + ref + "]"


def row(i, group, hour, minute, raw="", post="message", sender="900001"):
    return (i, group, post, raw, ts(hour, minute), sender)


class SimulationTests(unittest.TestCase):
    def test_score_requires_unread_and_a_pause(self):
        self.assertEqual(sim.browse_score(0, 1, 100, True, 180, 9), 0)
        self.assertEqual(sim.browse_score(20, 1, 4, True, 180, 9), 0)
        self.assertGreater(sim.browse_score(8, 1, 60, True, 180, 9),
                           sim.browse_score(1, 0, 10, False, 0, 12))

    def test_one_unread_does_not_force_an_open(self):
        self.assertEqual(sim.simulate([row(1, "g", 23, 59)], 5), (1, 0, 0))

    def test_limit_dedup_and_open_discards_overflow(self):
        raw = "".join(sticker(x) for x in ("a", "b", "c", "d", "a"))
        rows = [row(i, "g", 9, 1, raw if i == 1 else "") for i in range(1, 9)]
        self.assertEqual(sim.simulate(rows, 5), (1, 1, 3))

    def test_night_boundary_and_expiry(self):
        rows = [row(i, "g", 1, 1, sticker("old") if i == 1 else "") for i in range(1, 9)]
        self.assertEqual(sim.simulate(rows, 5), (1, 1, 0))

    def test_busy_and_sent_private_are_not_unread(self):
        rows = [row(i, "g", 12, 1, sticker(str(i))) for i in range(1, 9)]
        rows.append(row(9, None, 12, 4, sticker("sent"), "message_sent"))
        self.assertEqual(sim.simulate(rows, 5), (1, 1, 3))

    def test_safety_interval_changes_open_times(self):
        rows = [row(group * 10 + n, str(group), 9, 1,
                    sticker(str(group)) if n == 0 else "")
                for group in range(4) for n in range(8)]
        fast = sim.simulate(rows, 5)
        slow = sim.simulate(rows, 30)
        self.assertGreater(fast[2], slow[2])

    def test_marker_and_decoding(self):
        self.assertEqual(sim.sticker_refs('[CQ:image,subType=1,url=x&#44;y]'), ['x,y'])
        self.assertEqual(sim.sticker_refs('[CQ:image,sub_type=1,file=x]'), [])

    def test_sqlite_read_and_output_is_summary_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'made-up.db'
            with contextlib.closing(sqlite3.connect(path)) as db, db:
                db.execute('CREATE TABLE messages (id INTEGER, group_id TEXT, post_type TEXT, raw_message TEXT, timestamp REAL, user_id TEXT)')
                db.executemany('INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?)',
                               [row(i, 'private-group', 9, 1, sticker('private-url')) for i in range(1, 9)])
            self.assertEqual(len(sim.load_rows(path)), 8)
            output = io.StringIO()
            with patch('sys.argv', ['sim', '--chat', str(path), '--price', '0.25']), contextlib.redirect_stdout(output):
                sim.main()
            self.assertEqual(len(output.getvalue().splitlines()), 3)
            self.assertNotIn('private', output.getvalue())

    def test_empty(self):
        self.assertEqual(sim.simulate([], 5), (0, 0, 0))


if __name__ == '__main__':
    unittest.main()
