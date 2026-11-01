# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What she sends, and the platform actions she asks for (messenger.py,
adapter_astrbot_messenger.py), and that the components are the plugin's own. All numbers,
names and links are made up."""
import asyncio
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE / 'stubs'))

import attention  # noqa: E402
import messenger  # noqa: E402
from adapter_astrbot_messenger import AstrBotMessenger  # noqa: E402
from astrbot.api.message_components import Image, Plain, Record  # noqa: E402
from events import Segment  # noqa: E402

PLACE = 'group:900001'                    # a group, made up
UMO = 'default:GroupMessage:900001'       # its session, made up


class RecordingContext:
    """A context that keeps what was sent; its answer or error is set per test."""

    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.sent = []

    async def send_message(self, umo, chain):
        self.sent.append((umo, chain))
        if self.error is not None:
            raise self.error
        return self.result


def shape(chain):
    """What a chain is made of: (class name, its attributes) of every component."""
    return [(type(component).__name__, vars(component)) for component in chain]


def send(context, segments, place=PLACE, umo=UMO):
    """Send these segments to this place, synchronously, for one test."""
    one = AstrBotMessenger(context, lambda p: umo if p == place else '', lambda: None)
    return asyncio.run(one.send(place, segments))


def call(bot, action, **params):
    """Ask for this action, synchronously, for one test."""
    one = AstrBotMessenger(RecordingContext(), lambda place: UMO, lambda: bot)
    return asyncio.run(one.call(action, **params))


GOOD = (Segment('text', {'text': '你好'}),
        Segment('face', {'id': 0}),                      # QQ's first face is 0, not empty
        Segment('face', {'id': '14'}),
        Segment('image', {'path': 'made-up.png'}),
        Segment('image', {'base64': 'AAAA'}),
        Segment('image', {'url': 'http://img.test/a.png'}),
        Segment('image', {'url': 'https://img.test/a.png'}),
        Segment('record', {'path': 'made-up.amr'}))


class TextSegments(unittest.TestCase):
    """Words and QQ faces, as attention.pieces splits them."""

    def test_words_and_faces_in_order(self):
        self.assertEqual(messenger.text_segments('你好[表情:微笑]呀'),
                         (Segment('text', {'text': '你好'}), Segment('face', {'id': 14}),
                          Segment('text', {'text': '呀'})))

    def test_every_split_follows_attention(self):
        for text in ('你好', '好的[表情:微笑]', '嗯[表情:调皮]！还有[表情:偷笑]', '[表情:哭]'):
            with self.subTest(text=text):
                self.assertEqual([(seg.type, seg.data.get('text', seg.data.get('id')))
                                  for seg in messenger.text_segments(text)],
                                 [(kind, value) for kind, value in attention.pieces(text)])

    def test_an_unknown_face_name_stays_words(self):
        self.assertEqual(messenger.text_segments('好[表情:没有这个]呀'),
                         (Segment('text', {'text': '好[表情:没有这个]呀'}),))

    def test_without_a_face_one_text(self):
        self.assertEqual(messenger.text_segments('你好呀'), (Segment('text', {'text': '你好呀'}),))

    def test_nothing_for_nothing(self):
        self.assertEqual(messenger.text_segments(''), ())
        self.assertEqual(messenger.text_segments(None), ())


class Checked(unittest.TestCase):
    """What a message she sends may be made of."""

    def test_the_table_passes(self):
        self.assertEqual(messenger.check_segments(GOOD), GOOD)

    def test_a_list_comes_back_as_a_tuple(self):
        self.assertEqual(messenger.check_segments(list(GOOD)), GOOD)

    def test_these_are_refused(self):
        refused = [Segment('text', {'text': ''}),
                   Segment('text', {'text': '   '}),
                   Segment('text', {}),
                   Segment('face', {}),
                   Segment('image', {}),                                      # no key at all
                   Segment('image', {'path': '', 'base64': ''}),              # two keys
                   Segment('image', {'path': 'made-up.png', 'url': 'http://img.test/a.png'}),
                   Segment('image', {'path': ''}),
                   Segment('image', {'url': ''}),
                   Segment('image', {'url': 'ftp://img.test/a.png'}),
                   Segment('image', {'url': 'img.test/a.png'}),
                   Segment('record', {}),
                   Segment('record', {'url': 'http://img.test/a.amr'}),
                   Segment('reply', {'id': 'm-1'}),
                   Segment('at', {'qq': '10001'}),
                   Segment('forward', {'id': 'f-1'}),
                   Segment('other', {'kind': 'Sticker'})]
        for segment in refused:
            with self.subTest(segment=segment):
                with self.assertRaises(ValueError):
                    messenger.check_segments((segment,))

    def test_one_bad_segment_refuses_them_all(self):
        with self.assertRaises(ValueError):
            messenger.check_segments(messenger.text_segments('你好') + (Segment('reply', {'id': 'm-1'}),))


class SameAsThePlugin(unittest.TestCase):
    """The components the messenger builds are the plugin's own."""

    @classmethod
    def setUpClass(cls):
        # The plugin mixins import common, which wants a data dir; running this file alone
        # gets a temporary one, outside the repository.
        cls.made = None
        if not os.environ.get('AMS_LIFE_DATA_DIR'):
            cls.made = tempfile.mkdtemp(prefix='ams-life-messenger-')
            cls.addClassCleanup(shutil.rmtree, cls.made, ignore_errors=True)
            cls.addClassCleanup(os.environ.pop, 'AMS_LIFE_DATA_DIR', None)
            os.environ['AMS_LIFE_DATA_DIR'] = cls.made
        import mixin_attention
        cls.plugin = mixin_attention.AttentionMixin()

    def test_the_words_and_faces_are_the_plugins_chain(self):
        for text in ('你好', '好的[表情:微笑]', '嗯[表情:调皮]！还有[表情:偷笑]'):
            with self.subTest(text=text):
                context = RecordingContext()
                send(context, messenger.text_segments(text))
                self.assertEqual([sent[0] for sent in context.sent], [UMO])
                self.assertEqual(shape(context.sent[0][1].chain), shape(self.plugin._chain_of(text).chain))

    def test_a_photo_and_a_sentence(self):
        context = RecordingContext()
        send(context, messenger.text_segments('看这个') + (Segment('image', {'path': 'made-up.png'}),))
        self.assertEqual(shape(context.sent[0][1].chain),
                         shape([Plain('看这个'), Image.fromFileSystem('made-up.png')]))

    def test_a_voice(self):
        context = RecordingContext()
        send(context, (Segment('record', {'path': 'made-up.amr'}),))
        self.assertEqual(shape(context.sent[0][1].chain), shape([Record.fromFileSystem('made-up.amr')]))

    def test_a_sticker_as_a_base64_picture(self):
        context = RecordingContext()
        send(context, (Segment('image', {'base64': 'AAAA'}),))
        self.assertEqual(shape(context.sent[0][1].chain), shape([Image.fromBase64('AAAA')]))


