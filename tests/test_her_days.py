# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her local activities, notebook sections and deleted notes."""
import datetime
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import forget_registry
import harness
import her_days
import interpretation
import mixin_discretion
import mixin_llm


class HerDays(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = her_days.Store(self.root)

    def add(self, day, person='10003'):
        ts = datetime.datetime(2026, 11, day, 12).timestamp()
        return self.store.add({'ts': ts, 'do': '做' * 20, 'detail': '细' * 50,
                               'feel': '好' * 50, 'liked': '喜欢' * 15,
                               'minutes': 15, 'related_users': [person]})

    def test_days_recent_and_limits(self):
        first, second, third = self.add(1), self.add(2), self.add(2, '10005')
        self.assertEqual(self.store.day('2026-11-01'), [first])
        self.assertEqual(self.store.recent(3), [third, second, first])
        self.assertEqual(self.store.recent(0), [])
        self.assertEqual([len(first[x]) for x in ('do', 'detail', 'feel', 'liked')], [12, 40, 40, 20])
        self.assertEqual(first['origin']['where'], 'self')

    def test_set_liked_and_forget(self):
        first, second = self.add(1), self.add(2, '10005')
        self.assertTrue(self.store.set_liked(first['id'], '很' * 30))
        self.assertEqual(self.store.day('2026-11-01')[0]['liked'], '很' * 20)
        self.assertFalse(self.store.set_liked('missing', 'x'))
        self.assertEqual(self.store.forget('10003'), 1)
        self.assertEqual(self.store.recent(3), [second])

    def test_sections(self):
        entries = [{'section': name} for name in her_days.SECTIONS] + [{}, {'section': 'other'}]
        sections = her_days.notebook_sections(entries)
        for name, entry in zip(her_days.SECTIONS, entries):
            self.assertEqual(sections[name], [entry])
        self.assertEqual(sections['未分'], entries[-2:])

    def test_forget_wiring_and_failure(self):
        self.add(1)
        plugin = test_basics.make_plugin(harness.FakeContext())
        plugin._forget_reg = forget_registry.ForgetRegistry()
        self.addCleanup(plugin._forget_reg.close)
        with patch.object(mixin_discretion, 'DATA_DIR', self.root):
            plugin._forget(person='10003')
        self.assertEqual(self.store.recent(5), [])
        with patch.object(mixin_discretion.her_days.Store, 'forget', side_effect=OSError('private details')):
            with patch.object(mixin_discretion.logger, 'warning') as warning, \
                    patch.object(plugin, '_history_store') as history:
                result = plugin._forget(person='10003')
        self.assertIn('her days delete failed', warning.call_args_list[0].args[0])
        history.return_value.forget_person.assert_called_once_with('10003')
        self.assertIn('memories', result)


class NotebookArchive(unittest.IsolatedAsyncioTestCase):
    async def test_forget_message_removes_only_matching_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            origin = {'where': 'group:900001', 'people': ['10003'], 'source_ids': ['msg-1'], 'visibility': 'public'}
            entries = [{'id': 'n1', 'origin': origin},
                       {'id': 'n2', 'origin': dict(origin, source_ids=['msg-2'])}]
            her_days.archive_notebook(root, entries, 42)
            plugin = test_basics.make_plugin(harness.FakeContext())
            with patch.object(mixin_discretion, 'DATA_DIR', root):
                plugin._forget(source_ids=['msg-1'])
            rows = [json.loads(line) for line in (root / 'notebook_archive.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(rows, [dict(entries[1], deleted_at=42)])

    async def test_existing_overflow_is_archived(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plugin = test_basics.make_plugin(harness.FakeContext())
            origin = {'where': 'self', 'people': [], 'source_ids': [], 'visibility': 'self'}
            entries = [{'id': 'n%d' % i, 'text': 'note %d' % i, 'ts': i, 'origin': origin}
                       for i in range(mixin_llm.NOTEBOOK_MAX + 1)]
            plugin.self_model['notebook'] = entries.copy()
            plugin._notebook_time_reached = lambda now: True
            plugin._notebook_night = lambda now: {'tried': [], 'changes': 0}
            plugin._notebook_sittings = lambda now: ['group']
            plugin._notebook_materials = lambda core, sitting, now: []
            plugin._core = lambda event: None
            plugin._persona_text = AsyncMock(return_value='')
            plugin._llm_v2_call = AsyncMock(return_value=[{'op': 'edit', 'no': 1, 'text': 'edited'}])
            plugin._job_stale = lambda: False
            plugin._sitting_origin = lambda sitting, materials: origin
            plugin._save_self_model = lambda: None
            with patch.object(mixin_llm, 'DATA_DIR', root):
                self.assertTrue(await plugin._maybe_write_notebook(now=42))
            self.assertEqual(len(plugin.self_model['notebook']), mixin_llm.NOTEBOOK_MAX)
            self.assertEqual(plugin.self_model['notebook'][0]['text'], 'edited')
            archive = json.loads((root / 'notebook_archive.jsonl').read_text(encoding='utf-8'))
            self.assertEqual(archive, dict(entries[-1], deleted_at=42))

    async def test_delete_archives_and_forget_removes_origin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plugin = test_basics.make_plugin(harness.FakeContext())
            origin = {'where': 'group:900001', 'people': ['10003'], 'source_ids': [], 'visibility': 'public'}
            entry = {'id': 'n1', 'text': '旧的一条', 'ts': 12, 'origin': origin, 'section': '习惯'}
            plugin.self_model['notebook'] = [entry]
            plugin._notebook_time_reached = lambda now: True
            plugin._notebook_night = lambda now: {'tried': [], 'changes': 0}
            plugin._notebook_sittings = lambda now: ['group']
            plugin._notebook_materials = lambda core, sitting, now: []
            plugin._core = lambda event: None
            plugin._persona_text = AsyncMock(return_value='')
            plugin._llm_v2_call = AsyncMock(return_value=[{'op': 'delete', 'no': 1}])
            plugin._job_stale = lambda: False
            plugin._sitting_origin = lambda sitting, materials: origin
            plugin._save_self_model = lambda: None
            with patch.object(mixin_llm, 'DATA_DIR', root):
                self.assertTrue(await plugin._maybe_write_notebook(now=42))
            prompt = plugin._llm_v2_call.await_args.args[1]
            self.assertEqual(prompt, interpretation.notebook_prompt(
                [(entry['text'], True)], [], False, mixin_llm.NOTEBOOK_MAX,
                mixin_llm.NOTEBOOK_CHARS, mixin_llm.NOTEBOOK_EDITS))
            self.assertEqual(plugin.self_model['notebook'], [])
            path = root / 'notebook_archive.jsonl'
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), dict(entry, deleted_at=42))
            other = dict(entry, id='n2', origin=dict(origin, people=['10005']))
            her_days.archive_notebook(root, [other], 43)
            plugin._forget_reg = forget_registry.ForgetRegistry()
            self.addCleanup(plugin._forget_reg.close)
            with patch.object(mixin_discretion, 'DATA_DIR', root):
                plugin._forget(person='10003')
            self.assertEqual([json.loads(x)['id'] for x in path.read_text(encoding='utf-8').splitlines()], ['n2'])
