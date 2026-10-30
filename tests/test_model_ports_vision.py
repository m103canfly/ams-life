# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline vision calls through the model port."""
import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))

import harness
import interpretation
import main
import stickers
from mixin_ports import PortsMixin
from mixin_stickers import StickersMixin


class Provider:
    def __init__(self, text='', error=None):
        self.text = text
        self.error = error
        self.calls = []

    async def text_chat(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return harness.FakeResponse(self.text)


class VisionModelPorts(unittest.TestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.context = harness.FakeContext()
        self.plugin.image_llama_server = ''
        self.plugin.image_llama_model = ''
        self.plugin.image_service_port = 0
        self.plugin._llm_allowed = Mock(return_value=True)
        self.plugin._load_image_cache = Mock(return_value={})
        self.plugin._save_image_cache = Mock()
        self.plugin._here = Mock(return_value='friend:10001')
        self.plugin._speaker = Mock(return_value=('10001', 'Alice'))
        self.plugin._stickers_on = Mock(return_value=False)
        self.plugin._model = Mock(wraps=self.plugin._model)
        self.event = harness.FakeEvent('hello')
        self.event._ams_image_refs = ['picture.png']

    def test_caption_arguments_and_text(self):
        provider = Provider('  a picture  ')
        self.plugin._vision_provider_for = Mock(return_value=provider)
        result = asyncio.run(self.plugin._image_context_locked(self.event))
        self.assertEqual(result, 'a picture')
        self.assertEqual(provider.calls, [{'prompt': interpretation.image_caption_prompt(None),
                                           'image_urls': ['picture.png']}])
        self.plugin._model.assert_called_once_with(provider)

    def test_look_arguments_and_text(self):
        provider = Provider('{"caption": "a sticker", "kind": "sticker", "keep": true}')
        standalone = StickersMixin()
        standalone._model = Mock(wraps=standalone._model)
        caption, look = asyncio.run(standalone._look_once(provider, 'picture.png', self.event))
        self.assertEqual(caption, 'a sticker')
        self.assertEqual(look, stickers.parse_look(provider.text))
        self.assertEqual(provider.calls, [{'prompt': stickers.LOOK_PROMPT, 'image_urls': ['picture.png']}])
        standalone._model.assert_called_once_with(provider)

    def test_provider_error_is_caught_by_image_context(self):
        for stickers_on in (False, True):
            with self.subTest(stickers_on=stickers_on):
                provider = Provider(error=RuntimeError('offline failure'))
                self.plugin._vision_provider_for = Mock(return_value=provider)
                self.plugin._stickers_on.return_value = stickers_on
                self.plugin._sticker_refs = Mock(return_value=[])
                self.assertEqual(asyncio.run(self.plugin._image_context_locked(self.event)), '')
                self.assertEqual(len(provider.calls), 1)

    def test_plugin_mro_has_one_ports_mixin(self):
        self.assertEqual(main.BioCorePlugin.__mro__.count(PortsMixin), 1)
