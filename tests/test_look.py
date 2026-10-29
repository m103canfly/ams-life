"""Her look (10-29, the owner chose "v2丙月白"): 月白 colours on clear glass, no BioCore wording on screen.

- her pictures: read only from <data dir>/ui/ (ui_look.py, page/look); nothing that is not a small picture,
  and the panel works without them (look.js keeps its drawn mark);
- no BioCore wording in what the pages show, the "about" line with the licence and the source in its place,
  and "update" no longer pointing at BioCore's repository;
- the look itself: no glow around words, an opaque way out without backdrop-filter or with less transparency,
  nothing pulled from the network, and no pictures of her in the repository.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import ui_look  # noqa: E402  (needs nothing of AstrBot; the plugin itself is tried in its own process below)

PAGES = ROOT / 'pages'
DASH = PAGES / 'dashboard'
PNG = b'\x89PNG\r\n\x1a\n' + b'\x00' * 40
JPEG = b'\xff\xd8\xff\xe0' + b'\x00' * 40
ABOUT = '小爱的身体和记忆用的是 ams-life（AGPL-3.0），基于 BioCore v1.2.99（Johnhmzm，AGPL-3.0）。'
SOURCE = 'https://github.com/m103canfly/ams-life'


def shown_text(path):
    """A page file without its comments (where the BioCore credit lines belong) and without the about line."""
    t = path.read_text('utf-8')
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    if path.suffix in ('.js', '.css'):
        t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    if path.suffix == '.js':
        t = re.sub(r'(?m)^\s*//.*$|(?<=[;{}(),\s])//[^\n"\']*$', '', t)
    return t.replace(ABOUT, '')


def page_files():
    for p in sorted(PAGES.rglob('*')):
        if p.is_file() and 'licenses' not in p.parts and p.name != 'brain.bundle.js' \
                and p.suffix in ('.html', '.js', '.css'):
            yield p


class Pictures(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ams-life-ui-'))
        self.ui = self.tmp / 'ui'
        self.ui.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_none_is_fine(self):
        shutil.rmtree(self.ui)
        self.assertEqual(ui_look.read_ui_images(self.tmp), {'avatar': '', 'art': ''})

    def test_pictures_become_data_urls(self):
        (self.ui / 'avatar.png').write_bytes(PNG)
        (self.ui / 'art.jpg').write_bytes(JPEG)
        got = ui_look.read_ui_images(self.tmp)
        self.assertTrue(got['avatar'].startswith('data:image/png;base64,'))
        self.assertTrue(got['art'].startswith('data:image/jpeg;base64,'))

    def test_not_a_picture_too_big_or_wrongly_named_is_left_out(self):
        (self.ui / 'avatar.png').write_bytes(b'<svg onload=alert(1)>')
        (self.ui / 'art.png').write_bytes(PNG + b'\x00' * ui_look.MAX_BYTES)
        (self.ui / 'other.png').write_bytes(PNG)
        self.assertEqual(ui_look.read_ui_images(self.tmp), {'avatar': '', 'art': ''})

    def test_kinds(self):
        self.assertEqual(ui_look.picture_kind(PNG[:16]), 'png')
        self.assertEqual(ui_look.picture_kind(b'RIFF\x00\x00\x00\x00WEBPVP8 '), 'webp')
        self.assertEqual(ui_look.picture_kind(b'GIF89a'), '')

    def test_the_route_is_read_only_and_reads_the_data_folder(self):
        # in its own process: the plugin needs harness.prepare (data folder, frozen clock), which must not
        # touch the other test modules' clock
        script = r'''
import asyncio, json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import harness
data = Path(sys.argv[2])
harness.prepare(data)
import main
ctx = harness.FakeContext()
plugin = main.BioCorePlugin(ctx, config={})
(data / 'ui').mkdir()
(data / 'ui' / 'avatar.png').write_bytes(bytes.fromhex(sys.argv[3]))
print(json.dumps({'routes': [r for r in ctx.web_routes if r.endswith('/page/look')], 'got': asyncio.run(plugin.page_look())}))
'''
        out = subprocess.run([sys.executable, '-c', script, str(HERE), str(self.tmp / 'data'), PNG.hex()],
                             capture_output=True, text=True, encoding='utf-8', timeout=120, check=True).stdout
        r = json.loads(out.strip().splitlines()[-1])
        self.assertEqual(r['routes'], ['/astrbot_plugin_ams_life/page/look'])
        self.assertRegex((ROOT / 'mixin_pages.py').read_text('utf-8'), r'page/look", self\.page_look, \["GET"\]')
        self.assertEqual(r['got']['status'], 'ok')
        self.assertTrue(r['got']['data']['avatar'].startswith('data:image/png;base64,'))
        self.assertEqual(r['got']['data']['art'], '')


@unittest.skipUnless(shutil.which('node'), 'needs Node.js')
class PicturesOnThePage(unittest.TestCase):
    """look.js takes only small data-URL pictures from page/look; anything else leaves the drawn mark."""

    def test_only_pictures(self):
        script = r'''
const fs = require('fs');
const props = {}, classes = new Set();
const root = { style: { setProperty: (k, v) => { props[k] = v; } }, classList: { add: (c) => classes.add(c) } };
global.window = {};
global.document = { readyState: 'complete', querySelector: () => null, documentElement: root };
eval(fs.readFileSync(process.argv[1], 'utf8'));
const use = window.BioLook.usePictures;
const png = 'data:image/png;base64,iVBORw0KGgo=';
const out = {
  ok: use({ status: 'ok', data: { avatar: png, art: 'data:image/webp;base64,UklGRg==' } }, root),
  bad: [use({ data: { avatar: 'javascript:alert(1)' } }, root), use({ data: { art: 'https://example.com/a.png' } }, root),
        use({ data: { avatar: 'data:image/svg+xml;base64,PHN2Zz4=' } }, root), use({ data: { avatar: png + '")' } }, root),
        use({ data: { avatar: 'data:image/png;base64,' + 'A'.repeat(7 * 1024 * 1024) } }, root), use(null, root), use('x', root)],
  props: Object.keys(props).sort(),
};
console.log(JSON.stringify(out));
'''
        out = json.loads(subprocess.run(['node', '-e', script, str(DASH / 'look.js')], capture_output=True, text=True,
                                        encoding='utf-8', timeout=60, check=True).stdout)
        self.assertEqual(out['ok'], ['has-avatar', 'has-art'])
        self.assertEqual(out['bad'], [[]] * 7)
        self.assertEqual(out['props'], ['--art', '--avatar'])


class Wording(unittest.TestCase):
    def test_exact_page_title(self):
        title = re.search(r'<title>(.*?)</title>', (DASH / 'index.html').read_text('utf-8'))
        self.assertIsNotNone(title)
        self.assertEqual(title.group(1), '小爱的内心世界')

    def test_no_biocore_on_screen(self):
        words = ('BioCore', 'BIOCORE', 'EMOTION CORE', '生物情绪核心', 'tendency layer')
        found = []
        for p in page_files():
            t = shown_text(p)
            found += ['%s: %s' % (p.relative_to(ROOT).as_posix(), w) for w in words if w in t]
        self.assertEqual(found, [])

    def test_about_line_is_there(self):
        for p in (DASH / 'index.html', PAGES / 'starmap' / 'index.html', DASH / 'brain' / 'index.html'):
            t = p.read_text('utf-8')
            self.assertIn(ABOUT, t, p)
            self.assertIn(SOURCE, t, p)
        self.assertIn('Galaxy View（MIT）', (PAGES / 'starmap' / 'index.html').read_text('utf-8'))

    def test_update_does_not_point_at_biocore(self):
        app = (DASH / 'app.js').read_text('utf-8')
        html = (DASH / 'index.html').read_text('utf-8')
        self.assertNotIn('astrbot_plugin_biocore', app + html)
        self.assertRegex(app, r'storeGet\(GITEE_KEY, ""\)')
        self.assertIn('ams-life 的更新由开发窗口装机', html)


class Look(unittest.TestCase):
    def test_no_glow_on_words(self):
        for p in (DASH / 'look.css',):
            self.assertNotIn('text-shadow', p.read_text('utf-8'))

    def test_ways_out(self):
        css = (DASH / 'look.css').read_text('utf-8')
        self.assertIn('@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px)))', css)
        self.assertIn('@media (prefers-reduced-transparency:reduce)', css)
        self.assertIn('@media (prefers-reduced-motion:reduce)', css)

    def test_loaded_after_the_old_styles_and_nothing_from_the_network(self):
        html = (DASH / 'index.html').read_text('utf-8')
        self.assertLess(html.index('./styles.css'), html.index('./look.css'))
        self.assertLess(html.index('./feedback.js'), html.index('./look.js'))
        self.assertNotRegex((DASH / 'look.css').read_text('utf-8'), r'https?://|@import|url\(')
        self.assertNotRegex((DASH / 'look.js').read_text('utf-8'), r'https?://|fetch\(|XMLHttpRequest')

    def test_no_pictures_of_her_in_the_repository(self):
        exts = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
        self.assertEqual([p for p in PAGES.rglob('*') if p.suffix.lower() in exts], [])
        for p in page_files():
            self.assertNotIn('data:image/png;base64', p.read_text('utf-8'), p)

    def test_star_map_copies_are_the_same(self):
        src = (ROOT / 'tools' / 'brain' / 'src' / 'page' / 'brain.css').read_bytes()
        for p in (PAGES / 'starmap' / 'brain.css', DASH / 'brain' / 'brain.css'):
            self.assertEqual(p.read_bytes(), src, p)


if __name__ == '__main__':
    unittest.main()
