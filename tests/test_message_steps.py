# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Check the message steps against the frozen AstrBot behavior."""
import ast
import dataclasses
import inspect
import sys
import textwrap
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot
import harness
import main
import mixin_attention
import mixin_turn
import turn


# main.py 601-643 at 1cf9e62.
OLD_MESSAGE = '''    if not self._private_allowed(event):
        logger.info("[ams-life] 别人的私聊，没收")
        event.stop_event()
        return
    if self._ignored_sender(event):
        logger.info("[ams-life] a message from a sender on ignore_senders: not answered, not kept")
        event.stop_event()
        return
    if not self.enabled:
        if not self._may_speak_in(self._here(event)):
            event.stop_event()
        return
    try:
        self._begin_job(self._here(event))
        self._check_registry(event)  # someone (or a message) she may not keep: nothing is stored
        self._window_add_message(event)
        self._listen_body(event)
        if getattr(self, "mood_events_enabled", False):
            self._mood_clock()
            _sid = str(self._speaker(event)[0] or "")
            _self_id = adapter_astrbot_turn.incoming_of(event).self_id
            if not (_self_id and _sid == _self_id):
                _why = self._why_called(event)
                setattr(event, "_mood_direct", bool(_why))
                _core = self._core(None)
                for _kind in mood_kinds(adapter_astrbot_turn.incoming_of(event).text, bool(_why)):
                    _familiar = self._familiarity(_sid)
                    _weight = (.6 + .4 * _familiar) if _kind == "criticism" else 1.0
                    if not _why and _familiar < .3:
                        _weight *= MOOD_BYSTANDER_WEIGHT
                    _core.mood_event(_kind, _weight)
                if self._mood_note_answer(event, _why):
                    _core.mood_event("answered")
                if not getattr(self, "self_decide", False) and not _why:
                    self._hear_mood(event)
        self._ensure_autonomy_task()  # the 5-minute loop also sweeps her phone
        self._group_heard(event)
        self._sticker_in_passing(event)  # queue an uncalled QQ sticker for a later opening
    except Exception as exc:
        logger.warning("[ams-life] window store failed (%s)", type(exc).__name__)
    finally:
        if not self._message_may_speak(event):
            event.stop_event()'''

# mixin_attention.py 242-318 at 1cf9e62.
OLD_DECISION = '''    if not self._private_allowed(event) or not self._message_may_speak(event):
        self._stop(event)
        return None
    cfg = self._attention_cfg()
    here = self._here(event)
    sid = str(self._speaker(event)[0] or "")
    private = here.startswith("private:")
    why = self._why_called(event)
    self._note_tie(sid, called_her=bool(why), private=private)
    st = self._window_state(here)
    now = time.time()
    night = attention.is_night(now, cfg["night_start"], cfg["night_end"])
    if getattr(self, "mood_events_enabled", False):
        self._mood_clock(now)
    if night:
        if not why:
            self._hear_mood(event)
            return None   # at night she never speaks up herself
        calls = [t for t in st.get("night_calls") or [] if now - float(t) < 3600] + [now]
        st["night_calls"] = calls
        answer, woken, until = attention.night_gate(calls, now, st.get("awake_until", 0.0))
        st["awake_until"] = until
        self._save_attention()
        if woken:
            self._woken_at = now   # (乙: woken up, a bit cross)
            if getattr(self, "mood_events_enabled", False):
                self._core(None).mood_event("woken")
        if not answer:
            self._stop(event)
            return None
    # wait a few seconds: only the last message of a stretch is judged
    st["seq"] = int(st.get("seq", 0) or 0) + 1
    st["called"] = st.get("called") or why
    mine = st["seq"]
    wait = WAIT_SECONDS["private" if private else "called" if why else "group"]
    if getattr(self, "mood_events_enabled", False):
        core = self._core(None)
        core._decay_to_now()
        wait = attention.mood_wait(wait, core.v, core.energy)
    await asyncio.sleep(wait)
    if st.get("seq") != mine:
        if not why:
            self._hear_mood(event)
        self._stop(event)   # more came meanwhile; that one decides (kept all the same)
        return None
    why = st.pop("called", "") or why
    # the two safety nets
    state = attention.budget(self._spent_today(), cfg["soft"], cfg["hard"])
    if state == "hard" or (state == "soft" and not (private and cfg["owner"] and sid == cfg["owner"])):
        logger.info("[ams-life] attention: the money of the day (%s), not answered", state)
        self._stop(event)
        if not why:
            self._hear_mood(event)
        return None
    if not private and not attention.hour_ok(st.get("sent") or [], now, cfg["group_hour_max"]):
        logger.info("[ams-life] attention: %d of hers in this group this hour, not answered", cfg["group_hour_max"])
        self._stop(event)
        if not why:
            self._hear_mood(event)
        return None
    if why:
        if getattr(event, "is_at_or_wake_command", False):
            return None   # AstrBot answers it as before
        return await self._ask_for_reply(event)
    if night or private:
        return None
    s = await self._score(event)
    limit = attention.threshold(cfg["level"])
    if getattr(self, "mood_events_enabled", False):
        core = self._core(None)
        core._decay_to_now()
        limit = attention.mood_threshold(cfg["level"], core.v, core.energy)
    if s >= limit:
        logger.info("[ams-life] attention: not called, %.2f over the threshold: asked", s)
        return await self._ask_for_reply(event)
    self._hear_mood(event)
    return None'''


