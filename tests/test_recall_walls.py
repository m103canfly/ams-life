# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks of text placed in the reply recall sections."""
import asyncio
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import discretion
import harness
import main
import mixin_discretion


class RecallWalls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.users = Path(self.temp.name)
        self.user_patch = patch.object(mixin_discretion, 'USER_DIR', self.users)
        self.user_patch.start()
        self.addCleanup(self.user_patch.stop)
        self.plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        self.plugin._known_names = lambda people: list(people) + ['Alice']
        self.plugin._known_numbers = lambda: {'10001', '900001'}
        self.plugin._present_people = lambda event: set()
        self.plugin._bump_event_recall = lambda ids: None
        self.plugin._forbid_names = lambda *args: None
        self.plugin._forbid = lambda *args: None
        self.private = discretion.make_origin('private:10001', ['10001'])
        self.group = discretion.make_origin('group:900001', ['10001'])

    def event(self, group=None, sender='10001'):
        return harness.FakeEvent('hello', sender=sender, group=group)

    def sections(self, origin, event, global_memory):
        p = self.plugin
        p.global_memory = global_memory
        note = {'id': 'n', 'origin': origin, 'text': 'Alice 10001 蓝鲸三号摘要'}
        ev = {'id': 'e', 'origin': origin, 'title': '蓝鲸三号标题',
              'central_details': 'Alice 10001 蓝鲸三号正文', 'meaning_to_her': '蓝鲸三号意义'}
        memory = {'id': 'm', 'origin': origin, 'text': 'Alice 10001 蓝鲸三号记忆',
                  'vector': [1.0], 'sender_id': '10001'}
        p.self_model = {'notebook': [note]}
        p._event_archive = lambda count: [ev]
        p._cross_session_memory_entries = lambda event: [('other', memory)]
        p._cosine = lambda a, b: 1.0
        p._memory_score = lambda *args, **kwargs: 1.0
        if global_memory:
            notes = p._labeled_notebook(event)
            memories = p._labeled_elsewhere(event, [1.0], None, [])[0]
        else:
            notes = p._notebook_for(event)
            memories = []  # The same permission is used by the non-global memory path.
        return '\n'.join(notes) + '\n' + p._event_context(event) + '\n' + '\n'.join(memories)

    def test_private_text_and_summary_stay_in_owner_chat(self):
        for enabled in (False, True):
            for event in (self.event('900001'), self.event('900002'), self.event(sender='10003')):
                output = self.sections(self.private, event, enabled)
                self.assertNotIn('蓝鲸三号', output)
            self.assertIn('蓝鲸三号', self.sections(self.private, self.event(), enabled))

    def test_public_anonymous_members_and_shared_groups(self):
        for enabled in (False, True):
            output = self.sections(self.group, self.event('900002'), enabled)
            self.assertIn('蓝鲸三号', output)
            self.assertNotIn('Alice', output)
            self.assertNotIn('10001', output)
            output = self.sections(self.group, self.event(sender='10003'), enabled)
            self.assertNotIn('Alice', output)
            (self.users / '10003.json').write_text(json.dumps({'sessions': ['group:900001']}), encoding='utf-8')
            self.assertIn('Alice', self.sections(self.group, self.event(sender='10003'), enabled))
            (self.users / '10003.json').unlink()
            self.plugin.config['shared_groups'] = [['900001', '900002']]
            self.assertIn('Alice', self.sections(self.group, self.event('900002'), enabled))
            self.assertNotIn('Alice', self.sections(self.group, self.event('900003'), enabled))
            self.plugin.config['shared_groups'] = []

    def test_self_web_and_merged_sources(self):
        for origin in (discretion.make_origin('self'), discretion.make_origin('web:example')):
            self.assertEqual(discretion.may_recall(origin, 'group:900002'), discretion.SAY)
        merged = discretion.merge([self.private, self.group])
        self.assertEqual(merged['where'], 'private:10001')
        self.assertEqual(discretion.may_recall(merged, 'group:900001'), discretion.DROP)
        self.assertEqual(discretion.may_recall(merged, 'private:10001'), discretion.ANON)
        self.assertEqual(discretion.may_recall(merged, 'private:10001', member_of=lambda person, group: True),
                         discretion.SAY)
        self.assertIn('蓝鲸三号', self.sections(merged, self.event(), True))
        self.assertNotIn('蓝鲸三号', self.sections(merged, self.event('900001'), True))

    def test_merged_public_groups_use_strictest_permission(self):
        other = discretion.make_origin('group:900002', ['10003'])
        merged = discretion.merge([self.group, other])
        for place in ('group:900001', 'group:900002', 'group:900003'):
            self.assertEqual(discretion.may_recall(merged, place), discretion.ANON)
            text = self.sections(merged, self.event(place.split(':')[1]), True)
            self.assertIn('蓝鲸三号', text)
            self.assertNotIn('Alice', text)
        self.plugin.config['shared_groups'] = [['900001', '900002']]
        for group in ('900001', '900002'):
            self.assertEqual(discretion.may_recall(merged, 'group:' + group,
                                                   shared=self.plugin.config['shared_groups']), discretion.SAY)
            self.assertIn('Alice', self.sections(merged, self.event(group), True))

    def test_merged_private_and_group_membership(self):
        merged = discretion.merge([self.private, self.group])
        output = self.sections(merged, self.event(), True)
        self.assertIn('蓝鲸三号', output)
        self.assertNotIn('Alice', output)
        (self.users / '10001.json').write_text(json.dumps({'sessions': ['group:900001']}), encoding='utf-8')
        self.assertIn('Alice', self.sections(merged, self.event(), True))
        for group in ('900001', '900002'):
            self.assertNotIn('蓝鲸三号', self.sections(merged, self.event(group), True))

    def test_membership_file_is_read_once_per_turn(self):
        (self.users / '10003.json').write_text(json.dumps({'sessions': ['group:900001']}), encoding='utf-8')
        event = self.event(sender='10003')
        original = Path.read_text
        calls = []
        def read(path, *args, **kwargs):
            calls.append(path)
            return original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', read):
            for _ in range(4):
                self.assertEqual(mixin_discretion.recall_permission(self.plugin, {'origin': self.group}, event),
                                 discretion.SAY)
        self.assertEqual(len(calls), 1)

    def test_private_not_in_prompt_but_send_check_stops_leak(self):
        p = self.plugin
        p._forbid = type(p)._forbid.__get__(p)
        p._cross_session_memory_entries = lambda event: [('private', {
            'id': 'secret', 'origin': self.private, 'text': '我的暗号是蓝鲸三号',
            'vector': [1.0], 'sender_id': '10001'})]
        p._cosine = lambda *args: 1.0
        p._memory_score = lambda *args, **kwargs: 1.0
        event = self.event('900001', sender='10003')
        lines, _, _ = p._labeled_elsewhere(event, [1.0], None, [])
        self.assertNotIn('蓝鲸三号', '\n'.join(lines))
        async def no_vector(*args):
            return None
        async def no_redo(*args):
            return None
        p._embed_text = no_vector
        p._redo_reply = no_redo
        p._common_pieces = lambda: set()
        p._count_check = lambda *args: None
        p._set_reply = lambda *args: None
        sent = asyncio.run(p._look_at_reply(event, object(), '蓝鲸三号'))
        self.assertEqual(sent, '')

    def test_private_event_and_note_are_forbidden_without_being_shown(self):
        p = self.plugin
        p._forbid = type(p)._forbid.__get__(p)
        event = self.event('900001', sender='10003')
        p.self_model = {'notebook': [{'id': 'n', 'origin': self.private, 'text': '蓝鲸三号笔记'}]}
        archive = [{'id': 'e', 'origin': self.private, 'title': '蓝鲸三号标题',
                    'central_details': '蓝鲸三号正文', 'meaning_to_her': '蓝鲸三号意义'}]
        self.assertEqual(p._labeled_notebook(event), [])
        self.assertEqual(p._labeled_event_context(event, archive), '')
        forbidden = p._check_note(event)['forbidden']
        self.assertEqual({item['id'] for item in forbidden}, {'note:n', 'event:e'})
        self.assertTrue(all(item['private'] for item in forbidden))

    def test_blocked_event_does_not_use_a_slot(self):
        p = self.plugin
        p.global_memory = True
        entries = [{'id': 'private', 'origin': self.private, 'central_details': 'secret', 'importance': 9}]
        entries += [{'id': str(i), 'origin': self.group, 'central_details': 'visible' + str(i),
                     'importance': 4 - i} for i in range(4)]
        p._event_archive = lambda count: entries
        result = p._event_context(self.event('900001'))
        for i in range(3):
            self.assertIn('visible' + str(i), result)
        self.assertNotIn('secret', result)

    def test_memory_prompt_filters_and_fills_slots(self):
        p = self.plugin
        p._usable_memory_text = lambda text: True
        p._schedule_consolidation = lambda *args: None
        p._save_memory = lambda *args: None
        p._memory_top_k = lambda *args: 3
        p._cosine = lambda *args: 0.8
        p._memory_score = lambda *args, **kwargs: 1.0
        p._cross_session_memory_entries = lambda event: []
        p._restabilize_if_expired = lambda *args: False
        p._chain_event_lines = lambda *args, **kwargs: []
        entries = [{'id': 'private', 'origin': self.private, 'text': '蓝鲸三号摘要',
                    'vector': [1.0], 'importance': 1.0}]
        entries += [{'id': str(i), 'origin': self.group, 'text': 'visible' + str(i),
                     'vector': [1.0], 'importance': 1.0} for i in range(4)]
        p._load_memory = lambda event: {'entries': entries}
        for enabled in (False, True):
            p.global_memory = enabled
            output = asyncio.run(p._memory_recall(self.event('900001'), 'visible', vec=[1.0]))
            self.assertNotIn('蓝鲸三号', output)
            self.assertEqual(sum('visible' in line for line in output.splitlines()), 3, output)
