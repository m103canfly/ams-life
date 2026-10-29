"""No tools in her reply (the owner, 10-29: "现在关掉"): AstrBot adds tools of its own to every
reply (future_task, send_message_to_user, ...); on_llm_request takes them all out but those on
the setting allowed_tools (empty by default). The plugin cases run in a fresh interpreter
(tests/reply_tools_cases.py). All numbers, names and messages are made up.
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
            proc = subprocess.run([sys.executable, str(HERE / 'reply_tools_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class NoTools(unittest.TestCase):
    def test_every_tool_is_taken_out(self):
        r = run_case('default')
        self.assertIsNone(r['three'])                    # nothing left: AstrBot sends the model no tools
        self.assertEqual(r['logged'], ['[ams-life] tools taken out of the reply: '
                                       'future_task, send_message_to_user, web_search_deepseek'])

    def test_no_tools_no_trouble(self):
        r = run_case('default')
        self.assertEqual(r['empty'], [])
        self.assertEqual(r['none'], 'unset')

    def test_only_the_allowed_ones_stay(self):
        r = run_case('allowed')
        self.assertEqual(r['three'], ['web_search_deepseek'])
        self.assertEqual(r['logged'], ['[ams-life] tools taken out of the reply: future_task, send_message_to_user'])

    def test_with_the_plugin_switched_off_too(self):
        r = run_case('plugin_off')
        self.assertIsNone(r['three'])


if __name__ == '__main__':
    unittest.main()
