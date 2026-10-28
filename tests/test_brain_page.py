"""The brain map page (pages/brain/): stays on this computer, only reads, sample is made up.

The page is built by tools/brain/build.mjs from tools/brain/src/ (our code plus
the vendored Galaxy View renderer, MIT) and three.js / d3-force-3d into one file,
brain.bundle.js. Static checks of the page files run everywhere. The sample-format
checks run the sample generator with Node.js when it is installed (skipped
otherwise); no browser, no network.
"""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'pages' / 'brain'
SRC = ROOT / 'tools' / 'brain' / 'src'
FILES = sorted(p for p in PAGE.iterdir() if p.is_file())
OURS = [SRC / 'brain.js', PAGE / 'index.html', PAGE / 'sample.js']

# What the graph may carry for one point: categories and ids, never content.
NODE_KEYS = {'id', 'kind', 'sub', 'label', 'cat', 'where', 'ts', 'w', 'vis', 'self'}
KINDS = {'window', 'person', 'memory', 'event', 'note'}
EDGE_KINDS = {'link', 'origin', 'about', 'impression'}
# The only URLs in the bundle are strings inside three.js that are never fetched:
# the XHTML namespace for createElementNS and a paper cited in a shader comment.
INERT_URLS = {'http://www.w3.org/1999/xhtml', 'https://jcgt.org/published/0007/04/01/'}


class StaysLocal(unittest.TestCase):
    def test_nothing_is_loaded_from_or_sent_to_the_network(self):
        for f in FILES + [SRC / 'brain.js']:
            text = f.read_text(encoding='utf-8')
            for bad in ('fetch(', 'XMLHttpRequest', 'WebSocket', 'sendBeacon', 'EventSource',
                        'importScripts', '@import', 'import('):
                self.assertFalse(bad in text, f'{f.name} contains {bad!r}')
            urls = set(re.findall(r'''https?://[^\s"'`)<>]+''', text))
            allowed = INERT_URLS if f.name == 'brain.bundle.js' else set()
            self.assertLessEqual(urls, allowed, f.name)

    def test_page_only_loads_its_own_files(self):
        html = (PAGE / 'index.html').read_text(encoding='utf-8')
        refs = re.findall(r'(?:src|href)="([^"]+)"', html)
        self.assertTrue(refs)
        for ref in refs:
            self.assertTrue(ref.startswith('./') and (PAGE / ref[2:]).is_file(), ref)

    def test_every_bundled_package_has_its_license(self):
        lic = PAGE / 'licenses'
        rows = re.findall(r'^\| ([^|]+?) \| [^|]+ \| ([^|]+?) \|$', (lic / 'README.md').read_text(encoding='utf-8'), re.M)
        rows = [(n, l) for n, l in rows if n != 'Package' and not n.startswith('-')]
        names = {name for name, _ in rows}
        self.assertIn('galaxy-view', names)
        self.assertIn('three', names)
        self.assertIn('d3-force-3d', names)
        for name, license_ in rows:
            self.assertTrue((lic / (name.replace('/', '__') + '.LICENSE.txt')).is_file(), name)
            self.assertIn(license_.strip(), {'MIT', 'ISC', 'BSD-3-Clause', 'Apache-2.0'}, name)
        self.assertIn('Copyright (c) 2026 Rick', (SRC / 'galaxy' / 'LICENSE').read_text(encoding='utf-8'))


class ReadOnly(unittest.TestCase):
    def test_page_never_writes(self):
        for f in FILES + [SRC / 'brain.js']:
            text = f.read_text(encoding='utf-8')
            for bad in ('apiPost', 'apiPut', 'apiDelete', 'apiPatch'):
                self.assertFalse(bad in text, f'{f.name} contains {bad!r}')

    def test_reads_only_the_brain_routes(self):
        text = (SRC / 'brain.js').read_text(encoding='utf-8')
        routes = set(re.findall(r"apiGet\('([^']+)'", text))
        self.assertEqual(routes, {'page/brain', 'page/brain/node', 'page/brain/search'})

    def test_bundle_is_built_from_this_source(self):
        bundle = (PAGE / 'brain.bundle.js').read_text(encoding='utf-8')
        self.assertTrue(bundle.startswith('/* ams-life brain map (AGPL-3.0)'))
        for marker in ('page/brain/node', '没说 · ', '想被看见'):   # strings only our source has
            self.assertIn(marker, bundle)


