"""Her writes ("temp file, then os.replace") while something else keeps reading the same file
(atomic_file.py). On Windows a file open for reading cannot be replaced; the write must still
go through. No AstrBot, no network."""
import os
import re
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import atomic_file  # noqa: E402


class WhileRead(unittest.TestCase):
    def test_every_write_goes_through(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'library.json'
            path.write_text('x' * 1000000, 'utf-8')
            stop = threading.Event()

            def reader():   # opens, reads, closes, again and again
                while not stop.is_set():
                    try:
                        with open(path, encoding='utf-8') as f:
                            f.read()
                    except OSError:
                        pass
                    time.sleep(0.002)
            t = threading.Thread(target=reader)
            t.start()
            failed = []
            try:
                for i in range(200):
                    part = Path(tmp) / 'library.tmp'
                    part.write_text(str(i) * 1000, 'utf-8')
                    try:
                        atomic_file.replace(part, path)
                    except PermissionError as exc:
                        failed.append(exc)
            finally:
                stop.set()
                t.join()
            self.assertEqual(failed, [])
            self.assertEqual(path.read_text('utf-8'), '199' * 1000)

    def test_other_errors_are_not_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                atomic_file.replace(Path(tmp) / 'missing.tmp', Path(tmp) / 'x.json')

    def test_her_writes_all_use_it(self):
        bare = []
        for path in sorted(ROOT.glob('*.py')):
            if path.name == 'atomic_file.py':
                continue
            for n, line in enumerate(path.read_text('utf-8').splitlines(), 1):
                if re.search(r'\bos\.replace\(', line):
                    bare.append('%s:%d' % (path.name, n))
        self.assertEqual(bare, [])


if __name__ == '__main__':
    unittest.main()
