"""The panel's "GitHub 仓库地址" (pages/dashboard/repo_link.js, signoff 44): AstrBot's frame opens no new window,
so the button shows the address with "复制"; where the frame does not let the page use the clipboard, the
address is selected for Ctrl+C. The copying runs with Node.js against stand-ins (skipped without Node)."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

DASH = Path(__file__).resolve().parent.parent / 'pages' / 'dashboard'
REPO = 'https://github.com/m103canfly/ams-life'


def node(script, *args):
    out = subprocess.run(['node', '-e', script, str(DASH / 'repo_link.js'), *args], capture_output=True, text=True,
                         encoding='utf-8', timeout=60, check=True).stdout
    return json.loads(out.strip().splitlines()[-1])


class OnThePage(unittest.TestCase):
    def test_no_new_window(self):
        html = (DASH / 'index.html').read_text('utf-8')
        for name in ['index.html', 'app.js', 'repo_link.js']:
            text = (DASH / name).read_text('utf-8')
            self.assertNotIn('_blank', text, name)
            self.assertNotIn('window.open', text, name)
        btn = re.search(r'<button [^>]*id="updateOpenRepo"[^>]*>', html)
        self.assertIsNotNone(btn, 'the GitHub one is a button, not a link')
        self.assertIn('data-repo="%s"' % REPO, btn.group(0))
        self.assertIsNotNone(re.search(r'<button [^>]*id="updateOpenGitee"', html))
        self.assertIn('<input type="text" id="repoAddrText" readonly', html)
        self.assertIn('<script src="./repo_link.js"></script>', html)
        self.assertLess(html.index('./repo_link.js'), html.index('./app.js'))   # app.js attaches it
        for name in ['updateOpenRepo', 'updateOpenGitee', 'repoCopyBtn']:   # no call to the plugin: no "好了"/"没成功"
            self.assertRegex(html, r'<button [^>]*class="[^"]*\bfb-skip\b[^"]*" id="%s"' % name)

    def test_the_address_is_the_repo(self):
        app = (DASH / 'app.js').read_text('utf-8')
        self.assertIn('const BIO_REPO_SLUG = "m103canfly/ams-life";', app)
        self.assertIn('源码：' + REPO, (DASH / 'index.html').read_text('utf-8'))


@unittest.skipUnless(shutil.which('node'), 'needs Node.js')
class Copying(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = node(r'''
const R = require(process.argv[1]);
const input = () => ({ value: 'https://github.com/m103canfly/ams-life', focused: 0, selected: 0,
                       focus() { this.focused++; }, select() { this.selected++; } });
async function run(clip) {
  const i = input(), note = { textContent: '' }, wrote = [];
  if (clip === 'ok') clip = { writeText: async (t) => { wrote.push(t); } };
  else if (clip === 'no') clip = { writeText: async () => { throw new Error('NotAllowedError'); } };
  else if (clip === 'hangs') clip = { writeText: () => new Promise(() => {}) };
  const got = await R.copyAddress(i, note, clip, 50);
  return { got, wrote, selected: i.selected, focused: i.focused, note: note.textContent };
}
(async () => {
  const out = { ok: await run('ok'), no: await run('no'), none: await run(undefined),
                hangs: await run('hangs'), consts: [R.COPIED, R.SELECTED] };
  process.stdout.write(JSON.stringify(out));
})();
''')

    def test_the_clipboard_first(self):
        r = self.r['ok']
        self.assertEqual((r['got'], r['wrote'], r['selected']), ('copied', [REPO], 0))
        self.assertEqual(r['note'], self.r['consts'][0])

    def test_not_allowed_selects_for_ctrl_c(self):
        for case in ['no', 'none', 'hangs']:
            r = self.r[case]
            self.assertEqual((r['got'], r['selected'], r['focused']), ('selected', 1, 1), case)
            self.assertEqual(r['note'], self.r['consts'][1], case)
            self.assertIn('Ctrl+C', r['note'])


@unittest.skipUnless(shutil.which('node'), 'needs Node.js')
class TheLine(unittest.TestCase):
    """Clicking a button shows its address; the Gitee mirror's line goes when the mirror is cleared."""

    def test_show_and_follow(self):
        r = node(r'''
const R = require(process.argv[1]);
function el(init) {
  return Object.assign({ listeners: {}, dataset: {}, style: {}, hidden: false, value: '', textContent: '',
                         addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); },
                         focus() {}, select() {} }, init);
}
const gh = el({ dataset: { repo: 'https://github.com/m103canfly/ams-life' } });
const gitee = el({ dataset: { repo: 'https://gitee.com/someone/ams-life' } });
const els = { repoAddr: el({ hidden: true }), repoAddrText: el(), repoCopyBtn: el(), repoCopyNote: el() };
const doc = { getElementById: (id) => els[id] || null, querySelectorAll: () => [gh, gitee] };
const link = R.attach(doc, undefined);
const click = (e) => e.listeners.click.forEach((f) => f());
const seen = [els.repoAddr.hidden];
click(gh); seen.push([els.repoAddr.hidden, els.repoAddrText.value, els.repoCopyNote.textContent === R.SHOWN]);
click(gitee); gitee.dataset.repo = 'https://gitee.com/other/ams-life'; link.refresh();
seen.push([els.repoAddr.hidden, els.repoAddrText.value]);
gitee.dataset.repo = ''; gitee.style.display = 'none'; link.refresh(); seen.push(els.repoAddr.hidden);
click(gh); seen.push([els.repoAddr.hidden, els.repoAddrText.value]);
const none = R.attach({ getElementById: () => null, querySelectorAll: () => [] }); none.refresh();
process.stdout.write(JSON.stringify(seen));
''')
        self.assertEqual(r, [True, [False, REPO, True], [False, 'https://gitee.com/other/ams-life'], True,
                             [False, REPO]])


if __name__ == '__main__':
    unittest.main()
