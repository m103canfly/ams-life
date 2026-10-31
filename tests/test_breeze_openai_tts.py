# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for the Breeze bridge."""
import asyncio
import email.policy
import importlib.util
import io
import sys
import tempfile
import threading
import time
import types
import unittest
import urllib.error
import wave
from email.parser import BytesParser
from pathlib import Path
from unittest.mock import MagicMock, patch


def load_bridge():
    fastapi = types.ModuleType('fastapi')

    class FakeApp:
        """Route decorators hand the function back, so the tests can call the routes."""
        def __init__(self, **kwargs):
            pass

        def get(self, path):
            return lambda function: function

        def post(self, path):
            return lambda function: function

    fastapi.FastAPI = FakeApp
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code, self.detail = status_code, detail
    fastapi.HTTPException, fastapi.Request = HTTPException, object
    responses = types.ModuleType('fastapi.responses')
    responses.Response = MagicMock
    modules = {'fastapi': fastapi, 'fastapi.responses': responses,
               'uvicorn': types.ModuleType('uvicorn')}
    spec = importlib.util.spec_from_file_location('breeze_bridge_test',
        Path(__file__).resolve().parent.parent / 'tools' / 'breeze_openai_tts.py')
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module


def parts(body, content_type):
    msg = BytesParser(policy=email.policy.default).parsebytes(
        ('Content-Type: ' + content_type + '\r\nMIME-Version: 1.0\r\n\r\n').encode() + body)
    return {part.get_param('name', header='content-disposition'): part for part in msg.iter_parts()}


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = load_bridge()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.tmp.cleanup)
        self.ref = Path(self.tmp.name) / 'reference.wav'
        self.ref.write_bytes(b'clip')
        self.c = dict(self.b.DEFAULT, ref_audio=str(self.ref), ref_text='sample reference')

    def test_local_url(self):
        for url in ('http://127.0.0.1:7860', 'http://localhost', 'http://[::1]:7860'):
            self.assertTrue(self.b.local_url(url), url)
        for url in ('http://192.168.1.5:7860', 'http://example.test',
                    'https://127.0.0.1.example.test', 'http://localhost@evil.test',
                    'http://localhost:invalid', 'http://localhost/path', 'http://localhost?x=1'):
            self.assertFalse(self.b.local_url(url), url)

    def test_ref_ok(self):
        self.assertTrue(self.b.ref_ok(self.c))
        for path, text in ((self.ref / 'missing', 'words'), (Path(self.tmp.name), 'words'),
                           (self.ref, '  ')):
            self.assertFalse(self.b.ref_ok(dict(self.c, ref_audio=str(path), ref_text=text)))
        with self.ref.open('wb') as f:
            f.truncate(20 * 1024 * 1024 + 1)
        self.assertFalse(self.b.ref_ok(self.c))

    def test_multipart(self):
        fields = {'text': '[laugh] hello', 'ref_text': 'reference', 'cfg_scale': 1, 'seed': 1234}
        body, ct = self.b.multipart(fields, 'ref_audio', 'reference.wav', b'clip')
        parsed = parts(body, ct)
        self.assertEqual(set(parsed), set(fields) | {'ref_audio'})
        for key, value in fields.items():
            self.assertEqual(parsed[key].get_content(), str(value))
        self.assertEqual(parsed['ref_audio'].get_filename(), 'reference.wav')
        self.assertEqual(parsed['ref_audio'].get_payload(decode=True), b'clip')

    def test_sample_rate(self):
        for headers, expected in (({'X-Sample-Rate': '24000'}, 24000),
                                  ({'X-Sample-Rate': '48000'}, 48000), ({}, 24000),
                                  ({'X-Sample-Rate': 'abc'}, 24000),
                                  ({'X-Sample-Rate': '999999'}, 24000)):
            self.assertEqual(self.b.sample_rate_of(headers), expected)

    def test_pcm_to_wav(self):
        pcm = b'\x01\x02\x03\x04'
        with wave.open(io.BytesIO(self.b.pcm_to_wav(pcm, 16000))) as f:
            self.assertEqual((f.getnchannels(), f.getsampwidth(), f.getframerate(), f.getnframes()),
                             (1, 2, 16000, 2))
            self.assertEqual(f.readframes(2), pcm)
        for data in (b'', b'1'):
            with self.assertRaises(ValueError):
                self.b.pcm_to_wav(data, 24000)

    def test_call_breeze_request(self):
        class Response:
            headers = {'X-Sample-Rate': '16000'}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return b'\x00\x01'
        def opener(req, timeout):
            self.assertEqual(req.full_url, self.c['breeze_url'] + '/v1/audio/speech')
            self.assertEqual(timeout, 300)
            parsed = parts(req.data, req.get_header('Content-type'))
            self.assertEqual(parsed['text'].get_content(), '[laugh] hello')
            self.assertEqual(parsed['ref_text'].get_content(), 'sample reference')
            self.assertEqual(parsed['cfg_scale'].get_content(), '1')
            self.assertEqual(parsed['seed'].get_content(), str(self.c['seed']))
            self.assertEqual(parsed['ref_audio'].get_payload(decode=True), b'clip')
            return Response()
        self.assertEqual(self.b.call_breeze('[laugh] hello', self.c, opener=opener), (b'\x00\x01', 16000))

    def test_busy_retry(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'12'
        response.headers = {}
        error = urllib.error.HTTPError('http://localhost', 409, 'busy', {}, None)
        opener, sleep = MagicMock(side_effect=[error, response]), MagicMock()
        self.assertEqual(self.b.call_breeze('hello', self.c, opener=opener, sleep=sleep), (b'12', 24000))
        sleep.assert_called_once_with(2)
        opener = MagicMock(side_effect=error)
        with self.assertRaises(Exception):
            self.b.call_breeze('hello', self.c, opener=opener, sleep=MagicMock())
        self.assertEqual(opener.call_count, 2)

    def test_serialized_calls(self):
        active, peak = 0, 0
        guard = threading.Lock()
        barrier = threading.Barrier(3)
        def opener(req, timeout):
            nonlocal active, peak
            with guard:
                active += 1
                peak = max(peak, active)
            time.sleep(0.1)
            with guard: active -= 1
            response = MagicMock()
            response.__enter__.return_value = response
            response.read.return_value, response.headers = b'12', {}
            return response
        errors = []
        def run():
            barrier.wait()
            try: self.b.call_breeze('hello', self.c, opener=opener)
            except Exception as exc: errors.append(exc)
        threads = [threading.Thread(target=run) for _ in range(2)]
        for thread in threads: thread.start()
        barrier.wait()
        for thread in threads: thread.join()
        self.assertFalse(errors)
        self.assertEqual(peak, 1)

    def test_errors_hide_private_values_and_remote_blocked(self):
        opener = MagicMock(side_effect=OSError(str(self.ref) + ' sample reference'))
        with self.assertRaises(Exception) as cm:
            self.b.call_breeze('hello', self.c, opener=opener)
        self.assertNotIn(str(self.ref), str(cm.exception))
        self.assertNotIn('sample reference', str(cm.exception))
        opener.reset_mock()
        with self.assertRaises(Exception):
            self.b.call_breeze('hello', dict(self.c, breeze_url='http://example.test'), opener=opener)
        opener.assert_not_called()

    def test_speech_statuses(self):
        class Request:
            async def json(self): return {'input': 'hello'}
        for effect, status, detail in ((self.b.BusyError(), 503, 'busy'),
                                       (ValueError('private'), 502, 'Breeze failed')):
            with patch.object(self.b, 'conf', return_value=self.c), patch.object(self.b, 'call_breeze', side_effect=effect):
                with self.assertRaises(self.b.HTTPException) as cm:
                    asyncio.run(self.b.speech(Request()))
                self.assertEqual((cm.exception.status_code, cm.exception.detail), (status, detail))

    def tone_entry(self, name, text):
        path = Path(self.tmp.name) / name
        path.write_bytes(name.encode())
        return {'ref_audio': str(path), 'ref_text': text}

    def speak_with_config(self, config, voice):
        class Request:
            async def json(self): return {'input': 'hello', 'voice': voice}
        with patch.object(self.b, 'conf', return_value=config), \
                patch.object(self.b, 'call_breeze', return_value=(b'12', 24000)) as call:
            asyncio.run(self.b.speech(Request()))
        return call.call_args.args[1]

    def test_tones_choose_first_for_each_voice(self):
        tones = {name: [self.tone_entry(str(i), 'first ' + str(i)),
                        self.tone_entry('backup' + str(i), 'second ' + str(i))]
                 for i, name in enumerate(('开心', '平静', '温柔', '认真', '难过'))}
        for name, entries in tones.items():
            with self.subTest(name=name):
                selected = self.speak_with_config(dict(self.c, tones=tones), name)
                self.assertEqual((selected['ref_audio'], selected['ref_text']),
                                 (entries[0]['ref_audio'], entries[0]['ref_text']))

    def test_tone_uses_second_when_first_missing(self):
        missing = {'ref_audio': str(Path(self.tmp.name) / 'missing'), 'ref_text': 'missing'}
        backup = self.tone_entry('backup', 'backup words')
        selected = self.speak_with_config(dict(self.c, tones={'开心': [missing, backup]}), '开心')
        self.assertEqual((selected['ref_audio'], selected['ref_text']),
                         (backup['ref_audio'], backup['ref_text']))

    def test_unknown_voice_uses_calm(self):
        calm = self.tone_entry('calm', 'calm words')
        other = self.tone_entry('other', 'other words')
        config = dict(self.c, tones={'平静': [calm], '': [other], 'alloy': [other], 'v4': [other]})
        for voice in ('', 'alloy', 'v4', 'unknown', None, [], {}):
            with self.subTest(voice=voice):
                self.assertEqual(self.speak_with_config(config, voice)['ref_text'], 'calm words')

    def test_tone_fallback_chain_and_unavailable(self):
        bad = {'ref_audio': str(Path(self.tmp.name) / 'missing'), 'ref_text': 'missing'}
        calm = self.tone_entry('calm', 'calm words')
        config = dict(self.c, tones={'开心': [bad], '平静': [calm]})
        self.assertEqual(self.speak_with_config(config, '开心')['ref_text'], 'calm words')
        config['tones']['平静'] = [bad]
        self.assertEqual(self.speak_with_config(config, '开心')['ref_text'], 'sample reference')
        config['ref_audio'] = bad['ref_audio']
        class Request:
            async def json(self): return {'input': 'hello', 'voice': '开心'}
        with patch.object(self.b, 'conf', return_value=config), \
                patch.object(self.b, 'call_breeze') as call:
            with self.assertRaises(self.b.HTTPException) as cm:
                asyncio.run(self.b.speech(Request()))
            self.assertEqual(cm.exception.status_code, 503)
            call.assert_not_called()

    def test_old_config_uses_top_level_reference(self):
        selected = self.speak_with_config(self.c, '开心')
        self.assertEqual((selected['ref_audio'], selected['ref_text']),
                         (self.c['ref_audio'], self.c['ref_text']))

    def test_selected_reference_reaches_breeze(self):
        entry = self.tone_entry('selected', 'selected reference words')
        config = dict(self.c, tones={'温柔': [entry]})
        class Request:
            async def json(self): return {'input': 'hello', 'voice': '温柔'}
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value, response.headers = b'12', {}
        def opener(req, timeout):
            parsed = parts(req.data, req.get_header('Content-type'))
            self.assertEqual(parsed['ref_text'].get_content(), entry['ref_text'])
            self.assertEqual(parsed['ref_audio'].get_filename(), 'reference.wav')
            self.assertEqual(parsed['ref_audio'].get_payload(decode=True), b'selected')
            return response
        original = self.b.call_breeze
        with patch.object(self.b, 'conf', return_value=config), \
                patch.object(self.b, 'call_breeze', side_effect=lambda text, c: original(text, c, opener=opener)):
            asyncio.run(self.b.speech(Request()))
