"""Step 2 (丙): her stickers in the plugin (mixin_stickers.py), end to end in stickers_cases.py with a
stand-in model, NapCat client and picture server. All made up; the pictures are a few bytes made there."""
import json
import os
import shutil
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
    def test_offers_are_not_saved_in_five_turns(self):
        turns = run_case('history')['turns']
        self.assertEqual(len(turns), 5)
        for turn in turns:
            self.assertTrue(turn['offer_in_prompt'])
            self.assertIn('[她的表情包]', str(turn['model_parts']))
            self.assertNotIn('[她的表情包]', str(turn['kept_parts']))

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

    def test_a_label_the_send_check_holds_back_the_whole_reply(self):
        r = run_case('held')
        self.assertEqual(r['r']['text'], '好呀，你最棒')
        self.assertTrue(r['r']['stopped'])
        self.assertFalse(r['r']['sent_flag'])
        self.assertEqual(r['calls'], 0)                                # no call_action
        self.assertEqual(r['sent'], [])                                # and no plain picture either


class Looked(unittest.TestCase):
    def test_called_reply_opens_queue_without_waiting(self):
        r = run_case('called_open')
        self.assertEqual(r['before'], 0)
        self.assertEqual(r['after'], 3)

    def test_scored_reply_opens_queue_without_waiting(self):
        r = run_case('scored_open')
        self.assertTrue(r['asked'])
        self.assertEqual(r['before'], 0)
        self.assertEqual(r['after'], 3)

    def test_qq_stickers_wait_for_open_then_are_kept_by_the_program(self):
        r = run_case('look')
        self.assertEqual(r['looks_before_open'], 0)
        self.assertEqual(len(r['looks']), 3)                          # at most three a message
        self.assertEqual(r['fetched'], ['https://gchat.qpic.cn/a.png', 'https://gchat.qpic.cn/a.png',
                                        'https://gchat.qpic.cn/b.png', 'https://gchat.qpic.cn/c.png'])
        self.assertEqual(len(r['content_cache']), 3)
        self.assertEqual(r['kept'], [['一只在笑的猫', '10001', 'group:900001', 'self']])
        # every look is noted with who sent it and where (deleting him deletes it)
        self.assertEqual(r['cache'], [['一只在笑的猫', '10001', 'group:900001'], ['一张证件照', '10001', 'group:900001'],
                                      ['写着群友名字的图', '10001', 'group:900001']])
        self.assertEqual(r['looks_after'], 3)                         # the same picture: no second look
        self.assertEqual(r['spend_kinds'], ['calls', 'vision', 'vision_calls'])       # in the day's money, once

    def test_someone_deleted_is_not_looked_at(self):
        r = run_case('look')
        self.assertFalse(r['queue_has_deleted'])
        self.assertEqual(r['kept_after_gone'], 1)
        self.assertEqual(r['looks_after_gone'], 3)


class ImageInput(unittest.TestCase):
    def test_text_file_is_not_sent_and_reply_continues(self):
        r = run_case('non_image_reply')
        self.assertEqual(r['vision_calls'], 0)
        self.assertEqual(r['text'], 'okay')


class VisionStatus(unittest.TestCase):
    def test_vision_shown_only_after_a_look_today(self):
        r = run_case('vision_status')
        self.assertFalse(r['off_empty'])
        self.assertFalse(r['on_empty'])
        self.assertEqual(r['on_used']['calls'], 1)
        self.assertEqual(r['on_used']['reply'], 1)
        self.assertEqual(r['off_used'], r['on_used'])


