# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Neutral session identities in people records and dashboard rows."""
import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import common
import harness
import mixin_people


class PeopleSessions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=test_basics.DATA)
        self.addCleanup(self.tmp.cleanup)
        self.users = Path(self.tmp.name)
        user_dir = patch.object(mixin_people, 'USER_DIR', self.users)
        user_dir.start()
        self.addCleanup(user_dir.stop)
        self.plugin = test_basics.make_plugin(harness.FakeContext())
        self.event = harness.FakeEvent('hello', sender='10001', name='Alice', group='900001')
        self.path = self.users / '10001.json'

    def test_group_message_writes_neutral_session(self):
        self.plugin._touch_user(self.event)
        data = json.loads(self.path.read_text(encoding='utf-8'))
        self.assertEqual(data['sessions'][-1], 'group:900001')

    def test_legacy_session_is_replaced_and_moved_to_end(self):
        self.path.write_text(json.dumps({'sessions': ['default:GroupMessage:900001', 'private:10003',
                                                      'group:900001']}), encoding='utf-8')
        self.plugin._touch_user(self.event)
        data = json.loads(self.path.read_text(encoding='utf-8'))
        self.assertEqual(data['sessions'], ['private:10003', 'group:900001'])

    def test_dashboard_normalizes_and_deduplicates_in_first_seen_order(self):
        self.path.write_text(json.dumps({'sessions': ['default:GroupMessage:1', 'group:1',
                                                      'default:FriendMessage:2']}), encoding='utf-8')
        rows = common._relationship_rows(self.users)
        self.assertEqual(rows[0]['sessions'], ['group:1', 'private:2'])

    def test_touch_user_does_not_read_astrbot_origin(self):
        self.assertNotIn('unified_msg_origin', inspect.getsource(mixin_people.PeopleMixin._touch_user))


if __name__ == '__main__':
    unittest.main()
