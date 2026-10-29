"""Her camera and her voice as the owner wired them in on 10-30 (mixin_selfie.py), end to end
in media_cases.py with the two services faked. All words and numbers are made up."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'media_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class Media(unittest.TestCase):
    def test_off_unless_the_settings_say_on(self):
        r = run_case('off')
        self.assertEqual(r['asked'], {'selfie': [], 'voice': []})
        self.assertEqual(r['turns'], [[]])

    def test_a_keyword_brings_a_voice_note_and_a_photo(self):
        r = run_case('on')
        self.assertEqual(r['asked']['voice'], ['我在窗边看书呢'])     # her words, said aloud
        self.assertEqual(r['asked']['selfie'], ['我在窗边看书呢'])    # and what she is doing
        self.assertEqual(r['turns'], [[['Record'], ['Image']]])
        self.assertEqual((r['counters']['selfie'], r['counters']['voice']), (1, 1))

    def test_the_daily_limit(self):
        r = run_case('limit')
        self.assertEqual(r['turns'], [[['Record'], ['Image']], []])
        self.assertEqual(len(r['asked']['selfie']), 1)

    def test_what_is_held_back_is_never_said_aloud(self):
        r = run_case('held')
        self.assertEqual(r['asked'], {'selfie': [], 'voice': []})
        self.assertEqual(r['turns'], [[]])


if __name__ == '__main__':
    unittest.main()
