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

try:
    from . import discretion, her_days
except ImportError:
    import discretion
    import her_days


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


def _days(root, week, selected):
    start = datetime.date.fromisocalendar(int(week[:4]), int(week[6:]), 1)
    store = her_days.Store(root)
    candidates = []
    for offset in range(7):
        date = (start + datetime.timedelta(days=offset)).isoformat()
        if 'day-' + date in selected:
            continue
        rows = store.day(date)
        if rows:
            candidates.append((date, rows))
    rng = random.Random('likeness-days-' + week)
    rng.shuffle(candidates)
    result = []
    for date, rows in candidates[:max(0, 2 - len(selected))]:
        entries = [{'time': datetime.datetime.fromtimestamp(row['ts']).strftime('%H:%M'),
                    'do': row.get('do', ''), 'detail': row.get('detail', ''),
                    'minutes': row.get('minutes'), 'feel': row.get('feel', ''),
                    'related_users': row.get('related_users', [])}
                   for row in sorted(rows, key=lambda row: row['ts'])]
        result.append({'id': 'day-' + date, 'kind': 'day', 'date': date, 'rows': entries})
    return result


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

    def select(self, week, *, now=None):
        week = _week(week)
        path = self._selection(week)
        if path.exists():
            chosen = _read(path, [])
            now = time.time() if now is None else now
            if week != week_of(now):
                return chosen
            selected_ids = {row['id'] for row in chosen}
            candidates = [row for row in self.samples(week) if row['id'] not in selected_ids]
            replies = sum(row.get('kind') != 'day' for row in chosen)
            added = self.rng.sample(candidates, min(max(0, 20 - replies), len(candidates)))
            days = {row['id'] for row in chosen if row.get('kind') == 'day'}
            added.extend(_days(self.root.parent, week, days))
            if added:
                chosen.extend(added)
                _write(path, json.dumps(chosen, ensure_ascii=False) + '\n')
            return chosen
        rows = self.samples(week)
        chosen = self.rng.sample(rows, min(20, len(rows)))
        chosen.extend(_days(self.root.parent, week, set()))
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
            changed = len(kept) != len(rows)
            for row in kept:
                if row.get('kind') == 'day':
                    entries = row['rows']
                    row['rows'] = [entry for entry in entries
                                   if str(person) not in {str(x) for x in entry.get('related_users', [])}]
                    removed += len(entries) - len(row['rows'])
                    changed |= len(entries) != len(row['rows'])
            if changed:
                text = (''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in kept) if is_samples
                        else json.dumps(kept, ensure_ascii=False) + '\n')
                _write(path, text)
        return removed


def public(rows, names=None):
    def hide_numbers(text):
        return re.sub(r'\d{5,}', '[number]', str(text))

    result = []
    for row in rows:
        if row.get('kind') == 'day':
            entries = []
            for entry in row['rows']:
                known = names(entry.get('related_users', [])) if names else []
                entries.append({key: (hide_numbers(discretion.anonymize(entry.get(key, ''), known))
                                      if key in ('detail', 'feel') else
                                      hide_numbers(entry.get(key, '')) if key == 'do' else entry.get(key))
                                for key in ('time', 'do', 'detail', 'minutes', 'feel')})
            result.append({'id': row['id'], 'kind': 'day', 'date': row['date'], 'rows': entries,
                           'rating': row.get('rating'), 'reason': hide_numbers(row.get('reason', ''))})
            continue
        result.append({'id': row['id'], 'ts': row['ts'], 'place': row['place'].split(':', 1)[0],
             'reply': hide_numbers(row['reply']),
             'context': [{'name': hide_numbers(x['name']), 'text': hide_numbers(x['text'])} for x in row['context']],
             'rating': row.get('rating'), 'reason': row.get('reason', '')})
    return result
