# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for owner-only Qzone posting."""
import asyncio
import base64
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_onebot_messenger as adapter
import messenger
import mixin_selfie
import qzone


class Api:
    def __init__(self):
        self.calls = []

    async def __call__(self, action, params):
        self.calls.append((action, params))
        return {'status': 'ok', 'data': {'tid': 'abc123'}}


class Plugin:
    def __init__(self, api):
        self.config = {'qzone_enabled': True, 'owner_qq': '10001'}
        self._neutral_messenger = adapter.OneBotMessenger(api)

    def _names_index(self):
        return {'10001': {'Owner'}, '10003': {'Alice'}}

    def _known_names(self, people):
        return [name for person in people for name in self._names_index()[person]]

    def _owner_rules(self):
        return ['abcdefghijklmnop']


class QzoneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ams-qzone-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.selfies = self.root / 'selfie'
        self.selfies.mkdir()
        self.state = self.root / 'states'
        self.name = 'ams-phone-photo-20261101010203-' + 'a' * 32 + '.png'
        self.photo = self.selfies / self.name
        self.photo.write_bytes(b'fake photo')
        state_patch = patch.object(qzone, 'STATE_DIR', self.state)
        state_patch.start()
        self.addCleanup(state_patch.stop)
        photo_patch = patch.object(mixin_selfie, 'SELFIE_DIR', self.selfies)
        photo_patch.start()
        self.addCleanup(photo_patch.stop)
        self.api = Api()
        self.plugin = Plugin(self.api)

    def post(self, text='hello', photo=None):
        return asyncio.run(qzone.post(self.plugin, text, photo))

    def test_photo_and_private_record(self):
        self.assertEqual(self.post(' hello ', self.photo), ('abc123', ''))
        self.assertEqual(self.api.calls, [('send_qzone_msg', {
            'content': 'hello', 'images': ['base64://' + base64.b64encode(b'fake photo').decode()],
            'ugc_right': 16, 'target_uins': ['10001']})])
        state = json.loads((self.state / 'qzone.json').read_text(encoding='utf-8'))
        self.assertEqual(set(state['posts'][0]), {'tid', 'ts', 'text_sha256'})
        self.assertNotIn('hello', json.dumps(state))

    def test_bad_photos_are_refused(self):
        for photo in (self.root / 'shots' / self.name, self.selfies / 'refs' / self.name,
                      'https://example.invalid/a.png', self.selfies / '..' / 'selfie' / self.name):
            with self.subTest(photo=photo):
                params = {'content': 'hello', 'images': [str(photo)], 'ugc_right': 16, 'target_uins': ['10001']}
                with self.assertRaises(messenger.ActionRefused):
                    asyncio.run(self.plugin._neutral_messenger.call('send_qzone_msg', **params))
        self.assertEqual(self.api.calls, [])

    def test_bad_parameters_and_delete_are_refused(self):
        base = {'content': 'hello', 'ugc_right': 16, 'target_uins': ['10001']}
        for changes in ({'ugc_right': 1}, {'target_uins': ['10001', '10003']},
                        {'target_uins': [10001]}, {'extra': 1}, {'content': ' '}, {'ugc_right': True}):
            with self.subTest(changes=changes), self.assertRaises(messenger.ActionRefused):
                asyncio.run(self.plugin._neutral_messenger.call('send_qzone_msg', **dict(base, **changes)))
        for tid in ('', 'bad-id', 'a' * 65):
            with self.assertRaises(messenger.ActionRefused):
                asyncio.run(self.plugin._neutral_messenger.call('delete_qzone_msg', tid=tid))
        self.assertEqual(self.api.calls, [])

    def test_limit_next_day_and_delete(self):
        self.assertEqual(self.post()[0], 'abc123')
        self.assertTrue(asyncio.run(qzone.delete(self.plugin, 'abc123')))
        self.assertFalse(asyncio.run(qzone.delete(self.plugin, 'other')))
        self.assertEqual(self.post()[0], 'abc123')
        self.assertEqual(self.post()[1], 'limit')
        tomorrow = datetime.now() + timedelta(days=1)
        with patch.object(qzone, 'datetime') as clock:
            clock.now.return_value = tomorrow
            self.assertEqual(self.post()[0], 'abc123')
        self.assertEqual([a for a, _ in self.api.calls], ['send_qzone_msg', 'delete_qzone_msg', 'send_qzone_msg', 'send_qzone_msg'])

    def test_privacy_checks(self):
        with patch.object(qzone.redline, 'hit', return_value='hit'):
            self.assertEqual(self.post('hello')[1], 'redline')
        self.assertEqual(self.post('abcdefghijklmnop')[1], 'owner_rule')
        self.assertEqual(self.post('Alice 10003 and 10001')[0], 'abc123')
        text = self.api.calls[0][1]['content']
        self.assertNotIn('Alice', text)
        self.assertEqual(text.count('[号码]'), 2)

    def test_disabled_and_missing_owner(self):
        self.plugin.config['qzone_enabled'] = False
        self.assertEqual(self.post()[1], 'disabled')
        self.plugin.config = {'qzone_enabled': True}
        self.assertEqual(self.post()[1], 'owner')
        self.assertEqual(self.api.calls, [])
