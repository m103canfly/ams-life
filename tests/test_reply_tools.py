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

    def test_an_error_leaves_no_tools(self):
        # review of PR #27: should taking them out fail, she gets none (not all of them)
        self.assertIsNone(run_case('broken')['broken'])

    def test_with_the_plugin_switched_off_too(self):
        r = run_case('plugin_off')
        self.assertIsNone(r['three'])



class HookOrder(unittest.TestCase):
    """Her on_llm_request runs after every other plugin's (AstrBot's own is priority 0, and
    AstrBot sorts by priority, highest first): the tools are taken out last, and the numbers
    come out of the group context lines the built-in plugin adds (step 2). The stand-in
    AstrBot of the tests drops the decorator's arguments, so this reads them from main.py."""

    def test_on_llm_request_priority_is_below_zero(self):
        import ast
        tree = ast.parse((HERE.parent / 'main.py').read_text(encoding='utf-8'))
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef) and n.name == 'on_llm_request')
        deco = next(d for d in fn.decorator_list
                    if isinstance(d, ast.Call) and getattr(d.func, 'attr', '') == 'on_llm_request')
        prio = {k.arg: ast.literal_eval(k.value) for k in deco.keywords}.get('priority', 0)
        self.assertLess(prio, 0)


if __name__ == '__main__':
    unittest.main()
