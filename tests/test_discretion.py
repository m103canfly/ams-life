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

    def test_origin_keeps_every_person_and_source(self):
        # no cap: whoever is left out of an origin could not be forgotten
        o = d.make_origin('group:1', [str(i) for i in range(100)], ['m%d' % i for i in range(200)])
        self.assertEqual((len(o['people']), len(o['source_ids'])), (100, 200))

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


class Listening(unittest.TestCase):
    """Her phone has everyone's messages, woken or not, each in its own window."""

    def test_everyones_messages_go_into_their_own_window(self):
        r = run_case('listen')
        a = r['phone_heard']['group:900001']['recent']
        self.assertIn(('10003', '我家猫今天学会开冰箱了'), [(x.get('sender_id'), x['text']) for x in a])
        self.assertIn('看[图片]', [x['text'] for x in a])          # a picture is a placeholder, no file
        self.assertNotIn('小爱你看过冰箱猫吗', [x['text'] for x in a])  # her own account is not stored here
        for place in ('group:900002', 'private:10001'):
            self.assertNotIn('冰箱', json.dumps(r['phone_heard'][place], ensure_ascii=False))
        for t in r['turns'][1:]:
            self.assertNotIn('冰箱', t['prompt'], t['session'])
            self.assertNotIn('阿星', t['prompt'], t['session'])

    def test_listening_only_stores(self):
        r = run_case('listen')
        self.assertEqual(r['listen_calls'], {'provider': 0, 'embed': 0, 'network': 0})
        self.assertEqual(r['event_done'], {'send': 0, 'stop': 0, 'result': 0})
        self.assertTrue(r['body_same'])

    def test_window_keeps_24_hours_and_at_most_1000_lines(self):
        r = run_case('listen')
        full = r['phone_full']['group:900001']['recent']
        self.assertEqual(len(full), 1000)
        self.assertEqual(full[-1]['text'], '刷屏第1004条')
        # after 23 hours what others said is still there ...
        self.assertIn('刷屏第1004条', [x['text'] for x in r['phone_23h']['group:900001']['recent']])
        self.assertIn('小爱 在吗', [x['text'] for x in r['phone_23h']['private:10001']['recent']])
        self.assertIn('assistant', [x['role'] for x in r['phone_23h']['private:10001']['recent']])
        later = r['phone_later']
        self.assertEqual([x['text'] for x in later['group:900001']['recent']], ['快一天了', '过了好久'])
        # ... after 24 hours it is gone, her own replies too
        for place in ('group:900002', 'private:10001'):
            self.assertEqual(later[place]['recent'], [])

    def test_forgetting_a_person_removes_his_messages_from_every_window(self):
        r = run_case('listen')
        self.assertEqual(r['forgot']['phone'], 2)
        for win in r['phone_after_forget'].values():
            for x in win['recent']:
                self.assertNotEqual(x.get('sender_id'), '10003')
                self.assertNotIn('10003', x['origin']['people'])


class ForgetWhileWaiting(unittest.TestCase):
    """He is forgotten while work of his is waiting (model, vector service);
    what that work holds is not written back."""

    def check(self, case):
        r = run_case(case)
        self.assertEqual(len(r['fired']), 1, case)
        a = r['after']
        self.assertFalse([m for m in a['memories']
                          if m['sender_id'] == '10001' or '10001' in (m['origin'] or {}).get('people', [])], case)
        self.assertFalse([e for e in a['events'] if '10001' in e['origin']['people']], case)
        self.assertNotIn('10001', a['users'], case)
        self.assertNotIn('private:10001', a['phone'], case)
        for win in a['phone'].values():
            self.assertFalse([x for x in win['recent'] + win['open_loops'] if '10001' in x['origin']['people']], case)
        self.assertFalse([x for x in r['self_model'].get('narrative_items') or []
                          if '10001' in (x.get('origin') or {}).get('people', [])], case)

    def test_strong_event_waiting_for_its_summary(self):
        self.check('wait_event')

    def test_request_waiting_for_the_vector_service(self):
        self.check('wait_embed')

    def test_per_turn_event_archive(self):
        self.check('wait_archive')

    def test_consolidation_with_nothing_to_group(self):
        self.check('wait_consolidate')


