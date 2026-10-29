"""tools/import_aliases.py: an import bundle's registry and what people were called, staged into a
new empty folder (step 1, installing on this computer). Every number and name is made up."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import forget_registry  # noqa: E402
from tools import _guard, import_aliases  # noqa: E402

G = 'group:900001'
KEPT, GONE = '10001', '10003'   # 10003 is in the registry


def made_up_bundle(folder):
    """2 people with names in one group; one of them is in the registry (and one message is)."""
    folder.mkdir(parents=True)
    with forget_registry.ForgetRegistry(folder / forget_registry.FILE_NAME) as reg:
        reg.forget_person(GONE, stamp=1.0, note='legacy:test')
        reg.forget_message('m-5003', stamp=1.0, note='legacy:test')
        reg.remember_names(GONE, ['阿星'])
    rows = [{'place': G, 'qq': KEPT, 'name': '芒果', 'aliases': ['小芒', '芒芒', '你'], 'origin': {}},
            {'place': G, 'qq': GONE, 'name': '阿星', 'aliases': ['星星'], 'origin': {}}]
    (folder / 'aliases.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), 'utf-8')
    (folder / 'manifest.json').write_text('{}', 'utf-8')
    return folder


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def files(folder):
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file())


class Stage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        cls.bundle = made_up_bundle(tmp / 'bundle')
        cls.before = {name: sha(cls.bundle / name) for name in files(cls.bundle)}
        cls.out = tmp / 'stage' / 'data'
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        proc = subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'import_aliases.py'),
                               '--bundle', str(cls.bundle), '--out', str(cls.out)],
                              capture_output=True, text=True, encoding='utf-8', env=env, timeout=60)
        if proc.returncode != 0:
            raise AssertionError(proc.stdout + proc.stderr)
        cls.printed = json.loads(proc.stdout)
        cls.report = json.loads((cls.out / 'import_aliases.json').read_text('utf-8'))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_what_is_written(self):
        self.assertEqual(files(self.out), sorted(['forget_registry.sqlite3', 'import_aliases.json',
                                                  'people/names.json', 'people/' + self._group_file()]))

    def _group_file(self):
        return next(p.name for p in (self.out / 'people').iterdir() if p.name != 'names.json')

    def test_the_registry_is_copied_as_it_is_and_the_bundle_left_alone(self):
        self.assertEqual(sha(self.out / forget_registry.FILE_NAME), self.before[forget_registry.FILE_NAME])
        self.assertEqual({name: sha(self.bundle / name) for name in files(self.bundle)}, self.before)

    def test_who_the_registry_rules_out_is_left_out(self):
        group = json.loads((self.out / 'people' / self._group_file()).read_text('utf-8'))
        self.assertEqual(group['place'], G)
        self.assertEqual(sorted(group['people']), [KEPT])
        self.assertEqual(group['people'][KEPT]['aliases'], ['小芒', '芒芒'])   # '你' is no name (check_alias)
        names = (self.out / 'people' / 'names.json').read_text('utf-8')
        self.assertNotIn(GONE, names)
        self.assertNotIn('星星', names)

    def test_counts_only(self):
        r = self.report
        self.assertEqual(r['aliases_lines'], 2)
        self.assertEqual(r['aliases'], {'people': 1, 'person_forgotten': 1})
        self.assertEqual(r['registry']['rows']['qq'], 1)
        self.assertEqual(r['registry']['rows']['source'], 1)
        self.assertEqual(r['registry']['rows']['people'], 1)
        self.assertEqual(r['registry']['names'], {'people': 1, 'name_hashes': 1})
        self.assertEqual(self.printed, r)
        text = json.dumps(r, ensure_ascii=False)
        for secret in (KEPT, GONE, '芒果', '小芒', '阿星', '星星', 'm-5003'):
            self.assertNotIn(secret, text)


class Refuses(unittest.TestCase):
    """--out never in the repository, in AstrBot's data, or a folder with something in it; nothing made."""

    def run_tool(self, bundle, out):
        return subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'import_aliases.py'),
                               '--bundle', str(bundle), '--out', str(out)],
                              capture_output=True, text=True, encoding='utf-8', timeout=60)

    def test_refused_and_nothing_made(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bundle = made_up_bundle(tmp / 'bundle')
            full = tmp / 'full'
            full.mkdir()
            (full / 'left.txt').write_text('编造', 'utf-8')
            cases = {
                'inside the repository': ROOT / 'made-up-stage',
                'AstrBot data folder': tmp / 'astrbot' / 'data' / 'plugin_data' / 'astrbot_plugin_ams_life',
                'plugin_data folder': tmp / 'x' / 'plugin_data' / 'astrbot_plugin_ams_life',
                'not an empty folder': full,
            }
            for said, out in cases.items():
                proc = self.run_tool(bundle, out)
                self.assertNotEqual(proc.returncode, 0, said)
                self.assertIn('refusing', proc.stderr, said)
                if said == 'not an empty folder':
                    self.assertEqual(files(full), ['left.txt'])
                else:
                    self.assertFalse(out.exists(), said)
            self.assertFalse((tmp / 'astrbot').exists())
            self.assertFalse((tmp / 'x').exists())

    def test_not_a_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'out'
            proc = self.run_tool(Path(tmp) / 'nothing', out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('not an import bundle', proc.stderr)
            self.assertFalse(out.exists())

    def test_the_guard_is_the_tools_guard(self):
        self.assertIs(import_aliases._guard, _guard)


if __name__ == '__main__':
    unittest.main()
