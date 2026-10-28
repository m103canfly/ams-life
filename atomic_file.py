# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Putting a freshly written temp file in place of the old one (os.replace), a few times over.

On Windows a file that is open for reading (a virus scanner, a backup, another
program) cannot be replaced: os.replace raises PermissionError while it is open.
Her writes all go "temp file, then os.replace"; without trying again, that one
write would just be lost (a phone line, a turn of memory) with a warning in the log.

Only the standard library; no AstrBot.
"""
from __future__ import annotations

import os
import time

WAITS = (0.005, 0.01, 0.02, 0.04, 0.08, 0.1, 0.15, 0.2)   # seconds; about 0.6 s in all, then it gives up


def replace(tmp, path) -> None:
    """os.replace(tmp, path); while the target is held open elsewhere (PermissionError),
    wait a little and try again. Anything else, or the last try failing, raises as before."""
    for wait in WAITS:
        try:
            os.replace(str(tmp), str(path))
            return
        except PermissionError:
            time.sleep(wait)
    os.replace(str(tmp), str(path))
