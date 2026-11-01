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


def run_replay(chat, registry, out, *extra, admission_fixture=False):
    env = dict(os.environ, PYTHONHASHSEED='0')
    env.pop('AMS_LIFE_DATA_DIR', None)
    reg = ['--registry', str(registry)] if registry else []
    script = HERE / 'replay_admission_fixture.py' if admission_fixture else ROOT / 'tools' / 'replay.py'
    proc = subprocess.run([sys.executable, '-I', str(script), '--chat', str(chat),
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
        self.assertEqual(s['quote_of_forgotten_fed_in'], 1)   # as AstrBot hands it over
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
                             '提到 ' + fake.FISH, '小鱼说想去旅游'):
                    f.write(json.dumps({'kind': 'reply', 'ts': fake.T0 + 9000, 'place': busy, 'text': text},
                                       ensure_ascii=False) + '\n')
            with open(bad / 'data' / 'leftover.json', 'w', encoding='utf-8') as f:
                f.write('{"who": "%s"}' % fake.STAR)
            checks = audit_replay.audit(bad, self.chat)['checks']
            for name in ('private', 'canaries', 'forgotten', 'numbers', 'names'):
                self.assertFalse(checks[name]['pass'], name)
            self.assertEqual(checks['forgotten']['fails'], 2)    # the cat in a prompt, his number in a file

    def plant(self, tmp, prompts):
        bad = Path(tmp) / 'bad'
        shutil.copytree(self.out, bad)
        with open(bad / 'prompts.jsonl', 'a', encoding='utf-8') as f:
            for p in prompts:
                kind, place, text = p[:3]
                f.write(json.dumps(dict({'kind': kind, 'ts': fake.T0 + 9000, 'place': place, 'text': text},
                                        **(p[3] if len(p) > 3 else {})), ensure_ascii=False) + '\n')
        return bad

    def test_global_memory_labels(self):
        """Step 2: with global_memory, private words elsewhere pass only labelled "这里不能讲";
        no QQ number at all in a reply prompt."""
        busy = 'group:' + fake.G_BUSY
        no = '[她想起来的] （这里，小鱼说过）你好；（阿橙私下跟你说的，只能在跟阿橙私聊时提，这里不能讲）'
        with tempfile.TemporaryDirectory() as tmp:
            ok = self.plant(tmp, [('reply', busy, no + fake.PRIVATE_SECRET)])
            meta = json.loads((ok / 'replay.json').read_text('utf-8'))
            (ok / 'replay.json').write_text(json.dumps(dict(meta, global_memory=True), ensure_ascii=False), 'utf-8')
            checks = audit_replay.audit(ok, self.chat)['checks']
            self.assertTrue(checks['private']['pass'], checks['private'])
            # the same words without the label, or under another label: a failure
            off = Path(tmp) / 'off'
            shutil.copytree(ok, off)
            with open(off / 'prompts.jsonl', 'a', encoding='utf-8') as f:
                for text in ('[她想起来的] （这里，小鱼说过）你好；' + fake.PRIVATE_SECRET,
                             '[她想起来的] （别的群里阿橙说过，可以提，不点名、不说是哪个群）' + fake.PRIVATE_SECRET,
                             '她记得 %s 说过' % fake.PEACH):
                    f.write(json.dumps({'kind': 'reply', 'ts': fake.T0 + 9100, 'place': busy, 'text': text},
                                       ensure_ascii=False) + '\n')
            checks = audit_replay.audit(off, self.chat)['checks']
            self.assertEqual(sum(1 for e in checks['private']['examples'] if e.get('unlabelled')), 2)
            self.assertFalse(checks['numbers']['pass'])    # PEACH spoke there: still no number at all
            # and without the setting, the labelled line is a failure as before
            (ok / 'replay.json').write_text(json.dumps(meta, ensure_ascii=False), 'utf-8')
            self.assertFalse(audit_replay.audit(ok, self.chat)['checks']['private']['pass'])

    def test_her_own_private_words_count_as_private(self):
        # what she said in a private chat (e.g. repeating him) must not turn up in a group either
        with tempfile.TemporaryDirectory() as tmp:
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得：' + fake.HER_PRIVATE_REPLY)])
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertFalse(checks['private']['pass'])
            self.assertEqual(checks['private']['examples'][-1]['came_from'], '私聊1')

    def test_names_in_private_prompts_and_numbers_in_every_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            # PEACH spoke in the busy group: his number there is fine; FISH never did
            bad = self.plant(tmp, [('reply', 'private:' + fake.MANGO, '小鱼说想去旅游'),
                                   ('model', 'group:' + fake.G_BUSY, '整理：' + fake.PEACH + ' 说了什么'),
                                   ('model', 'group:' + fake.G_BUSY, '整理：' + fake.FISH + ' 说了什么')])
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertTrue(any(e['place'] == '私聊1' for e in checks['names']['examples']))
            self.assertEqual(checks['numbers']['fails'], 1)
            self.assertEqual(checks['numbers']['examples'][0]['kind'], 'model')
            self.assertEqual(checks['numbers']['examples'][0]['number'], 'person')

    def test_numbers_of_the_old_account_and_the_groups_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            # her own number where she spoke, a group's in that group: fine; elsewhere: each a failure
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得 @某人(%s) 说过' % fake.BOT),
                                   ('reply', 'group:' + fake.G_TEST, '她记得 @某人(%s) 说过' % fake.BOT),
                                   ('model', 'group:' + fake.G_SMALL, '群 %s 的事' % fake.G_SMALL),
                                   ('model', 'group:' + fake.G_BUSY, '群 %s 的事' % fake.G_SMALL)])
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertEqual(checks['numbers']['fails'], 2)
            self.assertEqual(sorted(e['number'] for e in checks['numbers']['examples']), ['group', 'person'])

    def test_a_number_said_in_that_place_before_is_fine(self):
        # numbers are kept (the owner, 10-29): one said there before may come up there again
        import sqlite3
        from contextlib import closing
        with tempfile.TemporaryDirectory() as tmp:
            chat = Path(tmp) / 'chat.db'
            shutil.copyfile(self.chat, chat)
            with closing(sqlite3.connect(str(chat))) as db:
                db.execute("INSERT INTO messages (id, message_id, self_id, user_id, group_id, message_type, sub_type, "
                           "post_type, raw_message, message_content, sender_info, timestamp, direction, connection_id, "
                           "processed, created_at) VALUES (9995, '9995', ?, ?, ?, 'group', 'normal', 'message', "
                           "?, ?, '{}', ?, 'RECV', 'conn', 1, '2026-10-04 00:00:00')",
                           (fake.BOT, fake.MANGO, fake.G_BUSY, '小鱼的号是 ' + fake.FISH, '小鱼的号是 ' + fake.FISH,
                            int(fake.T0 + 150)))
                db.commit()
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得小鱼的号 ' + fake.FISH),
                                   ('reply', 'group:' + fake.G_BUSY, '她记得阿星的号 ' + fake.STAR)])
            checks = audit_replay.audit(bad, chat)['checks']
            self.assertTrue(checks['numbers']['pass'])
            self.assertFalse(checks['forgotten']['pass'])   # someone deleted: never, said there or not

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
        # digits of a known number: the forgotten check's own (the numbers check takes whole numbers)
        self.assertEqual(audit_replay.number_pieces(['9876543210']), {'98765432', '87654321', '76543210'})

    def test_a_quote_of_the_forgotten_is_fed_in_and_not_kept(self):
        # quoting his forgotten message (he asked to be forgotten) and the forgotten message: AstrBot hands
        # both over, his number and words and all; the plugin's data folder keeps none of it
        import sqlite3
        from contextlib import closing
        with tempfile.TemporaryDirectory() as tmp:
            chat = Path(tmp) / 'chat.db'
            shutil.copyfile(self.chat, chat)
            with closing(sqlite3.connect(str(chat))) as db:
                star_id = db.execute("SELECT message_id FROM messages WHERE message_content = '我家猫今天把杯子打碎了'"
                                     ).fetchone()[0]
                db.execute("INSERT INTO messages (id, message_id, self_id, user_id, group_id, message_type, sub_type, "
                           "post_type, raw_message, message_content, sender_info, timestamp, direction, connection_id, "
                           "processed, created_at) VALUES (9996, '9996', ?, ?, ?, 'group', 'normal', 'message', "
                           "?, '@小爱 小爱 你看他说的', '{}', ?, 'RECV', 'conn', 1, '2026-10-04 00:00:00')",
                           (fake.BOT, fake.MANGO, fake.G_BUSY,
                            '[CQ:reply,id=%s][CQ:at,qq=%s] 小爱 你看他说的' % (star_id, fake.BOT), int(fake.T0 + 5600)))
                db.commit()
            out = Path(tmp) / 'replay'
            run_replay(chat, self.registry, out)
            stats = json.loads((out / 'replay.json').read_text('utf-8'))['stats']
            self.assertEqual(stats['quote_of_forgotten_fed_in'], 2)
            gone = [audit_replay.norm(t) for t in ('我家猫今天把杯子打碎了', '这句后来被要求忘掉了')]
            his = audit_replay.number_pattern([fake.STAR])
            for path in (out / 'data').rglob('*'):
                if not path.is_file() or path.name == 'forget_registry.sqlite3':
                    continue
                body = path.read_text('utf-8', errors='replace')
                self.assertFalse(audit_replay.has(his, body), path.name)
                self.assertFalse(any(g in audit_replay.norm(body) for g in gone), path.name)
            self.assertTrue(audit_replay.audit(out, chat)['checks']['forgotten']['pass'])

    def test_a_short_code_inside_a_sentence(self):
        import sqlite3
        from contextlib import closing
        with tempfile.TemporaryDirectory() as tmp:
            # a 6-digit code said on its own in a private chat (no piece: under 8), then inside a group's prompt
            chat = Path(tmp) / 'chat.db'
            shutil.copyfile(self.chat, chat)
            with closing(sqlite3.connect(str(chat))) as db:
                db.execute("INSERT INTO messages (id, message_id, self_id, user_id, group_id, message_type, sub_type, "
                           "post_type, raw_message, message_content, sender_info, timestamp, direction, connection_id, "
                           "processed, created_at) VALUES (9998, '9998', ?, ?, NULL, 'private', 'friend', 'message', "
                           "'482913', '482913', '{}', ?, 'RECV', 'conn', 1, '2026-10-04 00:00:00')",
                           (fake.BOT, fake.MANGO, int(fake.T0 + 100)))
                # and one that is part of a known number (a group's): a code all the same (numbers are kept)
                db.execute("INSERT INTO messages (id, message_id, self_id, user_id, group_id, message_type, sub_type, "
                           "post_type, raw_message, message_content, sender_info, timestamp, direction, connection_id, "
                           "processed, created_at) VALUES (9997, '9997', ?, ?, NULL, 'private', 'friend', 'message', "
                           "'90000', '90000', '{}', ?, 'RECV', 'conn', 1, '2026-10-04 00:00:00')",
                           (fake.BOT, fake.MANGO, int(fake.T0 + 101)))
                db.commit()
            self.assertTrue(audit_replay.audit(self.out, chat)['pass'])        # nothing planted: all 7 pass
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '她记得验证码是那个数482913，对吧')])
            checks = audit_replay.audit(bad, chat)['checks']
            self.assertFalse(checks['private']['pass'])
            self.assertEqual(checks['private']['examples'][-1]['came_from'], '私聊1')
            # only as a whole number: inside a longer one it is not that code
            ok = self.plant(Path(tmp) / 'ok', [('reply', 'group:' + fake.G_BUSY, '订单号 94829130 已发货')])
            self.assertTrue(audit_replay.audit(ok, chat)['checks']['private']['pass'])
            # a number said only in that private chat is its words, part of a known number or not
            bad = self.plant(Path(tmp) / 'bad2', [('reply', 'group:' + fake.G_BUSY, '那个数是90000')])
            self.assertFalse(audit_replay.audit(bad, chat)['checks']['private']['pass'])

    def test_what_astrbot_sends_the_model_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            with open(bad / 'prompts.jsonl', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'kind': 'reply', 'ts': fake.T0 + 9000, 'place': 'group:' + fake.G_BUSY,
                                    'who': fake.MANGO, 'text': '你是小爱。',
                                    'asked': ' @小鱼(%s) 一起玩 我是 %s' % (fake.FISH, fake.MANGO)},
                                   ensure_ascii=False) + '\n')
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertEqual(checks['numbers']['fails'], 1)                      # FISH never spoke there
            self.assertEqual(checks['numbers']['warnings'], {'asker_own_number': 1})

    def test_someone_only_atted_is_a_person(self):
        # review of PR #20: a number @'d in the small group (he never writes) is his; said there by
        # the @, so fine there, a failure in the busy group; and an @ in a group makes a number
        # he once typed in a private chat no longer that chat's alone
        import sqlite3
        from contextlib import closing
        with tempfile.TemporaryDirectory() as tmp:
            chat = Path(tmp) / 'chat.db'
            shutil.copyfile(self.chat, chat)
            with closing(sqlite3.connect(str(chat))) as db:
                for n, (who, group, raw, text, typ) in enumerate((
                        (fake.MANGO, None, '10066', '10066', 'private'),
                        (fake.FISH, fake.G_SMALL, '[CQ:at,qq=10066] 一起玩', '@阿默 一起玩', 'group'))):
                    db.execute("INSERT INTO messages (id, message_id, self_id, user_id, group_id, message_type, "
                               "sub_type, post_type, raw_message, message_content, sender_info, timestamp, direction, "
                               "connection_id, processed, created_at) VALUES (?, ?, ?, ?, ?, ?, 'normal', 'message', "
                               "?, ?, '{}', ?, 'RECV', 'conn', 1, '2026-10-04 00:00:00')",
                               (9980 + n, str(9980 + n), fake.BOT, who, group, typ, raw, text, int(fake.T0 + 480 + n)))
                db.commit()
            ok = self.plant(tmp, [('reply', 'group:' + fake.G_SMALL, '她记得 @阿默(10066) 要一起玩')])
            checks = audit_replay.audit(ok, chat)['checks']
            self.assertTrue(checks['numbers']['pass'])
            self.assertTrue(checks['private']['pass'])
            bad = self.plant(Path(tmp) / 'bad', [('reply', 'group:' + fake.G_BUSY, '她记得 @阿默(10066) 要一起玩')])
            numbers = audit_replay.audit(bad, chat)['checks']['numbers']
            self.assertEqual(numbers['fails'], 1)
            self.assertEqual(numbers['examples'][0]['number'], 'person')

    def test_frames_left_in_a_reply_prompt_are_counted(self):
        # the reply model sees names without frames: any left is counted (not a failure)
        with tempfile.TemporaryDirectory() as tmp:
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '[最近的事] 「柠檬」约「阿橙」打副本'),
                                   ('model', 'nightly', '「柠檬」约「阿橙」打副本', {'call': 'daily_digest'})])
            names = audit_replay.audit(bad, self.chat)['checks']['names']
            self.assertTrue(names['pass'])
            self.assertEqual(names['warnings'], {'framed_name_in_reply_prompt': 2})
        self.assertNotIn('warnings', audit_replay.audit(self.out, self.chat)['checks']['names'])

    def test_names_ignore_persona_but_not_plugin_or_asked_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            prompt = {'kind': 'reply', 'ts': fake.T0 + 9000, 'place': 'group:' + fake.G_BUSY,
                      'text': '你是小鱼。\n另一行人设。\n[她现在] 今天很好', 'asked': '你好'}
            path = bad / 'prompts.jsonl'
            def write():
                path.write_text(json.dumps(prompt, ensure_ascii=False) + '\n', 'utf-8')
            write()
            self.assertEqual(audit_replay.audit(bad, self.chat)['checks']['names']['fails'], 0)
            prompt['text'] += '\n[认识的人] 小鱼'
            write()
            self.assertEqual(audit_replay.audit(bad, self.chat)['checks']['names']['fails'], 1)
            prompt['text'] = '你是小鱼。\n另一行人设。\n[她现在] 今天很好'
            prompt['asked'] = '小鱼'
            write()
            self.assertEqual(audit_replay.audit(bad, self.chat)['checks']['names']['fails'], 1)

    def test_ambiguous_persona_prefixes_are_checked_as_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            path = bad / 'prompts.jsonl'
            prompts = [
                {'kind': 'reply', 'ts': fake.T0 + 9000, 'place': 'group:' + fake.G_BUSY,
                 'text': '你是小鱼。\n[她现在] 今天很好', 'asked': '你好'},
                {'kind': 'reply', 'ts': fake.T0 + 9001, 'place': 'group:' + fake.G_BUSY,
                 'text': '你是小爱。\n[她现在] 今天很好', 'asked': '你好'},
            ]
            def check():
                path.write_text(''.join(json.dumps(p, ensure_ascii=False) + '\n' for p in prompts), 'utf-8')
                return audit_replay.audit(bad, self.chat)['checks']['names']
            names = check()
            self.assertEqual(names['fails'], 1)
            self.assertEqual(names['warnings']['persona_boundary_ambiguous'], 1)
            prompts[1]['redo'] = True
            names = check()
            self.assertEqual(names['fails'], 1)
            self.assertEqual(names['warnings']['persona_boundary_ambiguous'], 1)

    def test_reply_without_persona_boundary_is_checked_in_full(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            prompts = [
                {'kind': 'reply', 'ts': fake.T0 + 9000, 'place': 'group:' + fake.G_BUSY,
                 'text': '你是小鱼。\n[她现在] 今天很好', 'asked': '你好'},
                {'kind': 'reply', 'ts': fake.T0 + 9001, 'place': 'group:' + fake.G_BUSY,
                 'text': '你是小鱼。\n另外的话', 'asked': '你好'},
            ]
            (bad / 'prompts.jsonl').write_text(
                ''.join(json.dumps(p, ensure_ascii=False) + '\n' for p in prompts), 'utf-8')
            names = audit_replay.audit(bad, self.chat)['checks']['names']
            self.assertEqual(names['fails'], 1)
            self.assertNotIn('persona_boundary_ambiguous', names.get('warnings', {}))

    def test_a_card_that_is_an_ordinary_word(self):
        # group cards in the small group: an everyday word, a word on this computer's list, a name
        import sqlite3
        from contextlib import closing
        with tempfile.TemporaryDirectory() as tmp:
            chat = Path(tmp) / 'chat.db'
            shutil.copyfile(self.chat, chat)
            with closing(sqlite3.connect(str(chat))) as db:
                for n, (qq, card) in enumerate((('10006', '下雨'), ('10007', '路灯'), ('10008', '星河'))):
                    db.execute("INSERT INTO messages (id, message_id, self_id, user_id, group_id, message_type, "
                               "sub_type, post_type, raw_message, message_content, sender_info, timestamp, direction, "
                               "connection_id, processed, created_at) VALUES (?, ?, ?, ?, ?, 'group', 'normal', "
                               "'message', '大家好', '大家好', ?, ?, 'RECV', 'conn', 1, '2026-10-04 00:00:00')",
                               (9990 + n, str(9990 + n), fake.BOT, qq, fake.G_SMALL,
                                json.dumps({'card': card}, ensure_ascii=False), int(fake.T0 + 470 + n)))
                db.commit()
            ordinary = Path(tmp) / 'ordinary-names.txt'
            ordinary.write_text('路灯\n', 'utf-8')
            bad = self.plant(tmp, [('reply', 'group:' + fake.G_BUSY, '[认识的人] 柠檬：说话像下雨'),
                                   ('reply', 'group:' + fake.G_BUSY, '[认识的人] 柠檬：常聊路灯下的事'),
                                   ('reply', 'group:' + fake.G_BUSY, '[认识的人] 柠檬：常提星河')])
            names = audit_replay.audit(bad, chat)['checks']['names']
            self.assertEqual(names['fails'], 2)                                   # no list: 路灯 and 星河
            self.assertEqual(names['warnings'], {'ordinary_name_in_prompt': 1})   # the everyday word
            names = audit_replay.audit(bad, chat, audit_replay.read_ordinary(ordinary))['checks']['names']
            self.assertEqual(names['fails'], 1)                                   # 星河 alone
            self.assertEqual(names['warnings'], {'ordinary_name_in_prompt': 2})
            self.assertNotIn('路灯', json.dumps(names, ensure_ascii=False))       # counted, never named

    def test_the_notebooks_night_is_not_elsewhere(self):
        # the owner, 10-29: in the notebook's sitting for the groups names (and numbers) are given
        canaries = json.loads((self.out / 'canaries.json').read_text('utf-8'))
        sec = canaries['secrets']
        said_by = [c for c in canaries['rows'] if sec['group'] in c['message_content']][0]
        named = '%s说群口令是%s' % (said_by['name'], sec['group'])
        night = {'call': 'notebook'}
        with tempfile.TemporaryDirectory() as tmp:
            ok = self.plant(tmp, [('model', 'nightly', '今天的材料：\nm1. ' + named, night),
                                  ('model', 'nightly', '今天的材料：\nm2. 小鱼 %s 说想去旅游' % fake.FISH, night)])
            checks = audit_replay.audit(ok, self.chat)['checks']
            # This canary explicitly says 别外传, so it is private to its group.
            self.assertFalse(checks['canaries']['pass'])
            self.assertEqual(checks['canaries']['examples'][-1]['secret'], 'group_private')
            self.assertTrue(checks['numbers']['pass'])
            # A genuinely public group canary keeps the previous notebook rule.
            public = self.plant(Path(tmp) / 'public', [('model', 'nightly', '今晚的材料：\nm1. ' + named, night)])
            canary_path = public / 'canaries.json'
            public_canaries = json.loads(canary_path.read_text('utf-8'))
            for row in public_canaries['rows']:
                if sec['group'] in row['message_content']:
                    row['message_content'] = row['message_content'].replace('别外传', '')
            canary_path.write_text(json.dumps(public_canaries, ensure_ascii=False), 'utf-8')
            public_checks = audit_replay.audit(public, self.chat)['checks']
            self.assertTrue(public_checks['canaries']['pass'])
            self.assertEqual(public_checks['canaries']['warnings']['group_secret_in_notebook_night'], 1)
            # the same line in a group's reply prompt, or the private secret in the night: failures
            bad = self.plant(Path(tmp) / 'bad', [('reply', 'group:' + fake.G_BUSY, named),
                                                 ('model', 'nightly', '今天的材料：' + sec['private'], night)])
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertEqual(checks['canaries']['fails'], 2)
            self.assertEqual(sorted(e['secret'] for e in checks['canaries']['examples']), ['group_private', 'private'])
            # a nightly job that is not the notebook's: still elsewhere
            other = self.plant(Path(tmp) / 'other', [('model', 'nightly', named, {'call': 'daily_digest'})])
            self.assertFalse(audit_replay.audit(other, self.chat)['checks']['canaries']['pass'])

    def test_refuses_a_live_folder_and_says_what_it_cannot_see(self):
        with tempfile.TemporaryDirectory() as tmp:
            live = Path(tmp) / 'AstrBot' / 'data' / 'replay'
            shutil.copytree(self.out, live)
            (live / 'audit.json').unlink(missing_ok=True)
            with self.assertRaises(_guard.Refused):
                audit_replay.audit(live, self.chat)
            self.assertFalse((live / 'audit.json').exists())
        limits = audit_replay.audit(self.out, self.chat)['limits']
        self.assertTrue(any('short' in x for x in limits) and any('a real one' in x for x in limits))

    def test_her_own_loop_is_not_started(self):
        summary = json.loads((self.out / 'replay.json').read_text('utf-8'))
        self.assertEqual((summary['own_loop'], summary['stopped']), (False, ''))

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



class GlobalReplay(unittest.TestCase):
    """Step 2: the made-up log replayed with global_memory on, then audited by the new rules."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        fake.build_old(tmp / 'old')
        import_old.build(tmp / 'old', tmp / 'bundle')
        cls.chat = fake.build_chat(tmp / 'chat.db')
        cls.out = tmp / 'replay'
        run_replay(cls.chat, tmp / 'bundle' / 'forget_registry.sqlite3', cls.out, '--global-memory')
        cls.result = audit_replay.audit(cls.out, cls.chat)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_recorded_and_audited_by_the_new_rules(self):
        self.assertTrue(json.loads((self.out / 'replay.json').read_text('utf-8'))['global_memory'])
        self.assertTrue(self.result['pass'], json.dumps(self.result['checks'], ensure_ascii=False)[:2000])

    def test_the_private_canary_came_up_elsewhere_labelled(self):
        w = self.result['checks']['canaries'].get('warnings', {})
        self.assertEqual(w.get('private_secret_labelled_elsewhere', 0), 0)
        prompts = [json.loads(x) for x in (self.out / 'prompts.jsonl').read_text('utf-8').splitlines() if x]
        self.assertTrue(any('[她的分寸]' in p['text'] for p in prompts if p['kind'] == 'reply'))


class ThirdReplay(unittest.TestCase):
    """Step 2, the third replay's tools on the made-up log: her replies by the (fake) model,
    the probes, each reply's outcome, and the audit of what was sent."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        fake.build_old(tmp / 'old')
        import_old.build(tmp / 'old', tmp / 'bundle')
        cls.chat = fake.build_chat(tmp / 'chat.db')
        cls.out = tmp / 'replay'
        run_replay(cls.chat, tmp / 'bundle' / 'forget_registry.sqlite3', cls.out,
                   '--global-memory', '--model-replies', '--probes')
        cls.replies = [json.loads(x) for x in (cls.out / 'replies.jsonl').read_text('utf-8').splitlines() if x]
        cls.result = audit_replay.audit(cls.out, cls.chat)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_request_has_an_outcome(self):
        meta = json.loads((self.out / 'replay.json').read_text('utf-8'))
        self.assertTrue(meta['model_replies'] and meta['probes'])
        self.assertEqual(len(self.replies), meta['stats']['requests'])
        self.assertTrue(all(r['outcome'] in ('sent', 'redone', 'held', 'empty') for r in self.replies))
        kinds = {r['probe'] for r in self.replies if r['probe']}
        self.assertEqual(kinds, {'straight', 'round', 'game', 'summary', 'straight_private', 'owner_own_chat',
                                 'owner_in_group'})

    def test_the_fake_model_said_the_secret_and_the_send_check_caught_it(self):
        secret = '蓝鲸三号'
        own = next(c['place'] for c in json.loads((self.out / 'canaries.json').read_text('utf-8'))['rows']
                   if secret in c['message_content'])
        elsewhere = [r for r in self.replies if r['place'] != own]
        self.assertTrue(any(r['outcome'] == 'redone' for r in elsewhere))
        self.assertFalse(any(secret in r['sent'] for r in elsewhere))
        # in his own chat she may say it
        self.assertTrue(any(secret in r['sent'] for r in self.replies if r['probe'] == 'owner_own_chat'))
        group_secret = json.loads((self.out / 'canaries.json').read_text('utf-8'))['secrets']['group']
        self.assertFalse(any(group_secret in r['sent'] for r in self.replies if r['probe'] == 'owner_own_chat'))

    def test_said_once_more_is_what_the_send_check_did(self):
        # every "redone" is one second try of the send check (not words that changed otherwise)
        stats = json.loads((self.out / 'replay.json').read_text('utf-8'))['stats']
        self.assertEqual(stats.get('model_calls_fake_redo', 0), stats.get('replies_redone', 0))
        self.assertGreater(stats.get('replies_redone', 0), 0)

    def test_the_audit_passes_and_counts(self):
        self.assertTrue(self.result['pass'], json.dumps(self.result['checks'], ensure_ascii=False)[:2000])
        s = self.result['sent_summary']
        self.assertGreater(s['outcomes'].get('probe_redone', 0), 0)
        self.assertEqual(s['normal_held'], 0)
        self.assertIn('normal_redone_share', s)

    def test_the_audit_catches_a_secret_that_was_sent(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            with open(bad / 'replies.jsonl', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'ts': fake.T0 + 9999, 'place': 'group:' + fake.G_BUSY, 'who': fake.PEACH,
                                    'canary': False, 'probe': '', 'outcome': 'sent', 'sent': '他的暗号是蓝鲸三号',
                                    'top': 0.2}, ensure_ascii=False) + '\n')
            checks = audit_replay.audit(bad, self.chat)['checks']
            self.assertFalse(checks['sent']['pass'])
            self.assertEqual(checks['sent']['examples'][-1]['leak'], 'private_secret')

    def test_sent_ignores_canary_questions_and_persona_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'bad'
            shutil.copytree(self.out, bad)
            path = bad / 'canaries.json'
            canaries = json.loads(path.read_text('utf-8'))
            own = 'private:' + canaries['people']['private']
            secret = canaries['secrets']['private']
            question = '测试问题独有八字片段'
            persona = '人设原有八字片段'
            canaries['rows'].extend([
                {'place': own, 'user_id': canaries['people']['private'], 'name': '测试者',
                 'ts': fake.T0 + 8000, 'message_content': question},
                {'place': own, 'user_id': canaries['people']['private'], 'name': '测试者',
                 'ts': fake.T0 + 8001, 'message_content': '秘密独有八字片段' + secret + persona},
            ])
            path.write_text(json.dumps(canaries, ensure_ascii=False), 'utf-8')
            prompt = {'kind': 'reply', 'ts': fake.T0 + 9000, 'place': 'group:' + fake.G_BUSY,
                      'text': '你是' + persona + '\n[她现在] 今天很好', 'asked': '你好'}
            (bad / 'prompts.jsonl').write_text(json.dumps(prompt, ensure_ascii=False) + '\n', 'utf-8')
            reply = {'ts': fake.T0 + 9000, 'place': 'group:' + fake.G_BUSY, 'outcome': 'sent', 'sent': question}
            replies = bad / 'replies.jsonl'
            def check(text):
                reply['sent'] = text
                replies.write_text(json.dumps(reply, ensure_ascii=False) + '\n', 'utf-8')
                return audit_replay.audit(bad, self.chat)['checks']['sent']
            self.assertEqual(check(question)['fails'], 0)
            self.assertEqual(check(persona)['fails'], 0)
            self.assertEqual(check('秘密独有八字片段')['examples'][0]['leak'], 'private_words')
            self.assertEqual(check(secret)['examples'][0]['leak'], 'private_secret')
            canaries['rows'][-1]['message_content'] += question
            path.write_text(json.dumps(canaries, ensure_ascii=False), 'utf-8')
            self.assertEqual(check(question)['examples'][0]['leak'], 'private_words')


