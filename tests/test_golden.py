"""Golden traces: the scripted conversation must produce exactly the recorded trace.

The traces in tests/golden/ were recorded from the unmodified BioCore v1.2.99 code (plus the rename). Pure refactors
must keep them byte-for-byte. A change that is meant to alter behaviour regenerates them on purpose:

    AMS_UPDATE_GOLDEN=1 python3 -m unittest tests.test_golden

and the diff of tests/golden/ shows exactly what changed.
"""
import difflib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOLDEN = HERE / 'golden'


def run_scenario(mode):
    with tempfile.TemporaryDirectory() as tmp:
        data, out = Path(tmp) / 'data', Path(tmp) / 'trace.json'
        data.mkdir()
        env = dict(os.environ, PYTHONHASHSEED='0')
        env.pop('AMS_LIFE_DATA_DIR', None)
        proc = subprocess.run([sys.executable, str(HERE / 'scenario.py'), str(data), str(out), mode],
                              env=env, capture_output=True, text=True, timeout=300)
        if proc.returncode != 0:
            raise AssertionError(f'scenario {mode} failed:\n{proc.stdout}\n{proc.stderr}')
        return out.read_text('utf-8')


class Golden(unittest.TestCase):
    maxDiff = None

    def check(self, mode):
        got = run_scenario(mode)
        path = GOLDEN / f'{mode}.json'
        if os.environ.get('AMS_UPDATE_GOLDEN') == '1':
            path.write_text(got, 'utf-8')
            self.skipTest(f'golden {mode} rewritten')
        want = path.read_text('utf-8')
        if got != want:
            diff = ''.join(list(difflib.unified_diff(want.splitlines(True), got.splitlines(True),
                                                     'golden', 'now', n=2))[:120])
            self.fail(f'trace for {mode} changed:\n{diff}')
        json.loads(got)  # still valid JSON

    def test_basic(self):
        self.check('basic')

    def test_full(self):
        self.check('full')


if __name__ == '__main__':
    unittest.main()
