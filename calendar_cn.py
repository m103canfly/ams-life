# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Calendar material for the current turn."""
import logging
from datetime import date, timedelta

TERMS = ((1, 5, '小寒'), (1, 20, '大寒'), (2, 4, '立春'), (2, 19, '雨水'),
         (3, 6, '惊蛰'), (3, 21, '春分'), (4, 5, '清明'), (4, 20, '谷雨'),
         (5, 6, '立夏'), (5, 21, '小满'), (6, 6, '芒种'), (6, 21, '夏至'),
         (7, 7, '小暑'), (7, 23, '大暑'), (8, 8, '立秋'), (8, 23, '处暑'),
         (9, 8, '白露'), (9, 23, '秋分'), (10, 8, '寒露'), (10, 23, '霜降'),
         (11, 7, '立冬'), (11, 22, '小雪'), (12, 7, '大雪'), (12, 22, '冬至'))

SOLAR = ((1, 1, '元旦'), (2, 14, '情人节'), (3, 8, '妇女节'),
         (5, 1, '劳动节'), (6, 1, '儿童节'), (10, 1, '国庆'),
         (12, 24, '平安夜'), (12, 25, '圣诞'))
LUNAR_NAMES = ('除夕', '春节', '元宵', '端午', '七夕', '中秋', '重阳')
LUNAR = {
    2026: ((2, 16), (2, 17), (3, 3), (6, 19), (8, 19), (9, 25), (10, 18)),
    2027: ((2, 5), (2, 6), (2, 20), (6, 9), (8, 8), (9, 15), (10, 8)),
    2028: ((1, 25), (1, 26), (2, 9), (5, 28), (8, 26), (10, 3), (10, 26)),
    2029: ((2, 12), (2, 13), (2, 27), (6, 16), (8, 16), (9, 22), (10, 16)),
    2030: ((2, 2), (2, 3), (2, 17), (6, 5), (8, 5), (9, 12), (10, 5)),
}
_warned = False


def _festivals(day):
    return ([name for month, number, name in SOLAR if (month, number) == (day.month, day.day)] +
            [name for (month, number), name in zip(LUNAR.get(day.year, ()), LUNAR_NAMES)
             if (month, number) == (day.month, day.day)])


def today_line(day):
    global _warned
    if day.year not in LUNAR and not _warned:
        logging.getLogger(__name__).warning('Lunar festival dates are unavailable for year %s', day.year)
        _warned = True
    terms = [name for month, number, name in TERMS if (month, number) == (day.month, day.day)]
    today = terms + _festivals(day)
    if today:
        return '今天%s。' % today[0]
    for offset in range(1, 8):
        future = day + timedelta(days=offset)
        festivals = _festivals(future)
        if festivals:
            return '再过 %d 天是%s。' % (offset, festivals[0])
    return ''
