# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for her own configuration file (app_config.py).

Every file is built in the test's own temp folder and removed at the end. The real
`_conf_schema.json` is read as it is; nothing else is read and no value is printed.
"""
import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import app_config  # noqa: E402
from app_config import ConfigError, compare, defaults, load, load_schema, save  # noqa: E402

TYPES = ('bool', 'int', 'float', 'string', 'list')
SCHEMA = {
    'is_on': {'description': 'a switch', 'type': 'bool', 'default': False},
    'count': {'description': 'a count', 'type': 'int', 'default': 3},
    'price': {'description': 'a price', 'type': 'float', 'default': 0.5},
    'name': {'description': 'a name', 'type': 'string', 'default': 'x'},
    'words': {'description': 'some words', 'type': 'list', 'default': ['a']},
    'no_switch': {'description': 'no default', 'type': 'bool'},
    'no_count': {'description': 'no default', 'type': 'int'},
    'no_price': {'description': 'no default', 'type': 'float'},
    'no_name': {'description': 'no default', 'type': 'string'},
    'no_words': {'description': 'no default', 'type': 'list'},
}


class TempFolder(unittest.TestCase):
    """A folder of its own per test, removed afterwards."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.path = self.folder / 'config.json'

    def write(self, data):
        self.path.write_text(json.dumps(data), encoding='utf-8')

    def files(self):
        return sorted(p.name for p in self.folder.iterdir())


class RealSchema(unittest.TestCase):
    def test_the_repository_schema_is_flat_and_typed(self):
        schema = load_schema()   # the real _conf_schema.json next to app_config.py
        self.assertGreaterEqual(len(schema), 100)
        for key, item in schema.items():
            self.assertIsInstance(item, dict, key)
            self.assertIn(item.get('type'), TYPES, key)

    def test_the_schema_defaults_are_used_as_they_are(self):
        schema = load_schema()
        values = defaults(schema)
        self.assertEqual(list(values), list(schema))
        for key, item in schema.items():
            if 'default' in item:
                self.assertEqual(values[key], item['default'], key)


class Defaults(unittest.TestCase):
    def test_a_default_in_the_schema_is_used_as_it_is(self):
        values = defaults(SCHEMA)
        self.assertIs(values['is_on'], False)
        self.assertEqual(values['count'], 3)
        self.assertEqual(values['price'], 0.5)
        self.assertEqual(values['name'], 'x')
        self.assertEqual(values['words'], ['a'])
        self.assertEqual(list(values), list(SCHEMA))

    def test_a_setting_without_a_default_gets_the_empty_one_of_its_type(self):
        values = defaults(SCHEMA)
        self.assertIs(values['no_switch'], False)
        self.assertEqual(values['no_count'], 0)
        self.assertIsInstance(values['no_count'], int)
        self.assertEqual(values['no_price'], 0.0)
        self.assertIsInstance(values['no_price'], float)
        self.assertEqual(values['no_name'], '')
        self.assertEqual(values['no_words'], [])

    def test_a_list_default_is_ours_and_not_the_schema_s(self):
        values = defaults(SCHEMA)
        values['words'].append('b')
        self.assertEqual(defaults(SCHEMA)['words'], ['a'])
        self.assertEqual(SCHEMA['words']['default'], ['a'])


class Load(TempFolder):
    def test_a_missing_file_is_all_defaults(self):
        config, problems = load(self.path, SCHEMA)
        self.assertEqual(config, defaults(SCHEMA))
        self.assertEqual(problems, [])

    def test_bad_json_and_a_file_that_is_not_an_object_are_unreadable(self):
        for text in ('{not json', '[]', '"a string"', '[1, 2]'):
            with self.subTest(text=text):
                self.path.write_text(text, encoding='utf-8')
                config, problems = load(self.path, SCHEMA)
                self.assertEqual(config, defaults(SCHEMA))
                self.assertEqual(problems, ['unreadable'])

    def test_a_wrong_type_takes_the_default(self):
        cases = (('is_on', 'yes'), ('is_on', 1), ('count', True), ('count', 1.5),
                 ('price', '1.5'), ('price', True), ('name', 5), ('words', 'a word'))
        for key, value in cases:
            with self.subTest(key=key, value=type(value).__name__):
                self.write({key: value})
                config, problems = load(self.path, SCHEMA)
                self.assertEqual(config[key], defaults(SCHEMA)[key])
                self.assertEqual(problems, ['type: ' + key])

    def test_problems_name_the_key_and_never_the_value(self):
        self.write({'is_on': 'a-secret-word', 'count': '900001', 'price': '1.5'})
        config, problems = load(self.path, SCHEMA)
        self.assertEqual(problems, ['type: is_on', 'type: count', 'type: price'])
        text = ' '.join(problems)
        for value in ('a-secret-word', '900001', '1.5'):
            self.assertNotIn(value, text)
        self.assertEqual(config, defaults(SCHEMA))

    def test_a_float_takes_a_whole_number(self):
        self.write({'price': 1})
        config, problems = load(self.path, SCHEMA)
        self.assertEqual(config['price'], 1.0)
        self.assertIsInstance(config['price'], float)
        self.assertEqual(problems, [])

    def test_a_file_astrbot_wrote_with_a_bom_is_read(self):
        data = {'is_on': True, 'count': 7, 'price': 1.5, 'name': 'hello',
                'words': ['a', 'b']}
        with open(self.path, 'w', encoding='utf-8-sig') as file:
            json.dump(data, file)
        self.assertTrue(self.path.read_bytes().startswith(b'\xef\xbb\xbf'))
        config, problems = load(self.path, SCHEMA)
        self.assertIs(config['is_on'], True)
        self.assertEqual(config['count'], 7)
        self.assertEqual(config['price'], 1.5)
        self.assertEqual(config['name'], 'hello')
        self.assertEqual(config['words'], ['a', 'b'])
        self.assertEqual(problems, [])

    def test_a_key_outside_the_schema_is_kept(self):
        self.write({'count': 4, 'a_new_setting': {'inner': [1, 2]}})
        config, problems = load(self.path, SCHEMA)
        self.assertEqual(config['count'], 4)
        self.assertEqual(config['a_new_setting'], {'inner': [1, 2]})
        self.assertEqual(problems, ['unknown: a_new_setting'])
        self.assertEqual(config['is_on'], False)


