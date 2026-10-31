# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check that test databases close before their directory is removed."""
import unittest
import sqlite3
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests import harness


class CloseBeforeDelete(unittest.TestCase):
    def test_exit_cleanup_handles_database_opened_after_module_cleanup(self):
        class Plugin:
            pass

        with tempfile.TemporaryDirectory() as root:
            data = Path(root) / 'data'
            data.mkdir()
            with mock.patch.object(harness, '_cleanup_dirs', []), \
                    mock.patch.object(harness, '_cleanup_registered', False), \
                    mock.patch.object(harness.atexit, 'register') as register, \
                    mock.patch.dict(sys.modules, {'main': SimpleNamespace(BioCorePlugin=Plugin)}):
                harness.register_atexit_data(data)
                harness.register_atexit_data(data)
                register.assert_called_once_with(harness.cleanup_registered_plugin_data)
                harness.cleanup_plugin_data([], data)
                self.assertFalse(data.exists())
                data.mkdir()
                plugin = Plugin()
                plugin._forget_reg = sqlite3.connect(str(data / 'registry.sqlite3'))
                plugin._vectors_db = sqlite3.connect(str(data / 'vectors.sqlite3'))
                registry, vectors = plugin._forget_reg, plugin._vectors_db
                harness.cleanup_registered_plugin_data()
                self.assertFalse(data.exists())
                self.assertIsNone(plugin._forget_reg)
                self.assertIsNone(plugin._vectors_db)
                for db in (registry, vectors):
                    with self.assertRaises(sqlite3.ProgrammingError):
                        db.execute('SELECT 1')

    def test_close_plugin_databases_before_removing_directory(self):
        events = []

        class Store:
            def __init__(self, name):
                self.name = name

            def close(self):
                events.append(self.name)

        plugin = type('Plugin', (), {})()
        plugin._forget_reg = Store('registry')
        plugin._vectors_db = Store('vectors')
        empty = type('Plugin', (), {})()
        with mock.patch.object(harness.shutil, 'rmtree', side_effect=lambda *a, **k: events.append('remove')):
            harness.cleanup_plugin_data([plugin, empty], Path('test-data'))
        self.assertEqual(events, ['registry', 'vectors', 'remove'])
        self.assertIsNone(plugin._forget_reg)
        self.assertIsNone(plugin._vectors_db)
