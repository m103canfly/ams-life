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
FORMER = '10009'                                     # on the --exclude-people list (her former account)
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
    memory('m10', G1, FORMER, '小爱 我是她以前的号'),
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
    dict(event('e6', G2, ['10002', '10004'], '柠檬和桃子聊天', 'default:GroupMessage:900002'),
         links=[{'id': 'e5', 'weight': 1.0}, {'id': 'e1', 'weight': 0.5}]),
    event('e7', G1, [FORMER], '以前的号说了话', 'default:GroupMessage:900001'),
]
KEPT_EVENTS = ['e1', 'e3', 'e6']

NOTEBOOK = [
    {'id': 'n1', 'text': '想多听听大家在聊什么', 'ts': T, 'origin': origin('self', [], [], 'self')},
    {'id': 'n2', 'text': '有人告诉我一个暗号', 'ts': T, 'origin': origin('private:' + TEST['private'], [TEST['private']], [], 'private')},
    {'id': 'n3', 'text': '柠檬家的猫很可爱', 'ts': T, 'origin': origin(G1, ['10002'])},
    {'id': 'n4', 'text': '那个人好久没来了', 'ts': T, 'origin': origin(G1, [GONE])},
]


def user(qq, name, milestones=(), maps=None, sessions=('default:GroupMessage:900001',)):
    rel = {'state': 'friendly', 'trajectory': 0.2, 'we_memory': [], 'annotations': [], 'milestones': list(milestones),
           'transactive_map': {}, 'destination_map': {}, 'social_world': []}
    rel.update(maps or {})
    return {'sender_id': qq, 'sender_name': name, 'names': [name], 'interactions': 7, 'trust': 0.6,
            'sessions': list(sessions), 'relationship': rel}


USERS = {
    '10001': user('10001', '芒果', [{'text': '一起去爬山', 'source_ids': ['s1']}]),                  # nothing to clean
    '10002': user('10002', '柠檬', [{'text': '一起去爬山', 'source_ids': ['s1']},
                                  {'text': '测试2 说了口令', 'source_ids': ['s2']},                  # a made-up name
                                  {'text': '没说从哪来的'}],                                          # no source
                  {'destination_map': {TEST['group']: {'sender_id': TEST['group'], 'count': 2, 'latest_text': '你好'}},
                   'social_world': ['群里的朋友']}),
    '10005': user('10005', '小鱼', [{'text': '阿星今天没来', 'source_ids': ['s5']},                    # someone deleted
                                  {'text': '小鱼爱钓鱼', 'source_ids': ['s6']}]),
    '10004': user('10004', '桃子', sessions=('default:GroupMessage:900002', 'default:FriendMessage:' + TEST['private'])),
    GONE: user(GONE, '阿星'),
    TEST['private']: user(TEST['private'], '测试1'),
    FORMER: user(FORMER, '旧号'),
}


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
                               TEST['probe']: rec(TEST['probe'], '测试4', []), FORMER: rec(FORMER, '旧号', [])},
                    'tried': {'2026-10-28': 1}})
    store.save(G2, {'people': {'10002': rec('10002', '柠檬', [], style='常说' + SECRETS['group']),
                               '10004': rec('10004', '桃子', ['桃桃'])}})
    for qq, ns in (('10001', ['芒果', '小芒']), (GONE, ['阿星']), (TEST['private'], ['测试1']), ('10004', ['桃子', '桃桃']),
                   (FORMER, ['旧号'])):
        store.keep_names(qq, ns)
    (data / 'self_model.json').write_text(json.dumps({'heart': 1, 'who_am_i': '', 'notebook': NOTEBOOK,
                                                      'digest_night': {'x': 1}, '_history': ['编造']}, ensure_ascii=False), 'utf-8')
    # what is not taken
    for rel, body in (('phone/group_900001.json', '{"recent": []}'), ('brain_turns.json', '{"turns": []}'),
                      ('states/her.json', '{}'), ('api_config.json', '{"k": "编造"}')):
        (data / rel).parent.mkdir(parents=True, exist_ok=True)
        (data / rel).write_text(body, 'utf-8')
    (data / 'users').mkdir()
    for qq, body in USERS.items():
        (data / 'users' / (qq + '.json')).write_text(json.dumps(body, ensure_ascii=False, indent=1), 'utf-8')
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


