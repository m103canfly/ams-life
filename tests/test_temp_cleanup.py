# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check that tests using temporary directories mention cleanup."""
import unittest
from pathlib import Path


class TempCleanup(unittest.TestCase):
    def test_mkdtemp_files_mention_cleanup(self):
        missing = []
        for path in sorted(Path(__file__).resolve().parent.rglob('*.py')):
            source = path.read_text('utf-8')
            if 'mkdtemp(' in source and not any(word in source for word in ('rmtree', 'addCleanup', 'atexit')):
                missing.append(path.relative_to(Path(__file__).resolve().parent).as_posix())
        self.assertEqual(missing, [], 'Missing temporary directory cleanup: ' + ', '.join(missing))
