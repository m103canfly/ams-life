"""Forgetting wired into the plugin (step 1-3-2): the forget registry, the owner's deletes in the
panel, no chat command that changes her memory, sources on what only went by person, an id of
its own for every memory and the vector store. Each case runs in a fresh interpreter
(tests/forget_cases.py). All numbers and names are made up.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'forget_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


def where(files, words):
    return {w: sorted(k for k, v in files.items() if w in v) for w in words}


class Registry(unittest.TestCase):
    def test_nothing_of_someone_registered_is_kept(self):
        r = run_case('registered')
        # his message, her reply to him, a registered message and her reply to it: nowhere
        self.assertEqual(where(r['files'], ['晚霞', '是呀好漂亮', '后来被要求忘掉']),
                         {'晚霞': [], '是呀好漂亮': [], '后来被要求忘掉': []})
        self.assertNotIn('10003.json', r['users'])
        # everyone else as before
        self.assertTrue(where(r['files'], ['周末去爬山'])['周末去爬山'])


class OwnerDeletes(unittest.TestCase):
    def test_a_person_everywhere(self):
        r = run_case('owner_person')
        his = ['学弹吉他', '好厉害', '准备一个惊喜', '我帮你保密', '10001', '阿橙']
        self.assertTrue(all(where(r['before'], his).values()))
        self.assertEqual(where(r['after'], his), {w: [] for w in his})
        counts = r['answer']['data']['counts']
        self.assertEqual((counts['memories'], counts['relationship'], counts['phone']), (4, 1, 4))
        self.assertEqual(counts['places'], ['group:900001', 'private:10001'])
        # what AstrBot keeps: his private conversation, his rows of the message history
        self.assertEqual(counts['astrbot'], {'conversations': 1, 'message_history': 2, 'group_contexts': 1})
        self.assertEqual(counts['archived_copies'], 0)                  # nothing was migrated here
        self.assertEqual(r['astrbot']['conversations'], ['default:FriendMessage:10001'])
        self.assertEqual(r['astrbot']['history_left'], ['10002', '10004'])
        self.assertEqual(r['astrbot']['group_histories']['default:GroupMessage:900001'], [])
        self.assertEqual(r['astrbot']['group_histories']['default:GroupMessage:900002'],
                         [{'role': 'user', 'content': 'second'}])
        # registered: what he says afterwards is not kept either
        self.assertEqual(r['registry'], [{'kind': 'qq', 'place': '*', 'qq': '10001', 'source_id': '',
                                          'note': 'owner:panel'}])
        self.assertEqual(where(r['later'], ['又回来啦'])['又回来啦'], [])
        # others untouched
        self.assertTrue(where(r['after'], ['周末去爬山', '晚上好呀'])['晚上好呀'])
        self.assertEqual(r['bad_person']['status'], 'error')

    def test_group_context_missing_api_does_not_block_local_deletion(self):
        self._group_context_failure('group_missing_api')

    def test_group_context_error_does_not_block_local_deletion(self):
        self._group_context_failure('group_update_error')

    def _group_context_failure(self, case):
        r = run_case(case)
        self.assertEqual(r['answer']['status'], 'ok')
        self.assertGreater(r['answer']['data']['counts']['phone'], 0)
        self.assertEqual(r['answer']['data']['counts']['astrbot']['group_contexts'], 0)
        self.assertTrue(any(row['qq'] == '10001' and row['kind'] == 'qq' for row in r['registry']))
        self.assertEqual(where(r['after'], ['m-one']), {'m-one': []})
        self.assertEqual(r['history'], [{'role': 'user', 'content': 'first'}])

    def test_one_memory_and_her_reply_to_it(self):
        r = run_case('owner_memory')
        counts = r['answer']['data']['counts']
        self.assertEqual((counts['memories'], counts['phone'], counts['places']), (2, 2, ['group:900001']))
        # the message, and her reply to it (it came from that message), everywhere
        self.assertEqual(where(r['after'], ['周末去爬山', '记得带水']), {'周末去爬山': [], '记得带水': []})
        for kept in ('学弹吉他', '我帮你保密', '晚上好呀'):
            self.assertTrue(where(r['after'], [kept])[kept], kept)
        self.assertEqual(r['registry'], [{'kind': 'source', 'place': 'group:900001', 'qq': '', 'source_id': 'm-hike',
                                          'note': 'owner:panel'}])
        self.assertEqual(r['missing']['status'], 'error')

    def test_other_stores(self):
        r = run_case('other_stores')
        self.assertEqual(r['image_cache'], {})                     # the picture he sent: its description
        self.assertEqual([json.loads(x)['kept_id'] for x in r['dedupe'].splitlines() if x.strip()], ['evt_hike'])
        # by message: what came from it, and what does not say where it came from; the numbers stay
        rel = r['user_10002']['relationship']
        self.assertEqual(rel['we_memory'], [])
        self.assertEqual([a['text'] for a in rel['annotations']], ['爱拍照'])
        self.assertEqual(rel['milestones'], [])
        self.assertEqual(rel['transactive_map'], {})
        self.assertEqual(rel['state'], {'trust': 0.6, 'closeness': 0.5})
        self.assertEqual(r['user_10002']['interactions'], 7)
        self.assertEqual(r['events'].strip(), '')
        self.assertEqual(r['vector_ids'], [])                      # their vectors went with them
        # the library copied before the vectors moved out still holds the old data: the panel says so
        self.assertEqual(r['by_message']['data']['counts']['archived_copies'], 1)


class Review(unittest.TestCase):
    """PR #9 review: a registry that cannot be read never empties the library; deleting a person
    does not touch someone else who merely has an everyday name or a number inside a timestamp;
    the old rollback / restore endpoints are gone; a registered person's picture is not described."""

    def test_unreadable_registry_writes_nothing_and_drops_nothing(self):
        r = run_case('registry_broken')
        self.assertEqual(r['after'], r['before'])                   # nothing lost, nothing new
        self.assertEqual(r['vectors'][1], r['vectors'][0])
        self.assertEqual(r['notebook'], ['今天群里很热闹'])
        self.assertFalse(r['phone_food'])

    def test_deleting_someone_leaves_unrelated_records_alone(self):
        r = run_case('mention')
        self.assertTrue(r['untouched'])
        self.assertEqual(r['user_10002'].get('destination_map'), {})   # this one did draw from him
        self.assertEqual(r['user_10002']['state'], {'trust': 0.5})

    def test_latest_lines_and_evidence_count(self):
        r = run_case('mention')
        self.assertEqual(r['user_10011'].get('destination_map'), {})
        self.assertEqual(r['user_10012'].get('social_world'), [])

    def test_old_rollback_and_restore_are_gone(self):
        r = run_case('old_endpoints')
        self.assertEqual((r['routes'], r['methods']), ([], []))
        self.assertTrue(r['backup_restore_kept'])      # the owner's whole-folder restore stays

    def test_no_picture_description_for_someone_registered(self):
        r = run_case('picture')
        self.assertFalse(r['blocked'])
        self.assertEqual(r['allowed'], ['k-10002'])

    def test_migration_does_not_reread_the_library_for_every_id(self):
        r = run_case('migrate_many')
        self.assertEqual(r['ids'], [30, 30, True])
        self.assertLessEqual(r['reads_at_start'], 5)


