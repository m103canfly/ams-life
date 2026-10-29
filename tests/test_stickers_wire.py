"""Step 2 (丙): her stickers in the plugin (mixin_stickers.py), end to end in stickers_cases.py with a
stand-in model, NapCat client and picture server. All made up; the pictures are a few bytes made there."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'stickers_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


class Offered(unittest.TestCase):
    def test_a_few_offered_she_names_one_it_goes_as_a_sticker(self):
        r = run_case('reply')
        n = r['named']
        self.assertTrue(n['offer_in_prompt'])
        self.assertEqual(n['offered'][0], '一只在笑的猫')            # her mood and the talk: the nearest first
        self.assertIn('主人给的兔子', n['offered'])                   # what the owner gave is offered too
        self.assertEqual(n['text'], '好呀，你最棒')                    # the mark is not sent
        self.assertEqual(n['chain'], [['Plain', '好呀，你最棒']])
        # sent by the adapter's own client: one of the two actions, to this group only, a sticker
        self.assertEqual(r['calls'], [{'action': 'send_group_msg', 'group_id': 900001,
                                       'segments': [['image', 1, '[动画表情]', 'base64://']],
                                       'keys': ['group_id', 'message']}])
        self.assertEqual(r['uses_after'], 1)
        self.assertEqual(r['sent'], [])                               # nothing went the plain way

    def test_only_an_offered_one_and_qq_faces_stay_faces(self):
        r = run_case('reply')
        self.assertNotIn('一只在笑的猫', r['not_offered']['offered'])  # sent a moment ago: not again
        self.assertEqual(r['not_offered']['text'], '嗯嗯')              # [表情包:9] was not offered
        self.assertFalse(r['not_offered']['sent_flag'])
        self.assertEqual(r['face_stays']['chain'], [['Plain', '好的'], ['Face', 14]])   # 甲's QQ face
        self.assertEqual(r['calls_total'], 1)

    def test_kept_as_sent(self):
        r = run_case('reply')
        self.assertEqual(r['phone'], ['好呀，你最棒\n[表情包：一只在笑的猫]', '嗯嗯', '好的[表情:微笑]'])
        self.assertTrue(r['named']['sent_flag'])                      # AstrBot's history is settled to it

    def test_a_sticker_alone(self):
        r = run_case('alone')
        self.assertTrue(r['r']['stopped'])                            # AstrBot sends nothing
        self.assertEqual(r['calls'], 1)                               # the plugin sends the sticker
        self.assertEqual(r['phone'], ['[表情包：一只在笑的猫]'])

    def test_napcat_says_no_a_plain_picture(self):
        r = run_case('fallback')
        self.assertEqual(r['r']['text'], '好呀')
        self.assertEqual(r['sent'][0], {'umo': 'default:GroupMessage:900001', 'chain': [['Image', None, 'base64://']]})
        self.assertEqual(r['sent_total'], 2)                          # no client at all: the same

    def test_switch_off_nothing_sent_marks_still_taken_out(self):
        r = run_case('off')
        self.assertFalse(r['r']['offer_in_prompt'])
        self.assertEqual(r['r']['text'], '好呀')                       # a mark never reaches QQ
        self.assertEqual(r['old_mark'], '好呀')                        # nor one copied from her history
        self.assertEqual(r['calls'], [])

    def test_a_label_the_send_check_holds_back_the_words_still_go(self):
        r = run_case('held')
        self.assertEqual(r['r']['text'], '好呀，你最棒')
        self.assertFalse(r['r']['stopped'])
        self.assertFalse(r['r']['sent_flag'])
        self.assertEqual(r['calls'], 0)                                # no call_action
        self.assertEqual(r['sent'], [])                                # and no plain picture either


class Looked(unittest.TestCase):
    def test_qq_stickers_in_passing_one_look_each_kept_by_the_program(self):
        r = run_case('look')
        self.assertEqual(len(r['looks']), 3)                          # at most three a message
        self.assertEqual(r['fetched'], ['https://gchat.qpic.cn/a.png'])   # only the one she keeps
        self.assertEqual(r['kept'], [['一只在笑的猫', '10001', 'group:900001', 'self']])
        # every look is noted with who sent it and where (deleting him deletes it)
        self.assertEqual(r['cache'], [['一只在笑的猫', '10001', 'group:900001'], ['一张证件照', '10001', 'group:900001'],
                                      ['写着群友名字的图', '10001', 'group:900001']])
        self.assertEqual(r['looks_after'], 3)                         # the same picture: no second look
        self.assertEqual(r['spend_kinds'], ['calls', 'vision'])       # in the day's money, once

    def test_someone_deleted_is_not_looked_at(self):
        r = run_case('look')
        self.assertEqual(r['kept_after_gone'], 1)
        self.assertEqual(r['looks_after_gone'], 3)


class Forgotten(unittest.TestCase):
    def test_deleting_a_person_deletes_what_he_sent(self):
        r = run_case('forget')
        self.assertEqual(r['result']['counts']['stickers'], 1)
        self.assertEqual(r['left'], ['一只在哭的狗', '主人给的兔子'])   # the others', and the owner's gift
        self.assertEqual(r['cache_left'], ['柠檬的图'])
        self.assertEqual(r['result']['counts']['pictures'], 1)


class Fetching(unittest.TestCase):
    """Pictures she keeps come from QQ's picture servers only (no network here: refused first)."""

    def setUp(self):
        if str(HERE.parent) not in sys.path:
            sys.path.insert(0, str(HERE.parent))
        import stickers   # the standard library only: nothing of the plugin is loaded here
        self.m = stickers

    def test_refused_before_any_connection(self):
        for url in ('https://evil.example/x.png', 'http://127.0.0.1/x.png', 'file:///c:/x.png',
                    'https://gchat.qpic.cn:8080/x.png', 'https://u:p@gchat.qpic.cn/x.png'):
            self.assertEqual(self.m.fetch_picture(url), b'', url)

    def test_a_redirect_away_from_qq_is_not_followed(self):
        h = self.m.QQOnlyRedirect()
        with self.assertRaises(urllib.error.URLError):
            h.redirect_request(None, None, 302, 'Found', {}, 'https://evil.example/x.png')


if __name__ == '__main__':
    unittest.main()
