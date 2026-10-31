"""A scripted conversation driven through the plugin's hooks; prints a JSON trace of everything observable.

Run in a fresh interpreter with a fixed hash seed (the golden test does this):
    PYTHONHASHSEED=0 python3 tests/scenario.py <empty data dir> <trace.json> [basic|full]

basic = default config. full = every optional LLM function on, safety on, autonomy on with a fixed noise seed,
so the proposal-only paths and the private autonomy bookkeeping run too.
"""
import asyncio
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA, OUT = Path(sys.argv[1]), Path(sys.argv[2])
MODE = sys.argv[3] if len(sys.argv) > 3 else 'basic'
clock = harness.prepare(DATA)

import main  # noqa: E402
from astrbot.api import logger  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

from golden_script import GROUP_A, GROUP_B, TAG_JOY, TAG_SAD, SCRIPT, FULL_CONFIG, sqlite_snapshot, files_snapshot


def main_run():
    ctx = harness.FakeContext()
    config = dict(FULL_CONFIG) if MODE == 'full' else {}
    config.update(owner_qq='10001', reply_groups=[GROUP_A, GROUP_B])
    plugin = main.BioCorePlugin(ctx, config=config)
    plugin._ipv4_json = harness.fake_ipv4_json
    if MODE == 'full':
        plugin.llm_functions = {k: {'enabled': True, 'provider': 'follow_llm'} for k in main.LLM_FUNCTIONS}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    trace = {'routes': list(ctx.web_routes), 'turns': []}
    for delay, ev, reply in SCRIPT:
        clock.advance(delay)
        event = harness.FakeEvent(**ev)
        event.is_at_or_wake_command = reply is not None  # the scripted replies are to messages that wake her
        loop.run_until_complete(plugin.on_message(event))  # AstrBot calls it for every message
        harness.drain(loop)
        if reply is None:
            continue
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        resp = LLMResponse(reply)
        loop.run_until_complete(plugin.on_llm_response(event, resp))
        harness.drain(loop)
        trace['turns'].append({
            'session': event.unified_msg_origin,
            'inject': [p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts],
            'system': req.system_prompt,
            'clean': resp.completion_text,
        })
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
    except Exception as exc:  # recorded, not raised: the trace shows it either way
        trace['page_status'] = 'error: ' + type(exc).__name__
    harness.drain(loop)
    for task in asyncio.all_tasks(loop):
        task.cancel()
    trace['provider_prompts'] = ctx.provider.prompts
    trace['log'] = [r for r in logger.records if r[0] in ('warning', 'error')]
    trace['files'] = files_snapshot(DATA)
    OUT.write_text(json.dumps(trace, ensure_ascii=False, indent=1, sort_keys=True, default=str), 'utf-8')


main_run()