def body_lines(method):
    source = textwrap.dedent(inspect.getsource(method))
    node = ast.parse(source).body[0]
    return source.splitlines()[node.body[1].lineno - 1:]


class SourceTests(unittest.TestCase):
    def test_frozen_message_body(self):
        self.assertEqual(body_lines(mixin_turn.TurnMixin._on_message), OLD_MESSAGE.splitlines())

    def test_frozen_decision_body(self):
        expected = OLD_DECISION.replace('return await self._ask_for_reply(event)', 'return "reply"')
        self.assertEqual(body_lines(mixin_attention.AttentionMixin._decision), expected.splitlines())

    def test_hooks_and_decision_have_no_old_bodies(self):
        for method in (main.BioCorePlugin.on_message, main.BioCorePlugin.on_message_decide):
            source = inspect.getsource(method)
            self.assertNotIn('_window_add_message', source)
            self.assertNotIn('self._decide(', source)
        self.assertNotIn('_ask_for_reply', inspect.getsource(mixin_attention.AttentionMixin._decision))


class Decision(mixin_attention.AttentionMixin):
    def __init__(self, score=0, called=False):
        self.state, self.score, self.called = {}, score, called

    def _attention_cfg(self):
        return {'night_start': '01:00', 'night_end': '08:25', 'level': 'normal',
                'soft': 8, 'hard': 10, 'owner': '', 'group_hour_max': 30, 'names': ['Alice']}

    def _here(self, event): return 'group:900001'
    def _private_allowed(self, event): return True
    def _message_may_speak(self, event): return True
    def _speaker(self, event): return ('10001', '')
    def _why_called(self, event): return 'name' if self.called else ''
    def _note_tie(self, *args, **kwargs): pass
    def _window_state(self, here): return self.state
    def _spent_today(self): return 0
    def _hear_mood(self, event): pass
    async def _score(self, event): return self.score
    async def _ask_for_reply(self, event): return 'request'


