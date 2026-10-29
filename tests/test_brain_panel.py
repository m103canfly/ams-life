"""The brain map inside the panel ("她的脑子", pages/dashboard/brain_frame.js, tools/brain/src/embed.js).

Static checks run everywhere. The request rules and the panel's wiring run with Node.js
against a small stand-in page (skipped without Node). The whole thing runs in a headless
Edge or Chrome inside tests/panel_shell/ -- a stand-in for AstrBot's web panel: sandboxed
frame, its headers, a bridge answering with invented data -- when one is installed
(skipped otherwise). No network: everything listens on 127.0.0.1.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASH = ROOT / 'pages' / 'dashboard'
FRAME_JS = DASH / 'brain_frame.js'
EMBED_JS = ROOT / 'tools' / 'brain' / 'src' / 'embed.js'
SHELL = ROOT / 'tests' / 'panel_shell'


def browser():
    for exe in (os.environ.get('AMS_BROWSER', ''),
                r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                shutil.which('microsoft-edge') or '', shutil.which('google-chrome') or '', shutil.which('chromium') or ''):
        if exe and Path(exe).is_file():
            return exe
    return ''


def node(script, *args):
    out = subprocess.run(['node', '-e', script, *map(str, args)], capture_output=True, text=True, encoding='utf-8',
                         timeout=60, check=True).stdout
    return json.loads(out)


class InThePanel(unittest.TestCase):
    def test_a_view_after_the_overview(self):
        html = (DASH / 'index.html').read_text(encoding='utf-8')
        views = re.findall(r'class="nav-item[^"]*" data-view="([a-z]+)"', html)
        self.assertEqual(views[:2], ['overview', 'brain'])
        self.assertIn('<span class="ni-icon">✦</span><span>她的脑子</span>', html)
        section = re.search(r'<section class="view" id="view-brain">(.*?)</section>', html, re.S).group(1)
        self.assertIn('id="brainBox"', section)
        self.assertIn('id="brainFill"', section)
        self.assertNotIn('<iframe', html)            # no frame until the view is first opened
        self.assertIn('<script src="./brain/panel-page.js"></script><script src="./brain_frame.js"></script>', html)

    def test_the_map_comes_from_the_panels_own_folder(self):
        text = FRAME_JS.read_text(encoding='utf-8')
        self.assertIn('frame.srcdoc = String(window.BioBrainPage', text)
        self.assertNotRegex(text, r'https?://')
        page = (DASH / 'brain' / 'panel-page.js').read_text(encoding='utf-8')
        html = json.loads(page.split('window.BioBrainPage = ', 1)[1].rstrip().rstrip(';'))
        self.assertIn('<base href="brain/" /><meta name="ams-brain-embed" content="panel" />', html)
        refs = re.findall(r'(?:src|href)="([^"]+)"', html)
        self.assertEqual(sorted(refs), ['./brain.bundle.js', './brain.css', './sample.js', 'brain/'])

    def test_no_way_to_write(self):
        for f in (FRAME_JS, EMBED_JS, ROOT / 'tools' / 'brain' / 'src' / 'brain.js'):
            text = f.read_text(encoding='utf-8')
            for bad in ('apiPost', 'apiPut', 'apiDelete', 'apiPatch', 'upload(', 'download('):
                self.assertNotIn(bad, text, f.name)

    def test_full_screen_or_fill(self):
        text = FRAME_JS.read_text(encoding='utf-8')
        self.assertIn('box.requestFullscreen()', text)
        self.assertIn('frame.setAttribute("allowfullscreen", "")', text)
        self.assertIn('realFull ? "全屏" : "铺满"', text)
        css = (DASH / 'styles.css').read_text(encoding='utf-8')
        self.assertIn('body.brain-view{overflow:hidden}', css)
        self.assertIn('body.brain-filled #view-brain{position:fixed;inset:0', css)

    def test_wheel_and_drag_stay_on_the_map(self):
        css = (ROOT / 'pages' / 'starmap' / 'brain.css').read_text(encoding='utf-8')
        self.assertIn('overscroll-behavior:none', css)
        self.assertIn('#galaxy canvas{display:block;width:100%;height:100%;outline:none;touch-action:none}', css)
        globe = (ROOT / 'tools' / 'brain' / 'src' / 'globe.js').read_text(encoding='utf-8')
        self.assertRegex(globe, r"addEventListener\('wheel', \(e\) => \{\s*e\.preventDefault\(\);")


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class RequestRules(unittest.TestCase):
    """What the panel passes on of the map's requests (brain_frame.js cleanRequest)."""

    @classmethod
    def setUpClass(cls):
        script = r"""
const F = require(process.argv[1]);
const c = (m) => F.cleanRequest(m);
process.stdout.write(JSON.stringify({
  ok: c({ id: 3, route: 'page/brain/node', query: { id: 'm:1', reveal: 'qq', extra: 'x', token: 't', q: null } }),
  routes: ['page/status', 'page/memory/delete', 'page/brain/../status', ''].map((r) => c({ id: 1, route: r })),
  long: c({ id: 2, route: 'page/brain/search', query: { q: 'x'.repeat(500) } }).query.q.length,
  num: c({ id: 4, route: 'page/brain', query: { part: 2 } }).query,
  noId: [c({ route: 'page/brain' }), c({ id: 0, route: 'page/brain' }), c({ id: 'a', route: 'page/brain' })],
  consts: [F.ROUTES, F.KEYS, F.MAX_VALUE, F.MAX_WAITING],
}));
"""
        cls.r = node(script, FRAME_JS)

    def test_only_the_three_routes_and_five_keys(self):
        self.assertEqual(self.r['ok'], {'id': 3, 'route': 'page/brain/node', 'query': {'id': 'm:1', 'reveal': 'qq'}})
        self.assertEqual([x['error'] for x in self.r['routes']], ['只能读她的脑子'] * 4)
        self.assertEqual(self.r['consts'], [['page/brain', 'page/brain/node', 'page/brain/search'],
                                            ['part', 'snap', 'id', 'reveal', 'q'], 200, 8])

    def test_values_are_short_strings(self):
        self.assertEqual(self.r['long'], 200)
        self.assertEqual(self.r['num'], {'part': '2'})

    def test_no_usable_id_no_answer(self):
        self.assertEqual(self.r['noId'], [None, None, None])


