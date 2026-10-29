"""Senders she ignores (setting ignore_senders; the owner, 10-29: the new account does not answer
the old companion, nor keep what it says). The plugin cases run in a fresh interpreter
(tests/ignore_cases.py). All numbers, names and messages are made up.
"""
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
            proc = subprocess.run([sys.executable, str(HERE / 'ignore_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class Listed(unittest.TestCase):
    def test_an_at_of_her_from_him_is_stopped_and_not_kept(self):
        r = run_case('listed')
        self.assertTrue(r['stopped'][0])                     # stopped: AstrBot calls no model for it
        self.assertNotIn('10099', r['model_calls'])
        self.assertFalse([t for who, t in r['phone'] if who == '10099'])

    def test_what_he_says_without_an_at_is_not_kept_either(self):
        r = run_case('listed')
        self.assertTrue(r['stopped'][1])
        self.assertNotIn('今天天气不错', [t for _w, t in r['phone']])
        self.assertTrue(r['stopped'][4])                      # the list's second number, spaces around it
        self.assertNotIn('我也在', [t for _w, t in r['phone']])
        self.assertNotIn('10098', r['names'])                 # not in her names either (10099 is: @'d by 柠檬)

    def test_everyone_else_as_before(self):
        r = run_case('listed')
        self.assertEqual(r['stopped'][2:4], [False, False])
        self.assertEqual(r['model_calls'], ['10002'])
        self.assertIn(['10002', '@小爱 你好'], r['phone'])
        self.assertIn(['10002', '问问 @机器人(10099) 在吗'], r['phone'])   # someone else's words about him: kept

    def test_the_later_hooks_stop_him_too(self):
        r = run_case('listed')
        self.assertTrue(r['late_request_stopped'])
        self.assertTrue(r['late_request_untouched'])
        self.assertTrue(r['late_response_stopped'])
        self.assertEqual(r['phone_after'], r['phone'])         # her answer to him is not kept


class Empty(unittest.TestCase):
    def test_no_list_as_before(self):
        r = run_case('empty')
        self.assertEqual(r['stopped'], [False] * 5)
        self.assertEqual(r['model_calls'], ['10099', '10002'])
        self.assertIn(['10099', '@小爱 欢迎新人！'], r['phone'])
        self.assertIn(['10099', '今天天气不错'], r['phone'])


if __name__ == '__main__':
    unittest.main()
