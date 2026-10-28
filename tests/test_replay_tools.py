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

    def test_the_plugin_checks_the_registry_too(self):
        import forget_registry
        with forget_registry.ForgetRegistry(self.out / 'data' / forget_registry.FILE_NAME) as reg,                 forget_registry.ForgetRegistry(self.registry) as bundle:
            self.assertEqual([r['kind'] for r in reg.rows()], [r['kind'] for r in bundle.rows()])
            self.assertTrue(reg.rows())

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

    def test_numbers_of_the_old_account_and_the_groups_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得 @某人(%s) 说过' % fake.BOT),
                                   ('model', 'group:' + fake.G_BUSY, '群 %s 的事' % fake.G_SMALL)])
            self.assertEqual(audit_replay.audit(bad, self.chat)['checks']['qq']['fails'], 2)

    def test_pieces_never_across_two_lines_or_two_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            # his forgotten words, cut in two: across two lines of a prompt, two fields of a file
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得我家猫今\n天把杯子打碎了')])
            (bad / 'data' / 'split.json').write_text(json.dumps(['我家猫今天把', '杯子打碎了'], ensure_ascii=False),
                                                     'utf-8')
            self.assertTrue(audit_replay.audit(bad, self.chat)['checks']['forgotten']['pass'])
            # in one line, in one field: caught
            (bad / 'data' / 'whole.json').write_text(json.dumps({'t': '他说我家猫今天把杯子打碎了'}, ensure_ascii=False),
                                                     'utf-8')
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertEqual(checks['forgotten']['examples'], [{'file': 'whole.json'}])

    def test_digits_count_unless_part_of_a_known_number(self):
        import sqlite3
        with tempfile.TemporaryDirectory() as tmp:
            # a phone number said only in a private chat, then in a group's prompt
            chat = Path(tmp) / 'chat.db'
            shutil.copyfile(self.chat, chat)
            from contextlib import closing
            with closing(sqlite3.connect(str(chat))) as db:
                db.execute("INSERT INTO messages (id, message_id, self_id, user_id, group_id, message_type, sub_type, "
                           "post_type, raw_message, message_content, sender_info, timestamp, direction, connection_id, "
                           "processed, created_at) VALUES (9999, '9999', ?, ?, NULL, 'private', 'friend', 'message', "
                           "'13812345678', '13812345678', '{}', ?, 'RECV', 'conn', 1, '2026-10-04 00:00:00')",
                           (fake.BOT, fake.MANGO, int(fake.T0 + 100)))
                db.commit()
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得有人的号码是13812345678')])
            self.assertFalse(audit_replay.audit(bad, chat)['checks']['private']['pass'])
        # digits of a known number stay the qq check's
        self.assertEqual(audit_replay.number_pieces(['9876543210']), {'98765432', '87654321', '76543210'})

    def test_what_astrbot_sends_the_model_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            with open(bad / 'prompts.jsonl', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'kind': 'reply', 'ts': fake.T0 + 9000, 'place': 'group:' + fake.G_BUSY,
                                    'who': fake.MANGO, 'text': '你是小爱。',
                                    'asked': ' @柠檬(%s) 一起玩' % fake.LEMON}, ensure_ascii=False) + '\n')
            self.assertEqual(audit_replay.audit(bad, self.chat)['checks']['qq']['fails'], 1)

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



