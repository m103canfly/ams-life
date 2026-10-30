"""Step 2 (甲): she decides herself whether to answer -- the pure rules (attention.py) here, the
plugin around them end to end in attention_cases.py with a fake model. All made up."""
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
import attention as at  # noqa: E402

DAY = 86400
_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'attention_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class Called(unittest.TestCase):
    def test_the_ways_she_is_called(self):
        now = 1000.0
        self.assertEqual(at.called(False, True, '10001', now=now), 'private')
        self.assertEqual(at.called(True, False, '10001', now=now), 'at')
        self.assertEqual(at.called(False, False, '10001', now - 60, ['10001'], now), 'continue')
        self.assertEqual(at.called(False, False, '10002', now - 60, ['10001'], now), '')    # not to him
        self.assertEqual(at.called(False, False, '10001', now - 400, ['10001'], now), '')   # too long ago
        self.assertEqual(at.called(False, False, '10001', now=now), '')


class MoodAttention(unittest.TestCase):
    def test_mood_threshold_and_wait_follow_state(self):
        self.assertLess(at.mood_threshold('normal', 0.8, 0.8), at.threshold('normal'))
        self.assertGreater(at.mood_threshold('normal', -0.8, 0.2), at.threshold('normal'))
        self.assertLess(at.mood_wait(6, 0.8, 0.8), 6)
        self.assertGreater(at.mood_wait(6, -0.8, 0.2), 6)

    def test_mood_adjustments_are_bounded(self):
        for valence in (-10, 0, 10):
            for energy in (-10, 0, 10):
                self.assertTrue(0.20 <= at.mood_threshold('normal', valence, energy) <= 0.75)
                self.assertTrue(1.0 <= at.mood_wait(6, valence, energy) <= 10.0)


class HerName(unittest.TestCase):
    def test_her_name_as_a_call(self):
        for t in ('小爱，在吗', '小爱 你看这个', '好吧 小爱', '小爱你好', '小爱', '爱弥斯？', '@小爱 来'):
            self.assertTrue(at.names_her(t), t)
        for t in ('小爱乱撞', '看到她我心里小爱乱撞', '可爱的小爱乱跑', '我爱弥斯特', ''):
            self.assertFalse(at.names_her(t), t)
        self.assertTrue(at.names_her('阿爱，在吗', ['阿爱']))


class Night(unittest.TestCase):
    def test_night_hours(self):
        def at_hour(h, m=0):
            return time.mktime((2026, 10, 30, h, m, 0, 0, 0, -1))
        self.assertTrue(at.is_night(at_hour(3)))
        self.assertTrue(at.is_night(at_hour(8, 24)))
        self.assertFalse(at.is_night(at_hour(8, 25)))
        self.assertFalse(at.is_night(at_hour(0, 59)))
        self.assertTrue(at.is_night(at_hour(23, 30), '23:00', '07:00'))   # across midnight

    def test_called_once_she_sleeps_on_three_times_she_wakes(self):
        now = 10000.0
        self.assertEqual(at.night_gate([now], now)[0], False)
        self.assertEqual(at.night_gate([now - 120, now], now)[0], False)
        answer, woken, until = at.night_gate([now - 300, now - 120, now], now)
        self.assertTrue(answer and woken)
        self.assertEqual(until, now + 20 * 60)
        # three calls but not within 10 minutes: asleep
        self.assertFalse(at.night_gate([now - 900, now - 700, now], now)[0])
        # awake: called again keeps her up; nobody for a while: asleep again
        self.assertEqual(at.night_gate([now], now + 60, until)[:2], (True, False))
        self.assertFalse(at.night_gate([now + 3000], now + 3000, until)[0])


