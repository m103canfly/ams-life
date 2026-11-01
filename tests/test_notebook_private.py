# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Private notebook material and writes."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import discretion
import harness
import impressions
import interpretation
import mixin_discretion
import mixin_llm


class NotebookPrivate(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plugin = test_basics.make_plugin(harness.FakeContext())

    def test_prompt_differs_only_for_private(self):
        private = interpretation.notebook_prompt([], [], True)
        group = interpretation.notebook_prompt([], [], False)
        self.assertIn('这一次的材料来自私聊。只写你自己学到的、感受到的（比如“跟熟的人聊天会放松”），不写人名、群名，也不写私事的细节。', private)
        self.assertNotIn('名字照材料里那样，用「」框着', private)
        self.assertIn('名字照材料里那样，用「」框着', group)

    def test_materials_skip_raw_and_unknown_sources(self):
        place = 'private:10003'
        origin = discretion.make_origin(place, ['10003'], [], discretion.PRIVATE)
        events = [dict(id='digest', origin=origin, summary_status='digest', title='整理', small_summary='学会放松', event='原话甲'),
                  dict(id='llm', origin=origin, summary_status='llm', title='原话乙', small_summary='感到温暖', event='原话丙'),
                  dict(id='fallback', origin=origin, summary_status='fallback', title='原话丁', small_summary='原话戊'),
                  dict(id='legacy', origin=origin, small_summary='原话己')]
        self.plugin._today_events = lambda now: events
        mats = self.plugin._notebook_materials(None, place, 42)
        text = ''.join(m['text'] for m in mats)
        self.assertIn('学会放松', text)
        self.assertIn('感到温暖', text)
        for raw in ('原话甲', '原话乙', '原话丙', '原话丁', '原话戊', '原话己'):
            self.assertNotIn(raw, text)
        self.assertEqual({m['ref'] for m in mats}, {'body', 'digest', 'llm'})

    async def test_private_write_anonymizes_and_preserves_origin(self):
        p = self.plugin
        place = 'private:10003'
        p._people_store = impressions.Store(self.root / 'people')
        p._people_store.keep_names('10003', ['小星'])
        users = self.root / 'users'
        users.mkdir()
        (users / '10003.json').write_text(json.dumps({'names': ['星仔']}, ensure_ascii=False), encoding='utf-8')
        p._name_index = {'10003': {'阿星'}}
        p._read_window = lambda sitting: {'recent': [{'sender_id': '10003', 'sender_name': '阿星'}]}
        p._notebook_time_reached = lambda now: True
        p._notebook_night = lambda now: {'tried': [], 'changes': 0}
        p._notebook_sittings = lambda now: [place]
        p._notebook_materials = lambda core, sitting, now: []
        p._core = lambda event: None
        p._persona_text = AsyncMock(return_value='')
        p._llm_v2_call = AsyncMock(return_value=[{'op': 'add', 'text': '「阿星」说他下周要去考试，星仔和小星知道 900001'}])
        p._job_stale = lambda: False
        p._without_gone = lambda text: text
        p._save_self_model = lambda: None
        p.self_model['notebook'] = []
        with patch.object(mixin_discretion, 'USER_DIR', users), patch.object(mixin_llm, 'DATA_DIR', self.root):
            self.assertTrue(await p._maybe_write_notebook(now=42))
        note = p.self_model['notebook'][0]
        self.assertTrue(note['text'].startswith('有人说他下周要去考试'))
        for forbidden in ('阿星', '星仔', '小星', '900001'):
            self.assertNotIn(forbidden, note['text'])
        self.assertEqual(note['origin']['where'], place)
        self.assertEqual(note['origin']['visibility'], discretion.PRIVATE)

    async def test_group_write_keeps_names(self):
        p = self.plugin
        p._notebook_time_reached = lambda now: True
        p._notebook_night = lambda now: {'tried': [], 'changes': 0}
        p._notebook_sittings = lambda now: ['group']
        p._notebook_materials = lambda core, sitting, now: []
        p._core = lambda event: None
        p._persona_text = AsyncMock(return_value='')
        p._llm_v2_call = AsyncMock(return_value=[{'op': 'add', 'text': '「阿星」说今天很开心'}])
        p._job_stale = lambda: False
        p._without_gone = lambda text: text
        p._save_self_model = lambda: None
        p.self_model['notebook'] = []
        with patch.object(mixin_llm, 'DATA_DIR', self.root):
            self.assertTrue(await p._maybe_write_notebook(now=42))
        self.assertEqual(p.self_model['notebook'][0]['text'], '「阿星」说今天很开心')
