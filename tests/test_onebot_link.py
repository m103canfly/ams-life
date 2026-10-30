# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The OneBot 11 link without aiohttp: who may connect, what a frame is, and call/answer pairing.

Everything here is offline and made up (the token, the port, 10001, 20002). No socket is opened:
``Calls`` only needs an async ``send_frame``, so a small recorder stands in for the link.
"""
import ast
import asyncio
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from onebot_link import (CALL_SECONDS, MAX_FRAME_BYTES, Calls, check_handshake, kind_of,
                         parse_frame, self_id_of)  # noqa: E402

TOKEN = 'tok-2f7c1b'   # a made-up token
PORT = 6100            # a made-up port
PEER = '127.0.0.1'
HOST = PEER + ':' + str(PORT)
AUTH = 'Bearer ' + TOKEN
REASONS = ('no token', 'not local', 'host', 'origin', 'token', 'role')


def good(**changes):
    """The headers of an attempt that passes every check, with these changes; None drops a header."""
    out = {'Host': HOST, 'Authorization': AUTH}
    for name, value in changes.items():
        if value is None:
            out.pop(name, None)
        else:
            out[name] = value
    return out


class Handshake(unittest.TestCase):
    def check(self, headers, **kwargs):
        kwargs.setdefault('token', TOKEN)
        kwargs.setdefault('peer', PEER)
        kwargs.setdefault('port', PORT)
        return check_handshake(headers, **kwargs)

    def test_a_good_attempt_passes(self):
        self.assertEqual(self.check(good()), (True, ''))

    def test_no_token_configured(self):
        for token in ('', None):
            self.assertEqual(self.check(good(), token=token), (False, 'no token'))

    def test_peer_must_be_this_machine(self):
        for peer in ('127.0.0.1', '127.0.0.2', '::1', '::ffff:127.0.0.1'):
            self.assertEqual(self.check(good(), peer=peer), (True, ''), peer)
        for peer in ('192.168.1.5', '0.0.0.0', '10.0.0.2', 'abc', '', '::ffff:192.168.1.5', None):
            self.assertEqual(self.check(good(), peer=peer), (False, 'not local'), repr(peer))

    def test_host_must_be_one_of_three(self):
        for host in ('localhost:' + str(PORT), '[::1]:' + str(PORT)):
            self.assertEqual(self.check(good(Host=host)), (True, ''), host)
        for host in ('evil.test:' + str(PORT), '127.0.0.1:' + str(PORT + 1), '',
                     '127.0.0.1:' + str(PORT) + '/', '192.168.1.5:' + str(PORT), 'localhost', None):
            self.assertEqual(self.check(good(Host=host)), (False, 'host'), repr(host))

    def test_an_origin_header_is_refused(self):
        # a browser sends Origin; NapCat does not, so any Origin means something else is calling
        for origin in ('https://evil.test', 'null', ''):
            self.assertEqual(self.check(good(Origin=origin)), (False, 'origin'), repr(origin))

    def test_authorization(self):
        for value in ('Bearer ' + TOKEN, 'Token ' + TOKEN, 'bearer ' + TOKEN, 'token ' + TOKEN):
            self.assertEqual(self.check(good(Authorization=value)), (True, ''), value)
        for value in (None, '', TOKEN, 'Bearer ' + TOKEN + 'x', 'Bearer x' + TOKEN,
                      'Bearers ' + TOKEN, 'Basic ' + TOKEN, 'Bearer ' + TOKEN[:-1]):
            self.assertEqual(self.check(good(Authorization=value)), (False, 'token'), value)

    def test_a_token_in_the_url_is_not_read(self):
        # only the header counts; the query string is not even passed to the check
        self.assertEqual(self.check(good(Authorization=None)), (False, 'token'))
        self.assertNotEqual(self.check({'Host': HOST}), (True, ''))

    def test_client_role(self):
        for value in ('Universal', 'universal', 'UNIVERSAL'):
            self.assertEqual(self.check(good(**{'X-Client-Role': value})), (True, ''), value)
        for value in ('Client', 'universal x', '', 'Universal '):
            self.assertEqual(self.check(good(**{'X-Client-Role': value})), (False, 'role'), repr(value))

    def test_header_names_ignore_case(self):
        self.assertEqual(self.check({'hOsT': HOST, 'aUtHoRiZaTiOn': 'bEaReR ' + TOKEN}), (True, ''))
        self.assertEqual(self.check({'HOST': HOST, 'AUTHORIZATION': AUTH,
                                     'x-client-role': 'universal', 'x-self-id': '20002'}), (True, ''))
        self.assertEqual(self.check({'hOsT': 'evil.test:' + str(PORT), 'AUTHORIZATION': AUTH}),
                         (False, 'host'))

    def test_the_rules_are_checked_in_order(self):
        self.assertEqual(self.check(good(Host='evil.test:' + str(PORT)), token=''),
                         (False, 'no token'))
        self.assertEqual(self.check(good(Host='evil.test:' + str(PORT)), peer='192.168.1.5'),
                         (False, 'not local'))
        self.assertEqual(self.check(good(Host='evil.test:' + str(PORT), Origin='null')),
                         (False, 'host'))
        self.assertEqual(self.check(good(Origin='null', Authorization='Bearer wrong')),
                         (False, 'origin'))
        self.assertEqual(self.check(good(Authorization='Bearer wrong',
                                         **{'X-Client-Role': 'Client'})), (False, 'token'))
        self.assertEqual(self.check(good(**{'X-Client-Role': 'Client'})), (False, 'role'))

    def test_a_reason_never_carries_a_header_value(self):
        cases = [good(Origin='https://evil.test'), good(Host='evil.test:' + str(PORT)),
                 good(Authorization='Bearer ' + TOKEN[:-1]), good(Authorization=None),
                 good(**{'X-Client-Role': 'Client'})]
        for headers in cases:
            ok, reason = self.check(headers)
            self.assertFalse(ok)
            self.assertIn(reason, REASONS)
            self.assertNotIn(TOKEN, reason)
            self.assertNotIn(TOKEN.lower(), reason)
        ok, reason = self.check(good(), peer='192.168.1.5')
        self.assertFalse(ok)
        self.assertNotIn(TOKEN, reason)


class SelfId(unittest.TestCase):
    def test_digits(self):
        self.assertEqual(self_id_of({'X-Self-ID': '20002'}), '20002')
        self.assertEqual(self_id_of({'x-self-id': '10001'}), '10001')
        self.assertEqual(self_id_of({'X-Self-ID': 20002}), '20002')

    def test_anything_else_is_empty(self):
        for value in ('abc', '', '20002 ', '2 0002', '20002a', '-20002', None):
            self.assertEqual(self_id_of({'X-Self-ID': value}), '', repr(value))
        self.assertEqual(self_id_of({}), '')


class Frames(unittest.TestCase):
    def test_a_json_object(self):
        self.assertEqual(parse_frame('{"post_type": "message", "message_type": "group"}'),
                         {'post_type': 'message', 'message_type': 'group'})
        self.assertEqual(parse_frame('{"echo": "e", "retcode": 0}'), {'echo': 'e', 'retcode': 0})

    def test_bytes_are_read_as_utf8(self):
        self.assertEqual(parse_frame('{"a": "中文"}'.encode('utf-8')), {'a': '中文'})
        self.assertIsNone(parse_frame(b'\xff\xfe'))

    def test_not_an_object(self):
        for raw in ('[]', '[1, 2]', '42', '"text"', 'null', 'true', '', 'not json', '{', '{}extra'):
            self.assertIsNone(parse_frame(raw), raw)
        self.assertIsNone(parse_frame(None))

    def test_too_big(self):
        raw = '{"a": "' + 'x' * MAX_FRAME_BYTES + '"}'
        self.assertGreater(len(raw), MAX_FRAME_BYTES)
        self.assertIsNone(parse_frame(raw))
        self.assertIsNone(parse_frame(raw.encode('utf-8')))

    def test_a_frame_at_the_limit_is_still_read(self):
        raw = '{"a":"' + 'x' * (MAX_FRAME_BYTES - 8) + '"}'
        self.assertEqual(len(raw), MAX_FRAME_BYTES)
        self.assertEqual(parse_frame(raw)['a'][:1], 'x')

    def test_the_limits_are_the_specified_ones(self):
        self.assertEqual(MAX_FRAME_BYTES, 16 * 1024 * 1024)
        self.assertEqual(CALL_SECONDS, 30)


class Kinds(unittest.TestCase):
    def test_response(self):
        for frame in ({'echo': 'e', 'status': 'ok', 'retcode': 0},
                      {'echo': 'e', 'status': 'ok'}, {'echo': 'e', 'retcode': 0},
                      {'post_type': 'message', 'echo': 'e', 'status': 'ok'}):
            self.assertEqual(kind_of(frame), 'response', frame)

    def test_event(self):
        for frame in ({'post_type': 'message'}, {'post_type': 'meta_event', 'self_id': '20002'}):
            self.assertEqual(kind_of(frame), 'event', frame)

    def test_neither(self):
        for frame in ({}, {'echo': 'e'}, {'status': 'ok'}, {'retcode': 0}, 'text', None, []):
            self.assertEqual(kind_of(frame), '', repr(frame))


class Recorder:
    """An async send_frame: keeps every frame, answers nothing."""

    def __init__(self):
        self.frames = []

    async def __call__(self, frame):
        self.frames.append(frame)


class CallsTest(unittest.IsolatedAsyncioTestCase):
    async def sent(self, recorder, count):
        for _ in range(100):
            if len(recorder.frames) >= count:
                return
            await asyncio.sleep(0)
        self.fail('%d frame(s) were not sent' % count)

    async def test_one_call_gets_its_whole_answer(self):
        recorder = Recorder()
        calls = Calls(recorder, seconds=5)
        params = {'message_id': 'm-1'}
        task = asyncio.create_task(calls.call('get_msg', params))
        await self.sent(recorder, 1)
        frame = recorder.frames[0]
        self.assertEqual(frame['action'], 'get_msg')
        self.assertEqual(frame['params'], {'message_id': 'm-1'})
        self.assertIsNot(frame['params'], params)
        echo = frame['echo']
        self.assertEqual(len(echo), 16)
        int(echo, 16)   # secrets.token_hex(8): hex digits only
        answer = {'status': 'ok', 'retcode': 0, 'data': {'message_id': 'm-1'}, 'echo': echo}
        self.assertTrue(calls.settle(answer))
        self.assertEqual(await task, answer)
        self.assertFalse(calls.settle(answer))   # the same answer a second time is nobody's

    async def test_two_calls_get_their_own_answers(self):
        recorder = Recorder()
        calls = Calls(recorder, seconds=5)
        first = asyncio.create_task(calls.call('get_msg', {'id': 1}))
        await self.sent(recorder, 1)
        second = asyncio.create_task(calls.call('get_msg', {'id': 2}))
        await self.sent(recorder, 2)
        echo_one, echo_two = recorder.frames[0]['echo'], recorder.frames[1]['echo']
        self.assertNotEqual(echo_one, echo_two)
        # the second answer comes back first, and each call still gets its own
        self.assertTrue(calls.settle({'status': 'ok', 'retcode': 0, 'data': {'id': 2},
                                      'echo': echo_two}))
        self.assertTrue(calls.settle({'status': 'ok', 'retcode': 0, 'data': {'id': 1},
                                      'echo': echo_one}))
        self.assertEqual((await first)['data'], {'id': 1})
        self.assertEqual((await second)['data'], {'id': 2})

    async def test_a_timeout_leaves_nothing_behind(self):
        recorder = Recorder()
        calls = Calls(recorder, seconds=0.01)
        with self.assertRaises(asyncio.TimeoutError):
            await calls.call('get_msg', {'id': 1})
        late = {'status': 'ok', 'retcode': 0, 'data': {'id': 1},
                'echo': recorder.frames[0]['echo']}
        self.assertFalse(calls.settle(late))

    async def test_close_fails_the_calls_that_are_waiting(self):
        recorder = Recorder()
        calls = Calls(recorder, seconds=5)
        task = asyncio.create_task(calls.call('get_msg', {'id': 1}))
        await self.sent(recorder, 1)
        calls.close()
        with self.assertRaises(ConnectionError):
            await task
        self.assertFalse(calls.settle({'status': 'ok', 'retcode': 0,
                                       'echo': recorder.frames[0]['echo']}))

    async def test_close_before_a_call(self):
        calls = Calls(Recorder(), seconds=5)
        calls.close()
        with self.assertRaises(ConnectionError):
            await calls.call('get_msg', {})

    async def test_an_unwanted_echo_is_left_alone(self):
        calls = Calls(Recorder(), seconds=5)
        for frame in ({'status': 'ok', 'retcode': 0, 'echo': 'ff' * 8},
                      {'status': 'ok', 'retcode': 0}, {'echo': None}, {'echo': ['a']}):
            self.assertFalse(calls.settle(frame), frame)
        self.assertFalse(calls.settle('not a frame'))
        self.assertFalse(calls.settle(None))

    async def test_a_failed_send_raises_as_it_is(self):
        frames = []

        async def send(frame):
            frames.append(frame)
            raise OSError('link down')

        calls = Calls(send, seconds=5)
        with self.assertRaises(OSError) as caught:
            await calls.call('get_msg', {'id': 1})
        self.assertEqual(str(caught.exception), 'link down')
        self.assertFalse(calls.settle({'status': 'ok', 'retcode': 0, 'echo': frames[0]['echo']}))


class Standalone(unittest.TestCase):
    """The new module stands alone: it imports no AstrBot and no aiohttp."""

    def test_no_framework_import(self):
        source = (ROOT / 'onebot_link.py').read_text('utf-8')
        tree = ast.parse(source)
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names.add(node.module.split('.')[0])
        self.assertNotIn('aiohttp', names)
        self.assertNotIn('astrbot', names)
        self.assertIn('asyncio', names)


if __name__ == '__main__':
    unittest.main()
