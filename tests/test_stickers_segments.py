# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Recognize QQ stickers from neutral and raw message segments."""
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_onebot
import events
import stickers
import turn
from mixin_stickers import StickersMixin


def image(**data):
    return {'type': 'image', 'data': data}


def incoming(parts, quoted=None):
    payload = {'post_type': 'message', 'message_type': 'group', 'group_id': 900001,
               'user_id': 10001, 'self_id': 20002, 'message': parts}
    return adapter_onebot.from_onebot(payload, quoted=quoted)


class StickerSegmentsTest(unittest.TestCase):
    def test_onebot_preserves_markers_in_message_and_quote(self):
        quoted = {'message': [image(file='quoted.png', sub_type=1, summary=stickers.STICKER_SUMMARY)]}
        one = incoming([image(url='https://img.test/a', sub_type='1'),
                        image(file='b.png', summary=stickers.STICKER_SUMMARY),
                        image(file='plain.png'), {'type': 'reply', 'data': {'id': 'm'}}], quoted)
        self.assertEqual(one.segments[0].data['sub_type'], '1')
        self.assertEqual(one.segments[1].data['summary'], stickers.STICKER_SUMMARY)
        self.assertEqual((one.segments[2].data['sub_type'], one.segments[2].data['summary']), ('', ''))
        quote = one.segments[3].data['chain'][0].data
        self.assertEqual((quote['sub_type'], quote['summary']), ('1', stickers.STICKER_SUMMARY))

    def test_stickers_in_segments(self):
        segments = (events.Segment('image', {'url': 'a', 'file': 'a.png', 'sub_type': ' 1 '}),
                    events.Segment('image', {'url': 'plain'}),
                    events.Segment('image', {'file': 'b.png', 'summary': stickers.STICKER_SUMMARY}),
                    events.Segment('text', {'sub_type': '1'}))
        self.assertEqual(stickers.stickers_in_segments(segments),
                         [{'url': 'a', 'file': 'a.png'}, {'url': '', 'file': 'b.png'}])

    def test_turn_event_sticker_refs(self):
        one = incoming([image(url='https://img.test/sticker', sub_type='1'),
                        image(url='https://img.test/summary', summary=stickers.STICKER_SUMMARY),
                        image(url='https://img.test/plain')])
        self.assertEqual(StickersMixin._sticker_refs(None, turn.TurnEvent(one)),
                         ['https://img.test/sticker', 'https://img.test/summary'])

    def test_raw_message_sticker_refs(self):
        raw = {'message': [image(url='https://img.test/raw', sub_type='1'),
                           image(url='https://img.test/plain')]}
        event = types.SimpleNamespace(message_obj=types.SimpleNamespace(raw_message=raw))
        self.assertEqual(StickersMixin._sticker_refs(None, event), ['https://img.test/raw'])
        event.message_obj.raw_message = {'message': []}
        self.assertEqual(StickersMixin._sticker_refs(None, event), [])


if __name__ == '__main__':
    unittest.main()