class MessageStepTests(unittest.IsolatedAsyncioTestCase):
    async def test_decide_preserves_requests(self):
        event = harness.FakeEvent('hello', group='900001')
        event.is_at_or_wake_command = False
        async def no_wait(_): pass
        with mock.patch.object(mixin_attention.attention, 'is_night', return_value=False), \
             mock.patch.object(mixin_attention.asyncio, 'sleep', no_wait):
            self.assertIsNone(await Decision()._decide(event))
            self.assertEqual(await Decision(called=True)._decide(event), 'request')
            self.assertEqual(await Decision(score=1)._decide(event), 'request')

    async def test_hook_reply_none_and_exceptions(self):
        plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        plugin.enabled = plugin.self_decide = True
        plugin._ignored_sender = lambda event: False
        plugin._private_allowed = plugin._message_may_speak = lambda event: True
        event = harness.FakeEvent('hello', group='900001')
        for decision, request, expected, warning in (
            ('reply', 'request', ['request'], False),
            (None, 'request', [], False),
            (ValueError(), 'request', [], True),
            ('reply', ValueError(), [], True),
            ('reply', None, [], False),
        ):
            with self.subTest(decision=decision, request=request):
                plugin._decision = mock.AsyncMock(side_effect=decision if isinstance(decision, Exception) else None,
                                                  return_value=decision)
                plugin._ask_for_reply = mock.AsyncMock(side_effect=request if isinstance(request, Exception) else None,
                                                       return_value=request)
                with mock.patch.object(main.logger, 'warning') as log:
                    self.assertEqual([item async for item in plugin.on_message_decide(event)], expected)
                    if warning:
                        log.assert_called_once_with('[ams-life] attention: the decision failed (%s)', 'ValueError')
                    else:
                        log.assert_not_called()
                self.assertEqual(plugin._ask_for_reply.await_count, int(decision == 'reply'))

    async def test_turn_event_message_and_decision(self):
        plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        plugin.config = {'owner_qq': '', 'reply_private': [], 'reply_groups': ['900001'],
                         'ignore_senders': []}
        plugin.enabled = plugin.self_decide = True
        private = harness.FakeEvent('hello', sender='10001')
        neutral = turn.TurnEvent(adapter_astrbot.from_astrbot(private), unified_msg_origin=private.unified_msg_origin)
        await plugin._on_message(neutral)
        self.assertTrue(neutral.is_stopped())
        blocked = turn.TurnEvent(adapter_astrbot.from_astrbot(private), unified_msg_origin=private.unified_msg_origin)
        self.assertIsNone(await plugin._decide_turn(blocked))
        self.assertTrue(blocked.is_stopped())

        event = harness.FakeEvent('Alice hello', group='900001')
        neutral = turn.TurnEvent(adapter_astrbot.from_astrbot(event), unified_msg_origin=event.unified_msg_origin)
        seen = []
        plugin._begin_job = lambda here: None
        plugin._check_registry = lambda event: None
        plugin._window_add_message = lambda event: seen.append(adapter_astrbot.from_astrbot(event)
                                                                 if event is not neutral else event.incoming)
        plugin._listen_body = plugin._group_heard = plugin._sticker_in_passing = lambda event: None
        plugin._ensure_autonomy_task = lambda: None
        await plugin._on_message(event)
        await plugin._on_message(neutral)
        self.assertEqual(len(seen), 2)
        # ts is when each Incoming was built: not part of what was kept
        self.assertEqual(dataclasses.replace(seen[0], ts=0), dataclasses.replace(seen[1], ts=0))

        decision = Decision()
        decision.enabled = decision.self_decide = True
        decision._ignored_sender = lambda event: False
        decision._last_reply_here = lambda here: (0, [])
        decision._addresses_her = lambda event: False
        decision._why_called = mixin_attention.AttentionMixin._why_called.__get__(decision)
        decision._decide_turn = mixin_turn.TurnMixin._decide_turn.__get__(decision)
        async def no_wait(_): pass
        with mock.patch.object(mixin_attention.attention, 'is_night', return_value=False), \
             mock.patch.object(mixin_attention.asyncio, 'sleep', no_wait):
            self.assertEqual(await decision._decide_turn(neutral), 'reply')
            self.assertIsNone(await decision._decision(event))


if __name__ == '__main__':
    unittest.main()
