"""tools/import_aliases.py --replay: what a replay run left her, merged into the staged data folder
through two gates (the run's made-up test data, the forget registry). Every number, name and
sentence here is made up; the run's "made-up test data" is made up a second time on purpose."""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import forget_registry  # noqa: E402
import impressions  # noqa: E402
import vector_store  # noqa: E402
from tools import import_aliases  # noqa: E402

G1, G2, P1 = 'group:900001', 'group:900002', 'private:10001'
GONE = '10003'                                       # in the registry
TEST = {'private': '880000001', 'group': '880000002', 'probe': '880000004'}   # the run's test people
SECRETS = {'private': '蓝鲸三号', 'group': '青柠七号'}
T = 1_793_000_000.0


def origin(where, people, sids=(), vis='public'):
    return {'where': where, 'people': list(people), 'source_ids': list(sids), 'visibility': vis}


def memory(mid, where, who, text, sids=(), **extra):
    return dict({'id': mid, 'text': text, 'role': 'user', 'ts': T + 60, 'sender_id': who, 'sender_name': '某人',
                 'origin': origin(where, [who], sids or ['s-' + mid], 'private' if where.startswith('private:') else 'public')},
                **extra)


MEMORIES = [
    memory('m1', G1, '10001', '小爱 周末去爬山吗'),
    memory('m2', G1, '10002', '小爱 我家猫好可爱'),
    memory('m3', P1, '10001', '小爱 我在准备一个惊喜'),
    memory('m4', G1, GONE, '小爱 我是被忘掉的那个'),                       # forgotten person
    memory('m5', G2, '10002', '小爱 这句被要求忘掉了', sids=['m-gone']),  # forgotten message
    memory('m6', 'private:' + TEST['private'], TEST['private'], '小爱 我的暗号是' + SECRETS['private']),
    memory('m7', G2, TEST['group'], '小爱 我们群的口令是' + SECRETS['group']),
    memory('m8', G1, '10002', '小爱 有人说过' + SECRETS['private'] + '吗'),    # a real person, the secret
    memory('m9', G1, '10002', '小爱 爬山要带水', links=[{'id': 'm4', 'ts': T, 'weight': 1}, {'id': 'm1', 'ts': T, 'weight': 1}],
           assoc={'m4': 0.5, 'm1': 0.7}),
]
KEPT_MEMORIES = ['m1', 'm2', 'm3', 'm9']


def event(eid, where, people, text, session, sids=()):
    return {'id': eid, 'ts': T + 120, 'session': session, 'title': '编造的事' + eid, 'event_key': 'made-up-' + eid, 'event': text,
            'origin': origin(where, people, sids or ['s-' + eid])}


EVENTS = [
    event('e1', G1, ['10001'], '芒果约大家周末爬山', 'default:GroupMessage:900001'),
    event('e2', G2, [TEST['group']], '有人说了群口令', 'default:GroupMessage:900002'),
    event('e3', P1, ['10001'], '芒果在准备惊喜', 'default:FriendMessage:10001'),
    event('e4', G1, [GONE], '被忘掉的人说了话', 'default:GroupMessage:900001'),
    event('e5', G2, ['10002'], '柠檬提到 %s 这个号' % TEST['probe'], 'default:GroupMessage:900002'),
    event('e6', G2, ['10002', '10004'], '柠檬和桃子聊天', 'default:GroupMessage:900002'),
]
KEPT_EVENTS = ['e1', 'e3', 'e6']

NOTEBOOK = [
    {'id': 'n1', 'text': '想多听听大家在聊什么', 'ts': T, 'origin': origin('self', [], [], 'self')},
    {'id': 'n2', 'text': '有人告诉我一个暗号', 'ts': T, 'origin': origin('private:' + TEST['private'], [TEST['private']], [], 'private')},
    {'id': 'n3', 'text': '柠檬家的猫很可爱', 'ts': T, 'origin': origin(G1, ['10002'])},
    {'id': 'n4', 'text': '那个人好久没来了', 'ts': T, 'origin': origin(G1, [GONE])},
]


def vec(i):
    return [float(i), 0.5, -0.25]


