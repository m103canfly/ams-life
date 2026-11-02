# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for her outfit and lasting appearance."""
import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import test_selfie  # noqa: E402
import harness  # noqa: E402
import look  # noqa: E402
import main  # noqa: E402
import mixin_people  # noqa: E402
import mixin_selfie as phone  # noqa: E402


class HerLookTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plugin = main.BioCorePlugin(harness.FakeContext(), config={'photo_enabled': True})
        test_basics.PLUGINS.append(self.plugin)
        self.event = test_selfie.Event()
        self.path = self.root / 'look.json'
        self.look_patch = patch.object(phone, 'LOOK_PATH', self.path)
        self.look_patch.start()
        self.addCleanup(self.look_patch.stop)
        self.model_patch = patch.object(mixin_people, 'SELF_MODEL_PATH', self.root / 'self_model.json')
        self.model_patch.start()
        self.addCleanup(self.model_patch.stop)

    async def set_look(self, today, change=''):
        tool = next(x for x in self.plugin._phone_tools(self.event) if x.name == 'set_look')
        return await tool.handler(self.event, today=today, change=change)

    def test_prompt_base(self):
        for phrase in ('高马尾', '呆毛', '发型、头饰都照参考图1'):
            self.assertNotIn(phrase, phone.SELFIE_PROMPT)
        self.assertIn('参考图只管脸型、眼睛（琥珀色，神态）、身高体态，不管发色、发型、发饰和衣服', phone.SELFIE_PROMPT)

    async def test_set_look_retention_and_reload(self):
        self.assertEqual(await self.set_look('在家穿宽松卫衣，头发随便扎了个丸子', '挑染了一小撮浅蓝色发尾'), '记下了')
        state = json.loads(self.path.read_text(encoding='utf-8'))
        self.assertEqual(state['date'], datetime.now().date().isoformat())
        self.assertEqual(self.plugin._load_self_model()['look'][0]['text'], '挑染了一小撮浅蓝色发尾')
        for i in range(8):
            await self.set_look('宽松卫衣', '变化' + str(i))
        self.assertEqual(len(self.plugin.self_model['look']), 8)
        self.assertEqual(self.plugin.self_model['look'][0]['text'], '变化0')
        self.assertEqual(self.plugin._load_self_model()['look'], self.plugin.self_model['look'])

    async def test_reject_unsafe_and_empty(self):
        for value in ('和10002在 https://x.example', '10002', ''):
            self.assertEqual(await self.set_look(value), '不能这样写')
        self.assertFalse(self.path.exists())

    async def test_photo_gate_and_prompts(self):
        args = dict(what='在家拍照', where='家', doing='休息', caption='你好')
        self.assertEqual(await self.plugin._tool_take_photo(self.event, kind='selfie', **args),
                         '先用 set_look 定今天的打扮再拍')
        self.assertNotIn('photo', getattr(self.event, '_ams_phone_queue', {}))
        await self.set_look('宽松卫衣', '浅蓝色发尾')
        self.assertEqual(await self.plugin._tool_take_photo(self.event, kind='selfie', **args), phone.PHOTO_QUEUED)
        ref = self.root / 'her_base.png'
        ref.write_bytes(b'fake')
        self.plugin.api_config = {'image': {'base_url': 'https://image.invalid'}}
        self.plugin._post_selfie = AsyncMock(return_value=b'{"data":[{"b64_json":"cG5n"}]}')
        self.plugin._post_json = AsyncMock(return_value=(b'{"data":[{"b64_json":"cG5n"}]}', ''))
        self.plugin._phone_account = Mock()
        self.plugin._phone_price = Mock(return_value=0)
        self.plugin._phone_path = Mock(return_value=self.root / 'photo.png')
        with patch.object(phone, 'REF_DIR', self.root), patch.object(self.plugin, '_phone_clear', AsyncMock(return_value=True)):
            await phone._prepare_photo(self.plugin, self.event, self.event._ams_phone_queue)
            self.assertTrue(self.event._ams_phone_queue['photo_path'])
            prompt = self.plugin._post_selfie.await_args.args[1]
            self.assertIn('今天的打扮：宽松卫衣', prompt)
            self.assertIn('最近的样子：浅蓝色发尾', prompt)
            await self.plugin._make_photo('snap', '窗外')
            self.assertIn('她今天穿：宽松卫衣', self.plugin._post_json.await_args.args[1]['prompt'])
        self.path.unlink()
        event = test_selfie.Event()
        self.assertEqual(await self.plugin._tool_take_photo(event, kind='snap', **args), phone.PHOTO_QUEUED)

    def test_line_seasons_and_yesterday(self):
        today = date(2026, 11, 8)
        self.assertEqual(look.season_of(date(2026, 11, 1)), ('秋', '霜降'))
        self.assertEqual(look.season_of(today), ('冬', '立冬'))
        self.assertEqual(look.season_of(date(2027, 1, 1)), ('冬', '冬至'))
        model = {'look': [{'text': '浅蓝发尾', 'date': (today - timedelta(days=3)).isoformat()}]}
        self.assertIn('浅蓝发尾（3天前）', look.look_line(today, '', model))
        self.assertIn('今天还没定穿什么', look.look_line(today, '', model))
        self.assertIn('今天的打扮：卫衣', look.look_line(today, '卫衣', model))
        look.write_look(self.path, {'date': (today - timedelta(days=1)).isoformat(), 'today': '卫衣'})
        self.assertEqual(look.read_look(self.path, today), '')
