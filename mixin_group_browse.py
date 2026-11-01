# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""In-memory group openings and the stickers encountered on those openings."""
from __future__ import annotations

try:
    from .common import *  # noqa: F401,F403
    from . import adapter_astrbot_turn, attention, stickers
except ImportError:
    from common import *  # noqa: F401,F403
    import adapter_astrbot_turn
    import attention
    import stickers


class _GroupEvent:
    def __init__(self, place, sender, source):
        self.unified_msg_origin = 'default:GroupMessage:' + place.split(':', 1)[1]
        self.message_obj = types.SimpleNamespace(message_id=source)
        self.message_str = ''
        self._sender = sender

    def get_sender_id(self):
        return self._sender

    def get_sender_name(self):
        return ''


class GroupBrowseMixin:
    @property
    def browse_groups_enabled(self):
        return bool(getattr(self, '_browse_groups_enabled', False))

    @browse_groups_enabled.setter
    def browse_groups_enabled(self, value):
        self._browse_groups_enabled = bool(value)
        if not self._browse_groups_enabled:
            self._group_switch_epoch = int(getattr(self, '_group_switch_epoch', 0)) + 1
            self._group_prune()

    def _group_state(self):
        state = getattr(self, '_group_open_state', None)
        if state is None:
            state = self._group_open_state = {}
        return state

    def _group_prune(self, now=None):
        now = time.time() if now is None else now
        state = self._group_state()
        if not getattr(self, 'browse_groups_enabled', False):
            for group in state.values():
                group['queue'] = []
                for rows in group.pop('pending', []):
                    rows.clear()
            return
        for group in state.values():
            group['queue'] = [x for x in group.get('queue', []) if 0 <= now - x[1] <= 3600][-100:]
            for rows in group.get('pending', []):
                rows[:] = [x for x in rows if 0 <= now - x[1] <= 3600]
            group['pending'] = [rows for rows in group.get('pending', []) if rows]

    def _group_heard(self, event):
        here = self._here(event)
        if not here.startswith('group:') or self._job_stale():
            return
        sid = str(self._speaker(event)[0] or '')
        if sid and sid == adapter_astrbot_turn.incoming_of(event).self_id:
            return
        now = time.time()
        group = self._group_state().setdefault(here, {})
        group.setdefault('first_unread', now)
        group['unread'] = min(int(group.get('unread', 0)) + 1, 100)
        people = group.setdefault('people', {})
        if sid:
            people[sid] = now
            if len(people) > 100:
                people.pop(min(people, key=people.get), None)
        self._group_prune(now)

    def _group_forget_queue(self, person='', source_ids=()):
        ids = set(str(x) for x in source_ids or ())
        for group in self._group_state().values():
            group['queue'] = [x for x in group.get('queue', [])
                              if not (person and x[2] == person) and x[3] not in ids]
            for rows in group.get('pending', []):
                rows[:] = [x for x in rows if not (person and x[2] == person) and x[3] not in ids]
            group.get('people', {}).pop(person, None)

    def _group_queue_sticker(self, event):
        self._group_prune()
        if not getattr(self, 'browse_groups_enabled', False) or not self._stickers_on():
            return
        here = self._here(event)
        if not here.startswith('group:') or self._job_stale() or self._addresses_her(event):
            return
        sid = str(self._speaker(event)[0] or '')
        ids = self._source_ids(event)
        now = time.time()
        try:
            if not self._may_keep([sid] if sid else [], here, now, ids):
                return
        except Exception:
            return
        queue = self._group_state().setdefault(here, {}).setdefault('queue', [])
        for ref in self._sticker_refs(event):
            if ref and stickers.check_image_url(ref)[0]:
                queue.append((ref, now, sid, ids[0] if ids else ''))
        del queue[:-100]

    def _group_open(self, here, current_id=''):
        now = time.time()
        self._group_prune(now)
        group = self._group_state().setdefault(here, {})
        rows = [x for x in group.pop('queue', []) if x[1] <= now
                and 0 <= now - x[1] <= 3600 and (not current_id or x[3] != current_id)]
        group.update(opened=now, unread=0, people={})
        group.pop('first_unread', None)
        if rows:
            group.setdefault('pending', []).append(rows)
        return rows, (self._forget_count(), getattr(self, '_group_switch_epoch', 0))

    def _group_reply_open(self, event):
        here = self._here(event)
        if not here.startswith('group:') or getattr(event, '_ams_group_open', None) is not None:
            return
        ids = self._source_ids(event)
        rows, mark = self._group_open(here, ids[0] if ids else '')
        current = set(self._sticker_refs(event))
        rows[:] = [x for x in rows if x[0] not in current]
        setattr(event, '_ams_group_open', (here, (rows, mark)))

    def _group_reply_after(self, event):
        if getattr(self, 'enabled', True):
            self._group_last_reply = time.time()
        opened = getattr(event, '_ams_group_open', None)
        if opened is None:
            return
        setattr(event, '_ams_group_open', None)
        self._group_last_reply = time.time()
        here, batch = opened
        self._group_state().setdefault(here, {})['last_reply'] = self._group_last_reply
        if batch[0] and getattr(self, 'browse_groups_enabled', False):
            asyncio.create_task(self._group_look(here, batch))

    def _group_action(self, now=None):
        now = time.time() if now is None else float(now)
        self._group_prune(now)
        if not getattr(self, 'browse_groups_enabled', False):
            return 'none', ''
        cfg = self._attention_cfg()
        # Until the mood block supplies its tiredness interpretation, only night rules it out.
        if attention.is_night(now, cfg['night_start'], cfg['night_end']):
            return 'none', ''
        quiet = (now - float(getattr(self, '_group_last_reply', 0) or 0)) / 60
        if quiet < 5:
            return 'none', ''
        try:
            interval = max(5.0, float((getattr(self, 'config', None) or {}).get('browse_groups_min_minutes', 5)))
        except (TypeError, ValueError):
            interval = 5.0
        if now - float(getattr(self, '_group_last_browse', 0) or 0) < interval * 60:
            return 'none', ''
        hour = time.localtime(now).tm_hour
        mood = max(-1.0, min(1.0, float(getattr(self._core(None), 'v', 0) or 0)))
        choices = []
        for here, group in self._group_state().items():
            if not self._may_speak_in(here):
                continue
            unread = int(group.get('unread', 0) or 0)
            if not unread:
                continue
            known = max([self._familiarity(p) for p, ts in group.get('people', {}).items()
                         if 0 <= now - ts <= 3600] or [0.0])
            age = min(max((now - float(group.get('opened', 0) or 0)) / 10800, 0), 1)
            idle = min(max((quiet - 5) / 60, 0), 1)
            waiting = 0 < now - float(group.get('last_reply', 0) or 0) <= 3600
            score = (.35 * idle + .4 * min(unread / 8, 1) + .25 * known + .2 * age
                     + .2 * waiting + (.15 if 8 <= hour < 10 or 22 <= hour < 24 else 0)
                     + .05 * mood + .3 * min(max((now - group.get('first_unread', now)) / 43200, 0), 1))
            choices.append((-score, float(group.get('opened', 0) or 0), here))
        if getattr(self, 'browse_groups_enabled', False) and choices:
            best = min(choices)
            if -best[0] >= .8:
                return 'group', best[2]
        return ('web', '') if quiet >= 60 else ('none', '')

    async def _group_browse_tick(self):
        try:
            from . import life_loop
        except ImportError:
            import life_loop
        if life_loop.enabled(self):
            if not life_loop.consume(self, 'group_browse') or not self.browse_groups_enabled:
                return
            self._group_prune()
            places = [here for here, group in self._group_state().items()
                      if (group.get('unread') or group.get('queue')) and self._may_speak_in(here)]
            if not places:
                return
            here = min(places, key=lambda p: (self._group_state()[p].get('opened', 0), p))
            action = 'group'
        else:
            action, here = self._group_action()
        if action == 'web':
            return  # Connect PR #41 after its scheduler and entry point are verified.
        if action != 'group' or not self._may_speak_in(here):
            return
        batch = self._group_open(here)
        self._group_last_browse = time.time()
        if batch[0]:
            asyncio.create_task(self._group_look(here, batch))

    def _group_image_lock(self):
        lock = getattr(self, '_group_vision_lock', None)
        if lock is None:
            lock = self._group_vision_lock = asyncio.Lock()
        return lock

    async def _group_look(self, here, batch):
        paused = False
        try:
            paused = await self._group_look_pending(here, batch)
        finally:
            rows = batch[0]
            group = self._group_state().get(here, {})
            pending = group.get('pending', [])
            pending[:] = [item for item in pending if item is not rows]
            if (paused and getattr(self, 'browse_groups_enabled', False)
                    and (self._forget_count(), getattr(self, '_group_switch_epoch', 0)) == batch[1]):
                now = time.time()
                remaining = [x for x in rows if 0 <= now - x[1] <= 3600]
                group['queue'] = sorted(remaining + group.get('queue', []), key=lambda x: x[1])[-100:]
            rows.clear()

    async def _group_look_pending(self, here, batch):
        rows, mark = batch
        if not getattr(self, 'browse_groups_enabled', False) or not self._stickers_on():
            return
        if not self._llm_allowed('image_caption'):
            return
        self._begin_job()
        count = 0
        while rows and count < 3 and getattr(self, 'browse_groups_enabled', False):
            if getattr(self, '_group_reply_vision_active', 0):
                return True
            keep = None
            async with self._group_image_lock():
                if getattr(self, '_group_reply_vision_active', 0):
                    return True
                if not rows:
                    break
                ref, stamp, sender, source = rows.pop(0)
                attempted = getattr(self, '_group_failed_refs', None)
                if attempted is None:
                    attempted = self._group_failed_refs = {}
                now = time.time()
                for old in [k for k, v in attempted.items() if now - v > 3600]:
                    attempted.pop(old, None)
                cache = self._load_image_cache()
                key = _sha256(ref)
                if key in cache or key in attempted or not (0 <= time.time() - stamp <= 3600):
                    continue
                try:
                    if (self._forget_count(), getattr(self, '_group_switch_epoch', 0)) != mark or self._job_stale() or not self._may_keep(
                            [sender] if sender else [], here, stamp, [source] if source else []):
                        continue
                    cfg = self._attention_cfg()
                    if attention.budget(self._spent_today(), cfg['soft'], cfg['hard']) == 'hard':
                        break
                    event = _GroupEvent(here, sender, source)
                    event._ams_group_origin = ([sender] if sender else [], here, stamp,
                                               [source] if source else [])
                    provider = self._vision_provider_for(event, source="browse")
                    if provider is None:
                        break
                    attempted[key] = time.time()
                    count += 1
                    caption, look = await self._look_once(provider, ref, event)
                    if (not caption or not getattr(self, 'browse_groups_enabled', False)
                            or (self._forget_count(), getattr(self, '_group_switch_epoch', 0)) != mark or self._job_stale()
                            or not self._may_keep([sender] if sender else [], here, stamp,
                                                  [source] if source else [])):
                        continue
                    cache[key] = stickers.cache_entry(ref, look, sender, here, time.time())
                    self._save_image_cache(cache)
                    attempted.pop(key, None)
                    keep = (event, ref, look)
                except Exception as exc:
                    logger.warning('[ams-life] group sticker look failed (%s)', type(exc).__name__)
            if keep is not None:
                try:
                    await self._maybe_keep(*keep)
                except Exception as exc:
                    logger.warning('[ams-life] group sticker keep failed (%s)', type(exc).__name__)
        return False
