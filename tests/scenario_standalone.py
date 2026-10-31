# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Run the golden conversation through the standalone turn runner."""
import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402
from golden_script import GROUP_A, GROUP_B, SCRIPT, FULL_CONFIG, files_snapshot  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('data', type=Path)
parser.add_argument('out', type=Path)
parser.add_argument('mode', nargs='?', choices=('basic', 'full'), default='basic')
parser.add_argument('--path', choices=('astrbot', 'nohistory', 'standalone'), default='standalone')
parser.add_argument('--dump-each-turn', type=Path, help='copy window and event state after each scripted turn')
args = parser.parse_args()
DATA, OUT, MODE = args.data, args.out, args.mode
if args.dump_each_turn is not None:
    dump_path = args.dump_each_turn.resolve()
    data_path = DATA.resolve()
    if dump_path == data_path or data_path in dump_path.parents or dump_path in data_path.parents:
        parser.error('dump directory and data directory must not contain each other')
    if dump_path.exists() and (not dump_path.is_dir() or any(dump_path.iterdir())):
        parser.error('dump directory must be empty')
# aiohttp creates a Random at import; keep every path's harness seed sequence aligned.
sys.path.insert(0, str(HERE.parent))
try:
    import panel_api  # noqa: E402,F401
finally:
    del sys.path[0]
clock = harness.prepare(DATA)

import adapter_onebot  # noqa: E402
import attention  # noqa: E402
import messenger  # noqa: E402
import mixin_attention  # noqa: E402
import model_client  # noqa: E402
import turn  # noqa: E402
import turn_runner  # noqa: E402
from common import LLM_FUNCTIONS  # noqa: E402
from astrbot.api import logger  # noqa: E402


class FakeModel(model_client.ModelClient):
    def __init__(self):
        self.provider = harness.FakeProvider()
        self.reply = None
        self.index = None
        self.asked_uncalled = []

    async def chat(self, *, prompt=None, system=None, messages=None, images=None, tools=None):
        if messages is not None and prompt is None:
            # A real reply waits on the network while the request's background work runs.
            current = asyncio.current_task()
            for _ in range(20):
                pending = [task for task in asyncio.all_tasks()
                           if task is not current and not task.done()
                           and getattr(task.get_coro(), '__name__', '') not in harness.FOREVER]
                if not pending:
                    break
                await asyncio.gather(*pending, return_exceptions=True)
            if self.reply is None:
                self.asked_uncalled.append(self.index)
                text = ''
            else:
                text = self.reply
        elif prompt is not None and messages is None:
            text = (await self.provider.text_chat(prompt=prompt, system_prompt=system)).completion_text
        else:
            raise ValueError('cannot distinguish model calls')
        return model_client.ModelReply(text=text, tool_calls=(), usage={}, reasoning='')


class FakeMessenger(messenger.Messenger):
    def __init__(self):
        self.sent = []

    async def send(self, place, segments):
        self.sent.append([place, [{'type': part.type, 'data': part.data} for part in segments]])
        return messenger.Sent(True, 'made-up')


