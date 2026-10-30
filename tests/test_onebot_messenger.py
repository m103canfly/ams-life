# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What the OneBot messenger sends to NapCat, and the actions it asks for.

Every number, link and file name here is made up (10001, 10003, 900001); every file is written
in a temporary folder of this test's own, and the folder is removed afterwards.

The last class compares what ``OneBotMessenger`` sends with what AstrBot 4.29.3 would send for
the same segments, written by hand from AstrBot's own rules, so moving to our own NapCat
connection does not change what NapCat receives.
"""
import asyncio
import base64
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE / 'stubs'))

import messenger  # noqa: E402
from adapter_onebot_messenger import (  # noqa: E402
    MAX_FILE_BYTES, ActionFailed, OneBotMessenger, to_onebot)
from events import Segment  # noqa: E402

GROUP = '900001'        # a group, made up
HIM = '10001'           # someone in the group, made up
OTHER = '10003'         # someone else, made up
PHOTO = b'made-up-picture-bytes'   # not a real picture
VOICE = b'made-up-voice-bytes'     # not a real voice
PREFIX = 'base64://'


def ok(data=None, retcode=0):
    """The frame NapCat answers a call with when it worked."""
    return {'status': 'ok', 'retcode': retcode, 'data': data}


def failed(retcode=100):
    """The frame NapCat answers a call with when it did not."""
    return {'status': 'failed', 'retcode': retcode, 'data': None}


def base64_ref(payload):
    """The "base64://" file reference AstrBot sends for these bytes."""
    return PREFIX + base64.b64encode(payload).decode('ascii')


class Api:
    """A fake call_api: it keeps every call, and answers what the test set or raises it."""

    def __init__(self, answer=None, error=None):
        self.answer = ok() if answer is None else answer
        self.error = error
        self.calls = []

    async def __call__(self, action, params):
        self.calls.append((action, dict(params)))
        if self.error is not None:
            raise self.error
        return self.answer

    @property
    def actions(self):
        """The actions of every call, in order."""
        return [action for action, _ in self.calls]

    @property
    def message(self):
        """The OneBot segments of the one send."""
        return self.calls[0][1]['message']


def send(api, place, segments, roots=()):
    """Send these segments to this place, synchronously, for one test."""
    return asyncio.run(OneBotMessenger(api, roots=roots).send(place, segments))


def call(api, action, **params):
    """Ask for this action, synchronously, for one test."""
    return asyncio.run(OneBotMessenger(api, roots=()).call(action, **params))


class InFiles(unittest.TestCase):
    """A temporary folder of this test's own (her data folder), with a picture and a voice in it."""

    def setUp(self):
        self.made = tempfile.TemporaryDirectory(prefix='ams-life-onebot-')
        self.addCleanup(self.made.cleanup)
        self.folder = Path(self.made.name)
        self.roots = (str(self.folder),)
        self.photo = self.write('photo.png', PHOTO)
        self.voice = self.write('voice.amr', VOICE)

    def write(self, name, data):
        """One made-up file in her folder."""
        path = self.folder / name
        path.write_bytes(data)
        return path

    def folder_beside(self):
        """Another temporary folder, outside her folders."""
        other = tempfile.TemporaryDirectory(prefix='ams-life-onebot-elsewhere-')
        self.addCleanup(other.cleanup)
        return Path(other.name)


