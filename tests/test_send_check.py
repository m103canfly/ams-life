"""The last look at a reply before it is sent (step 2, global_memory; send_check.py), and the
plugin around it (mixin_send_check.py) end to end in send_check_cases.py with a fake model.
All words, names and numbers are made up."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import send_check as sc  # noqa: E402

SECRET = '芒果私下说：我的暗号是蓝鲸三号，下周三去医院复查'
NO = [{'id': 'memory:m1', 'text': SECRET, 'names': ['芒果'], 'vec': [1.0, 0.0, 0.0]}]
_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'send_check_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class Look(unittest.TestCase):
    def test_said_as_it_is(self):
        r = sc.check('偷偷告诉你，蓝鲸三号是他的暗号', NO, '你好呀')
        self.assertTrue(r['leak'])
        self.assertIn('piece', r['why']['memory:m1'])

    def test_a_number_of_it(self):
        no = [{'id': 'memory:m2', 'text': '他家门锁密码是 4071', 'names': [], 'vec': None}]
        self.assertTrue(sc.check('密码应该是4071吧', no)['leak'])

    def test_said_another_way_is_caught_by_the_vectors(self):
        r = sc.check('他好像下礼拜要去看病', NO, '', reply_vec=[0.9, 0.3, 0.0])
        self.assertTrue(r['leak'])
        self.assertEqual(r['why']['memory:m1'], ['cosine'])

    def test_split_up(self):
        # "蓝鲸……三号": no four in a row left; the meaning still is
        r = sc.check('蓝鲸……嗯，三号', NO, '', reply_vec=[0.95, 0.2, 0.0])
        self.assertTrue(r['leak'])

    def test_close_is_only_noted(self):
        r = sc.check('最近大家都挺忙的', NO, '', reply_vec=[0.8, 0.6, 0.0])
        self.assertFalse(r['leak'])
        self.assertEqual(r['close'][0][0], 'memory:m1')

    def test_a_name_from_it(self):
        self.assertTrue(sc.check('芒果最近还好吗', NO, '')['leak'])
        # his name said here already (he is in this chat's talk): not a leak by itself
        self.assertFalse(sc.check('芒果最近还好吗', NO, '芒果：大家好')['leak'])

    def test_what_may_be_said_here_is_not_held_back(self):
        allowed = '（这里，柠檬说过）我下周三去医院复查'
        self.assertFalse(sc.check('下周三去医院复查别忘了', NO, allowed)['leak'])

    def test_common_words_are_not_pieces(self):
        common = sc.common_pieces([('下周三去医院复查', '10002', 'group:900001'),
                                   ('我下周三去医院复查', '10003', 'group:900002')])
        self.assertIn('医院复查', common)
        self.assertFalse(sc.check('下周三去医院复查别忘了', NO, '', common)['leak'])

    def test_one_persons_words_said_again_and_again_stay_his(self):
        common = sc.common_pieces([('我的暗号是蓝鲸三号', '10001', 'private:10001')] * 5)
        self.assertNotIn('蓝鲸三号', common)
        self.assertTrue(sc.check('蓝鲸三号', NO, '', common)['leak'])

    def test_nothing_to_hold_back(self):
        self.assertFalse(sc.check('随便聊聊', [], '')['leak'])
        self.assertFalse(sc.check('', NO, '')['leak'])

    def test_names_as_names(self):
        self.assertTrue(sc.mentions('@鹿 你好', '鹿'))
        self.assertFalse(sc.mentions('小鹿乱撞', '鹿'))
        self.assertTrue(sc.mentions('「芒果」来了', '芒果'))


class InThePlugin(unittest.TestCase):
    """send_check_cases.py: global_memory on; mango tells her a secret in private; then in a
    group the (fake) model answers with it."""

    def test_said_once_more(self):
        r = run_case('redo')
        g = r['group']
        self.assertEqual(g['sent'], '周末一起去爬山吧')               # the words said once more
        self.assertFalse(g['stopped'])
        self.assertIn('只回这一句话本身', r['redo_prompt'])            # asked once, with the line
        self.assertEqual(r['counts']['redone'], 1)
        self.assertIn('send check: redone (memory:', '\n'.join(r['log']))
        # what AstrBot will save: the words sent, no thinking, the thinking on the event cleared
        self.assertEqual(g['history'], [{'type': 'text', 'text': '周末一起去爬山吧'}])
        self.assertIsNone(g['reasoning'])
        # her phone and memory have the words sent, never the first ones
        self.assertNotIn('蓝鲸三号', json.dumps(r['kept'], ensure_ascii=False))
        self.assertIn('周末一起去爬山吧', json.dumps(r['kept'], ensure_ascii=False))

    def test_nothing_sent(self):
        r = run_case('hold')
        g = r['group']
        self.assertTrue(g['stopped'])
        self.assertEqual(r['counts']['held'], 1)
        self.assertIn('send check: held back (memory:', '\n'.join(r['log']))
        self.assertNotIn('蓝鲸三号', json.dumps(r['kept'], ensure_ascii=False))
        self.assertTrue(all('蓝鲸' not in line for line in r['log']))   # ids only in the log

    def test_what_may_be_said_goes_out(self):
        r = run_case('fine')
        g = r['group']
        self.assertFalse(g['stopped'])
        self.assertEqual(g['sent'], '周末去爬山记得带水')
        self.assertEqual(r['counts'].get('redone', 0) + r['counts'].get('held', 0), 0)
        self.assertEqual(r['redo_prompt'], '')
        # the thinking is taken out of what AstrBot saves even when nothing was wrong
        self.assertEqual(g['history'], [{'type': 'text', 'text': '周末去爬山记得带水'}])

    def test_his_own_private_chat_is_not_checked_against_itself(self):
        r = run_case('own_chat')
        self.assertEqual(r['private']['sent'], '记得呀，你的暗号是蓝鲸三号')
        self.assertFalse(r['private']['stopped'])

    def test_switch_off_nothing_changes(self):
        r = run_case('off')
        self.assertEqual(r['group']['sent'], '偷偷告诉你，芒果的暗号是蓝鲸三号')
        self.assertFalse(r['group']['stopped'])
        self.assertEqual(r['counts'], {})
        # nothing of AstrBot's saved turn is touched
        self.assertEqual(r['group']['history'][0]['type'], 'think')


if __name__ == '__main__':
    unittest.main()
