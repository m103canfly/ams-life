# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for the reply piece guidance and limit."""
import asyncio
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402

import adapter_astrbot_turn as adapter
import attention
import harness
import main
from astrbot.api.provider import ProviderRequest


NOTE = '绝大多数时候只写一段（发一条）。只有在确有必要时才可以分段（最多不超过 10段）。一段里别换行。'


class FewerPiecesTests(unittest.TestCase):
    def test_note_matches_owner_words(self):
        self.assertEqual(attention.PIECES_NOTE, NOTE)

    def test_split_at_ten(self):
        pieces = [str(i) for i in range(12)]
        self.assertEqual(attention.split('【下一条】'.join(pieces[:10])), pieces[:10])
        self.assertEqual(attention.split('【下一条】'.join(pieces)), pieces[:9] + ['9 10 11'])

    def test_prepare_turn_includes_new_note(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={})
        test_basics.PLUGINS.append(plugin)
        event = harness.FakeEvent('hello', sender='10001', group='900001')
        req = ProviderRequest(prompt='hello')
        req.extra_user_content_parts = []
        converted = adapter.request_from_astrbot(req)
        asyncio.run(plugin._prepare_turn(event, converted))
        prompt = '\n'.join(part.get('text', '') for part in converted.extra_user_content_parts)
        self.assertIn(NOTE, prompt)
        self.assertNotIn('最多 5 条', prompt)