class AstrBotMessage(unittest.TestCase):
    """What the replay hands the plugin: a QQ message as AstrBot 4.29.3 makes it."""

    def test_as_astrbot_writes_it(self):
        from tools import replay
        sys.path.insert(0, str(HERE / 'stubs'))
        import astrbot.api.message_components as comps
        raw = ('[CQ:reply,id=77][CQ:at,qq=20002,name=小爱] 你好 [CQ:at,qq=10004,name=桃] 在吗 '
               '[CQ:image,file=a.jpg,url=http://x.test/a.jpg][CQ:at,qq=all]')
        text, parts = replay.astrbot_message(raw, '20002', {'10004': '桃子'}, comps)
        self.assertEqual(text, '你好 @桃子(10004) 在吗')        # the first @ of her is left out
        self.assertEqual([type(p).__name__ for p in parts], ['Reply', 'At', 'Plain', 'At', 'Plain', 'Image', 'At'])
        self.assertEqual(parts[3].name, '桃子')                 # the name he writes under
        text, _ = replay.astrbot_message('[CQ:at,qq=20002][CQ:at,qq=20002] 哈哈', '20002', {}, comps)
        self.assertEqual(text, ' @(20002) 哈哈')                 # a second @ of her in the same run stays
        # group cards with a space and with brackets (of people who never wrote: the name in the @)
        text, _ = replay.astrbot_message('明天叫上 [CQ:at,qq=10077,name=Tom Lee] 和 [CQ:at,qq=10078,name=小明（学生）] 一起',
                                         '20002', {}, comps)
        self.assertEqual(text, '明天叫上 @Tom Lee(10077) 和 @小明（学生）(10078) 一起')

    def test_a_quote_as_astrbot_makes_it(self):
        from tools import replay
        sys.path.insert(0, str(HERE / 'stubs'))
        import astrbot.api.message_components as comps
        hers = {'message_id': '81', 'sent': True, 'user_id': '', 'name': '小爱', 'ts': 5.0,
                'raw_message': '好呀', 'message_content': '好呀'}
        reply = replay.astrbot_reply(hers, '20002', {}, comps)
        self.assertEqual((reply.id, reply.sender_id, reply.message_str), ('81', '20002', '好呀'))  # quoting her wakes her
        self.assertEqual([type(p).__name__ for p in reply.chain], ['Plain'])


