# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Event-driven choices for her own day; the minute tick never invents work."""
import asyncio
import json
import logging
import re
import time
from datetime import datetime, timedelta

try:
    from . import atomic_file, bodily, body, browse, daily, discretion, her_days, look, weather
    from .common import DATA_DIR, STATE_DIR
    from . import mixin_selfie as phone
except ImportError:
    import atomic_file
    import bodily
    import body
    import browse
    import daily
    import discretion
    import her_days
    import look
    import weather
    from common import DATA_DIR, STATE_DIR
    import mixin_selfie as phone

logger = logging.getLogger('ams-life.life')
NEEDS = ('sleepiness', 'hunger', 'physical_fatigue')
BODY_FIELDS = (*NEEDS, 'last_sleep_end', 'last_meal', 'last_rest')
BASE_MENU = ('吃饭', '睡觉', '休息', '什么都不干')


def enabled(plugin):
    return bool(getattr(plugin, 'enabled', True) and
                (getattr(plugin, 'config', None) or {}).get('life_loop_enabled', False))


def read_state():
    try:
        value = json.loads((STATE_DIR / 'life.json').read_text(encoding='utf-8'))
        if isinstance(value, dict):
            return value
    except (OSError, ValueError):
        pass
    return {'last_think_ts': 0, 'today': {}, 'last_body': {},
            'pending': {'group_browse': False, 'go_browse': False}, 'last_item_id': ''}


def save_state(state):
    path = STATE_DIR / 'life.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding='utf-8')
    atomic_file.replace(temp, path)


def budget(plugin):
    cfg = plugin._attention_cfg()
    spent = plugin._spent_today()
    return 'hard' if spent >= cfg['hard'] else 'soft' if spent >= cfg['soft'] else 'ok'


def bind_body(core):
    """Restore the newest bodily checkpoint and account for time spent offline once."""
    core._life_now_path = phone.NOW_PATH
    core._life_state_path = STATE_DIR / 'life.json'
    if getattr(core, '_life_body_loaded', False):
        return
    core._life_body_loaded = True
    checkpoint = read_state().get('body', {})
    stamp = checkpoint.get('ts', 0)
    saved = STATE_DIR / 'her.json'
    saved_at = saved.stat().st_mtime if saved.exists() else 0
    if stamp and stamp >= saved_at:
        for field in BODY_FIELDS:
            if field in checkpoint:
                setattr(core, field, float(checkpoint[field]))
    else:
        stamp = saved_at
    now = time.time()
    if 0 < stamp < now:
        body._advance_needs(core, stamp, now)


def checkpoint(state, core, now):
    state['body'] = dict({key: getattr(core, key) for key in BODY_FIELDS}, ts=now)


def consume(plugin, name):
    """Consume before an entry point awaits, even if that entry cannot run."""
    state = read_state()
    pending = state.setdefault('pending', {})
    picked = bool(pending.pop(name, False))
    if picked:
        save_state(state)
    return picked and enabled(plugin) and budget(plugin) == 'ok'


def menu(plugin):
    config = plugin.config or {}
    choices = list(BASE_MENU)
    if getattr(plugin, 'browse_groups_enabled', False):
        choices.append('去测试群看看')
    if plugin._browse_on() and getattr(plugin, 'browse_trips_enabled', False):
        choices.append('刷手机')
    if config.get('photo_enabled', False):
        choices.append('拍照')
    if config.get('qzone_enabled', False):
        choices.append('发说说')
    return choices


def parse(raw, choices):
    try:
        value = browse._json_object(raw)
        if not isinstance(value, dict) or value.get('do') not in choices:
            return None
        value = dict(value)
        for key in ('detail', 'liked_last', 'post', 'look'):
            if value.get(key) is None:
                value[key] = ''
        if any(not isinstance(value.get(k, ''), str) for k in ('detail', 'liked_last', 'post', 'look')):
            return None
        minutes = value.get('minutes', 30)
        if isinstance(minutes, str):
            minutes = int(minutes)
        if type(minutes) is not int:
            return None
        low, high = (60, 720) if value['do'] == '睡觉' else (5, 120)
        return dict(value, minutes=max(low, min(high, minutes)), detail=value.get('detail', '')[:40],
                    liked_last=value.get('liked_last', '')[:20], post=value.get('post', '')[:300],
                    look=value.get('look', '')[:30])
    except (ValueError, TypeError):
        return None