class VisionCounting(unittest.TestCase):
    def test_each_vision_source_and_phone_selfie_are_shown(self):
        r = run_case('vision_sources')
        self.assertEqual([r['after_reply'][k] for k in ('reply', 'browse', 'owner_add')], [1, 0, 0])
        self.assertEqual([r['after_browse'][k] for k in ('reply', 'browse', 'owner_add')], [1, 1, 0])
        self.assertEqual([r['after_owner_add'][k] for k in ('reply', 'browse', 'owner_add')], [1, 1, 1])
        self.assertEqual(r['after_owner_add']['calls'], 3)
        self.assertEqual(r['gift'], 'ok')
        self.assertEqual(r['phone_before'], 0)
        self.assertEqual(r['phone_after'], 1)
        self.assertEqual(r['calls'], 3)
        self.assertEqual(set(r['vision_record']), {'reply', 'browse', 'owner_add', 'last'})
        self.assertGreater(r['vision_record']['last'], 0)

    def test_three_paths_count_without_stopping_for_both_provider_types(self):
        for case in ('count_astrbot', 'count_api'):
            with self.subTest(provider=case):
                r = run_case(case)
                self.assertEqual(r['marks'], {'31': 31, '100': 100})
                self.assertEqual(r['calls'], 102)
                self.assertEqual(r['last_gift'], {'status': 'ok', 'labelled': True})
                self.assertEqual(r['panel']['calls'], 102)
                self.assertEqual([r['panel'][k] for k in ('reply', 'browse', 'owner_add')], [34, 34, 34])
                self.assertEqual(r['panel_without_decide'], r['panel'])
                self.assertEqual(r['spent'], 0)
                self.assertFalse(r['panel_next_day'])
                self.assertEqual(r['calls_next_day'], 103)
                self.assertEqual(r['panel_after_next']['calls'], 1)
                self.assertEqual(r['panel_after_next']['reply'], 1)


class OwnersPage(unittest.TestCase):
    """The owner's page of her stickers (pages/stickers): page/stickers, .../image, .../delete, .../add."""

    def test_the_list_says_where_from_never_a_number(self):
        r = run_case('page')
        # newest kept first; days left counted from when each was last used (kept: not used yet)
        self.assertEqual(r['list'], [['一只在哭的狗', '私聊1', False, 29], ['一只在笑的猫', '群1', False, 28],
                                     ['旧的猫', '旧小爱', False, 2]])
        self.assertEqual(r['soon'], ['旧的猫', '一只在笑的猫', '一只在哭的狗'])
        for number in ('900001', '10001', '10002'):
            self.assertNotIn(number, r['list_text'])
        self.assertEqual(r['sources'], ['旧小爱', '群1', '私聊1'])
        self.assertEqual(r['only_sad'], ['一只在哭的狗'])

    def test_one_picture_by_its_id_only(self):
        r = run_case('page')
        self.assertEqual(r['image'], ['ok', 'data:image/png;base64,'])
        self.assertEqual(r['image_missing'], 'error')

    def test_the_owner_adds_pictures_only(self):
        r = run_case('page')
        self.assertEqual(r['add'], 'ok')
        self.assertEqual(r['add_html']['status'], 'error')
        self.assertEqual(r['add_html']['message'], '不是图片')
        self.assertEqual(r['add_svg_named_png'], 'error')            # a name that says png is not enough
        self.assertEqual(r['add_big'], 'error')
        self.assertEqual(r['add_huge_side'], 'error')
        self.assertEqual(r['owner_row'], ['主人的小猫', '10009', 'owner'])

    def test_the_owners_gifts_stay_until_the_owner_deletes_them(self):
        r = run_case('page')
        self.assertEqual(r['after_sweep'], ['主人的小猫'])            # a year on: only the gift is left
        self.assertEqual((r['delete_gift'], r['delete_again']), ('ok', 'error'))
        self.assertEqual(r['left'], [])

    def test_deleted_on_the_page_never_kept_again_unless_the_owner_adds_it(self):
        r = run_case('page')
        self.assertEqual(r['dropped_file'], [r['gift_id']])           # a fingerprint, nothing else
        self.assertEqual(r['keep_again'], ['', '主人删过'])
        self.assertEqual(r['owner_again'], 'ok')


