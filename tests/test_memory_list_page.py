""""她记住了什么" in the panel (pages/dashboard/memories.js) and memory_list.py's paging rules.

The plugin side (page/memories on the brain map's snapshot) is in test_brain_data.Memories.
Here: the panel's markup, the page script with Node.js against a stand-in page (skipped
without Node), and the list's paging and filters on made-up rows. No browser, no network.
"""
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import memory_list  # noqa: E402

DASH = ROOT / 'pages' / 'dashboard'
JS = DASH / 'memories.js'


class InThePanel(unittest.TestCase):
    def test_a_view_after_her_brain(self):
        html = (DASH / 'index.html').read_text(encoding='utf-8')
        views = re.findall(r'class="nav-item[^"]*" data-view="([a-z]+)"', html)
        self.assertEqual(views[:3], ['overview', 'brain', 'memories'])
        section = re.search(r'<section class="view" id="view-memories">(.*?)</section>', html, re.S).group(1)
        for el in ('memKind', 'memPlace', 'memVis', 'memFrom', 'memTo', 'memQ', 'memGo', 'memList', 'memMore', 'memBadge'):
            self.assertIn('id="%s"' % el, section, el)
        self.assertIn('<script src="./brain_frame.js"></script><script src="./memories.js"></script>', html)
        app = (DASH / 'app.js').read_text(encoding='utf-8')
        self.assertIn('if(memoryList) memoryList.onView(name);', app)

    def test_reads_and_one_confirmed_delete_only(self):
        text = JS.read_text(encoding='utf-8')
        self.assertNotRegex(text, r'https?://')
        self.assertEqual(text.count('apiPost('), 1)                      # the delete, nothing else
        self.assertIn('const DELETE = "page/memory/delete/default/";', text)
        self.assertIn('b.apiPost(DELETE + encodeURIComponent(t.dataset.delete), {})', text)
        branch = text[text.index('t.dataset.delete'):]
        self.assertLess(branch.index('window.confirm('), branch.index('apiPost('))
        for bad in ('apiPut', 'apiDelete', 'apiPatch', 'upload(', 'download(', 'fetch(', 'XMLHttpRequest'):
            self.assertNotIn(bad, text)
        pages = (ROOT / 'mixin_pages.py').read_text(encoding='utf-8')
        self.assertIn('"/astrbot_plugin_ams_life/page/memory/delete/<path:session>/<entry_id>"', pages)


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class PageScript(unittest.TestCase):
    """memories.js with Node: the query, a row, the sample, and the view with a stand-in page."""

    @classmethod
    def setUpClass(cls):
        script = r"""
const els = {};
const el = (id) => (els[id] = els[id] || { id, value: '', innerHTML: '', textContent: '', hidden: false, disabled: false,
  listeners: {}, addEventListener(k, f) { this.listeners[k] = f; },
  insertAdjacentHTML(where, html) { this.innerHTML += html; } });
['memList', 'memKind', 'memPlace', 'memVis', 'memFrom', 'memTo', 'memQ', 'memGo', 'memMore', 'memState', 'memBadge'].forEach(el);
let confirmAnswer = false;
global.window = { confirm: () => confirmAnswer };
global.document = { getElementById: (id) => els[id] };
const M = require(process.argv[1]);
const calls = [];
let answer = null;
const bridge = { apiGet: async (route, q) => { calls.push(['GET', route, q]); return answer(route, q); },
                 apiPost: async (route, body) => { calls.push(['POST', route, body]); return { id: 'x', deleted: true }; } };
let withBridge = false;
const out = {};
out.query = M.query({ kind: 'memory', place: '', vis: ' private ', q: 'x'.repeat(80), from: null }, 'tok');
const row = { id: 'm:1', kind: 'memory', kind_name: '记忆', where: '群1', date: '2026-10-29 10:00', may: '公开', who: ['<b>'],
              text: '<script>1</script>\n第二行', has_number: true, entry: 'mem1' };
out.row = M.rowHtml(row);
out.rowEvent = M.rowHtml(Object.assign({}, row, { kind: 'event', has_number: false, entry: '' }));
out.sample = M.sample();
out.badge = M.SAMPLE_BADGE;
(async () => {
  const tick = () => new Promise((r) => setTimeout(r, 0));
  // no bridge: the sample, saying so
  const view = M.attach({ bridge: () => (withBridge ? bridge : null) });
  view.onView('overview');
  await tick();
  out.beforeVisit = els.memList.innerHTML;
  view.onView('memories');
  await tick(); await tick();
  out.sampleShown = (els.memList.innerHTML.match(/data-row=/g) || []).length;
  out.badgeShown = [!els.memBadge.hidden, els.memBadge.textContent];
  // with the bridge: one page, then the next
  withBridge = true;
  answer = (route, q) => route === M.LIST
    ? { items: q.after ? [Object.assign({}, row, { id: 'm:2' })] : [row], next: q.after ? '' : 'tok1', total: 2,
        places: [{ id: 'w:1', label: '群1' }] }
    : { id: q.id, text: '号码 12345678' };
  els.memKind.value = 'memory';
  els.memGo.listeners.click();
  await tick(); await tick();
  out.firstCall = calls[calls.length - 1];
  out.badgeAfter = els.memBadge.hidden;
  out.moreShown = !els.memMore.hidden;
  els.memMore.listeners.click();
  await tick(); await tick();
  out.secondCall = calls[calls.length - 1];
  out.rows = (els.memList.innerHTML.match(/data-row="m:\d"/g) || []);
  // the buttons of a row
  const card = { querySelector: (sel) => (sel === '.mem-row-state' ? state : text), remove() { out.removed = true; } };
  const state = { textContent: '' }, text = { innerHTML: '' };
  const button = (data) => ({ dataset: data, disabled: false, remove() { out.buttonGone = true; }, closest: () => card });
  await els.memList.listeners.click({ target: button({ number: 'm:1' }) });
  out.numberCall = calls[calls.length - 1];
  out.revealed = text.innerHTML;
  const before = calls.length;
  confirmAnswer = false;
  await els.memList.listeners.click({ target: button({ delete: 'mem1' }) });
  out.callsWhenNotConfirmed = calls.length - before;
  confirmAnswer = true;
  await els.memList.listeners.click({ target: button({ delete: 'mem1' }) });
  out.deleteCall = calls[calls.length - 1];
  out.posts = calls.filter((c) => c[0] === 'POST').length;
  process.stdout.write(JSON.stringify(out));
})();
"""
        out = subprocess.run(['node', '-e', script, str(JS)], capture_output=True, text=True, encoding='utf-8',
                             timeout=60, check=True).stdout
        cls.r = json.loads(out)

    def test_query_only_what_is_set(self):
        self.assertEqual(self.r['query'], {'kind': 'memory', 'vis': 'private', 'q': 'x' * 50, 'after': 'tok'})

    def test_a_row_is_escaped_with_its_buttons(self):
        row = self.r['row']
        self.assertNotIn('<script>', row)
        self.assertIn('&lt;script&gt;1&lt;/script&gt;<br>第二行', row)
        self.assertIn('跟谁有关：&lt;b&gt;', row)
        self.assertIn('data-number="m:1"', row)
        self.assertIn('data-delete="mem1"', row)
        self.assertNotIn('data-delete', self.r['rowEvent'])          # only a memory can be deleted
        self.assertNotIn('data-number', self.r['rowEvent'])

    def test_static_preview_shows_the_sample_saying_so(self):
        self.assertEqual(self.r['beforeVisit'], '')                  # nothing until the view is opened
        self.assertEqual(self.r['sampleShown'], len(self.r['sample']['items']))
        self.assertEqual(self.r['badgeShown'], [True, self.r['badge']])
        self.assertTrue(self.r['badge'].startswith('示例数据（编造）'))
        words = json.dumps([[i['text'], i['who'], i['where']] for i in self.r['sample']['items']], ensure_ascii=False)
        self.assertNotRegex(words, r'\d{5,}')                         # no number in its words
        self.assertEqual([i['date'][-5:] for i in self.r['sample']['items']], ['20:00', '19:00', '18:00', '17:00', '16:00', '15:00'])

    def test_with_the_bridge_pages_numbers_and_a_confirmed_delete(self):
        r = self.r
        self.assertEqual(r['firstCall'], ['GET', 'page/memories', {'kind': 'memory'}])
        self.assertTrue(r['badgeAfter'])
        self.assertTrue(r['moreShown'])
        self.assertEqual(r['secondCall'], ['GET', 'page/memories', {'kind': 'memory', 'after': 'tok1'}])
        self.assertEqual(r['rows'], ['data-row="m:1"', 'data-row="m:2"'])
        self.assertEqual(r['numberCall'], ['GET', 'page/memories/number', {'id': 'm:1'}])
        self.assertEqual(r['revealed'], '号码 12345678')
        self.assertEqual(r['callsWhenNotConfirmed'], 0)
        self.assertEqual(r['deleteCall'], ['POST', 'page/memory/delete/default/mem1', {}])
        self.assertEqual(r['posts'], 1)
        self.assertTrue(r['removed'])