def current():
    try:
        value = json.loads(phone.NOW_PATH.read_text(encoding='utf-8'))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def item_end(item):
    try:
        minutes = item.get('minutes', 30)
        if type(minutes) is not int or minutes < 1:
            return 0
        return datetime.fromisoformat(item['start']).timestamp() + minutes * 60
    except (KeyError, TypeError, ValueError, OverflowError):
        return 0


def sleeping(item):
    return item.get('source') == 'her' and item.get('kind', item.get('doing')) == '睡觉'


def note_called(plugin, event):
    """Remember an actual addressed event, without examining its words."""
    if not enabled(plugin) or event is None or not plugin._addresses_her(event):
        return
    here = plugin._here(event)
    state = read_state()
    state.setdefault('called', {})[here] = time.time()
    save_state(state)


def observe_messages(plugin):
    """Keep the existing message method; observe its structured @ flag after storage."""
    if getattr(plugin, '_life_observing', False):
        return
    original = getattr(plugin, '_window_add_message', None)
    if original is None:
        return

    def receive(event):
        result = original(event)
        note_called(plugin, event)
        return result

    plugin._window_add_message = receive
    plugin._life_observing = True


def quiet_chats(plugin, state, now):
    """Observe reply timestamps and silence in the same window, once per exchange."""
    consumed = state.setdefault('quiet_seen', {})
    called = state.setdefault('called', {})
    due = []
    places = plugin._window_places()
    for here in places:
        rows = plugin._read_window(here).get('recent') or []
        last = max([float(x.get('ts', 0) or 0) for x in rows] or [0])
        replies = max([float(x.get('ts', 0) or 0) for x in rows if x.get('role') == 'assistant'] or [0])
        exchange = max(replies, called.get(here, 0))
        if exchange > consumed.get(here, 0) and now - max(last, exchange) >= 600:
            due.append((here, exchange))
    # Keep only windows still present; no names or words enter this state.
    state['quiet_seen'] = {k: v for k, v in consumed.items() if k in places}
    state['called'] = {k: v for k, v in called.items() if k in places}
    return due


def due_events(state, now):
    """Reserved for 1d. Entries have an id and an absolute timestamp."""
    return [row for row in state.get('due', []) if isinstance(row, dict)
            and row.get('id') and isinstance(row.get('ts'), (int, float)) and row['ts'] <= now]


def clock_time(stamp):
    try:
        local = datetime.fromisoformat(stamp) if isinstance(stamp, str) else datetime.fromtimestamp(stamp)
        return local.strftime('%H:%M')
    except (TypeError, ValueError, OverflowError, OSError):
        return ''


def materials(plugin, state, item, core, reason, now, choices, outfit):
    local = datetime.fromtimestamp(now)
    activity = {'在哪': item.get('where', ''), '在干什么': item.get('doing', ''),
                '几点开始': clock_time(item.get('start')), '打算多久': item.get('minutes')}
    lines = ['现在：' + local.strftime('%Y-%m-%d %H:%M') + '，星期' + '一二三四五六日'[local.weekday()],
             '此刻：' + json.dumps(activity, ensure_ascii=False), '这会儿想：' + reason]
    forecast = weather.weather_line(STATE_DIR / 'weather.json', plugin.config or {})
    if forecast:
        lines.append(forecast)
    lines += bodily.feel_lines({key: getattr(core, key) for key in NEEDS})
    lines.append('醒了多久：%d 分钟；上一顿：%s' %
                 (max(0, int((now - core.last_sleep_end) / 60)),
                  datetime.fromtimestamp(core.last_meal).strftime('%H:%M')))
    rows = her_days.Store(DATA_DIR).day(local.date().isoformat())[-8:]
    activities = [{'几点': clock_time(row.get('ts')), '做了什么': row.get('do', '') + '：' + row.get('detail', ''),
                   '多久': row.get('minutes'), '感觉': row.get('feel', ''), '喜不喜欢': row.get('liked', '')}
                  for row in rows]
    lines.append('今天已经做过：' + json.dumps(activities, ensure_ascii=False))
    lines.append('菜单：' + '、'.join(choices))
    lines.append('自己挑这会儿做什么，只回 JSON：{"do":"菜单里的一样","detail":"具体干什么/在哪，最多40字",'
                 '"minutes":30,"liked_last":"刚才那件喜不喜欢，最多20字，没有就空",'
                 '"post":"公开短句，最多300字，不需要就空","look":""}。')
    if outfit:
        lines.append('刚睡醒，今天还没定打扮，顺手在 look 里说今天穿什么（最多30字）。')
    return re.sub(r'\d{5,}', '[号码]', '\n'.join(lines))