class Familiarity(unittest.TestCase):
    def test_by_the_dealings_and_the_owner_closest(self):
        now = 400 * DAY
        nobody = at.familiarity({}, now)
        some = at.familiarity({'days': [399, 398], 'calls': {}}, now)
        often = at.familiarity({'days': list(range(371, 400)), 'calls': {'399': 10}, 'private': True}, now)
        old = at.familiarity({'days': list(range(300, 330))}, now)
        self.assertEqual(nobody, 0.0)
        self.assertLess(some, often)
        self.assertLess(old, often)          # long ago weighs less
        self.assertGreater(often, 0.9)
        self.assertEqual(at.familiarity({}, now, owner=True), 1.0)

    def test_note_tie(self):
        t = at.note_tie({}, 10 * DAY + 5, called_her=True)
        t = at.note_tie(t, 10 * DAY + 50, called_her=True, private=True)
        t = at.note_tie(t, 11 * DAY + 5)
        self.assertEqual(t['days'], [10, 11])
        self.assertEqual(t['calls'], {'10': 2})
        self.assertTrue(t['private'])


class Score(unittest.TestCase):
    def test_what_draws_her_in(self):
        base = at.score(0.5, 0.5, 0, False, 30)
        self.assertGreater(at.score(0.9, 0.5, 0, False, 30), base)        # closer to what she keeps
        self.assertGreater(at.score(0.5, 0.9, 0, False, 30), base)        # people she knows
        self.assertLess(at.score(0.5, 0.5, 3, False, 30), base)           # she said a lot here lately
        self.assertLess(at.score(0.5, 0.5, 0, True, 30), base)            # a quarrel
        self.assertGreater(at.score(0.5, 0.5, 0, False, 240), base)       # quiet here a long while

    def test_levels(self):
        self.assertGreater(at.threshold('less'), at.threshold('normal'))
        self.assertGreater(at.threshold('normal'), at.threshold('more'))
        self.assertEqual(at.threshold('nonsense'), at.threshold('normal'))


class SafetyNets(unittest.TestCase):
    def test_an_hour_in_a_group(self):
        now = 10000.0
        self.assertTrue(at.hour_ok([now - 10] * 29, now))
        self.assertFalse(at.hour_ok([now - 10] * 30, now))
        self.assertTrue(at.hour_ok([now - 4000] * 30, now))

    def test_money(self):
        prices = {'input_miss': 2.0, 'input_hit': 0.05, 'output': 8.0}
        self.assertAlmostEqual(at.cost({'input_miss': 1_000_000, 'input_hit': 0, 'output': 500_000}, prices), 6.0)
        self.assertEqual(at.budget(7.9), 'ok')
        self.assertEqual(at.budget(8.0), 'soft')
        self.assertEqual(at.budget(10.0), 'hard')


class WhatSheSends(unittest.TestCase):
    def test_silent(self):
        self.assertTrue(at.silent('【不说】'))
        self.assertTrue(at.silent('  【不说】 '))
        self.assertTrue(at.silent(''))
        self.assertFalse(at.silent('不说了，睡觉'))
        self.assertFalse(at.silent('【不说】好吧还是说一句'))

    def test_split_at_most_five(self):
        self.assertEqual(at.split('一\n【下一条】\n二'), ['一', '二'])
        self.assertEqual(at.split('嗯【不说】'), ['嗯【不说】'])
        seven = '【下一条】'.join(str(i) for i in range(7))
        parts = at.split(seven)
        self.assertEqual(len(parts), 5)
        self.assertEqual(parts[-1], '4 5 6')

    def test_newlines_lists_and_code_blocks(self):
        self.assertEqual(at.split('a\n\nb\nc\nd\ne\nf'), ['a', 'b', 'c', 'd', 'e f'])
        self.assertEqual(at.split('a\n- one\n- two\nb\n```\nx\ny\n```\nc'),
                         ['a', '- one\n- two', 'b', '```\nx\ny\n```', 'c'])

    def test_faces_stay_in_their_piece(self):
        parts = at.split('one\ntwo[表情:微笑]')
        self.assertEqual(at.pieces(parts[1]), [('text', 'two'), ('face', 14)])

    def test_faces(self):
        self.assertEqual(at.pieces('好呀[表情:微笑]'), [('text', '好呀'), ('face', 14)])
        self.assertEqual(at.pieces('[表情:赞]'), [('face', 76)])
        self.assertEqual(at.pieces('[表情:不存在] 嗯'), [('text', '[表情:不存在] 嗯')])   # unknown: words

    def test_typing_pause(self):
        self.assertEqual(at.typing_seconds(''), 1.0)
        self.assertEqual(at.typing_seconds('字' * 200), 3.0)
        for length in (1, 30, 60, 100):
            self.assertTrue(1.0 <= at.typing_seconds('字' * length) <= 3.0)

    def test_choices_are_told_not_ordered(self):
        self.assertIn('【不说】', at.CHOICES_NOTE)
        self.assertNotIn('【下一条】', at.CHOICES_NOTE)
        self.assertIn('最多 5 条', at.PIECES_NOTE)