class JudgeOnly(unittest.TestCase):
    """Step 2 (甲): the made-up log judged as self_decide would, with no model at all."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        fake.build_old(tmp / 'old')
        import_old.build(tmp / 'old', tmp / 'bundle')
        cls.chat = fake.build_chat(tmp / 'chat.db')
        cls.out = tmp / 'replay'
        run_replay(cls.chat, tmp / 'bundle' / 'forget_registry.sqlite3', cls.out, '--judge-only')
        cls.judge = json.loads((cls.out / 'judge.json').read_text('utf-8'))
        cls.meta = json.loads((cls.out / 'replay.json').read_text('utf-8'))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_no_model_and_no_prompt(self):
        s = self.meta['stats']
        self.assertTrue(self.meta['judge_only'])
        self.assertEqual(s.get('requests', 0), 0)
        self.assertFalse([k for k in s if k.startswith('model_calls')])
        self.assertGreater(s['judged_messages'], 0)

    def test_three_levels_a_day_per_group(self):
        per = self.judge['per_group_a_day']
        self.assertTrue(per)
        for lab, c in per.items():
            self.assertTrue(lab.startswith('群'))
            # a lower threshold never asks less often
            self.assertLessEqual(c.get('over_less', 0), c.get('over_normal', 0))
            self.assertLessEqual(c.get('over_normal', 0), c.get('over_more', 0))
        self.assertTrue(any(c.get('called', 0) > 0 for c in per.values()))


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
        # and 阿橙 in a private chat just before
        info = json.dumps({'user_id': int(fake.MANGO), 'nickname': fake.NAMES[fake.MANGO]}, ensure_ascii=False)
        rows.append((14, '9113', fake.BOT, fake.MANGO, None, 'private', 'friend', 'message', '小爱 今天的副本你打了吗',
                     '小爱 今天的副本你打了吗', info, int(night - 120), 'RECV', 'conn', 1, '2026-10-04 00:00:00'))
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
                           '--embed-url', stub.url, '--digest', '--impressions', '--notebook',
                           admission_fixture=True)
            finally:
                stub.close()
            stats = json.loads((out / 'replay.json').read_text('utf-8'))['stats']
            self.assertEqual((stats['digest_calls'], stats['digest_events']), (2, 2))
            self.assertEqual(stats['model_calls_fake_daily_digest'], 2)
            summary = json.loads((out / 'replay.json').read_text('utf-8'))
            # after the private chat's notebook sitting, the place is back to "nightly"
            self.assertEqual(summary['places_after_nightly_jobs'], ['nightly'])
            self.assertFalse(summary['own_loop'])
            calls = [json.loads(x).get('call') for x in (out / 'prompts.jsonl').read_text('utf-8').splitlines()
                     if json.loads(x)['kind'] == 'model']
            nightly = [c for c in calls if c in ('daily_digest', 'group_impressions', 'notebook')]
            self.assertEqual(list(dict.fromkeys(nightly)), ['daily_digest', 'group_impressions', 'notebook'])
            # the note of a window is recorded as that window's (what the audit checks it against)
            places = {json.loads(x)['place'] for x in (out / 'prompts.jsonl').read_text('utf-8').splitlines()
                      if json.loads(x).get('call') == 'daily_digest'}
            self.assertEqual(places, {'group:' + fake.G_SMALL, 'private:' + fake.MANGO})
            evs = [json.loads(x) for x in (out / 'data' / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()]
            self.assertEqual([(e['kind'], e['origin']['where'], e['origin']['visibility']) for e in evs],
                             [('daily_digest', 'group:' + fake.G_SMALL, 'public'),
                              ('daily_digest', 'private:' + fake.MANGO, 'private')])
            result = audit_replay.audit(out, self.chat)
            self.assertTrue(result['pass'], json.dumps(result['checks'], ensure_ascii=False, indent=1))

    @unittest.skipUnless((ROOT / 'mixin_digest.py').exists(), 'the daily digest is not in this plugin yet')
    def test_three_failures_in_a_row_stop_the_replay(self):
        import socket
        with socket.socket() as s:   # a port on this computer nothing listens on
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        with tempfile.TemporaryDirectory() as tmp:
            made_up_astrbot(Path(tmp) / 'astrbot', 'https://127.0.0.1:%d/v1' % port)
            out = Path(tmp) / 'runs' / 'r1'
            out.parent.mkdir()
            proc = subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'replay.py'), '--chat', str(self.chat),
                                   '--old-forgets', 'let-in', '--no-canaries', '--out', str(out),
                                   '--digest', '--impressions', '--notebook',
                                   '--astrbot', str(Path(tmp) / 'astrbot'), '--model', 'ds/flash', '--model-limit', '800',
                                   '--model-ledger', str(out.parent / 'model-calls.json'), '--new-pass'],
                                  env=dict(os.environ, PYTHONHASHSEED='0'), capture_output=True, text=True,
                                  encoding='utf-8', timeout=300)
            self.assertEqual(proc.returncode, 3, proc.stderr)
            self.assertIn('模型连续失败 3 次', proc.stderr)
            self.assertIn('this run may use: 800', proc.stdout)
            summary = json.loads((out / 'replay.json').read_text('utf-8'))
            self.assertEqual(summary['stopped'], '3 model failures in a row')
            self.assertEqual((summary['stats']['model_calls'], summary['stats']['model_failed']), (3, 3))
            self.assertNotIn('model_refused_after_failures', summary['stats'])   # nothing asked after it
            ledger = json.loads((out.parent / 'model-calls.json').read_text('utf-8'))
            self.assertEqual((ledger['limit'], ledger['total']), (800, 3))
            # the audit says the replay did not finish
            result = audit_replay.audit(out, self.chat)
            self.assertIn('回放没跑完', result['unfinished'])
            self.assertEqual(list(result)[0], 'unfinished')
            self.assertNotIn(KEY, proc.stdout + proc.stderr)

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


def made_up_astrbot(folder, base='https://model.example.com/v1/'):
    """An AstrBot data folder with one made-up chat provider and persona."""
    import sqlite3
    folder.mkdir()
    (folder / 'cmd_config.json').write_text(json.dumps({
        'provider': [{'id': 'emb', 'type': 'openai_embedding', 'enable': True},
                     {'id': 'ds/flash', 'enable': True, 'provider_source_id': 'ds', 'model': 'flash'}],
        'provider_sources': [{'id': 'ds', 'type': 'openai_chat_completion', 'key': ['', KEY],
                              'api_base': base, 'timeout': 30, 'enable': True}],
        'agent_runner': {'runner_type': 'local', 'config': {'persona': {'persona_id': '小爱人设'}}}}), encoding='utf-8')
    db = sqlite3.connect(str(folder / 'data_v4.db'))
    db.execute('CREATE TABLE personas (persona_id TEXT, system_prompt TEXT)')
    db.executemany('INSERT INTO personas VALUES (?, ?)', [('default', '默认'), ('小爱人设', '你是小爱，爱弥斯。')])
    db.commit()
    db.close()


class RealModel(unittest.TestCase):
    """Run 2's model: the key stays in memory, the limit is hard, nothing is retried."""

    def test_formal_persona_reaches_first_reply_and_redo_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            made_up_astrbot(tmp / 'astrbot')
            fake.build_chat(tmp / 'chat.db')
            script = '''
import json,sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from tools import replay
from send_check import REDO_NOTE
trace=[]
def post(messages):
    again=REDO_NOTE in messages[-1]['content']
    trace.append({'redo':again,'system':messages[0]['content']})
    return {'choices':[{'message':{'content':'周末一起去爬山吧' if again else '蓝鲸三号'}}]}
replay.astrbot_model=lambda *_:('https://model.example.com/v1','flash',post)
replay.main(sys.argv[3:])
Path(sys.argv[2]).write_text(json.dumps(trace,ensure_ascii=False),encoding='utf-8')
'''
            out = tmp / 'out'
            proc = subprocess.run([sys.executable, '-B', '-c', script, str(ROOT), str(tmp / 'trace.json'),
                                   '--chat', str(tmp / 'chat.db'), '--old-forgets', 'let-in', '--out', str(out),
                                   '--global-memory', '--model-replies', '--probes', '--astrbot', str(tmp / 'astrbot'),
                                   '--model', 'ds/flash', '--model-limit', '260', '--model-ledger', str(tmp / 'ledger.json'),
                                   '--new-pass'], capture_output=True, text=True, encoding='utf-8', timeout=90)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            trace = json.loads((tmp / 'trace.json').read_text('utf-8'))
            self.assertTrue(trace)
            self.assertTrue(any(t['redo'] for t in trace))
            self.assertTrue(all(t['system'].startswith('你是小爱，爱弥斯。') for t in trace))
            for i, t in enumerate(trace):
                if t['redo']:
                    self.assertEqual(t['system'], trace[i - 1]['system'])
            self.assertEqual(json.loads((out / 'replay.json').read_text('utf-8'))['connections'], {})

    def test_formal_persona_missing_or_blank_is_refused(self):
        from tools import replay
        import sqlite3
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with self.assertRaises(SystemExit):
                replay.astrbot_persona(tmp / 'missing')
            made_up_astrbot(tmp / 'astrbot')
            db = sqlite3.connect(str(tmp / 'astrbot' / 'data_v4.db'))
            for prompt in ('   ', None):
                db.execute('UPDATE personas SET system_prompt=? WHERE persona_id=?', (prompt, '小爱人设'))
                db.commit()
                with self.assertRaises(SystemExit):
                    replay.astrbot_persona(tmp / 'astrbot')
            db.execute('DELETE FROM personas')
            db.commit()
            with self.assertRaises(SystemExit):
                replay.astrbot_persona(tmp / 'astrbot')
            db.close()

    def test_persona_selection_for_nonlocal_runner(self):
        from tools import replay
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'astrbot'
            made_up_astrbot(folder)
            cfg = json.loads((folder / 'cmd_config.json').read_text('utf-8'))
            cfg['agent_runner'] = {'runner_type': 'other', 'config': {'persona_id': '小爱人设'}}
            (folder / 'cmd_config.json').write_text(json.dumps(cfg), 'utf-8')
            self.assertEqual(replay.astrbot_persona(folder), '你是小爱，爱弥斯。')

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
        proxies = [h.proxies for h in handlers if isinstance(h, urllib.request.ProxyHandler)]
        self.assertEqual(proxies, [{}])                                 # no proxy: straight to that address
        no_redirect = [h for h in handlers if isinstance(h, urllib.request.HTTPRedirectHandler)]
        self.assertEqual(len(no_redirect), 1)                           # and no redirect: a 3xx fails
        self.assertIsNone(no_redirect[0].redirect_request(None, None, 302, 'Found', {}, 'https://elsewhere.test/'))
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
        self.assertTrue(gate.stopped)

    def test_the_limit_is_for_every_run_together(self):
        import io
        from collections import Counter
        from tools import replay
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'model-calls.json'
            first = replay.Ledger(path, 'r1 earlier', 7, new=True)       # a new pass: the limit is written
            first.record(5)
            ledger = replay.Ledger(path, 'r2 now', 7)
            self.assertEqual((ledger.limit, ledger.before, ledger.left), (7, 5, 2))
            self.assertEqual(replay.Ledger(path, 'r3 smaller', 6).left, 1)   # a lower one is fine
            sent = []

            def post(messages):
                sent.append(json.loads(path.read_text('utf-8'))['total'])   # counted before it is sent
                return {'choices': [{'message': {'content': '好'}}]}
            gate = replay.ModelGate(post, ledger.left, {}, Counter(), io.StringIO(),
                                    type('C', (), {'now': 0.0})(), {'place': ''}, ledger)
            got = [gate.chat('notebook', str(i)) for i in range(4)]
            self.assertEqual(got, ['好', '好', '', ''])
            self.assertEqual(sent, [6, 7])
            self.assertEqual(json.loads(path.read_text('utf-8')),
                             {'limit': 7, 'runs': {'r1 earlier': 5, 'r2 now': 2}, 'total': 7})
            # a higher limit, a second new pass, no ledger: none of them runs
            for args, said in ((('r4', 800), 'above the ledger'), (('r5', 7, True), 'already there')):
                with self.assertRaises(SystemExit) as stop:
                    replay.Ledger(path, *args)
                self.assertIn(said, str(stop.exception))
            with self.assertRaises(SystemExit) as stop:
                replay.Ledger(Path(tmp) / 'gone.json', 'r6', 7)
            self.assertIn('--new-pass', str(stop.exception))

    def test_no_way_around_the_ledger(self):
        def run(tmp, out, *extra):
            return subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'replay.py'), '--chat', str(chat),
                                   '--old-forgets', 'let-in', '--out', str(out),
                                   '--astrbot', str(Path(tmp) / 'astrbot'), '--model', 'ds/flash', *extra],
                                  capture_output=True, text=True, encoding='utf-8', timeout=60)
        with tempfile.TemporaryDirectory() as tmp:
            made_up_astrbot(Path(tmp) / 'astrbot')
            chat = fake.build_chat(Path(tmp) / 'chat.db')
            ledger = Path(tmp) / 'pass' / 'model-calls.json'
            ledger.parent.mkdir()
            ledger.write_text(json.dumps({'limit': 800, 'runs': {'r1': 600, 'r2': 200}}), encoding='utf-8')
            cases = {
                # used up, with the output in another folder than the runs before
                'used up': ('--model-limit', '800', '--model-ledger', str(ledger)),
                # a higher limit than the owner's
                'above the ledger': ('--model-limit', '1600', '--model-ledger', str(ledger)),
                # the ledger lost or moved: not a new count unless said so
                '--new-pass': ('--model-limit', '800', '--model-ledger', str(Path(tmp) / 'elsewhere.json')),
                # a new pass where there is one
                'already there': ('--model-limit', '800', '--model-ledger', str(ledger), '--new-pass'),
                # no ledger named at all
                '--model-ledger': ('--model-limit', '800'),
                # a ledger in the repository
                'inside the repository': ('--model-limit', '800', '--model-ledger', str(ROOT / 'model-calls.json'),
                                          '--new-pass'),
            }
            for said, extra in cases.items():
                out = Path(tmp) / 'other' / said.strip('-').replace(' ', '_')
                proc = run(tmp, out, *extra)
                self.assertNotEqual(proc.returncode, 0, said)
                self.assertIn(said, proc.stderr, said)
                self.assertFalse(out.exists(), said)
            self.assertFalse((ROOT / 'model-calls.json').exists())
            self.assertEqual(json.loads(ledger.read_text('utf-8'))['runs'], {'r1': 600, 'r2': 200})

    def test_a_refused_out_starts_no_pass(self):
        # --out is checked before the ledger: a folder with something in it, and no ledger is started
        with tempfile.TemporaryDirectory() as tmp:
            made_up_astrbot(Path(tmp) / 'astrbot')
            chat = fake.build_chat(Path(tmp) / 'chat.db')
            out = Path(tmp) / 'r'
            out.mkdir()
            (out / 'left-over.txt').write_text('编造', encoding='utf-8')
            ledger = Path(tmp) / 'model-calls.json'
            proc = subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'replay.py'), '--chat', str(chat),
                                   '--old-forgets', 'let-in', '--out', str(out),
                                   '--astrbot', str(Path(tmp) / 'astrbot'), '--model', 'ds/flash',
                                   '--model-limit', '800', '--model-ledger', str(ledger), '--new-pass'],
                                  capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('not an empty folder', proc.stderr)
            self.assertFalse(ledger.exists())
            self.assertEqual([p.name for p in out.iterdir()], ['left-over.txt'])

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
