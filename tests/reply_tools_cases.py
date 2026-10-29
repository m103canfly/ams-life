"""Scripted runs for the reply-tools tests; prints a JSON result.

Run in a fresh interpreter (test_reply_tools does this):
    PYTHONHASHSEED=0 python tests/reply_tools_cases.py <empty data dir> <out.json> <case>

All numbers, names and messages are made up. No network, no model, no messages sent.
"""
import asyncio
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA, OUT, CASE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
clock = harness.prepare(DATA)
G1 = '900001'

import main  # noqa: E402
from astrbot.api.provider import ProviderRequest  # noqa: E402


class Tool:
    def __init__(self, name):
        self.name = name


class ToolSet:
    """What AstrBot hands over in req.func_tool (core/agent/tool.py): its tools, names(),
    remove_tool(); empty is false."""

    def __init__(self, names):
        self.tools = [Tool(n) for n in names]

    def names(self):
        return [t.name for t in self.tools]

    def remove_tool(self, name):
        self.tools = [t for t in self.tools if t.name != name]

    def __bool__(self):
        return bool(self.tools)


config = {'allowed_tools': ['web_search_deepseek']} if CASE in ('allowed', 'broken') else {}
if CASE == 'plugin_off':
    config = {'enabled': False}
plugin = main.BioCorePlugin(harness.FakeContext(), config=config)
plugin._ipv4_json = harness.fake_ipv4_json
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

logged = []
real_info = main.logger.info
main.logger.info = lambda msg, *a, **k: logged.append(str(msg) % a if a else str(msg)) or real_info(msg, *a, **k)


def ask(tools, text='小爱 你好'):
    clock.advance(60)
    event = harness.FakeEvent(text, sender='10002', name='柠檬', group=G1)
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    if tools is not None:
        req.func_tool = tools
    loop.run_until_complete(plugin.on_message(event))
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    left = getattr(req, 'func_tool', 'unset')
    return None if left is None else 'unset' if left == 'unset' else left.names()


class Broken(ToolSet):
    """A tool set that fails while tools are taken out of it."""

    def remove_tool(self, name):
        raise RuntimeError('made-up failure')


if CASE == 'broken':
    result = {'broken': ask(Broken(['future_task', 'web_search_deepseek']))}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), 'utf-8')
    raise SystemExit(0)

result = {
    'three': ask(ToolSet(['future_task', 'send_message_to_user', 'web_search_deepseek'])),
    'empty': ask(ToolSet([])),
    'none': ask(None),
    'logged': [x for x in logged if 'tools taken out' in x],
}
for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), 'utf-8')
