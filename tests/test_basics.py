"""Import, identity and licence checks that need no conversation."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA = Path(tempfile.mkdtemp(prefix='ams-life-basics-'))
CLOCK = harness.prepare(DATA)
import main  # noqa: E402
import interpretation  # noqa: E402


class Identity(unittest.TestCase):
    def test_data_dir_follows_env(self):
        self.assertEqual(main.DATA_DIR, DATA)

    def test_default_data_dir_name(self):
        self.assertEqual(main._PERSIST_DATA_DIR.name, 'astrbot_plugin_ams_life')

    def test_routes_use_new_name(self):
        ctx = harness.FakeContext()
        main.BioCorePlugin(ctx, config={})
        self.assertTrue(ctx.web_routes)
        self.assertTrue(all(r.startswith('/astrbot_plugin_ams_life/page/') for r in ctx.web_routes), ctx.web_routes)

    def test_metadata(self):
        text = (ROOT / 'metadata.yaml').read_text('utf-8')
        self.assertIn('name: astrbot_plugin_ams_life', text)
        self.assertIn('repo: https://github.com/m103canfly/ams-life', text)

    def test_licence_and_attribution(self):
        self.assertIn('GNU AFFERO GENERAL PUBLIC LICENSE', (ROOT / 'LICENSE').read_text('utf-8'))
        notice = (ROOT / 'NOTICE.md').read_text('utf-8')
        self.assertIn('b3c214c80c85f3e35d82fdb5e04c1809dfac9b28', notice)
        self.assertIn('Johnhmzm', notice)
        self.assertIn('NOTICE.md', (ROOT / 'main.py').read_text('utf-8').splitlines()[2])


class Interpretation(unittest.TestCase):
    def test_reply_tag_is_stripped(self):
        clean, meta = interpretation.parse_response('好呀~<bc>{"e":"joy","i":0.6}</bc>')
        self.assertEqual(clean, '好呀~')
        self.assertTrue(meta)

    def test_no_tag(self):
        self.assertEqual(interpretation.parse_response('好呀~'), ('好呀~', None))


if __name__ == '__main__':
    unittest.main()