def exclude_list(folder, people=(FORMER,)):
    path = folder / 'exclude-people.txt'
    path.write_text('# her former account, made up\n' + ''.join(p + '\n' for p in people), 'utf-8')
    return path


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
        proc = run_tool('--bundle', cls.bundle, '--replay', cls.run_dir, '--exclude-people', exclude_list(tmp),
                        '--out', cls.out)
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
        for s in list(SECRETS.values()) + list(TEST.values()) + ['测试1', '测试2', '测试4', FORMER, '旧号']:
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
        # each line as the run wrote it, but links to an event left out
        run_lines = (self.run_dir / 'data' / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()
        out_lines = (self.out / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()
        self.assertEqual(out_lines[:2], [run_lines[0], run_lines[2]])
        self.assertEqual(json.loads(out_lines[2])['links'], [{'id': 'e1', 'weight': 0.5}])
        self.assertEqual(dict(json.loads(out_lines[2]), links=None), dict(json.loads(run_lines[5]), links=None))

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
        self.assertEqual(sorted(sm), ['heart', 'notebook'])   # "heart": 1, so no copy is kept at her first start
        self.assertEqual(sm['heart'], 1)
        self.assertEqual([x['id'] for x in sm['notebook']], ['n1', 'n3'])

    def test_what_is_not_taken(self):
        files = set(tree(self.out))
        for rel in files:
            self.assertFalse(rel.startswith(('phone/', 'states/')), rel)
        for rel in ('brain_turns.json', 'api_config.json'):
            self.assertNotIn(rel, files)
        # the registry is the bundle's, not the run's (which forgets 10002)
        self.assertEqual(tree(self.out)[forget_registry.FILE_NAME], tree(self.bundle)[forget_registry.FILE_NAME])

    def test_the_run_is_left_alone(self):
        self.assertEqual(tree(self.run_dir), self.before)

    def test_counts(self):
        m = self.report['replay']['merged']
        self.assertTrue(self.report['replay']['made_up_test_data'])
        self.assertEqual(m['memory'], {'merged': 4, 'forgotten': 2, 'made_up_person': 2, 'made_up_secret': 1,
                                       'excluded_person': 1})
        self.assertEqual(m['memory_vectors'], {'stored': 4})
        self.assertEqual(m['event'], {'merged': 3, 'forgotten': 1, 'made_up_person': 1, 'made_up_number': 1,
                                      'excluded_person': 1})
        self.assertEqual(m['event_copies'], {'places': 3})
        self.assertEqual(m['impression'], {'merged': 2, 'forgotten': 1, 'made_up_person': 1, 'made_up_secret': 1,
                                           'excluded_person': 1})
        self.assertEqual(m['names'], {'merged': 2, 'forgotten': 1, 'made_up_person': 1, 'excluded_person': 1})
        self.assertEqual(m['users'], {'merged': 1, 'cleaned': 2, 'still_draws_from_someone_left_out': 1,
                                      'forgotten': 1, 'made_up_person': 1, 'excluded_person': 1})
        self.assertEqual(self.report['replay']['excluded_people'], 1)
        self.assertEqual(m['notebook'], {'merged': 2, 'forgotten': 1, 'made_up_person': 1})
        text = json.dumps(self.report, ensure_ascii=False)
        for s in list(SECRETS.values()) + list(TEST.values()) + ['10001', GONE, FORMER, '芒果']:
            self.assertNotIn(s, text)

    def test_relationship_records(self):
        users = self.out / 'users'
        self.assertEqual(sorted(p.name for p in users.iterdir()), ['10001.json', '10002.json', '10005.json'])
        # nothing to clean: the file as it was
        self.assertEqual((users / '10001.json').read_bytes(), (self.run_dir / 'data' / 'users' / '10001.json').read_bytes())
        for qq, kept in (('10002', ['一起去爬山']), ('10005', ['小鱼爱钓鱼'])):
            rec = json.loads((users / (qq + '.json')).read_text('utf-8'))
            rel, was = rec['relationship'], USERS[qq]['relationship']
            self.assertEqual([x['text'] for x in rel['milestones']], kept)          # what drew from them, or says no source
            self.assertEqual((rel['transactive_map'], rel['destination_map'], rel['social_world']), ({}, {}, []))
            self.assertEqual((rel['state'], rel['trajectory'], rec['interactions'], rec['trust']),
                             (was['state'], was['trajectory'], 7, 0.6))              # the numbers stay
        text = ''.join(p.read_text('utf-8') for p in users.iterdir())
        for s in list(SECRETS.values()) + list(TEST.values()) + ['测试1', '测试2', FORMER, GONE, '阿星']:
            self.assertNotIn(s, text)

    def test_without_replay_as_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'plain'
            proc = run_tool('--bundle', self.bundle, '--out', out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertNotIn('replay', json.loads((out / 'import_aliases.json').read_text('utf-8')))
            self.assertEqual(sorted(tree(out)), sorted(['forget_registry.sqlite3', 'import_aliases.json',
                                                        'people/names.json', next(k for k in tree(out) if k.startswith('people/group'))]))


class EmptyList(unittest.TestCase):
    def test_nobody_on_it_nobody_left_out_for_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run, bundle = made_up_run(tmp / 'run'), made_up_bundle(tmp / 'bundle')
            out = tmp / 'out'
            proc = run_tool('--bundle', bundle, '--replay', run, '--exclude-people', exclude_list(tmp, ()), '--out', out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            lib = json.loads((out / 'memory' / 'library.json').read_text('utf-8'))
            self.assertIn('m10', [e['id'] for e in lib['entries']])
            self.assertTrue((out / 'users' / (FORMER + '.json')).is_file())
            self.assertNotIn('excluded_person', json.dumps(json.loads((out / 'import_aliases.json').read_text('utf-8'))))

    def test_the_list_needs_replay_and_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run, bundle = made_up_run(tmp / 'run'), made_up_bundle(tmp / 'bundle')
            bad = tmp / 'bad.txt'
            bad.write_text('不是号码\n', 'utf-8')
            for args, said in ((('--exclude-people', exclude_list(tmp)), 'goes with --replay'),
                               (('--replay', run, '--exclude-people', tmp / 'nothing.txt'), 'no list'),
                               (('--replay', run, '--exclude-people', bad), 'one number a line')):
                out = tmp / ('out-' + said.split()[0])
                proc = run_tool('--bundle', bundle, *args, '--out', out)
                self.assertNotEqual(proc.returncode, 0, said)
                self.assertIn(said, proc.stderr)
                self.assertFalse(out.exists(), said)


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


class SameRulesAsThePlugin(unittest.TestCase):
    """The relationship-record rules, the plugin's own (mixin_discretion, mixin_people) and the tool's."""

    def test_mentions_and_file_names(self):
        script = r"""
import sys, json, tempfile
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[1] + '/tests')
import harness
harness.prepare(tempfile.mkdtemp())
import mixin_discretion, mixin_people
D = mixin_discretion.DiscretionMixin
cases = json.loads(sys.argv[2])
class Who:
    def __init__(self, sid): self.sid = sid
    def _speaker(self, event): return self.sid, ''
print(json.dumps({'mentions': [D._record_mentions(D, rec, person, names) for rec, person, names in cases['mentions']],
                  'files': [mixin_people.PeopleMixin._user_path(Who(q), None).name for q in cases['files']],
                  'consts': [list(D._REL_TEXT_LISTS), list(D._REL_TEXT_MAPS), sorted(D._EVERYDAY_WORDS)]}))
"""
        ms = [(USERS['10002'], TEST['group'], ['测试2']), (USERS['10002'], '10001', ['芒果']),
              (USERS['10005'], GONE, ['阿星']), (USERS['10005'], GONE, []), (USERS['10001'], GONE, ['阿星']),
              (user('1', '甲', [{'text': '大家 好', 'source_ids': ['x']}]), '2', ['大家']),
              (user('1', '甲', [{'text': '%s 来了' % GONE}]), GONE, []),
              (user('1', '甲', maps={'transactive_map': {GONE: '他知道'}}), GONE, [])]
        files = ['10001', 'a:b/c', 'x' * 80, '']
        proc = subprocess.run([sys.executable, '-c', script, str(ROOT), json.dumps({'mentions': ms, 'files': files})],
                              capture_output=True, text=True, encoding='utf-8', timeout=120)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        r = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(r['mentions'], [import_aliases.record_mentions(*c) for c in ms])
        self.assertEqual(r['mentions'], [True, False, True, False, False, False, True, True])
        self.assertEqual(r['files'], [import_aliases.user_file(q) for q in files])
        self.assertEqual(r['consts'], [list(import_aliases.REL_TEXT_LISTS), list(import_aliases.REL_TEXT_MAPS),
                                       sorted(import_aliases.EVERYDAY_WORDS)])


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
                  'self_model_keys': sorted(plugin.self_model), 'file_keys': sorted(sm), 'before_heart': __import__('os').path.exists(data + '/self_model.before_heart.json')}))
"""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run = made_up_run(tmp / 'run')
            bundle = made_up_bundle(tmp / 'bundle')
            out = tmp / 'stage'
            proc = run_tool('--bundle', bundle, '--replay', run, '--exclude-people', exclude_list(tmp), '--out', out)
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
        # "heart": 1 in the staged file: no copy of it is kept at her first start (no delete would reach it)
        self.assertFalse(r['before_heart'])


if __name__ == '__main__':
    unittest.main()
