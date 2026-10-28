"""The group members she knows, wired into the plugin (step 1-3-3): what a reply sees where, the
nightly update, what people are called and how it is made anonymous, the panel. Each case runs
in a fresh interpreter (tests/impressions_cases.py). All numbers and names are made up.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import discretion  # noqa: E402

_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'impressions_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class WhatAReplySees(unittest.TestCase):
    """The owner's table: her group all of it; another group where he is, what he is called;
    his own private chat, name and how he talks (topics he raised there); anyone else's, nothing."""

    def test_the_table(self):
        r = run_case('views')
        self.assertEqual(r['her_group'], '[认识的人] 柠檬（大家叫 小柠、柠柠）：说话很快，爱用语气词；常聊 抽卡、副本')
        self.assertEqual(r['other_group_present'], '[认识的人] 柠檬（大家叫 小柠、柠柠）')
        self.assertEqual(r['other_group_absent'], '')
        self.assertEqual(r['her_private'], '[认识的人] 柠檬（大家叫 小柠、柠柠）：说话很快，爱用语气词；常聊 副本')
        self.assertEqual(r['someone_elses_private'], '')

    def test_no_numbers_no_qq(self):
        for line in run_case('views').values():
            self.assertNotRegex(line, r'\d')


class Nightly(unittest.TestCase):
    def test_off_by_default(self):
        self.assertEqual(run_case('nightly')['off'], {'answer': {}, 'calls': 0})

    def test_once_a_night_per_group(self):
        on = run_case('nightly')['on']
        self.assertEqual(on['first'], {'group:900001': {'called': 1, 'picked': 2, 'written': 2, 'rejected': 0}})
        self.assertEqual(on['again'], {'group:900001': {'skipped': 'tried today'}})
        self.assertEqual(on['calls'], 1)

    def test_who_and_what(self):
        r = run_case('nightly')
        people = r['people']
        self.assertEqual(sorted(people), ['10001', '10002'])           # 阿星 is registered: no impression
        self.assertEqual(people['10002']['aliases'], ['柠柠'])           # others called her that, twice
        self.assertEqual(people['10001']['aliases'], [])                # nobody called him 柠柠子
        self.assertEqual(r['prompt_has'], {'柠檬': False, '芒果': False, '阿星': False, '柠柠': True, '10002': False})

    def test_the_panel(self):
        r = run_case('nightly')
        page = r['page'][0]
        self.assertEqual(page['place'], 'group:900001')
        self.assertEqual({p['qq']: p['style'] for p in page['people']},
                         {'10001': '说话慢慢的', '10002': '爱用语气词，常接别人的梗'})
        self.assertEqual(r['delete'], {'status': 'ok', 'data': {'person': '10002', 'groups': 1}})
        self.assertEqual(r['after_delete'], ['10001'])
        self.assertIn(['impression', '10002'], r['registry_kinds'])
        self.assertEqual(r['next_night'], ['10001'])                    # she does not write one of her again
        self.assertEqual(r['after_person'], [])                         # deleting the person takes his too


class Names(unittest.TestCase):
    def test_what_people_are_called_is_made_anonymous(self):
        r = run_case('anon')
        self.assertEqual(r['names'], ['10002', '小柠', '柠柠', '柠檬'])  # the owner's name and hers
        self.assertEqual(r['text'], '有人说周末去爬山，有人也去')
        self.assertEqual(r['event_elsewhere'], '有人约大家周末去爬山')

    def test_one_character_names_only_where_they_name_someone(self):
        a = discretion.anonymize
        self.assertEqual(a('@鹿 快来', ['鹿']), '@有人 快来')
        self.assertEqual(a('鹿说今天下雨', ['鹿']), '有人说今天下雨')
        self.assertEqual(a('鹿：好的', ['鹿']), '有人：好的')
        for kept in ('小鹿乱撞', '一只鹿跑过去', '@鹿鹿 你好'):
            self.assertEqual(a(kept, ['鹿']), kept)

    def test_one_letter_names(self):
        a = discretion.anonymize
        self.assertEqual(a('@A 快来', ['A']), '@有人 快来')
        self.assertEqual(a('A说今天下雨', ['A']), '有人说今天下雨')
        for kept in ('@Alice 你好', 'BA说的'):
            self.assertEqual(a(kept, ['A']), kept)

    def test_english_names_are_whole_words(self):
        a = discretion.anonymize
        self.assertEqual(a('Al说他也去', ['Al']), '有人说他也去')
        self.assertEqual(a('@Al 快来', ['Al']), '@有人 快来')
        for kept in ('Alice 你好', 'Al2 在吗', 'HAL 来了'):
            self.assertEqual(a(kept, ['Al']), kept)
        self.assertEqual(a('柠檬汁', ['柠檬']), '有人汁')             # Chinese as before


class NamesStay(unittest.TestCase):
    """PR #10 review: the names he went by stay for making things anonymous after his impression
    is deleted or an alias is pushed out of the last four; they go when he is deleted."""

    def test_after_the_impression_is_deleted(self):
        r = run_case('anon_kept')
        self.assertEqual(r['before'], '有人说周末去爬山')
        self.assertFalse(r['impression_left'])
        self.assertEqual(r['after_delete'], '有人说周末去爬山')
        self.assertEqual(r['event_after_delete'], '有人约大家周末去爬山')

    def test_after_an_alias_is_pushed_out(self):
        r = run_case('anon_kept')
        self.assertEqual(r['aliases_10006'], ['阿二', '阿三', '阿四', '阿五'])
        self.assertEqual(r['pushed_out'], '有人说今天下雨')

    def test_deleting_the_person_takes_them(self):
        self.assertEqual(run_case('anon_kept')['names_after_person'], ['10002'])


class Review(unittest.TestCase):
    def test_his_name_here_in_another_group(self):
        self.assertEqual(run_case('card_here')['other_group'], '[认识的人] 小柠檬（大家叫 柠柠）')

    def test_red_lines_by_the_switch(self):
        self.assertEqual((run_case('red')['seen'], run_case('red')['counts']), (True, {'finance': 1, 'judgement': 2}))
        self.assertEqual((run_case('red_on')['seen'], run_case('red_on')['counts']),
                         (False, {'finance': 1, 'judgement': 2}))

    def test_judgements_by_the_switch(self):
        # what a person is ("性格开朗", "靠谱"): written down with the switch off (counted), not when on
        self.assertEqual(run_case('red')['written'], {'style': '性格开朗，说话很快', 'topics': ['靠谱攻略']})
        self.assertEqual(run_case('red_on')['written'], {'style': '', 'topics': []})

    def test_the_nightly_material_codes_every_name_she_knows(self):
        r = run_case('material')
        self.assertEqual(r['prompt_has'], {'大芒': False, '芒芒': False, '鹿说': False, '芒果': False, '柠檬': False})
        self.assertTrue(any(ln.startswith('- P2今天没来') for ln in r['lines']), r['lines'])   # 大芒: elsewhere
        self.assertTrue(any(ln.startswith('- P2快来打本') for ln in r['lines']), r['lines'])   # 芒芒: the owner's
        self.assertTrue(any(ln.startswith('- Q1说他也去') for ln in r['lines']), r['lines'])   # 鹿


if __name__ == '__main__':
    unittest.main()
