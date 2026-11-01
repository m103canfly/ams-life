# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The look at a picture says who of a work is in it and what it means, offline.

No network and no model: a fake provider answers with a made-up look, and no file is written.
"""
import asyncio
import base64
import json
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import events
import harness
import interpretation
import mixin_media
import mixin_stickers
import stickers
import turn
import vision

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+'
                       'l0ZkAAAAASUVORK5CYII=')
WHO = '星际旅店的阿蓝'                    # a work and a character that are both made up
ANSWER = {'who': WHO, 'caption': '粉发女孩比 V', 'meaning': '打招呼、开心', 'emotion': '开心',
          'text': '耶', 'kind': 'photo', 'personal': False, 'group_meme': False, 'keep': True}


class Provider:
    """A vision provider that answers with the look it was given, and records the calls."""

    def __init__(self, answer=None):
        self.calls = []
        self.answer = answer

    async def text_chat(self, **kwargs):
        self.calls.append(kwargs)
        answer = self.answer if self.answer is not None else ANSWER
        text = answer if isinstance(answer, str) else json.dumps(answer, ensure_ascii=False)
        return harness.FakeResponse(text)


class FakeLibrary:
    """Only what she keeps: no picture, no folder, no file."""

    def __init__(self):
        self.rows = {}

    def add(self, data, now, source="self", from_qq="", from_where="", look=None, note="", owner_name=""):
        look = look or {}
        sid = "made-up-%d" % (len(self.rows) + 1)
        self.rows[sid] = {"caption": str(look.get("caption") or ""), "kind": str(look.get("kind") or ""),
                          "source": source}
        return sid, ""

    def sweep(self, now, days=stickers.DAYS, cap=stickers.CAP):
        return []


class Her(mixin_media.MediaMixin, mixin_stickers.StickersMixin):
    """The two parts of the plugin these tests need; nothing is started and nothing is written."""


class TheQuestion(unittest.TestCase):
    def test_both_questions_ask_who_and_never_a_real_person(self):
        self.assertIn('"who"', stickers.LOOK_PROMPT)
        for text in (stickers.LOOK_PROMPT, interpretation.image_caption_prompt()):
            for word in ('角色', '像是', '真人'):
                self.assertIn(word, text)
        for word in ('认得出', '认不准', '不认得'):
            self.assertIn(word, stickers.LOOK_PROMPT)

    def test_the_character_is_short_and_a_persons_name_in_a_photo_is_dropped(self):
        long_ = stickers.parse_look(json.dumps({'who': '长' * 60, 'caption': '猫'}, ensure_ascii=False))
        self.assertEqual(long_['who'], '长' * 40)
        photo = stickers.parse_look(json.dumps({'who': WHO, 'caption': '一张证件照',
                                                'kind': 'photo', 'personal': True}, ensure_ascii=False))
        self.assertEqual(photo['who'], '')
        kept = stickers.parse_look(json.dumps({'who': WHO, 'caption': '猫', 'kind': 'sticker',
                                               'personal': True}, ensure_ascii=False))
        self.assertEqual(kept['who'], WHO)      # a work's character, not a real person

    def test_the_line_puts_the_name_first_and_leaves_the_empty_ones_out(self):
        item = stickers.cache_entry('a.png', stickers.parse_look(json.dumps(ANSWER, ensure_ascii=False)),
                                    '10001', 'private:10001', 1)
        line = stickers.look_line(item)
        self.assertTrue(line.startswith(stickers.MATERIAL_LABEL))
        self.assertLess(line.index(WHO), line.index('粉发女孩'))
        for part in ('想表达：打招呼、开心', '情绪：开心', '图上的字：耶'):
            self.assertIn(part, line)
        self.assertEqual(stickers.look_line({'caption': '图里是一只猫'}),
                         stickers.MATERIAL_LABEL + '图里是一只猫')     # an older entry: the caption only
        self.assertEqual(stickers.look_line({}), '')


class LookingAtPictures(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = Her()
        self.plugin.image_llama_server = ''
        self.plugin.image_llama_model = ''
        self.plugin.image_service_port = 0
        self.plugin._here = lambda event: event.incoming.place
        self.plugin._speaker = lambda event: (event.incoming.sender_id, event.incoming.sender_name)
        self.plugin._addresses_her = lambda event: event.incoming.at_me
        self.plugin._sticker_refs = lambda event: []
        self.plugin._job_stale = lambda: False
        self.plugin._may_keep = Mock(return_value=True)
        self.plugin._llm_allowed = lambda _name: True
        self.plugin._for_model = lambda name, _event: name
        self.plugin._stickers_on = Mock(return_value=False)
        self.plugin._group_image_lock = lambda: self.lock
        self.lock = asyncio.Lock()
        self.provider = Provider()
        self.plugin._vision_provider_for = Mock(return_value=self.provider)
        self.cache = {}
        self.plugin._load_image_cache = lambda: dict(self.cache)
        self.plugin._save_image_cache = lambda cache: self.cache.update(cache)
        self.lib = FakeLibrary()
        self.plugin._sticker_lib = lambda: self.lib

    def event(self, refs=('picture.png',)):
        return turn.TurnEvent(events.Incoming(
            place='private:10001', sender_id='10001', sender_name='Example', self_id='10003',
            message_id='20002', segments=tuple(events.Segment('image', {'file': ref}) for ref in refs),
            at_me=False, reply_to='', image_refs=tuple(refs), is_private=True, is_self=False, ts=0))

    async def test_the_character_comes_before_the_caption_and_stickers_off_keeps_nothing(self):
        result = await self.plugin._image_context(self.event())
        self.assertIn(WHO, result)
        self.assertIn('打招呼', result)
        self.assertLess(result.index(WHO), result.index('粉发女孩'))
        self.assertTrue(result.startswith(stickers.MATERIAL_LABEL))
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.provider.calls[0]['prompt'], stickers.LOOK_PROMPT)
        self.assertEqual(self.lib.rows, {})      # an ordinary picture does not join her stickers

    async def test_stickers_on_keeps_by_should_keep(self):
        self.plugin._stickers_on.return_value = True
        with patch.object(stickers, 'fetch_picture', return_value=PNG):
            result = await self.plugin._image_context(self.event())
        self.assertIn(WHO, result)
        self.assertIn('打招呼', result)
        self.assertEqual(self.lib.rows, {})      # a photo is not kept
        self.provider.answer = dict(ANSWER, kind='sticker')
        with patch.object(stickers, 'fetch_picture', return_value=PNG):
            await self.plugin._image_context(self.event(('another.png',)))
        self.assertEqual([row['caption'] for row in self.lib.rows.values()], ['粉发女孩比 V'])

    async def test_a_cached_look_gives_the_name_and_the_meaning_again(self):
        first = await self.plugin._image_context(self.event())
        second = await self.plugin._image_context(self.event())
        self.assertEqual(second, first)
        self.assertEqual(len(self.provider.calls), 1)
        for text in (first, second):
            self.assertIn(WHO, text)
            self.assertIn('打招呼', text)

    async def test_a_cached_look_with_stickers_on_gives_them_again(self):
        self.plugin._stickers_on.return_value = True
        with patch.object(stickers, 'fetch_picture', return_value=PNG):
            first = await self.plugin._image_context(self.event())
            second = await self.plugin._image_context(self.event())
        self.assertEqual(len(self.provider.calls), 1)
        for text in (first, second):
            self.assertIn(WHO, text)
            self.assertIn('打招呼', text)

    async def test_a_real_person_in_a_photo_is_never_named(self):
        self.provider.answer = dict(ANSWER, personal=True)
        for stickers_on in (False, True):
            with self.subTest(stickers_on=stickers_on):
                self.plugin._stickers_on.return_value = stickers_on
                with patch.object(stickers, 'fetch_picture', return_value=PNG):
                    result = await self.plugin._image_context(self.event(('photo-%s.png' % stickers_on,)))
                self.assertNotIn(WHO, result)
                self.assertIn('粉发女孩', result)
        self.assertNotIn(WHO, json.dumps(self.cache, ensure_ascii=False))
        self.assertEqual(self.lib.rows, {})

    async def test_three_pictures_are_not_cut_before_the_third_name(self):
        names = (WHO + '一', WHO + '二', WHO + '三')
        answers = iter(json.dumps({'who': name, 'caption': '图' * 60, 'meaning': '意' * 40},
                                  ensure_ascii=False) for name in names)

        async def answer(**kwargs):
            self.provider.calls.append(kwargs)
            return harness.FakeResponse(next(answers))

        self.provider.text_chat = answer
        result = await self.plugin._image_context(self.event(('a.png', 'b.png', 'c.png')))
        for name in names:
            self.assertIn(name, result)
        block = interpretation.render_compact(None, image=result)
        self.assertIn('[图片里是] ', block)
        for name in names:
            self.assertIn(name, block)            # three lines, not the old 160 characters

    async def test_an_old_cache_with_the_caption_only_still_gives_it(self):
        ref = 'picture.png'
        self.cache[mixin_media._sha256(ref)] = {'ref': ref, 'caption': '图里是一只猫',
                                                'ts': time.time(),
                                                'from_qq': '10001', 'where': 'private:10001'}
        result = await self.plugin._image_context(self.event())
        self.assertIn('图里是一只猫', result)
        self.assertEqual(self.provider.calls, [])


class TheGateCache(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = Her()
        self.plugin.cache = {}
        self.plugin._speaker = lambda event: ('10001', 'Example')
        self.plugin._here = lambda event: 'private:10001'
        self.plugin._job_stale = lambda: False
        self.plugin._load_image_cache = lambda: dict(self.plugin.cache)
        self.plugin._save_image_cache = lambda cache: setattr(self.plugin, 'cache', dict(cache))

    async def test_the_second_look_gets_the_whole_look_back(self):
        provider = Provider()
        gate = vision.VisionGate(self.plugin, provider, object())
        with patch.object(vision, '_bytes', return_value=PNG), \
                patch.object(vision.mixin_attention, '_read_json', return_value={}), \
                patch.object(vision.mixin_attention, '_write_json'):
            first = await gate.text_chat(prompt=stickers.LOOK_PROMPT,
                                         image_urls=['https://gchat.qpic.cn/a.png'])
            second = await gate.text_chat(prompt=stickers.LOOK_PROMPT,
                                          image_urls=['https://gchat.qpic.cn/b.png'])
        self.assertEqual(len(provider.calls), 1)      # the same picture is not asked twice
        self.assertIn(WHO, first.completion_text)
        look = stickers.parse_look(second.completion_text)
        self.assertEqual(look['who'], WHO)
        self.assertEqual(look['meaning'], '打招呼、开心')
        self.assertIn('look', list(self.plugin.cache.values())[0])    # the whole look is kept


if __name__ == '__main__':
    unittest.main()