def made_up_run(run):
    """A run folder as tools/replay.py leaves it, with the run's own made-up test data mixed in."""
    data = run / 'data'
    (data / 'memory').mkdir(parents=True)
    (data / 'memory' / 'library.json').write_text(json.dumps(
        {'schema_version': 3, 'rooms': {'default:GroupMessage:900001': {'what': '编造的房间'}}, 'entries': MEMORIES},
        ensure_ascii=False), 'utf-8')
    with vector_store.VectorStore(data / 'memory' / vector_store.FILE_NAME) as store:
        store.put_many({m['id']: vec(i) for i, m in enumerate(MEMORIES, 1)})
    (data / 'archives').mkdir()
    lines = [json.dumps(e, ensure_ascii=False) for e in EVENTS]
    (data / 'archives' / 'events.jsonl').write_text(''.join(x + '\n' for x in lines), 'utf-8')
    for e, line in zip(EVENTS, lines):   # each place's copy, as the plugin appends it
        folder = data / 'archives' / 'sessions' / import_aliases.session_dir(e['session'])
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder / 'events.jsonl', 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    store = impressions.Store(data / 'people')
    rec = lambda qq, name, aliases, style='话不多': {'qq': qq, 'name': name, 'aliases': aliases, 'style': style,  # noqa: E731
                                                     'topics': ['爬山'], 'stats': {'msgs': 3, 'days': 1}, 'since': '2026-10-20',
                                                     'updated': '2026-10-28', 'origin': {}}
    store.save(G1, {'people': {'10001': rec('10001', '芒果', ['小芒']), GONE: rec(GONE, '阿星', ['星星']),
                               TEST['probe']: rec(TEST['probe'], '测试4', [])}, 'tried': {'2026-10-28': 1}})
    store.save(G2, {'people': {'10002': rec('10002', '柠檬', [], style='常说' + SECRETS['group']),
                               '10004': rec('10004', '桃子', ['桃桃'])}})
    for qq, ns in (('10001', ['芒果', '小芒']), (GONE, ['阿星']), (TEST['private'], ['测试1']), ('10004', ['桃子', '桃桃'])):
        store.keep_names(qq, ns)
    (data / 'self_model.json').write_text(json.dumps({'heart': 1, 'who_am_i': '', 'notebook': NOTEBOOK,
                                                      'digest_night': {'x': 1}, '_history': ['编造']}, ensure_ascii=False), 'utf-8')
    # what is not taken
    for rel, body in (('phone/group_900001.json', '{"recent": []}'), ('brain_turns.json', '{"turns": []}'),
                      ('states/her.json', '{}'), ('users/10001.json', '{}'), ('api_config.json', '{"k": "编造"}')):
        (data / rel).parent.mkdir(parents=True, exist_ok=True)
        (data / rel).write_text(body, 'utf-8')
    with forget_registry.ForgetRegistry(data / forget_registry.FILE_NAME) as reg:
        reg.forget_person('10002', stamp=1.0, note='legacy:test')   # the run's own copy: must not be used
    (run / 'canaries.json').write_text(json.dumps({
        'enabled': True, 'people': TEST, 'secrets': SECRETS,
        'rows': [{'place': 'private:' + TEST['private'], 'user_id': TEST['private'], 'ts': T, 'name': '测试1',
                  'message_content': '小爱，跟你说个秘密，我的暗号是' + SECRETS['private']},
                 {'place': G2, 'user_id': TEST['group'], 'ts': T, 'name': '测试2',
                  'message_content': '小爱 我们群的口令是' + SECRETS['group']}]}, ensure_ascii=False), 'utf-8')
    return run


def made_up_bundle(folder):
    folder.mkdir(parents=True)
    with forget_registry.ForgetRegistry(folder / forget_registry.FILE_NAME) as reg:
        reg.forget_person(GONE, stamp=1.0, note='legacy:test')
        reg.forget_message('m-gone', stamp=1.0, note='legacy:test')
        reg.remember_names(GONE, ['阿星'])
    rows = [{'place': G1, 'qq': '10001', 'name': '芒果', 'aliases': ['芒芒'], 'origin': {}}]
    (folder / 'aliases.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), 'utf-8')
    return folder


def tree(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file()}


def run_tool(*args):
    return subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'import_aliases.py'), *map(str, args)],
                          capture_output=True, text=True, encoding='utf-8', timeout=120,
                          env=dict(os.environ, PYTHONIOENCODING='utf-8'))


