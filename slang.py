# -*- coding: utf-8 -*-
"""Group slang statistics. The ledger contains no message text."""
import hashlib
import json
import re
import time
from pathlib import Path

try:
    from . import atomic_file, discretion, everyday_words, redline
except ImportError:
    import atomic_file
    import discretion
    import everyday_words
    import redline

DAYS = 14 * 86400
FADE = 60 * 86400
UNKNOWN = '还不懂'
PARTS = re.compile(r'\[[^\]]*\]|https?://\S+|www\.\S+|\S+@\S+|[A-Za-z0-9]*\d[A-Za-z0-9]*')
RUNS = re.compile(r'[\u4e00-\u9fff]{2,12}|[A-Za-z]{2,20}')
DIGITS = re.compile(r'\d')


def phrases(text, names=()):
    text = PARTS.sub(' ', str(text or ''))
    result = set()
    for run in RUNS.findall(text):
        chunks = [run] if not re.search(r'[\u4e00-\u9fff]', run) else [run[i:i+n] for n in range(2, len(run) + 1) for i in range(len(run)-n+1)]
        for word in chunks:
            if (word not in everyday_words.WORDS and not DIGITS.search(word)
                    and not any(word in name or name in word for name in names if name)
                    and not redline.hit(word)):
                result.add(word)
    return result


class Store:
    def __init__(self, directory):
        self.directory = Path(directory)

    def path(self, place):
        return self.directory / (hashlib.sha256(place.encode('utf-8')).hexdigest() + '.json')

    def load(self, place):
        try:
            data = json.loads(self.path(place).read_text(encoding='utf-8'))
            if data.get('place') == place:
                return data
        except (OSError, ValueError, AttributeError):
            pass
        return {'place': place, 'hits': [], 'words': {}, 'blocked': [], 'tried': '', 'asked_day': '', 'asked': 0}

    def save(self, place, data):
        self.directory.mkdir(parents=True, exist_ok=True)
        if not data.get('group_number'):
            used = [int(self.load(p).get('group_number') or 0) for p in self.places()]
            data['group_number'] = max(used, default=0) + 1
        path = self.path(place)
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        atomic_file.replace(tmp, path)

    def places(self):
        result = []
        if self.directory.exists():
            for path in self.directory.glob('*.json'):
                try:
                    place = str(json.loads(path.read_text(encoding='utf-8')).get('place') or '')
                    if place.startswith('group:') and path == self.path(place):
                        result.append(place)
                except (OSError, ValueError, AttributeError):
                    continue
        return sorted(result)


def refresh(data, now):
    data['hits'] = [h for h in data.get('hits', []) if 0 <= now - float(h.get('ts', 0)) <= DAYS]
    groups = {}
    for h in data['hits']:
        groups.setdefault(h['word'], []).append(h)
    for word, rec in list(data.get('words', {}).items()):
        hits = groups.get(word, [])
        if not hits:
            rec['count'] = 0
            rec['people_count'] = 0
        if hits:
            rec['last'] = max(float(rec.get('last', 0)), max(h['ts'] for h in hits))
            rec['count'] = len(hits)
            rec['people_count'] = len({h['person'] for h in hits})
        if len(hits) < 5 or len({h['person'] for h in hits}) < 3:
            # A learned word fades after 60 days, but explicit withdrawal must remove it sooner.
            if now - float(rec.get('last', 0)) > FADE:
                del data['words'][word]
            continue
        rec.update(count=len(hits), people_count=len({h['person'] for h in hits}), last=max(h['ts'] for h in hits),
                   origin=discretion.make_origin(data['place'], [h['person'] for h in hits],
                                                 [h['id'] for h in hits], discretion.PUBLIC))
    return {w: hs for w, hs in groups.items() if len(hs) >= 5 and len({h['person'] for h in hs}) >= 3}


def withdraw(data, person='', source_ids=(), now=None):
    ids = set(map(str, source_ids))
    removed = {h['word'] for h in data.get('hits', []) if (person and h['person'] == person) or h['id'] in ids}
    data['hits'] = [h for h in data.get('hits', []) if not ((person and h['person'] == person) or h['id'] in ids)]
    groups = refresh(data, time.time() if now is None else now)
    for word in removed:
        if word not in groups:
            data.get('words', {}).pop(word, None)
    for word, rec in list(data.get('words', {}).items()):
        origin = discretion.origin_of(rec)
        if discretion.is_about(origin, person=person or None, source_ids=ids) and word not in groups:
            del data['words'][word]
            removed.add(word)
    return len(removed)





