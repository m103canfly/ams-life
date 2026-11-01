""""小黑盒" in the panel's 钥匙 (pages/dashboard/heybox.js, card 1d, panel half).

The plugin side (heybox.Login, page/heybox/*) is in test_heybox. Here: the panel's markup, the
vendored code drawer (qrcodegen.js) and its notice, and the page script with Node.js against a
stand-in page (skipped without Node): what each state says, the code drawn here and its address
nowhere on the page, asking every few seconds and when that stops, and logging out only after a yes.
No browser, no network, no real dialog.
"""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASH = ROOT / 'pages' / 'dashboard'
JS = DASH / 'heybox.js'
QR = DASH / 'qrcodegen.js'
# made up: the shape of a 小黑盒 sign-in address, and what of it must not reach the page
URL = 'https://api.xiaoheihe.cn/account/qr_login/?qr=QRTOKEN12345abc&expire=1'
SECRETS = ('QRTOKEN12345abc', 'xiaoheihe', 'https://', 'qr_login')


class InThePanel(unittest.TestCase):
    def test_a_block_in_keys(self):
        html = (DASH / 'index.html').read_text(encoding='utf-8')
        keys = re.search(r'<div class="panel settings settings-panel keys-panel" id="settingsKeys" hidden>(.*?)\n      </div>\n', html, re.S).group(1)
        block = re.search(r'<div class="heybox" id="heyboxBox" hidden>(.*?)\n        </div>', keys, re.S).group(1)
        for cls in ('hb-state', 'hb-actions', 'hb-badge', 'hb-qr', 'hb-tip', 'hb-msg'):
            self.assertIn('class="', block)
            self.assertRegex(block, r'class="[^"]*\b%s\b' % cls, cls)
        order = [html.index(s) for s in ('<script src="./qrcodegen.js', '<script src="./heybox.js', '<script src="./app.js')]
        self.assertEqual(order, sorted(order))
        app = (DASH / 'app.js').read_text(encoding='utf-8')
        self.assertIn('if(heyboxPage) heyboxPage.onView(name);', app)
        self.assertIn('window.BioHeybox.attach({bridge:()=>bridge})', app)

    def test_only_the_three_routes_and_nothing_sent_elsewhere(self):
        text = JS.read_text(encoding='utf-8')
        self.assertNotRegex(text, r'https?://')
        for route in ('page/heybox/status', 'page/heybox/login', 'page/heybox/logout'):
            self.assertEqual(text.count('"%s"' % route), 1, route)
        self.assertEqual(len(re.findall(r'apiPost\((STATUS|LOGIN|LOGOUT), \{\}\)', text)), 4)
        self.assertEqual(text.count('apiPost('), 4)
        for bad in ('apiGet', 'fetch(', 'XMLHttpRequest', 'new Image', 'console.', '.src', 'src=', 'href', 'localStorage', 'sendBeacon', 'WebSocket'):
            self.assertNotIn(bad, text, bad)
        # qr_url is read once, straight into the code drawer
        code = re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)
        self.assertEqual(re.findall(r'[\w.]*qr_url[\w.]*', code), ['a.qr_url', 'a.qr_url', 'a.qr_url'])
        self.assertIn('waitFor(a.qr_url, a.expire)', code)

    def test_the_code_drawer_keeps_its_mit_notice(self):
        head = QR.read_text(encoding='utf-8')[:3000]
        self.assertTrue(head.startswith('/* \n * QR Code generator library (TypeScript)\n') or
                        head.startswith('/* \r\n * QR Code generator library (TypeScript)\r\n'))
        for must in ('Copyright (c) Project Nayuki. (MIT License)', 'Permission is hereby granted, free of charge',
                     'https://github.com/nayuki/QR-Code-generator', 'v1.8.0', '720f62bddb7226106071d4728c292cb1df519ceb'):
            self.assertIn(must, head, must)
        whole = QR.read_text(encoding='utf-8')
        self.assertNotRegex(re.sub(r'/\*.*?\*/', '', whole, flags=re.S), r'https?://|fetch\(|XMLHttpRequest|import\(|require\(')
        notice = (ROOT / 'NOTICE.md').read_text(encoding='utf-8')
        self.assertIn('pages/dashboard/qrcodegen.js', notice)
        self.assertIn('720f62bddb7226106071d4728c292cb1df519ceb', notice)