class Segments(InFiles):
    """The table: each sendable segment becomes one OneBot 11 segment."""

    def test_text(self):
        self.assertEqual(to_onebot((Segment('text', {'text': '你好'}),), self.roots),
                         [{'type': 'text', 'data': {'text': '你好'}}])

    def test_face(self):
        for given, onebot in ((14, '14'), ('14', '14'), (0, '0')):
            with self.subTest(given=given):
                self.assertEqual(to_onebot((Segment('face', {'id': given}),), self.roots),
                                 [{'type': 'face', 'data': {'id': onebot}}])

    def test_a_picture_from_a_file_is_read_as_base64(self):
        self.assertEqual(to_onebot((Segment('image', {'path': str(self.photo)}),), self.roots),
                         [{'type': 'image', 'data': {'file': base64_ref(PHOTO)}}])

    def test_a_picture_from_base64_gets_the_prefix_once(self):
        for given, onebot in (('AAAA', PREFIX + 'AAAA'), (PREFIX + 'AAAA', PREFIX + 'AAAA')):
            with self.subTest(given=given):
                self.assertEqual(to_onebot((Segment('image', {'base64': given}),), self.roots),
                                 [{'type': 'image', 'data': {'file': onebot}}])

    def test_a_picture_from_a_url_keeps_the_url(self):
        for url in ('http://img.test/a.png', 'https://img.test/b.png'):
            with self.subTest(url=url):
                self.assertEqual(to_onebot((Segment('image', {'url': url}),), self.roots),
                                 [{'type': 'image', 'data': {'file': url}}])

    def test_a_voice_from_a_file_is_read_as_base64(self):
        self.assertEqual(to_onebot((Segment('record', {'path': str(self.voice)}),), self.roots),
                         [{'type': 'record', 'data': {'file': base64_ref(VOICE)}}])

    def test_the_order_of_the_segments_is_kept(self):
        segments = (Segment('text', {'text': '看'}), Segment('image', {'path': str(self.photo)}),
                    Segment('face', {'id': 14}), Segment('text', {'text': '这个'}))
        self.assertEqual([part['type'] for part in to_onebot(segments, self.roots)],
                         ['text', 'image', 'face', 'text'])

    def test_the_bytes_read_back_are_the_file(self):
        parts = to_onebot((Segment('image', {'path': str(self.photo)}),
                           Segment('record', {'path': str(self.voice)}),
                           Segment('image', {'base64': 'AAAA'})), self.roots)
        for part, payload in zip(parts, (PHOTO, VOICE)):
            self.assertTrue(part['data']['file'].startswith(PREFIX))
            self.assertEqual(base64.b64decode(part['data']['file'][len(PREFIX):]), payload)
        self.assertEqual(parts[2]['data'], {'file': PREFIX + 'AAAA'})   # base64 is not decoded

    def test_these_are_refused(self):
        for segment in (Segment('text', {'text': '   '}), Segment('face', {}),
                        Segment('image', {}), Segment('record', {}),
                        Segment('reply', {'id': 'm-1'}), Segment('at', {'qq': HIM})):
            with self.subTest(segment=segment):
                with self.assertRaises(ValueError):
                    to_onebot((segment,), self.roots)

    def test_one_bad_segment_refuses_them_all(self):
        with self.assertRaises(ValueError):
            to_onebot((Segment('text', {'text': '你好'}), Segment('reply', {'id': 'm-1'})), self.roots)

    def test_no_segments_no_parts(self):
        self.assertEqual(to_onebot((), self.roots), [])
        self.assertEqual(to_onebot(None, self.roots), [])

    def test_the_most_a_file_may_be(self):
        self.assertEqual(MAX_FILE_BYTES, 20 * 1024 * 1024)
        largest = self.write('largest.bin', b'x' * MAX_FILE_BYTES)
        part = to_onebot((Segment('image', {'path': str(largest)}),), self.roots)[0]
        self.assertEqual(len(base64.b64decode(part['data']['file'][len(PREFIX):])), MAX_FILE_BYTES)


class HerFolders(InFiles):
    """A local file goes only when it is a file inside her folders; nothing is called otherwise."""

    def refused(self, path, roots=None):
        """Sending this local file raises ValueError and calls nothing."""
        api = Api()
        with self.assertRaises(ValueError):
            send(api, 'group:' + GROUP, (Segment('image', {'path': str(path)}),),
                 self.roots if roots is None else roots)
        self.assertEqual(api.calls, [])

    def test_a_file_inside_her_folders_goes(self):
        api = Api()
        self.assertEqual(send(api, 'group:' + GROUP, (Segment('image', {'path': str(self.photo)}),),
                              self.roots), messenger.Sent(True, ''))
        self.assertEqual(api.actions, ['send_group_msg'])

    def test_a_file_outside_her_folders_is_refused(self):
        outside = self.folder_beside() / 'photo.png'
        outside.write_bytes(PHOTO)
        self.refused(outside)

    def test_a_dot_dot_that_leaves_her_folders_is_refused(self):
        outside = self.folder_beside() / 'photo.png'
        outside.write_bytes(PHOTO)
        escape = self.folder / '..' / outside.parent.name / outside.name
        self.assertEqual(escape.resolve(), outside.resolve())   # the path really leaves the folder
        self.refused(escape)

    def test_a_folder_is_refused(self):
        inside = self.folder / 'screenshots'
        inside.mkdir()
        self.refused(inside)

    def test_a_file_too_big_is_refused(self):
        self.refused(self.write('huge.bin', b'x' * (MAX_FILE_BYTES + 1)))

    def test_a_file_that_is_not_there_is_refused(self):
        self.refused(self.folder / 'not-there.png')

    def test_without_a_folder_no_local_file_goes(self):
        self.refused(self.photo, ())

    def test_a_file_in_a_later_folder_goes(self):
        other = self.folder_beside()
        path = other / 'photo.png'
        path.write_bytes(PHOTO)
        api = Api()
        self.assertEqual(send(api, 'private:' + HIM, (Segment('image', {'path': str(path)}),),
                              (str(self.folder), str(other))), messenger.Sent(True, ''))
        self.assertEqual(api.actions, ['send_private_msg'])


