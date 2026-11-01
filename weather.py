# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline display and bounded background weather retrieval."""
import asyncio
import json
import math
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

try:
    from . import atomic_file
except ImportError:
    import atomic_file

ZONE = timezone(timedelta(hours=8))
LIMIT = 64 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(lat, lon, *, get=None):
    lat, lon = float(lat), float(lon)
    if not math.isfinite(lat) or not math.isfinite(lon) or not -90 <= lat <= 90 or not -180 <= lon <= 180:
        raise ValueError('invalid coordinates')
    query = urlencode({'latitude': lat, 'longitude': lon,
                       'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max',
                       'timezone': 'Asia/Shanghai', 'forecast_days': 1})
    request = Request('https://api.open-meteo.com/v1/forecast?' + query, method='GET')
    get = get or build_opener(NoRedirect()).open
    with get(request, timeout=5) as response:
        if response.status != 200:
            raise ValueError('weather response status')
        data = response.read(LIMIT)
    if len(data) >= LIMIT:
        raise ValueError('weather response too large')
    daily = json.loads(data)['daily']
    day = datetime.now(ZONE).date().isoformat()
    if daily['time'] != [day]:
        raise ValueError('weather date')
    arrays = [daily[key] for key in ('weather_code', 'temperature_2m_max',
                                      'temperature_2m_min', 'precipitation_probability_max')]
    if any(not isinstance(value, list) or len(value) != 1 for value in arrays):
        raise ValueError('weather values')
    values = [value[0] for value in arrays]
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError('weather values')
    code, maximum, minimum, rain = values
    if int(code) != code or not 0 <= rain <= 100 or minimum > maximum:
        raise ValueError('weather values')
    return {'date': day, 'code': int(code), 'max': maximum, 'min': minimum, 'rain': rain}


def describe(code):
    if type(code) is not int:
        return ''
    if code in (0, 1, 2, 3, 45, 48, 61, 65):
        return {0: '晴', 1: '少云', 2: '多云', 3: '阴', 45: '雾', 48: '雾', 61: '小雨', 65: '大雨'}[code]
    for low, high, label in ((51, 57, '毛毛雨'), (61, 67, '雨'), (71, 77, '雪'),
                              (80, 82, '阵雨'), (85, 86, '阵雪'), (95, 99, '雷雨')):
        if low <= code <= high:
            return label
    return ''


def line(cache, place):
    try:
        label = describe(cache['code'])
        if not label:
            return ''
        return '天气：%s%s %s–%s℃，降水 %s%%' % (
            (str(place).strip() + ' ') if place else '', label,
            cache['min'], cache['max'], cache['rain'])
    except (KeyError, TypeError):
        return ''


def read(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def weather_line(path, config):
    if any(config.get(key) is None or config.get(key) == '' for key in ('weather_lat', 'weather_lon')):
        return ''
    cache = read(path)
    if cache.get('date') != datetime.now(ZONE).date().isoformat():
        return ''
    return line(cache, config.get('weather_place', ''))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    atomic_file.replace(tmp, path)


async def tick(config, path, logger, *, now=None, fetcher=None):
    lat, lon = config.get('weather_lat'), config.get('weather_lon')
    if lat is None or lon is None or lat == '' or lon == '':
        return
    now = now or datetime.now(ZONE)
    day = now.astimezone(ZONE).date().isoformat()
    if read(path).get('date') == day:
        return
    attempts_path = path.with_name('weather-attempts.json')
    attempts = read(attempts_path)
    count = attempts.get('count', 0) if attempts.get('date') == day else 0
    last = attempts.get('last', 0)
    if type(count) is not int or not isinstance(last, (int, float)):
        logger.warning('[ams-life] weather failed (%s)', 'ValueError')
        return
    if count >= 3 or now.timestamp() - last < 3 * 3600:
        return
    try:
        write(attempts_path, {'date': day, 'count': count + 1, 'last': now.timestamp()})
        result = await asyncio.to_thread(fetcher or fetch, lat, lon)
        write(path, {key: (now.timestamp() if key == 'fetched' else result[key])
                     for key in ('date', 'fetched', 'code', 'max', 'min', 'rain')})
    except Exception as exc:
        logger.warning('[ams-life] weather failed (%s)', type(exc).__name__)
