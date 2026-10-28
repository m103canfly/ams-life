"""tools/replay.py and tools/audit_replay.py on a made-up chat log.

The replay runs in a fresh interpreter (it freezes the clock and imports the plugin, like the
golden test). Then the audit must pass; and an audit of a replay with a planted leak must fail.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import fake_old_data as fake  # noqa: E402
from tools import _guard, audit_replay, import_old  # noqa: E402


def run_replay(chat, registry, out, *extra):
    env = dict(os.environ, PYTHONHASHSEED='0')
    env.pop('AMS_LIFE_DATA_DIR', None)
    reg = ['--registry', str(registry)] if registry else []
    proc = subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'replay.py'), '--chat', str(chat),
                           *reg, '--out', str(out), *extra],
                          env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
    if proc.returncode != 0:
        raise AssertionError('replay failed:\n%s\n%s' % (proc.stdout, proc.stderr))
    return json.loads(proc.stdout.strip().splitlines()[-1])


class Replay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        fake.build_old(tmp / 'old')
        import_old.build(tmp / 'old', tmp / 'bundle')
        cls.chat = fake.build_chat(tmp / 'chat.db')
        cls.registry = tmp / 'bundle' / 'forget_registry.sqlite3'
        cls.out = tmp / 'replay'
        cls.printed = run_replay(cls.chat, cls.registry, cls.out)
        cls.stats = json.loads((cls.out / 'replay.json').read_text('utf-8'))['stats']
        cls.prompts = [json.loads(x) for x in (cls.out / 'prompts.jsonl').read_text('utf-8').splitlines() if x]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_what_was_fed_in(self):
        s = self.stats
        self.assertEqual(s['skipped_forgotten'], 1)       # his message before he asked
        self.assertEqual(s['skipped_optout'], 1)          # and after (his forget row read as "not again")
        self.assertEqual(s['skipped_source'], 1)          # the one forgotten message
        self.assertEqual(s['quote_of_forgotten_dropped'], 1)
        self.assertEqual(s['her_messages_used_as_replies'], 7)
        self.assertNotIn('her_unprompted_skipped', s)
        self.assertEqual(s['requests'], 7 + 5)            # 7 from the log, 5 canary requests

    def test_nothing_left_the_folder(self):
        self.assertTrue((self.out / 'data' / 'memory' / 'library.json').exists())
        import forget_registry
        with forget_registry.ForgetRegistry(self.out / 'forget_registry.sqlite3') as reg:
            self.assertEqual(reg.stats()['people'], 1)

    def test_her_replies_are_not_remembered(self):
        lib = json.loads((self.out / 'data' / 'memory' / 'library.json').read_text('utf-8'))
        self.assertEqual([e for e in lib['entries'] if e.get('role') == 'assistant'], [])

    def test_audit_passes(self):
        result = audit_replay.audit(self.out, self.chat)
        self.assertTrue(result['pass'], json.dumps(result['checks'], ensure_ascii=False, indent=1))
        self.assertGreater(result['prompts']['reply'], 0)

    def test_audit_catches_a_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            busy = 'group:' + fake.G_BUSY
            with open(bad / 'prompts.jsonl', 'a', encoding='utf-8') as f:
                for text in ('她记得：' + fake.PRIVATE_SECRET, '她记得蓝鲸三号', '她记得我家猫今天把杯子打碎了',
                             '提到 ' + fake.LEMON, '小鱼说想去旅游'):
                    f.write(json.dumps({'kind': 'reply', 'ts': fake.T0 + 9000, 'place': busy, 'text': text},
                                       ensure_ascii=False) + '\n')
            with open(bad / 'data' / 'leftover.json', 'w', encoding='utf-8') as f:
                f.write('{"who": "%s"}' % fake.STAR)
            checks = audit_replay.audit(bad, self.chat)['checks']
            for name in ('private', 'canaries', 'forgotten', 'qq', 'names'):
                self.assertFalse(checks[name]['pass'], name)
            self.assertEqual(checks['forgotten']['fails'], 2)    # the cat in a prompt, his number in a file

    def plant(self, tmp, prompts):
        bad = Path(tmp) / 'bad'
        shutil.copytree(self.out, bad)
        with open(bad / 'prompts.jsonl', 'a', encoding='utf-8') as f:
            for kind, place, text in prompts:
                f.write(json.dumps({'kind': kind, 'ts': fake.T0 + 9000, 'place': place, 'text': text},
                                   ensure_ascii=False) + '\n')
        return bad

    def test_her_own_private_words_count_as_private(self):
        # what she said in a private chat (e.g. repeating him) must not turn up in a group either
        with tempfile.TemporaryDirectory() as tmp:
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得：' + fake.HER_PRIVATE_REPLY)])
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertFalse(checks['private']['pass'])
            self.assertEqual(checks['private']['examples'][-1]['came_from'], '私聊1')

    def test_names_in_private_prompts_and_numbers_in_every_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = self.plant(tmp, [('reply', 'private:' + fake.MANGO, '小鱼说想去旅游'),
                                   ('model', 'group:' + fake.G_BUSY, '整理：' + fake.PEACH + ' 说了什么')])
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertTrue(any(e['place'] == '私聊1' for e in checks['names']['examples']))
            self.assertEqual(checks['qq']['fails'], 1)
            self.assertEqual(checks['qq']['examples'][0]['kind'], 'model')

    def test_refuses_a_live_folder_and_says_what_it_cannot_see(self):
        with tempfile.TemporaryDirectory() as tmp:
            live = Path(tmp) / 'AstrBot' / 'data' / 'replay'
            shutil.copytree(self.out, live)
            (live / 'audit.json').unlink(missing_ok=True)
            with self.assertRaises(_guard.Refused):
                audit_replay.audit(live, self.chat)
            self.assertFalse((live / 'audit.json').exists())
        limits = audit_replay.audit(self.out, self.chat)['limits']
        self.assertTrue(any('short' in x for x in limits) and any('fake model' in x for x in limits))

    def test_old_forgets_let_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_replay(self.chat, '', Path(tmp) / 'r', '--old-forgets', 'let-in', '--no-canaries')
            stats = json.loads((Path(tmp) / 'r' / 'replay.json').read_text('utf-8'))['stats']
            self.assertFalse([k for k in stats if k.startswith('skipped_') and k != 'skipped_empty'])
            result = audit_replay.audit(Path(tmp) / 'r', self.chat)
            self.assertTrue(result['pass'], json.dumps(result['checks'], ensure_ascii=False, indent=1))
            self.assertIn('skipped', result['checks']['forgotten'])

    def test_cutoff_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_replay(self.chat, self.registry, Path(tmp) / 'r', '--forget-me', 'cutoff', '--no-canaries')
            stats = json.loads((Path(tmp) / 'r' / 'replay.json').read_text('utf-8'))['stats']
            self.assertNotIn('skipped_optout', stats)      # what he said after asking is kept
            self.assertEqual(stats['skipped_forgotten'], 1)
            result = audit_replay.audit(Path(tmp) / 'r', self.chat)
            self.assertTrue(result['pass'], json.dumps(result['checks'], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    unittest.main()