# A stand-in page for brain_frame.js's browser part: the elements it looks up, a window
# that keeps its listeners, frames whose postMessage is recorded.
FAKE_PAGE = r"""
const posted = [], listeners = {}, docListeners = {}, bridgeCalls = [];
const el = (id) => ({ id, textContent: '', title: '', children: [], listeners: {},
  addEventListener(k, f) { this.listeners[k] = f; }, appendChild(c) { this.children.push(c); },
  requestFullscreen: () => Promise.reject(new Error('not allowed')), setAttribute(k, v) { this[k] = v; } });
const els = { brainBox: el('brainBox'), brainFill: el('brainFill') };
const classes = new Set();
global.MutationObserver = class { constructor(f) { this.f = f; } observe() {} };
global.window = { addEventListener: (k, f) => { listeners[k] = f; }, BioBrainPage: '<p>the page</p>' };
global.document = {
  fullscreenEnabled: false, fullscreenElement: null,
  getElementById: (id) => els[id],
  createElement: () => { const f = el('frame'); f.contentWindow = { postMessage: (m, o) => posted.push([m, o]) }; return f; },
  addEventListener: (k, f) => { docListeners[k] = f; },
  documentElement: { dataset: { theme: 'dark' } },
  body: { classList: { toggle: (c, on) => (on ? classes.add(c) : classes.delete(c)), add: (c) => classes.add(c),
                       contains: (c) => classes.has(c) } },
};
const F = require(process.argv[1]);
let answerNext = null;
const bridge = { apiGet: (route, query) => { bridgeCalls.push([route, query]); return new Promise((ok) => { answerNext = ok; }); },
                 apiPost: () => { bridgeCalls.push(['POST']); return Promise.resolve(); } };
const panel = F.attach({ bridge: () => bridge, dark: () => true });
const box = els.brainBox, btn = els.brainFill;
const from = (src, m) => listeners.message({ source: src, data: Object.assign({ channel: 'ams-brain' }, m) });
const tick = () => new Promise((r) => setTimeout(r, 0));
"""


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class PanelWiring(unittest.TestCase):
    """brain_frame.js in the panel: loaded on the first visit, stopped and started, reads passed on."""

    @classmethod
    def setUpClass(cls):
        script = FAKE_PAGE + r"""
(async () => {
const out = {};
out.label = btn.textContent;
panel.onView('overview');
out.framesBefore = box.children.length;
panel.onView('brain');
const frame = box.children[0];
out.framesAfter = box.children.length;
out.frame = { srcdoc: frame.srcdoc, allowfullscreen: frame.allowfullscreen, bodyView: classes.has('brain-view') };
const win = frame.contentWindow;
from(win, { kind: 'hello' });
out.hello = posted.splice(0).map(([m, o]) => [m.kind, m.isDark, o]);
// another window saying the same is not listened to
from({ postMessage() {} }, { kind: 'get', id: 1, route: 'page/brain', query: {} });
out.strangerCalls = bridgeCalls.length;
// a read: passed on cleaned, answered to the frame only
from(win, { kind: 'get', id: 7, route: 'page/brain/node', query: { id: 'p:1', reveal: 'qq', secret: 'x' } });
await tick();
out.passed = bridgeCalls.splice(0);
answerNext({ qq: '示例-1' });
await tick(); await tick();
out.answer = posted.splice(0).map(([m, o]) => [m.kind, m.id, m.ok, m.data, o]);
from(win, { kind: 'get', id: 8, route: 'page/status', query: {} });
await tick();
out.refused = posted.splice(0).map(([m]) => [m.id, m.ok, m.error]);
// at most 8 waiting
for (let i = 0; i < 10; i++) from(win, { kind: 'get', id: 100 + i, route: 'page/brain', query: { part: i } });
await tick(); await tick();
out.waitingCalls = bridgeCalls.splice(0).length;
out.tooMany = posted.splice(0).filter(([m]) => !m.ok).map(([m]) => [m.id, m.error]);
// leaving the view stops it, coming back starts it, the frame is not made again
panel.onView('persona');
panel.onView('brain');
out.runs = posted.splice(0).filter(([m]) => m.kind === 'run').map(([m]) => m.on);
out.framesAgain = box.children.length;
// fill (no real full screen here), then exit-fill from the map
btn.listeners.click();
out.filled = [classes.has('brain-filled'), btn.textContent];
from(win, { kind: 'exit-fill' });
out.exited = [classes.has('brain-filled'), btn.textContent];
btn.listeners.click();
docListeners.keydown({ key: 'Escape' });
out.escaped = classes.has('brain-filled');
out.posts = bridgeCalls.filter((c) => c[0] === 'POST').length;
process.stdout.write(JSON.stringify(out));
})();
"""
        cls.r = node(script, FRAME_JS)

    def test_loaded_on_the_first_visit_only(self):
        r = self.r
        self.assertEqual((r['framesBefore'], r['framesAfter'], r['framesAgain']), (0, 1, 1))
        self.assertEqual(r['frame'], {'srcdoc': '<p>the page</p>', 'allowfullscreen': '', 'bodyView': True})

    def test_stops_away_and_goes_on_back(self):
        self.assertEqual(self.r['runs'], [False, True])

    def test_reads_passed_on_read_only(self):
        r = self.r
        self.assertEqual(r['hello'], [['hello', True, '*']])
        self.assertEqual(r['strangerCalls'], 0)
        self.assertEqual(r['passed'], [['page/brain/node', {'id': 'p:1', 'reveal': 'qq'}]])
        self.assertEqual(r['answer'], [['answer', 7, True, {'qq': '示例-1'}, '*']])
        self.assertEqual(r['refused'], [[8, False, '只能读她的脑子']])
        self.assertEqual(r['waitingCalls'], 8)
        self.assertEqual(r['tooMany'], [[108, '同时请求太多，稍后再试'], [109, '同时请求太多，稍后再试']])
        self.assertEqual(r['posts'], 0)

    def test_fill_and_its_ways_out(self):
        r = self.r
        self.assertEqual(r['label'], '铺满')             # no real full screen in AstrBot: says so
        self.assertEqual(r['filled'], [True, '退出铺满'])
        self.assertEqual(r['exited'], [False, '铺满'])     # Esc inside the map
        self.assertFalse(r['escaped'])                     # Esc in the panel


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class MapSide(unittest.TestCase):
    """tools/brain/src/embed.js: the map asks only its parent, and stops while not shown."""

    @classmethod
    def setUpClass(cls):
        script = r"""
(async () => {
const E = await import(process.argv[1]);
const out = {};
const flips = [];
const gate = E.runGate((on) => flips.push(on));
gate.set('panel', false); gate.set('page', false); gate.set('panel', true); gate.set('page', true);
out.flips = flips;
out.running = gate.running;
const sent = [], listeners = {};
const parent = { postMessage: (m, o) => sent.push([m, o]) };
const win = { parent, addEventListener: (k, f) => { listeners[k] = f; } };
const runs = [];
const b = E.panelBridge(win, { run: (on) => runs.push(on) });
const ready = b.ready();
listeners.message({ source: { other: 1 }, data: { channel: 'ams-brain', kind: 'hello', isDark: true } });   // not its parent
listeners.message({ source: parent, data: { channel: 'ams-brain', kind: 'hello', isDark: true } });
out.ready = await ready;
const got = b.apiGet('page/brain', { part: '1' });
const id = sent[sent.length - 1][0].id;
listeners.message({ source: { other: 1 }, data: { channel: 'ams-brain', kind: 'answer', id, ok: true, data: 'wrong' } });
listeners.message({ source: parent, data: { channel: 'ams-brain', kind: 'answer', id, ok: true, data: 'right' } });
out.got = await got;
listeners.message({ source: parent, data: { channel: 'ams-brain', kind: 'run', on: false } });
out.runs = runs;
b.exitFill();
out.sent = sent.map(([m, o]) => [m.kind, m.route || '', o]);
out.inPanel = [E.inPanel({ querySelector: () => ({}) }), E.inPanel({ querySelector: () => null })];
process.stdout.write(JSON.stringify(out));
process.exit(0);
})();
"""
        cls.r = node(script, EMBED_JS.as_uri())

    def test_runs_only_while_shown_and_visible(self):
        self.assertEqual(self.r['flips'], [False, True])
        self.assertTrue(self.r['running'])

    def test_only_its_parent_is_listened_to_and_written_to(self):
        r = self.r
        self.assertEqual(r['ready'], {'isDark': True})
        self.assertEqual(r['got'], 'right')
        self.assertEqual(r['runs'], [False])
        self.assertEqual(r['sent'], [['hello', '', '*'], ['get', 'page/brain', '*'], ['exit-fill', '', '*']])
        self.assertEqual(r['inPanel'], [True, False])