def anonymized(plugin, text):
    index = plugin._names_index()
    owner = str((plugin.config or {}).get('owner_qq') or '').strip()
    related = []
    names = []
    for person in index:
        aliases = plugin._known_names([person])
        if discretion.anonymize(text, aliases) != text:
            related.append(str(person))
        if str(person) != owner:
            names.extend(aliases)
    return discretion.anonymize(text, names), related


def fallback(plugin, core, now):
    where, doing, start = daily.schedule(datetime.fromtimestamp(now), core.energy, core.v, core.stress)
    phone._write_json(phone.NOW_PATH, {'where': where, 'doing': doing, 'start': start.isoformat(),
                                     'source': 'schedule'})


def notebook_day(now):
    """The hours before 18:00 belong to the previous evening's sitting."""
    local = datetime.fromtimestamp(now)
    return (local - timedelta(days=local.hour < 18)).date().isoformat()


def notebook_due(plugin, now):
    state = read_state()
    day = notebook_day(now)
    local = datetime.fromtimestamp(now)
    triggered = state.get('notebook_sleep') == day
    fallback_time = 3 <= local.hour < 18
    return (triggered or fallback_time) and state.get('notebook_done') != day and budget(plugin) == 'ok'


async def notebook(plugin, now):
    if not notebook_due(plugin, now) or not plugin._llm_allowed('notebook'):
        return False
    try:
        return await plugin._maybe_write_notebook(now=now)
    finally:
        state = read_state()
        state['notebook_done'] = notebook_day(now)
        save_state(state)


async def photo(plugin, detail):
    try:
        if enabled(plugin) and budget(plugin) == 'ok' and plugin.config.get('photo_enabled', False):
            path = await plugin._make_photo('photo', detail)
            if path:
                state = read_state()
                state['last_photo'] = {'path': str(path), 'date': datetime.fromtimestamp(time.time()).date().isoformat()}
                save_state(state)
    except Exception as exc:
        logger.warning('[ams-life] life photo failed (%s)', type(exc).__name__)


async def apply_choice(plugin, value, core, now, outfit):
    state = read_state()
    action = value['do']
    started = int(now) if action == '睡觉' else now
    detail, users = anonymized(plugin, value['detail'])
    post, post_users = anonymized(plugin, value['post'])
    liked, _ = anonymized(plugin, value['liked_last'])
    detail = browse.clean_query(detail)[:40]
    doing = detail or value['do']
    # Prefer an explicit place; otherwise keep her at home.
    match = re.search(r'(?:^|[，,；;])在([^，,；;。]{1,12})(?:[，,；;。]|$)', detail)
    where = browse.clean_query(match.group(1)) if match else '家里'
    plugin._set_now(where or '家里', doing, now=datetime.fromtimestamp(started), minutes=value['minutes'],
                    source='her', kind=value['do'])
    store = her_days.Store(DATA_DIR)
    if liked and state.get('last_item_id'):
        store.set_liked(state['last_item_id'], liked)
    row = store.add({'ts': now, 'do': value['do'], 'detail': detail, 'minutes': value['minutes'],
                     'origin': discretion.make_origin(discretion.SELF),
                     'related_users': sorted(set(users + post_users))})
    state['last_item_id'] = row['id']
    state.pop('handled_item', None)
    if action == '吃饭':
        body.ate(core, now)
    elif action == '休息':
        body.rested(core, value['minutes'], now)
    elif action == '睡觉':
        state['sleep'] = {'start': int(started), 'end': int(started + value['minutes'] * 60)}
        hour = datetime.fromtimestamp(now).hour
        if hour >= 18 or hour < 3:
            state['notebook_sleep'] = notebook_day(now)
    elif action in ('去测试群看看', '刷手机'):
        state.setdefault('pending', {})['group_browse' if action == '去测试群看看' else 'go_browse'] = True
    checkpoint(state, core, now)
    save_state(state)
    if outfit and value['look']:
        await look.set_look(plugin, None, phone.LOOK_PATH, today=value['look'])
    if action == '睡觉':
        await notebook(plugin, now)
    elif action == '拍照':
        tasks = getattr(plugin, '_life_photo_tasks', None)
        if tasks is None:
            tasks = plugin._life_photo_tasks = set()
        task = asyncio.create_task(photo(plugin, detail or action))
        tasks.add(task)
        task.add_done_callback(tasks.discard)
    elif action == '发说说' and post:
        try:
            from . import qzone
        except ImportError:
            import qzone
        last_photo = state.get('last_photo', {})
        picture = last_photo.get('path') if last_photo.get('date') == datetime.fromtimestamp(now).date().isoformat() else None
        if budget(plugin) == 'ok':
            await qzone.post(plugin, post, photo=picture)