class Sending(InFiles):
    """One message to one place, and what came of it."""

    def test_a_group_gets_send_group_msg_with_a_number(self):
        api = Api(answer=ok({'message_id': 12345}))
        self.assertEqual(send(api, 'group:' + GROUP, (Segment('text', {'text': '你好'}),)),
                         messenger.Sent(True, '12345'))
        self.assertEqual(api.actions, ['send_group_msg'])
        _, params = api.calls[0]
        self.assertEqual(params['group_id'], int(GROUP))
        self.assertIsInstance(params['group_id'], int)
        self.assertEqual(params['message'], [{'type': 'text', 'data': {'text': '你好'}}])

    def test_a_private_chat_gets_send_private_msg_with_a_number(self):
        api = Api(answer=ok({'message_id': 'm-1'}))
        self.assertEqual(send(api, 'private:' + HIM, (Segment('text', {'text': '在吗'}),)),
                         messenger.Sent(True, 'm-1'))
        self.assertEqual(api.actions, ['send_private_msg'])
        _, params = api.calls[0]
        self.assertEqual(params['user_id'], int(HIM))
        self.assertIsInstance(params['user_id'], int)

    def test_a_place_that_is_not_a_place_sends_nothing(self):
        for place in ('group:abc', 'other:x', '', 'group:', 'private:', 'group:10 01',
                      'group:+900001', 'group:-1'):
            with self.subTest(place=place):
                api = Api()
                self.assertEqual(send(api, place, (Segment('text', {'text': '你好'}),)),
                                 messenger.Sent(False, ''))
                self.assertEqual(api.calls, [])

    def test_ok_without_a_message_id_is_sent_with_an_empty_one(self):
        for data in ({}, None, {'other': 1}):
            with self.subTest(data=data):
                api = Api(answer=ok(data))
                self.assertEqual(send(api, 'group:' + GROUP, (Segment('text', {'text': '你好'}),)),
                                 messenger.Sent(True, ''))

    def test_an_answer_that_is_not_ok_is_not_sent(self):
        for answer in (failed(), dict(failed(100), data={'message_id': 12345}),
                       {'status': 'async', 'retcode': 1, 'data': {'message_id': 1}},
                       {'retcode': 0, 'data': {'message_id': 1}}):
            with self.subTest(answer=answer):
                api = Api(answer=answer)
                self.assertEqual(send(api, 'group:' + GROUP, (Segment('text', {'text': '你好'}),)),
                                 messenger.Sent(False, ''))
                self.assertEqual(api.actions, ['send_group_msg'])

    def test_no_segments_calls_nothing(self):
        for segments in ((), [], None):
            with self.subTest(segments=segments):
                api = Api()
                self.assertEqual(send(api, 'group:' + GROUP, segments), messenger.Sent(False, ''))
                self.assertEqual(api.calls, [])

    def test_one_bad_segment_sends_nothing(self):
        for segments in ((Segment('text', {'text': '你好'}), Segment('reply', {'id': 'm-1'})),
                         (Segment('text', {'text': '   '}),),   # only whitespace: nothing to send
                         (Segment('record', {'url': 'http://v.test/a.amr'}),)):
            with self.subTest(segments=segments):
                api = Api()
                with self.assertRaises(ValueError):
                    send(api, 'group:' + GROUP, segments)
                self.assertEqual(api.calls, [])

    def test_a_local_file_outside_her_folders_sends_nothing(self):
        outside = self.folder_beside() / 'photo.png'
        outside.write_bytes(PHOTO)
        api = Api()
        with self.assertRaises(ValueError):
            send(api, 'group:' + GROUP, (Segment('image', {'path': str(outside)}),), self.roots)
        self.assertEqual(api.calls, [])

    def test_an_error_is_raised_as_it_is(self):
        error = RuntimeError('offline failure')
        api = Api(error=error)
        with self.assertRaises(RuntimeError) as caught:
            send(api, 'group:' + GROUP, (Segment('text', {'text': '你好'}),))
        self.assertIs(caught.exception, error)


