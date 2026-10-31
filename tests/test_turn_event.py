# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Compare message gates with the frozen AstrBot behavior."""
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot
import adapter_astrbot_turn
import discretion
import events
import harness
import main
import turn
from astrbot.api.message_components import At, Plain, Reply


# mixin_memory.py 257 at 6568a29.
def old_here(event):
    return discretion.place_of(getattr(event, "unified_msg_origin", "") or "")


# mixin_settings.py 251-275 at 6568a29.
def old_speaker(event):
    sid = ""
    name = ""
    try:
        fn = getattr(event, "get_sender_id", None)
        if callable(fn):
            sid = str(fn() or "")
    except Exception:
        pass
    try:
        fn = getattr(event, "get_sender_name", None)
        if callable(fn):
            name = str(fn() or "")
    except Exception:
        pass
    try:
        obj = getattr(event, "message_obj", None)
        sender = getattr(obj, "sender", None) if obj is not None else None
        if sender is not None:
            if not sid:
                sid = str(getattr(sender, "user_id", "") or "")
            if not name:
                name = str(getattr(sender, "nickname", "") or "")
    except Exception:
        pass
    return sid.strip(), name.strip()


# mixin_phone.py 342-353 at 6568a29.
def old_addresses_her(event):
    try:
        self_id = str(getattr(getattr(event, "message_obj", None), "self_id", "") or "")
        if self_id:
            for comp in event.get_messages() or []:
                kind = type(comp).__name__
                if kind == "At" and str(getattr(comp, "qq", "") or "") == self_id:
                    return True
                if kind == "Reply" and str(getattr(comp, "sender_id", "") or "") == self_id:
                    return True
        return bool(getattr(event, "is_at_or_wake_command", False))
    except Exception:
        return False


# main.py 621 at 6568a29.
def old_self_id(event):
    return str(getattr(getattr(event, "message_obj", None), "self_id", "") or "")


class TurnEventTests(unittest.TestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)

        def event(group='900001'):
            ev = harness.FakeEvent('hello', sender='10001', name='Alice', group=group, self_id='20002')
            ev.is_at_or_wake_command = False
            return ev

        self.cases = [event(), event(None)]
        for part in (At(qq='20002'), At(qq='10003'),
                     Reply(id='m1', sender_id='20002'), Reply(id='m2', sender_id='10003')):
            ev = event()
            ev.get_messages = lambda part=part: [part, Plain('hello')]
            self.cases.append(ev)
        wake = event()
        wake.is_at_or_wake_command = True
        self.cases.append(wake)
        sender = event()
        sender.get_sender_id = sender.get_sender_name = None
        sender.message_obj.sender = types.SimpleNamespace(user_id='10003', nickname='Bob')
        self.cases.append(sender)
        self.cases.append(harness.FakeEvent('hello', sender=' 10001 ', name=' Alice ', group='900001'))
        missing_obj = event()
        missing_obj.message_obj = None
        self.cases.append(missing_obj)
        missing_place = event()
        del missing_place.unified_msg_origin
        self.cases.append(missing_place)

    def test_frozen_fields_for_astrbot_events(self):
        for index, ev in enumerate(self.cases):
            with self.subTest(event=index):
                self.assertEqual(self.plugin._here(ev), old_here(ev))
                self.assertEqual(self.plugin._speaker(ev), old_speaker(ev))
                self.assertEqual(self.plugin._addresses_her(ev), old_addresses_her(ev))
                self.assertEqual(adapter_astrbot_turn.incoming_of(ev).self_id, old_self_id(ev))

    def test_gates_match_for_turn_event(self):
        for enabled in (False, True):
            self.plugin.config = {'owner_qq': '10001' if enabled else '',
                                  'reply_private': ['10003'] if enabled else [],
                                  'reply_groups': ['900001'] if enabled else [],
                                  'ignore_senders': ['10003'] if enabled else [],
                                  'reply_other_groups_when_called': enabled}
            for index, ev in enumerate(self.cases):
                neutral = turn.TurnEvent(adapter_astrbot.from_astrbot(ev))
                for name in ('_here', '_speaker', '_addresses_her', '_private_allowed',
                             '_ignored_sender', '_message_may_speak'):
                    with self.subTest(enabled=enabled, event=index, gate=name):
                        gate = getattr(self.plugin, name)
                        self.assertEqual(gate(neutral), gate(ev))

    def test_turn_event_identity_stop_and_notes(self):
        incoming = adapter_astrbot.from_astrbot(self.cases[0])
        ev = turn.TurnEvent(incoming)
        self.assertFalse(ev.is_stopped())
        ev.stop_event()
        self.assertTrue(ev.is_stopped())
        ev._ams_check = {}
        self.assertEqual(ev._ams_check, {})
        self.assertNotEqual(turn.TurnEvent(incoming), turn.TurnEvent(incoming))

    def test_magic_mock_is_not_a_turn_event(self):
        self.assertIsInstance(adapter_astrbot_turn.incoming_of(MagicMock()), events.Incoming)

    def test_unreadable_event_is_forgiving(self):
        class Broken:
            @property
            def unified_msg_origin(self):
                raise RuntimeError('unreadable place')

            def get_messages(self):
                raise RuntimeError('unreadable message')

        ev = Broken()
        self.assertEqual(self.plugin._here(ev), '')
        self.assertFalse(self.plugin._addresses_her(ev))


if __name__ == '__main__':
    unittest.main()
