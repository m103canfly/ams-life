# ams-life (AGPL-3.0); see NOTICE.md.
"""Test the bridge payload without installing its server dependencies or starting it."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


def load_bridge():
    fastapi = types.ModuleType('fastapi')
    fastapi.FastAPI = MagicMock
    fastapi.HTTPException = Exception
    fastapi.Request = object
    responses = types.ModuleType('fastapi.responses')
    responses.JSONResponse = responses.Response = object
    modules = {'fastapi': fastapi, 'fastapi.responses': responses,
               'uvicorn': types.ModuleType('uvicorn')}
    path = Path(__file__).resolve().parent.parent / 'tools' / 'gsv_openai_tts.py'
    spec = importlib.util.spec_from_file_location('gsv_openai_tts_test', path)
    bridge = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(bridge)
    return bridge


class BridgePayload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bridge = load_bridge()

    def test_config_values_are_included_and_converted(self):
        payload = self.bridge.speech_payload('hello', {}, {'temperature': '1.3', 'top_k': '30'})
        self.assertEqual(payload['temperature'], 1.3)
        self.assertIs(type(payload['temperature']), float)
        self.assertEqual(payload['top_k'], 30)
        self.assertIs(type(payload['top_k']), int)

    def test_absent_values_are_omitted(self):
        payload = self.bridge.speech_payload('hello', {}, {})
        self.assertNotIn('temperature', payload)
        self.assertNotIn('top_k', payload)
        self.assertEqual(payload['speed_factor'], 1.0)

    def test_request_overrides_config(self):
        payload = self.bridge.speech_payload('hello', {'temperature': 0, 'top_k': '12'},
                                             {'temperature': 1.3, 'top_k': 30})
        self.assertEqual(payload['temperature'], 0.0)
        self.assertEqual(payload['top_k'], 12)

    def test_invalid_values_are_omitted(self):
        for body, config in (({}, {'temperature': 'bad', 'top_k': []}),
                             ({'temperature': None, 'top_k': 'bad'},
                              {'temperature': 1.3, 'top_k': 30}),
                             ({'top_k': float('inf')}, {})):
            with self.subTest(body=body, config=config):
                payload = self.bridge.speech_payload('hello', body, config)
                self.assertNotIn('temperature', payload)
                self.assertNotIn('top_k', payload)


if __name__ == '__main__':
    unittest.main()
