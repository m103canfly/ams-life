# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Dates remembered in the owner's private conversation."""
import datetime
import json
import re
import time
from pathlib import Path

try:
    from . import atomic_file
except ImportError:
    import atomic_file


def _path(root):
    return Path(root) / 'states' / 'our_days.json'


def _read(root):
    path = _path(root)
    if not path.exists():
        return []
    rows = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(rows, list):
        raise ValueError('invalid dates')
    return rows


def _write(root, rows):
    path = _path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    atomic_file.replace(tmp, path)


def _date(value):
    if not isinstance(value, str) or not re.fullmatch(r'(?:\d{4}-)?\d{2}-\d{2}', value):
        raise ValueError('invalid date')
    return datetime.date.fromisoformat(value if len(value) == 10 else '2000-' + value)


def remember(root, owner, date, what):
    _date(date)
    if not isinstance(what, str) or not what.strip() or len(what.strip()) > 20 or '\n' in what or '\r' in what:
        raise ValueError('invalid description')
    owner = str(owner or '').strip()
    if not owner:
        raise ValueError('missing owner')
    rows = _read(root)
    rows.append({'date': date, 'what': what.strip(),
                 'origin': {'where': 'private:' + owner, 'people': [owner], 'source_ids': [], 'visibility': 'private'},
                 'related_users': [owner], 'ts': time.time()})
    _write(root, rows)


def forget(root, person):
    rows = _read(root)
    kept = [row for row in rows if str(person) not in [str(x) for x in row.get('related_users', [])]]
    if len(kept) != len(rows):
        _write(root, kept)
    return len(rows) - len(kept)


def line(root, owner, today):
    items = []
    for row in _read(root):
        if not isinstance(row, dict) or str(owner) not in [str(x) for x in row.get('related_users', [])]:
            continue
        try:
            original = _date(row['date'])
            what = row['what']
            if not isinstance(what, str) or not what or len(what) > 20:
                continue
            upcoming = None
            for year in range(today.year, min(today.year + 9, 10000)):
                if len(row['date']) == 10 and year < original.year:
                    continue
                try:
                    candidate = original.replace(year=year)
                except ValueError:
                    continue
                if candidate >= today:
                    upcoming = candidate
                    break
            delta = (upcoming - today).days if upcoming else None
            text = ('今天是%s。' % what if delta == 0 else
                    '再过 %d 天是%s。' % (delta, what) if delta is not None and delta <= 7 else
                    '%s：%s。' % (row['date'], what))
            items.append((delta if delta is not None and delta <= 7 else 999999, text))
        except (KeyError, TypeError, ValueError, OverflowError):
            continue
    items.sort(key=lambda item: item[0])
    return '你们之间记下的日子：' + (' '.join(text for _, text in items) if items else '还没有。')
