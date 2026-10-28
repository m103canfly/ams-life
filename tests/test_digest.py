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


LINES = [line(0, '10002', '柠檬', '周末一起打副本吗'),
         line(1, '10001', '芒果', '我来 @柠檬 柠柠别鸽'),
         line(2, '', '', '好呀', role='assistant'),
         line(3, '10003', '阿星', '我家猫叫团子'),
         line(4, '10001', '芒果', '我的号码是13812345678'),
         line(5, '10002', '柠檬', '昨天的事', day_offset=-1)]


class Material(unittest.TestCase):
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
        for word in ('柠檬', '芒果', '阿星', '柠柠', '1381234', '10002'):
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
        self.assertEqual(digest.named('P1约了P2和Q1', codes, {'10002': '柠檬', '10001': '芒果'}), '柠檬约了芒果和某人')


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
        events = [ev('柠檬约周末打副本', 'g1'), ev('大家聊抽卡', 'g1'), ev('芒果的副本攻略', 'g1', what='周末副本的打法'),
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
            for word in ('柠檬', '芒果', '阿星', '桃子', '10001', '10002', '10004', '900001'):
                self.assertNotIn(word, prompt)
        # the person and the message the registry rules out are not there at all
        self.assertNotIn('团子', group)
        self.assertNotIn('1381234', group)
        self.assertIn('2 P2：我来我来 @P1', group)

    def test_origins(self):
        evs = {e['title']: e for e in run_case('nightly')['events']}
        self.assertEqual(sorted(evs), sorted(['柠檬约周末打副本', '有人在聊抽卡', '桃子说了蓝莓计划', '芒果说了件事']))
        one = evs['柠檬约周末打副本']
        self.assertEqual(one['event'], '柠檬约大家周末一起打副本，芒果说要来')
        self.assertEqual(one['origin'], {'where': 'group:900001', 'people': ['10001', '10002'],
                                         'source_ids': ['g1', 'g2'], 'visibility': 'public'})
        # no lines named / a wrong one: the whole day (but nothing ruled out)
        for title in ('有人在聊抽卡', '芒果说了件事'):
            self.assertEqual(evs[title]['origin'], {'where': 'group:900001', 'people': ['10001', '10002'],
                                                    'source_ids': ['g1', 'g2', 'g3', 'g4'], 'visibility': 'public'})
        self.assertEqual(evs['桃子说了蓝莓计划']['origin'], {'where': 'private:10004', 'people': ['10004'],
                                                        'source_ids': ['p1'], 'visibility': 'private'})

    def test_private_stays_there(self):
        seen = run_case('nightly')['seen']
        self.assertNotIn('蓝莓', ''.join(seen['group']) + ''.join(seen['g2']))
        self.assertIn('桃子说了蓝莓计划', seen['private'])
        self.assertIn('柠檬约周末打副本', seen['group'])
        self.assertIn('有人约周末打副本', seen['g2'])       # another group: without names
        self.assertNotIn('柠檬', ''.join(seen['g2']))

    def test_her_notebook_uses_them(self):
        nb = run_case('nightly')['notebook']
        self.assertIn('事件：柠檬约周末打副本：柠檬约大家周末一起打副本，芒果说要来', nb['group'])
        self.assertNotIn('蓝莓', ''.join(nb['group']))
        self.assertIn('事件：桃子说了蓝莓计划：桃子跟她说起蓝莓计划的安排', nb['private'])

    def test_deleted_with_the_message_and_the_person(self):
        r = run_case('nightly')
        self.assertEqual(r['forget_message']['events'], 3)   # every group event holds that message
        self.assertEqual(r['after_message'], ['桃子说了蓝莓计划'])
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

    def test_and_with_a_restored_backup(self):
        r = run_case('restore')
        self.assertEqual(len(r['before']), 4)
        self.assertEqual(r['after'], ['桃子说了蓝莓计划'])


if __name__ == '__main__':
    unittest.main()
