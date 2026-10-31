# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Autonomy sends and screenshot captions through ports, offline."""
import asyncio
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))

import harness  # noqa: E402


class AutonomyPorts(unittest.TestCase):
    def setUp(self):
        global interpretation, main, mixin_selfie, real_browser, _AutonomySendTarget, PortsMixin
        import interpretation
        import main
        import mixin_selfie
        import real_browser
        from common import _AutonomySendTarget
        from mixin_ports import PortsMixin
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.context = harness.FakeContext()
        self.plugin.context.send_message = AsyncMock()
        self.plugin.proactive_autonomy = True
        self.plugin.proactive_send = True
        self.plugin._user_record = Mock(return_value={})
        self.plugin._relationship_of = Mock(return_value={})
        self.core = SimpleNamespace(_proactive_autonomy={})

    def send(self, event, text):
        self.plugin._autonomy_gate = Mock(return_value=(text, {}))
        self.assertTrue(asyncio.run(self.plugin._maybe_proactive_send(event, self.core, now=1000)))

    def assert_plain(self, chain, text):
        self.assertEqual(len(chain.chain), 1)
        self.assertEqual(type(chain.chain[0]).__name__, 'Plain')
        self.assertEqual(chain.chain[0].text, text)

    def test_event_send_keeps_text_and_face_marker_whole(self):
        event = harness.FakeEvent('hello')
        event.send = AsyncMock()
        text = 'hello [表情:微笑]'
        self.send(event, text)
        event.send.assert_awaited_once()
        self.assert_plain(event.send.await_args.args[0], text)
        self.plugin.context.send_message.assert_not_awaited()

    def test_background_target_sends_to_its_session(self):
        session = 'default:FriendMessage:10003'
        target = _AutonomySendTarget(self.plugin, session, '10003', 'friend')
        self.send(target, 'hello')
        self.plugin.context.send_message.assert_awaited_once()
        umo, chain = self.plugin.context.send_message.await_args.args
        self.assertEqual(umo, session)
        self.assert_plain(chain, 'hello')

    def test_screenshot_caption_provider_arguments_and_missing_provider(self):
        path = Path('shot.jpg')
        provider = SimpleNamespace(text_chat=AsyncMock(return_value=harness.FakeResponse('  a  picture\n here  ')))
        self.plugin._browse_ledger = Mock(return_value=SimpleNamespace(add=Mock()))
        self.plugin._vision_provider_for = Mock(return_value=provider)
        event = harness.FakeEvent('hello')
        with patch.object(mixin_selfie, 'SHOT_DIR') as directory, \
                patch.object(mixin_selfie, '_prune_browser_shots'), \
                patch.object(real_browser, 'screenshot', new_callable=AsyncMock, return_value=path):
            directory.__truediv__.return_value = path
            result = asyncio.run(mixin_selfie._browser_screenshot(self.plugin, event, 'https://example.test'))
            self.assertEqual(result, (path, 'a picture here'))
            provider.text_chat.assert_awaited_once_with(prompt=interpretation.image_caption_prompt(), image_urls=[str(path)])
            self.plugin._vision_provider_for.return_value = None
            self.assertIsNone(asyncio.run(mixin_selfie._browser_screenshot(self.plugin, event, 'https://example.test')))
            provider.text_chat.assert_awaited_once()

    def test_ports_mixin_occurs_once_in_plugin_mro(self):
        self.assertEqual(main.BioCorePlugin.__mro__.count(PortsMixin), 1)

    def test_model_factory_wraps_provider_and_mixin_uses_factory(self):
        import mixin_ports
        from adapter_astrbot_model import AstrBotModel

        provider = object()
        client = mixin_ports.model_for(provider)
        self.assertIsInstance(client, AstrBotModel)
        self.assertIs(client.provider, provider)
        with patch.object(mixin_ports, 'model_for', return_value=client) as factory:
            self.assertIs(PortsMixin()._model(provider), client)
            factory.assert_called_once_with(provider)
