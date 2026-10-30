"""Offline replay over a made-up SQLite database."""
import contextlib
import io
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools import sim_slang


class SlangSimulationTests(unittest.TestCase):
    def test_simulation_counts_without_chat_or_identifiers(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'chat.sqlite'
            with contextlib.closing(sqlite3.connect(path)) as db, db:
                db.execute('CREATE TABLE messages (id TEXT, group_id TEXT, post_type TEXT, raw_message TEXT, timestamp REAL, user_id TEXT)')
                for i in range(25):
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                               ('r' + str(i), '900002', 'message', '参考词条', 1000000, '10006'))
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                               ('s' + str(i), '900003', 'message', '参考词条', 1000000, '10007'))
                for i in range(5):
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                               ('m' + str(i), '900001', 'message', '猫猫冲鸭', 1000000, str(10001 + i % 3)))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(sim_slang.main(['--chat', str(path)]), 0)
            text = out.getvalue()
            self.assertIn('群1', text)
            self.assertIn('黑话 1', text)
            self.assertNotIn('猫猫冲鸭', text)
            self.assertNotIn('900001', text)
            self.assertNotIn('10001', text)
            shown = io.StringIO()
            with contextlib.redirect_stdout(shown):
                self.assertEqual(sim_slang.main(['--chat', str(path), '--show']), 0)
            self.assertIn('猫猫冲鸭', shown.getvalue())

    def test_nightly_new_words_are_bounded(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'chat.sqlite'
            with contextlib.closing(sqlite3.connect(path)) as db, db:
                db.execute('CREATE TABLE messages (id TEXT, group_id TEXT, post_type TEXT, raw_message TEXT, timestamp REAL, user_id TEXT)')
                for i in range(100):
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                               ('r' + str(i), '900002', 'message', '参考词条', 1000000, '10006'))
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                               ('s' + str(i), '900003', 'message', '参考词条', 1000000, '10007'))
                words = ['memeaa', 'memeab', 'memeac', 'memead', 'memeae',
                         'memeaf', 'memeag', 'memeah', 'memeai', 'memeaj']
                for number, word in enumerate(words):
                    for i in range(5):
                        db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                                   ('m%d-%d' % (number, i), '900001', 'message', word, 1000000, str(10001 + i % 3)))
            result = sim_slang.simulate(path)
            self.assertEqual(result[0][0], 2)

    def test_boundary_time_quantity_filtered_before_ledger(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'chat.sqlite'
            with contextlib.closing(sqlite3.connect(path)) as db, db:
                db.execute('CREATE TABLE messages (id TEXT, group_id TEXT, post_type TEXT, raw_message TEXT, timestamp REAL, user_id TEXT)')
                for i in range(5):
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                               ('m' + str(i), '900001', 'message', '的猫 猫了 你我 九点 三个',
                                1000000, str(10001 + i % 3)))
                for group in ('900002', '900003'):
                    for i in range(20):
                        db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',
                                   (group + str(i), group, 'message', '参考词条', 1000000, '10006'))
            self.assertEqual(sim_slang.simulate(path)[0][:2], (0, 0))

    def test_missing_sender_column_does_not_invent_people(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'chat.sqlite'
            with contextlib.closing(sqlite3.connect(path)) as db, db:
                db.execute('CREATE TABLE messages (id TEXT, group_id TEXT, post_type TEXT, raw_message TEXT, timestamp REAL)')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(sim_slang.main(['--chat', str(path)]), 1)


if __name__ == '__main__':
    unittest.main()
