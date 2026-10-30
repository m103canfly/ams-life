"""Offline group-opening rules with a stand-in vision provider and forget registry."""
import asyncio
import sys
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
# Reuse the suite's prepared stubs and clock without replacing its global time.time.
from test_body_heart import CLOCK as _CLOCK  # noqa: E402,F401
import mixin_group_browse as groups  # noqa: E402
import mixin_media  # noqa: E402


def event(source='m1', sender='10001', group='900001', refs=(), wake=False):
    return SimpleNamespace(group=group, sender=sender, source=source, refs=list(refs), wake=wake,
                           message_obj=SimpleNamespace(self_id='20002', message_id=source))


def ref(n):
    return 'https://gchat.qpic.cn/fake%s.png' % n


class Dummy(groups.GroupBrowseMixin):
    def __init__(self):
        self.browse_groups_enabled = True
        self.config = {}
        self.looks, self.kept, self.cache = [], [], {}
        self.gone, self.gone_sources = set(), set()
        self.generation = 0
        self.spent = 0
        self.block = None

    def _here(self, ev): return 'group:' + ev.group
    def _speaker(self, ev): return ev.sender, ''
    def _source_ids(self, ev): return [ev.source]
    def _message_id(self, ev): return ev.source
    def _sticker_refs(self, ev): return ev.refs
    def _addresses_her(self, ev): return ev.wake
    def _job_stale(self): return False
    def _begin_job(self): pass
    def _forget_count(self): return self.generation
    def _stickers_on(self): return True
    def _llm_allowed(self, name): return True
    def _attention_cfg(self): return {'night_start': '01:00', 'night_end': '08:25', 'soft': 8, 'hard': 10}
    def _spent_today(self): return self.spent
    def _familiarity(self, person): return .7
    def _core(self, event): return SimpleNamespace(v=0)
    def _vision_provider_for(self, event, source='reply'): return object()
    def _load_image_cache(self): return dict(self.cache)
    def _save_image_cache(self, cache): self.cache = dict(cache)
    def _may_keep(self, people, place, stamp, sources):
        return not (set(people) & self.gone or set(sources) & self.gone_sources)
    async def _look_once(self, provider, url, ev):
        self.looks.append(url)
        if self.block is not None:
            await self.block.wait()
        return 'picture', {'caption': 'picture'}
    async def _maybe_keep(self, ev, url, look): self.kept.append(url)


class GroupBrowseTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.p = Dummy()

    async def test_import_preserves_shared_clock(self):
        self.assertIs(time.time, _CLOCK)

    def add(self, ev):
        self.p._group_heard(ev)
        self.p._group_queue_sticker(ev)

    async def test_off_does_not_queue_or_look(self):
        self.p.browse_groups_enabled = False
        self.add(event(refs=[ref(1)]))
        await self.p._group_browse_tick()
        self.assertEqual(self.p._group_state()['group:900001'].get('queue', []), [])
        self.assertEqual(self.p.looks, [])

    async def test_open_only_new_max_three_and_discards_overflow(self):
        self.add(event(refs=[ref(n) for n in range(4)]))
        self.assertEqual(self.p.looks, [])
        batch = self.p._group_open('group:900001')
        await self.p._group_look('group:900001', batch)
        self.assertEqual(self.p.looks, [ref(0), ref(1), ref(2)])
        self.assertEqual(self.p._group_open('group:900001')[0], [])

    async def test_expired_and_cached_are_skipped(self):
        self.add(event(refs=[ref(1), ref(2)]))
        queue = self.p._group_state()['group:900001']['queue']
        old = queue[0]
        queue[0] = (old[0], old[1] - 3601, old[2], old[3])
        self.p.cache[groups._sha256(ref(2))] = {'caption': 'cached'}
        await self.p._group_look('group:900001', self.p._group_open('group:900001'))
        self.assertEqual(self.p.looks, [])

    async def test_night_and_no_unread_do_not_browse(self):
        with patch.object(groups.attention, 'is_night', return_value=True):
            self.add(event(refs=[ref(1)]))
            await self.p._group_browse_tick()
            self.assertEqual(self.p.looks, [])
            self.assertEqual(self.p._group_action()[0], 'none')
        self.p._group_open('group:900001')
        with patch.object(groups.attention, 'is_night', return_value=False):
            self.assertNotEqual(self.p._group_action()[0], 'group')

    async def test_budget_checked_before_every_look(self):
        self.add(event(refs=[ref(1)]))
        self.p.spent = 10
        await self.p._group_look('group:900001', self.p._group_open('group:900001'))
        self.assertEqual(self.p.looks, [])

    async def test_budget_can_stop_between_two_pictures(self):
        async def look(provider, url, ev):
            self.p.looks.append(url)
            self.p.spent = 10
            return 'picture', {'caption': 'picture'}
        self.p._look_once = look
        self.add(event(refs=[ref(1), ref(2)]))
        await self.p._group_look('group:900001', self.p._group_open('group:900001'))
        self.assertEqual(self.p.looks, [ref(1)])

    async def test_forget_registry_and_delete_person_or_message(self):
        self.p.gone.add('10001')
        self.add(event(refs=[ref(1)]))
        self.assertEqual(self.p._group_state()['group:900001'].get('queue', []), [])
        self.p.gone.clear()
        self.add(event('m1', refs=[ref(1)]))
        self.add(event('m2', sender='10002', refs=[ref(2)]))
        self.p._group_forget_queue('10001')
        self.assertEqual([x[0] for x in self.p._group_state()['group:900001']['queue']], [ref(2)])
        self.p._group_forget_queue(source_ids=['m2'])
        self.assertEqual(self.p._group_state()['group:900001']['queue'], [])

    async def test_delete_during_look_drops_result(self):
        self.add(event(refs=[ref(1)]))
        self.p.block = asyncio.Event()
        task = asyncio.create_task(self.p._group_look('group:900001', self.p._group_open('group:900001')))
        await asyncio.sleep(0)
        self.p.generation += 1
        self.p.block.set()
        await task
        self.assertEqual(self.p.cache, {})
        self.assertEqual(self.p.kept, [])

    async def test_reply_opens_then_schedules_without_waiting_and_excludes_current(self):
        self.add(event('old', refs=[ref(n) for n in range(4)]))
        current = event('current', refs=[ref(4)], wake=True)
        self.p._group_reply_open(current)
        self.p.block = asyncio.Event()
        self.p._group_reply_after(current)
        self.assertEqual(self.p.looks, [])
        await asyncio.sleep(0)
        self.assertEqual(self.p.looks, [ref(0)])
        self.p.block.set()
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        self.assertEqual(self.p.looks, [ref(0), ref(1), ref(2)])

    async def test_reply_image_interrupts_batch_after_first_and_requeues_remaining(self):
        class ReplyDummy(Dummy, mixin_media.MediaMixin):
            async def _image_context_locked(self, event):
                self.order.append('reply')
                self.reply_started.set()
                return 'reply image'

        self.p = ReplyDummy()
        self.p.order = []
        self.p.reply_started = asyncio.Event()
        first_started, first_done = asyncio.Event(), asyncio.Event()
        second_done = asyncio.Event()

        async def look(provider, url, ev):
            self.p.looks.append(url)
            self.p.order.append(url)
            if url == ref(0):
                first_started.set()
                await first_done.wait()
            elif url == ref(1):
                await second_done.wait()
            return 'picture', {'caption': 'picture'}

        self.p._look_once = look
        self.add(event('old', refs=[ref(n) for n in range(3)]))
        browse = asyncio.create_task(self.p._group_look('group:900001', self.p._group_open('group:900001')))
        reply = None
        try:
            await asyncio.wait_for(first_started.wait(), 1)
            reply = asyncio.create_task(self.p._image_context(event('reply', wake=True, refs=[ref(4)])))
            await asyncio.sleep(0)
            self.assertEqual(self.p._group_reply_vision_active, 1)
            first_done.set()
            await asyncio.wait_for(self.p.reply_started.wait(), 1)
            self.assertEqual(await reply, 'reply image')
            await asyncio.wait_for(browse, 1)
            self.assertEqual(self.p.order, [ref(0), 'reply'])
            queue = self.p._group_state()['group:900001']['queue']
            self.assertEqual([x[0] for x in queue], [ref(1), ref(2)])
            second_done.set()
            await self.p._group_look('group:900001', self.p._group_open('group:900001'))
            self.assertEqual(self.p.looks, [ref(0), ref(1), ref(2)])
        finally:
            first_done.set()
            second_done.set()
            if reply is not None:
                await asyncio.gather(reply, return_exceptions=True)
            await asyncio.gather(browse, return_exceptions=True)

    async def test_text_reply_does_not_wait_or_interrupt_group_look(self):
        class ReplyDummy(Dummy, mixin_media.MediaMixin):
            async def _image_context_locked(self, event):
                raise AssertionError('text must not acquire the vision lock')

        self.p = ReplyDummy()
        self.p.block = asyncio.Event()
        self.add(event('old', refs=[ref(n) for n in range(3)]))
        browse = asyncio.create_task(self.p._group_look('group:900001', self.p._group_open('group:900001')))
        try:
            await asyncio.sleep(0)
            self.assertEqual(self.p.looks, [ref(0)])
            self.assertEqual(await asyncio.wait_for(self.p._image_context(event('text', wake=True)), 1), '')
            self.assertEqual(getattr(self.p, '_group_reply_vision_active', 0), 0)
        finally:
            self.p.block.set()
            await asyncio.gather(browse, return_exceptions=True)
        self.assertEqual(self.p.looks, [ref(0), ref(1), ref(2)])

    async def test_cached_reply_image_does_not_wait_for_vision_lock(self):
        class ReplyDummy(Dummy, mixin_media.MediaMixin):
            async def _image_context_locked(self, event):
                raise AssertionError('cached images must not acquire the vision lock')

        self.p = ReplyDummy()
        self.p.cache[groups._sha256(ref(4))] = {'caption': 'cached picture'}
        self.assertEqual(self.p._load_image_cache()[groups._sha256(ref(4))]['caption'], 'cached picture')
        async with self.p._group_image_lock():
            result = await asyncio.wait_for(self.p._image_context(event('reply', refs=[ref(4)])), 1)
        self.assertEqual(result, 'cached picture')
        self.assertEqual(getattr(self.p, '_group_reply_vision_active', 0), 0)

    async def test_disabled_image_caption_does_not_wait_for_vision_lock(self):
        class ReplyDummy(Dummy, mixin_media.MediaMixin):
            def _llm_allowed(self, name): return False

        self.p = ReplyDummy()
        async with self.p._group_image_lock():
            result = await asyncio.wait_for(self.p._image_context(event('reply', refs=[ref(4)])), 1)
        self.assertEqual(result, '')
        self.assertEqual(getattr(self.p, '_group_reply_vision_active', 0), 0)

    async def test_regular_image_rechecks_cache_after_waiting_for_lock(self):
        class ReplyDummy(Dummy, mixin_media.MediaMixin):
            image_llama_server = ''
            image_llama_model = ''
            image_service_port = 0
            def _image_refs(self, event): return event.refs
            def _stickers_on(self): return False

        self.p = ReplyDummy()
        async with self.p._group_image_lock():
            reply = asyncio.create_task(self.p._image_context(event('reply', refs=[ref(4)])))
            await asyncio.sleep(0)
            self.assertFalse(reply.done())
            self.assertEqual(self.p._group_reply_vision_active, 1)
            self.p.cache[groups._sha256(ref(4))] = {'caption': 'cached while waiting'}
            self.assertEqual(self.p._load_image_cache()[groups._sha256(ref(4))]['caption'], 'cached while waiting')
        self.assertEqual(await asyncio.wait_for(reply, 1), 'cached while waiting')
        self.assertEqual(self.p._group_reply_vision_active, 0)

    async def test_cancelled_reply_does_not_leave_priority_flag_set(self):
        class ReplyDummy(Dummy, mixin_media.MediaMixin):
            async def _image_context_locked(self, event):
                return ''

        self.p = ReplyDummy()
        async with self.p._group_image_lock():
            reply = asyncio.create_task(self.p._image_context(event('reply', wake=True, refs=[ref(4)])))
            await asyncio.sleep(0)
            self.assertEqual(self.p._group_reply_vision_active, 1)
            reply.cancel()
            await asyncio.gather(reply, return_exceptions=True)
            self.assertEqual(self.p._group_reply_vision_active, 0)

    async def test_deferred_pictures_still_obey_forgetting_and_expiry(self):
        self.add(event('old', sender='10001', refs=[ref(1)]))
        self.add(event('other', sender='10002', refs=[ref(2)]))
        self.p._group_reply_vision_active = 1
        await self.p._group_look('group:900001', self.p._group_open('group:900001'))
        self.p._group_reply_vision_active = 0
        self.p._group_forget_queue('10001')
        queue = self.p._group_state()['group:900001']['queue']
        self.assertEqual([x[0] for x in queue], [ref(2)])
        row = queue[0]
        queue[0] = (row[0], row[1] - 3601, row[2], row[3])
        await self.p._group_look('group:900001', self.p._group_open('group:900001'))
        self.assertEqual(self.p.looks, [])

    async def test_queue_limit_and_switch_clears(self):
        self.add(event(refs=[ref(n) for n in range(101)]))
        queue = self.p._group_state()['group:900001']['queue']
        self.assertEqual(len(queue), 100)
        self.assertEqual(queue[0][0], ref(1))
        self.p.browse_groups_enabled = False
        self.p._group_prune()
        self.assertEqual(self.p._group_state()['group:900001']['queue'], [])

    async def test_closing_switch_immediately_discards_queue(self):
        self.add(event(refs=[ref(1)]))
        self.p.browse_groups_enabled = False
        self.p.browse_groups_enabled = True
        self.assertEqual(self.p._group_state()['group:900001']['queue'], [])

    async def test_busy_and_low_score_do_not_open(self):
        self.add(event(refs=[ref(1)]))
        with patch.object(groups.attention, 'is_night', return_value=False):
            now = time.time()
            self.p._group_last_reply = now
            self.assertEqual(self.p._group_action(now + 60)[0], 'none')
            self.p._group_state()['group:900001']['opened'] = now
            self.assertNotEqual(self.p._group_action(now + 600)[0], 'group')

    async def test_action_uses_threshold_and_five_minute_safety_net(self):
        for n in range(8):
            self.add(event('m%d' % n))
        with patch.object(groups.attention, 'is_night', return_value=False):
            now = time.time()
            self.assertEqual(self.p._group_action(now)[0], 'group')
            self.p._group_last_browse = now
            self.assertEqual(self.p._group_action(now + 299)[0], 'none')

    async def test_groups_are_isolated_and_reply_current_image_is_excluded(self):
        self.add(event('old', group='900001', refs=[ref(1)]))
        self.add(event('other', group='900002', refs=[ref(2)]))
        self.add(event('current', group='900001', refs=[ref(3)]))
        current = event('current', group='900001', refs=[ref(3)], wake=True)
        self.p._group_reply_open(current)
        self.assertEqual([x[0] for x in current._ams_group_open[1][0]], [ref(1)])
        self.assertEqual([x[0] for x in self.p._group_state()['group:900002']['queue']], [ref(2)])

    async def test_failed_look_is_not_retried(self):
        async def fail(provider, url, ev):
            self.p.looks.append(url)
            raise ValueError('failed')
        self.p._look_once = fail
        self.add(event('m1', refs=[ref(1)]))
        await self.p._group_look('group:900001', self.p._group_open('group:900001'))
        self.add(event('m2', refs=[ref(1)]))
        await self.p._group_look('group:900001', self.p._group_open('group:900001'))
        self.assertEqual(self.p.looks, [ref(1)])

    async def test_concurrent_openings_share_deduplication(self):
        self.add(event('m1', refs=[ref(1)]))
        first = self.p._group_open('group:900001')
        self.add(event('m2', refs=[ref(1)]))
        second = self.p._group_open('group:900001')
        await asyncio.gather(self.p._group_look('group:900001', first),
                             self.p._group_look('group:900001', second))
        self.assertEqual(self.p.looks, [ref(1)])

    async def test_registry_is_checked_again_before_look(self):
        self.add(event('m1', refs=[ref(1)]))
        batch = self.p._group_open('group:900001')
        self.p.gone_sources.add('m1')
        await self.p._group_look('group:900001', batch)
        self.assertEqual(self.p.looks, [])

    async def test_deleting_person_clears_already_opened_batch(self):
        self.add(event('m1', refs=[ref(1)]))
        current = event('m2', wake=True)
        self.p._group_reply_open(current)
        self.p._group_forget_queue('10001')
        self.assertEqual(current._ams_group_open[1][0], [])
        self.p._group_reply_after(current)
        await asyncio.sleep(0)
        self.assertEqual(self.p.looks, [])


if __name__ == '__main__':
    unittest.main()
