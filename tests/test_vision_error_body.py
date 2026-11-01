# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline checks for vision HTTP error logging."""
import asyncio
import io
import sys
import types
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import vision


class VisionErrorBodyTest(unittest.TestCase):
    def request(self, stream, key='sk-test-xxxxxxxx'):
        plugin = types.SimpleNamespace(
            api_config={'image': {'base_url': 'https://vision.invalid/v1', 'api_key': key}},
            config={'vision_image_api_model': 'fictional-vision'})

        def fail(req, timeout):
            raise urllib.error.HTTPError(req.full_url, 400, 'rejected', {}, stream)

        with patch('urllib.request.urlopen', side_effect=fail), patch.object(vision.logger, 'warning') as warning:
            with self.assertRaises(RuntimeError) as error:
                asyncio.run(vision.ImageAPI(plugin).text_chat())
        self.assertEqual(str(error.exception), 'vision request failed')
        self.assertIsNone(error.exception.__cause__)
        return warning

    def test_chinese_error_body(self):
        body = '{"error":{"message":"仅支持含 role/content 的非空纯文字消息"}}'
        warning = self.request(io.BytesIO(body.encode('utf-8')))
        warning.assert_called_once_with('[ams-life] vision request status %d: %s', 400, body)

    def test_body_is_bounded_and_single_line(self):
        stream = Mock()
        stream.read.return_value = ('  ' + 'a' * 100 + '\n\r\t' + 'b' * 900).encode('utf-8')
        warning = self.request(stream)
        stream.read.assert_called_once_with(4096)
        args = warning.call_args.args
        self.assertEqual(args[:2], ('[ams-life] vision request status %d: %s', 400))
        self.assertEqual(len(args[2]), 200)
        self.assertNotRegex(args[2], r'[\n\r\t]')
        self.assertEqual(args[2], 'a' * 100 + '   ' + 'b' * 97)

    def test_key_is_redacted_from_log_and_exception(self):
        key = 'sk-test-xxxxxxxx'
        warning = self.request(io.BytesIO(('bad key: ' + key).encode('utf-8')), key)
        warning.assert_called_once_with('[ams-life] vision request status %d: %s', 400, 'bad key: ***')
        self.assertNotIn(key, str(warning.call_args))

    def test_empty_or_unreadable_body_logs_only_status(self):
        broken = Mock()
        broken.read.side_effect = OSError('unavailable')
        for stream in (io.BytesIO(b''), broken):
            with self.subTest(stream=type(stream).__name__):
                warning = self.request(stream)
                warning.assert_called_once_with('[ams-life] vision request status %d', 400)

    def test_invalid_utf8_is_replaced(self):
        warning = self.request(io.BytesIO(b'bad \xff body'))
        warning.assert_called_once_with('[ams-life] vision request status %d: %s', 400, 'bad \ufffd body')


if __name__ == '__main__':
    unittest.main()
