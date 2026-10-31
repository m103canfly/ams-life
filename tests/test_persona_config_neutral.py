# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The new program's persona and its config write-back (move 5e-4a).

`_persona_text` answers from `_neutral_persona` when the new program set it, and
`_persist_plugin_config` writes `config.json` through `app_config` when the new program set
`_config_path`. Neither is set on AstrBot, where both methods must behave exactly as at
97faf6e; the frozen `_persona_text` is copied here for the comparison. Every file is built in
this test's own temporary folder and every persona text is made up.
"""
import asyncio
import ast
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import app_config
import harness
import main
import mixin_llm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


# mixin_llm.py 66-85 at 97faf6e.
OLD_PERSONA_TEXT = '''\
async def old_persona_text(self, event):
    try:
        pm = self.context.persona_manager
        _pid = str(getattr(self, "persona_id", "") or self.config.get("persona_id") or "").strip()
        if _pid:
            try:
                _p = pm.get_persona_v3_by_id(_pid)
            except Exception:
                _p = None
            if _p:
                if isinstance(_p, dict):
                    return str(_p.get("prompt") or _p.get("system_prompt") or "")
                return str(getattr(_p, "prompt", "") or getattr(_p, "system_prompt", "") or "")
        p = await pm.get_default_persona_v3(getattr(event, "unified_msg_origin", None))
        if isinstance(p, dict):
            return str(p.get("prompt") or p.get("system_prompt") or "")
        return str(getattr(p, "prompt", "") or getattr(p, "system_prompt", "") or "")
    except Exception as exc:
        logger.warning("[biocore] persona read failed: %s", exc)
        return ""
'''
_old_namespace = dict(vars(mixin_llm))
exec(OLD_PERSONA_TEXT, _old_namespace)
old_persona_text = _old_namespace['old_persona_text']

# A made-up schema, so no real setting is read or written.
SCHEMA = {
    'is_on': {'description': 'a switch', 'type': 'bool', 'default': False},
    'count': {'description': 'a count', 'type': 'int', 'default': 3},
}


class Manager:
    """AstrBot's persona management, giving back what the case asked for or raising."""

    def __init__(self, by_id=None, default=None):
        self.by_id, self.default = by_id, default

    def get_persona_v3_by_id(self, pid):
        if isinstance(self.by_id, Exception):
            raise self.by_id
        return self.by_id

    async def get_default_persona_v3(self, umo=None):
        if isinstance(self.default, Exception):
            raise self.default
        return self.default


class Config(dict):
    """An AstrBot configuration object: a dict with one of the two savers."""

    def __init__(self, async_saver=False, sync_saver=False):
        super().__init__()
        self.calls = []
        if async_saver:
            self.save_config_async = self._async_saver
        if sync_saver:
            self.save_config = self._sync_saver

    async def _async_saver(self, updates):
        self.calls.append(('async', dict(updates)))

    def _sync_saver(self, updates):
        self.calls.append(('sync', dict(updates)))


def new_plugin(config=None):
    plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
    plugin.config = {} if config is None else config
    plugin.context = harness.FakeContext()
    return plugin


class PersonaText(unittest.TestCase):
    """1. The new program's persona, and AstrBot's path beside it."""

    def test_the_new_program_reads_her_own_persona(self):
        plugin = new_plugin()
        manager = Mock()
        for name in ('get_persona_v3_by_id', 'get_default_persona_v3'):
            getattr(manager, name).side_effect = AssertionError('AstrBot was asked')
        plugin.context.persona_manager = manager
        plugin._neutral_persona = '编的人设'
        self.assertEqual(asyncio.run(plugin._persona_text(None)), '编的人设')
        plugin._neutral_persona = ''
        self.assertEqual(asyncio.run(plugin._persona_text(None)), '')
        self.assertEqual(manager.mock_calls, [])   # her persona is never asked of AstrBot

    def test_the_astrbot_persona_path_is_unchanged(self):
        event = harness.FakeEvent('hello', sender='10001', name='Alice', group='900001')
        cases = (
            ('a dict from the default persona', {}, Manager(default={'prompt': '编的人设一'}),
             '编的人设一'),
            ('a dict by id', {'persona_id': 'p1'},
             Manager(by_id={'prompt': '编的人设二'}), '编的人设二'),
            ('a system prompt by id', {'persona_id': 'p2'},
             Manager(by_id={'system_prompt': '编的人设三'}), '编的人设三'),
            ('an object by id', {'persona_id': 'p3'},
             Manager(by_id=SimpleNamespace(prompt='编的人设四')), '编的人设四'),
            ('an object from the default', {},
             Manager(default=SimpleNamespace(prompt='编的人设五')), '编的人设五'),
            ('an id the manager cannot find', {'persona_id': 'p4'},
             Manager(default={'prompt': '编的人设六'}), '编的人设六'),
            ('an id lookup that fails', {'persona_id': 'p5'},
             Manager(by_id=RuntimeError('gone'), default={'prompt': '编的人设七'}), '编的人设七'),
            ('persona management gone', {}, Manager(default=RuntimeError('gone')), ''),
        )
        for name, config, manager, expected in cases:
            with self.subTest(case=name):
                plugin = new_plugin(config)
                self.assertFalse(hasattr(plugin, '_neutral_persona'))
                plugin.context.persona_manager = manager
                self.assertEqual(asyncio.run(plugin._persona_text(event)), expected)
                self.assertEqual(asyncio.run(old_persona_text(plugin, event)), expected)


