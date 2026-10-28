"""tools/import_old.py on made-up old data: only what people were called and the forget registry
are carried over (the owner's decision), and it never writes where it must not."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import fake_old_data as fake  # noqa: E402
from tools import _guard, import_old  # noqa: E402

BUSY, SMALL = 'group:' + fake.G_BUSY, 'group:' + fake.G_SMALL


def lines(path):
    return [json.loads(x) for x in Path(path).read_text('utf-8').splitlines() if x.strip()]


class Import(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        old = Path(cls.tmp.name) / 'old'
        fake.build_old(old)
        cls.out = Path(cls.tmp.name) / 'bundle'
        cls.summary = import_old.build(old, cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_only_names_and_the_registry(self):
        self.assertEqual(sorted(p.name for p in self.out.iterdir()),
                         ['aliases.jsonl', 'forget_registry.sqlite3', 'manifest.json', 'skipped.json'])
        self.assertEqual(lines(self.out / 'aliases.jsonl'), [
            {'place': SMALL, 'qq': fake.PEACH, 'name': '桃子', 'aliases': ['桃桃'],
             'origin': {'where': SMALL, 'people': [fake.PEACH], 'source_ids': [], 'visibility': 'public'}}])

    def test_left_out(self):
        self.assertEqual(self.summary['skipped'], {'forgotten': 1, 'no_alias_left': 1})   # 星星, 大佬
        dump = (self.out / 'aliases.jsonl').read_text('utf-8')
        for gone in ('星星', '大佬', '抽卡', '猫', '爬山'):   # nothing of the archive, cards, profiles, notebook
            self.assertNotIn(gone, dump)

    def test_registry_and_manifest(self):
        manifest = json.loads((self.out / 'manifest.json').read_text('utf-8'))
        self.assertEqual(manifest['registry']['rows']['people'], 1)
        self.assertEqual(manifest['registry']['rows']['source'], 3)
        self.assertEqual(manifest['replay_registries_found'], 1)
        self.assertNotIn('replay_1', manifest['registry']['imported'])           # not counted unless asked
        self.assertEqual(set(manifest['inputs']), {'notebook_forget', 'ledger_registry', 'cognition'})

    def test_replay_registries_when_asked(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path(tmp) / 'old'
            fake.build_old(old)
            s = import_old.build(old, Path(tmp) / 'b', replay_registries=True)
            self.assertEqual(s['registry']['rows']['optout'], 1)
            self.assertEqual(s['registry']['rows']['people'], 2)

    def test_no_one_registered_under_the_cutoff_reading(self):
        import forget_registry
        with tempfile.TemporaryDirectory() as tmp:
            old = Path(tmp) / 'old'
            fake.build_old(old)
            reading = forget_registry.FORGET_ME
            forget_registry.FORGET_ME = forget_registry.FORGET_ME_CUTOFF
            try:
                s = import_old.build(old, Path(tmp) / 'b')
            finally:
                forget_registry.FORGET_ME = reading
            self.assertEqual(s['skipped']['forgotten'], 1)
            self.assertNotIn('星星', (Path(tmp) / 'b' / 'aliases.jsonl').read_text('utf-8'))

    def test_old_forgets_let_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path(tmp) / 'old'
            fake.build_old(old)
            s = import_old.build(old, Path(tmp) / 'b', old_forgets='let-in')
            self.assertEqual(s['registry']['rows']['people'], 0)
            self.assertIn('星星', (Path(tmp) / 'b' / 'aliases.jsonl').read_text('utf-8'))


class Guard(unittest.TestCase):
    def test_refuses_live_data_repo_and_full_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            for bad in (Path(tmp) / 'AstrBot' / 'data' / 'x', Path(tmp) / 'a' / 'plugin_data' / 'x',
                        Path(__file__).resolve().parent / 'should_not_exist'):
                with self.assertRaises(_guard.Refused, msg=str(bad)):
                    _guard.output_dir(bad)
                self.assertFalse(bad.exists())
            full = Path(tmp) / 'full'
            full.mkdir()
            (full / 'f').write_text('x')
            with self.assertRaises(_guard.Refused):
                _guard.output_dir(full)
            self.assertTrue(_guard.output_dir(Path(tmp) / 'new').is_dir())

    def test_cli_refuses_before_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                import_old.main(['--old', os.path.join(tmp, 'nothing'), '--out',
                                 os.path.join(tmp, 'astrbot', 'data', 'plugin_data', 'x')])


if __name__ == '__main__':
    unittest.main()