class PageLook(unittest.TestCase):
    """The page in the panel's look (#37): 月白 on clear glass, no glow around words (item 33)."""

    def test_the_panels_colours_and_no_glow(self):
        import re
        pages = HERE.parent / 'pages'
        page = (pages / 'stickers' / 'stickers.css').read_text('utf-8')
        look = (pages / 'dashboard' / 'look.css').read_text('utf-8')
        self.assertNotIn('text-shadow', page)

        def values(css, theme):
            block = re.search((r':root\{(.*?)\}' if theme == 'light' else r'\[data-theme="dark"\]\{(.*?)\}'), css, re.S).group(1)
            return dict(re.findall(r'(--[\w-]+):\s*([^;]+);', block))
        for theme in ('light', 'dark'):
            mine, panel = values(page, theme), values(look, theme)
            for key in ('--bg', '--bg2', '--ink', '--text', '--muted', '--faint', '--accent', '--accent2',
                        '--accent-strong', '--glass-thin', '--glass-thick', '--glass-pop'):
                self.assertEqual(mine.get(key), panel.get(key), (theme, key))


class FromThePanel(unittest.TestCase):
    """The panel's "她的表情包" opens a copy of the page (pages/dashboard/stickers/) in the panel's own frame:
    AstrBot gives a plugin page no way to another page of the plugin. Only there is there a way back."""
    PAGES = HERE.parent / 'pages'

    def test_the_panels_copy_is_the_page(self):
        def files(folder):
            return {p.name: p.read_bytes().replace(b'\r\n', b'\n') for p in folder.iterdir() if p.is_file()}
        page, copy = files(self.PAGES / 'stickers'), files(self.PAGES / 'dashboard' / 'stickers')
        self.assertEqual(sorted(copy), sorted(page))
        for name in page:
            self.assertEqual(copy[name], page[name], name + ': copy pages/stickers/ into pages/dashboard/stickers/')

    def test_the_panel_opens_it_in_its_own_frame(self):
        import re
        dash = self.PAGES / 'dashboard'
        link = re.search(r'<a class="nav-item" id="stickersLink" href="([^"]*)"[^>]*>', (dash / 'index.html').read_text('utf-8'))
        self.assertEqual(link.group(1), './stickers/?from=panel')
        self.assertNotIn('target=', link.group(0))
        app = (dash / 'app.js').read_text('utf-8')
        self.assertIn('document.querySelectorAll(".nav-item[data-view]").forEach', app)   # the link is no view
        self.assertIn('if (v && $("view-" + v)) switchView(v);', app)                       # ?view= only a real one

    @unittest.skipUnless(shutil.which('node'), 'needs Node.js')
    def test_the_way_back_only_from_the_panel(self):
        script = r'''
function stub(init) {   // any element: what is set is kept, anything else is another stub
  const t = Object.assign(function () {}, init || {}, { listeners: {} });
  return new Proxy(t, {
    get(o, k) {
      if (k in o) return o[k];
      if (k === 'addEventListener') return (type, fn) => { (o.listeners[type] = o.listeners[type] || []).push(fn); };
      if (k === Symbol.toPrimitive) return () => '';
      if (typeof k === 'symbol') return undefined;
      return (o[k] = stub());
    },
    apply() { return stub(); },
    construct() { return stub(); },
  });
}
const els = {};
global.window = global;
global.location = { search: process.argv[2] };
global.document = { readyState: 'complete', documentElement: stub(), addEventListener() {}, createElement: () => stub(),
                    getElementById: (id) => els[id] || (els[id] = stub(id === 'backLink' ? { hidden: true, href: '../' } : {})) };
global.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
global.FileReader = class {};
process.on('unhandledRejection', () => {});
require(process.argv[1]);
const link = document.getElementById('backLink');
(link.listeners.click || []).forEach((f) => f());
console.log(JSON.stringify([link.hidden, link.href]));
process.exit(0);
'''
        def opened(search):
            out = subprocess.run(['node', '-e', script, str(self.PAGES / 'stickers' / 'stickers.js'), search],
                                 capture_output=True, text=True, encoding='utf-8', timeout=60, check=True).stdout
            return json.loads(out.strip().splitlines()[-1])
        self.assertEqual(opened(''), [True, '../'])                                     # its own page: no way back
        self.assertEqual(opened('?from=panel&back=memories&theme=dark'), [False, '../?view=memories&theme=dark'])
        self.assertEqual(opened('?from=panel&back=../../x'), [False, '../?view=overview&theme=light'])


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
