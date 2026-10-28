"""Scripted runs for the daily digest wiring tests; prints a JSON result.

Run in a fresh interpreter (test_digest does this):
    PYTHONHASHSEED=0 python tests/digest_cases.py <empty data dir> <out.json> <case>

All numbers, names and messages are made up. No network, no model (a fake one), no messages sent.
"""
import asyncio
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA, OUT, CASE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
clock = harness.prepare(DATA)
G1, G2 = '900001', '900002'
EVENING = time.mktime(time.strptime('2026-10-04 20:00:00', '%Y-%m-%d %H:%M:%S'))
LATE = EVENING + 3 * 3600 + 10 * 60   # 23:10
clock.now = EVENING

import forget_registry  # noqa: E402
import main  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402


class Model(harness.FakeProvider):
    """Answers the digest prompt (group and private); keeps every digest prompt."""
    digests = []

    async def text_chat(self, prompt='', system_prompt=None, **kwargs):
        p = str(prompt)
        if '今天在这里发生的几件事' in p:
            Model.digests.append(p)
            if '一个私聊' in p:
                return harness.FakeResponse(json.dumps({'events': [
                    {'title': 'P1说了蓝莓计划', 'what': 'P1跟她说起蓝莓计划的安排', 'who': ['P1'], 'lines': [1, 2]}]},
                    ensure_ascii=False))
            return harness.FakeResponse(json.dumps({'events': [
                # P1 is 柠檬 (spoke first), P2 芒果; Q codes are people only mentioned
                {'title': 'P1约周末打副本', 'what': 'P1约大家周末一起打副本，P2说要来', 'who': ['P1', 'P2'],
                 'lines': [1, 2]},
                {'title': '有人在聊抽卡', 'what': '几个人在聊今天抽卡的运气', 'who': ['P1']},       # no lines
                {'title': 'P2说了件事', 'what': 'P2讲了一件事', 'who': ['P9'], 'lines': [99]},      # wrong code, line
                {'title': 'P7的事', 'what': 'P7出了点事', 'who': ['P1'], 'lines': [1]},           # unknown code in text
                {'title': '号码', 'what': 'P1报了号码123456', 'who': ['P1'], 'lines': [1]},       # a long number
            ]}, ensure_ascii=False))
        return await super().text_chat(prompt=prompt, system_prompt=system_prompt, **kwargs)


def new_plugin():
    ctx = harness.FakeContext()
    ctx.provider = Model()
    plugin = main.BioCorePlugin(ctx, config={})
    plugin._ipv4_json = harness.fake_ipv4_json
    return plugin


plugin = new_plugin()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def turn(text, sender, name, group=None, reply=None, advance=60, msg_id=None):
    clock.advance(advance)
    event = harness.FakeEvent(text, sender=sender, name=name, group=group)
    event.message_obj.message_id = msg_id or ('m-%s-%d' % (sender, int(clock.now)))
    loop.run_until_complete(plugin.on_message(event))
    harness.drain(loop)
    if reply is not None:
        req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
        harness.drain(loop)


def events():
    return [e for e in plugin._event_archive(100, read_only=True) if e.get('kind') == 'daily_digest']


def chat():
    turn('周末一起打副本吗', '10002', '柠檬', group=G1, msg_id='g1')
    turn('我来我来 @柠檬', '10001', '芒果', group=G1, msg_id='g2')
    turn('今天抽卡又歪了', '10002', '柠檬', group=G1, msg_id='g3')
    turn('阿星今天没来', '10001', '芒果', group=G1, msg_id='g4')
    turn('我的手机号是13812345678', '10001', '芒果', group=G1, msg_id='g5')
    turn('我是阿星，我家的猫叫团子', '10003', '阿星', group=G1, msg_id='g6')
    turn('我跟你说个秘密 我在弄蓝莓计划', '10004', '桃子', reply='好呀', msg_id='p1')
    turn('蓝莓计划下周开始', '10004', '桃子', msg_id='p2')


result = {}
if CASE == 'nightly':
    chat()
    # after the lines are in her phone: one person and one message ruled out (as a restored
    # backup or an imported registry would have them, without anything deleted yet)
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')
        reg.forget_message('g5', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')
    result['off'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE))
    result['calls_off'] = len(Model.digests)
    plugin.llm_functions = dict(plugin.llm_functions or {}, daily_digest={'enabled': True, 'provider': 'follow_llm'})
    result['before_time'] = loop.run_until_complete(plugin._maybe_daily_digest(now=EVENING + 3 * 3600))
    result['first'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE))
    result['again'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE + 600))
    plugin = new_plugin()       # a restart: the same night is not done again
    plugin.llm_functions = dict(plugin.llm_functions or {}, daily_digest={'enabled': True, 'provider': 'follow_llm'})
    result['after_restart'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE + 1200))
    result['calls'] = len(Model.digests)
    result['prompts'] = Model.digests
    result['tried_file'] = (DATA / 'self_model.json').read_text('utf-8') if (DATA / 'self_model.json').exists() else ''
    evs = events()
    result['events'] = [{k: e.get(k) for k in ('title', 'event', 'origin', 'session')} for e in evs]
    # what a reply sees: the group's in that group, not the private one; the private one there only
    in_group = harness.FakeEvent('x', sender='10002', name='柠檬', group=G1)
    in_g2 = harness.FakeEvent('x', sender='10005', name='桃桃', group=G2)
    in_private = harness.FakeEvent('x', sender='10004', name='桃子')
    result['seen'] = {name: [e['title'] for e in plugin._visible_events(ev, evs)] + [
        e['event'] for e in plugin._visible_events(ev, evs)]
        for name, ev in (('group', in_group), ('g2', in_g2), ('private', in_private))}
    # her notebook: the group sitting gets the group's events, the private sitting that chat's
    plugin.llm_functions = dict(plugin.llm_functions or {}, notebook={'enabled': True, 'provider': 'follow_llm'})
    clock.now = EVENING + 3.5 * 3600
    mats = {s: [m['text'] for m in plugin._notebook_materials(plugin._core(None), s, clock.now)]
            for s in plugin._notebook_sittings(clock.now)}
    result['notebook'] = {('group' if s == 'group' else 'private'): v for s, v in mats.items()}
    # deleting: by message, by person, and what a restored backup brings back
    result['forget_message'] = plugin._forget(source_ids=['g2'])
    result['after_message'] = [e['title'] for e in events()]
    loop.run_until_complete(plugin.page_forget_person('10004'))
    result['after_person'] = [e['title'] for e in events()]

if CASE == 'restore':
    chat()
    plugin.llm_functions = dict(plugin.llm_functions or {}, daily_digest={'enabled': True, 'provider': 'follow_llm'})
    loop.run_until_complete(plugin._maybe_daily_digest(now=LATE))
    result['before'] = sorted(e['title'] for e in events())
    # the owner deleted 柠檬 while this copy of the archive was kept aside, then it came back
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        reg.owner_delete(person='10002', stamp=2.0)
    plugin._forget_registered()
    result['after'] = sorted(e['title'] for e in events())

for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), 'utf-8')