class ForgetWhileReplying(unittest.TestCase):
    def test_forgotten_while_the_model_answers_him(self):
        # the reply step keeps the mark its request set, so nothing of him is written back
        r = run_case('wait_reply')
        self.assertEqual(r['forgot']['relationship'], 1)
        a = r['after']
        self.assertFalse([m for m in a['memories']
                          if m['sender_id'] == '10001' or '10001' in (m['origin'] or {}).get('people', [])])
        self.assertNotIn('爬山记得带水哦', [m['text'] for m in a['memories']])
        self.assertNotIn('10001', a['users'])
        for win in a['phone'].values():
            self.assertFalse([x for x in win['recent'] + win['open_loops'] if '10001' in x['origin']['people']])
            self.assertNotIn('爬山记得带水哦', [x['text'] for x in win['recent']])
        # someone else in the same group is untouched
        self.assertIn('小爱 早上好', [x['text'] for x in a['phone']['group:900001']['recent']])


class ForgetWhileWaitingForTheLock(unittest.TestCase):
    def test_forgotten_while_his_message_waits_for_the_session_lock(self):
        # on_message sets the mark; the request and the reply keep it
        r = run_case('wait_lock')
        self.assertEqual(r['forgot']['phone'], 1)  # the line on_message had stored
        a = r['after']
        self.assertFalse([m for m in a['memories']
                          if m['sender_id'] == '10001' or '10001' in (m['origin'] or {}).get('people', [])])
        self.assertFalse([e for e in a['events'] if '10001' in e['origin']['people']])
        self.assertNotIn('10001', a['users'])
        for win in a['phone'].values():
            self.assertFalse([x for x in win['recent'] + win['open_loops'] if '10001' in x['origin']['people']])
            self.assertFalse([x for x in win['open_loops'] if '交报告' in str(x.get('text'))])
        self.assertIn('小爱 早上好', [m['text'] for m in a['memories']])


class MergedRecordsKeepEveryOrigin(unittest.TestCase):
    """Whatever is merged into a record brings its people and source ids into its origin."""

    def test_duplicate_strong_event(self):
        r = run_case('merge_event')
        [ev] = r['merged_raw']
        self.assertIn('看海我也要去，我带相机', ev['source_texts'])
        self.assertEqual(ev['origin']['people'], ['10002', '10003'])
        self.assertEqual(ev['origin']['source_ids'], ['m_lemon', 'm_star'])
        self.assertEqual(ev['origin']['where'], 'group:900001')
        # forgetting by the merged message or by its speaker removes the whole event
        self.assertEqual(r['forgot_by_id']['events'], 1)
        self.assertEqual(r['after_by_id'], [])
        self.assertEqual(r['forgot_person']['events'], 1)
        self.assertEqual(r['after_person'], [])

    def test_one_time_duplicate_cleanup(self):
        r = run_case('cleanup_merge')
        self.assertEqual(r['merged_count'], 1)
        [ev] = r['merged_raw']
        self.assertIn('记得带相机', ev['source_texts'])
        self.assertEqual(ev['origin']['source_ids'], ['m_one', 'm_two'])
        self.assertEqual(r['after'], [])

    def test_per_turn_event_is_made_of_its_own_entries(self):
        r = run_case('turn_event')
        [ev] = r['events']
        self.assertIn('10003', ev['origin']['people'])
        for i in range(3):
            self.assertIn('m_star%d' % i, ev['origin']['source_ids'])
        self.assertNotIn('嗯嗯好', ev['text'])
        [raw] = r['events_raw']
        self.assertEqual(raw['source_texts'], ['我答应你以后一定去看海', '以后我们永远一起去看海，我承诺', '别害怕，我答应过你的'])
        self.assertEqual(r['forgot']['events'], 1)
        self.assertEqual(r['after'], [])

    def test_summary_and_facts_take_the_origin_of_their_whole_group(self):
        r = run_case('summary_origin')
        self.assertTrue(r['summaries'])
        for item in r['summaries']:
            self.assertIn('m_star', item['origin']['source_ids'])
            self.assertIn('10003', item['origin']['people'])
        for item in r['summaries']:
            self.assertNotIn(item['text'], r['after'])


class PicturesInAnEvent(unittest.TestCase):
    """A picture's caption is added to its text when the stretch is cut; its entry
    still counts as one of the event's sources."""

    def check(self, case):
        r = run_case(case)
        for events in (r['events'], r['events_again']):
            [ev] = [e for e in events if '海边的日落' in e['text']]  # the event the picture is in
            self.assertIn('10006', ev['origin']['people'], case)
            self.assertIn('m_pic1', ev['origin']['source_ids'], case)
        for after in (r['after_by_id'], r['after_person']):
            self.assertFalse([e for e in after if '海边的日落' in e['text'] or '10006' in e['origin']['people']], case)

    def test_a_picture_among_words(self):
        self.check('picture_event')

    def test_only_pictures(self):
        r = run_case('picture_only')
        [ev] = r['events']
        for i in range(3):
            self.assertIn('m_pic%d' % i, ev['origin']['source_ids'])
        self.check('picture_only')


