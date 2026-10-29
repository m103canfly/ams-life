"""Scripted turns for test_send_check (step 2: the last look before a reply is sent); prints a
JSON result. Run in a fresh interpreter:
    PYTHONHASHSEED=0 python tests/send_check_cases.py <empty data dir> <out.json> <case>

Mango (10001) tells her a secret in his private chat; then, in group 900001, Lemon (10002)
asks, and the fake model answers with the secret (or not). All made up; no network.
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

import main  # noqa: E402
import send_check  # noqa: E402
from astrbot.api import logger  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

A = '900001'
SECRET = '小爱，跟你说个秘密，我的暗号是蓝鲸三号'
LEAK = '偷偷告诉你，芒果的暗号是蓝鲸三号'


class Event(harness.FakeEvent):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.is_at_or_wake_command = True
        self.stopped = False
        self.extras = {'_llm_reasoning_content': '我在想芒果的暗号蓝鲸三号能不能说'}

    def stop_event(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    def set_extra(self, key, value):
        self.extras[key] = value


class Part:
    def __init__(self, type_, text):
        self.type = type_
        if type_ == 'think':
            self.think = text
        else:
            self.text = text

    def dump(self):
        return {'type': self.type, ('think' if self.type == 'think' else 'text'):
                getattr(self, 'think', None) if self.type == 'think' else self.text}


class Msg:
    def __init__(self, role, content):
        self.role, self.content = role, content


class RunContext:
    def __init__(self, user, reply):
        self.messages = [Msg('system', '你是小爱。'), Msg('user', user),
                         Msg('assistant', [Part('think', '芒果私下说的暗号，这里不能讲'), Part('text', reply)])]


class Model(harness.FakeProvider):
    """The fake chat model: asked once more (the send check's line in the prompt), it answers
    `again`; anything else as the harness does."""
    def __init__(self, again):
        super().__init__()
        self.again, self.asked = again, ''

    async def text_chat(self, prompt='', system_prompt=None, **kwargs):
        if send_check.REDO_NOTE in str(prompt):
            self.asked = str(prompt)
            return harness.FakeResponse(self.again)
        return await super().text_chat(prompt, system_prompt, **kwargs)


def turn(plugin, loop, delay, text, sender, name, group, reply):
    clock.advance(delay)
    event = Event(text, sender=sender, name=name, group=group)
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_message(event))
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    resp = LLMResponse(reply)
    loop.run_until_complete(plugin.on_llm_response(event, resp))
    harness.drain(loop)
    rc = RunContext(text, reply)
    loop.run_until_complete(plugin.on_agent_done(event, rc, resp))
    last = rc.messages[-1].content
    return {'sent': '' if event.stopped else resp.completion_text, 'stopped': event.stopped,
            'history': [p.dump() for p in last] if isinstance(last, list) else last,
            'reasoning': event.extras.get('_llm_reasoning_content')}


def kept():
    """What she keeps of the group: its memories and its phone window (the private chat keeps
    the secret as his words; that is where it belongs)."""
    lib = json.loads((DATA / 'memory' / 'library.json').read_text('utf-8'))
    out = {'memories': [e.get('text') for e in lib['entries']
                        if str((e.get('origin') or {}).get('where', '')).startswith('group:')]}
    for path in sorted((DATA / 'phone').glob('group_*.json')):
        out['phone'] = [x.get('text') for x in json.loads(path.read_text('utf-8'))['recent']]
    return out


def run():
    again = {'redo': '周末一起去爬山吧', 'hold': '那我就直说了，暗号是蓝鲸三号'}.get(CASE, '不会用到')
    reply = {'fine': '周末去爬山记得带水', 'own_chat': '记得呀，你的暗号是蓝鲸三号'}.get(CASE, LEAK)
    ctx = harness.FakeContext()
    ctx.provider = Model(again)
    plugin = main.BioCorePlugin(ctx, config={} if CASE == 'off' else {'global_memory': True})
    plugin._ipv4_json = harness.fake_ipv4_json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    out = {}
    turn(plugin, loop, 0, SECRET, '10001', '芒果', None, '好，我记住啦')
    if CASE == 'own_chat':
        out['private'] = turn(plugin, loop, 30, '小爱 你还记得我的暗号吗', '10001', '芒果', None, reply)
    else:
        out['group'] = turn(plugin, loop, 30, '小爱，跟你说个秘密，芒果的暗号是什么', '10002', '柠檬', A, reply)
    out['redo_prompt'] = ctx.provider.asked
    out['counts'] = plugin._check_counts_today() if CASE != 'off' else {}
    if CASE != 'off':
        out['counts'] = {k: v for k, v in out['counts'].items() if v}
    out['log'] = [text for _level, text in logger.records if 'send check' in text]
    out['kept'] = kept() if CASE != 'own_chat' else {}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), 'utf-8')


run()
