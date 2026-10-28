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