async def tick(plugin, now=None):
    if not enabled(plugin):
        return False
    now = time.time() if now is None else float(now)
    gate = budget(plugin)
    if gate == 'hard':
        return False
    core = plugin._core(None)
    bind_body(core)
    core._decay_to_now()
    state = read_state()
    item = current()
    end = item_end(item)
    sleep = state.get('sleep', {})
    if sleep and core.last_tick < sleep['end'] <= now:
        # Chat may have decayed the body less than thirty seconds before waking.
        body._advance_needs(core, core.last_tick, now)
        core.last_tick = now
    checkpoint(state, core, now)
    if (sleep and now < sleep['end']) or (sleeping(item) and now < end):
        save_state(state)
        return False
    if sleep and now >= sleep['end']:
        state['woke_date'] = datetime.fromtimestamp(sleep['end']).date().isoformat()
        state.pop('sleep', None)
    local = datetime.fromtimestamp(now)
    if state.get('today', {}).get('date') != local.date().isoformat():
        state['today'] = {'date': local.date().isoformat(), 'count': 0}
    previous = state.get('last_body', {})
    needs = {key: float(getattr(core, key)) for key in NEEDS}
    crossed = any(previous.get(key, needs[key]) < .7 <= needs[key] for key in NEEDS)
    if crossed:
        state['crossed_pending'] = True
    crossed = bool(state.get('crossed_pending'))
    state['last_body'] = needs
    quiet = quiet_chats(plugin, state, now)
    due = due_events(state, now)
    token = item.get('start', '')
    finished = bool(item.get('source') == 'her' and end and now >= end and state.get('handled_item') != token)
    startup = not getattr(plugin, '_life_start_checked', False)
    plugin._life_start_checked = True
    valid = bool(item.get('source') == 'her' and phone._her_now_valid(item, local))
    if item.get('source') == 'schedule':
        valid = item.get('start') == daily.period_start(local).isoformat()
    startup = startup and not valid
    reason = ('刚才那件事到时候了' if finished or sleep else '程序刚起来，此刻是空的或过期了' if startup
              else '跟人聊完了，那个地方静下来了' if quiet else '身体有了新的感觉' if crossed else '到点了' if due else '')
    if gate == 'soft':
        fallback(plugin, core, now)
        state['pending'] = {'group_browse': False, 'go_browse': False}
        save_state(state)
        return False
    cooldown = not (finished or startup or sleep) and now - state.get('last_think_ts', 0) < 600
    if not reason or cooldown or state['today']['count'] >= 48:
        save_state(state)
        return False
    if getattr(plugin, '_neutral_model', None) is None or not plugin._llm_allowed('life'):
        plugin._life_start_checked = not startup
        save_state(state)
        return False
    state['last_think_ts'] = now
    state.pop('crossed_pending', None)
    state['today']['count'] += 1
    state['handled_item'] = token
    for here, exchange in quiet:
        state['quiet_seen'][here] = exchange
    state['due'] = [row for row in state.get('due', []) if row not in due]
    save_state(state)
    choices = menu(plugin)
    outfit = state.get('woke_date') == local.date().isoformat() and not look.read_look(phone.LOOK_PATH, local.date())
    prompt = materials(plugin, state, item, core, reason, now, choices, outfit)
    value = await plugin._llm_v2_call('life', prompt, lambda raw: parse(raw, choices),
                                      system_prompt=await plugin._persona_text(None))
    if not value:
        logger.warning('[ams-life] life choice ignored: invalid or unavailable answer')
        return False
    if not enabled(plugin) or budget(plugin) != 'ok':
        return False
    await apply_choice(plugin, value, core, now, outfit)
    return True


async def run(plugin):
    while True:
        try:
            await tick(plugin)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning('[ams-life] life tick failed (%s)', type(exc).__name__)
        await asyncio.sleep(60)


def start(plugin):
    # Her starts before App assigns its model. Readiness belongs to each tick.
    if not enabled(plugin):
        return
    observe_messages(plugin)
    task = getattr(plugin, '_life_task', None)
    if task is None or task.done():
        plugin._life_task = asyncio.create_task(run(plugin))


async def stop(plugin):
    tasks = [getattr(plugin, '_life_task', None), *getattr(plugin, '_life_photo_tasks', ())]
    tasks = [task for task in tasks if task is not None]
    for task in tasks:
        task.cancel()
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
