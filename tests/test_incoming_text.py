# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Platform words on Incoming, including the OneBot spelling rules."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot
import adapter_astrbot_turn
import harness
import main
import turn
from adapter_onebot import from_onebot
from astrbot.api.message_components import At, Plain
from test_adapter_onebot import message, part


# Frozen read from mixin_attention.py 337 at 2255b7f.
def old_words(event):
    return str(getattr(event, 'message_str', '') or '')


class BrokenWords:
    @property
    def message_str(self):
        raise ValueError('unreadable')


class AstrBotWords(unittest.TestCase):
    def test_platform_words_and_unreadable(self):
        for ev, expected in [(SimpleNamespace(message_str='hello'), 'hello'),
                             (SimpleNamespace(message_str=None), ''),
                             (SimpleNamespace(), ''), (BrokenWords(), '')]:
            with self.subTest(event=type(ev).__name__):
                self.assertEqual(adapter_astrbot.from_astrbot(ev).text, expected)

    def test_frozen_read_and_fresh_wake_check(self):
        ev = harness.FakeEvent('/hello')
        cases = [ev, SimpleNamespace(message_str=None), SimpleNamespace()]
        different = harness.FakeEvent('在吗 @柠檬(10003)')
        different.get_messages = lambda: [Plain('在吗'), At(qq='10003', name='柠檬')]
        cases.append(different)
        for case in cases:
            self.assertEqual(adapter_astrbot_turn.incoming_of(case).text, old_words(case))
        ev.message_str = 'hello'
        self.assertEqual(adapter_astrbot.from_astrbot(ev).text, old_words(ev))
        with self.assertRaises(ValueError):
            old_words(BrokenWords())
        self.assertEqual(adapter_astrbot_turn.incoming_of(BrokenWords()).text, '')

    def test_turn_event_call_and_browse_words(self):
        plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        plugin._last_reply_here = MagicMock(return_value=(0, []))
        plugin._attention_cfg = MagicMock(return_value={'names': ['小月']})
        for words in ('小月 hello', 'hello'):
            ev = harness.FakeEvent(words, group='900001')
            ev.is_at_or_wake_command = False
            wrapped = turn.TurnEvent(adapter_astrbot.from_astrbot(ev))
            self.assertEqual(plugin._why_called(wrapped), plugin._why_called(ev))
            self.assertEqual(plugin._message_words(wrapped).split('\n')[0],
                             plugin._message_words(ev).split('\n')[0])
        self.assertNotEqual(plugin._why_called(turn.TurnEvent(adapter_astrbot.from_astrbot(
            harness.FakeEvent('小月', group='900001')))), '')


class OneBotWords(unittest.TestCase):
    def test_spelling(self):
        cases = [
            ([part('text', text=' a '), part('image'), part('text', text=' b ')], {}, 'ab'),
            ([part('text', text='   ')], {}, ''),
            ([part('at', qq='10003')], {'10003': '柠檬'}, '@柠檬(10003)'),
            ([part('at', qq='20002'), part('at', qq='20002')], {'20002': '小月'}, '@小月(20002)'),
            ([part('at', qq='all')], {}, ''),
            ([part('text', text='x'), part('markdown', markdown='  card  '), part('text', text='y')], {}, 'x  card  y'),
            ([part('markdown', content=' card ')], {}, 'card'),
            ([part('markdown', markdown='  x  ')], {}, 'x'),
        ]
        for parts, names, expected in cases:
            with self.subTest(parts=parts):
                self.assertEqual(from_onebot(message(*parts), names=names).text, expected)


if __name__ == '__main__':
    unittest.main()