class NothingSent(unittest.TestCase):
    """Nothing goes when the place is unknown or a segment is not sendable."""

    def test_no_session_for_the_place(self):
        context = RecordingContext()
        self.assertEqual(send(context, messenger.text_segments('你好'), umo=''), messenger.Sent(False, ''))
        self.assertEqual(context.sent, [])

    def test_one_bad_segment_nothing_goes(self):
        context = RecordingContext()
        segments = messenger.text_segments('你好') + (Segment('reply', {'id': 'm-1'}),)
        with self.assertRaises(ValueError):
            send(context, segments)
        self.assertEqual(context.sent, [])


class WhatTheContextAnswers(unittest.TestCase):
    """What came of the send, as AstrBot's own answer says."""

    def test_false_is_not_sent(self):
        self.assertEqual(send(RecordingContext(result=False), messenger.text_segments('你好')),
                         messenger.Sent(False, ''))

    def test_true_is_sent(self):
        self.assertEqual(send(RecordingContext(result=True), messenger.text_segments('你好')),
                         messenger.Sent(True, ''))

    def test_none_is_sent(self):
        self.assertEqual(send(RecordingContext(result=None), messenger.text_segments('你好')),
                         messenger.Sent(True, ''))

    def test_an_error_is_raised_as_it_is(self):
        error = RuntimeError('offline failure')
        with self.assertRaises(RuntimeError) as caught:
            send(RecordingContext(error=error), messenger.text_segments('你好'))
        self.assertIs(caught.exception, error)


class _Api:
    """The adapter client AstrBot's bot carries: api.call_action."""

    def __init__(self, result):
        self.result = result
        self.seen = []

    async def call_action(self, action, **params):
        self.seen.append((action, params))
        return self.result


class _BotWithApi:
    def __init__(self, result):
        self.api = _Api(result)


class _BotWithoutApi:
    """A bot that answers call_action straight, as mixin_stickers expects."""

    def __init__(self, result):
        self.result = result
        self.seen = []

    async def call_action(self, action, **params):
        self.seen.append((action, params))
        return self.result


class Actions(unittest.TestCase):
    """The four allowed actions, and nothing else."""

    def test_the_four_actions_with_an_api(self):
        for action in sorted(messenger.ALLOWED_ACTIONS):
            with self.subTest(action=action):
                bot = _BotWithApi({'message_id': 'm-1'})
                self.assertEqual(call(bot, action, message_id='m-1', group_id='900001'),
                                 {'message_id': 'm-1'})
                self.assertEqual(bot.api.seen, [(action, {'message_id': 'm-1', 'group_id': '900001'})])

    def test_without_an_api_the_bot_is_asked(self):
        bot = _BotWithoutApi({'message_id': 'm-2'})
        self.assertEqual(call(bot, 'get_msg', message_id='m-2'), {'message_id': 'm-2'})
        self.assertEqual(bot.seen, [('get_msg', {'message_id': 'm-2'})])

    def test_an_action_not_in_the_list_is_refused(self):
        for action in ('send_like', 'delete_msg', 'set_qq_profile', 'set_group_kick'):
            with self.subTest(action=action):
                bot = _BotWithApi({'message_id': 'm-1'})
                with self.assertRaises(messenger.ActionRefused):
                    call(bot, action, user_id='10001')
                self.assertEqual(bot.api.seen, [])

    def test_no_bot(self):
        one = AstrBotMessenger(RecordingContext(), lambda place: UMO, lambda: None)
        with self.assertRaises(RuntimeError) as caught:
            asyncio.run(one.call('get_msg', message_id='m-1'))
        self.assertEqual(str(caught.exception), 'no bot')

    def test_what_is_not_a_dict_is_empty(self):
        for result in ('ok', None, [1], 0):
            with self.subTest(result=result):
                self.assertEqual(call(_BotWithApi(result), 'get_msg', message_id='m-1'), {})


class NoFramework(unittest.TestCase):
    """messenger.py is apart from AstrBot: its source never mentions it."""

    def test_the_source_does_not_mention_astrbot(self):
        source = (ROOT / 'messenger.py').read_text(encoding='utf-8')
        self.assertNotIn('astrbot', source.lower())


if __name__ == '__main__':
    unittest.main()
