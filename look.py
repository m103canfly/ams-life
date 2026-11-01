# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her daily outfit and lasting changes."""
import json
import re
from datetime import date, datetime

try:
    from . import browse, atomic_file
except ImportError:
    import browse
    import atomic_file

TERMS = ((1, 5, '小寒'), (1, 20, '大寒'), (2, 4, '立春'), (2, 19, '雨水'),
         (3, 6, '惊蛰'), (3, 21, '春分'), (4, 5, '清明'), (4, 20, '谷雨'),
         (5, 6, '立夏'), (5, 21, '小满'), (6, 6, '芒种'), (6, 21, '夏至'),
         (7, 7, '小暑'), (7, 23, '大暑'), (8, 8, '立秋'), (8, 23, '处暑'),
         (9, 8, '白露'), (9, 23, '秋分'), (10, 8, '寒露'), (10, 23, '霜降'),
         (11, 8, '立冬'), (11, 22, '小雪'), (12, 7, '大雪'), (12, 22, '冬至'))


def season_of(day):
    index = next((i for i in range(len(TERMS) - 1, -1, -1)
                  if (day.month, day.day) >= TERMS[i][:2]), 23)
    return ('冬' if index < 2 or index >= 20 else '春' if index < 8 else
            '夏' if index < 14 else '秋', TERMS[index][2])


def days_ago(day, today):
    return (today - date.fromisoformat(day) if isinstance(day, str) else today - day).days


def read_look(path, today):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(value, dict) and value.get('date') == today.isoformat() and isinstance(value.get('today'), str):
            return value['today']
    except (OSError, ValueError):
        pass
    return ''


def write_look(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=1), encoding='utf-8')
    atomic_file.replace(tmp, path)


def changes(model):
    return [x for x in (model.get('look') or []) if isinstance(x, dict) and x.get('text') and x.get('date')]


def look_line(today, outfit, model, weather=''):
    season, term = season_of(today)
    parts = ['今天的打扮：' + outfit if outfit else '今天还没定穿什么；要拍自拍或聊到穿什么时，先用 set_look 定一句',
             '季节：%s，%s' % (season, term)]
    recent = []
    for item in changes(model):
        try:
            recent.append('%s（%d天前）' % (item['text'], days_ago(item['date'], today)))
        except (ValueError, TypeError):
            continue
    if recent:
        parts.append('最近的样子：' + '；'.join(recent))
    if weather:
        parts.append(weather)
    return ('[她今天] ' + '；'.join(parts))[:200]


async def set_look(plugin, event, path, today='', change=''):
    values = [str(value or '').strip() for value in (today, change)]
    if any(re.search(r'http|www\.|://|@|\d{5,}', value, re.IGNORECASE) for value in values):
        return '不能这样写'
    values = [browse.clean_query(value, names=plugin._browse_names()) for value in values]
    today, change = values
    if not today or any(len(value) > 30 for value in values):
        return '不能这样写'
    now = datetime.now()
    here = getattr(plugin, '_here', None)
    place = here(event) if here else ''
    write_look(path, {'date': now.date().isoformat(), 'today': today, 'place': place, 'ts': now.timestamp()})
    if change:
        model = plugin.self_model
        model['look'] = (list(model.get('look') or []) +
                         [{'text': change, 'date': now.date().isoformat(), 'origin': '她自己'}])[-8:]
        plugin._save_self_model()
    return '记下了'
