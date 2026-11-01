# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Local weekly reply samples and ratings."""
import datetime
import hashlib
import json
import random
import re
import time
from pathlib import Path


def week_of(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp).date().isocalendar()
    return '%04d-W%02d' % (date.year, date.week)


def _week(value):
    value = str(value)
    if not re.fullmatch(r'\d{4}-W\d{2}', value):
        raise ValueError('invalid week')
    datetime.date.fromisocalendar(int(value[:4]), int(value[6:]), 1)
    return value


def _read(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(text, encoding='utf-8')
    tmp.replace(path)


class Store:
    def __init__(self, root, rng=None):
        self.root = Path(root) / 'likeness'
        self.rng = rng if rng is not None else random.Random()

    def _samples(self, week):
        return self.root / ('samples-' + _week(week) + '.jsonl')

    def _selection(self, week):
        return self.root / ('week-' + _week(week) + '.json')

    def samples(self, week):
        path = self._samples(week)
        return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line] if path.exists() else []

    def add(self, place, reply, context, timestamp=None):
        timestamp = time.time() if timestamp is None else timestamp
        week = week_of(timestamp)
        rows = self.samples(week)
        used = {row['id'] for row in rows}
        used.update(row['id'] for row in _read(self._selection(week), []))
        identity = json.dumps([timestamp, place, reply, context], ensure_ascii=False, sort_keys=True)
        sequence = 0
        while True:
            sample_id = hashlib.sha256((identity + ':' + str(sequence)).encode('utf-8')).hexdigest()[:32]
            if sample_id not in used:
                break
            sequence += 1
        row = {'id': sample_id, 'ts': timestamp, 'place': place, 'reply': reply, 'context': context}
        if len(rows) < 300:
            rows.append(row)
        else:
            index = self.rng.randrange(len(rows) + 1)
            if index < len(rows):
                rows[index] = row
        _write(self._samples(week), ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))

    def select(self, week):
        path = self._selection(week)
        if path.exists():
            return _read(path, [])
        rows = self.samples(week)
        chosen = self.rng.sample(rows, min(20, len(rows)))
        _write(path, json.dumps(chosen, ensure_ascii=False) + '\n')
        return chosen

    def rate(self, week, sample_id, rating, reason):
        if rating not in ('like', 'unlike', 'unsure') or not isinstance(reason, str):
            raise ValueError('invalid rating')
        path = self._selection(week)
        rows = _read(path, [])
        for row in rows:
            if row['id'] == sample_id:
                row['rating'] = rating
                row['reason'] = reason[:500]
                _write(path, json.dumps(rows, ensure_ascii=False) + '\n')
                return True
        return False

    def forget(self, person):
        if not self.root.exists():
            return 0
        removed = 0
        for path in list(self.root.glob('samples-*.jsonl')) + list(self.root.glob('week-*.json')):
            is_samples = path.suffix == '.jsonl'
            rows = ([json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x]
                    if is_samples else _read(path, []))
            kept = [row for row in rows if not any(str(line.get('sender_id') or '') == person
                                                    for line in row.get('context', []))]
            removed += len(rows) - len(kept)
            if len(kept) != len(rows):
                text = (''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in kept) if is_samples
                        else json.dumps(kept, ensure_ascii=False) + '\n')
                _write(path, text)
        return removed


def public(rows):
    def hide_numbers(text):
        return re.sub(r'\d{5,}', '[number]', str(text))

    return [{'id': row['id'], 'ts': row['ts'], 'place': row['place'].split(':', 1)[0],
             'reply': hide_numbers(row['reply']),
             'context': [{'name': hide_numbers(x['name']), 'text': hide_numbers(x['text'])} for x in row['context']],
             'rating': row.get('rating'), 'reason': row.get('reason', '')} for row in rows]
