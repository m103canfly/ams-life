# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""History forgetting through the plugin's discretion mixin."""
import tempfile
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # prepares the offline harness
import forget_registry
import history_store
import mixin_discretion as md


class Plugin(md.DiscretionMixin):
    def __init__(self):
        self.self_model = {}
        self.library = {'entries': [], 'rooms': {}}
        self._forget_reg = forget_registry.ForgetRegistry()

    def _group_forget_queue(self, *args): pass
    def _forget_recent_images(self, *args): pass
    def _known_names(self, *args): return []
    def _read_library(self): return self.library
    def _write_library(self, lib): self.library = lib; return True
    def _window_places(self): return []
    def _forget_pictures(self, *args): return 0
    def _forget_pictures_of(self, *args): return 0
    def _forget_dedupe_rows(self, *args): pass
    def _refresh_loop_pressure(self, *args): pass
    def _core(self, *args): return None


class ForgetHistory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        paths = {name: root / name for name in
                 ('EVENT_ARCHIVE_PATH', 'INSIGHT_ARCHIVE_PATH', 'EVENT_SESSION_DIR', 'USER_DIR')}
        self.patch = patch.multiple(md, **paths)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.plugin = Plugin()
        self.addCleanup(self.plugin._forget_reg.close)
        self.path = root / 'history.sqlite3'

    def history(self):
        store = history_store.HistoryStore(self.path, gate=self.plugin._history_gate)
        self.addCleanup(store.close)
        self.plugin._history = store
        return store

    def memory(self):
        self.plugin.library['entries'] = [{'id': 'entry-1', 'text': 'memory',
            'origin': {'where': 'group:900001', 'people': ['10001'], 'source_ids': ['m-1']}}]

    def test_without_history_keeps_existing_counts(self):
        self.memory()
        result = self.plugin._forget(person='10001')
        self.assertEqual(result, {'memories': 1, 'events': 0, 'relationship': 0, 'notes': 0,
                                  'phone': 0, 'insights': 0, 'pictures': 0,
                                  'places': ['group:900001']})

    def test_forget_person_removes_speech_and_replies(self):
        store = self.history()
        store.append('group:900001', 'user', 'first', sender_id='10001')
        store.append('group:900001', 'assistant', 'reply first', about=['10001'])
        store.append('group:900001', 'user', 'second', sender_id='10003')
        store.append('group:900001', 'assistant', 'reply second', about=['10003'])
        self.assertEqual(self.plugin._forget(person='10001')['history'], 2)
        self.assertEqual([row['content'] for row in store.recent('group:900001')], ['second', 'reply second'])

    def test_forget_message_removes_message_and_reply(self):
        store = self.history()
        store.append('group:900001', 'user', 'first', message_id='m-1')
        store.append('group:900001', 'assistant', 'reply', sources=['m-1'])
        store.append('group:900001', 'user', 'other', message_id='m-2')
        self.assertEqual(self.plugin._forget(source_ids=['m-1'])['history'], 2)
        self.assertEqual([row['content'] for row in store.recent('group:900001')], ['other'])

    def test_entry_ids_leave_history_alone(self):
        store = self.history()
        store.append('group:900001', 'user', 'first', sender_id='10001', message_id='m-1')
        self.memory()
        result = self.plugin._forget(entry_ids=['entry-1'])
        self.assertEqual(result['memories'], 1)
        self.assertEqual(result['history'], 0)
        self.assertEqual(len(store.recent('group:900001')), 1)

    def test_gate_checks_people_sources_and_message_id(self):
        store = self.history()
        reg = self.plugin._forget_reg
        reg.forget_person('10003')
        reg.forget_message('m-9')
        self.assertEqual(store.append('group:900001', 'user', 'blocked', sender_id='10003'), 0)
        self.assertEqual(store.append('group:900001', 'assistant', 'blocked source', sources=['m-9']), 0)
        self.assertEqual(store.append('group:900001', 'user', 'blocked id', message_id='m-9'), 0)
        self.assertGreater(store.append('group:900001', 'user', 'allowed', sender_id='10001'), 0)
        self.assertEqual(len(store.recent('group:900001')), 1)

    def test_unreadable_registry_blocks_write(self):
        store = self.history()
        with patch.object(self.plugin, '_registry_sets', side_effect=OSError('unreadable')):
            self.assertEqual(store.append('group:900001', 'user', 'blocked'), 0)
        self.assertEqual(store.recent('group:900001'), [])

    def test_history_error_does_not_block_other_deletes(self):
        class BrokenStore:
            def forget_person(self, person): raise OSError('history unavailable')

        self.plugin._history = BrokenStore()
        self.memory()
        result = self.plugin._forget(person='10001')
        self.assertEqual(result['memories'], 1)
        self.assertEqual(self.plugin.library['entries'], [])


if __name__ == '__main__':
    unittest.main()
