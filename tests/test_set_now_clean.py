# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for shared now state."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import mixin_selfie as phone
from test_selfie import Event, Phone


class SetNowClean(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'now.json'
        self.path_patch = patch.object(phone, 'NOW_PATH', self.path)
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)
        self.p = Phone()
        self.private = Event()

    def state(self):
        return json.loads(self.path.read_text(encoding='utf-8'))

    async def test_reject_sensitive_original_and_store_place(self):
        for where, doing in [('和10002在一起', '看 https://x.example'),
                             ('和10002在一起', '排队'), ('便利店', '看 HTTPS://x.example'),
                             ('www.example', '排队'), ('便利店', '看 x://y'),
                             ('便利店', '@某人')]:
            with self.subTest(where=where, doing=doing):
                self.assertEqual(await self.p._tool_set_now(self.private, where, doing), '不能这样写')
                self.assertFalse(self.path.exists())
        self.assertEqual(await self.p._tool_set_now(self.private, '便利店', '排队'), '记下了')
        self.assertEqual(self.state()['place'], self.p._here(self.private) if hasattr(self.p, '_here')
                         else phone.adapter_astrbot_turn.incoming_of(self.private).place)

    async def test_names_removed_and_empty_rejected(self):
        self.p._browse_names = lambda: ['虚构名字']
        self.assertEqual(await self.p._tool_set_now(self.private, '和虚构名字散步', '走路'), '记下了')
        self.assertNotIn('虚构名字', self.state()['where'])
        before = self.path.read_bytes()
        self.assertEqual(await self.p._tool_set_now(self.private, '虚构名字', '走路'), '不能这样写')
        self.assertEqual(self.path.read_bytes(), before)

    async def test_long_text_rejected(self):
        self.assertEqual(await self.p._tool_set_now(self.private, '地' * 13, '走路'), '不能这样写')
        self.assertFalse(self.path.exists())

    async def test_private_state_is_clean_in_group(self):
        self.p._browse_names = lambda: ['虚构名字']
        self.assertEqual(await self.p._tool_set_now(self.private, '和虚构名字散步', '走路'), '记下了')
        group = Event()
        group.unified_msg_origin = 'default:GroupMessage:900001'
        line = self.p._now_line(group)
        self.assertIn('散步', line)
        self.assertNotIn('虚构名字', line)
        self.assertNotIn(self.state()['place'], line)

    async def test_photo_rejects_without_queue_and_cleans_names(self):
        self.p._browse_names = lambda: ['虚构名字']
        for where, doing in [('10002', '走路'), ('便利店', 'http://x.example'),
                             ('虚构名字', '走路'), ('地' * 13, '走路')]:
            self.assertEqual(await self.p._tool_take_photo(self.private, 'snap', '天空', where, doing, ''), '不能拍这张')
            self.assertFalse(self.path.exists())
            self.assertNotIn('photo', self.p._phone_queue(self.private))
        self.assertEqual(await self.p._tool_take_photo(self.private, 'snap', '天空', '和虚构名字散步', '走路', ''),
                         phone.PHOTO_QUEUED)
        self.assertNotIn('虚构名字', self.state()['where'])
