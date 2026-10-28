"""No QQ numbers in what she keeps; someone deleted is 某人; red lines are not kept (step 1-3-5).

The plugin cases run in a fresh interpreter (tests/numbers_cases.py). All numbers, names and
messages are made up.
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
import discretion  # noqa: E402

_CACHE = {}
LONG = re.compile(r'\d{5,}')


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'numbers_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class StripNumbers(unittest.TestCase):
    def test_at_and_known_numbers(self):
        s = discretion.strip_numbers
        self.assertEqual(s(' @桃子(10004) 一起玩', ['10004']), ' @桃子 一起玩')
        self.assertEqual(s('@小爱bot(20002) 在吗', her=['20002'], her_name='小爱'), '@小爱 在吗')
        self.assertEqual(s('@(10005) 快来'), '@某人 快来')
        self.assertEqual(s('@10005 快来'), '@某人 快来')
        self.assertEqual(s('@阿星(10003) 在吗', gone=['10003']), '@某人 在吗')
        self.assertEqual(s('加我 10002，群 900001', ['10002', '900001']), '加我 [号码]，群 [号码]')
        self.assertEqual(s('分数 1100020 和 123456', ['10002']), '分数 1100020 和 123456')   # whole numbers only

    def test_anonymize_to(self):
        self.assertEqual(discretion.anonymize('阿星你还在吗', ['阿星'], to='某人'), '某人你还在吗')


class WhatSheKeeps(unittest.TestCase):
    def test_no_numbers_in_her_phone_or_memory(self):
        r = run_case('at')
        for text in r['phone'] + r['library'] + r['loops']:
            self.assertNotIn('10002', text)
            self.assertNotIn('10004', text)
            self.assertNotIn('20002', text)
            self.assertNotIn('10005', text)
        self.assertEqual(r['phone'][:4], ['@小爱 你好呀', '问问 @桃子 在吗', '@某人 快来',
                                         '我的号是 [号码] 加我 游戏里的分是 123456'])   # other numbers stay
        self.assertIn('记得提醒我 @桃子 明天要还我书 我号 [号码] @小爱', r['library'])
        self.assertIn('记得提醒我 @桃子 明天要还我书 我号 [号码] @小爱', r['loops'])

    def test_group_cards_with_spaces_and_brackets(self):
        # people who never wrote here: only the message's own @ parts know their numbers
        r = run_case('at')
        for text in r['phone'] + r['library'] + r['loops'] + [r['users']] + r['asked']:
            self.assertNotIn('10077', text)
            self.assertNotIn('10078', text)
        self.assertIn('明天叫上 @Tom Lee 一起去爬山', r['library'])
        self.assertIn('记得提醒 @小明（学生） 周五交作业', r['library'])

    def test_what_astrbot_sends_the_model(self):
        r = run_case('at')
        self.assertEqual(r['asked'][0], '记得提醒我 @桃子 明天要还我书 我号 [号码] @小爱')
        for text in r['asked']:
            self.assertIsNone(LONG.search(text), text)

    def test_someone_deleted_is_somebody(self):
        r = run_case('at')
        self.assertEqual(r['phone'][4:6], ['@某人 某人你还在吗', '某人昨天也这么说'])
        self.assertFalse([t for t in r['phone'] + r['library'] if '阿星' in t or '10003' in t])

    def test_red_lines_are_counted_not_held_back_by_default(self):
        # the owner, 10-28: nothing is held back in the first version; the panel counts what
        # is kept now, afresh (nothing of a hit is recorded, what is deleted is not counted)
        r = run_case('redline')
        self.assertIn('小爱 我最近失眠好严重 每天都睡不着', r['library'])
        self.assertEqual(r['page'], {'filter': False, 'by_line': {'health': 2},
                                     'by_store': {'memory': {'health': 1}, 'material': {'health': 1}}})
        self.assertEqual(r['page_after_delete'], {'filter': False, 'by_line': {}, 'by_store': {}})
        self.assertNotIn('redline_counts.json', r['files'])

    def test_red_lines_are_not_kept_when_the_switch_is_on(self):
        r = run_case('redline_on')
        self.assertEqual(r['library'], ['小爱 我周末想去海边看日落'])
        self.assertIn('小爱 我最近失眠好严重 每天都睡不着', r['phone'])   # her phone keeps everyone's words, 24 hours
        self.assertEqual(r['page']['by_store'], {'material': {'health': 1}})
        self.assertTrue(r['page']['filter'])

    def test_turning_the_switch_on_archives_first(self):
        r = run_case('sweep')
        self.assertEqual(r['library'], ['小爱 我周末想去海边看日落'])
        self.assertEqual(r['archived'], 1)
        self.assertIn('小爱 我最近失眠好严重', r['copy'])
        off = run_case('sweep_off')
        self.assertEqual(off['library'], ['小爱 我最近失眠好严重', '小爱 我周末想去海边看日落'])
        self.assertEqual(off['archived'], 0)


class OldNumbers(unittest.TestCase):
    def test_taken_out_at_start_archived_first(self):
        r = run_case('migrate')
        self.assertEqual(r['counts'], {'library': 1, 'phone': 1, 'users': 1})
        self.assertEqual(r['again'], {})
        self.assertEqual(r['phone'], ['@桃子 明天见 我号 [号码]', '@某人 你还在吗'])
        self.assertEqual(r['library'], ['@桃子 明天见 我号 [号码]'])
        self.assertEqual(r['user']['latest_text'], '@桃子 明天见')
        self.assertEqual(r['user']['sender_id'], '10004')                 # ids are not text
        self.assertEqual(r['ids_kept'], ['10002', '10004'])
        self.assertEqual(r['archived'], ['before', 'before', 'library.before'])


if __name__ == '__main__':
    unittest.main()