@unittest.skipUnless(shutil.which('node') and browser(), 'Node.js or a Chromium browser (Edge / Chrome) not installed')
class InTheShell(unittest.TestCase):
    """The panel in a stand-in for AstrBot's web panel (tests/panel_shell/), in a headless browser."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        server = subprocess.Popen([sys.executable, str(SHELL / 'serve.py'), '0'], stdout=subprocess.PIPE, text=True)
        try:
            url = server.stdout.readline().strip()
            proc = subprocess.run(['node', str(SHELL / 'drive.mjs'), url, browser(), str(Path(cls.tmp.name) / 'profile')],
                                  capture_output=True, text=True, encoding='utf-8', timeout=240)
            cls.r = json.loads(proc.stdout.strip().splitlines()[-1])
        finally:
            server.terminate()
            server.wait(timeout=10)
            server.stdout.close()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.tmp.cleanup()
        except OSError:
            pass   # the browser may still hold its profile for a moment

    def test_ran_through(self):
        self.assertNotIn('failed', self.r, self.r.get('failed'))
        self.assertEqual(self.r['errors'], [])

    def test_loaded_on_the_first_visit_with_live_data(self):
        s = self.r['steps']
        self.assertEqual(s['before']['frames'], 0)
        self.assertEqual(s['before']['nav'][:2], ['overview', 'brain'])
        self.assertEqual(s['before']['fillLabel'], '铺满')
        self.assertTrue(s['opened']['running'])
        self.assertEqual(s['opened']['badge'], '')          # not the sample: the panel passed the reads on
        self.assertFalse(s['opened']['agentBridge'])        # AstrBot's bridge is not in the map's frame
        self.assertEqual(s['panelScroll'][0], s['panelScroll'][1])   # the panel itself does not scroll

    def test_qq_only_on_the_second_click(self):
        p = self.r['steps']['person']
        self.assertFalse(p['qqShownBefore'])
        self.assertTrue(p['button'])
        self.assertRegex(p['qqAfter'], r'^示例-\d+$')

    def test_fill_then_esc_inside_the_map(self):
        s = self.r['steps']
        self.assertEqual((s['filled']['filled'], s['filled']['label']), (True, '退出铺满'))
        self.assertGreater(s['filled']['widthAfter'], s['filled']['widthBefore'])   # the map's canvas follows
        self.assertEqual((s['escaped']['filled'], s['escaped']['label']), (False, '铺满'))
        self.assertEqual(s['escaped']['width'], s['filled']['widthBefore'])

    def test_stops_away_goes_on_back(self):
        s = self.r['steps']
        self.assertEqual(s['away'], {'running': False, 'framesWhileAway': 0})
        self.assertTrue(s['back']['running'])
        self.assertGreater(s['back']['framesAfter'], 0)
        self.assertEqual(s['back']['framesInPanel'], 1)

    def test_only_reads_of_the_brain_and_the_panel_reached_astrbot(self):
        host = self.r['host']
        self.assertEqual(host['posts'], [])
        self.assertEqual(host['other'], [])
        self.assertLessEqual({g['endpoint'] for g in host['gets']},
                             {'page/status', 'page/brain', 'page/brain/node', 'page/brain/search'})


if __name__ == '__main__':
    unittest.main()
