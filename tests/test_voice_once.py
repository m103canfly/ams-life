# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Voice and text deduplication on the neutral turn route."""
import asyncio
import math
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import mixin_selfie
import test_turn_runner
import turn_runner


class VoiceOnce(unittest.IsolatedAsyncioTestCase):
    setUp = test_turn_runner.OneTurn.setUp
    close_cached_stores = test_turn_runner.OneTurn.close_cached_stores
    event = test_turn_runner.OneTurn.event

    def prepare(self, url='http://localhost'):
        self.her.config['say_aloud_enabled'] = True
        self.her._embedding_runtime_config = Mock(return_value={'base_url': url})
        self.her._phone_clear = AsyncMock(return_value=True)
        self.her._make_voice = AsyncMock(return_value=Path('voice.wav'))
        self.her._phone_account = Mock()
        self.her._phone_prune = Mock()
        self.her._note_she_sent = Mock()
        self.her._remember = AsyncMock()
        self.her.memory_dedup_embedding = False

    async def run_voice(self, text, voice):
        self.fake.call_tools(('say_aloud', {'text': voice}))
        self.fake.say(text)
        event = self.event()
        with patch.object(mixin_selfie, 'SEND_DELAY', 0):
            await turn_runner.run_turn(self.her, event)
            await asyncio.sleep(0.03)
        return event

    def types(self):
        return [[segment.type for segment in segments] for _, segments in self.sends.sent]

    async def test_similar_meaning_sends_voice_only(self):
        self.prepare()
        self.her._embed_text = AsyncMock(side_effect=[[1, 0], [0.85, math.sqrt(1 - 0.85 ** 2)]])
        event = await self.run_voice('窗边很安静', '这里没有什么声音')
        self.assertTrue(event.is_stopped())
        self.assertEqual(self.types(), [['record']])
        self.her._embed_text.assert_awaited()

    async def test_different_meaning_sends_both(self):
        self.prepare()
        self.her._embed_text = AsyncMock(side_effect=[[1, 0], [0.2, math.sqrt(0.96)]])
        await self.run_voice('我去吃饭', '晚安朋友')
        self.assertEqual(self.types(), [['text'], ['record']])

    async def test_embedding_error_falls_back_to_bigrams(self):
        self.prepare()
        self.her._embed_text = AsyncMock(side_effect=ValueError('offline'))
        self.assertTrue(await mixin_selfie._same_as_voice(self.her, '阳光照在窗边', '阳光照在桌边'))
        self.assertFalse(await mixin_selfie._same_as_voice(self.her, '准备出门散步', '今天吃了苹果'))

    async def test_only_matching_piece_is_dropped(self):
        self.prepare()
        async def vector(text):
            return [1, 0] if text in ('窗边很安静', '这里没有什么声音') else [0, 1]
        self.her._embed_text = AsyncMock(side_effect=vector)
        await self.run_voice('窗边很安静【下一条】我去吃饭', '这里没有什么声音')
        self.assertEqual(self.types(), [['text'], ['record']])
        self.assertEqual(self.sends.sent[0][1][0].data['text'], '我去吃饭')

    async def test_remote_address_uses_bigrams_without_embedding(self):
        self.prepare('https://example.invalid/v1')
        self.her._embed_text = AsyncMock()
        await self.run_voice('阳光照在窗边', '阳光照在桌边')
        self.assertEqual(self.types(), [['record']])
        self.her._embed_text.assert_not_awaited()

    async def test_local_address_calls_fake_embedding(self):
        self.prepare('http://[::1]/v1')
        self.her._embed_text = AsyncMock(side_effect=[[1, 0], [1, 0]])
        await self.run_voice('窗边很安静', '这里没有什么声音')
        self.assertEqual(self.types(), [['record']])
        self.assertEqual(self.her._embed_text.await_count, 2)

    async def test_tool_returns_voice_instruction(self):
        self.prepare()
        self.assertEqual(await self.her._tool_say_aloud(self.event(), '晚安朋友'), mixin_selfie.VOICE_QUEUED)

    async def test_voice_only_is_kept_and_in_next_turn_history(self):
        self.prepare()
        self.her._embed_text = AsyncMock()
        event = await self.run_voice('窗边很安静', '窗边很安静')
        rows = self.store.recent('group:900001')
        self.assertEqual([row['role'] for row in rows], ['user', 'assistant'])
        self.assertIn(event.incoming.text, rows[0]['content'])
        self.assertEqual(rows[1]['content'], '[语音] 窗边很安静')
        self.fake.say('知道了')
        await turn_runner.run_turn(self.her, self.event())
        messages = self.fake.requests[-1]['messages']
        self.assertIn({'role': 'user', 'content': rows[0]['content']}, messages)
        self.assertIn({'role': 'assistant', 'content': '[语音] 窗边很安静'}, messages)

    async def test_unsent_voice_is_not_kept(self):
        self.prepare()
        self.her._embed_text = AsyncMock()
        self.her._phone_clear.return_value = False
        await self.run_voice('窗边很安静', '窗边很安静')
        self.assertEqual(self.store.recent('group:900001'), [])
        self.her._phone_clear.return_value = True
        self.sends.fail = True
        await self.run_voice('窗边很安静', '窗边很安静')
        self.assertEqual(self.store.recent('group:900001'), [])
