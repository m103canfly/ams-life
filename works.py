# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her works: the songs and the reading notes she really made, one line each.

A work is kept only after the call that made it came back with something and
the words passed the red line and the names were taken out, so "I wrote a song"
is always something she can show. Only her own words are in it: no one else's
name (his too), so forgetting someone has nothing to do here.

    {"id", "ts", "kind": "song" | "review", "title", "text", "url", "origin"}

`url` is set for a reading note (the page she read) and empty for a song; the
origin of every work is her own (`self`).
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

try:
    from . import discretion
except ImportError:
    import discretion

KINDS = ('song', 'review')
TITLE_CHARS = 80      # a title is short: the name of the song or of the page
TEXT_CHARS = 1000     # only a guard against a model running away: she writes what she likes
SHOWN = 3             # how many recent works a later call (a public line) is shown
MEMORY_CHARS = 60


def path(root):
    return Path(root) / 'works.jsonl'


def read(root):
    """Every work, oldest first; a line that is not a work is left out."""
    try:
        lines = path(root).read_text(encoding='utf-8').splitlines()
    except OSError:
        return []
    rows = []
    for line in lines:
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and row.get('id') and row.get('kind') in KINDS:
            rows.append(row)
    return rows


def add(root, kind, title, text, url='', now=None, origin=None):
    """One work, appended; {} when there is nothing to keep."""
    kind = str(kind or '')
    title = str(title or '').strip()[:TITLE_CHARS]
    text = str(text or '').strip()[:TEXT_CHARS]
    if kind not in KINDS or not title or not text:
        return {}
    now = float(time.time() if now is None else now)
    row = {'id': uuid.uuid4().hex, 'ts': now, 'kind': kind, 'title': title, 'text': text,
           'url': str(url or ''), 'origin': dict(origin or discretion.make_origin(discretion.SELF))}
    target = path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('a', encoding='utf-8') as out:
        out.write(json.dumps(row, ensure_ascii=False) + '\n')
    return row


def recent(root, n=SHOWN):
    """The newest `n` works, newest first."""
    rows = read(root)
    rows.sort(key=_stamp, reverse=True)
    return rows[:max(0, int(n))]


def _stamp(row):
    try:
        return float((row or {}).get('ts') or 0)
    except (TypeError, ValueError):
        return 0.0


def head(work, lines=2, chars=MEMORY_CHARS):
    """The opening lines of a work, on one line: what a memory or a post shows of it."""
    parts = [part.strip() for part in str((work or {}).get('text') or '').splitlines() if part.strip()]
    return '；'.join(parts[:lines])[:chars]


def opening(work, chars=MEMORY_CHARS):
    """The first sentence of a work, on one line."""
    text = ' '.join(str((work or {}).get('text') or '').split())
    for mark in ('。', '！', '？'):
        text = text.split(mark, 1)[0]
    return text.strip()[:chars]


def memory_line(work):
    """Her own memory of a work, one line: "我写了首歌《…》：头两句" or "我读了《…》，觉得…"."""
    work = work if isinstance(work, dict) else {}
    title = str(work.get('title') or '').strip()
    if not title:
        return ''
    if work.get('kind') == 'song':
        return '我写了首歌《%s》：%s' % (title, head(work))
    said = opening(work)
    return '我读了《%s》，觉得%s' % (title, said) if said else '我读了《%s》' % title