def dump_turn(index, her, provider):
    """Copy the persisted inputs and record the in-memory archive gates after drain."""
    if args.dump_each_turn is None:
        return
    target = args.dump_each_turn / str(index)
    target.mkdir(parents=True, exist_ok=False)
    for name in ('sessions', 'phone', 'archives'):
        source = DATA / name
        if source.is_dir():
            shutil.copytree(source, target / name)
    for name in ('states/spend.json', 'brain_turns.json'):
        source = DATA / name
        if source.is_file():
            destination = target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    meta = {'script_index': index, 'clock': clock(),
            'last_strong_event_summary': getattr(her, '_last_strong_event_summary', None),
            'last_event_archive': getattr(her, '_last_event_archive', None),
            'provider_prompts': list(provider.prompts)}
    (target / 'diagnostic.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True), 'utf-8')


def main_run():
    if args.path == 'astrbot':
        return astrbot_run()
    import panel_api
    from her import Her
    from history_store import HistoryStore

    (DATA / 'api_config.json').write_text(json.dumps({'embedding': {
        'source': 'custom', 'base_url': 'http://embed.test/v1', 'model': 'fake-embed', 'api_key': ''}}), 'utf-8')
    config = dict(FULL_CONFIG) if MODE == 'full' else {}
    config.update(owner_qq='10001', reply_groups=[GROUP_A, GROUP_B])
    collector = panel_api.RouteCollector()
    her = Her(collector, config)
    her.self_decide = True
    her._ipv4_json = harness.fake_ipv4_json
    her._neutral_persona = '你是小爱。'
    her._neutral_model = model = FakeModel()
    her._neutral_messenger = sends = FakeMessenger()
    history = HistoryStore(DATA / 'history.sqlite3', gate=her._history_gate) if args.path == 'standalone' else None
    her._history = history
    if MODE == 'full':
        her.llm_functions = {k: {'enabled': True, 'provider': 'follow_llm'} for k in LLM_FUNCTIONS}
    mixin_attention.WAIT_SECONDS.update({key: 0 for key in mixin_attention.WAIT_SECONDS})
    attention.typing_seconds = lambda text: 0
    trace = {'routes': [route for route, handler, methods, desc in collector.routes], 'turns': []}
    prepare, after = her._prepare_turn, her._after_reply
    current = {}

    async def record_prepare(event, request):
        await prepare(event, request)
        current.update(session=her._here(event),
                       inject=[p.get('text') if isinstance(p, dict) else str(p)
                               for p in request.extra_user_content_parts], system=request.system_prompt)

    async def record_after(event, reply):
        await after(event, reply)
        current['clean'] = reply.text
        trace['turns'].append(dict(current))

    her._prepare_turn, her._after_reply = record_prepare, record_after
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for index, (delay, ev, reply) in enumerate(SCRIPT):
        clock.advance(delay)
        model.index, model.reply = index, reply
        parts = [{'type': 'text', 'data': {'text': ev['text']}}]
        if reply is not None:
            parts.insert(0, {'type': 'at', 'data': {'qq': '20002'}})
        frame = {'post_type': 'message', 'message_type': 'group' if ev.get('group') else 'private',
                 'self_id': '20002', 'user_id': ev['sender'], 'group_id': ev.get('group', ''),
                 'message_id': 'm' + ev['text'][:6], 'time': clock(),
                 'sender': {'user_id': ev['sender'], 'nickname': ev['name']}, 'message': parts}
        event = turn.TurnEvent(adapter_onebot.from_onebot(frame))
        current.clear()
        loop.run_until_complete(turn_runner.run_turn(her, event, history_limit=20))
        harness.drain(loop)
        dump_turn(index, her, model.provider)
    if MODE == 'full':
        ticks = []
        for _ in range(3):
            clock.advance(300)
            try:
                loop.run_until_complete(her._autonomy_tick())
                ticks.append('ok')
            except Exception as exc:
                ticks.append('error: ' + type(exc).__name__)
            harness.drain(loop)
        trace['autonomy_ticks'] = ticks
    clock.advance(3600)
    try:
        trace['page_status'] = loop.run_until_complete(her.page_status())
    except Exception as exc:
        trace['page_status'] = 'error: ' + type(exc).__name__
    harness.drain(loop)
    for task in asyncio.all_tasks(loop):
        task.cancel()
    trace['provider_prompts'] = model.provider.prompts
    trace['log'] = [r for r in logger.records if r[0] in ('warning', 'error')]
    trace['sent'], trace['asked_uncalled'] = sends.sent, model.asked_uncalled
    if history is not None:
        history.close()
    trace['files'] = files_snapshot(DATA)
    OUT.write_text(json.dumps(trace, ensure_ascii=False, indent=1, sort_keys=True, default=str), 'utf-8')


def astrbot_run():
    import main
    from astrbot.api.message_components import At
    from astrbot.api.provider import ProviderRequest, LLMResponse

    class CalledEvent(harness.FakeEvent):
        def get_messages(self):
            parts = super().get_messages()
            if self.is_at_or_wake_command:
                parts.insert(0, At(qq=self.message_obj.self_id))
            return parts

    ctx = harness.FakeContext()
    config = dict(FULL_CONFIG) if MODE == 'full' else {}
    config.update(owner_qq='10001', reply_groups=[GROUP_A, GROUP_B])
    plugin = main.BioCorePlugin(ctx, config=config)
    plugin.self_decide = True
    plugin._ipv4_json = harness.fake_ipv4_json
    if MODE == 'full':
        plugin.llm_functions = {k: {'enabled': True, 'provider': 'follow_llm'} for k in LLM_FUNCTIONS}
    mixin_attention.WAIT_SECONDS.update({key: 0 for key in mixin_attention.WAIT_SECONDS})
    attention.typing_seconds = lambda text: 0
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    trace = {'routes': list(ctx.web_routes), 'turns': [], 'sent': [], 'asked_uncalled': []}

    async def decide(event):
        return [request async for request in plugin.on_message_decide(event)]

    for index, (delay, ev, reply) in enumerate(SCRIPT):
        clock.advance(delay)
        event = CalledEvent(**ev)
        event.is_at_or_wake_command = reply is not None
        event.request_llm = lambda **kwargs: kwargs
        loop.run_until_complete(plugin.on_message(event))
        harness.drain(loop)
        if event.stopped:
            dump_turn(index, plugin, ctx.provider)
            continue
        requests = loop.run_until_complete(decide(event))
        harness.drain(loop)
        if reply is None:
            if requests:
                trace['asked_uncalled'].append(index)
            dump_turn(index, plugin, ctx.provider)
            continue
        if event.stopped:
            dump_turn(index, plugin, ctx.provider)
            continue
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        resp = LLMResponse(reply)
        loop.run_until_complete(plugin.on_llm_response(event, resp))
        harness.drain(loop)
        dump_turn(index, plugin, ctx.provider)
        trace['turns'].append({'session': event.unified_msg_origin,
                               'inject': [p.get('text') if isinstance(p, dict) else str(p)
                                          for p in req.extra_user_content_parts],
                               'system': req.system_prompt, 'clean': resp.completion_text})
    if MODE == 'full':
        ticks = []
        for _ in range(3):
            clock.advance(300)
            try:
                loop.run_until_complete(plugin._autonomy_tick())
                ticks.append('ok')
            except Exception as exc:
                ticks.append('error: ' + type(exc).__name__)
            harness.drain(loop)
        trace['autonomy_ticks'] = ticks
    clock.advance(3600)
    try:
        trace['page_status'] = loop.run_until_complete(plugin.page_status())
    except Exception as exc:
        trace['page_status'] = 'error: ' + type(exc).__name__
    harness.drain(loop)
    for task in asyncio.all_tasks(loop):
        task.cancel()
    trace['provider_prompts'] = ctx.provider.prompts
    trace['log'] = [r for r in logger.records if r[0] in ('warning', 'error')]
    trace['files'] = files_snapshot(DATA)
    OUT.write_text(json.dumps(trace, ensure_ascii=False, indent=1, sort_keys=True, default=str), 'utf-8')


main_run()