class Actions(unittest.TestCase):
    """The four allowed actions, and nothing else."""

    def test_the_four_actions_with_their_parameters(self):
        for action in sorted(messenger.ALLOWED_ACTIONS):
            with self.subTest(action=action):
                api = Api(answer=ok({'message_id': 'm-1'}))
                self.assertEqual(call(api, action, message_id='m-1', group_id=GROUP),
                                 {'message_id': 'm-1'})
                self.assertEqual(api.calls, [(action, {'message_id': 'm-1', 'group_id': GROUP})])

    def test_data_that_is_not_a_dict_is_empty(self):
        for data in ('ok', None, [1], 0):
            with self.subTest(data=data):
                api = Api(answer=ok(data))
                self.assertEqual(call(api, 'get_msg', message_id='m-1'), {})

    def test_an_answer_that_is_not_ok_raises_with_the_retcode(self):
        api = Api(answer=failed(1200))
        with self.assertRaises(ActionFailed) as caught:
            call(api, 'get_msg', message_id='m-1')
        self.assertEqual(caught.exception.retcode, 1200)
        self.assertEqual(caught.exception.action, 'get_msg')
        self.assertIsInstance(caught.exception, RuntimeError)
        self.assertEqual(api.actions, ['get_msg'])

    def test_an_action_outside_the_list_is_refused(self):
        for action in ('delete_msg', 'send_like', 'set_qq_profile', 'send_qzone_msg'):
            with self.subTest(action=action):
                api = Api()
                with self.assertRaises(messenger.ActionRefused):
                    call(api, action, user_id=HIM)
                self.assertEqual(api.calls, [])


def astrbot_sends(segments):
    """What AstrBot 4.29.3 hands NapCat for these segments, written by hand.

    The rules, from astrbot/core/platform/sources/aiocqhttp/aiocqhttp_message_event.py
    (36-125): a local picture or voice is read from its file and sent as base64, never as a
    local path; a picture given as base64 keeps one "base64://" prefix; a picture given as a
    url sends the url; words are sent as they are; a face sends its id as a string. No segments
    send nothing, and words that are only whitespace are not sent.
    """
    out = []
    for segment in segments or ():
        kind, data = segment.type, segment.data
        if kind == 'text':
            if not str(data['text']).strip():
                continue   # AstrBot sends no words that are only whitespace
            out.append({'type': 'text', 'data': {'text': str(data['text'])}})
        elif kind == 'face':
            out.append({'type': 'face', 'data': {'id': str(data['id'])}})
        elif kind == 'image':
            if 'path' in data:
                payload = Path(str(data['path'])).read_bytes()
                out.append({'type': 'image', 'data': {'file': base64_ref(payload)}})
            elif 'base64' in data:
                given = str(data['base64'])
                out.append({'type': 'image',
                            'data': {'file': given if given.startswith(PREFIX) else PREFIX + given}})
            else:
                out.append({'type': 'image', 'data': {'file': str(data['url'])}})
        elif kind == 'record':
            payload = Path(str(data['path'])).read_bytes()
            out.append({'type': 'record', 'data': {'file': base64_ref(payload)}})
    return out


class SameAsAstrBot(InFiles):
    """The same segments, sent by us and (by hand) the way AstrBot 4.29.3 sends them."""

    def check(self, segments, case):
        with self.subTest(case=case):
            api = Api(answer=ok({'message_id': 'm-1'}))
            send(api, 'group:' + GROUP, segments, self.roots)
            self.assertEqual(len(api.calls), 1)
            self.assertEqual(api.message, astrbot_sends(segments))

    def test_words_and_a_face(self):
        self.check((Segment('text', {'text': '你好'}), Segment('face', {'id': 14})), 'words and a face')

    def test_a_photo_and_a_sentence(self):
        segments = (Segment('text', {'text': '看这个'}), Segment('image', {'path': str(self.photo)}))
        self.check(segments, 'a photo and a sentence')
        sent = to_onebot(segments, self.roots)[1]
        self.assertEqual(sent['data']['file'], base64_ref(PHOTO))   # the picture itself, not a path
        self.assertNotIn(str(self.photo), sent['data']['file'])

    def test_a_voice(self):
        segments = (Segment('record', {'path': str(self.voice)}),)
        self.check(segments, 'a voice')
        self.assertEqual(to_onebot(segments, self.roots)[0]['data']['file'], base64_ref(VOICE))

    def test_a_sticker_as_base64(self):
        self.check((Segment('image', {'base64': 'AAAA'}),), 'a sticker')

    def test_a_picture_from_a_url(self):
        self.check((Segment('image', {'url': 'http://img.test/a.png'}),), 'a url')

    def test_a_whole_message(self):
        self.check((Segment('text', {'text': '看'}), Segment('image', {'path': str(self.photo)}),
                    Segment('face', {'id': 14}), Segment('text', {'text': '这个'}),
                    Segment('record', {'path': str(self.voice)})), 'a whole message')


class NoFrameworkForSending(unittest.TestCase):
    """The OneBot messenger stands alone: it imports neither AstrBot nor aiohttp."""

    def test_the_source_imports_neither(self):
        source = (ROOT / 'adapter_onebot_messenger.py').read_text(encoding='utf-8')
        for n, line in enumerate(source.splitlines(), 1):
            words = line.strip()
            if words.startswith(('import ', 'from ')):
                for name in ('astrbot', 'aiohttp'):
                    self.assertNotIn(name, words.lower(), 'adapter_onebot_messenger.py:%d' % n)


if __name__ == '__main__':
    unittest.main()
