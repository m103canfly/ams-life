"""astrbot.api stand-in: a logger that keeps every record so tests can inspect warnings."""
import logging


class _Logger:
    def __init__(self):
        self.records = []

    def _log(self, level, msg, *args, **kwargs):
        try:
            text = (str(msg) % args) if args else str(msg)
        except Exception:
            text = str(msg) + ' ' + ' '.join(map(str, args))
        self.records.append((level, text))

    def debug(self, msg, *a, **k):
        self._log('debug', msg, *a, **k)

    def info(self, msg, *a, **k):
        self._log('info', msg, *a, **k)

    def warning(self, msg, *a, **k):
        self._log('warning', msg, *a, **k)

    warn = warning

    def error(self, msg, *a, **k):
        self._log('error', msg, *a, **k)

    def exception(self, msg, *a, **k):
        self._log('error', msg, *a, **k)


logger = _Logger()
