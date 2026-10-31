# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for the DPAPI key store."""
import ast
import base64
import ctypes
import json
import os
import tempfile
import unittest
from pathlib import Path

from key_store import KeyStore, KeyStoreError, MAX_VALUE_CHARS

ROOT = Path(__file__).resolve().parent.parent
VALUE = 'test-value-0000'


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'keys.json'
        self.store = KeyStore(self.path)

    def test_validation_and_safe_errors(self):
        for name in ('', 'Upper', 'a' * 41, 'has space'):
            with self.subTest(name=name), self.assertRaises(KeyStoreError) as error:
                self.store.set(name, VALUE)
            self.assertNotIn(VALUE, str(error.exception))
        for value in ('', '  ', 'x' * (MAX_VALUE_CHARS + 1), None):
            with self.subTest(value=type(value).__name__), self.assertRaises(KeyStoreError) as error:
                self.store.set('valid', value)
            if isinstance(value, str) and value.strip():
                self.assertNotIn(value, str(error.exception))
        self.assertNotIn(VALUE, repr(self.store))

    def test_bad_files_are_empty(self):
        for content in ('not json', '{"version": 2, "keys": {"valid": "blob"}}',
                        '{"version": 1, "keys": []}'):
            self.path.write_text(content, encoding='utf-8')
            self.assertEqual(self.store.names(), [])
            self.assertEqual(self.store.status(), {})
            self.assertFalse(self.store.has('valid'))
            self.assertFalse(self.store.clear('valid'))

    def test_status_contains_only_names_and_booleans(self):
        self.path.write_text(json.dumps({'version': 1, 'keys': {'valid': 'opaque'}}), encoding='utf-8')
        self.assertEqual(self.store.status(), {'valid': True})
        self.assertEqual(self.store.names(), ['valid'])
        self.assertTrue(self.store.has('valid'))
        self.assertNotIn('opaque', repr(self.store))
        self.assertTrue(self.store.clear('valid'))
        self.assertFalse(self.store.clear('valid'))

    def test_module_has_no_forbidden_imports_or_print(self):
        tree = ast.parse((ROOT / 'key_store.py').read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(n.name.split('.')[0] in ('astrbot', 'logging') for n in node.names))
            if isinstance(node, ast.ImportFrom):
                self.assertNotIn((node.module or '').split('.')[0], ('astrbot', 'logging'))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotEqual(node.func.id, 'print')

    @unittest.skipIf(os.name == 'nt', 'non-Windows behavior')
    def test_non_windows(self):
        for call in (lambda: self.store.set('valid', VALUE), lambda: self.store.get('valid')):
            with self.assertRaisesRegex(KeyStoreError, '^DPAPI is only on Windows$'):
                call()


@unittest.skipUnless(os.name == 'nt', 'DPAPI requires Windows')
class WindowsStoreTest(StoreTest):
    def test_round_trip_clear_and_reopen(self):
        value = '  ' + VALUE + '  '
        self.store.set('valid', value)
        self.assertEqual(self.store.get('valid'), value)
        self.assertEqual(KeyStore(self.path).get('valid'), value)
        self.assertTrue(self.store.has('valid'))
        self.assertEqual(self.store.names(), ['valid'])
        self.assertEqual(self.store.status(), {'valid': True})
        self.assertNotIn(value, repr(self.store))
        self.assertTrue(self.store.clear('valid'))
        with self.assertRaisesRegex(KeyStoreError, '^not set$'):
            self.store.get('valid')

    def test_file_has_no_plaintext_or_base64_plaintext(self):
        self.store.set('valid', VALUE)
        data = self.path.read_bytes()
        self.assertNotIn(VALUE.encode(), data)
        self.assertNotIn(base64.b64encode(VALUE.encode()), data)

    def test_modified_blob_cannot_decrypt(self):
        self.store.set('valid', VALUE)
        data = json.loads(self.path.read_text(encoding='utf-8'))
        blob = bytearray(base64.b64decode(data['keys']['valid']))
        blob[-1] ^= 1
        data['keys']['valid'] = base64.b64encode(blob).decode('ascii')
        self.path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(KeyStoreError, '^cannot decrypt$') as error:
            self.store.get('valid')
        self.assertNotIn(VALUE, str(error.exception))

    def test_blob_without_entropy_cannot_decrypt(self):
        class Blob(ctypes.Structure):
            _fields_ = [('size', ctypes.c_ulong), ('data', ctypes.POINTER(ctypes.c_ubyte))]
        buf = (ctypes.c_ubyte * len(VALUE.encode())).from_buffer_copy(VALUE.encode())
        source = Blob(len(buf), buf)
        result = Blob()
        crypt = ctypes.windll.crypt32.CryptProtectData
        crypt.argtypes = [ctypes.POINTER(Blob), ctypes.c_wchar_p, ctypes.POINTER(Blob),
                          ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(Blob)]
        crypt.restype = ctypes.c_int
        free = ctypes.windll.kernel32.LocalFree
        free.argtypes = [ctypes.c_void_p]
        free.restype = ctypes.c_void_p
        self.assertTrue(crypt(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(result)))
        try:
            blob = ctypes.string_at(result.data, result.size)
        finally:
            free(result.data)
        self.path.write_text(json.dumps({'version': 1, 'keys': {'valid': base64.b64encode(blob).decode('ascii')}}), encoding='utf-8')
        with self.assertRaisesRegex(KeyStoreError, '^cannot decrypt$'):
            self.store.get('valid')

    def test_bad_file_is_rewritten_on_set(self):
        for content in ('bad json', '{"version": 2, "keys": {}}'):
            self.path.write_text(content, encoding='utf-8')
            self.store.set('valid', VALUE)
            self.assertEqual(self.store.get('valid'), VALUE)
            self.assertEqual(json.loads(self.path.read_text(encoding='utf-8'))['version'], 1)
