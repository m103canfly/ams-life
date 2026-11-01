# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Owner-only Qzone posts with privacy checks and a daily limit."""
import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime

try:
    from . import discretion, redline, mixin_turn
    from .common import STATE_DIR
except ImportError:
    import discretion
    import redline
    import mixin_turn
    from common import STATE_DIR

logger = logging.getLogger('ams-life.qzone')
_lock = asyncio.Lock()
_tid = re.compile(r'[A-Za-z0-9]{1,64}\Z')
_numbers = re.compile(r'\d{5,}')


def _read():
    path = STATE_DIR / 'qzone.json'
    if not path.exists():
        return {'posts': [], 'days': {}}
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not isinstance(data.get('posts'), list) or not isinstance(data.get('days', {}), dict):
        raise ValueError('invalid state')
    data.setdefault('days', {})
    return data


def _write(data):
    path = STATE_DIR / 'qzone.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    temp.replace(path)


def _blocked(reason):
    logger.info('[ams-life] qzone not sent (%s)', reason)
    return None, reason


async def post(plugin, text, photo=None):
    """Send one checked post and return its id and an error category."""
    async with _lock:
        try:
            config = plugin.config or {}
            if not config.get('qzone_enabled', False):
                return _blocked('disabled')
            owner = str(config.get('owner_qq') or '').strip()
            if not owner or not owner.isascii() or not owner.isdigit():
                return _blocked('owner')
            data = _read()
            now = datetime.now()
            day = now.date().isoformat()
            if data['days'].get(day, 0) >= 2:
                return _blocked('limit')
            if not isinstance(text, str):
                return _blocked('text')
            if redline.hit(text):
                return _blocked('redline')
            if mixin_turn._copies_owner_rule(text, plugin._owner_rules()):
                return _blocked('owner_rule')
            people = [p for p in plugin._names_index() if str(p) != owner]
            names = [n for n in plugin._known_names(people) if not str(n).isdigit()]
            text = _numbers.sub('[号码]', discretion.anonymize(text, names)).strip()
            if not text or len(text) > 300:
                return _blocked('text')
            params = {'content': text, 'ugc_right': 16, 'target_uins': [owner]}
            if photo is not None:
                params['images'] = [str(photo)]
            data['days'] = {day: data['days'].get(day, 0) + 1}
            _write(data)
            result = await plugin._neutral_messenger.call('send_qzone_msg', **params)
            tid = result.get('tid') if isinstance(result, dict) else None
            if not isinstance(tid, str) or not _tid.fullmatch(tid):
                return _blocked('response')
            data['posts'].append({'tid': tid, 'ts': now.isoformat(),
                                  'text_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest()})
            _write(data)
            return tid, ''
        except Exception as exc:
            return _blocked(type(exc).__name__)


async def delete(plugin, tid):
    """Delete only a post in the local record."""
    async with _lock:
        try:
            if not isinstance(tid, str) or not _tid.fullmatch(tid):
                return False
            data = _read()
            if not any(p.get('tid') == tid for p in data['posts']):
                return False
            await plugin._neutral_messenger.call('delete_qzone_msg', tid=tid)
            data['posts'] = [p for p in data['posts'] if p.get('tid') != tid]
            _write(data)
            return True
        except Exception as exc:
            logger.warning('[ams-life] qzone delete failed (%s)', type(exc).__name__)
            return False