class Save(TempFolder):
    def test_write_then_read_is_the_same(self):
        config = defaults(SCHEMA)
        config.update({'is_on': True, 'count': 7, 'price': 1.5, 'name': 'hello',
                       'words': ['a', 'b']})
        save(self.path, config, SCHEMA)
        loaded, problems = load(self.path, SCHEMA)
        self.assertEqual(loaded, config)
        self.assertEqual(problems, [])
        self.assertEqual(self.files(), ['config.json'])   # no temp file left behind

    def test_keys_follow_the_schema_order_and_unknown_ones_come_last(self):
        config = {'a_new_setting': 'kept', 'words': ['b'], 'name': 'hello', 'count': 1}
        save(self.path, config, SCHEMA)
        pairs = json.loads(self.path.read_text(encoding='utf-8'), object_pairs_hook=list)
        self.assertEqual([key for key, _ in pairs], list(SCHEMA) + ['a_new_setting'])

    def test_a_wrong_type_writes_nothing(self):
        self.write({'count': 4})
        before = self.path.read_bytes()
        config = defaults(SCHEMA)
        config['count'] = True
        with self.assertRaises(ConfigError) as error:
            save(self.path, config, SCHEMA)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.files(), ['config.json'])
        self.assertNotIn('True', str(error.exception))

    def test_a_failed_replace_keeps_the_old_file(self):
        self.write({'count': 4})
        before = self.path.read_bytes()
        config = defaults(SCHEMA)
        config['count'] = 9
        seen = []

        def failing_replace(tmp, path):
            seen.append(Path(tmp).parent)
            raise OSError('the disk is full')

        with mock.patch.object(app_config.atomic_file, 'replace', failing_replace):
            with self.assertRaises(OSError):
                save(self.path, config, SCHEMA)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.files(), ['config.json'])   # the temp file is gone too
        self.assertEqual([folder.resolve() for folder in seen], [self.folder.resolve()])


class Compare(unittest.TestCase):
    def test_the_same_values_are_no_difference(self):
        ours = defaults(SCHEMA)
        self.assertEqual(compare(ours, dict(ours), SCHEMA), [])

    def test_a_changed_value_is_the_key(self):
        ours = defaults(SCHEMA)
        other = dict(ours)
        other['count'] = ours['count'] + 1
        self.assertEqual(compare(ours, other, SCHEMA), ['count'])
        self.assertEqual(compare(other, ours, SCHEMA), ['count'])

    def test_a_key_astrbot_lacks_counts_as_its_default(self):
        ours = defaults(SCHEMA)
        other = {key: value for key, value in ours.items() if key != 'count'}
        self.assertEqual(compare(ours, other, SCHEMA), [])
        other['is_on'] = True
        self.assertEqual(compare(ours, other, SCHEMA), ['is_on'])

    def test_a_float_written_whole_is_not_a_difference(self):
        ours = defaults(SCHEMA)
        ours['price'] = 1.0
        other = dict(ours)
        other['price'] = 1
        self.assertEqual(compare(ours, other, SCHEMA), [])

    def test_every_difference_is_listed_once_in_schema_order(self):
        ours = defaults(SCHEMA)
        other = dict(ours)
        other['words'] = ['b']
        other['is_on'] = True
        self.assertEqual(compare(ours, other, SCHEMA), ['is_on', 'words'])


class Source(unittest.TestCase):
    def test_no_astrbot_and_no_logging(self):
        tree = ast.parse((ROOT / 'app_config.py').read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(alias.name.split('.')[0], ('astrbot', 'logging'))
            elif isinstance(node, ast.ImportFrom):
                self.assertNotIn((node.module or '').split('.')[0], ('astrbot', 'logging'))
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotEqual(node.func.id, 'print')


if __name__ == '__main__':
    unittest.main()