class EmbedStub:
    """A vector service on this computer for the test: fake vectors, counts its requests."""

    def __init__(self):
        import http.server
        import threading
        import harness
        stub = self
        self.requests = 0

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                stub.requests += 1
                out = json.dumps({'data': [{'embedding': harness.fake_vector(t)} for t in body['input']]}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(out)))
                self.end_headers()
                self.wfile.write(out)

            def log_message(self, *a):
                pass
        self.server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
        self.url = 'http://127.0.0.1:%d/v1/embeddings' % self.server.server_port
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class ReplayOptions(unittest.TestCase):
    """--aliases, --embed-url (a vector service on this computer, nothing else reachable),
    --impressions (the nightly impressions, answered by the fake model)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        fake.build_old(tmp / 'old')
        import_old.build(tmp / 'old', tmp / 'bundle')
        # one evening in the small group: 桃子 says a dozen things from 23:00 on
        night = fake.T0 - (fake.T0 + 8 * 3600) % 86400 + 23 * 3600
        rows = []
        for i in range(13):
            who = fake.PEACH if i < 12 else fake.MANGO
            text = '今天的副本真的好难打第%d次' % i if i < 12 else '@小爱 晚上好呀'
            info = json.dumps({'user_id': int(who), 'nickname': fake.NAMES[who], 'card': fake.NAMES[who]},
                              ensure_ascii=False)
            raw = ('[CQ:at,qq=%s] ' % fake.BOT if i == 12 else '') + text
            rows.append((i + 1, str(9100 + i), fake.BOT, who, fake.G_SMALL, 'group', 'normal', 'message', raw, text,
                         info, int(night + i * 200), 'RECV', 'conn', 1, '2026-10-04 00:00:00'))
        cls.chat = tmp / 'night.db'
        fake._db(cls.chat, fake.LOG_SCHEMA, [('messages', rows)])
        cls.stub = EmbedStub()
        cls.out = tmp / 'replay'
        run_replay(cls.chat, tmp / 'bundle' / 'forget_registry.sqlite3', cls.out, '--no-canaries',
                   '--aliases', str(tmp / 'bundle' / 'aliases.jsonl'), '--embed-url', cls.stub.url, '--impressions')
        cls.summary = json.loads((cls.out / 'replay.json').read_text('utf-8'))
        cls.stats = cls.summary['stats']

    @classmethod
    def tearDownClass(cls):
        cls.stub.close()
        cls.tmp.cleanup()

    def test_aliases_first(self):
        self.assertEqual(self.stats['aliases_people'], 1)
        names = json.loads((self.out / 'data' / 'people' / 'names.json').read_text('utf-8'))
        self.assertEqual(names[fake.PEACH], ['桃子', '桃桃'])

    def test_vectors_from_the_local_service_only(self):
        self.assertGreater(self.stats['embed_requests'], 0)
        self.assertEqual(self.stats['embed_requests'], self.stub.requests)
        self.assertEqual((self.stats['network_refused'], self.summary['refused_hosts']), (0, []))

    def test_impressions_run_with_the_fake_model(self):
        self.assertEqual(self.stats['impression_calls'], 1)
        self.assertGreaterEqual(self.stats['model_calls_fake'], 1)
        files = [json.loads(p.read_text('utf-8')) for p in (self.out / 'data' / 'people').glob('group*.json')]
        self.assertEqual([f['people'][fake.PEACH]['style'] for f in files], ['说话简短，爱接话'])
        result = audit_replay.audit(self.out, self.chat)
        self.assertTrue(result['pass'], json.dumps(result['checks'], ensure_ascii=False, indent=1))

    @unittest.skipUnless((ROOT / 'mixin_digest.py').exists(), 'the daily digest is not in this plugin yet')
    def test_digest_then_impressions_then_notebook(self):
        stub = EmbedStub()   # its own: the class's stub counts the class's replay
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'nightly'
            try:
                run_replay(self.chat, Path(self.tmp.name) / 'bundle' / 'forget_registry.sqlite3', out, '--no-canaries',
                           '--embed-url', stub.url, '--digest', '--impressions', '--notebook')
            finally:
                stub.close()
            stats = json.loads((out / 'replay.json').read_text('utf-8'))['stats']
            self.assertEqual((stats['digest_calls'], stats['digest_events']), (1, 1))
            self.assertEqual(stats['model_calls_fake_daily_digest'], 1)
            calls = [json.loads(x).get('call') for x in (out / 'prompts.jsonl').read_text('utf-8').splitlines()
                     if json.loads(x)['kind'] == 'model']
            nightly = [c for c in calls if c in ('daily_digest', 'group_impressions', 'notebook')]
            self.assertEqual(nightly[:3], ['daily_digest', 'group_impressions', 'notebook'])
            # the note of a window is recorded as that window's (what the audit checks it against)
            places = {json.loads(x)['place'] for x in (out / 'prompts.jsonl').read_text('utf-8').splitlines()
                      if json.loads(x).get('call') == 'daily_digest'}
            self.assertEqual(places, {'group:' + fake.G_SMALL})
            evs = [json.loads(x) for x in (out / 'data' / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()]
            self.assertEqual([(e['kind'], e['origin']['where'], e['origin']['visibility']) for e in evs],
                             [('daily_digest', 'group:' + fake.G_SMALL, 'public')])
            result = audit_replay.audit(out, self.chat)
            self.assertTrue(result['pass'], json.dumps(result['checks'], ensure_ascii=False, indent=1))

    def test_only_a_service_on_this_computer(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'replay.py'), '--chat', str(self.chat),
                                   '--old-forgets', 'let-in', '--out', str(Path(tmp) / 'r'),
                                   '--embed-url', 'http://example.org/v1/embeddings'],
                                  capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(proc.returncode, 2)
            self.assertFalse((Path(tmp) / 'r').exists())

    def test_everything_else_is_refused(self):
        code = '\n'.join([
            'import sys, urllib.request; sys.path.insert(0, sys.argv[1]); from tools import replay',
            'refused = replay.guard_network(set())',
            'try:',
            '    urllib.request.urlopen("http://example.org/", timeout=2)',
            'except OSError:',
            '    pass',
            'print(len(refused))'])
        proc = subprocess.run([sys.executable, '-I', '-c', code, str(ROOT)], capture_output=True, text=True, timeout=60)
        self.assertGreater(int(proc.stdout.strip()), 0, proc.stderr)

    def test_connections_let_through_are_counted_by_name(self):
        code = '\n'.join([
            'import collections, sys, urllib.request; sys.path.insert(0, sys.argv[1]); from tools import replay',
            'port = int(sys.argv[2]); used = collections.Counter()',
            'refused = replay.guard_network({("localhost", port)}, used)',
            'req = urllib.request.Request("http://localhost:%d/v1/embeddings" % port, data=b\'{"input": ["a"]}\')',
            'urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=5).read()',
            'print(dict(used), len(refused))'])
        stub = EmbedStub()   # its own: the replay's stub counts the replay's requests
        try:
            port = stub.server.server_port
            proc = subprocess.run([sys.executable, '-I', '-c', code, str(ROOT), str(port)],
                                  capture_output=True, text=True, timeout=60)
        finally:
            stub.close()
        used, refused = proc.stdout.strip().rsplit(' ', 1)
        # under the name asked for (each address it resolves to that was tried counts)
        self.assertEqual((list(eval(used)), refused, stub.requests), (['localhost:%d' % port], '0', 1), proc.stderr)


KEY = 'sk-made-up-key-0000'


def made_up_astrbot(folder):
    """An AstrBot data folder with one made-up chat provider and persona."""
    import sqlite3
    folder.mkdir()
    (folder / 'cmd_config.json').write_text(json.dumps({
        'provider': [{'id': 'emb', 'type': 'openai_embedding', 'enable': True},
                     {'id': 'ds/flash', 'enable': True, 'provider_source_id': 'ds', 'model': 'flash'}],
        'provider_sources': [{'id': 'ds', 'type': 'openai_chat_completion', 'key': ['', KEY],
                              'api_base': 'https://model.example.com/v1/', 'timeout': 30, 'enable': True}],
        'agent_runner': {'config': {'persona': {'persona_id': '小爱人设'}}}}), encoding='utf-8')
    db = sqlite3.connect(str(folder / 'data_v4.db'))
    db.execute('CREATE TABLE personas (persona_id TEXT, system_prompt TEXT)')
    db.executemany('INSERT INTO personas VALUES (?, ?)', [('default', '默认'), ('小爱人设', '你是小爱，爱弥斯。')])
    db.commit()
    db.close()


class RealModel(unittest.TestCase):
    """Run 2's model: the key stays in memory, the limit is hard, nothing is retried."""

    def test_provider_and_persona_from_astrbot(self):
        import urllib.request
        from tools import replay
        sent = []

        class Opener:
            def open(self, req, timeout=None):
                sent.append((req.full_url, dict(req.header_items()), json.loads(req.data), timeout))
                import io
                return io.BytesIO(json.dumps({'choices': [{'message': {'content': '好'}}]}).encode())
        handlers = []
        real = urllib.request.build_opener
        urllib.request.build_opener = lambda *h: handlers.extend(h) or Opener()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                made_up_astrbot(Path(tmp) / 'astrbot')
                base, model, post = replay.astrbot_model(Path(tmp) / 'astrbot', 'ds/flash')
                persona = replay.astrbot_persona(Path(tmp) / 'astrbot')
                with self.assertRaises(SystemExit) as no_such:
                    replay.astrbot_model(Path(tmp) / 'astrbot', 'emb2')
        finally:
            urllib.request.build_opener = real
        self.assertEqual((base, model, persona), ('https://model.example.com/v1', 'flash', '你是小爱，爱弥斯。'))
        self.assertEqual(post([{'role': 'user', 'content': '嗨'}])['choices'][0]['message']['content'], '好')
        url, headers, body, timeout = sent[0]
        self.assertEqual((url, headers['Authorization'], body['model'], timeout),
                         ('https://model.example.com/v1/chat/completions', 'Bearer ' + KEY, 'flash', 30))
        self.assertEqual([h.proxies for h in handlers], [{}])          # no proxy: straight to that address
        self.assertNotIn(KEY, repr((base, model, persona, str(no_such.exception))))

    def test_hard_limit_caps_and_no_retry(self):
        import io
        import urllib.error
        from collections import Counter
        from tools import replay
        calls = []

        def post(messages):
            calls.append(messages)
            if len(calls) == 2:   # the provider says no, and echoes the key in its answer
                raise urllib.error.HTTPError('https://model.example.com/v1/chat/completions', 401, 'Unauthorized',
                                             {}, io.BytesIO(('bad key %s' % KEY).encode()))
            return {'choices': [{'message': {'content': '答%d' % len(calls)}}],
                    'usage': {'prompt_tokens': 100, 'completion_tokens': 10, 'prompt_cache_hit_tokens': 60}}
        stats, answers = Counter(), io.StringIO()
        clock = type('Clock', (), {'now': 5.0})()
        gate = replay.ModelGate(post, 4, {'notebook': 1}, stats, answers, clock, {'place': 'nightly'})
        got = [gate.chat('event_summary', '一'), gate.chat('event_summary', '二', system_prompt='她'),
               gate.chat('notebook', '三'), gate.chat('notebook', '四'), gate.chat('event_summary', '五'),
               gate.chat('event_summary', '六')]
        self.assertEqual(got, ['答1', '', '答3', '', '答4', ''])
        self.assertEqual(len(calls), 4)                                # the failed one is not tried again
        self.assertEqual(calls[1][0], {'role': 'system', 'content': '她'})
        self.assertEqual((stats['model_calls'], stats['model_ok'], stats['model_failed'], stats['model_failed_HTTP 401']),
                         (4, 3, 1, 1))                                 # the failed one counts
        self.assertEqual((stats['model_refused_cap_notebook'], stats['model_refused_limit']), (1, 1))
        self.assertEqual((stats['tokens_prompt_tokens'], stats['tokens_completion_tokens'],
                          stats['tokens_prompt_cache_hit_tokens']), (300, 30, 180))
        recs = [json.loads(x) for x in answers.getvalue().splitlines()]
        self.assertEqual([(r['call'], r['kind'], r['ok']) for r in recs],
                         [(1, 'event_summary', True), (2, 'event_summary', False), (3, 'notebook', True),
                          (4, 'event_summary', True)])
        self.assertEqual(recs[1]['failure'], 'HTTP 401')
        self.assertNotIn(KEY, answers.getvalue())

    def test_three_failures_in_a_row_stop_it(self):
        import io
        from collections import Counter
        from tools import replay
        calls = []

        def post(messages):
            calls.append(messages)
            if len(calls) in (1, 3, 4, 5):
                raise TimeoutError()
            return {'choices': [{'message': {'content': '好'}}]}
        stats = Counter()
        gate = replay.ModelGate(post, 800, {}, stats, io.StringIO(), type('C', (), {'now': 0.0})(), {'place': ''})
        got = [gate.chat('notebook', str(i)) for i in range(7)]
        self.assertEqual(got, ['', '好', '', '', '', '', ''])
        self.assertEqual(len(calls), 5)                                # one failure, then three in a row: stop
        self.assertEqual((stats['model_failed_timeout'], stats['model_refused_after_failures']), (4, 2))

    def test_a_real_model_needs_a_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            made_up_astrbot(Path(tmp) / 'astrbot')
            chat = fake.build_chat(Path(tmp) / 'chat.db')
            proc = subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'replay.py'), '--chat', str(chat),
                                   '--old-forgets', 'let-in', '--out', str(Path(tmp) / 'r'),
                                   '--astrbot', str(Path(tmp) / 'astrbot'), '--model', 'ds/flash'],
                                  capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(proc.returncode, 2)
            self.assertFalse((Path(tmp) / 'r').exists())
            self.assertNotIn(KEY, proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()
