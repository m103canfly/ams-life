"""The plugin's pages as AstrBot 4.29.3 lists them (dashboard/services/plugin_page_service.py,
discover_plugin_pages): every folder under pages/ with an index.html is a page, sorted by its
name in lower case, and the sidebar links only to the first. That must be the panel
("dashboard"); the brain map's own page is "starmap" so it sorts after it, and her stickers'
"stickers" after that (the console opens it straight away).

Page titles come from .astrbot-plugin/i18n/<locale>.json ("pages.<name>.title", and the
newer "views.<name>.title"). The sidebar's one entry for the plugin takes the first page's
title, so the panel's title still says ams-life.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
I18N = ROOT / '.astrbot-plugin' / 'i18n'


def pages():
    """The page names as AstrBot lists them."""
    dirs = sorted((d for d in (ROOT / 'pages').iterdir() if d.is_dir()), key=lambda d: d.name.lower())
    return [d.name for d in dirs if (d / 'index.html').is_file()]


class PluginPages(unittest.TestCase):
    def test_the_panel_comes_first(self):
        self.assertEqual(pages()[0], 'dashboard')

    def test_the_pages(self):
        self.assertEqual(pages(), ['dashboard', 'starmap', 'stickers'])

    def test_titles(self):
        files = sorted(I18N.glob('*.json'))
        self.assertEqual([f.stem for f in files], ['en-US', 'zh-CN'])
        for f in files:
            data = json.loads(f.read_text(encoding='utf-8'))
            for key in ('pages', 'views'):
                self.assertEqual(sorted(data[key]), pages(), (f.name, key))
                for name in pages():
                    self.assertTrue(data[key][name]['title'].strip(), (f.name, key, name))
            self.assertEqual(data['pages'], data['views'], f.name)
            self.assertIn('ams-life', data['pages']['dashboard']['title'], f.name)
        zh = json.loads((I18N / 'zh-CN.json').read_text(encoding='utf-8'))
        self.assertEqual(zh['pages']['dashboard']['title'], 'ams-life 面板')
        self.assertEqual(zh['pages']['starmap']['title'], '她的脑子（单独一页）')
        self.assertEqual(zh['pages']['stickers']['title'], '她的表情包')


if __name__ == '__main__':
    unittest.main()
