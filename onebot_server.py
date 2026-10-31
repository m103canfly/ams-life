# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""A local reverse WebSocket server for a single OneBot connection."""
import asyncio
import logging

from aiohttp import WSMsgType, web

try:
    from . import onebot_link, adapter_onebot_messenger
except ImportError:
    import onebot_link
    import adapter_onebot_messenger

EVENT_TYPES = ("message", "message_sent", "notice", "request")
logger = logging.getLogger(__name__)


class OneBotServer:
    def __init__(self, *, token, on_event, port=6199, host="127.0.0.1", path="/ws",
                 call_seconds=onebot_link.CALL_SECONDS):
        if host not in ("127.0.0.1", "::1") or not token:
            raise ValueError("a loopback host and a token are required")
        self.token, self.on_event = token, on_event
        self.port, self.host, self.path = port, host, path
        self.call_seconds = call_seconds
        self._runner = None
        self._ws = None
        self._calls = None
        self._self_id = ""
        self._events = set()
        self._lock = asyncio.Lock()
        self._stopping = False
        self.bad_frames = 0

    async def start(self) -> int:
        app = web.Application()
        app.router.add_get(self.path, self._handle, allow_head=False)
        runner = web.AppRunner(app, access_log=None)
        await runner.setup()
        try:
            site = web.TCPSite(runner, host=self.host, port=self.port)
            await site.start()
        except BaseException:
            await runner.cleanup()
            raise
        self._runner = runner
        self.port = runner.addresses[0][1]
        self._stopping = False
        return self.port

    @property
    def connected(self) -> bool:
        return self._ws is not None and not self._ws.closed

    @property
    def self_id(self) -> str:
        return self._self_id if self.connected else ""

    async def _handle(self, request):
        ok, reason = onebot_link.check_handshake(request.headers, token=self.token,
                                                  peer=request.remote, port=self.port)
        if not ok:
            logger.info("handshake refused: %s", reason)
            return web.Response(status=401, text="unauthorized")
        ws = web.WebSocketResponse(max_msg_size=onebot_link.MAX_FRAME_BYTES, heartbeat=30)
        async with self._lock:
            if self._stopping:
                return web.Response(status=503)
            if self._calls is not None:
                self._calls.close()
            if self._ws is not None:
                await self._ws.close()
            await ws.prepare(request)
            calls = onebot_link.Calls(ws.send_json, seconds=self.call_seconds)
            self._ws, self._calls = ws, calls
            self._self_id = onebot_link.self_id_of(request.headers)
            logger.info("connected")
        try:
            async for msg in ws:
                if msg.type != WSMsgType.TEXT:
                    continue
                frame = onebot_link.parse_frame(msg.data)
                if frame is None:
                    self.bad_frames += 1
                    logger.info("unreadable frame")
                elif onebot_link.kind_of(frame) == "response":
                    calls.settle(frame)
                elif onebot_link.kind_of(frame) == "event" and frame.get("post_type") in EVENT_TYPES:
                    task = asyncio.create_task(self._deliver(frame))
                    self._events.add(task)
                    task.add_done_callback(self._events.discard)
        finally:
            calls.close()
            if self._ws is ws:
                self._ws, self._calls, self._self_id = None, None, ""
            logger.info("disconnected")
        return ws

    async def _deliver(self, frame):
        try:
            await self.on_event(frame)
        except Exception as error:
            logger.error("on_event error: %s", type(error).__name__)

    async def call_api(self, action, params) -> dict:
        calls = self._calls
        if not self.connected or calls is None:
            raise ConnectionError("the link is closed")
        return await calls.call(action, params)

    def messenger(self, roots):
        return adapter_onebot_messenger.OneBotMessenger(self.call_api, roots=roots)

    async def stop(self) -> None:
        async with self._lock:
            self._stopping = True
            if self._calls is not None:
                self._calls.close()
            if self._ws is not None:
                await self._ws.close()
            self._ws, self._calls, self._self_id = None, None, ""
        if self._runner is not None:
            runner, self._runner = self._runner, None
            await runner.cleanup()
        tasks = tuple(self._events)
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
