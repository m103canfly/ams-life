"""Group members she knows (impressions.py), on made-up phone windows. No model: a fake `ask`."""
import asyncio
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import forget_registry as fr  # noqa: E402
import impressions as im  # noqa: E402

G1, G2 = 'group:900001', 'group:900002'
DAY = '2026-10-04'
T = time.mktime(time.strptime(DAY + ' 20:00:00', '%Y-%m-%d %H:%M:%S'))


def line(qq, name, text, i=0, day_offset=0, role='user', msg_id=''):
    out = {'ts': T + i * 60 + day_offset * 86400, 'role': role, 'sender_id': qq, 'sender_name': name, 'text': text}
    if msg_id:
        out['msg_id'] = msg_id
    return out


def window():
    lines = []
    for i in range(12):   # 柠檬: 12 lines, a pet phrase on most of them
        lines.append(line('10002', '柠檬', ['又歪了 冲鸭', '冲鸭 今天也要抽', '这期角色好看', '冲鸭冲鸭',
                                            '我工资好低', '@芒果 你抽了吗', '我的号是 123456789',
                                            '[图片]', '副本打不过', '冲鸭', '晚上一起副本', '好耶'][i], i))
    for i in range(6):    # 芒果: 6 lines, no impression yet
        lines.append(line('10001', '芒果', '今天的副本好难 %d' % i, 20 + i))
    for i in range(4):    # 路人: too few
        lines.append(line('10005', '路人', '路过', 40 + i))
    for i in range(15):   # 昨天的：不算今天
        lines.append(line('10003', '阿星', '昨天的话', i, day_offset=-1))
    lines.append(line('20002', '小爱', '她自己的话', 50, role='assistant'))
    return lines


class Pick(unittest.TestCase):
    def test_who(self):
        picked = im.pick_people(window(), DAY)
        self.assertEqual([p['qq'] for p in picked], ['10002', '10001'])
        self.assertEqual([p['count'] for p in picked], [12, 6])
        # 芒果 already has an impression and only said 6 lines: not tonight
        self.assertEqual([p['qq'] for p in im.pick_people(window(), DAY, known={'10001'})], ['10002'])

    def test_at_most_twelve_and_registry(self):
        lines = [line(str(10100 + n), '人%d' % n, '说话', n) for n in range(20) for _ in range(11)]
        self.assertEqual(len(im.pick_people(lines, DAY)), im.MAX_PEOPLE)
        with fr.ForgetRegistry() as reg:
            reg.forget_person('10002', fr.EVERYWHERE, stamp=0)
            self.assertNotIn('10002', [p['qq'] for p in im.pick_people(window(), DAY, place=G1, registry=reg)])

    def test_stats_and_pet_phrases(self):
        picked = im.pick_people(window(), DAY)
        others = [ln for ln in window() if ln['sender_id'] != '10002']
        s = im.day_stats(picked[0]['lines'], others)
        self.assertEqual(s['msgs'], 12)
        self.assertEqual(s['image_ratio'], 0.08)
        self.assertEqual(s['hours'], [20])
        self.assertEqual(s['phrases'], ['冲鸭'])          # 副本: others say it more; 工资: red line

    def test_material_hides_who_and_numbers(self):
        picked = im.pick_people(window(), DAY)
        text, codes = im.material(picked)
        self.assertEqual(codes, {'P1': '10002', 'P2': '10001'})
        for gone in ('柠檬', '芒果', '10002', '123456789', '工资', '[图片]'):
            self.assertNotIn(gone, text)
        self.assertIn('@P2 你抽了吗', text)
        self.assertIn('我的号是 #', text)

    def test_english_names_are_whole_words_in_the_material(self):
        picked = im.pick_people([line('10002', '柠檬', 'Alice 和 Al 都来了', i) for i in range(12)], DAY)
        text, _codes = im.material(picked, {'10007': {'Al'}})
        self.assertIn('Alice 和 Q1 都来了', text)

    def test_everyone_in_the_group_becomes_a_code(self):
        lines = window() + [line('10002', '柠檬', t, 30 + i) for i, t in enumerate(
            ['阿星昨天说他也歪了', '桃桃今天没来', '@小鱼儿 快来', '路人甲也在'])]
        people = {'10004': {'name': '桃子', 'aliases': ['桃桃']}}
        names = im.group_names(lines + [line('10006', '小鱼儿', '在的', 99, day_offset=-1)], people)
        picked = im.pick_people(lines, DAY)
        text, codes = im.material(picked, names)
        self.assertEqual(codes, {'P1': '10002', 'P2': '10001'})   # only the picked are asked about
        for name in ('阿星', '桃桃', '小鱼儿', '路人', '柠檬', '芒果'):
            self.assertNotIn(name, text)
        self.assertRegex(text, r'Q\d昨天说他也歪了')
        self.assertRegex(text, r'Q\d今天没来')
        self.assertRegex(text, r'@Q\d 快来')
        self.assertRegex(text, r'Q\d甲也在')
        prompt, _ = im.prompt_for(picked, names)
        self.assertIn('Q1、Q2', prompt)