class LinesOnlyWhenRecalled(unittest.TestCase):
    """Stars stand alone; lines are drawn only when something is called up."""

    def test_show_all_switch_is_off_by_default(self):
        html = (PAGE / 'index.html').read_text(encoding='utf-8')
        box = re.search(r'<input[^>]*id="allLines"[^>]*>', html).group(0)
        self.assertNotIn('checked', box)
        self.assertNotIn('edgeBoxes', html)
        self.assertIn('export const SHOW_ALL_DEFAULT = false;', (SRC / 'lines.js').read_text(encoding='utf-8'))

    def test_page_hides_the_base_layer_and_idle_sparks(self):
        text = (SRC / 'brain.js').read_text(encoding='utf-8')
        self.assertIn('renderer.linkSegments.visible = baseLinesVisible(showAll)', text)
        self.assertIn('if (!showAll || !motion', text)   # no lights running along hidden lines


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class LineRules(unittest.TestCase):
    """tools/brain/src/lines.js, run with Node."""

    @classmethod
    def setUpClass(cls):
        script = r"""
const L = await import(process.argv[1]);
// stars 0..5; 5 is held back. links: 0-1 link, 1-2 link, 2-3 link, 3-5 link, 0-4 about
const links = [{source:0,target:1,kind:'link'},{source:1,target:2,kind:'link'},{source:2,target:3,kind:'link'},
  {source:3,target:5,kind:'link'},{source:0,target:4,kind:'about'}];
const map = L.lineMap(links);
const steps = L.turnSteps(map, [[0,1],[1,2],[2,3],[3,5]], [5]);
const end = 4 * L.TURN.step + L.TURN.hold;
const out = {
  idle: L.baseLinesVisible(L.SHOW_ALL_DEFAULT), on: L.baseLinesVisible(true),
  steps: steps.map((s) => s.line),
  still: L.turnFrame(steps, 4, 0, false),
  early: L.turnFrame(steps, 4, 0.6 * L.TURN.step, true),
  mid: L.turnFrame(steps, 4, end, true),
  fading: L.turnFrame(steps, 4, end + L.TURN.fade / 2, true),
  gone: L.turnFrame(steps, 4, end + L.TURN.fade + 1, true),
  over: L.turnFrame(steps, 4, L.turnLength(4), true),
  openMemory: L.openedLines(links, 0), openPerson: L.openedLines(links, 4),
};
process.stdout.write(JSON.stringify(out));
"""
        out = subprocess.run(['node', '--input-type=module', '-e', script, (SRC / 'lines.js').as_uri()],
                             capture_output=True, text=True, encoding='utf-8', timeout=60, check=True).stdout
        cls.r = json.loads(out)

    def test_no_lines_unless_switched_on(self):
        self.assertFalse(self.r['idle'])
        self.assertTrue(self.r['on'])

    def test_a_turn_draws_only_its_own_path_and_never_to_the_held_star(self):
        self.assertEqual(self.r['steps'], [0, 1, 2])          # 3-5 leads to the held star: no line
        self.assertEqual(self.r['still']['lines'], [0, 1, 2])  # without motion: all of them, steady
        self.assertEqual(self.r['still']['alpha'], 1)

    def test_lines_appear_as_she_goes_then_fade(self):
        self.assertEqual(self.r['early']['lines'], [0])
        self.assertEqual(self.r['early']['lit'], 1)
        self.assertEqual(self.r['mid']['lines'], [0, 1, 2])
        self.assertEqual(self.r['mid']['alpha'], 1)
        self.assertTrue(0 < self.r['fading']['alpha'] < 1)
        self.assertEqual(self.r['gone']['lines'], [])
        self.assertEqual(self.r['gone']['lit'], 4)            # the stars stay lit, only the lines go
        self.assertTrue(self.r['over']['done'])

    def test_an_opened_star_calls_up_its_associations(self):
        self.assertEqual(self.r['openMemory'], [0])            # its association, not the about-line
        self.assertEqual(self.r['openPerson'], [4])            # no associations: its own line