class ConfigWriteBack(unittest.TestCase):
    """2. The new program's config.json, and the AstrBot savers beside it."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.path = self.folder / 'config.json'

    def files(self):
        return sorted(p.name for p in self.folder.iterdir())

    def test_the_new_program_writes_config_json(self):
        plugin = new_plugin({'is_on': False, 'count': 3})
        plugin._config_path = str(self.path)
        plugin._config_schema = SCHEMA
        asyncio.run(plugin._persist_plugin_config({'is_on': True}))
        self.assertIs(plugin.config['is_on'], True)
        loaded, problems = app_config.load(self.path, SCHEMA)
        self.assertEqual(problems, [])
        self.assertIs(loaded['is_on'], True)
        self.assertEqual(loaded['count'], 3)
        self.assertEqual(plugin.config['is_on'], loaded['is_on'])

    def test_the_owner_schema_is_used_when_none_was_set(self):
        plugin = new_plugin({'is_on': False})
        plugin._config_path = str(self.path)
        with patch.object(app_config, 'load_schema', return_value=SCHEMA):
            asyncio.run(plugin._persist_plugin_config({'is_on': True}))
        loaded, problems = app_config.load(self.path, SCHEMA)
        self.assertEqual(problems, [])
        self.assertIs(loaded['is_on'], True)

    def test_without_the_new_program_nothing_is_written(self):
        plugin = new_plugin({'is_on': False})
        asyncio.run(plugin._persist_plugin_config({'is_on': True}))
        self.assertFalse(hasattr(plugin, '_config_path'))
        self.assertIs(plugin.config['is_on'], True)   # the memory keeps the change
        self.assertEqual(self.files(), [])

    def test_a_saver_is_still_called_first(self):
        for kind in ('async', 'sync'):
            with self.subTest(saver=kind):
                config = Config(async_saver=kind == 'async', sync_saver=kind == 'sync')
                plugin = new_plugin(config)
                plugin._config_path = str(self.path)
                plugin._config_schema = SCHEMA
                asyncio.run(plugin._persist_plugin_config({'is_on': True}))
                self.assertEqual(config.calls, [(kind, {'is_on': True})])
                self.assertIs(plugin.config['is_on'], True)
                self.assertEqual(self.files(), [])   # the new program's file is not touched

    def test_a_failed_save_is_only_a_warning(self):
        plugin = new_plugin({'is_on': 'not a switch'})   # a made-up value of the wrong type
        plugin._config_path = str(self.path)
        plugin._config_schema = SCHEMA
        asyncio.run(plugin._persist_plugin_config({'count': 4}))
        self.assertEqual(plugin.config['count'], 4)   # the memory keeps the change
        self.assertEqual(self.files(), [])   # the wrong type wrote nothing


class Source(unittest.TestCase):
    """3. The two modules take nothing new from AstrBot."""

    def test_no_new_astrbot_imports(self):
        for name in ('mixin_llm.py', 'mixin_settings.py'):
            with self.subTest(module=name):
                tree = ast.parse((ROOT / name).read_text(encoding='utf-8'))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertNotEqual(alias.name.split('.')[0], 'astrbot')
                    elif isinstance(node, ast.ImportFrom):
                        self.assertNotEqual((node.module or '').split('.')[0], 'astrbot')


if __name__ == '__main__':
    unittest.main()
