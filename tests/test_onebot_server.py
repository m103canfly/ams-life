# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""A local fake OneBot client exercises the server when aiohttp is installed."""
import ast
import asyncio
import unittest
from pathlib import Path

try:
    import aiohttp
except ImportError:
    aiohttp = None

if aiohttp is not None:
    import onebot_link
    from adapter_onebot_messenger import OneBotMessenger
    from events import Segment
    from onebot_server import OneBotServer


@unittest.skipUnless(aiohttp is not None, 'aiohttp is not installed')
class ServerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.events = []
        self.arrived = asyncio.Event()

        async def on_event(frame):
            self.events.append(frame)
            self.arrived.set()
            if frame.get('fail'):
                raise ValueError('private event data')

        self.server = OneBotServer(token='fake-secret', on_event=on_event, port=0, call_seconds=0.1)
        self.port = await self.server.start()
        self.url = 'http://127.0.0.1:%d' % self.port
        self.session = aiohttp.ClientSession()
        self.headers = {'Authorization': 'Bearer fake-secret', 'X-Self-ID': '20002'}

    async def asyncTearDown(self):
        await self.session.close()
        await self.server.stop()

    async def connect(self):
        ws = await self.session.ws_connect(self.url + '/ws', headers=self.headers)
        for _ in range(100):
            if self.server.connected:
                return ws
            await asyncio.sleep(0.001)
        self.fail('connection was not registered')

    async def test_constructor(self):
        for kwargs in ({'host': '0.0.0.0'}, {'token': ''}):
            options = {'token': 'fake-secret', 'on_event': self.events.append}
            options.update(kwargs)
            with self.assertRaises(ValueError):
                OneBotServer(**options)

    async def test_handshake_and_private_logging(self):
        with self.assertLogs('onebot_server', level='INFO') as logs:
            for headers in ({'Authorization': 'Bearer wrong'}, {},
                            {**self.headers, 'Origin': 'null'},
                            {**self.headers, 'Host': 'invalid.test'}):
                with self.assertRaises(aiohttp.WSServerHandshakeError) as error:
                    await self.session.ws_connect(self.url + '/ws', headers=headers)
                self.assertEqual(error.exception.status, 401)
                self.assertFalse(self.server.connected)
            ws = await self.connect()
            self.assertEqual(self.server.self_id, '20002')
            await ws.close()
        self.assertNotIn('fake-secret', '\n'.join(logs.output))
        self.assertNotIn('wrong', '\n'.join(logs.output))

    async def test_other_path(self):
        async with self.session.get(self.url + '/other') as response:
            self.assertEqual(response.status, 404)
            self.assertFalse(any(key.lower().startswith('access-control-allow-') for key in response.headers))

    async def test_events_and_bad_frames(self):
        ws = await self.connect()
        event = {'post_type': 'message', 'text': 'example'}
        await ws.send_json(event)
        await asyncio.wait_for(self.arrived.wait(), 1)
        self.assertEqual(self.events, [event])
        self.arrived.clear()
        await ws.send_json({'post_type': 'meta_event'})
        await ws.send_str('{')
        await ws.send_bytes(b'{}')
        await ws.send_json({'post_type': 'message', 'fail': True})
        await asyncio.wait_for(self.arrived.wait(), 1)
        self.assertEqual(len(self.events), 2)
        self.arrived.clear()
        await ws.send_json(event)
        await asyncio.wait_for(self.arrived.wait(), 1)
        self.assertEqual(self.events, [event, {'post_type': 'message', 'fail': True}, event])
        self.assertTrue(self.server.connected)

    async def test_calls_and_timeout(self):
        ws = await self.connect()
        first = asyncio.create_task(self.server.call_api('get_msg', {'id': 1}))
        one = await ws.receive_json()
        self.assertEqual((one['action'], one['params']), ('get_msg', {'id': 1}))
        second = asyncio.create_task(self.server.call_api('get_msg', {'id': 2}))
        two = await ws.receive_json()
        for request in (two, one):
            await ws.send_json({'status': 'ok', 'data': request['params'], 'echo': request['echo']})
        self.assertEqual((await first)['data'], {'id': 1})
        self.assertEqual((await second)['data'], {'id': 2})
        with self.assertRaises(TimeoutError):
            await self.server.call_api('get_msg', {})

    async def test_disconnect_fails_calls(self):
        with self.assertRaises(ConnectionError):
            await self.server.call_api('get_msg', {})
        ws = await self.connect()
        task = asyncio.create_task(self.server.call_api('get_msg', {}))
        await ws.receive_json()
        await ws.close()
        with self.assertRaises(ConnectionError):
            await asyncio.wait_for(task, 1)
        self.assertFalse(self.server.connected)
        self.assertEqual(self.server.self_id, '')

    async def test_replacement_closes_old_connection(self):
        first = await asyncio.wait_for(self.connect(), timeout=5)
        task = asyncio.create_task(self.server.call_api('get_msg', {}))
        await asyncio.wait_for(first.receive_json(), timeout=5)
        second = await asyncio.wait_for(self.connect(), timeout=5)
        with self.assertRaises(ConnectionError):
            await asyncio.wait_for(task, timeout=5)
        closed = await asyncio.wait_for(first.receive(), timeout=5)
        self.assertIn(closed.type, (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED))
        call = asyncio.create_task(self.server.call_api('get_msg', {}))
        frame = await asyncio.wait_for(second.receive_json(), timeout=5)
        answer = {'status': 'ok', 'echo': frame['echo']}
        await asyncio.wait_for(second.send_json(answer), timeout=5)
        self.assertEqual(await asyncio.wait_for(call, timeout=5), answer)

    async def test_messenger(self):
        ws = await self.connect()
        messenger = self.server.messenger(())
        self.assertIsInstance(messenger, OneBotMessenger)
        send = asyncio.create_task(messenger.send('group:900001', (Segment('text', {'text': 'hello'}),)))
        frame = await ws.receive_json()
        self.assertEqual(frame['action'], 'send_group_msg')
        self.assertEqual(frame['params']['group_id'], 900001)
        await ws.send_json({'status': 'ok', 'data': {'message_id': 1}, 'echo': frame['echo']})
        sent = await send
        self.assertTrue(sent.ok)
        self.assertEqual(sent.message_id, '1')

    async def test_settle_done_future(self):
        calls = onebot_link.Calls(None)
        future = asyncio.get_running_loop().create_future()
        future.set_result(None)
        calls._waiting['done'] = future
        self.assertFalse(calls.settle({'echo': 'done'}))

    async def test_stop_cancels_event_tasks_and_closes_port(self):
        started = asyncio.Event()
        finished = asyncio.Event()

        async def slow(frame):
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                finished.set()

        self.server.on_event = slow
        ws = await self.connect()
        await ws.send_json({'post_type': 'message'})
        await asyncio.wait_for(started.wait(), 1)
        await self.server.stop()
        self.assertTrue(finished.is_set())
        self.assertFalse(self.server.connected)
        with self.assertRaises(aiohttp.ClientConnectorError):
            await self.session.get(self.url + '/ws')

    async def test_source_imports_and_binding(self):
        source = (Path(__file__).resolve().parent.parent / 'onebot_server.py').read_text('utf-8')
        tree = ast.parse(source)
        imports = [alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names]
        imports += [node.module or '' for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        self.assertFalse(any(name.startswith('astrbot') for name in imports))
        sites = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Attribute) and node.func.attr == 'TCPSite']
        self.assertEqual(len(sites), 1)
        self.assertTrue(any(isinstance(node, ast.Attribute) and node.attr == 'host'
                            and isinstance(node.value, ast.Name) and node.value.id == 'self'
                            for node in ast.walk(sites[0])))


if __name__ == '__main__':
    unittest.main()
