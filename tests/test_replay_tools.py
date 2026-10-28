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
from tools import audit_replay, import_old  # noqa: E402


def run_replay(chat, registry, out, *extra):
    env = dict(os.environ, PYTHONHASHSEED='0')
    env.pop('AMS_LIFE_DATA_DIR', None)
    proc = subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'replay.py'), '--chat', str(chat),
                           '--registry', str(registry), '--out', str(out), *extra],
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
        self.assertEqual(s['skipped_optout'], 2)          # and after ("forget me" read as "not again"), canary too
        self.assertEqual(s['skipped_source'], 1)          # the one forgotten message
        self.assertEqual(s['quote_of_forgotten_dropped'], 1)
        self.assertEqual(s['forget_me'], 1)               # the canary who asked
        self.assertEqual(s['her_messages_used_as_replies'], 7)
        self.assertNotIn('her_unprompted_skipped', s)
        self.assertEqual(s['requests'], 7 + 7)            # 7 from the log, 7 canary requests (one came after "forget me")

    def test_nothing_left_the_folder(self):
        self.assertTrue((self.out / 'data' / 'memory' / 'library.json').exists())
        # the registry given to the replay is not changed; its copy got the canary
        import forget_registry
        with forget_registry.ForgetRegistry(self.registry) as reg:
            self.assertEqual(reg.stats()['people'], 1)
        with forget_registry.ForgetRegistry(self.out / 'forget_registry.sqlite3') as reg:
            self.assertEqual(reg.stats()['people'], 2)

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

    def test_cutoff_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_replay(self.chat, self.registry, Path(tmp) / 'r', '--forget-me', 'cutoff', '--no-canaries')
            stats = json.loads((Path(tmp) / 'r' / 'replay.json').read_text('utf-8'))['stats']
            self.assertNotIn('skipped_optout', stats)      # what he said after asking is kept
            self.assertEqual(stats['skipped_forgotten'], 1)
            self.assertTrue(audit_replay.audit(Path(tmp) / 'r', self.chat)['pass'])


if __name__ == '__main__':
    unittest.main()
