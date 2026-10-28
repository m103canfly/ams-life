"""tools/import_old.py on made-up old data: what is carried over, what is left out, and where it may never write."""
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

BUSY, SMALL, TEST = 'group:' + fake.G_BUSY, 'group:' + fake.G_SMALL, 'group:' + fake.G_TEST


def lines(path):
    return [json.loads(x) for x in Path(path).read_text('utf-8').splitlines() if x.strip()]


class Import(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        old = Path(cls.tmp.name) / 'old'
        fake.build_old(old)
        cls.out = Path(cls.tmp.name) / 'bundle'
        cls.summary = import_old.build(old, cls.out, skip_places=[TEST])
        cls.events = lines(cls.out / 'events.jsonl')
        cls.memories = lines(cls.out / 'memories.jsonl')
        cls.people = lines(cls.out / 'people.jsonl')
        cls.groups = lines(cls.out / 'groups.jsonl')

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_events_kept_with_origin_and_names(self):
        texts = {e['text'] for e in self.events}
        self.assertEqual(texts, {'芒果 和大家约了周末一起打副本', '大家一起看了流星雨', '这周群里很热闹'})
        d1 = next(e for e in self.events if e['id'] == 'old:archive:d1')
        self.assertEqual(d1['origin'], {'where': BUSY, 'people': [fake.MANGO], 'source_ids': ['4001'],
                                        'visibility': 'public'})
        self.assertEqual(d1['names'], ['芒果'])
        self.assertNotIn('⟦', json.dumps(self.events, ensure_ascii=False))

    def test_left_out(self):
        skipped = self.summary['skipped']
        self.assertEqual(skipped['archive.day_line:redline'], 1)                 # wages
        self.assertEqual(skipped['archive.day_line:forgotten_or_revoked'], 1)    # the forgotten person's cat
        self.assertEqual(skipped['archive.day_line:skipped_place'], 1)           # the test group
        self.assertEqual(skipped['archive.day_line:state_expired'], 1)
        self.assertEqual(skipped['archive.lore:state_candidate'], 1)
        for book in ('person', 'self_said', 'diary'):                            # words verbatim / her old heart
            self.assertEqual(skipped['archive.%s:not_imported' % book], 1)
        self.assertEqual(skipped['notebook.self:not_imported'], 1)
        self.assertEqual(skipped['notebook.fact:no_place'], 1)                   # 'global': place unknown
        self.assertEqual(skipped['notebook.fact:forgotten'], 1)
        self.assertEqual(skipped['notebook.rule:state_archived'], 1)
        dump = json.dumps([self.events, self.memories, self.people], ensure_ascii=False)
        for gone in ('工资', '猫', '吉他', '早呀', fake.STAR):
            self.assertNotIn(gone, dump)

    def test_memories(self):
        by_id = {m['id']: m for m in self.memories}
        self.assertEqual(by_id['old:archive:l1']['text'], '歪了：抽卡没抽到想要的')
        self.assertNotIn('又歪了', json.dumps(self.memories, ensure_ascii=False))   # the quote stays behind
        self.assertEqual(by_id['old:notebook:1']['origin']['where'], SMALL)
        social = by_id['old:social:1']['origin']
        self.assertEqual((social['where'], social['visibility']), ('private:' + fake.MANGO, 'private'))

    def test_people_and_groups(self):
        by_key = {(p['place'], p['qq']): p for p in self.people}
        self.assertEqual(set(by_key), {(BUSY, fake.MANGO), (BUSY, fake.LEMON), (SMALL, fake.PEACH)})
        mango = by_key[(BUSY, fake.MANGO)]
        self.assertEqual(mango['stats']['口头禅'], ['哼哼'])                       # red-line phrase dropped
        self.assertEqual(by_key[(BUSY, fake.LEMON)]['style'], '')                 # an opinion, not kept
        self.assertEqual(by_key[(SMALL, fake.PEACH)]['aliases'], ['桃桃'])
        self.assertEqual({g['place'] for g in self.groups}, {BUSY, TEST})         # test group: profile only

    def test_registry_and_manifest(self):
        manifest = json.loads((self.out / 'manifest.json').read_text('utf-8'))
        self.assertEqual(manifest['registry']['rows']['people'], 1)
        self.assertEqual(manifest['replay_registries_found'], 1)
        self.assertNotIn('replay_1', manifest['registry']['imported'])           # not counted unless asked
        self.assertEqual(len(manifest['inputs']['archive']['sha256']), 64)

    def test_replay_registries_when_asked(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path(tmp) / 'old'
            fake.build_old(old)
            s = import_old.build(old, Path(tmp) / 'b', replay_registries=True)
            self.assertEqual(s['registry']['rows']['optout'], 1)
            self.assertEqual(s['registry']['rows']['people'], 2)


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
