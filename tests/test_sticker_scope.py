# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Sticker scope and single-fetch behavior, offline."""
import base64
import hashlib
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import main
import stickers

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+l0ZkAAAAASUVORK5CYII=')


class Scope(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ['TEMP'])
        self.addCleanup(self.tmp.cleanup)
        self.lib = stickers.Library(self.tmp.name)
        self.sid, _ = self.lib.add(PNG, time.time(), source='self', from_where='private:10001')
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.plugin._sticker_lib = Mock(return_value=self.lib)
        self.plugin._here = Mock(return_value='private:10001')
        self.plugin._may_speak_in = Mock(return_value=True)
        self.plugin._note_sent = Mock()
        self.plugin._neutral_messenger = SimpleNamespace(call=AsyncMock(), send=AsyncMock())
        self.event = SimpleNamespace()

    async def test_select_send_and_publish(self):
        group, private = 'group:900001', 'private:10001'
        self.assertEqual(stickers.pick_candidates(self.lib.rows, 2, place=group), [])
        self.plugin._here.return_value = group
        self.assertEqual(await self.plugin._sticker_offer(self.event, SimpleNamespace(v=0)), '')
        self.assertFalse(await self.plugin._send_sticker(self.event, self.sid, '', group))
        self.plugin._neutral_messenger.call.assert_not_awaited()
        self.plugin._here.return_value = private
        self.assertTrue(await self.plugin._sticker_offer(self.event, SimpleNamespace(v=0)))
        self.assertEqual(stickers.pick_candidates(self.lib.rows, 2, place=private), [self.sid])
        self.assertTrue(await self.plugin._send_sticker(self.event, self.sid, '', private))
        self.lib.rows[self.sid]['uses'] = 0
        result = await self.plugin.page_sticker_scope({'id': self.sid, 'scope': 'all'})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(stickers.pick_candidates(self.lib.rows, 2, place=group), [self.sid])
        self.assertEqual((await self.plugin.page_sticker_scope({'id': self.sid, 'scope': 'here'}))['status'], 'ok')
        self.assertEqual(stickers.pick_candidates(self.lib.rows, 2, place=group), [])
        self.assertFalse(self.lib.set_scope(self.sid, group))

    async def test_unavailable_picture_is_not_looked_at(self):
        model = SimpleNamespace(chat=AsyncMock())
        self.plugin._model = Mock(return_value=model)
        with patch.object(stickers, 'fetch_picture', return_value=b'') as fetch:
            caption, look = await self.plugin._look_once(object(), 'https://gchat.qpic.cn/a.png', self.event)
        self.assertEqual((caption, look), ('', {}))
        fetch.assert_called_once()
        model.chat.assert_not_awaited()

    async def test_group_sticker_shared_then_restricted(self):
        lib = stickers.Library(Path(self.tmp.name) / 'group-library')
        sid, why = lib.add(PNG, time.time(), source='self', from_where='group:900001')
        self.assertEqual(why, '')
        self.assertEqual(lib.rows[sid]['scope'], 'all')
        self.assertEqual(stickers.pick_candidates(lib.rows, 2, place='group:900002'), [sid])
        self.assertEqual(stickers.pick_candidates(lib.rows, 2, place='private:10001'), [sid])
        self.plugin._sticker_lib = Mock(return_value=lib)
        result = await self.plugin.page_sticker_scope({'id': sid, 'scope': 'here'})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(stickers.pick_candidates(lib.rows, 2, place='group:900002'), [])
        self.assertEqual(stickers.pick_candidates(lib.rows, 2, place='group:900001'), [sid])

    def test_legacy_scope_inference_and_saved_scope(self):
        group = {'source': 'self', 'from_where': 'group:900001'}
        private = {'source': 'self', 'from_where': 'private:10001'}
        self.assertEqual(stickers.scope_of(group), 'all')
        self.assertEqual(stickers.scope_of(private), 'private:10001')
        self.assertEqual(stickers.scope_of({'source': 'self'}), '')
        group['scope'] = 'group:900001'
        self.assertEqual(stickers.scope_of(group), 'group:900001')
        self.assertFalse(stickers.may_send(group, 'group:900002'))
        private['scope'] = 'all'
        self.assertTrue(stickers.may_send(private, 'group:900002'))

    async def test_old_rows_and_listing(self):
        for source in ('old', 'owner'):
            row = {'source': source}
            self.assertTrue(stickers.may_send(row, 'group:900001'))
            self.assertEqual(stickers.pick_candidates({'a': row}, 2, place='group:900001'), ['a'])
        self.assertFalse(stickers.may_send({'source': 'self'}, 'group:900001'))
        self.assertTrue(stickers.may_send({'source': 'self', 'from_where': 'private:10001'}, 'private:10001'))
        result = await self.plugin.page_stickers({})
        item = result['data']['items'][0]
        self.assertEqual(item['scope'], 'here')
        self.assertNotIn('from_where', item)
        self.assertNotIn('10001', json.dumps(result))
        self.assertNotIn('900001', json.dumps(result))

    async def test_look_and_keep_use_one_fetch(self):
        response = json.dumps({'caption': 'cat', 'kind': 'sticker', 'keep': True,
                               'personal': False, 'group_meme': False})
        model = SimpleNamespace(chat=AsyncMock(return_value=SimpleNamespace(text=response)))
        self.plugin._model = Mock(return_value=model)
        self.plugin._speaker = Mock(return_value=('10001', ''))
        self.plugin._job_stale = Mock(return_value=False)
        with patch.object(stickers, 'fetch_picture', return_value=PNG) as fetch:
            _, look = await self.plugin._look_once(object(), 'https://gchat.qpic.cn/a.png', self.event)
            sid = await self.plugin._maybe_keep(self.event, 'https://gchat.qpic.cn/a.png', look)
        self.assertEqual(fetch.call_count, 1)
        url = model.chat.await_args.kwargs['images'][0]
        self.assertEqual(base64.b64decode(url.split(',', 1)[1]), PNG)
        self.assertEqual(hashlib.sha256(self.lib.path_of(sid).read_bytes()).digest(), hashlib.sha256(PNG).digest())
        self.assertNotIn('_picture', stickers.cache_entry('x', look, '', '', 1)['look'])
        look['_picture'] = PNG + b'x'
        self.assertEqual(await self.plugin._maybe_keep(self.event, '', look), '')

    def test_unknown_look_fields_do_not_keep(self):
        base = {'caption': 'cat', 'kind': 'sticker', 'keep': True, 'personal': False, 'group_meme': False}
        for field in ('personal', 'group_meme'):
            for value in (None, 'maybe', 0):
                data = dict(base)
                if value is None:
                    del data[field]
                else:
                    data[field] = value
                self.assertFalse(stickers.should_keep(stickers.parse_look(json.dumps(data))))
        self.assertTrue(stickers.should_keep(stickers.parse_look(json.dumps(base))))


if __name__ == '__main__':
    unittest.main()
