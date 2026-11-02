# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Local records of her activities and archived notebook entries."""
import datetime
import json
import time
import uuid
from pathlib import Path

try:
    from . import discretion
except ImportError:
    import discretion


SECTIONS = ('习惯', '喜欢的', '最近在玩的', '想做的')


def notebook_sections(entries):
    result = {name: [] for name in (*SECTIONS, '未分')}
    for entry in entries or []:
        section = entry.get('section') if isinstance(entry, dict) else None
        result[section if section in SECTIONS else '未分'].append(entry)
    return result


def notebook_about(entry, person='', source_ids=None):
    return isinstance(entry, dict) and discretion.is_about(discretion.origin_of(entry), person, source_ids)


def _rows(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


def _write(path, rows):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')
    tmp.replace(path)


def archive_notebook(root, entries, deleted_at):
    if not entries:
        return
    path = Path(root) / 'notebook_archive.jsonl'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as out:
        for entry in entries:
            out.write(json.dumps(dict(entry, deleted_at=deleted_at), ensure_ascii=False) + '\n')


def forget_notebook_archive(root, person='', source_ids=None):
    path = Path(root) / 'notebook_archive.jsonl'
    if not path.exists():
        return 0
    rows = _rows(path)
    kept = [row for row in rows if not notebook_about(row, person, source_ids)]
    if len(kept) != len(rows):
        _write(path, kept)
    return len(rows) - len(kept)


class Store:
    def __init__(self, root):
        self.root = Path(root) / 'her_days'

    def _path(self, date):
        date = datetime.date.fromisoformat(str(date))
        return self.root / (date.isoformat() + '.jsonl')

    def add(self, entry):
        ts = entry.get('ts', time.time())
        row = {'id': str(entry.get('id') or uuid.uuid4().hex), 'ts': ts,
               'do': str(entry.get('do') or '')[:12], 'detail': str(entry.get('detail') or '')[:40],
               'minutes': entry.get('minutes'), 'feel': str(entry.get('feel') or '')[:40],
               'liked': str(entry.get('liked') or '')[:20],
               'work': str(entry.get('work') or '')[:40],
               'origin': dict(entry.get('origin') or {}, where='self'),
               'related_users': [str(x) for x in (entry.get('related_users') or [])]}
        path = self._path(datetime.datetime.fromtimestamp(ts).date())
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as out:
            out.write(json.dumps(row, ensure_ascii=False) + '\n')
        return row

    def day(self, date):
        return _rows(self._path(date))

    def recent(self, n):
        n = int(n)
        if n <= 0 or not self.root.exists():
            return []
        rows = []
        for path in sorted(self.root.glob('????-??-??.jsonl'), reverse=True):
            rows.extend(sorted(reversed(_rows(path)), key=lambda row: row['ts'], reverse=True))
            if len(rows) >= n:
                break
        return rows[:n]

    def _set_field(self, id, field, value):
        """One field of one row, found by id; False when no row has that id."""
        if not self.root.exists():
            return False
        for path in sorted(self.root.glob('????-??-??.jsonl'), reverse=True):
            rows = _rows(path)
            for row in rows:
                if row.get('id') == id:
                    row[field] = value
                    _write(path, rows)
                    return True
        return False

    def set_liked(self, id, text):
        return self._set_field(id, 'liked', str(text or '')[:20])

    def set_detail(self, id, text):
        """What she actually did, in place of what she meant to do."""
        return self._set_field(id, 'detail', str(text or '')[:40])

    def set_stopped(self, id, minutes):
        """How many minutes she gave it before putting it down; its minutes stays the plan."""
        if type(minutes) is not int or minutes < 0:
            return False
        return self._set_field(id, 'stopped_after', minutes)

    def forget(self, person):
        person = str(person or '')
        if not person or not self.root.exists():
            return 0
        count = 0
        for path in self.root.glob('????-??-??.jsonl'):
            rows = _rows(path)
            kept = [row for row in rows if person not in {str(x) for x in row.get('related_users', [])}]
            if len(kept) != len(rows):
                _write(path, kept)
                count += len(rows) - len(kept)
        return count