class Answer(unittest.TestCase):
    def test_checks(self):
        codes = {'P1': '10002', 'P2': '10001', 'P3': '10005'}
        answer = '好的：' + json.dumps({
            'P1': {'style': '说话很快，爱用“冲鸭”，常接别人的梗', 'topics': ['抽卡', '副本', '工资', '一起打3个本'],
                   'aliases': ['柠柠', '大佬', 'x']},
            'P2': {'style': '性格内向，说话慢', 'topics': []},          # a judgement: nothing kept
            'P3': {'style': '每天说 30 句', 'topics': ['美食']},        # a number: style dropped, topic kept
        }, ensure_ascii=False) + ' 以上'
        got = im.parse_answer(answer, codes)
        self.assertEqual(got['10002'], {'style': '说话很快，爱用“冲鸭”，常接别人的梗', 'topics': ['抽卡', '副本'],
                                        'aliases': ['柠柠']})         # 大佬: how anyone is addressed
        self.assertNotIn('10001', got)
        self.assertEqual(got['10005'], {'style': '', 'topics': ['美食'], 'aliases': []})
        self.assertEqual(im.parse_answer('不是 JSON', codes), {})
        self.assertEqual(im.check_style('x' * 61), '')
        self.assertEqual(im.check_alias('柠柠'), '柠柠')
        self.assertEqual(im.check_alias('a'), '')

    def test_masked_topics_say_nothing(self):
        for masked in ('有人的猫', '某人家', 'P1的号', '和Q2打本'):
            self.assertEqual(im.check_topic(masked), '', masked)
        self.assertEqual(im.check_topic('养猫'), '养猫')


class Aliases(unittest.TestCase):
    def lines(self):
        ls = [line('10002', '柠檬', '我来啦', i * 30, msg_id='m%d' % i) for i in range(3)]
        ls += [line('10001', '芒果', '@柠檬 柠柠快来打本', 2),                 # an @ to her
               dict(line('10003', '阿星', '柠柠你抽到了吗', 4), reply_to='m1'),  # a reply to her
               line('10005', '路人', '柠柠在吗', 300),                          # far from anything she said
               line('10001', '芒果', '芒芒说的', 5)]
        return ls

    def test_found_twice_when_talking_to_him(self):
        cards = {'10002': ['柠檬'], '10001': ['芒果'], '10003': ['阿星'], '10005': ['路人']}
        got = im.verify_aliases({'10002': ['柠柠', '冲冲']}, self.lines(), cards, DAY)
        self.assertEqual(got, {'10002': ['柠柠']})                          # 冲冲: nobody called her that
        once = [ln for ln in self.lines() if ln['sender_id'] != '10003']
        self.assertEqual(im.verify_aliases({'10002': ['柠柠']}, once, cards, DAY), {})   # only once near her

    def test_two_people_one_name_goes_for_both_and_cards_win(self):
        cards = {'10002': ['柠檬'], '10001': ['芒果']}
        self.assertEqual(im.verify_aliases({'10002': ['柠柠'], '10001': ['柠柠']}, self.lines(), cards, DAY), {})
        self.assertEqual(im.verify_aliases({'10002': ['芒果']}, self.lines(), cards, DAY), {})

    def test_the_model_sees_what_others_said_to_them_as_codes(self):
        picked = im.pick_people([line('10002', '柠檬', '在的', i, msg_id='m%d' % i) for i in range(12)], DAY)
        said_to = im.addressed(self.lines(), picked, DAY)
        text, _codes = im.material(picked, {'10001': {'芒果'}, '10003': {'阿星'}}, said_to)
        self.assertIn('别人对他们说的话', text)
        self.assertIn('@P1 柠柠快来打本', text)       # the unknown name stays for the model to find
        self.assertNotIn('芒果', text)


