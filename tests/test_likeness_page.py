""""像不像" in the panel (pages/dashboard/likeness.js, cards L1 and L2).

The plugin side (likeness.Store, page/likeness, page/likeness/rate) is in test_likeness. Here: the
panel's markup, and the page script with Node.js against a stand-in page (skipped without Node):
the ISO week, reading one week's answer, a day's lines, and rating through page/likeness/rate only.
No browser, no network.
"""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASH = ROOT / 'pages' / 'dashboard'
JS = DASH / 'likeness.js'


class InThePanel(unittest.TestCase):
    def test_a_view_before_settings(self):
        html = (DASH / 'index.html').read_text(encoding='utf-8')
        views = re.findall(r'class="nav-item[^"]*" data-view="([a-z]+)"', html)
        self.assertEqual(views[-2:], ['likeness', 'settings'])
        section = re.search(r'<section class="view" id="view-likeness">(.*?)</section>', html, re.S).group(1)
        for el in ('lkBadge', 'lkPrev', 'lkWeek', 'lkNext', 'lkState', 'lkSummary', 'lkReplies', 'lkDays'):
            self.assertIn('id="%s"' % el, section, el)
        self.assertLess(section.index('id="lkReplies"'), section.index('她的两天'))
        self.assertIn('<script src="./memories.js"></script><script src="./likeness.js?v=', html)
        app = (DASH / 'app.js').read_text(encoding='utf-8')
        self.assertIn('if(likenessPage) likenessPage.onView(name);', app)

    def test_only_the_two_routes(self):
        text = JS.read_text(encoding='utf-8')
        self.assertNotRegex(text, r'https?://')
        self.assertIn('const LIST = "page/likeness";', text)
        self.assertIn('const RATE = "page/likeness/rate";', text)
        self.assertEqual(text.count('apiPost('), 1)
        self.assertEqual(text.count('apiGet('), 1)
        for bad in ('apiPut', 'apiDelete', 'fetch(', 'XMLHttpRequest'):
            self.assertNotIn(bad, text)


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class PageScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script = r"""
const els = {};
const el = (id) => (els[id] = els[id] || { id, value: '', innerHTML: '', textContent: '', hidden: false, disabled: false,
  listeners: {}, addEventListener(k, f) { this.listeners[k] = f; } });
['lkReplies', 'lkDays', 'lkPrev', 'lkNext', 'lkWeek', 'lkState', 'lkSummary', 'lkBadge'].forEach(el);
global.window = {};
global.document = { getElementById: (id) => els[id] };
const M = require(process.argv[1]);
const out = {};
out.weeks = ['2026-11-01', '2026-10-26', '2026-01-01', '2024-12-30', '2021-01-03'].map((s) => {
  const [y, m, d] = s.split('-').map(Number); return M.weekOf(new Date(y, m - 1, d, 12)); });
const reply = { id: 'r1', ts: 1793000000, place: 'group', context: [{ name: '<i>阿橙</i>', text: '去爬山吗' }], reply: '去呀 [number]', rating: null, reason: '' };
const day = { id: 'day-2026-10-29', kind: 'day', date: '2026-10-29', rating: 'like', reason: '"像"', rows: [
  { time: '11:00', do: '听歌', detail: '', minutes: 30, feel: '耳熟' }, { time: '20:15', do: '<b>翻相册</b>', detail: '号码 [number]', minutes: null, feel: '' }] };
out.split = [M.split({ status: 'ok', data: [reply], days: [day] }), M.split({ status: 'ok', data: { status: 'ok', data: [reply], days: [] } }),
             M.split({ status: 'ok', data: [] })].map((s) => [s.replies.length, s.days.length]);
try { M.split({ status: 'error', message: 'invalid week', data: {} }); out.errorThrown = false; } catch (e) { out.errorThrown = e.message; }
out.lines = day.rows.map(M.dayLine);
out.day = M.dayHtml(day);
out.reply = M.replyHtml(reply);
(async () => {
  const tick = () => new Promise((r) => setTimeout(r, 0));
  const calls = [];
  let rateAnswer = { status: 'ok', data: {} };
  const bridge = { apiGet: async (route, q) => { calls.push(['GET', route, q]); return { status: 'ok', data: [reply], days: [day] }; },
                   apiPost: async (route, body) => { calls.push(['POST', route, body]); return rateAnswer; } };
  let withBridge = false;
  const view = M.attach({ bridge: () => (withBridge ? bridge : null) });
  view.onView('overview'); await tick();
  out.beforeVisit = els.lkReplies.innerHTML;
  view.onView('likeness'); await tick(); await tick();
  out.sample = [!els.lkBadge.hidden, (els.lkReplies.innerHTML.match(/lk-card/g) || []).length, (els.lkDays.innerHTML.match(/lk-card/g) || []).length];
  withBridge = true;
  view.reload(); await tick(); await tick();
  out.firstGet = calls[0];
  out.nextDisabled = els.lkNext.disabled;
  out.summary = els.lkSummary.textContent;
  // a stand-in card for the reply: 像 with a reason
  const card = (id, why) => { const state = { textContent: '' }; const picks = ['like', 'unlike', 'unsure'].map((r) => ({ dataset: { rating: r },
      classList: { on: new Set(), toggle(k, v) { v ? this.on.add(k) : this.on.delete(k); } }, setAttribute() {} }));
    return { dataset: { id }, state, picks, querySelector: (s) => (s === '.lk-state' ? state : { value: why }), querySelectorAll: () => picks }; };
  const click = (c, cls, rating) => els.lkReplies.listeners.click({ target: { classList: { contains: (k) => k === cls }, dataset: { rating }, closest: () => c } });
  const c1 = card('r1', ' 像她 ');
  await click(c1, 'lk-save', undefined);
  out.saveFirst = [calls.length, c1.state.textContent];
  await click(c1, 'lk-pick', 'like');
  out.rateCall = calls[calls.length - 1];
  out.rated = [c1.state.textContent, [...c1.picks[0].classList.on].sort(), els.lkSummary.textContent];
  const c2 = card('day-2026-10-29', '');
  rateAnswer = { status: 'error', data: {} };
  await click(c2, 'lk-save', undefined);
  out.dayCall = calls[calls.length - 1];
  out.notSaved = c2.state.textContent;
  els.lkPrev.listeners.click(); await tick(); await tick();
  out.prevGet = calls[calls.length - 1];
  out.posts = calls.filter((c) => c[0] === 'POST').map((c) => c[1]);
  process.stdout.write(JSON.stringify(out));
})();
"""
        run = subprocess.run(['node', '-e', script, str(JS)], capture_output=True, text=True, encoding='utf-8', timeout=60)
        if run.returncode:
            raise AssertionError(run.stderr)
        cls.out = json.loads(run.stdout)

    def test_iso_weeks_like_week_of(self):
        self.assertEqual(self.out['weeks'], ['2026-W44', '2026-W44', '2026-W01', '2025-W01', '2020-W53'])

    def test_reads_replies_and_days(self):
        self.assertEqual(self.out['split'], [[1, 1], [1, 0], [0, 0]])
        self.assertEqual(self.out['errorThrown'], 'invalid week')

    def test_a_day_one_line_each_escaped(self):
        first, second = self.out['lines']
        self.assertIn('11:00', first)
        self.assertIn('听歌（30 分钟）', first)
        self.assertIn('——耳熟', first)
        self.assertIn('&lt;b&gt;翻相册&lt;/b&gt;：号码 [号码]', second)
        self.assertNotIn('分钟', second)
        self.assertNotIn('<b>翻相册', self.out['day'])
        self.assertIn('10-29 周四', self.out['day'])
        self.assertIn('value="&quot;像&quot;"', self.out['day'])
        self.assertIn('lk-pick on primary" data-rating="like"', self.out['day'])

    def test_a_reply_escaped(self):
        self.assertIn('&lt;i&gt;阿橙&lt;/i&gt;', self.out['reply'])
        self.assertIn('去呀 [号码]', self.out['reply'])
        self.assertIn('>群里 · ', self.out['reply'])

    def test_sample_without_a_bridge_then_the_week(self):
        self.assertEqual(self.out['beforeVisit'], '')
        self.assertEqual(self.out['sample'], [True, 2, 2])
        self.assertEqual(self.out['firstGet'][:2], ['GET', 'page/likeness'])
        self.assertRegex(self.out['firstGet'][2]['week'], r'^\d{4}-W\d{2}$')
        self.assertTrue(self.out['nextDisabled'])
        self.assertEqual(self.out['summary'], '已经打了 1 / 2 个')

    def test_rating_only_through_rate(self):
        self.assertEqual(self.out['saveFirst'], [1, '先点 像 / 不像 / 说不准'])
        week = self.out['firstGet'][2]['week']
        self.assertEqual(self.out['rateCall'], ['POST', 'page/likeness/rate', {'week': week, 'id': 'r1', 'rating': 'like', 'reason': '像她'}])
        self.assertEqual(self.out['rated'], ['存好了', ['on', 'primary'], '已经打了 2 / 2 个'])
        self.assertEqual(self.out['dayCall'][2], {'week': week, 'id': 'day-2026-10-29', 'rating': 'like', 'reason': ''})
        self.assertEqual(self.out['notSaved'], '没存上：没存上')
        self.assertNotEqual(self.out['prevGet'][2]['week'], week)
        self.assertEqual(self.out['posts'], ['page/likeness/rate', 'page/likeness/rate'])


if __name__ == '__main__':
    unittest.main()
