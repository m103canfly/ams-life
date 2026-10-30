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
# Two other groups and 20 messages reduce one-group and sparse-reference bias.
# A fivefold rate is a conservative group-specificity threshold; two new words
# per night slow down first-use learning (up to 28 over fourteen nightly runs).
REFERENCE_MIN_GROUPS = 2
REFERENCE_MIN_MESSAGES = 20
SPECIFICITY_RATIO = 5.0
OVERLAP_RATIO = 0.8
NEW_PER_NIGHT = 2
# Boundary particles and pronouns commonly create incomplete phrase fragments.
BOUNDARY_WORDS = frozenset('的了着过吗呢吧啊就都也还你我他她它这那和与及而或但把被让给从在对向')
MAX_HITS_PER_GROUP = 20000
MAX_HITS_PER_WORD = 200
MAX_PHRASE_CHARS = 6
COMMON = frozenset('一个 不是 这么 感觉 一下 时候 给我 我的 这个 那个 我们 你们 他们'.split())
PARTS = re.compile(r'\[[^\]]*\]|https?://\S+|www\.\S+|\S+@\S+|[A-Za-z0-9]*\d[A-Za-z0-9]*')
RUNS = re.compile(r'[\u4e00-\u9fff]{2,12}|[A-Za-z]{2,20}')
DIGITS = re.compile(r'\d')
# Standalone dates, times and quantities are ordinary context, not group slang.
TIME_QUANTITY = re.compile(
    r'(?:(?:今|明|昨|前|后)(?:天|晚|夜|日)|(?:今天|明天|昨天)(?:早上|晚上|中午|下午|夜里)?|'
    r'早上|上午|中午|下午|傍晚|晚上|夜里|凌晨|白天|深夜|现在|刚才|待会|一会儿?|'
    r'这周|下周|上周|本周|这月|下月|上月|今年|明年|去年|'
    r'(?:[一二三四五六七八九十两零几]+|\d+)(?:点|时|分|秒|刻|天|周|月|年|个|次|回|小时|分钟|秒钟)(?:半|钟|一刻|三刻)?|'
    r'几点(?:钟)?|多少(?:个|次|天|分钟)?|一下|一个|几个|一些|一次|一回|很多|许多|少量|半个)'
)


def phrases(text, names=()):
    text = PARTS.sub(' ', str(text or ''))
    result = set()
    for run in RUNS.findall(text):
        chunks = [run] if not re.search(r'[\u4e00-\u9fff]', run) else [run[i:i+n] for n in range(2, min(len(run), MAX_PHRASE_CHARS) + 1) for i in range(len(run)-n+1)]
        for word in chunks:
            if (word[0] not in BOUNDARY_WORDS and word[-1] not in BOUNDARY_WORDS
                    and not TIME_QUANTITY.fullmatch(word)
                    and word not in everyday_words.WORDS and word not in COMMON and not DIGITS.search(word)
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
    data['hits'] = cap_hits([h for h in data.get('hits', []) if 0 <= now - float(h.get('ts', 0)) <= DAYS])
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







def cap_hits(hits):
    """Retain newest distinct phrase/message hits within both bounds."""
    counts, seen, kept = {}, set(), []
    for hit in sorted(hits, key=lambda h: (float(h['ts']), str(h['id']), h['word']), reverse=True):
        key = (hit['word'], str(hit['id']))
        if key in seen or counts.get(hit['word'], 0) >= MAX_HITS_PER_WORD:
            continue
        seen.add(key)
        counts[hit['word']] = counts.get(hit['word'], 0) + 1
        kept.append(hit)
        if len(kept) == MAX_HITS_PER_GROUP:
            break
    return list(reversed(kept))


def rank_candidates(data, references, now):
    """Rank distinct phrases against other groups using observable message rates."""
    own = refresh(data, now)
    own_messages = {h['id'] for h in data['hits']}
    reference_messages, reference_hits, reference_groups = set(), {}, set()
    for ref in references:
        if ref.get('place') == data.get('place'):
            continue
        for hit in ref.get('hits', []):
            if 0 <= now - float(hit['ts']) <= DAYS:
                reference_groups.add(ref.get('place'))
                key = (ref.get('place'), hit['id'])
                reference_messages.add(key)
                reference_hits.setdefault(hit['word'], set()).add(key)
    if len(reference_groups) < REFERENCE_MIN_GROUPS or len(reference_messages) < REFERENCE_MIN_MESSAGES or not own_messages:
        return []
    eligible = {}
    for word, hits in own.items():
        ids = {h['id'] for h in hits}
        # A one-message prior avoids an infinite score for an unseen phrase.
        score = (len(ids) / len(own_messages)) / ((len(reference_hits.get(word, ())) + 1) / len(reference_messages))
        if score >= SPECIFICITY_RATIO:
            eligible[word] = (hits, ids, score)
    merged = set()
    for longer, longer_hits in own.items():
        other_ids = {h['id'] for h in longer_hits}
        for size in range(2, len(longer)):
            for start in range(len(longer) - size + 1):
                part = longer[start:start + size]
                if part in eligible:
                    ids = eligible[part][1]
                    if len(ids & other_ids) / len(ids) >= OVERLAP_RATIO:
                        merged.add(part)
    result = [(word, hits, score) for word, (hits, ids, score) in eligible.items() if word not in merged]
    return sorted(result, key=lambda row: (-row[2], -len(row[1]), -len(row[0]), row[0]))