class Ball(unittest.TestCase):
    """The stars make a ball you turn and flick by hand (owner, 10-28)."""

    def test_layout_is_a_ball_not_a_disc(self):
        text = (SRC / 'brain.js').read_text(encoding='utf-8')
        physics = re.search(r'const PHYSICS = \{([^}]*)\}', text).group(1)
        for key in ('flatten', 'coreGravity', 'spiral'):
            self.assertRegex(physics, key + r': 0\b')
        self.assertRegex(physics, r'ballStrength: 0\.[1-9]')
        self.assertIn('ball: ballRadius(nodes.length)', text)
        for f in ('forceWorker.ts', 'MainThreadForceLayout.ts'):   # both layout engines use the ball force
            self.assertIn("forceBall(", (SRC / 'galaxy' / 'layout' / f).read_text(encoding='utf-8'))

    def test_turned_by_hand_with_touch(self):
        globe = (SRC / 'globe.js').read_text(encoding='utf-8')
        for word in ('pointerdown', 'pointermove', 'pointerup', 'pinchDistance', 'spinSpeed', 'autoSpeed('):
            self.assertIn(word, globe)
        self.assertIn('touch-action:none', (PAGE / 'brain.css').read_text(encoding='utf-8'))
        text = (SRC / 'brain.js').read_text(encoding='utf-8')
        self.assertIn('new GlobeCamera(', text)
        self.assertNotIn('CameraDirector', text)


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class BallRules(unittest.TestCase):
    """tools/brain/src/ball.js, run with Node."""

    @classmethod
    def setUpClass(cls):
        script = r"""
const B = await import(process.argv[1]);
const R = B.ballRadius(800);
const out = { R, R8000: B.ballRadius(8000) };
const nodes = [{ x: 2 * R, y: 0, z: 0, vx: 0, vy: 0, vz: 0 }, { x: R / 2, y: 0, z: 0, vx: 0, vy: 0, vz: 0 }];
const f = B.forceBall(R, 0.6); f.initialize(nodes); f(1);
out.outside = nodes[0].vx; out.inside = nodes[1].vx;
out.sides = [B.sideTarget(-1, R), B.sideTarget(0, R), B.sideTarget(1, R)];
out.dragRight = B.dragAngles(100, 0, 800); out.dragDown = B.dragAngles(0, 100, 800);
let s = 2; for (let k = 0; k < 600 && s > 0; k++) s = B.coast(s, 1 / 60); out.coastAfter10s = s;
out.coastHalf = B.coast(2, 0.2);
out.autoAtTouch = B.autoSpeed(0, true); out.autoLater = B.autoSpeed(B.SPIN.resumeMs + B.SPIN.rampMs, true);
out.autoOff = B.autoSpeed(1e9, false);
process.stdout.write(JSON.stringify(out));
"""
        out = subprocess.run(['node', '--input-type=module', '-e', script, (SRC / 'ball.js').as_uri()],
                             capture_output=True, text=True, encoding='utf-8', timeout=60, check=True).stdout
        cls.r = json.loads(out)

    def test_ball_grows_slowly_with_more_stars(self):
        self.assertGreater(self.r['R8000'], self.r['R'])
        self.assertLess(self.r['R8000'], self.r['R'] * 2.2)    # cube root: 10x stars, about 2x radius

    def test_outside_pulled_in_inside_left_alone(self):
        self.assertLess(self.r['outside'], 0)
        self.assertEqual(self.r['inside'], 0)

    def test_private_chats_lean_to_the_other_side(self):
        g, p, priv = self.r['sides']
        self.assertLess(g, 0)
        self.assertEqual(p, 0)
        self.assertGreater(priv, 0)

    def test_drag_turns_and_a_flick_coasts_to_a_stop(self):
        self.assertLess(self.r['dragRight']['yaw'], 0)
        self.assertEqual(self.r['dragRight']['pitch'], 0)
        self.assertLess(self.r['dragDown']['pitch'], 0)
        self.assertTrue(0 < self.r['coastHalf'] < 2)            # still turning, slower
        self.assertEqual(self.r['coastAfter10s'], 0)            # and stops

    def test_turns_by_itself_only_when_left_alone(self):
        self.assertEqual(self.r['autoAtTouch'], 0)
        self.assertGreater(self.r['autoLater'], 0)
        self.assertEqual(self.r['autoOff'], 0)


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class SampleFormat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script = ('globalThis.window = globalThis; require(process.argv[1]);'
                  'process.stdout.write(JSON.stringify(BrainSample.make({n: Number(process.argv[2])})));')
        cls.made = {}
        for n in (300, 900):
            out = subprocess.run(['node', '-e', script, str(PAGE / 'sample.js'), str(n)],
                                 capture_output=True, text=True, encoding='utf-8', timeout=60, check=True).stdout
            cls.made[n] = json.loads(out)

    def test_graph_carries_no_content(self):
        for made in self.made.values():
            g = made['graph']
            self.assertEqual(g['schema'], 'ams-life.brain/1')
            self.assertTrue(g['sample'])
            for n in g['nodes']:
                self.assertLessEqual(set(n), NODE_KEYS, n)
                self.assertIn(n['kind'], KINDS)
                self.assertLessEqual(len(n['label']), 6, n)
                no_time = {k: v for k, v in n.items() if k != 'ts'}
                self.assertNotRegex(json.dumps(no_time, ensure_ascii=False), r'\d{5,}')   # no QQ-like numbers

    def test_edges_and_turns_point_at_points(self):
        for made in self.made.values():
            g = made['graph']
            ids = {n['id'] for n in g['nodes']}
            self.assertEqual(len(ids), len(g['nodes']))
            for e in g['edges']:
                self.assertIn(e['kind'], EDGE_KINDS)
                self.assertIn(e['s'], ids)
                self.assertIn(e['t'], ids)
            self.assertTrue(g['turns'])
            for t in g['turns']:
                self.assertIn(t['where'], ids)
                for i in t['recalled'] + t['held']:
                    self.assertIn(i, ids)
                self.assertFalse(set(t['recalled']) & set(t['held']))
                # ids only: a turn never carries words
                self.assertLessEqual(set(t), {'id', 'ts', 'where', 'recalled', 'held', 'path', 'body'})

    def test_held_back_is_private_and_from_elsewhere(self):
        g = self.made[900]['graph']
        by = {n['id']: n for n in g['nodes']}
        held = [(t, i) for t in g['turns'] for i in t['held']]
        self.assertTrue(held)
        for t, i in held:
            self.assertEqual(by[i]['vis'], 'private')
            self.assertNotEqual(by[i]['where'], t['where'])

    def test_details_are_obviously_made_up(self):
        for made in self.made.values():
            for d in made['details'].values():
                if 'qq' in d:
                    self.assertTrue(d['qq'].startswith('示例-'), d['qq'])
                self.assertNotRegex(json.dumps(d, ensure_ascii=False), r'\d{5,}')


if __name__ == '__main__':
    unittest.main()
