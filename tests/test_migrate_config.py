# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for tools/migrate_config.py: AstrBot's plugin configuration turned into her own config.json.

Every file is built in the test's own temporary folder and removed at the end. The repository's
real `_conf_schema.json` is read as it is, and every value written here is made up. One test
checks that none of those values reaches the screen.
"""
import ast
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import app_config  # noqa: E402
from tools import migrate_config  # noqa: E402

BOOL = 'photo_enabled'                 # a switch, off by default
INT = 'phone_photo_retention'          # a count
FLOAT = 'phone_photo_price'            # a price
STRING = 'selfie_reference'            # a file name
LIST = 'her_names'                     # a list

MADE_UP = {BOOL: True, INT: 900001, FLOAT: 1.5, STRING: '编造-名字', LIST: ['编造-名单']}
MADE_UP_VALUES = ('编造-名字', '编造-名单', '编造-yes', '900001', '1.5')


def made_up(**changes):
    """An AstrBot-shaped configuration with made-up values; `changes` replace a few of them."""
    data = dict(MADE_UP)
    data.update(changes)
    return data


def write_astrbot(path, data):
    """AstrBot writes its configuration as utf-8-sig, so the file starts with a byte-order mark."""
    with open(path, 'w', encoding='utf-8-sig') as file:
        json.dump(data, file, ensure_ascii=False)


def move(*argv):
    """Run the tool in this interpreter; give back its exit code and everything it printed."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = migrate_config.main([str(x) for x in argv])
    return code, out.getvalue() + err.getvalue()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class TempFolder(unittest.TestCase):
    """A folder of its own per test, removed afterwards."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.astrbot = self.folder / 'astrbot_plugin_ams_life_config.json'
        self.out = self.folder / 'config.json'

    def names(self):
        return sorted(p.name for p in self.folder.iterdir())


class Convert(TempFolder):
    """--out: AstrBot's copy read, her config.json written and read back."""

    def test_write_then_read_has_no_bom_and_no_difference(self):
        data = made_up()
        write_astrbot(self.astrbot, data)
        self.assertTrue(self.astrbot.read_bytes().startswith(b'\xef\xbb\xbf'))
        code, text = move('--astrbot', self.astrbot, '--out', self.out)
        self.assertEqual(code, 0, text)
        self.assertFalse(self.out.read_bytes().startswith(b'\xef\xbb\xbf'))
        written = json.loads(self.out.read_text(encoding='utf-8'))
        for key, value in data.items():
            self.assertEqual(written[key], value, key)
        self.assertEqual(written[LIST], ['编造-名单'])
        schema = app_config.load_schema()
        read_back, problems = app_config.load(self.out, schema)
        self.assertEqual(problems, [])
        self.assertEqual(read_back, written)
        self.assertEqual(app_config.compare(read_back, data, schema), [])
        self.assertEqual(self.names(), ['astrbot_plugin_ams_life_config.json', 'config.json'])

    def test_a_wrong_type_takes_the_default_and_is_named_not_shown(self):
        write_astrbot(self.astrbot, made_up(**{BOOL: '编造-yes'}))
        code, text = move('--astrbot', self.astrbot, '--out', self.out)
        self.assertEqual(code, 1, text)
        self.assertIn(BOOL, text)
        self.assertNotIn('编造-yes', text)
        written = json.loads(self.out.read_text(encoding='utf-8'))
        self.assertIs(written[BOOL], app_config.defaults(app_config.load_schema())[BOOL])

    def test_bad_json_stops_with_nothing_written(self):
        self.astrbot.write_text('{not json', encoding='utf-8')
        code, text = move('--astrbot', self.astrbot, '--out', self.out)
        self.assertEqual(code, 2, text)
        self.assertFalse(self.out.exists())
        self.assertEqual(self.names(), ['astrbot_plugin_ams_life_config.json'])

    def test_an_existing_file_is_not_written_over(self):
        write_astrbot(self.astrbot, made_up())
        self.out.write_text('{"kept": true}\n', encoding='utf-8')
        before = sha(self.out)
        code, text = move('--astrbot', self.astrbot, '--out', self.out)
        self.assertEqual(code, 2, text)
        self.assertEqual(sha(self.out), before)

    def test_a_folder_under_astrbot_data_is_refused(self):
        write_astrbot(self.astrbot, made_up())
        out = self.folder / 'astrbot' / 'data' / 'plugin_data' / 'astrbot_plugin_ams_life' / 'config.json'
        code, text = move('--astrbot', self.astrbot, '--out', out)
        self.assertEqual(code, 2, text)
        self.assertIn('refusing', text)
        self.assertFalse(out.exists())
        self.assertFalse((self.folder / 'astrbot').exists())


class Check(TempFolder):
    """--check: an existing config.json compared with AstrBot's copy, nothing written."""

    def setUp(self):
        super().setUp()
        write_astrbot(self.astrbot, made_up())
        code, text = move('--astrbot', self.astrbot, '--out', self.out)
        self.assertEqual(code, 0, text)

    def test_the_same_values_are_exit_0_and_nothing_is_written(self):
        before = (sha(self.astrbot), sha(self.out))
        code, text = move('--astrbot', self.astrbot, '--check', self.out)
        self.assertEqual(code, 0, text)
        self.assertEqual((sha(self.astrbot), sha(self.out)), before)

    def test_a_changed_setting_is_exit_1_and_the_key_only(self):
        write_astrbot(self.astrbot, made_up(**{FLOAT: 1.25}))
        before = (sha(self.astrbot), sha(self.out))
        code, text = move('--astrbot', self.astrbot, '--check', self.out)
        self.assertEqual(code, 1, text)
        self.assertIn(FLOAT, text)
        self.assertNotIn('1.25', text)
        self.assertEqual((sha(self.astrbot), sha(self.out)), before)


class Screen(TempFolder):
    """Nothing made up is ever printed: only key names, counts and paths."""

    def test_no_made_up_value_is_printed(self):
        write_astrbot(self.astrbot, made_up())
        code, text = move('--astrbot', self.astrbot, '--out', self.out)
        self.assertEqual(code, 0, text)
        code, checked = move('--astrbot', self.astrbot, '--check', self.out)
        self.assertEqual(code, 0, checked)
        write_astrbot(self.astrbot, made_up(**{BOOL: '编造-yes'}))
        code, typed = move('--astrbot', self.astrbot, '--out', self.folder / 'second.json')
        self.assertEqual(code, 1, typed)
        screen = text + checked + typed
        for value in MADE_UP_VALUES:
            self.assertNotIn(value, screen)
        self.assertIn(BOOL, typed)   # a problem names its key


class Source(unittest.TestCase):
    def test_no_astrbot_and_no_logging(self):
        tree = ast.parse((ROOT / 'tools' / 'migrate_config.py').read_text(encoding='utf-8'))
        seen = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                seen.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                seen.add((node.module or '').split('.')[0])
        self.assertNotIn('astrbot', seen)
        self.assertNotIn('logging', seen)


if __name__ == '__main__':
    unittest.main()
