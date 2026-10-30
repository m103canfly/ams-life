# -*- coding: utf-8 -*-
"""Offline group-slang replay. Raw chat is held in memory only, never written."""
import argparse
from collections import defaultdict
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import attention
import redline
import slang


def simulate(path, names=(), self_id=''):
    names = tuple(attention.HER_NAMES) + tuple(names)
    # SQLite opens read-only; closing the connection is separate from transactions.
    with closing(sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)) as db:
        columns = {row[1] for row in db.execute('PRAGMA table_info(messages)')}
        required = {'id', 'group_id', 'post_type', 'raw_message', 'timestamp'}
        sender = next((name for name in ('user_id', 'sender_id') if name in columns), None)
        if not required <= columns or not sender:
            raise ValueError('messages must have the requested columns and a user_id or sender_id column')
        latest = db.execute("SELECT MAX(timestamp) FROM messages WHERE group_id IS NOT NULL "
                            "AND lower(post_type) IN ('message','group')").fetchone()[0]
        if latest is None:
            return []
        end = float(latest)
        query = ('SELECT id, group_id, post_type, raw_message, timestamp, ' + sender +
                 " FROM messages WHERE group_id IS NOT NULL AND lower(post_type) IN ('message','group')"
                 ' AND timestamp >= ? AND timestamp <= ? ORDER BY timestamp, id')
        rows = list(db.execute(query, (end - slang.DAYS, end)))
    valid = [r for r in rows if str(r[1] or '').strip() not in ('', '0') and r[4] is not None]
    by_day = defaultdict(list)
    for mid, group, kind, text, stamp, person in valid:
        stamp = float(stamp)
        if not 0 <= end - stamp <= slang.DAYS or not person or str(person) == str(self_id):
            continue
        if not text or redline.hit(text):
            continue
        day = time.strftime('%Y-%m-%d', time.localtime(stamp))
        by_day[day].append((str(group), str(mid), str(person), str(text), stamp))
    groups = {}
    for day in sorted(by_day):
        active = set()
        for group, mid, person, text, stamp in by_day[day]:
            data = groups.setdefault(group, {'place': 'group:' + group, 'hits': [], 'words': {}, 'blocked': []})
            active.add(group)
            for word in slang.phrases(text, names):
                data['hits'].append({'word': word, 'person': person, 'id': mid, 'ts': stamp})
        now = max(row[4] for row in by_day[day])
        for data in groups.values():
            slang.refresh(data, now)
        for group in sorted(active):
            data = groups[group]
            ranked = slang.rank_candidates(data, groups.values(), now)
            new = [(w, hs) for w, hs, _ in ranked if w not in data['words']][:slang.NEW_PER_NIGHT]
            for word, hits in new:
                data['words'][word] = {'last': max(h['ts'] for h in hits)}
            slang.refresh(data, now)
    result = []
    for _, data in sorted(groups.items()):
        ranked = [word for word, _hits, _score in slang.rank_candidates(data, groups.values(), end)
                  if word in data['words']]
        result.append((len(data['words']), len(data['hits']), ranked))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='Count group slang without displaying chat or identifiers.')
    parser.add_argument('--chat', required=True, help='SQLite chat database')
    parser.add_argument('--show', action='store_true', help='show up to ten expressions locally')
    parser.add_argument('--exclude-name', action='append', default=[], help='exclude a known name; repeat as needed')
    parser.add_argument('--self-id', default='', help='exclude her own messages')
    args = parser.parse_args(argv)
    try:
        result = simulate(args.chat, args.exclude_name, args.self_id)
    except (OSError, sqlite3.Error, ValueError, TypeError, OverflowError):
        print('Cannot read messages, timestamps, or a sender column.', file=sys.stderr)
        return 1
    for index, (words, hits, examples) in enumerate(result, 1):
        print('群%d：黑话 %d，命中账 %d' % (index, words, hits))
        if args.show:
            print('  ' + '、'.join(examples[:10]))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