@unittest.skipUnless(shutil.which('node'), 'Node.js not installed')
class PageScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script = r"""
const vm = require('vm'), fs = require('fs');
const [jsPath, qrPath, url] = process.argv.slice(1);
const logged = [];
for (const k of ['log', 'info', 'warn', 'error', 'debug']) console[k] = (...a) => logged.push(a.map(String).join(' '));
vm.runInThisContext(fs.readFileSync(qrPath, 'utf-8'));
const encoded = [];
const realEncode = qrcodegen.QrCode.encodeText;
qrcodegen.QrCode.encodeText = (text, ecl) => { encoded.push(text); return realEncode(text, ecl); };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const M = require(jsPath);
const out = {};

// a stand-in page: the 钥匙 tab, title and panel, and the block's own parts
function el(id) {
  return { id, innerHTML: '', textContent: '', hidden: true, dataset: {}, listeners: {}, cls: new Set(),
    classList: { toggle(k, v) { v ? this.owner.cls.add(k) : this.owner.cls.delete(k); } },
    addEventListener(k, f) { this.listeners[k] = f; } };
}
function page() {
  const els = {};
  for (const id of ['heyboxBox', 'settingsKeysTab', 'settingsKeysTitle', 'settingsKeys', 'settingsTabs']) els[id] = el(id);
  const parts = {};
  for (const c of ['hb-state', 'hb-actions', 'hb-badge', 'hb-qr', 'hb-tip', 'hb-msg']) { parts[c] = el(c); parts[c].hidden = false; }
  parts['hb-badge'].hidden = true; parts['hb-qr'].hidden = true;
  for (const e of Object.values(els).concat(Object.values(parts))) e.classList.owner = e;
  els.heyboxBox.querySelector = (s) => parts[s.slice(1)];
  global.document = { getElementById: (id) => els[id] };
  return { els, parts };
}
// what the block shows: its words (all of them) and its one button
function seen(p) {
  const m = /data-hb="(\w+)">([^<]+)</.exec(p.parts['hb-actions'].innerHTML);
  return { state: p.parts['hb-state'].textContent, button: m ? m[1] : null, word: m ? m[2] : null, msg: p.parts['hb-msg'].textContent,
    tip: p.parts['hb-tip'].textContent, qr: !p.parts['hb-qr'].hidden, hidden: p.els.heyboxBox.hidden };
}
function everything(p) {
  return JSON.stringify([p.els, p.parts], (k, v) => (k === 'owner' ? undefined : v instanceof Set ? [...v] : typeof v === 'function' ? undefined : v));
}
async function click(p, action) {
  const m = /data-hb="(\w+)"/.exec(p.parts['hb-actions'].innerHTML);
  if (!m || m[1] !== action) throw new Error('no ' + action + ' button, only ' + (m && m[1]));
  p.els.heyboxBox.listeners.click({ target: { closest: (s) => (s === '[data-hb]' ? { dataset: { hb: action } } : null) } });
  await sleep(5);
}
// a stand-in bridge: our own server's, answering each route from its own list (the last answer repeats)
function bridgeOf(answers, calls, standalone = true) {
  return { standalone, apiPost: async (route, body) => {
    calls.push(route);
    const list = answers[route] || [{ state: 'idle' }];
    const a = list.length > 1 ? list.shift() : list[0];
    if (a instanceof Error) throw a;
    return a;
  } };
}
const once = (make) => { let b; return () => (b = b || make()); };
let answerConfirm = false;
const asked = [];
global.window = { confirm: (q) => { asked.push(q); return answerConfirm; }, qrcodegen };

(async () => {
  // 1. every state: its words and its button, as the first look at 设置 reads it
  out.states = {};
  for (const state of Object.keys(M.STATES).concat(['something_new'])) {
    const p = page(), calls = [];
    const view = M.attach({ bridge: once(() => bridgeOf({ 'page/heybox/status': [{ status: 'ok', data: { state } }] }, calls)) });
    view.onView('settings'); await sleep(5);
    out.states[state] = seen(p);
  }

  // 2. a code: drawn here from qr_url, then asked about every few ms until signed in
  {
    const p = page(), calls = [];
    const answers = { 'page/heybox/status': [{ state: 'idle' }, { state: 'waiting' }, { state: 'waiting' }, { status: 'ok', data: { state: 'logged_in' } }],
      'page/heybox/login': [{ status: 'ok', data: { state: 'waiting', qr_url: url, expire: 120 } }] };
    const view = M.attach({ bridge: once(() => bridgeOf(answers, calls)), pollMs: 30, tickMs: 20 });
    view.onView('settings'); await sleep(5);
    await click(p, 'login');
    out.waiting = seen(p);
    out.svg = p.parts['hb-qr'].innerHTML.slice(0, 60);
    out.squares = (p.parts['hb-qr'].innerHTML.match(/h1v1h-1z/g) || []).length;
    out.encoded = encoded.slice();
    out.pageWhileWaiting = everything(p);
    await sleep(200);
    out.signedIn = seen(p);
    out.signedInCalls = calls.slice();
    await sleep(150);
    out.afterSignedIn = calls.length;
    out.pageAfter = everything(p);
  }

  // 3. the code's time runs out: 二维码过期了, and no more asking
  {
    const p = page(), calls = [];
    const view = M.attach({ bridge: once(() => bridgeOf({ 'page/heybox/status': [{ state: 'idle' }, { state: 'waiting' }],
      'page/heybox/login': [{ state: 'waiting', qr_url: url, expire: 1 }] }, calls)), pollMs: 200, tickMs: 50 });
    view.onView('settings'); await sleep(5);
    await click(p, 'login');
    await sleep(1250);
    out.expired = seen(p);
    const n = calls.length;
    await sleep(500);
    out.expiredMore = calls.length - n;
  }

  // 4. leaving 设置, another tab of 设置, 取消: each stops the asking
  out.stops = {};
  for (const how of ['view', 'tab', 'cancel']) {
    const p = page(), calls = [];
    const view = M.attach({ bridge: once(() => bridgeOf({ 'page/heybox/status': [{ state: 'idle' }, { state: 'waiting' }],
      'page/heybox/login': [{ state: 'waiting', qr_url: url, expire: 120 }] }, calls)), pollMs: 30, tickMs: 20 });
    view.onView('settings'); await sleep(5);
    await click(p, 'login');
    await sleep(80);
    const before = calls.length;
    if (how === 'view') view.onView('overview');
    else if (how === 'tab') p.els.settingsTabs.listeners.click({ target: { closest: () => ({ dataset: { settingsTarget: 'settingsMemory' } }) } });
    else await click(p, 'cancel');
    await sleep(200);
    out.stops[how] = { askedBefore: before, more: calls.length - before, shown: seen(p) };
  }

  // 5. 退出登录 asks first: no, nothing is sent; yes, logout is sent
  {
    const p = page(), calls = [];
    const view = M.attach({ bridge: once(() => bridgeOf({ 'page/heybox/status': [{ state: 'logged_in' }], 'page/heybox/logout': [{ state: 'idle' }] }, calls)) });
    view.onView('settings'); await sleep(5);
    answerConfirm = false;
    await click(p, 'logout');
    out.logoutNo = { calls: calls.slice(), asked: asked.length, shown: seen(p) };
    answerConfirm = true;
    await click(p, 'logout');
    out.logoutYes = { calls: calls.slice(), asked: asked.length, question: asked[asked.length - 1], shown: seen(p) };
  }

  // 6. failures say only a status; the login answer without a code is 没拿到二维码
  {
    const p = page(), calls = [];
    const view = M.attach({ bridge: once(() => bridgeOf({ 'page/heybox/status': [{ state: 'idle' }],
      'page/heybox/login': [{ state: 'waiting' }, { state: 'captcha' }, new Error('HTTP 403 token ' + url)] }, calls)) });
    view.onView('settings'); await sleep(5);
    await click(p, 'login'); out.noCode = seen(p);
    await click(p, 'retry'); out.captcha = seen(p);
    const p2 = page(), calls2 = [];
    const v2 = M.attach({ bridge: once(() => bridgeOf({ 'page/heybox/status': [{ state: 'failed' }], 'page/heybox/login': [new Error('HTTP 403 ' + url)] }, calls2)) });
    v2.onView('settings'); await sleep(5);
    await click(p2, 'retry'); out.http = seen(p2); out.httpPage = everything(p2);
  }

  // 7. no bridge (a static preview): an invented code, saying so, nothing sent; inside AstrBot: hidden
  {
    const p = page();
    encoded.length = 0;
    const view = M.attach({ bridge: () => null });
    view.onView('settings'); await sleep(5);
    await click(p, 'cancel');
    out.sample = { shown: seen(p), badge: p.parts['hb-badge'].hidden ? null : p.parts['hb-badge'].textContent, tab: !p.els.settingsKeysTab.hidden,
      encoded: encoded.slice() };
    const p2 = page(), calls = [];
    const v2 = M.attach({ bridge: once(() => bridgeOf({}, calls, false)) });
    v2.onView('settings'); await sleep(5);
    out.astrbot = { hidden: p2.els.heyboxBox.hidden, tab: !p2.els.settingsKeysTab.hidden, calls };
  }
  // 8. the panel opened straight on 设置 (?view=settings): 设置 comes before app.js has its bridge.
  //    Once the bridge is there, the next 设置 or 钥匙 is the real block, not the invented code.
  out.lateBridge = {};
  for (const how of ['view', 'tab', 'astrbot']) {
    const p = page(), calls = [];
    let cur = null;
    const real = bridgeOf({ 'page/heybox/status': [{ state: 'logged_in' }], 'page/heybox/login': [{ state: 'waiting', qr_url: url, expire: 120 }] },
      calls, how !== 'astrbot');
    const view = M.attach({ bridge: () => cur, pollMs: 30, tickMs: 20 });
    view.onView('settings'); await sleep(5);
    const before = { badge: !p.parts['hb-badge'].hidden, tab: !p.els.settingsKeysTab.hidden };
    cur = real;
    if (how === 'tab') p.els.settingsTabs.listeners.click({ target: { closest: () => ({ dataset: { settingsTarget: 'settingsKeys' } }) } });
    else { view.onView('overview'); view.onView('settings'); }
    await sleep(5);
    out.lateBridge[how] = { before, badge: !p.parts['hb-badge'].hidden, tab: !p.els.settingsKeysTab.hidden, calls: calls.slice(), shown: seen(p) };
    if (how === 'tab') {
      answerConfirm = true;
      out.lateBridge.tabLogout = await click(p, 'logout').then(() => calls.slice(), (e) => e.message);
    }
  }
  out.logged = logged;
  process.stdout.write(JSON.stringify(out), () => process.exit(0));
})().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
"""
        run = subprocess.run(['node', '-e', script, str(JS), str(QR), URL], capture_output=True, text=True,
                             encoding='utf-8', timeout=120)
        if run.returncode:
            raise AssertionError(run.stderr)
        cls.out = json.loads(run.stdout)

    def assertNothingOf(self, text):
        for s in SECRETS:
            self.assertNotIn(s, text, s)

    def test_each_state_its_words_and_button(self):
        want = {
            'idle': ('没登录', 'login', '登录'),
            'waiting': ('在等扫码，这边的二维码已经收起来了', 'retry', '再试'),
            'logged_in': ('已登录', 'logout', '退出登录'),
            'relogin': ('要重新扫码', 'login', '登录'),
            'captcha': ('小黑盒要人工验证，先停了；退出登录以后可以重新扫码', 'logout', '退出登录'),
            'review_required': ('第一次真跑没成功，先停了，等审核看', 'logout', '退出登录'),
            'failed': ('没拿到二维码', 'retry', '再试'),
            'expired': ('二维码过期了', 'retry', '再试'),
            'something_new': ('说不清现在是什么状态', 'login', '登录'),
        }
        for state, (words, button, word) in want.items():
            got = self.out['states'][state]
            self.assertEqual((got['state'], got['button'], got['word']), (words, button, word), state)
            self.assertFalse(got['qr'], state)
            self.assertFalse(got['hidden'], state)

    def test_the_code_is_drawn_here_and_its_address_is_nowhere(self):
        w = self.out['waiting']
        self.assertEqual((w['state'], w['button'], w['word']), ('等扫码', 'cancel', '取消'))
        self.assertTrue(w['qr'])
        self.assertRegex(w['tip'], r'^用她那个号的小黑盒 App 扫一下（还剩 1[12]\d 秒）$')
        self.assertEqual(self.out['encoded'], [URL])
        self.assertTrue(self.out['svg'].startswith('<svg class="hb-code" viewBox="0 0 '))
        self.assertGreater(self.out['squares'], 100)
        for page in ('pageWhileWaiting', 'pageAfter', 'httpPage'):
            self.assertNothingOf(self.out[page])
            self.assertNotRegex(self.out[page], r'\b(src|href)=')
        self.assertNothingOf(' '.join(self.out['logged']))
        self.assertEqual(self.out['logged'], [])

    def test_asks_every_few_seconds_until_signed_in(self):
        self.assertEqual(self.out['signedInCalls'][:2], ['page/heybox/status', 'page/heybox/login'])
        self.assertEqual(self.out['signedInCalls'][2:], ['page/heybox/status'] * 3)
        self.assertEqual(self.out['afterSignedIn'], 5)
        s = self.out['signedIn']
        self.assertEqual((s['state'], s['button'], s['qr'], s['tip']), ('已登录', 'logout', False, ''))

    def test_the_time_runs_out(self):
        e = self.out['expired']
        self.assertEqual((e['state'], e['button'], e['qr']), ('二维码过期了', 'retry', False))
        self.assertEqual(self.out['expiredMore'], 0)

    def test_leaving_or_cancelling_stops_asking(self):
        for how, got in self.out['stops'].items():
            self.assertGreater(got['askedBefore'], 2, how)
            self.assertEqual(got['more'], 0, how)
            self.assertFalse(got['shown']['qr'], how)
            self.assertEqual(got['shown']['button'], 'login', how)
        self.assertEqual(self.out['stops']['view']['shown']['state'], '离开了这一页，这边不再等扫码')
        self.assertEqual(self.out['stops']['tab']['shown']['state'], '离开了这一页，这边不再等扫码')
        self.assertEqual(self.out['stops']['cancel']['shown']['state'], '取消了：这边不再等扫码')

    def test_logout_only_after_a_yes(self):
        no, yes = self.out['logoutNo'], self.out['logoutYes']
        self.assertEqual(no['calls'], ['page/heybox/status'])
        self.assertEqual(no['asked'], 1)
        self.assertEqual(no['shown']['state'], '已登录')
        self.assertEqual(yes['calls'], ['page/heybox/status', 'page/heybox/logout'])
        self.assertEqual(yes['question'], '退出小黑盒登录吗？\n退出以后她就刷不了小黑盒，要重新扫码。')
        self.assertEqual((yes['shown']['state'], yes['shown']['button'], yes['shown']['msg']), ('没登录', 'login', '退出了'))

    def test_no_code_captcha_and_errors(self):
        self.assertEqual((self.out['noCode']['state'], self.out['noCode']['button']), ('没拿到二维码', 'retry'))
        self.assertEqual((self.out['captcha']['state'], self.out['captcha']['button']),
                         ('小黑盒要人工验证，先停了；退出登录以后可以重新扫码', 'logout'))
        self.assertEqual(self.out['http']['msg'], '没要到二维码（HTTP 403）')
        self.assertEqual(self.out['http']['state'], '没拿到二维码')

    def test_a_static_preview_sends_nothing_and_astrbot_hides_it(self):
        s = self.out['sample']
        self.assertTrue(s['badge'].startswith('示例（编造）'))
        self.assertTrue(s['shown']['qr'])
        self.assertEqual(s['shown']['msg'], '示例里不发')
        self.assertTrue(s['tab'])
        self.assertEqual(len(s['encoded']), 1)
        self.assertNotIn('xiaoheihe', s['encoded'][0])
        a = self.out['astrbot']
        self.assertEqual((a['hidden'], a['tab'], a['calls']), (True, False, []))

    def test_a_bridge_that_comes_late_is_used(self):
        for how in ('view', 'tab'):
            got = self.out['lateBridge'][how]
            self.assertEqual(got['before'], {'badge': True, 'tab': True}, how)
            self.assertFalse(got['badge'], how)
            self.assertEqual(got['calls'], ['page/heybox/status'], how)
            s = got['shown']
            self.assertEqual((s['state'], s['button'], s['qr'], s['tip'], s['hidden']), ('已登录', 'logout', False, '', False), how)
        self.assertEqual(self.out['lateBridge']['tabLogout'], ['page/heybox/status', 'page/heybox/logout'])
        a = self.out['lateBridge']['astrbot']
        self.assertEqual((a['shown']['hidden'], a['tab'], a['calls']), (True, False, []))


if __name__ == '__main__':
    unittest.main()