class InThePlugin(unittest.TestCase):
    """attention_cases.py: the plugin with self_decide on (a fake model, made-up people)."""

    def test_pieces_without_self_decide_and_switch_off(self):
        r = run_case('pieces')
        self.assertEqual(r['on']['chain'], [['Plain', 'one']])
        self.assertEqual([s['chain'] for s in r['sent']],
                         [[['Plain', 'two'], ['Face', 14]], [['Plain', 'three']]])
        self.assertEqual(r['off']['text'], 'one\ntwo')
        self.assertEqual(r['off']['chain'], [])
        self.assertEqual(r['phone'], ['one\ntwo[表情:微笑]\nthree', 'one\ntwo'])

    def test_pieces_stop_after_send_failure(self):
        self.assertEqual(run_case('pieces')['failed_calls'], ['second'])

    def test_split_reply_is_one_complete_astrbot_history_entry(self):
        self.assertEqual(run_case('pieces_contract')['history'], [['text', 'first\nsecond\nthird']])

    def test_sticker_follows_its_own_piece(self):
        r = run_case('pieces_contract')
        self.assertEqual(r['sticker_first'], [['Plain', 'first']])
        self.assertEqual(r['sticker_order'], [['text', [['Plain', 'second']]], ['sticker', 'fake'],
                                               ['text', [['Plain', 'third']]]])

    def test_failed_sticker_does_not_stop_later_words(self):
        r = run_case('pieces_contract')
        self.assertEqual(r['failed_sticker_first'], [['Plain', 'first']])
        self.assertEqual(r['failed_sticker_order'], [['text', [['Plain', 'second']]],
                                                     ['sticker_failed', 'fake'],
                                                     ['text', [['Plain', 'third']]]])

    def test_voice_waits_until_all_reply_pieces_are_sent(self):
        r = run_case('pieces_voice')
        self.assertEqual(r['before_release'], [['text', 'first']])
        self.assertEqual(r['order'], [['text', 'first'], ['text', 'second'], ['text', 'third'],
                                      ['delay', 1.5], ['voice', 'Record']])

    def test_send_check_and_silence_hold_the_entire_reply(self):
        self.assertEqual(run_case('pieces_contract')['held'], [True, True, []])

    def test_group_quote_and_at_only_on_first_piece(self):
        r = run_case('pieces_contract')
        self.assertEqual([c[0] for c in r['first']], ['Reply', 'At', 'Plain'])
        self.assertEqual(r['rest'], [['text', [['Plain', 'second']]], ['text', [['Plain', 'third']]]])

    def test_first_piece_has_no_pause_later_pieces_wait(self):
        delays = run_case('pieces_contract')['delays']
        self.assertEqual(len(delays), 2)
        self.assertTrue(all(1 <= delay <= 3 for delay in delays))

    def test_called_astrbot_answers_as_before(self):
        r = run_case('called_at')['r']
        self.assertEqual((r['stopped'], r['requests']), (False, []))

    def test_a_stretch_only_the_last_one_called_carried_on(self):
        r = run_case('burst')
        self.assertTrue(r['first']['stopped'])                       # not judged on its own
        self.assertEqual(r['second']['requests'], [{'request_llm': '周末一起去爬山吗', 'conversation': 'cid-1'}])
        self.assertEqual(r['conversations'], ['default:GroupMessage:900001'])   # in the conversation

    def test_not_called_by_the_score(self):
        r = run_case('not_called')
        self.assertEqual((r['low']['stopped'], r['low']['requests']), (False, []))
        self.assertEqual(len(r['high']['requests']), 1)

    def test_her_name_calls_her(self):
        r = run_case('named')
        self.assertEqual(len(r['named']['requests']), 1)          # not AstrBot's wake: the plugin asks
        self.assertEqual(r['not_a_call']['requests'], [])

    def test_taking_up_what_she_said_calls_her(self):
        r = run_case('continue')
        self.assertEqual(len(r['his']['requests']), 1)
        self.assertEqual(r['other']['requests'], [])

    def test_night(self):
        r = run_case('night')
        self.assertEqual([c['stopped'] for c in r['calls']], [True, True, False])
        self.assertTrue(r['woken'])
        self.assertEqual(r['not_called_at_night']['requests'], [])

    def test_an_hour_in_a_group(self):
        r = run_case('hour')
        self.assertTrue(r['r']['stopped'])
        self.assertFalse(r['private']['stopped'])

    def test_the_money_of_the_day(self):
        r = run_case('money')
        self.assertTrue(r['soft_group']['stopped'])
        self.assertFalse(r['soft_owner_private']['stopped'])        # only the owner's private chat
        self.assertTrue(r['soft_other_private']['stopped'])
        self.assertTrue(r['hard_owner_private']['stopped'])         # over it: nothing at all

    def test_what_she_picked(self):
        r = run_case('replies')
        self.assertTrue(r['silent']['stopped'])                     # 【不说】: nothing sent
        self.assertTrue(r['multi']['prompt_has_choices'])
        self.assertEqual(r['multi']['text'], '周末去爬山吧')            # the first by AstrBot
        self.assertEqual(r['multi']['chain'], [['Plain', '周末去爬山吧']])   # only the first
        self.assertEqual(r['sent'], [{'umo': 'default:GroupMessage:900001', 'chain': [['Plain', '记得带水'], ['Face', 14]]},
                                     {'umo': 'default:GroupMessage:900001', 'chain': [['Face', 76]]},
                                     {'umo': 'default:GroupMessage:900001', 'chain': [['Plain', '第二句']]}])
        self.assertEqual(r['face_first']['chain'], [['Face', 13]])   # a face alone as the first
        # DeepSeek's answer comes with a chain: AstrBot sends the chain, so it must hold the first
        # message only (else the whole reply went out first, then the rest again)
        self.assertEqual(r['with_chain']['chain'], [['Plain', '第一句']])
        self.assertEqual(r['with_chain']['text'], '第一句')
        self.assertEqual(r['silent_inside']['chain'], [['Plain', '嗯']])
        # kept: what she said (nothing of 【不说】)
        self.assertEqual(r['phone'], ['周末去爬山吧\n记得带水[表情:微笑]\n[表情:赞]', '[表情:呲牙]', '第一句\n第二句', '嗯'])
        # every reply's cost (the fake usage: 2.2 / 0.05 / 8.7 yuan a million)
        self.assertAlmostEqual(r['spend'][next(iter(r['spend']))]['reply'], 0.01274, places=5)
        self.assertEqual(r['panel']['state'], 'ok')

    def test_switch_off_nothing(self):
        r = run_case('off')['r']
        self.assertEqual((r['stopped'], r['requests']), (False, []))


if __name__ == '__main__':
    unittest.main()
