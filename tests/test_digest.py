"""What happened today in each chat window (digest.py, mixin_digest.py): the material and the
answer checks on their own, then the plugin in a fresh interpreter (tests/digest_cases.py). All
numbers, names and messages are made up; the model is a fake one.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import digest  # noqa: E402

_CACHE = {}
DAY = '2026-10-04'
T = time.mktime(time.strptime(DAY + ' 20:00:00', '%Y-%m-%d %H:%M:%S'))


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'digest_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


def line(i, who, name, text, role='user', day_offset=0):
    return {'ts': T + i * 60 + day_offset * 86400, 'role': role, 'sender_id': who, 'sender_name': name,
            'msg_id': 'm%d' % i, 'text': text}


class Registry:
    def __init__(self, people=(), ids=()):
        self.people, self.ids = set(people), set(ids)

    def may_keep(self, qq='', place='', at=None, source_id=''):
        return qq not in self.people and source_id not in self.ids

    def may_keep_all(self, people=(), place='', at=None, source_ids=()):
        return not (set(people) & self.people or set(source_ids) & self.ids)


LINES = [line(0, '10002', '柠檬', '周末一起打副本吗'),
         line(1, '10001', '阿橙', '我来 @柠檬 柠柠别鸽'),
         line(2, '', '', '好呀', role='assistant'),
         line(3, '10003', '阿星', '我家猫叫团子'),
         line(4, '10001', '阿橙', '我的号码是13812345678'),
         line(5, '10002', '柠檬', '昨天的事', day_offset=-1)]


class Material(unittest.TestCase):
    def test_her_own_lines_by_their_origin(self):
        hers = dict(line(6, '', '', '好呀柠檬', role='assistant'), msg_id='',
                    origin={'where': 'group:1', 'people': ['10002'], 'source_ids': ['m0']})
        kept = digest.day_lines(LINES[:2] + [hers], DAY, 'group:1')
        self.assertEqual(len(digest.day_lines(LINES[:2] + [hers], DAY, 'group:1', Registry(people={'10002'}))), 1)
        self.assertEqual(len(digest.day_lines(LINES[1:2] + [hers], DAY, 'group:1', Registry(ids={'m0'}))), 1)
        _text, codes, shown = digest.material(kept)
        only_hers = {'title': '她答应了', 'what': '她答应了', 'who': [], 'lines': [3], 'who_ok': True, 'lines_ok': True}
        self.assertEqual(digest.sources(only_hers, codes, shown, kept), (['10002'], ['m0']))

    def test_only_today_and_nothing_ruled_out(self):
        kept = digest.day_lines(LINES, DAY, 'group:1', Registry(people={'10003'}, ids={'m4'}))
        self.assertEqual([x['msg_id'] for x in kept], ['m0', 'm1', 'm2'])

    def test_codes_not_names_nor_numbers(self):
        kept = digest.day_lines(LINES, DAY, 'group:1')
        text, codes, shown = digest.material(kept, {'10002': {'柠柠'}, '10009': {'鹿鹿'}})
        self.assertEqual(codes, {'P1': '10002', 'P2': '10001', 'P3': '10003', 'Q1': '10009'})
        self.assertEqual(text.splitlines(), ['1 P1：周末一起打副本吗', '2 P2：我来 @P1 P1别鸽', '3 她：好呀',
                                             '4 P3：我家猫叫团子', '5 P2：我的号码是#'])
        self.assertEqual(len(shown), 5)
        for word in ('柠檬', '阿橙', '阿星', '柠柠', '1381234', '10002'):
            self.assertNotIn(word, text)

    def test_red_lines_by_the_switch(self):
        kept = digest.day_lines(LINES, DAY, 'group:1')
        text, _codes, shown = digest.material(kept, red=lambda t: 'pets' if '猫' in t else '')
        self.assertNotIn('猫', text)
        self.assertEqual(len(shown), 4)

    def test_only_the_most_recent_lines(self):
        many = [line(i, '10002', '柠檬', '第%d句' % i) for i in range(digest.MAX_LINES + 20)]
        text, _codes, shown = digest.material(many)
        self.assertEqual(len(shown), digest.MAX_LINES)
        self.assertTrue(text.splitlines()[0].endswith('第20句'))


class Answer(unittest.TestCase):
    codes = {'P1': '10002', 'P2': '10001', 'Q1': '10009'}

    def parse(self, items, **kw):
        return digest.parse_answer('好的：\n' + json.dumps({'events': items}, ensure_ascii=False), self.codes, 4, **kw)

    def test_checked_item_by_item(self):
        got = self.parse([
            {'title': 'P1约打副本', 'what': 'P1约大家周末打副本，P2要来', 'who': ['P1', 'P2'], 'lines': [1, 2]},
            {'title': 'P5的事', 'what': 'P5来了', 'who': ['P1'], 'lines': [1]},          # an unknown code
            {'title': '报号码', 'what': 'P2说了12345678', 'who': ['P2'], 'lines': [4]},   # a long number
            {'title': '', 'what': '没有标题', 'who': [], 'lines': []},
            {'title': '长' * 30, 'what': '太长的标题', 'who': [], 'lines': []},
            {'title': '聊抽卡', 'what': '大家聊抽卡', 'who': ['P9'], 'lines': [2, 9]}])   # wrong code and line
        self.assertEqual([g['title'] for g in got], ['P1约打副本', '聊抽卡'])
        self.assertEqual((got[0]['who_ok'], got[0]['lines_ok']), (True, True))
        self.assertEqual((got[1]['who'], got[1]['lines'], got[1]['who_ok'], got[1]['lines_ok']), ([], [2], False, False))

    def test_at_most_five_and_nonsense_is_nothing(self):
        items = [{'title': '事%d' % i, 'what': '经过%d' % i, 'who': ['P1'], 'lines': [1]} for i in range(8)]
        self.assertEqual(len(self.parse(items)), digest.MAX_EVENTS)
        self.assertEqual(digest.parse_answer('不知道', self.codes, 4), [])
        self.assertEqual(digest.parse_answer('{"events": "x"}', self.codes, 4), [])

    def test_red_lines_and_judgements_by_the_switch(self):
        item = [{'title': 'P1生病了', 'what': 'P1说自己生病了，人品不行', 'who': ['P1'], 'lines': [1]}]
        self.assertEqual(len(self.parse(item)), 0)    # the defaults: the red lines themselves
        self.assertEqual(len(self.parse(item, red=lambda t: '', judge=lambda t: '')), 1)   # the switch off

    def test_where_it_comes_from(self):
        kept = digest.day_lines(LINES, DAY, 'group:1')
        _text, codes, shown = digest.material(kept)
        named_lines = {'title': 'P1约打副本', 'what': 'P1约大家', 'who': ['P1'], 'lines': [1, 3],
                       'who_ok': True, 'lines_ok': True}
        self.assertEqual(digest.sources(named_lines, codes, shown, kept), (['10002'], ['m0', 'm2']))
        # no lines, or a wrong one: everyone who spoke today, every message of the day
        no_lines = dict(named_lines, lines=[], lines_ok=False)
        self.assertEqual(digest.sources(no_lines, codes, shown, kept),
                         (['10001', '10002', '10003'], ['m0', 'm1', 'm2', 'm3', 'm4']))
        # a wrong person: everyone who spoke, the lines it names
        wrong_who = dict(named_lines, who=[], who_ok=False)
        self.assertEqual(digest.sources(wrong_who, codes, shown, kept)[0], ['10001', '10002', '10003'])
        # a code in the text counts as someone it is about
        in_text = dict(named_lines, what='P1约了P2', who=['P1'])
        self.assertEqual(digest.sources(in_text, codes, shown, kept)[0], ['10001', '10002'])
        self.assertEqual(digest.named('P1约了P2和Q1', codes, {'10002': '柠檬', '10001': '阿橙'}), '「柠檬」约了「阿橙」和某人')   # framed (the owner, 10-29); 某人 not


def ev(title, where, people=(), digest_kind=True, importance=0.5, ts=0.0, what=''):
    e = {'title': title, 'event': what or title, 'importance': importance, 'ts': ts,
         'origin': {'where': where, 'people': list(people)}}
    if digest_kind:
        e['kind'] = 'daily_digest'
    return e


class WhereTheyAreUsed(unittest.TestCase):
    def test_fairly_between_windows(self):
        events = [ev('%s-%d' % (g, i), g, ts=n) for n, (g, i) in enumerate((g, i) for g in 'ABCDEF' for i in range(4))]
        events.append(ev('F大事', 'F', ['1', '2', '3'], digest_kind=False, ts=99))
        got = [e['title'] for e in digest.pick_fairly(events, 8)]
        self.assertEqual(len(got), 8)
        self.assertEqual({t[0] for t in got}, set('ABCDEF'))      # every window first
        self.assertIn('F大事', got)                                 # a strong event before the notes
        self.assertEqual(got, [e['title'] for e in events if e['title'] in got])   # in their order
        self.assertEqual(len(digest.pick_fairly(events[:3], 8)), 3)

    def test_more_windows_than_room(self):
        events = [ev('%d' % i, 'w%d' % i, ['p'] * (i % 3), ts=i) for i in range(6)]
        got = [e['title'] for e in digest.pick_fairly(events, 2)]
        self.assertEqual(got, ['2', '5'])                           # the windows of the weightiest

    def test_only_here_only_to_do_with_it_at_most_two(self):
        events = [ev('柠檬约周末打副本', 'g1'), ev('大家聊抽卡', 'g1'), ev('阿橙的副本攻略', 'g1', what='周末副本的打法'),
                  ev('副本开荒', 'g1', what='大家约好周末副本开荒'), ev('桃子也想打副本', 'g2', what='周末也想打副本'),
                  ev('周末打副本', 'g1', digest_kind=False)]
        got = [e['title'] for e in digest.for_reply('周末的副本几点开始', events, 'g1')]
        self.assertEqual(len(got), 2)
        self.assertNotIn('桃子也想打副本', got)
        self.assertNotIn('大家聊抽卡', got)
        self.assertNotIn('周末打副本', got)                         # a strong event is not one of these
        self.assertEqual(digest.for_reply('你好呀', events, 'g1'), [])


class Nightly(unittest.TestCase):
    def test_off_by_default_and_once_a_night(self):
        r = run_case('nightly')
        self.assertEqual((r['off'], r['calls_off'], r['before_time']), ({}, 0, {}))
        self.assertEqual(r['first'], {'group:900001': {'called': 1, 'written': 3},
                                      'private:10004': {'called': 1, 'written': 1}})
        self.assertEqual((r['again'], r['after_restart'], r['calls']), ({}, {}, 2))
        self.assertNotIn('900001', r['tried_file'])     # tried windows by a hash: no numbers kept
        self.assertNotIn('10004', r['tried_file'])

    def test_what_the_model_sees(self):
        group, private = run_case('nightly')['prompts']
        self.assertIn('一个群今天', group)
        self.assertIn('一个私聊今天', private)
        for prompt in (group, private):
            for word in ('柠檬', '阿橙', '阿星', '桃子', '10001', '10002', '10004', '900001'):
                self.assertNotIn(word, prompt)
        # the person and the message the registry rules out are not there at all
        self.assertNotIn('团子', group)
        self.assertNotIn('1381234', group)
        self.assertIn('2 P2：我来我来 @P1', group)

    def test_origins(self):
        evs = {e['title']: e for e in run_case('nightly')['events']}
        self.assertEqual(sorted(evs), sorted(['「柠檬」约周末打副本', '有人在聊抽卡', '「桃子」说了蓝莓计划', '「阿橙」说了件事']))
        one = evs['「柠檬」约周末打副本']
        self.assertEqual(one['event'], '「柠檬」约大家周末一起打副本，「阿橙」说要来')
        self.assertEqual(one['origin'], {'where': 'group:900001', 'people': ['10001', '10002'],
                                         'source_ids': ['g1', 'g2'], 'visibility': 'public'})
        # no lines named / a wrong one: the whole day (but nothing ruled out)
        for title in ('有人在聊抽卡', '「阿橙」说了件事'):
            self.assertEqual(evs[title]['origin'], {'where': 'group:900001', 'people': ['10001', '10002'],
                                                    'source_ids': ['g1', 'g2', 'g3', 'g4'], 'visibility': 'public'})
        self.assertEqual(evs['「桃子」说了蓝莓计划']['origin'], {'where': 'private:10004', 'people': ['10004'],
                                                        'source_ids': ['p1'], 'visibility': 'private'})

    def test_private_stays_there(self):
        seen = run_case('nightly')['seen']
        self.assertNotIn('蓝莓', ''.join(seen['group']) + ''.join(seen['g2']))
        self.assertIn('「桃子」说了蓝莓计划', seen['private'])
        self.assertIn('「柠檬」约周末打副本', seen['group'])
        self.assertIn('有人约周末打副本', seen['g2'])       # another group: without names (nor their frames)
        self.assertNotIn('柠檬', ''.join(seen['g2']))

    def test_her_notebook_uses_them(self):
        nb = run_case('nightly')['notebook']
        self.assertIn('事件：「柠檬」约周末打副本：「柠檬」约大家周末一起打副本，「阿橙」说要来', nb['group'])
        self.assertNotIn('蓝莓', ''.join(nb['group']))
        self.assertIn('事件：「桃子」说了蓝莓计划：「桃子」跟她说起蓝莓计划的安排', nb['private'])

    def test_deleted_with_the_message_and_the_person(self):
        r = run_case('nightly')
        self.assertEqual(r['forget_message']['events'], 3)   # every group event holds that message
        self.assertEqual(r['after_message'], ['「桃子」说了蓝莓计划'])
        self.assertEqual(r['after_person'], [])

    def test_her_notebook_fairly_between_windows(self):
        r = run_case('fair')
        self.assertEqual(len(r['texts']), 13)                       # her body and 12 events, as before
        self.assertEqual(r['windows'], ['group:90010%d' % g for g in range(6)])
        self.assertIn('事件：大事：三个人的大事', r['texts'])

    def test_recent_things_in_a_reply(self):
        r = run_case('reply')
        lines = r['related'].splitlines()
        self.assertEqual(lines[0], '- 柠檬的生日聚会：柠檬请大家去她家过生日')   # the strong one first, as before
        self.assertEqual(len(lines), 3)                            # and at most two of the notes
        self.assertNotIn('桃子', r['related'])                      # another window's
        self.assertNotIn('抽卡', r['related'])                      # nothing to do with it
        self.assertEqual(r['unrelated'], '- 柠檬的生日聚会：柠檬请大家去她家过生日')

    def test_not_merged_with_someone_ruled_out(self):
        r = run_case('merge_gone')
        self.assertIn('Q1来不来', r['prompt'])
        self.assertEqual(r['night'], {'group:900001': {'called': 1, 'written': 0}})
        self.assertEqual([e['origin']['people'] for e in r['events']], [['10002']])
        self.assertEqual(r['files_with_him'], [])

    def test_a_deleted_persons_name(self):
        r = run_case('gone_names')
        # what others said of him before: 某人 as soon as the owner deletes him
        self.assertEqual(r['phone_before_delete'][1], '周末打副本 阿星来不来')
        self.assertEqual(r['phone_at_once'][0], '周末打副本 某人来不来')
        self.assertEqual(r['deleted']['data']['counts']['named'].get('phone'), 1)
        # what is kept of what others say of him: 某人, after a restart too
        self.assertEqual(r['phone_before_restart'][-1], '某人今天在吗')
        self.assertEqual(r['phone_after_restart'][-1], '某人呢')
        self.assertNotIn('阿星', ''.join(r['phone_after_restart']))  # and at a restart, in what was kept before
        # in the nightly material (impressions and the note of the day) a code
        self.assertEqual(r['material_names'].get('10003'), ['阿星'])
        self.assertNotIn('阿星', r['prompt'])
        self.assertIn('1 P1：Q1说他周末有空', r['prompt'])
        self.assertIn('2 P1：周末打副本 某人来不来', r['prompt'])
        # what names him is not kept; the rest is
        self.assertEqual(r['night'], {'group:900001': {'called': 1, 'written': 1}})
        self.assertEqual(r['events'], ['「阿橙」说好呀'])
        self.assertFalse(r['registry_has_name'])                   # only hashes of his names

    def test_a_deleted_persons_name_everywhere_at_once(self):
        r = run_case('everywhere')
        self.assertIn('memory/library.json', r['before'])            # what others said of him, remembered
        self.assertIn('archives/events.jsonl', r['before'])          # and an event whose key names him
        self.assertIn(['柠檬约阿星打副本', ['阿星的副本局']], r['keys_before'])
        # the owner deletes him: nowhere she keeps things has his name any more, at once
        self.assertEqual(r['at_once'], [])
        self.assertIn('library', r['deleted']['data']['counts']['named'])
        self.assertIn(['柠檬约某人打副本', ['某人的副本局']], r['keys_at_once'])   # the event's keys too
        # a reply before any restart: not in what she recalls, not written back anywhere
        self.assertNotIn('阿星', r['prompt'])
        self.assertIn('某人', r['prompt'])
        self.assertEqual(r['after_a_turn'], [])
        # and a restart makes no new copy that has it
        self.assertNotIn('阿星', r['prompt_after_restart'])
        self.assertEqual((r['after_restart'], r['archives']), ([], []))

    def test_a_framed_name_goes_with_its_frame(self):
        # the owner, 10-29: names she writes back are framed; deleting him takes the frame too
        r = run_case('everywhere')
        self.assertEqual(r['framed_at_once'], [['某人约「柠檬」打副本', '「柠檬」答应了某人']])
        self.assertEqual(r['framed_somebody'], [])

    def test_a_name_that_is_an_everyday_word(self):
        r = run_case('everyday')
        # only where it plainly means him: after an @, or as the one who says something
        self.assertEqual(r['at_once'], ['周末一起打副本', '@某人 来不来', '某人说他不来'])  # his own line: gone
        self.assertEqual(r['after_restart'], ['周末去哪玩', '某人：我也不来了'])

    def test_tonights_marks_with_the_registry_unreadable(self):
        r = run_case('marks')
        self.assertEqual(set(r['first']), {'group:900001', 'private:10004'})
        self.assertEqual((r['after_restart'], r['calls']), ({}, 2))
        self.assertTrue(r['notebook_tried'])

    def test_and_with_a_restored_backup(self):
        r = run_case('restore')
        self.assertEqual(len(r['before']), 4)
        self.assertEqual(r['after'], ['「桃子」说了蓝莓计划'])


if __name__ == '__main__':
    unittest.main()
