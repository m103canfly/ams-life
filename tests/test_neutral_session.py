# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Neutral session identities in event and provenance storage."""
import asyncio
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import common
import harness
import mixin_events
import mixin_memory
from astrbot.api import logger


class NeutralSession(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=test_basics.DATA)
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name) / 'archives'
        for module in (mixin_events, mixin_memory):
            for name, path in (('EVENT_ARCHIVE_DIR', root), ('EVENT_ARCHIVE_PATH', root / 'events.jsonl'),
                               ('EVENT_SESSION_DIR', root / 'sessions')):
                p = patch.object(module, name, path)
                p.start()
                self.addCleanup(p.stop)
        p = patch.object(mixin_memory, 'INSIGHT_ARCHIVE_PATH', root / 'insights.jsonl')
        p.start()
        self.addCleanup(p.stop)
        self.plugin = test_basics.make_plugin(harness.FakeContext())
        self.event = harness.FakeEvent('A fictional event happened', group='900001')
        self.root = root

    def test_canonical_session_key(self):
        for value in ('default:GroupMessage:1', 'default_GroupMessage_1', 'group:1'):
            self.assertEqual(common.canonical_session_key(value), 'group:1')
        for value in ('default:FriendMessage:10001', 'default_TempMessage_10001'):
            self.assertEqual(common.canonical_session_key(value), 'private:10001')
        self.assertEqual(common.canonical_session_key(''), '')

    def archive_ranked(self):
        entry = {'text': 'A fictional event happened', 'importance': 1.0, 'ts': time.time(),
                 'provenance': self.plugin._memory_provenance(self.event)}
        with patch.object(self.plugin, '_segment_event_rows', return_value=[[(entry['text'], entry)]]), \
             patch.object(self.plugin, '_event_worthiness_for', return_value=None), \
             patch.object(self.plugin, '_embedding_for', new_callable=AsyncMock, return_value=[]):
            asyncio.run(self.plugin._archive_ranked_events_deterministic(self.event, None, [entry]))
        self.assertTrue((self.root / 'sessions' / 'group_900001' / 'events.jsonl').exists(), logger.records[-5:])

    def test_event_and_provenance_written_to_neutral_folder(self):
        self.archive_ranked()
        path = self.root / 'sessions' / 'group_900001' / 'events.jsonl'
        rows = [json.loads(line) for line in path.read_text('utf-8').splitlines()]
        self.assertEqual(rows[0]['session'], 'group:900001')
        self.assertEqual(rows[0]['provenance']['session'], 'group:900001')
        self.assertEqual(rows[0]['provenance']['sources'][0]['session'], 'group:900001')

    def test_legacy_event_chain_matches_neutral_place(self):
        self.plugin.memory_chain_enabled = True
        rows = [{'id': 'seed', 'session': 'default:GroupMessage:900001', 'title': 'seed',
                 'ts': time.time(), 'chain_links': [{'id': 'target', 'weight': 1, 'ts': time.time()}]},
                {'id': 'target', 'session': 'default:GroupMessage:900001', 'title': 'linked', 'ts': time.time()}]
        with patch.object(self.plugin, '_event_archive', return_value=rows):
            self.assertIn('linked', self.plugin._chain_event_lines('group:900001', 'seed')[0])

    def test_digest_window_uses_place_even_with_umo(self):
        now = time.time()
        day = time.strftime('%Y-%m-%d', time.localtime(now))
        line = {'ts': now, 'role': 'user', 'sender_id': '10001', 'sender_name': 'Alice',
                'text': 'A fictional event happened', 'msg_id': 'm1'}
        item = {'title': 'An event', 'what': 'A fictional event happened', 'who': [], 'lines': [1],
                'who_ok': False, 'lines_ok': True}
        with patch.object(self.plugin, '_read_window', return_value={'recent': [line], 'umo': self.event.unified_msg_origin}), \
             patch.object(self.plugin, '_material_names', return_value={}), \
             patch.object(self.plugin, '_save_self_model'), \
             patch.object(self.plugin, '_llm_v2_call', new_callable=AsyncMock, return_value=[item]), \
             patch.object(self.plugin, '_find_any_duplicate_event', return_value=None), \
             patch.object(self.plugin, '_append_event_archive') as write:
            result = asyncio.run(self.plugin._digest_window('group:900001', day, {'tried': []}, now))
        self.assertEqual(result['written'], 1)
        self.assertEqual(write.call_args.args[0]['session'], 'group:900001')

    def test_memory_deletion_redacts_neutral_event_file(self):
        text = 'A fictional event happened'
        self.plugin._append_event_archive({'id': 'event1', 'session': 'group:900001',
                                           'event': text, 'source_texts': [text]})
        path = self.root / 'sessions' / 'group_900001' / 'events.jsonl'
        self.plugin._propagate_memory_deletion(self.event, {'id': 'memory1', 'text': text}, {'entries': []})
        self.assertNotIn(text, path.read_text('utf-8'))

    def test_ranked_event_deduplicates_in_neutral_folder(self):
        self.archive_ranked()
        path = self.root / 'sessions' / 'group_900001' / 'events.jsonl'
        self.assertEqual(len(path.read_text('utf-8').splitlines()), 1)
        # Force lookup to rely on the session folder rather than the global archive.
        with patch.object(self.plugin, '_event_archive', return_value=[]):
            self.archive_ranked()
        self.assertEqual(len(path.read_text('utf-8').splitlines()), 1)

    def test_no_direct_session_write_from_astrbot_origin(self):
        for name in ('mixin_events.py', 'mixin_memory.py', 'mixin_digest.py'):
            source = (Path(__file__).resolve().parent.parent / name).read_text('utf-8')
            self.assertNotRegex(source, r'"session"\s*:\s*[^\n]*unified_msg_origin')


if __name__ == '__main__':
    unittest.main()