def _row(i, ts, kind='memory', place='w:1', vis='public', raw='话', who=('阿橙',)):
    return {'id': 'm:%02d' % i, 'kind': kind, 'place': place, 'where': '群1', 'ts': float(ts), 'vis': vis,
            'who': list(who), 'raw': raw, 'entry': 'e%d' % i if kind == 'memory' else ''}


class Paging(unittest.TestCase):
    """memory_list.select / page on made-up rows."""

    def setUp(self):
        self.rows = [_row(i, 1000 + (i // 2)) for i in range(7)]       # equal times in pairs

    def test_every_row_once_in_order_with_equal_times(self):
        sel = memory_list.select(self.rows)
        got, after = [], ''
        for _ in range(10):
            p = memory_list.page(sel, after, 2)
            got += [r['id'] for r in p['items']]
            after = p['next']
            if not after:
                break
        self.assertEqual(got, [r['id'] for r in sel])
        self.assertEqual(len(set(got)), 7)

    def test_limits_and_bad_tokens(self):
        sel = memory_list.select(self.rows)
        self.assertEqual(len(memory_list.page(sel, '', 500)['items']), 7)           # at most PAGE_MAX
        self.assertEqual(len(memory_list.page(sel, '', 'x')['items']), 7)
        self.assertEqual(memory_list.page(sel, 'not-a-token', 3)['items'][0]['id'], sel[0]['id'])
        big = [_row(i, i) for i in range(120)]
        self.assertEqual(len(memory_list.page(memory_list.select(big), '', 99)['items']), memory_list.PAGE_MAX)

    def test_filters_and_hidden_numbers(self):
        rows = [_row(1, 10, raw='他的号是 1234567'), _row(2, 20, kind='note', vis='self', who=()),
                _row(3, 86400 * 365 * 40, vis='private', place='w:2', raw='爬山去')]
        ids = lambda sel: [r['id'] for r in sel]   # noqa: E731
        self.assertEqual(ids(memory_list.select(rows, kind='note')), ['m:02'])
        self.assertEqual(ids(memory_list.select(rows, vis='private')), ['m:03'])
        self.assertEqual(ids(memory_list.select(rows, place='w:2')), ['m:03'])
        self.assertEqual(ids(memory_list.select(rows, q='1234567')), [])            # not by a hidden number
        self.assertEqual(ids(memory_list.select(rows, q='号码')), ['m:01'])
        self.assertEqual(ids(memory_list.select(rows, q='阿橙')), ['m:03', 'm:01'])  # by name too
        self.assertEqual(ids(memory_list.select(rows, start='15', end='30')), ['m:02'])
        shown = memory_list.page(memory_list.select(rows), '', 50)['items']
        first = [s for s in shown if s['id'] == 'm:01'][0]
        self.assertEqual((first['text'], first['has_number']), ('他的号是 [号码]', True))
        self.assertEqual(memory_list.number(rows, 'm:01'), {'id': 'm:01', 'text': '他的号是 1234567'})
        self.assertIsNone(memory_list.number(rows, 'm:99'))


if __name__ == '__main__':
    unittest.main()
