# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline image captions without an AstrBot configuration."""
import ast
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import events
import harness
import her
import interpretation
import turn


def route_collector():
    # The collector itself does not need panel_api's aiohttp import.
    source = (Path(__file__).resolve().parent.parent / 'panel_api.py').read_text('utf-8')
    node = next(n for n in ast.parse(source).body
                if isinstance(n, ast.ClassDef) and n.name == 'RouteCollector')
    namespace = {'PREFIX': '/astrbot_plugin_ams_life/'}
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'panel_api.py', 'exec'), namespace)
    return namespace['RouteCollector']()


class Provider:
    def __init__(self):
        self.calls = []

    async def text_chat(self, **kwargs):
        self.calls.append(kwargs)
        return harness.FakeResponse('图里是一只猫')


class ImageContextStandalone(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.context = route_collector()
        self.plugin = her.Her(self.context, config={'vision_image_api_model': 'made-up-model'})
        test_basics.PLUGINS.append(self.plugin)
        self.plugin._neutral_model = 'made-up-neutral-model'
        self.provider = Provider()
        self.plugin._vision_provider_for = Mock(return_value=self.provider)
        self.plugin._llm_allowed = Mock(return_value=True)
        self.plugin._stickers_on = Mock(return_value=False)
        self.cache = {}
        self.plugin._load_image_cache = lambda: dict(self.cache)
        self.plugin._save_image_cache = lambda cache: self.cache.update(cache)
        incoming = events.Incoming(
            place='private:10001', sender_id='10001', sender_name='Example', self_id='10003',
            message_id='20002', segments=(events.Segment('image', {'file': 'picture.png'}),),
            at_me=False, reply_to='', image_refs=('picture.png',), is_private=True,
            is_self=False, ts=0)
        self.event = turn.TurnEvent(incoming)

    async def test_standalone_caption_and_cache(self):
        first = await self.plugin._image_context(self.event)
        self.assertIn('猫', first)
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.provider.calls[0]['prompt'], interpretation.image_caption_prompt(''))
        self.assertEqual(await self.plugin._image_context(self.event), first)
        self.assertEqual(len(self.provider.calls), 1)

    async def test_astrbot_caption_prompt(self):
        self.context.get_config = lambda: {'provider_settings': {'image_caption_prompt': 'Describe this drawing.'}}
        self.assertIn('猫', await self.plugin._image_context(self.event))
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.provider.calls[0]['prompt'], interpretation.image_caption_prompt('Describe this drawing.'))

    async def test_config_error_uses_default_prompt(self):
        self.context.get_config = Mock(side_effect=RuntimeError('unavailable'))
        self.assertIn('猫', await self.plugin._image_context(self.event))
        self.assertEqual(self.provider.calls[0]['prompt'], interpretation.image_caption_prompt(''))
