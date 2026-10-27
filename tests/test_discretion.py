"""One her, memories with an origin, and the discretion table (ams-life step 1).

The table itself is unit-tested on discretion.py; the conversations in
discretion_cases.py check it end to end through the plugin's hooks, each in a
fresh interpreter like the golden test. All numbers and names are made up.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import discretion as d  # noqa: E402

_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'discretion_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, timeout=300)
            if proc.returncode != 0:
                raise AssertionError(f'case {case} failed:\n{proc.stdout}\n{proc.stderr}')
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


def flat(text):
    return re.sub(r'\s+', '', str(text or ''))


def pieces(text, n=5):
    t = flat(text)
    return {t[i:i + n] for i in range(len(t) - n + 1)}


class Table(unittest.TestCase):
    def test_places(self):
        self.assertEqual(d.place_of('default:GroupMessage:42'), 'group:42')
        self.assertEqual(d.place_of('ams-life_GroupMessage_42'), 'group:42')
        self.assertEqual(d.place_of('default:FriendMessage:7'), 'private:7')
        self.assertEqual(d.place_of('group:42'), 'group:42')

    def test_rows(self):
        public = d.make_origin('group:1', ['7'])
        private = d.make_origin('private:7', ['7'])
        own = d.make_origin('self')
        web = d.make_origin('web:example')
        self.assertEqual(public['visibility'], d.PUBLIC)
        self.assertEqual(private['visibility'], d.PRIVATE)
        # said openly in a group
        self.assertEqual(d.verdict(public, 'group:1'), d.FULL)
        self.assertEqual(d.verdict(public, 'group:2'), d.ANON)
        self.assertEqual(d.verdict(public, 'private:8'), d.ANON)
        # told in private
        self.assertEqual(d.verdict(private, 'private:7'), d.FULL)
        self.assertEqual(d.verdict(private, 'group:1'), d.DROP)
        self.assertEqual(d.verdict(private, 'private:8'), d.DROP)
        # her own, web pages
        for o in (own, web):
            for here in ('group:1', 'private:8'):
                self.assertEqual(d.verdict(o, here), d.FULL)

    def test_unknown_origin_is_never_shown(self):
        self.assertEqual(d.verdict(d.origin_of({'text': 'x'}), 'group:1'), d.DROP)
        self.assertEqual(d.verdict({}, 'private:7'), d.DROP)

    def test_merged_origin_is_as_narrow_as_its_narrowest_source(self):
        m = d.merge([d.make_origin('group:1', ['5']), d.make_origin('private:7', ['7'])])
        self.assertEqual(m['visibility'], d.PRIVATE)
        self.assertEqual(d.verdict(m, 'group:1'), d.DROP)
        self.assertEqual(sorted(m['people']), ['5', '7'])

    def test_old_records_get_an_origin_from_their_provenance(self):
        o = d.origin_of({'provenance': {'session': 'default:FriendMessage:7', 'sender_id': '7',
                                        'message_refs': ['m1']}})
        self.assertEqual(o, {'where': 'private:7', 'people': ['7'], 'source_ids': ['m1'], 'visibility': d.PRIVATE})

    def test_anonymize(self):
        self.assertEqual(d.anonymize('芒果：明天考试（10001）', ['芒果', '10001']), '有人：明天考试（有人）')


class PrivateStaysPrivate(unittest.TestCase):
    def test_private_never_reaches_a_group_prompt(self):
        r = run_case('private')
        secret = set().union(*(pieces(t) for t in r['private_texts']))
        groups = [t for t in r['turns'] if 'GroupMessage' in t['session']]
        self.assertEqual(len(groups), 3)
        for t in groups:
            leaked = [p for p in secret if p in flat(t['prompt'])]
            self.assertEqual(leaked, [], t['session'])

    def test_private_is_still_remembered_in_the_same_chat(self):
        r = run_case('private')
        self.assertIn('惊喜蛋糕给大家', r['turns'][1]['prompt'])


class PublicWithoutNames(unittest.TestCase):
    def test_other_group_hears_what_but_not_who(self):
        r = run_case('anon')
        b = r['turns'][-1]
        self.assertIn('GroupMessage:900002', b['session'])
        self.assertIn('爬山', b['prompt'])
        self.assertIn('（别处）有人：', b['prompt'])
        for who in ('柠檬', '阿星', '10002', '10003'):
            self.assertNotIn(who, b['prompt'])


class SaidInTheGroupToo(unittest.TestCase):
    """No exception any more: what he told her in private stays in that private chat,
    even after he says nearly the same thing in a group himself."""

    def test_private_wording_stays_out_of_the_group_he_repeated_it_in(self):
        r = run_case('echo')
        a = r['turns'][2]
        self.assertIn('GroupMessage:900001', a['session'])
        self.assertNotIn('惊喜蛋糕给大家', a['prompt'])
        self.assertFalse([ln for ln in a['prompt'].split('\n') if '（别处）' in ln and '惊喜蛋糕' in ln])

    def test_other_group_still_does_not_hear_the_private_wording(self):
        r = run_case('echo')
        b = r['turns'][3]
        self.assertIn('GroupMessage:900002', b['session'])
        self.assertNotIn('惊喜蛋糕给大家', b['prompt'])
        self.assertNotIn('芒果', b['prompt'])


class Phone(unittest.TestCase):
    """She has a phone: what was said stays in its own chat window; the body keeps no text."""

    def test_group_event_is_made_only_from_that_group(self):
        r = run_case('strong_event')
        secret = set().union(*(pieces(t) for t in r['private_texts']))
        group_events = [e for e in r['events'] if e['origin']['where'] == 'group:900001']
        self.assertTrue(group_events)
        for e in group_events:
            self.assertEqual([p for p in secret if p in flat(e['text'])], [])
            self.assertEqual(e['origin']['people'], ['10002'])
            self.assertTrue(e['origin']['source_ids'])
        for t in r['turns']:
            if 'GroupMessage' in t['session']:
                self.assertEqual([p for p in secret if p in flat(t['prompt'])], [], t['session'])

    def test_body_state_file_keeps_no_words(self):
        r = run_case('strong_event')
        said = set().union(*(pieces(t, 4) for t in r['all_texts']))
        self.assertTrue(r['her_state'])
        self.assertEqual([p for p in said if p in flat(r['her_state'])], [])
        # her replies are in the window they were said in
        self.assertIn('好呀，惊喜蛋糕我帮你保密', [x['text'] for x in r['phone']['private:10001']['recent']])
        self.assertNotIn('好呀，惊喜蛋糕我帮你保密', [x['text'] for x in r['phone']['group:900001']['recent']])

    def test_open_loops_stay_in_their_window(self):
        r = run_case('loops')
        w = r['windows_after_talk']
        private = [x for x in w['private:10001']['open_loops'] if x['text'] == '记得提醒我明天交报告']
        # the group's "报告我交了" does not close the private reminder ...
        self.assertEqual(private[0]['status'], 'open')
        # ... and the group's own reminder is not merged into it
        self.assertEqual(private[0]['mentioned'], 1)
        group = w['group:900001']['open_loops']
        self.assertEqual([(x['text'], x['origin']['where']) for x in group],
                         [('记得提醒我明天交报告', 'group:900001')])
        self.assertEqual(w['group:900002']['open_loops'], [])
        # loops show only in their own window
        prompts = [t['prompt'] for t in r['turns']]
        self.assertIn('loops=', prompts[0])
        self.assertNotIn('loops=', prompts[1])
        self.assertNotIn('loops=', prompts[3])
        self.assertNotIn('交报告', prompts[3])

    def test_open_loop_cap_is_per_window(self):
        r = run_case('loops')
        w = r['windows_after_many']
        self.assertEqual(len(w['group:900001']['open_loops']), 20)
        self.assertEqual(w['private:10001']['open_loops'], r['windows_after_talk']['private:10001']['open_loops'])

    def test_old_one_body_state_is_split_into_windows(self):
        r = run_case('migrate_her')
        her = json.dumps(r['her'], ensure_ascii=False)
        for word in ('保密', '爬山', '一句话', '报告', '蛋糕', '惊喜'):
            self.assertNotIn(word, her)
        self.assertEqual([x['text'] for x in r['phone']['private:10001']['recent']], ['蛋糕的事我帮你保密'])
        self.assertEqual([x['text'] for x in r['phone']['group:900001']['recent']], ['爬山记得带水哦'])
        self.assertEqual([x['text'] for x in r['phone']['group:900001']['open_loops']], ['记得提醒我交报告'])
        # lines whose window is unknown go nowhere; the old file is kept in the archive
        self.assertNotIn('不知道从哪来的一句话', json.dumps(r['phone'], ensure_ascii=False))
        self.assertNotIn('记得提醒我买蛋糕', json.dumps(r['phone'], ensure_ascii=False))
        self.assertEqual(r['archive'], ['her.before_phone.json'])


class OneBody(unittest.TestCase):
    def test_happy_in_group_a_is_still_happy_in_group_b(self):
        r = run_case('one_body')
        self.assertEqual(r['cores'], ['her'])
        self.assertGreater(r['v_after_a'], r['v_start'] + 0.3)
        v_b = float(re.search(r'v=(-?[\d.]+)', r['turns'][-1]['prompt']).group(1))
        self.assertGreater(v_b, r['v_start'] + 0.3)


class Forget(unittest.TestCase):
    def test_forgetting_a_person_removes_memories_events_and_relationship(self):
        r = run_case('forget')
        before, after = r['before'], r['after_person']
        # he was there in every store before
        self.assertTrue(any('10001' in m['origin']['people'] for m in before['memories']))
        self.assertTrue(any('10001' in e['origin']['people'] for e in before['events']))
        self.assertIn('10001', before['users'])
        self.assertIn('private:10001', before['rooms'])
        # and nowhere after
        self.assertFalse(any('10001' in m['origin']['people'] or m['sender_id'] == '10001'
                             for m in after['memories']))
        self.assertFalse(any('10001' in e['origin']['people'] for e in after['events']))
        self.assertEqual(sum(after['event_files'].values()), 0)
        self.assertNotIn('10001', after['users'])
        self.assertNotIn('private:10001', after['rooms'])
        self.assertFalse(any('惊喜蛋糕' in m['text'] or '气死' in m['text'] for m in after['memories']))
        # and her phone: his private window is gone, nothing from him in the group's
        self.assertIn('private:10001', before['phone'])
        self.assertNotIn('private:10001', after['phone'])
        for win in after['phone'].values():
            for item in win['recent'] + win['open_loops']:
                self.assertNotIn('10001', item['origin']['people'])
        # other people are untouched
        self.assertEqual(len([m for m in after['memories'] if m['sender_id'] == '10002']), 2)
        self.assertIn('10002', after['users'])

    def test_forgetting_a_message_removes_what_came_from_it(self):
        r = run_case('forget')
        self.assertEqual(r['forgot_source']['memories'], 1)
        texts = [m['text'] for m in r['after_source']['memories']]
        self.assertNotIn('小爱，我们群周末要去爬山', texts)
        self.assertIn('小爱，周末爬山带什么好', texts)


class ForgetWhileConsolidating(unittest.TestCase):
    def test_forgetting_during_consolidation_is_not_undone(self):
        r = run_case('consolidate')
        self.assertEqual(len(r['forgot_meanwhile']), 1)
        self.assertTrue(r['forgot_meanwhile'][0]['memories'])
        after = r['after']['memories']
        self.assertFalse(any(m['sender_id'] == '10001' or '10001' in m['origin']['people'] for m in after))
        self.assertFalse(any('蛋糕' in m['text'] for m in after))

    def test_consolidation_still_saves_when_nothing_was_forgotten(self):
        r = run_case('consolidate')
        summaries = [m['text'] for m in r['after_control']['memories'] if m['sender_id'] is None]
        self.assertTrue(summaries)


class Migration(unittest.TestCase):
    def test_per_session_files_fold_into_one_library_and_one_body(self):
        r = run_case('migrate')
        by_id = {x['id']: x['origin'] for x in r['library']}
        self.assertEqual(sorted(by_id), ['g1', 'p1'])  # BioCore's cross-session copy is not carried over
        self.assertEqual(by_id['p1']['where'], 'private:10001')
        self.assertEqual(by_id['p1']['visibility'], 'private')
        self.assertEqual(by_id['g1']['where'], 'group:900001')
        self.assertEqual(r['rooms'], ['group:900001', 'private:10001'])
        # old files are moved aside, not deleted
        self.assertEqual(r['memory_dir'], ['library.json'])
        self.assertEqual(r['legacy'], ['default_FriendMessage_10001.json', 'default_GroupMessage_900001.json'])
        self.assertEqual(r['states_dir'], ['her.json'])
        self.assertEqual(r['states_archive'], ['default_FriendMessage_10001.json', 'default_GroupMessage_900001.json'])
        # the most recently updated state is where the one body starts
        self.assertAlmostEqual(r['v'], 0.1)
        # what was said in each old session went into that session's window; the body keeps none of it
        self.assertEqual([x['text'] for x in r['phone']['group:900001']['open_loops']], ['记得提醒我交报告'])
        self.assertEqual([x['text'] for x in r['phone']['group:900001']['recent']], ['爬山记得带水哦'])
        self.assertEqual([x['text'] for x in r['phone']['private:10001']['recent']], ['蛋糕的事我帮你保密'])
        her = json.dumps(r['her'], ensure_ascii=False)
        for word in ('保密', '爬山', '报告', '蛋糕'):
            self.assertNotIn(word, her)

    def test_migrated_private_memory_stays_out_of_groups(self):
        r = run_case('migrate')
        for t in r['turns']:
            if 'GroupMessage' in t['session']:
                self.assertNotIn('惊喜蛋糕', t['prompt'])


if __name__ == '__main__':
    unittest.main()
