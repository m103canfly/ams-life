# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline lookup calls through the messenger port."""
import asyncio
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))

import harness
import main
import mixin_media
import mixin_phone
from astrbot.api.message_components import Reply
from messenger import ActionRefused
from mixin_ports import PortsMixin


class Forward:
    def __init__(self, fid):
        self.id = fid


class FakeAPI:
    def __init__(self, result):
        self.result = result
        self.calls = []

    async def call_action(self, action, **params):
        self.calls.append((action, params))
        return self.result


class LookupPorts(unittest.TestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin.context = harness.FakeContext()
        self.plugin._may_keep = Mock(return_value=True)
        self.plugin._here = Mock(return_value='')
        self.plugin._message_id = Mock(return_value='')
        self.plugin._for_model = lambda text, event: text
        self.plugin._messenger = Mock(wraps=self.plugin._messenger)
        self.event = harness.FakeEvent('hello')

    def set_api(self, result):
        api = FakeAPI(result)
        self.event.bot = types.SimpleNamespace(api=api)
        return api

    def test_quoted_image_lookup_and_non_dict(self):
        self.event.get_messages = lambda: [Reply(id=10001)]
        api = self.set_api({'data': {'message': [{'type': 'image', 'data': {'file': 'image.png'}}],
                                      'sender': {'user_id': '10003'}}})
        self.assertEqual(asyncio.run(self.plugin._quoted_image_refs(self.event)), ['image.png'])
        self.assertEqual(api.calls, [('get_msg', {'message_id': '10001'})])
        self.plugin._messenger.assert_called_with(self.event)
        api.result = ['unexpected']
        self.assertEqual(asyncio.run(self.plugin._quoted_image_refs(self.event)), [])

    def test_forward_lookup_and_non_dict(self):
        self.event.get_messages = lambda: [Forward(10001)]
        api = self.set_api({'data': {'messages': [{'sender': {'nickname': 'Alice', 'user_id': '10003'},
                                                   'message': [{'type': 'text', 'data': {'text': 'hello'}},
                                                               {'type': 'image', 'data': {'file': 'hidden'}}]}]}})
        result = asyncio.run(mixin_phone._expand_forward(self.plugin, self.event))
        self.assertEqual(result, '\uff08\u8f6c\u53d1\u6765\u7684\u804a\u5929\u8bb0\u5f55\uff0c\u51fa\u5904\u4e0e\u672c\u6d88\u606f\u76f8\u540c\uff09\n\uff08\u539f\u6587\uff09Alice\uff1ahello')
        self.assertEqual(api.calls, [('get_forward_msg', {'id': '10001'})])
        self.plugin._messenger.assert_called_with(self.event)
        api.result = ['unexpected']
        self.assertEqual(asyncio.run(mixin_phone._expand_forward(self.plugin, self.event)), '')

    def test_missing_bot_returns_empty(self):
        self.event.get_messages = lambda: [Reply(id=10001)]
        self.assertEqual(asyncio.run(self.plugin._quoted_image_refs(self.event)), [])
        self.event.get_messages = lambda: [Forward(10001)]
        self.assertEqual(asyncio.run(mixin_phone._expand_forward(self.plugin, self.event)), '')

    def test_disallowed_action_is_refused_before_bot_call(self):
        api = self.set_api({})
        with self.assertRaises(ActionRefused):
            asyncio.run(self.plugin._messenger(self.event).call('delete_msg', message_id='10001'))
        self.assertEqual(api.calls, [])

    def test_media_mixin_without_context_and_plugin_mro(self):
        class MediaOnly(mixin_media.MediaMixin):
            pass

        api = self.set_api({'data': {'message': []}})
        result = asyncio.run(MediaOnly()._messenger(self.event).call('get_msg', message_id='10001'))
        self.assertEqual(result, {'data': {'message': []}})
        self.assertEqual(api.calls, [('get_msg', {'message_id': '10001'})])
        self.assertEqual(main.BioCorePlugin.__mro__.count(PortsMixin), 1)