class QuotedMessages(unittest.TestCase):
    """Each message is known by its own id; the id of a message it quotes is kept apart."""

    def test_source_ids_are_the_messages_own(self):
        r = run_case('quote')
        self.assertEqual(r['ids']['second'], ['m' + '小爱 这个我也想去'[:6]])  # message_obj.message_id
        self.assertNotEqual(r['ids']['first'], r['ids']['second'])
        win = r['before']['phone']['group:900001']['recent']
        line = [x for x in win if x['text'] == '小爱 这个我也想去'][0]
        self.assertEqual(line['origin']['source_ids'], r['ids']['second'])
        self.assertEqual(line['reply_to'], r['ids']['first'][0])
        mem = [m for m in r['before']['memories'] if m['text'] == '小爱 这个我也想去'][0]
        self.assertEqual(mem['origin']['source_ids'], r['ids']['second'])

    def test_forgetting_the_quoted_message_keeps_the_one_quoting_it(self):
        r = run_case('quote')
        a = r['after_quoted']
        self.assertEqual([m['text'] for m in a['memories']], ['小爱 这个我也想去'])
        texts = [x['text'] for x in a['phone']['group:900001']['recent']]
        self.assertIn('小爱 这个我也想去', texts)
        self.assertNotIn('周末一起去爬山吧', texts)

    def test_forgetting_a_message_by_its_own_id_removes_it(self):
        r = run_case('quote')
        a = r['after_own']
        self.assertEqual(a['memories'], [])
        self.assertNotIn('小爱 这个我也想去', [x['text'] for x in a['phone']['group:900001']['recent']])


class Sweep(unittest.TestCase):
    """Expired lines leave the disk, even in a window nobody writes to any more."""

    def test_lines_are_on_disk_until_something_prunes_them(self):
        r = run_case('sweep')
        for place in ('group:900001', 'group:900002', 'private:10001'):
            self.assertEqual(len(r['disk_start'][place]), 2)
            self.assertEqual(len(r['disk_day_later'][place]), 2)

    def test_reading_a_window_writes_it_back_pruned(self):
        r = run_case('sweep')
        self.assertEqual(r['disk_after_read']['private:10001'], [])
        self.assertEqual(len(r['disk_after_read']['group:900002']), 2)

    def test_the_five_minute_loop_sweeps_every_window(self):
        r = run_case('sweep')
        self.assertTrue(r['loop_running'])
        self.assertEqual(r['disk_after_tick'], {'group:900001': [], 'group:900002': [], 'private:10001': []})

    def test_start_up_sweeps_too(self):
        r = run_case('sweep')
        self.assertEqual(r['disk_before_start']['group:900001'], ['有人吗'])
        self.assertEqual(r['disk_after_start']['group:900001'], [])


class MemoryTrace(unittest.TestCase):
    def test_no_recall_this_turn_means_no_mtrace(self):
        r = run_case('mtrace')
        self.assertIn('[BC]', r['b'])
        self.assertNotIn('mtrace=', r['b'])


class TwoWindowsAtOnce(unittest.TestCase):
    def test_interleaved_requests_keep_their_own_recall(self):
        r = run_case('interleave')
        self.assertIn('memwho=', r['prompt_a'])
        self.assertIn('memwho=', r['prompt_b'])
        for who in ('桃子', '路人'):
            self.assertNotIn(who, r['prompt_a'])
        for who in ('柠檬', '阿星'):
            self.assertNotIn(who, r['prompt_b'])


class WindowFiles(unittest.TestCase):
    def test_window_names_that_used_to_share_a_file_have_their_own(self):
        r = run_case('files')
        self.assertEqual(len(r['files']), 2)
        self.assertEqual(r['one'], ['一号窗口的话'])
        self.assertEqual(r['two'], ['二号窗口的话'])
        self.assertEqual(sorted(r['places']), ['other:a:b', 'other:a_b'])

    def test_a_file_of_another_window_is_not_read(self):
        r = run_case('files')
        self.assertEqual(r['mismatch'], [])


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
