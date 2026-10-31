# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""A small Windows DPAPI-backed store for application keys."""
import base64
import binascii
import ctypes
import json
import os
import re
import tempfile
from pathlib import Path

try:
    from . import atomic_file
except ImportError:
    import atomic_file

ENTROPY = b'ams-life key store v1'
MAX_VALUE_CHARS = 4096
NAME_CHARS = re.compile(r'^[a-z][a-z0-9_]{0,39}$')


class KeyStoreError(Exception):
    """Something went wrong; the message never holds a key."""


class _Blob(ctypes.Structure):
    _fields_ = [('size', ctypes.c_ulong), ('data', ctypes.POINTER(ctypes.c_ubyte))]


def _blob(data):
    buffer = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
    return _Blob(len(data), buffer), buffer


def _crypt(data, protect):
    source, source_buffer = _blob(data)
    entropy, entropy_buffer = _blob(ENTROPY)
    result = _Blob()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    function = crypt32.CryptProtectData if protect else crypt32.CryptUnprotectData
    function.argtypes = [ctypes.POINTER(_Blob), ctypes.c_void_p, ctypes.POINTER(_Blob),
                         ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_Blob)]
    function.restype = ctypes.c_int
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    kernel32.LocalFree.restype = ctypes.c_void_p
    if not function(ctypes.byref(source), None, ctypes.byref(entropy), None, None, 1, ctypes.byref(result)):
        raise KeyStoreError('cannot encrypt' if protect else 'cannot decrypt')
    try:
        return ctypes.string_at(result.data, result.size)
    finally:
        kernel32.LocalFree(result.data)


class KeyStore:
    def __init__(self, path):
        self.path = Path(path)

    def _read(self):
        try:
            with self.path.open(encoding='utf-8') as file:
                data = json.load(file)
            if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1:
                return {}
            keys = data.get('keys')
            if not isinstance(keys, dict) or any(not isinstance(k, str) or not NAME_CHARS.fullmatch(k)
                                                 or not isinstance(v, str) for k, v in keys.items()):
                return {}
            return keys
        except (OSError, ValueError, UnicodeError):
            return {}

    def _write(self, keys):
        tmp = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=self.path.parent,
                                             prefix='.key-store-', delete=False) as file:
                tmp = file.name
                json.dump({'version': 1, 'keys': keys}, file)
            atomic_file.replace(tmp, self.path)
        finally:
            if tmp is not None and os.path.exists(tmp):
                os.unlink(tmp)

    def set(self, name, value):
        if not isinstance(name, str) or not NAME_CHARS.fullmatch(name):
            raise KeyStoreError('invalid name')
        if not isinstance(value, str) or not value.strip() or len(value) > MAX_VALUE_CHARS:
            raise KeyStoreError('invalid value')
        if os.name != 'nt':
            raise KeyStoreError('DPAPI is only on Windows')
        try:
            encrypted = _crypt(value.encode('utf-8'), True)
        except (UnicodeError, OSError, ValueError):
            raise KeyStoreError('cannot encrypt') from None
        keys = self._read()
        keys[name] = base64.b64encode(encrypted).decode('ascii')
        self._write(keys)

    def get(self, name):
        if os.name != 'nt':
            raise KeyStoreError('DPAPI is only on Windows')
        keys = self._read()
        if name not in keys:
            raise KeyStoreError('not set')
        try:
            return _crypt(base64.b64decode(keys[name], validate=True), False).decode('utf-8')
        except (binascii.Error, UnicodeError, ValueError, OSError, KeyStoreError):
            raise KeyStoreError('cannot decrypt') from None

    def has(self, name):
        return name in self._read()

    def clear(self, name):
        keys = self._read()
        if name not in keys:
            return False
        del keys[name]
        self._write(keys)
        return True

    def names(self):
        return list(self._read())

    def status(self):
        return {name: True for name in self._read()}

    def __repr__(self):
        return f'KeyStore(path={str(self.path)!r}, names={len(self._read())})'