class ReviewOfPR10(unittest.TestCase):
    """PR #9 re-review (fixed on PR #10): a delete whose library write failed says so; a whole
    backup restored never brings back someone deleted."""

    def test_a_delete_that_could_not_write_the_library_says_so(self):
        r = run_case('forget_broken')
        self.assertEqual(r['page']['status'], 'error')
        self.assertIn('AstrBot 那边也还没删', r['page']['message'])
        self.assertTrue(r['still_there'])
        self.assertEqual(r['retry'], 'ok')
        self.assertTrue(r['gone_after_retry'])

    def test_restoring_a_backup_does_not_bring_anyone_back(self):
        r = run_case('restore')
        self.assertEqual(r['restore']['status'], 'ok', r['restore'])
        self.assertEqual(r['restore']['data']['deleted_again'], {'people': 1, 'messages': 1})
        self.assertFalse(r['guitar'])
        self.assertFalse(r['hike'])
        self.assertFalse(r['user_10001'])
        self.assertFalse(r['phone_guitar'])
        self.assertIn(['qq', '10001'], r['registry'])

    def test_restoring_deletes_again_only_what_the_owner_deleted(self):
        r = run_case('restore')
        # 10003 is forgotten in group 1 only, 10004 opted back in: what the registry lets her keep stays
        self.assertEqual(r['kept'], {'蛋糕': True, '下雨': True, '我回来啦': True})
        self.assertEqual(r['users'], {'10002': True, '10003': True, '10004': True})


class NoChatCommands(unittest.TestCase):
    def test_saying_it_changes_nothing(self):
        r = run_case('chat_commands')
        self.assertIn('小爱 周末一起去爬山吧', r['after'])         # still there, unchanged
        self.assertEqual(r['deleted_flags'], [])
        for inject in r['injects']:
            for word in ('已删除', '待确认', '已恢复', '回滚到上一版本'):
                self.assertNotIn(word, inject or '')
        # "其实是… 改成…" is kept as said; the older memory is not rewritten
        self.assertIn('小爱 其实是周日去爬山 改成周日', r['after'])


class Ids(unittest.TestCase):
    def test_the_same_words_in_two_groups(self):
        r = run_case('same_words')
        a, b = r['entries']
        self.assertEqual(a['text'], b['text'])
        self.assertNotEqual(a['id'], b['id'])
        self.assertEqual((a['where'], b['where']), ('group:900001', 'group:900002'))
        self.assertEqual(r['stored'], sorted([a['id'], b['id']]))   # each its own vector
        self.assertFalse(a['has_vector_in_json'] or b['has_vector_in_json'])

    def test_migration(self):
        r = run_case('migrate')
        ids = r['ids']
        self.assertTrue(all(ids) and len(set(ids)) == len(ids))
        self.assertEqual((ids[0], ids[3]), ('same', 'm9'))          # the first of a shared id keeps it
        self.assertEqual(r['vectors_in_json'], 0)
        self.assertEqual(r['vectors_back'], [True] * 5)             # every memory gets its own vector back
        self.assertEqual(len(r['archive']), 2)                      # archived before the ids, before the vectors
        self.assertEqual((r['archive_again'], r['ids_again']), (2, ids))   # starting again: nothing

    def test_recall_is_the_same_after_the_migration(self):
        self.assertEqual(run_case('recall_before')['inject'], run_case('recall_after')['inject'])


if __name__ == '__main__':
    unittest.main()
