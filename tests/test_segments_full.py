# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Full quote and attachment fields from both offline adapters."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import unittest  # noqa: E402

import adapter_astrbot  # noqa: E402
import adapter_onebot  # noqa: E402
import events  # noqa: E402
import harness  # noqa: E402
from astrbot.api.message_components import Image, Plain, Record, Reply  # noqa: E402


def part(kind, **data):
    return {'type': kind, 'data': data}


def message(*parts):
    return {'post_type': 'message', 'message_type': 'group', 'group_id': 900001,
            'self_id': 20002, 'sender': {'user_id': 10001}, 'message': list(parts)}


class FullSegments(unittest.TestCase):
    def test_astrbot_quote_and_paths(self):
        quote = Reply(id='m1', sender_id='10001',
                      chain=[Plain('看这个'), Image(url='http://img.test/a.png'), Reply(id='m2')],
                      text='看这个', message_str='看这个')
        event = harness.FakeEvent('', group='900001')
        event.get_messages = lambda: [quote, Image(path='image.png'), Record(path='voice.amr')]
        segments = adapter_astrbot.from_astrbot(event).segments
        data = segments[0].data
        self.assertEqual((data['id'], data['sender_id'], data['text'], data['message_str']),
                         ('m1', '10001', '看这个', '看这个'))
        self.assertEqual(data['chain'][:2], (events.Segment('text', {'text': '看这个'}),
                         events.Segment('image', {'url': 'http://img.test/a.png', 'file': '', 'path': ''})))
        self.assertEqual(data['chain'][2].data['chain'], ())
        self.assertEqual(segments[1].data['path'], 'image.png')
        self.assertEqual(segments[2].data['path'], 'voice.amr')

    def test_astrbot_unreadable_chain(self):
        class Reply:
            @property
            def chain(self):
                raise ValueError('unreadable')

        event = harness.FakeEvent('', group='900001')
        event.get_messages = lambda: [Reply()]
        self.assertEqual(adapter_astrbot.from_astrbot(event).segments[0].data['chain'], ())

    def test_onebot_quote_and_paths(self):
        quoted = {'message_type': 'group', 'sender': {'user_id': 10001},
                  'message': [part('text', text=' 看 '), part('image', url='http://img.test/a.png'),
                              part('at', qq='10003')]}
        payload = message(part('reply', id='m1'), part('image', path='image.png'),
                          part('record', path='voice.amr'))
        segments = adapter_onebot.from_onebot(payload, quoted=quoted, names={'10003': '柠檬'}).segments
        data = segments[0].data
        self.assertEqual([segment.type for segment in data['chain']], ['text', 'image', 'at'])
        self.assertEqual((data['text'], data['message_str']), ('看 @柠檬(10003) ',) * 2)
        self.assertEqual(segments[1].data['path'], 'image.png')
        self.assertEqual(segments[2].data['path'], 'voice.amr')
        empty = adapter_onebot.from_onebot(payload).segments[0].data
        self.assertEqual((empty['chain'], empty['text'], empty['message_str']), ((), '', ''))