class Merge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        cls.run_dir = made_up_run(tmp / 'run')
        cls.bundle = made_up_bundle(tmp / 'bundle')
        cls.before = tree(cls.run_dir)
        cls.out = tmp / 'stage' / 'data'
        proc = run_tool('--bundle', cls.bundle, '--replay', cls.run_dir, '--out', cls.out)
        if proc.returncode != 0:
            raise AssertionError(proc.stdout + proc.stderr)
        cls.report = json.loads((cls.out / 'import_aliases.json').read_text('utf-8'))
        cls.lib = json.loads((cls.out / 'memory' / 'library.json').read_text('utf-8'))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def everything(self):
        return '\n'.join(p.read_bytes().decode('utf-8', 'replace') for p in self.out.rglob('*')
                         if p.is_file() and p.suffix != '.sqlite3')

    def test_nothing_of_the_test_data(self):
        text = self.everything()
        for s in list(SECRETS.values()) + list(TEST.values()) + ['测试1', '测试2', '测试4']:
            self.assertNotIn(s, text)
        with vector_store.VectorStore(self.out / 'memory' / vector_store.FILE_NAME) as store:
            self.assertEqual(sorted(store.ids()), KEPT_MEMORIES)

    def test_nothing_the_registry_rules_out(self):
        text = self.everything()
        for s in ('我是被忘掉的那个', '这句被要求忘掉了', '被忘掉的人说了话', '那个人好久没来了', '阿星', '星星'):
            self.assertNotIn(s, text)
        self.assertNotRegex(text, r'(?<![0-9])%s(?![0-9])' % GONE)

    def test_memories_and_only_their_vectors(self):
        self.assertEqual([e['id'] for e in self.lib['entries']], KEPT_MEMORIES)
        self.assertEqual(self.lib['rooms'], {})
        self.assertTrue(all('vector' not in e for e in self.lib['entries']))
        with vector_store.VectorStore(self.out / 'memory' / vector_store.FILE_NAME) as store:
            self.assertEqual(store.get_many(KEPT_MEMORIES),
                             {m['id']: vec(i) for i, m in enumerate(MEMORIES, 1) if m['id'] in KEPT_MEMORIES})
        m9 = self.lib['entries'][-1]
        self.assertEqual([x['id'] for x in m9['links']], ['m1'])   # none to a memory left out
        self.assertEqual(m9['assoc'], {'m1': 0.7})

    def test_events_and_each_places_copy(self):
        archive = [json.loads(x) for x in (self.out / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()]
        self.assertEqual([e['id'] for e in archive], KEPT_EVENTS)
        copies = {}
        for f in (self.out / 'archives' / 'sessions').glob('*/events.jsonl'):
            copies[f.parent.name] = [json.loads(x)['id'] for x in f.read_text('utf-8').splitlines()]
        self.assertEqual(copies, {'default_GroupMessage_900001': ['e1'], 'default_FriendMessage_10001': ['e3'],
                                  'default_GroupMessage_900002': ['e6']})
        # each line as the run wrote it
        run_lines = (self.run_dir / 'data' / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()
        self.assertEqual((self.out / 'archives' / 'events.jsonl').read_text('utf-8').splitlines(),
                         [run_lines[0], run_lines[2], run_lines[5]])

    def test_impressions_on_top_of_the_names_loaded(self):
        store = impressions.Store(self.out / 'people')
        g1, g2 = store.load(G1)['people'], store.load(G2)['people']
        self.assertEqual(sorted(g1), ['10001'])
        self.assertEqual(g1['10001']['aliases'], ['芒芒', '小芒'])   # the bundle's, then the run's
        self.assertEqual(g1['10001']['style'], '话不多')              # the run's impression
        self.assertEqual(sorted(g2), ['10004'])                       # 10002's said the group's secret
        names = json.loads((self.out / 'people' / 'names.json').read_text('utf-8'))
        self.assertEqual(sorted(names), ['10001', '10004'])
        self.assertNotIn('tried', store.load(G1))

    def test_the_notebook_only(self):
        sm = json.loads((self.out / 'self_model.json').read_text('utf-8'))
        self.assertEqual(sorted(sm), ['notebook'])
        self.assertEqual([x['id'] for x in sm['notebook']], ['n1', 'n3'])

    def test_what_is_not_taken(self):
        files = set(tree(self.out))
        for rel in files:
            self.assertFalse(rel.startswith(('phone/', 'states/', 'users/')), rel)
        for rel in ('brain_turns.json', 'api_config.json'):
            self.assertNotIn(rel, files)
        # the registry is the bundle's, not the run's (which forgets 10002)
        self.assertEqual(tree(self.out)[forget_registry.FILE_NAME], tree(self.bundle)[forget_registry.FILE_NAME])

    def test_the_run_is_left_alone(self):
        self.assertEqual(tree(self.run_dir), self.before)

    def test_counts(self):
        m = self.report['replay']['merged']
        self.assertTrue(self.report['replay']['made_up_test_data'])
        self.assertEqual(m['memory'], {'merged': 4, 'forgotten': 2, 'made_up_person': 2, 'made_up_secret': 1})
        self.assertEqual(m['memory_vectors'], {'stored': 4})
        self.assertEqual(m['event'], {'merged': 3, 'forgotten': 1, 'made_up_person': 1, 'made_up_number': 1})
        self.assertEqual(m['event_copies'], {'places': 3})
        self.assertEqual(m['impression'], {'merged': 2, 'forgotten': 1, 'made_up_person': 1, 'made_up_secret': 1})
        self.assertEqual(m['names'], {'merged': 2, 'forgotten': 1, 'made_up_person': 1})
        self.assertEqual(m['notebook'], {'merged': 2, 'forgotten': 1, 'made_up_person': 1})
        text = json.dumps(self.report, ensure_ascii=False)
        for s in list(SECRETS.values()) + list(TEST.values()) + ['10001', GONE, '芒果']:
            self.assertNotIn(s, text)

    def test_without_replay_as_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'plain'
            proc = run_tool('--bundle', self.bundle, '--out', out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertNotIn('replay', json.loads((out / 'import_aliases.json').read_text('utf-8')))
            self.assertEqual(sorted(tree(out)), sorted(['forget_registry.sqlite3', 'import_aliases.json',
                                                        'people/names.json', next(k for k in tree(out) if k.startswith('people/group'))]))


class Refuses(unittest.TestCase):
    def test_no_canaries_or_unreadable_nothing_made(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run = made_up_run(tmp / 'run')
            bundle = made_up_bundle(tmp / 'bundle')
            for case, body in (('missing', None), ('broken', '{not json'), ('empty', '{"enabled": true}')):
                if body is None:
                    (run / 'canaries.json').unlink()
                else:
                    (run / 'canaries.json').write_text(body, 'utf-8')
                out = tmp / ('out-' + case)
                proc = run_tool('--bundle', bundle, '--replay', run, '--out', out)
                self.assertNotEqual(proc.returncode, 0, case)
                self.assertIn('nothing merged', proc.stderr, case)
                self.assertFalse(out.exists(), case)

    def test_not_a_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = made_up_bundle(Path(tmp) / 'bundle')
            out = Path(tmp) / 'out'
            proc = run_tool('--bundle', bundle, '--replay', Path(tmp) / 'nothing', '--out', out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('not a replay run', proc.stderr)
            self.assertFalse(out.exists())


class SameNamesAsThePlugin(unittest.TestCase):
    def test_session_folders(self):
        script = r"""
import sys, json, tempfile
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[1] + '/tests')
import harness
harness.prepare(tempfile.mkdtemp())
import mixin_events, common
out = [mixin_events.EventsMixin._event_session_file(s).relative_to(common.EVENT_SESSION_DIR).parent.as_posix()
       for s in json.loads(sys.argv[2])]
print(json.dumps(out))
"""
        sessions = ['default:GroupMessage:900001', 'default:FriendMessage:10001', '', 'aiocqhttp:Group/Message:1 2', 'x' * 100]
        proc = subprocess.run([sys.executable, '-c', script, str(ROOT), json.dumps(sessions)], capture_output=True,
                              text=True, encoding='utf-8', timeout=120)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout.strip().splitlines()[-1]), [import_aliases.session_dir(s) for s in sessions])


class ThePluginStartsOnIt(unittest.TestCase):
    """The staged folder as the plugin's data folder: it reads the memories, events and notebook,
    and fills in the rest of self_model.json."""

    def test_reads_it(self):
        script = r"""
import sys, json, shutil
root, staged, data = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root + '/tests')
import harness
shutil.copytree(staged, data)
harness.prepare(data)
import main
plugin = main.BioCorePlugin(harness.FakeContext(), config={})
lib = plugin._read_library()
sm = json.loads(open(data + '/self_model.json', encoding='utf-8').read())
print(json.dumps({'memories': sorted(e['id'] for e in lib['entries']),
                  'vectors': sorted(e['id'] for e in lib['entries'] if e.get('vector')),
                  'events': sorted(e['id'] for e in plugin._event_archive(50, read_only=True)),
                  'notebook': [x['id'] for x in plugin.self_model.get('notebook') or []],
                  'self_model_keys': sorted(sm), 'before_heart': __import__('os').path.exists(data + '/self_model.before_heart.json')}))
"""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run = made_up_run(tmp / 'run')
            bundle = made_up_bundle(tmp / 'bundle')
            out = tmp / 'stage'
            proc = run_tool('--bundle', bundle, '--replay', run, '--out', out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            env = dict(os.environ, PYTHONHASHSEED='0', PYTHONIOENCODING='utf-8')
            env.pop('AMS_LIFE_DATA_DIR', None)
            p = subprocess.run([sys.executable, '-c', script, str(ROOT), str(out), str(tmp / 'data')],
                               capture_output=True, text=True, encoding='utf-8', timeout=180, env=env)
            self.assertEqual(p.returncode, 0, p.stderr[-2000:])
            r = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertEqual(r['memories'], KEPT_MEMORIES)
        self.assertEqual(r['vectors'], KEPT_MEMORIES)
        self.assertEqual(r['events'], KEPT_EVENTS)
        self.assertEqual(r['notebook'], ['n1', 'n3'])
        for key in ('who_am_i', 'boundaries', 'consistency', 'narrative', 'notebook', 'heart', 'version'):
            self.assertIn(key, r['self_model_keys'])
        # no "heart": 1 in the staged file: at its first start the plugin keeps a copy of it
        # (self_model.before_heart.json) and goes on with the notebook as it is
        self.assertTrue(r['before_heart'])


if __name__ == '__main__':
    unittest.main()