class Nightly(unittest.TestCase):
    def run_night(self, store, lines, answer, day=DAY, registry=None):
        calls = []

        async def ask(prompt):
            calls.append(prompt)
            if isinstance(answer, Exception):
                raise answer
            return answer
        result = asyncio.run(im.nightly(store, G1, lines, ask, day, registry=registry, self_id='20002'))
        return result, calls

    def test_one_call_a_day_and_what_is_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            answer = json.dumps({'P1': {'style': '爱用语气词', 'topics': ['抽卡']}}, ensure_ascii=False)
            result, calls = self.run_night(store, window(), answer)
            self.assertEqual((result['called'], result['picked'], result['written']), (1, 2, 1))
            self.assertEqual(len(calls), 1)
            again, calls2 = self.run_night(store, window(), answer)
            self.assertEqual(again, {'skipped': 'tried today'})
            self.assertEqual(calls2, [])
            data = store.load(G1)
            lemon = data['people']['10002']
            self.assertEqual((lemon['name'], lemon['style'], lemon['topics']), ('柠檬', '爱用语气词', ['抽卡']))
            self.assertEqual(lemon['origin'], {'where': G1, 'people': ['10002'], 'source_ids': [],
                                               'visibility': 'public'})
            self.assertEqual(data['people']['10001']['style'], '')      # counts only
            raw = store.path(G1).read_text('utf-8')
            for verbatim in ('又歪了', '今天的副本好难', '123456789'):
                self.assertNotIn(verbatim, raw)

    def test_a_failed_call_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            result, _ = self.run_night(store, window(), RuntimeError('model down'))
            self.assertEqual((result['called'], result['error']), (1, 'RuntimeError'))
            self.assertEqual(self.run_night(store, window(), '{}')[0], {'skipped': 'tried today'})
            self.assertEqual(store.load(G1)['people']['10002']['stats']['msgs'], 12)

    def test_days_add_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            self.run_night(store, window(), '{}')
            nxt = [dict(ln, ts=ln['ts'] + 86400) for ln in window()]
            self.run_night(store, nxt, '{}', day='2026-10-05')
            s = store.load(G1)['people']['10002']['stats']
            self.assertEqual((s['msgs'], s['days'], s['last_day']), (24, 2, '2026-10-05'))

    def test_nobody(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_night(im.Store(Path(tmp) / 'p'), window()[-5:], '{}')
            self.assertEqual((result, calls), ({'skipped': 'nobody'}, []))


class StoreAndForget(unittest.TestCase):
    def test_files_and_deleting(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            for place in (G1, G2):
                data = store.load(place)
                rec = data['people'].setdefault('10002', im._record(place, '10002'))
                rec.update(name='柠檬', style='爱用语气词', topics=['抽卡'])
                store.save(place, data)
            self.assertEqual(sorted(store.places()), [G1, G2])
            self.assertTrue(store.forget_message_by(G1, '10002'))
            self.assertEqual(store.load(G1)['people']['10002']['style'], '')
            self.assertEqual(store.load(G2)['people']['10002']['style'], '爱用语气词')
            self.assertEqual(store.forget_person('10002'), 2)
            self.assertEqual(store.load(G2)['people'], {})

    def test_pet_phrases_go_with_a_deleted_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            data = store.load(G1)
            rec = data['people'].setdefault('10002', im._record(G1, '10002'))
            rec['stats'] = {'msgs': 12, 'phrases': ['冲鸭']}
            store.save(G1, data)
            self.assertTrue(store.forget_message_by(G1, '10002'))
            self.assertEqual(store.load(G1)['people']['10002']['stats'], {'msgs': 12, 'phrases': []})

    def test_pet_phrases_are_checked_before_they_are_stored(self):
        rec = im._record(G1, '10002')
        im.add_day(rec, '柠檬', {'msgs': 3, 'phrases': ['工资', '冲鸭', '说的是一整句话', '好笨', '冲鸭']}, DAY)
        self.assertEqual(rec['stats']['phrases'], ['冲鸭'])
        rec['stats']['phrases'] = ['冲鸭']
        self.assertNotIn('phrases', im.view(rec, G1, G1))           # never in a prompt
        self.assertNotIn('冲鸭', im.describe(im.view(rec, G1, G1)))

    def test_names_stay_until_he_is_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            data = store.load(G1)
            data['people']['10002'] = dict(im._record(G1, '10002'), name='柠檬', aliases=['柠柠'])
            store.save(G1, data)
            store.keep_names('10002', ['阿柠'])
            self.assertEqual(store.places(), [G1])                   # the names file is not a group
            self.assertEqual(store.forget_impression('10002'), 1)
            self.assertEqual(store.load(G1)['people'], {})
            self.assertEqual(store.names_of('10002'), ['阿柠', '柠檬', '柠柠'])
            store.forget_person('10002')
            self.assertEqual(store.names_of('10002'), [])

    def test_files_are_read_again_only_when_changed(self):
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            store.save(G1, {'people': {'10002': {'name': '柠檬'}}})
            with mock.patch.object(Path, 'read_text', side_effect=AssertionError('read again')):
                first = store.load(G1)
                self.assertEqual(store.places(), [G1])
            first['people'].clear()                                   # a copy: the cache is untouched
            self.assertEqual(store.load(G1)['people'], {'10002': {'name': '柠檬'}})
            other = im.Store(Path(tmp) / 'people')                    # written by someone else
            other.save(G1, {'people': {'10002': {'name': '柠檬'}, '10001': {'name': '芒果'}}})
            self.assertEqual(sorted(store.load(G1)['people']), ['10001', '10002'])

    def test_another_groups_file_is_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = im.Store(Path(tmp) / 'people')
            store.save(G1, {'people': {'10002': {'name': '柠檬'}}})
            store.path(G2).write_text(store.path(G1).read_text('utf-8'), 'utf-8')
            self.assertEqual(store.load(G2)['people'], {})


class View(unittest.TestCase):
    rec = {'qq': '10002', 'name': '柠檬', 'aliases': ['柠柠'], 'style': '爱用语气词', 'topics': ['抽卡', '副本']}

    def test_the_table(self):
        full = im.view(self.rec, G1, G1)
        self.assertEqual(full['topics'], ['抽卡', '副本'])
        self.assertEqual(im.view(self.rec, G1, 'default:GroupMessage:900001'), full)
        self.assertEqual(im.view(self.rec, G1, G2, present_here=True), {'name': '柠檬', 'aliases': ['柠柠']})
        self.assertIsNone(im.view(self.rec, G1, G2))
        own = im.view(self.rec, G1, 'private:10002', private_text='最近副本好难打')
        self.assertEqual((own['style'], own['topics']), ('爱用语气词', ['副本']))
        self.assertIsNone(im.view(self.rec, G1, 'private:10001'))
        self.assertIsNone(im.view(self.rec, G1, 'web:https://example.org'))

    def test_describe(self):
        self.assertEqual(im.describe(im.view(self.rec, G1, G1)), '柠檬（大家叫 柠柠）：爱用语气词；常聊 抽卡、副本')
        self.assertEqual(im.describe(im.view(self.rec, G1, G2, present_here=True)), '柠檬（大家叫 柠柠）')
        self.assertEqual(im.describe(None), '')


class OldNames(unittest.TestCase):
    def test_from_bundle_only_names(self):
        bundle = [{'place': G1, 'qq': '10002', 'name': '柠檬', 'aliases': ['柠柠', '大佬', 'x']},
                  {'place': G1, 'qq': '10003', 'name': '阿星', 'aliases': ['星星']},
                  {'place': G1, 'qq': '10005', 'name': '路人', 'aliases': ['各位']},
                  {'place': 'private:10001', 'qq': '10001', 'name': '芒果', 'aliases': ['芒芒']}]
        with tempfile.TemporaryDirectory() as tmp, fr.ForgetRegistry() as reg:
            reg.forget_person('10003', G1, stamp=0)
            store = im.Store(Path(tmp) / 'people')
            counts = im.from_bundle(store, bundle, registry=reg, day='2026-10-28')
            self.assertEqual(counts, {'people': 1, 'person_forgotten': 1, 'no_alias_left': 1, 'person_no_place': 1})
            rec = store.load(G1)['people']['10002']
            self.assertEqual((rec['name'], rec['aliases'], rec['style'], rec['topics'], rec['stats']),
                             ('柠檬', ['柠柠'], '', [], {}))
            self.assertNotIn('group', store.load(G1))


if __name__ == '__main__':
    unittest.main()
