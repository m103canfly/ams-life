# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for neutral vision routing and key selection."""
import asyncio
import ast
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import harness
import mixin_llm
import vision


# mixin_llm.py 669-705 at 7c8f5d3.
OLD_ROUTING = '''\
def old_vision_provider_for(self, event=None, source="reply"):
    _cfg = self._function_cfg("image_caption")
    _override = _cfg["provider"]
    if _override == "image_api":
        if not str((getattr(self, "config", {}) or {}).get("vision_image_api_model") or "").strip():
            return None
        return VisionGate(self, _counted(self, "vision", ImageAPI(self)), event, source)
    _tried = []
    if _override and _override not in ("follow_llm", "main", "default", ""):
        _tried.append(_override)
    try:
        _cfg_all = self.context.get_config()
        _ps = _cfg_all.get("provider_settings", {}) if isinstance(_cfg_all, dict) else {}
        _def = str(_ps.get("default_image_caption_provider_id") or "")
    except Exception:
        _def = ""
    if _def and _def not in _tried:
        _tried.append(_def)
    for _pid in _tried:
        try:
            _vp = self.context.get_provider_by_id(_pid)
        except Exception as exc:
            logger.warning("[biocore] vision provider lookup failed (%s): %s", _pid, exc)
            continue
        if _vp is not None and self._sees_images(_vp):
            return VisionGate(self, _counted(self, "vision", _vp), event, source) if hasattr(self, "_load_image_cache") else _counted(self, "vision", _vp)
        if _vp is not None:
            logger.warning("[biocore] image_caption provider %s is not a vision provider; ignored", _pid)
    try:
        _umo = str(getattr(event, "unified_msg_origin", "") or "") if event is not None else None
        _chat = self.context.get_using_provider(_umo)
    except Exception:
        _chat = None
    if _chat is not None and self._sees_images(_chat):
        return VisionGate(self, _counted(self, "vision", _chat), event, source) if hasattr(self, "_load_image_cache") else _counted(self, "vision", _chat)
    return None
'''
_old_namespace = dict(vars(mixin_llm))
exec(OLD_ROUTING, _old_namespace)
old_vision_provider_for = _old_namespace['old_vision_provider_for']


def plugin(override='follow_llm'):
    obj = mixin_llm.LLMMixin()
    obj.config = {'vision_image_api_model': 'fictional-vision', 'slang_image_api_model': 'fictional-slang'}
    obj.llm_functions = {'image_caption': {'provider': override}}
    obj.api_config = {'image': {'base_url': 'https://vision.invalid/v1', 'api_key': 'config-fictional-key'}}
    obj.context = harness.FakeContext()
    return obj


class RoutingTest(unittest.TestCase):
    def test_neutral_routes_to_image_api_without_context(self):
        obj = plugin()
        obj._neutral_model = object()
        obj.context = Mock(spec=harness.FakeContext)
        for name in ('get_config', 'get_provider_by_id', 'get_using_provider'):
            getattr(obj.context, name).side_effect = AssertionError('context called')
        gate = obj._vision_provider_for(source='browse')
        self.assertIsInstance(gate, vision.VisionGate)
        self.assertIsInstance(gate.provider, vision.ImageAPI)
        self.assertEqual(gate.source, 'browse')
        self.assertEqual(obj.context.method_calls, [])

    def test_neutral_without_model_returns_none(self):
        obj = plugin()
        obj._neutral_model = object()
        obj.config['vision_image_api_model'] = ''
        obj.context = Mock(spec=harness.FakeContext)
        self.assertIsNone(obj._vision_provider_for())
        self.assertEqual(obj.context.method_calls, [])

    def test_astrbot_matches_frozen_routing(self):
        for override in ('image_api', 'follow_llm'):
            with self.subTest(override=override):
                obj = plugin(override)
                obj.context.provider.provider_config['modalities'] = ['text', 'image']
                old = old_vision_provider_for(obj)
                new = obj._vision_provider_for()
                self.assertEqual(type(new), type(old))
                if override == 'image_api':
                    self.assertIsInstance(new.provider, vision.ImageAPI)
                    self.assertIsInstance(old.provider, vision.ImageAPI)
                else:
                    self.assertIs(new, old)
                    self.assertIs(new, obj.context.provider)


class KeyTest(unittest.TestCase):
    def request(self, obj, model_config='vision_image_api_model', reject=False):
        sent = []
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return b'{"choices":[{"message":{"content":"picture"}}]}'
        def fake_open(req, timeout):
            sent.append(req)
            if reject:
                raise urllib.error.HTTPError(req.full_url, 401, 'rejected', {}, None)
            return Response()
        with patch('urllib.request.urlopen', side_effect=fake_open), patch.object(vision.logger, 'warning') as warning:
            if reject:
                with self.assertRaisesRegex(RuntimeError, '^vision request failed$'):
                    asyncio.run(vision.ImageAPI(obj).text_chat(model_config=model_config))
                warning.assert_called_once_with('[ams-life] vision request status %d', 401)
            else:
                result = asyncio.run(vision.ImageAPI(obj).text_chat(model_config=model_config))
                self.assertEqual(result.completion_text, 'picture')
                warning.assert_not_called()
        return sent[0]

    def test_store_key_overrides_config(self):
        obj = plugin()
        obj._key_store = Mock()
        obj._key_store.get.return_value = 'store-fictional-key'
        self.assertEqual(self.request(obj).get_header('Authorization'), 'Bearer store-fictional-key')
        obj._key_store.get.assert_called_once_with('vision')

    def test_store_error_sends_empty_key_and_warns_on_rejection(self):
        obj = plugin()
        obj._key_store = Mock()
        obj._key_store.get.side_effect = ValueError('unavailable')
        self.assertEqual(self.request(obj, reject=True).get_header('Authorization'), 'Bearer ')
        obj._key_store.get.assert_called_once_with('vision')

    def test_without_store_uses_config_key(self):
        self.assertEqual(self.request(plugin()).get_header('Authorization'), 'Bearer config-fictional-key')

    def test_slang_model_uses_store_key(self):
        obj = plugin()
        obj._key_store = Mock()
        obj._key_store.get.return_value = 'store-fictional-key'
        req = self.request(obj, model_config='slang_image_api_model')
        self.assertEqual(req.get_header('Authorization'), 'Bearer store-fictional-key')
        import json
        self.assertEqual(json.loads(req.data)['model'], 'fictional-slang')
        obj._key_store.get.assert_called_once_with('vision')

    def test_vision_has_no_astrbot_import(self):
        tree = ast.parse(Path(vision.__file__).read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertTrue(all(not alias.name.startswith('astrbot') for alias in node.names))
            elif isinstance(node, ast.ImportFrom):
                self.assertFalse((node.module or '').startswith('astrbot'))


if __name__ == '__main__':
    unittest.main()
