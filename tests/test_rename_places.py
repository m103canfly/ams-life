# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""tools/rename_places.py on made-up data folders: the rename, the merge and the checks.

Every folder is made up inside the test's own temporary folder; every number and name is
invented. No real data folder is read or written."""
import ast
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from tools import rename_places  # noqa: E402

GROUP = '900001'
OTHER = '10001'
GUILD = '900002'
COLON = 'default:GroupMessage:' + GROUP
NEUTRAL = 'group:' + GROUP
TITLE = '编造的事件标题'
TEXT = '编造的聊天内容'
NAME = '虚构甲'
ALIAS = '虚构的别名'
PHONE_FILE = 'phone/group_900001-0123456789ab.json'
PEOPLE_FILE = 'people/group_900001.json'


def event(ident, ts, session, title=TITLE):
    """One made-up event, with a session in each of the fields the tool changes."""
    return {'id': ident, 'ts': ts, 'session': session, 'title': title,
            'provenance': {'session': session, 'sources': [{'session': session, 'sender_id': '10002'}]},
            'source_check': {'source_items': [{'session': session}]}}


GLOBAL_EVENTS = [event('evt_1', 100.0, COLON),
                 event('evt_2', 101.0, NEUTRAL),
                 event('evt_3', 102.0, '')]
A_EVENTS = [event('evt_10', 200.0, COLON), event('evt_11', 201.0, COLON)]
B_EVENTS = [event('evt_10', 200.0, NEUTRAL), event('evt_12', 199.0, NEUTRAL)]
LIBRARY_DOC = {'schema_version': 3, 'rooms': {}, 'entries': [
    {'id': 'm1', 'text': TEXT,
     'provenance': {'session': COLON, 'sources': [{'session': COLON, 'sender_id': '10002'}]}},
    {'id': 'm2', 'text': TEXT, 'provenance': {'session': NEUTRAL}}]}
USER_ONE = {'sender_id': OTHER, 'sender_name': NAME,
            'sessions': [COLON, NEUTRAL, COLON, 'private:10003']}
USER_MANY = {'sender_id': '10002', 'sessions': ['private:%d' % (20000 + i) for i in range(22)]}
DEDUPE_ROWS = [{'ts': 1.0, 'action': 'dedupe_merge', 'session': COLON, 'dropped_id': 'evt_9',
                'dropped_sessions': [COLON, NEUTRAL]}]
PHONE_WINDOW = {'place': NEUTRAL, 'umo': COLON,
                'recent': [{'ts': 1.0, 'role': 'user', 'text': TEXT,
                            'origin': {'where': NEUTRAL}}]}
PEOPLE_DOC = {'place': NEUTRAL,
              'people': {'10002': {'qq': '10002', 'name': NAME, 'aliases': [ALIAS]}}}


def write_json(path, doc):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False), 'utf-8')


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows), 'utf-8')


def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text('utf-8').splitlines() if x.strip()]


def files(folder):
    folder = Path(folder)
    return sorted(path.relative_to(folder).as_posix() for path in folder.rglob('*') if path.is_file())


def hashes(folder):
    return {name: hashlib.sha256((Path(folder) / name).read_bytes()).hexdigest() for name in files(folder)}


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = rename_places.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def made_up(data):
    """A made-up copy of her data folder: colon sessions, neutral ones and empty ones."""
    data = Path(data)
    data.mkdir(parents=True)
    write_jsonl(data / 'archives' / 'events.jsonl', GLOBAL_EVENTS)
    write_jsonl(data / 'archives' / 'sessions' / 'default_GroupMessage_900001' / 'events.jsonl', A_EVENTS)
    write_jsonl(data / 'archives' / 'sessions' / 'group_900001' / 'events.jsonl', B_EVENTS)
    write_jsonl(data / 'archives' / 'dedupe_log.jsonl', DEDUPE_ROWS)
    write_json(data / 'memory' / 'library.json', LIBRARY_DOC)
    write_json(data / 'users' / '10001.json', USER_ONE)
    write_json(data / 'users' / '10002.json', USER_MANY)
    write_json(data / PHONE_FILE, PHONE_WINDOW)
    write_json(data / PEOPLE_FILE, PEOPLE_DOC)
    return data


class Rename(unittest.TestCase):
    def test_one_run_renames_every_store_and_merges_the_places(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = made_up(Path(tmp) / 'data')
            before = hashes(data)
            code, out, err = run('--data', str(data))
            self.assertEqual(code, 0, out + err)
            after = hashes(data)

            # events.jsonl: every session field is neutral, the empty one stays empty, and no
            # line was lost
            events = read_jsonl(data / 'archives' / 'events.jsonl')
            self.assertEqual(len(events), 3)
            self.assertEqual([e['session'] for e in events], [NEUTRAL, NEUTRAL, ''])
            self.assertEqual(events[0]['provenance']['session'], NEUTRAL)
            self.assertEqual(events[0]['provenance']['sources'][0]['session'], NEUTRAL)
            self.assertEqual(events[0]['source_check']['source_items'][0]['session'], NEUTRAL)
            for rec in events:
                self.assertNotIn('GroupMessage', json.dumps(rec, ensure_ascii=False))

            # the two folders became one; the same event is kept once; sorted by ts
            self.assertEqual(sorted(p.name for p in (data / 'archives' / 'sessions').iterdir()),
                             ['group_900001'])
            merged = read_jsonl(data / 'archives' / 'sessions' / 'group_900001' / 'events.jsonl')
            self.assertEqual([e['id'] for e in merged], ['evt_12', 'evt_10', 'evt_11'])
            self.assertEqual([e['ts'] for e in merged], [199.0, 200.0, 201.0])
            for rec in merged:
                self.assertEqual(rec['session'], NEUTRAL)

            # the library's entries and their sources
            lib = json.loads((data / 'memory' / 'library.json').read_text('utf-8'))
            self.assertEqual([e['provenance']['session'] for e in lib['entries']], [NEUTRAL, NEUTRAL])
            self.assertEqual(lib['entries'][0]['provenance']['sources'][0]['session'], NEUTRAL)

            # users: the same place once, the newest kept last, at most 20
            user = json.loads((data / 'users' / '10001.json').read_text('utf-8'))
            self.assertEqual(user['sessions'], [NEUTRAL, 'private:10003'])
            many = json.loads((data / 'users' / '10002.json').read_text('utf-8'))
            self.assertEqual(len(many['sessions']), 20)
            self.assertEqual(many['sessions'][0], 'private:20002')
            self.assertEqual(many['sessions'][-1], 'private:20021')

            # the dedupe log
            rows = read_jsonl(data / 'archives' / 'dedupe_log.jsonl')
            self.assertEqual(rows[0]['session'], NEUTRAL)
            self.assertEqual(rows[0]['dropped_sessions'], [NEUTRAL, NEUTRAL])

            # the phone window's umo and the names she keeps of people are not a key
            for name in (PHONE_FILE, PEOPLE_FILE):
                self.assertEqual(after[name], before[name], name)

            # the report is numbers, folder names and relative paths: never a record's words
            for text in (TITLE, TEXT, NAME, ALIAS):
                self.assertNotIn(text, out + err)


class Check(unittest.TestCase):
    def test_check_before_and_after(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = made_up(Path(tmp) / 'data')
            before = hashes(data)
            code, out, err = run('--data', str(data), '--check')
            self.assertEqual(code, 1, out + err)
            self.assertIn('还有没改的会话串', out)
            self.assertEqual(hashes(data), before)      # --check writes nothing
            code, out, err = run('--data', str(data))
            self.assertEqual(code, 0, out + err)
            code, out, err = run('--data', str(data), '--check')
            self.assertEqual(code, 0, out + err)
            self.assertIn('都对上了', out)


class Stops(unittest.TestCase):
    def test_one_id_with_two_contents_stops_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = made_up(Path(tmp) / 'data')
            write_jsonl(data / 'archives' / 'sessions' / 'group_900001' / 'events.jsonl',
                        [event('evt_10', 200.0, NEUTRAL, title='另一件事'),
                         event('evt_12', 199.0, NEUTRAL)])
            before = hashes(data)
            code, out, err = run('--data', str(data))
            self.assertEqual(code, 2, out + err)
            self.assertEqual(hashes(data), before)     # nothing written
            self.assertIn('group_900001', err)         # the place and the id are printed
            self.assertIn('evt_10', err)
            self.assertNotIn('另一件事', out + err)     # the words are not
            self.assertNotIn(TITLE, out + err)

    def test_two_platform_prefixes_stop_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = made_up(Path(tmp) / 'data')
            write_jsonl(data / 'archives' / 'events.jsonl',
                        GLOBAL_EVENTS + [event('evt_20', 103.0, 'other:GroupMessage:' + GUILD)])
            before = hashes(data)
            code, out, err = run('--data', str(data))
            self.assertEqual(code, 2, out + err)
            self.assertEqual(hashes(data), before)
            self.assertIn('平台前缀', err)
            self.assertIn('default', err)
            self.assertIn('other', err)

    def test_a_json_that_cannot_be_read_stops_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = made_up(Path(tmp) / 'data')
            half = '{"sender_id": "10001", "sessions": ["' + COLON + '"'
            (data / 'users' / '10001.json').write_text(half, 'utf-8')
            before = hashes(data)
            code, out, err = run('--data', str(data))
            self.assertEqual(code, 2, out + err)
            self.assertEqual(hashes(data), before)
            self.assertIn('users/10001.json', err)     # the path is printed
            self.assertNotIn(COLON, out + err)         # its words are not


class SameAccount(unittest.TestCase):
    def test_group_folders_merge_and_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / 'data'
            root = data / 'archives' / 'sessions'
            for prefix, ident in [('default', 'evt_1'), ('other', 'evt_2')]:
                session = prefix + ':GroupMessage:' + GROUP
                write_jsonl(root / (prefix + '_GroupMessage_' + GROUP) / 'events.jsonl',
                            [event(ident, 1.0, session)])
            code, out, err = run('--data', str(data), '--same-account', 'other,default')
            self.assertEqual(code, 0, out + err)
            self.assertEqual([p.name for p in root.iterdir()], ['group_900001'])
            rows = read_jsonl(root / 'group_900001' / 'events.jsonl')
            self.assertEqual({row['id'] for row in rows}, {'evt_1', 'evt_2'})
            self.assertTrue(all(row['session'] == NEUTRAL for row in rows))
            code, out, err = run('--data', str(data), '--check',
                                 '--same-account', 'other,default')
            self.assertEqual(code, 0, out + err)

    def test_unlisted_prefix_stops_without_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / 'data'
            write_jsonl(data / 'archives' / 'events.jsonl', [
                event('evt_' + prefix, 1.0, prefix + ':GroupMessage:' + GROUP)
                for prefix in ('default', 'other', 'third')])
            before = hashes(data)
            for check in ((), ('--check',)):
                code, out, err = run('--data', str(data), '--same-account',
                                     'other,default', *check)
                self.assertEqual(code, 2, out + err)
                self.assertIn('third', err)
                self.assertEqual(hashes(data), before)

    def test_single_unlisted_prefix_stops_without_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / 'data'
            write_jsonl(data / 'archives' / 'events.jsonl',
                        [event('evt_1', 1.0, 'third:GroupMessage:' + GROUP)])
            before = hashes(data)
            code, out, err = run('--data', str(data), '--same-account', 'other,default')
            self.assertEqual(code, 2, out + err)
            self.assertIn('third', err)
            self.assertEqual(hashes(data), before)

    def test_private_folders_merge(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / 'data'
            root = data / 'archives' / 'sessions'
            for prefix, ident in [('default', 'evt_1'), ('other', 'evt_2')]:
                session = prefix + ':FriendMessage:' + OTHER
                write_jsonl(root / (prefix + '_FriendMessage_' + OTHER) / 'events.jsonl',
                            [event(ident, 1.0, session)])
            code, out, err = run('--data', str(data), '--same-account', 'other,default')
            self.assertEqual(code, 0, out + err)
            self.assertEqual([p.name for p in root.iterdir()], ['private_10001'])
            rows = read_jsonl(root / 'private_10001' / 'events.jsonl')
            self.assertEqual({row['id'] for row in rows}, {'evt_1', 'evt_2'})
            self.assertTrue(all(row['session'] == 'private:10001' for row in rows))


class Guard(unittest.TestCase):
    def test_a_live_data_folder_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            live = Path(tmp) / 'astrbot' / 'data' / 'plugin_data' / 'astrbot_plugin_ams_life'
            made_up(live)
            before = hashes(live)
            code, out, err = run('--data', str(live))
            self.assertEqual(code, 2, out + err)
            self.assertIn('AstrBot', err)
            self.assertEqual(hashes(live), before)

    def test_a_folder_that_is_not_there_and_the_repository_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / 'nothing-here'
            code, out, err = run('--data', str(missing))
            self.assertEqual(code, 2)
            self.assertFalse(missing.exists())
            code, out, err = run('--data', str(ROOT / 'tools'))
            self.assertEqual(code, 2)


class Report(unittest.TestCase):
    def test_temp_message_is_a_private_chat_and_guild_message_a_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = made_up(Path(tmp) / 'data')
            write_jsonl(data / 'archives' / 'events.jsonl', [
                event('evt_t', 1.0, 'default:TempMessage:' + OTHER),
                event('evt_g', 2.0, 'default:GuildMessage:' + GUILD)])
            code, out, err = run('--data', str(data))
            self.assertEqual(code, 0, out + err)
            self.assertIn('TempMessage 算成私聊：1 个', out)
            self.assertIn('GuildMessage 算成群：1 个', out)


class Source(unittest.TestCase):
    def test_no_astrbot_and_no_logging(self):
        tree = ast.parse((ROOT / 'tools' / 'rename_places.py').read_text('utf-8'))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {alias.name.split('.')[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split('.')[0])
        self.assertNotIn('astrbot', imported)
        self.assertNotIn('logging', imported)


if __name__ == '__main__':
    unittest.main()
