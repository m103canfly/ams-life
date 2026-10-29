"""What she keeps keeps its numbers (the owner, 10-29: QQ numbers, group numbers, "@名字(号码)");
someone deleted is 某人 and his number goes; red lines are not kept (step 1-3-5).

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


class DropGone(unittest.TestCase):
    def test_at_and_numbers_stay_but_her_and_someone_deleted(self):
        s = discretion.drop_gone
        self.assertEqual(s(' @桃子(10004) 一起玩'), ' @桃子(10004) 一起玩')            # as AstrBot wrote it
        self.assertEqual(s('@小爱bot(20002) 在吗', her=['20002'], her_name='小爱'), '@小爱 在吗')
        self.assertEqual(s('@(10005) 快来'), '@(10005) 快来')
        self.assertEqual(s('@10005 快来'), '@10005 快来')
        self.assertEqual(s('@阿星(10003) 在吗', gone=['10003']), '@某人 在吗')
        self.assertEqual(s('@10003 在吗', gone=['10003']), '@某人 在吗')
        self.assertEqual(s('加我 10002，群 900001', numbers=['10003']), '加我 10002，群 900001')
        self.assertEqual(s('阿星的号 10003', gone=['10003'], numbers=['10003']), '阿星的号 [号码]')
        self.assertEqual(s('分数 1100030 和 123456', numbers=['10003']), '分数 1100030 和 123456')   # whole numbers only

    def test_numbers_go_with_names_elsewhere(self):
        h = discretion.hide_numbers
        known = ['10002', '10004', '900001']
        self.assertEqual(h(' @桃子(10004) 加我 10002，群 900001，隔壁群 900077', known),
                         ' @有人 加我 [号码]，群 [号码]，隔壁群 900077')   # a group she is not in: not known
        self.assertEqual(h('@10004 来', known), '@有人 来')
        # an @ is always someone: his number and name go, known to her or not
        self.assertEqual(h('@路人(10099) 来 @(10098) 也来', known), '@有人 来 @有人 也来')
        self.assertEqual(h('分数 1100020', known), '分数 1100020')

    def test_anonymize_to(self):
        self.assertEqual(discretion.anonymize('阿星你还在吗', ['阿星'], to='某人'), '某人你还在吗')


class WhatSheKeeps(unittest.TestCase):
    def test_numbers_stay_in_her_phone_memory_and_events(self):
        # the owner, 10-29: QQ numbers and group numbers are kept, an @ as AstrBot wrote it
        r = run_case('at')
        self.assertEqual(r['phone'][:4], ['@小爱 你好呀', '问问 @桃子(10004) 在吗', '@(10005) 快来',
                                         '我的号是 10002 加我 游戏里的分是 123456'])
        self.assertIn('记得提醒我 @桃子(10004) 明天要还我书 我号 10002 @小爱', r['library'])
        self.assertIn('记得提醒我 @桃子(10004) 明天要还我书 我号 10002 @小爱', r['loops'])
        said = '小爱 我的号是 10002，我们群号是 900001 @桃子(10004) 周末见'
        self.assertIn(said, r['phone'])
        self.assertIn(said, r['library'])
        self.assertEqual(r['event'], {'title': '柠檬 10002 约周末', 'event': '柠檬（10002）在群 900001 约 @桃子(10004) 周末见'})
        for text in r['phone'] + r['library'] + r['loops']:
            self.assertNotIn('20002', text)    # an @ of her is her name

    def test_group_cards_with_spaces_and_brackets(self):
        # people who never wrote here: the @ as AstrBot wrote it, whatever the card holds
        r = run_case('at')
        self.assertIn('明天叫上 @Tom Lee(10077) 一起去爬山', r['library'])
        self.assertIn('记得提醒 @小明（学生）(10078) 周五交作业', r['library'])

    def test_what_astrbot_sends_the_model(self):
        r = run_case('at')
        self.assertEqual(r['asked'][0], '记得提醒我 @桃子(10004) 明天要还我书 我号 10002 @小爱')
        self.assertIn('小爱 我的号是 10002，我们群号是 900001 @桃子(10004) 周末见', r['asked'])
        self.assertIn('某人的号是 [号码] @某人 你在吗', r['asked'])   # someone deleted, as in what she keeps
        for text in r['asked']:
            self.assertNotIn('阿星(', text)
            self.assertNotIn('10003', text)
            self.assertNotIn('20002', text)

    def test_someone_deleted_is_somebody(self):
        r = run_case('at')
        self.assertEqual(r['phone'][4:6], ['@某人 某人你还在吗', '某人昨天也这么说'])
        self.assertIn('某人的号是 [号码] @某人 你在吗', r['phone'])   # his number, said as a number, goes too
        self.assertFalse([t for t in r['phone'] + r['library'] + r['loops'] if '阿星' in t or '10003' in t])
        self.assertEqual(r['files_with_his_number'], [])   # nowhere in the data folder (the registry aside)

    def test_red_lines_are_counted_not_held_back_by_default(self):
        # the owner, 10-28: nothing is held back in the first version; the panel counts what
        # is kept now, afresh (nothing of a hit is recorded, what is deleted is not counted)
        r = run_case('redline')
        self.assertIn('小爱 我最近失眠好严重 每天都睡不着', r['library'])
        self.assertEqual(r['page'], {'filter': False, 'by_line': {'health': 2},
                                     'by_store': {'memory': {'health': 1}, 'material': {'health': 1}}})
        self.assertEqual(r['page_after_delete'], {'filter': False, 'by_line': {}, 'by_store': {}})
        self.assertNotIn('redline_counts.json', r['files'])

    def test_the_panel_counts_her_phone_without_writing_it(self):
        # opening the panel writes nothing: an expired line stays on disk until her own sweep
        # takes it, and is not counted
        r = run_case('census_expired')
        self.assertTrue(r['unchanged'])
        self.assertEqual(r['page']['by_store'], {'material': {'health': 1}})

    def test_red_lines_are_not_kept_when_the_switch_is_on(self):
        r = run_case('redline_on')
        self.assertEqual(r['library'], ['小爱 我周末想去海边看日落'])
        self.assertIn('小爱 我最近失眠好严重 每天都睡不着', r['phone'])   # her phone keeps everyone's words, 24 hours
        self.assertEqual(r['page']['by_store'], {'material': {'health': 1}})
        self.assertTrue(r['page']['filter'])

    def test_changed_words_are_gone_over_like_new_ones(self):
        # a memory already kept whose words change: someone deleted out (numbers stay); over a
        # red line (switch on), not kept
        off = run_case('changed')
        self.assertEqual(off['library'], ['小爱 我周末想和 @桃子(10004) @某人 去海边看日落 我号 10002',
                                          '小爱 我最近失眠好严重 每天都睡不着'])
        on = run_case('changed_on')
        self.assertEqual(on['library'], ['小爱 我周末想和 @桃子(10004) @某人 去海边看日落 我号 10002'])
        self.assertNotIn('10003', json.dumps(off['library'] + on['library']))

    def test_a_delete_rewrite_is_not_taken_for_changed_words(self):
        r = run_case('after_delete')
        self.assertIn('小爱 某人明天要来玩', r['library'])                 # rewritten by the delete
        self.assertEqual(r['scrubbed_again'], 0)                          # and not gone over again

    def test_turning_the_switch_on_archives_first(self):
        r = run_case('sweep')
        self.assertEqual(r['library'], ['小爱 我周末想去海边看日落'])
        self.assertEqual(r['archived'], 1)
        self.assertIn('小爱 我最近失眠好严重', r['copy'])
        off = run_case('sweep_off')
        self.assertEqual(off['library'], ['小爱 我最近失眠好严重', '小爱 我周末想去海边看日落'])
        self.assertEqual(off['archived'], 0)

    def test_turning_the_switch_on_sweeps_each_places_events_too(self):
        r = run_case('sweep')
        both = ('archives/events.jsonl', 'archives/sessions/made-up-place/events.jsonl')
        self.assertEqual(r['events'], {rel: ['e2'] for rel in both})          # the archive and the place's copy
        self.assertEqual(r['events_archived'], sorted(both))                    # each archived first
        off = run_case('sweep_off')
        self.assertEqual(off['events'], {rel: ['e1', 'e2'] for rel in both})
        self.assertEqual(off['events_archived'], [])


class AtStart(unittest.TestCase):
    def test_someone_deleted_taken_out_at_start_archived_first(self):
        # kept before: numbers stay (the owner, 10-29); someone deleted goes, his file copied first
        r = run_case('migrate')
        self.assertEqual(r['counts'], {'phone': 1, 'users': 1})
        self.assertEqual(r['again'], {})
        self.assertEqual(r['phone'], ['@桃子(10004) 明天见 我号 10002', '@某人 你还在吗'])
        self.assertEqual(r['library'], ['@桃子(10004) 明天见 我号 10002'])
        self.assertEqual(r['user']['latest_text'], '@桃子(10004) 明天见 某人也来')
        self.assertEqual(r['user']['sender_id'], '10004')                 # ids are not text
        self.assertEqual(r['ids_kept'], ['10002', '10004'])
        self.assertEqual(r['archived'], ['before', 'before'])


if __name__ == '__main__':
    unittest.main()
