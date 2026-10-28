"""The brain map page (pages/brain/): stays on this computer, only reads, sample is made up.

Static checks of the page files run everywhere. The sample-format checks run the
sample generator with Node.js when it is installed (skipped otherwise); no browser,
no network.
"""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'pages' / 'brain'
FILES = sorted(p for p in PAGE.iterdir() if p.is_file())

# What the graph may carry for one point: categories and ids, never content.
NODE_KEYS = {'id', 'kind', 'sub', 'label', 'cat', 'where', 'ts', 'w', 'vis', 'self'}
KINDS = {'window', 'person', 'memory', 'event', 'note'}
EDGE_KINDS = {'link', 'origin', 'about', 'impression'}


class StaysLocal(unittest.TestCase):
    def test_nothing_is_loaded_from_or_sent_to_the_network(self):
        for f in FILES:
            text = f.read_text(encoding='utf-8')
            for bad in ('http://', 'https://', '//cdn', 'fetch(', 'XMLHttpRequest', 'WebSocket',
                        'sendBeacon', 'EventSource', '@import', 'import('):
                self.assertFalse(bad in text, f'{f.name} contains {bad!r}')

    def test_page_only_loads_its_own_files(self):
        html = (PAGE / 'index.html').read_text(encoding='utf-8')
        refs = re.findall(r'(?:src|href)="([^"]+)"', html)
        self.assertTrue(refs)
        for ref in refs:
            self.assertTrue(ref.startswith('./') and (PAGE / ref[2:]).is_file(), ref)


class ReadOnly(unittest.TestCase):
    def test_page_never_writes(self):
        for f in FILES:
            text = f.read_text(encoding='utf-8')
            for bad in ('apiPost', 'apiPut', 'apiDelete', 'apiPatch', 'method:'):
                self.assertFalse(bad in text, f'{f.name} contains {bad!r}')

    def test_reads_only_the_brain_routes(self):
        text = (PAGE / 'brain.js').read_text(encoding='utf-8')
        routes = set(re.findall(r'apiGet\("([^"]+)"', text))
        self.assertEqual(routes, {'page/brain', 'page/brain/node', 'page/brain/search'})


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
