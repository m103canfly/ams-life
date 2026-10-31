# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""tools/migrate_data.py on made-up folders: the copy, the keys left empty, and the check.

Every folder is made up inside the test's own temporary folder; every key and number is
invented. No real data folder is read or written."""
import ast
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from tools import migrate_data  # noqa: E402

KEY_ONE, KEY_TWO = 'fake-key-编造-1', 'fake-key-编造-2'
API_CONFIG = 'api_config.json'
CONFIG = {
    'llm': {'source': 'custom', 'base_url': 'https://model.invalid/v1', 'api_key': KEY_ONE,
            'model': 'made-up-model', 'enabled': True},
    'tts': {'source': 'astrbot', 'base_url': '', 'api_key': KEY_TWO, 'model': '', 'enabled': False},
    'image': {'source': 'custom', 'base_url': '', 'api_key': '', 'model': '', 'enabled': True},
    'functions': {'reply_summary': {'enabled': True, 'provider': 'follow_llm'}},
    'compression': {'enabled': False, 'threshold': 6000, 'max_chars': 800},
}


def made_up_src(folder, config=True):
    """A made-up plugin data folder: nested folders, an empty one, a binary file, a config."""
    folder = Path(folder)
    folder.mkdir(parents=True)
    if config:
        (folder / API_CONFIG).write_text(json.dumps(CONFIG, ensure_ascii=False, indent=1), 'utf-8')
    (folder / 'people').mkdir()
    (folder / 'people' / 'group_900001.json').write_text(
        json.dumps({'place': 'group:900001', 'people': {}}, ensure_ascii=False), 'utf-8')
    nested = folder / 'archives' / 'sessions' / 'default'
    nested.mkdir(parents=True)
    (nested / 'events.jsonl').write_text('{"id": "made-up"}\n', 'utf-8')
    (folder / 'logs').mkdir()
    (folder / 'logs' / 'old.log').write_text('虚构日志\n', 'utf-8')
    (folder / 'states').mkdir()
    (folder / 'blob.bin').write_bytes(bytes(range(256)))
    return folder


def src_at(tmp, config=True):
    """The made-up source, at the shape of the real one (old/plugin_data/...)."""
    return made_up_src(Path(tmp) / 'old' / 'plugin_data' / 'astrbot_plugin_ams_life', config)


def files(folder):
    folder = Path(folder)
    if not folder.is_dir():
        return []
    return sorted(path.relative_to(folder).as_posix() for path in folder.rglob('*') if path.is_file())


def hashes(folder):
    return {name: hashlib.sha256((Path(folder) / name).read_bytes()).hexdigest() for name in files(folder)}


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = migrate_data.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def copied(tmp):
    src, dst = src_at(tmp), Path(tmp) / 'new' / 'data'
    code, out, err = run('--src', str(src), '--dst', str(dst))
    if code:
        raise AssertionError(out + err)
    return src, dst, out, err


class Copy(unittest.TestCase):
    def test_copy_clears_the_keys_and_keeps_everything_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst, out, err = copied(Path(tmp))
            self.assertEqual(files(dst), files(src))
            for name in files(src):
                if name != API_CONFIG:
                    self.assertEqual((dst / name).read_bytes(), (src / name).read_bytes(), name)
            self.assertTrue((dst / 'states').is_dir())   # an empty folder is made too
            expected = json.loads(json.dumps(CONFIG, ensure_ascii=False))
            expected['llm']['api_key'] = ''
            expected['tts']['api_key'] = ''
            self.assertEqual((dst / API_CONFIG).read_text('utf-8'),
                             json.dumps(expected, ensure_ascii=False, indent=1))
            for kind in ('llm', 'tts'):
                self.assertIn(kind, out)
            for key in (KEY_ONE, KEY_TWO):
                self.assertNotIn(key, out + err)

    def test_the_source_is_not_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = src_at(tmp)
            before = hashes(src)
            code, out, err = run('--src', str(src), '--dst', str(Path(tmp) / 'new' / 'data'))
            self.assertEqual(code, 0, out + err)
            self.assertEqual(hashes(src), before)


class Verify(unittest.TestCase):
    def test_verify_passes_after_a_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst, _out, _err = copied(Path(tmp))
            code, out, err = run('--src', str(src), '--dst', str(dst), '--verify')
            self.assertEqual(code, 0, out + err)
            self.assertIn('都对上了', out)

    def test_verify_catches_one_changed_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst, _out, _err = copied(Path(tmp))
            blob = dst / 'blob.bin'
            data = blob.read_bytes()
            blob.write_bytes(data[:-1] + bytes([data[-1] ^ 1]))
            code, out, err = run('--src', str(src), '--dst', str(dst), '--verify')
            self.assertEqual(code, 1, out + err)
            self.assertIn('blob.bin', out)

    def test_verify_catches_a_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst, _out, _err = copied(Path(tmp))
            (dst / 'logs' / 'old.log').unlink()
            code, out, err = run('--src', str(src), '--dst', str(dst), '--verify')
            self.assertEqual(code, 1, out + err)
            self.assertIn('logs/old.log', out)

    def test_verify_catches_an_extra_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst, _out, _err = copied(Path(tmp))
            (dst / 'extra.txt').write_text('编造', 'utf-8')
            code, out, err = run('--src', str(src), '--dst', str(dst), '--verify')
            self.assertEqual(code, 1, out + err)
            self.assertIn('extra.txt', out)

    def test_a_key_in_another_file_is_found_and_only_its_path_is_printed(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst, _out, _err = copied(Path(tmp))
            (dst / 'logs' / 'old.log').write_text('虚构日志\n' + KEY_TWO + '\n', 'utf-8')
            code, out, err = run('--src', str(src), '--dst', str(dst), '--verify')
            self.assertEqual(code, 1)
            self.assertIn('logs/old.log', out)
            found = [line for line in out.splitlines() if line.startswith('含 Key 明文')]
            self.assertEqual(found, ['含 Key 明文：logs/old.log'])   # the copy's own config is clean
            self.assertNotIn(API_CONFIG, out)
            for key in (KEY_ONE, KEY_TWO):
                self.assertNotIn(key, out + err)


class Refuses(unittest.TestCase):
    def test_a_wal_still_being_written_stops_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            src = src_at(tmp)
            (src / 'forget_registry.sqlite3-wal').write_bytes(b'not empty')
            dst = tmp / 'new' / 'data'
            code, out, err = run('--src', str(src), '--dst', str(dst))
            self.assertEqual(code, 2)
            self.assertIn('AstrBot', err)
            self.assertEqual(list(dst.rglob('*')) if dst.exists() else [], [])
            # an empty one is quiet: AstrBot is not writing through it
            (src / 'forget_registry.sqlite3-wal').write_bytes(b'')
            code, out, err = run('--src', str(src), '--dst', str(dst))
            self.assertEqual(code, 0, out + err)
            self.assertIn('forget_registry.sqlite3-wal', files(dst))

    def test_the_guard_refuses_a_full_folder_and_a_live_data_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            src = src_at(tmp)
            full = tmp / 'full'
            full.mkdir()
            (full / 'left.txt').write_text('编造', 'utf-8')
            code, out, err = run('--src', str(src), '--dst', str(full))
            self.assertEqual(code, 2)
            self.assertIn('refusing', err)
            self.assertEqual(files(full), ['left.txt'])
            live = tmp / 'astrbot' / 'data' / 'plugin_data' / 'astrbot_plugin_ams_life'
            code, out, err = run('--src', str(src), '--dst', str(live))
            self.assertEqual(code, 2)
            self.assertIn('refusing', err)
            self.assertFalse(live.exists())


class NoConfig(unittest.TestCase):
    def test_no_api_config_still_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            src = src_at(tmp, config=False)
            dst = tmp / 'new' / 'data'
            code, out, err = run('--src', str(src), '--dst', str(dst))
            self.assertEqual(code, 0, out + err)
            self.assertIn('没有 Key 文件', out)
            self.assertEqual(files(dst), files(src))


class Source(unittest.TestCase):
    def test_no_astrbot_or_logging_and_no_read_content_is_printed(self):
        tree = ast.parse((ROOT / 'tools' / 'migrate_data.py').read_text('utf-8'))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {alias.name.split('.')[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split('.')[0])
        self.assertNotIn('astrbot', imported)
        self.assertNotIn('logging', imported)
        # A simple check, not a taint analysis: no printed argument is a name that could hold
        # a file's bytes or a key, and nothing is read inside a print call.
        content = {'raw', 'data', 'content', 'text', 'body', 'config', 'key', 'value', 'blob'}
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print'):
                continue
            for arg in node.args:
                for inner in ast.walk(arg):
                    if isinstance(inner, ast.Name):
                        self.assertNotIn(inner.id, content)
                    if isinstance(inner, ast.Call):
                        self.assertNotIn(getattr(inner.func, 'attr', ''), {'read_bytes', 'read_text', 'read'})


if __name__ == '__main__':
    unittest.main()
