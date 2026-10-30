# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Text model call sites keep provider arguments and parsed replies."""
import asyncio
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))

import harness
import main
import interpretation
import mixin_llm
import mixin_impressions
from mixin_ports import PortsMixin


class RecordingProvider:
    def __init__(self, text, fail=False):
        self.text, self.fail, self.calls = text, fail, []

    async def text_chat(self, **kwargs):
        self.calls.append(kwargs)
        if self.fail:
            raise ValueError('model failed')
        return harness.FakeResponse(self.text)


class TextModelCalls(unittest.TestCase):
    def setUp(self):
        self.p = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.p._llm_allowed = Mock(return_value=True)
        self.p._mask_if_safety = lambda value: value
        self.p._provider_for = AsyncMock()
        self.event = harness.FakeEvent('hello')

    def provider(self, text, fail=False):
        provider = RecordingProvider(text, fail)
        self.p._provider_for.return_value = provider
        return provider

    def run_async(self, coroutine):
        return asyncio.run(coroutine)

    def test_llm_v2_arguments_parsing_and_error(self):
        for system in (None, '', 'system'):
            with self.subTest(system=system):
                provider = self.provider('{"value": 7}')
                result = self.run_async(self.p._llm_v2_call('test', 'prompt', json.loads, system_prompt=system))
                expected = {'prompt': 'prompt'}
                if system:
                    expected['system_prompt'] = system
                self.assertEqual(provider.calls, [expected])
                self.assertEqual(result, {'value': 7})
        self.provider('{}', True)
        self.assertIsNone(self.run_async(self.p._llm_v2_call('test', 'prompt', json.loads)))

    def test_persona_compile_arguments_parsing_and_error(self):
        self.p._persona_text = AsyncMock(return_value='persona')
        reply = '{"schema": ["slot"], "profile": {"name": "test"}}'
        with patch.object(mixin_llm, 'PROFILE_PATH') as path:
            provider = self.provider(reply)
            self.run_async(self.p._compile_profile(self.event))
            self.assertEqual(provider.calls, [{'prompt': interpretation.persona_compile_prompt('persona'),
                                               'system_prompt': interpretation.persona_compile_system()}])
            self.assertEqual(self.p.schema_texts, interpretation.parse_persona_compile(reply, mixin_llm.DEFAULT_PROFILE)['schema'])
            self.p._persona_compiled_hash = ''
            self.provider(reply, True)
            self.run_async(self.p._compile_profile(self.event))
            self.assertEqual(self.p.profile, mixin_llm.DEFAULT_PROFILE)

    def test_memory_summary_arguments_parsing_and_error(self):
        texts = ['alpha memory', 'different memory']
        self.p._begin_job = Mock()
        self.p._here = Mock(return_value='private:10001')
        self.p._memory_thresholds = Mock(return_value=(True, 0, 0))
        self.p._cosine = Mock(return_value=1)
        self.p._embed_text_guarded = AsyncMock(return_value=[])
        self.p._load_memory = Mock(side_effect=lambda event: {'entries': [{'text': x} for x in texts]})
        self.p._end_job = Mock()
        reply = '{"summary": "combined", "candidates": []}'
        for fail in (False, True):
            provider = self.provider(reply, fail)
            self.p._embed_text_guarded.reset_mock()
            self.run_async(self.p._consolidate_memory(self.event, force=True))
            self.assertEqual(provider.calls, [{'prompt': interpretation.memory_summary_prompt(texts)}])
            if fail:
                self.p._embed_text_guarded.assert_not_awaited()
            else:
                self.assertEqual(self.p._embed_text_guarded.await_args.args[0], 'combined')

    def test_event_regenerate_arguments_parsing_and_error(self):
        record = {'source_texts': ['alpha event'], 'title': 'old'}
        reply = '{"big_summary": "big result", "small_summary": "small result"}'
        for fail in (False, True):
            provider = self.provider(reply, fail)
            result = self.run_async(self.p._regenerate_event_summary_fields(record))
            self.assertEqual(provider.calls, [{'prompt': interpretation.event_summary_prompt(['alpha event'])}])
            self.assertEqual(result['summary_status'], 'fallback' if fail else 'llm')
            if not fail:
                self.assertEqual(result['big_summary'], 'big result')

    def test_insight_arguments_parsing_and_error(self):
        events = [{'id': 'one', 'event': 'alpha'}]
        reply = '{"insight": "a pattern"}'
        self.p._append_insight = Mock()
        for fail in (False, True):
            provider = self.provider(reply, fail)
            self.p._append_insight.reset_mock()
            result = self.run_async(self.p._generate_insight(self.event, None, events))
            self.assertEqual(provider.calls, [{'prompt': interpretation.insight_prompt(events)}])
            self.assertEqual(result, not fail)
            if not fail:
                self.assertEqual(self.p._append_insight.call_args.args[0]['insight'], 'a pattern')
            else:
                self.p._append_insight.assert_not_called()

    def test_strong_event_arguments_parsing_and_error(self):
        texts = ['alpha event']
        reply = '{"event": "alpha event", "big_summary": "big result", "small_summary": "small result"}'
        core = SimpleNamespace(_intensity=lambda: 0.8, v=0, a=0, stress=0, labels={}, appraisal={})
        self.p._event_provenance = Mock(return_value={})
        self.p._source_check = Mock(return_value={})
        self.p._secondary_emotion = Mock(return_value='')
        self.p._event_emotion_intensity = Mock(return_value=0.8)
        self.p._event_worthiness_for = Mock(return_value=None)
        self.p._find_any_duplicate_event = Mock(return_value=None)
        self.p._event_boundary = Mock(return_value={})
        self.p._append_event_archive = Mock()
        self.p._maybe_archive_insight = AsyncMock()
        for fail in (False, True):
            provider = self.provider(reply, fail)
            self.p._append_event_archive.reset_mock()
            self.run_async(self.p._archive_strong_event(self.event, core, texts, 'alpha event'))
            self.assertEqual(provider.calls, [{'prompt': interpretation.event_summary_prompt(texts)}])
            if fail:
                self.p._append_event_archive.assert_not_called()
            else:
                self.assertEqual(self.p._append_event_archive.call_args.args[0]['big_summary'], 'big result')

    def test_impressions_arguments_parsing_and_error(self):
        self.p._impressions_time_reached = Mock(return_value=True)
        self.p._window_places = Mock(return_value=['group:900001'])
        self.p._read_window = Mock(return_value={'recent': []})
        self.p._impression_store = Mock()
        self.p._registry = Mock()
        self.p._material_names = Mock(return_value={})
        self.p._red_lines_for = Mock()
        self.p._judgements_for = Mock()
        async def nightly(store, place, lines, ask, day, **kwargs):
            return {'called': True, 'parsed': json.loads(await ask('impression prompt'))}
        for fail in (False, True):
            provider = self.provider('{"value": 7}', fail)
            with patch.object(mixin_impressions.impressions, 'nightly', nightly):
                result = self.run_async(self.p._maybe_update_impressions())
            self.assertEqual(provider.calls, [{'prompt': 'impression prompt'}])
            self.assertEqual(result, {} if fail else {'group:900001': {'called': True, 'parsed': {'value': 7}}})

    def test_plugin_mro_has_one_ports_mixin(self):
        self.assertEqual(main.BioCorePlugin.__mro__.count(PortsMixin), 1)
