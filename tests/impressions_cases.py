"""Scripted runs for the impressions wiring tests (step 1-3-3); prints a JSON result.

Run in a fresh interpreter (test_impressions_wiring does this):
    PYTHONHASHSEED=0 python tests/impressions_cases.py <empty data dir> <out.json> <case>

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
G1, G2, G3 = '900001', '900002', '900003'
EVENING = time.mktime(time.strptime('2026-10-04 20:00:00', '%Y-%m-%d %H:%M:%S'))

import forget_registry  # noqa: E402
import impressions  # noqa: E402

if CASE in ('views', 'anon'):
    store = impressions.Store(DATA / 'people')
    data = store.load('group:' + G1)
    rec = data['people'].setdefault('10002', impressions._record('group:' + G1, '10002'))
    rec.update(name='柠檬', aliases=['柠柠'], style='说话很快，爱用语气词', topics=['抽卡', '副本'],
               stats={'msgs': 40, 'days': 3}, updated='2026-10-03')
    store.save('group:' + G1, data)

if CASE == 'nightly':
    clock.now = EVENING
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')

import main  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402


class Model(harness.FakeProvider):
    """Answers the impressions prompt; counts the calls."""
    impressions_calls = 0

    async def text_chat(self, prompt='', system_prompt=None, **kwargs):
        if '群里几位群友今天说的话' in str(prompt):
            Model.impressions_calls += 1
            self.last = str(prompt)
            return harness.FakeResponse(json.dumps({
                # P1 is 芒果, P2 is 柠檬 (most lines first, then by number); a name is kept only
                # where others really called someone that: 柠柠 for her, nothing for him
                'P1': {'style': '说话慢慢的', 'topics': ['副本'], 'aliases': ['柠柠子']},
                'P2': {'style': '爱用语气词，常接别人的梗', 'topics': ['抽卡'], 'aliases': ['柠柠']}},
                ensure_ascii=False))
        return await super().text_chat(prompt=prompt, system_prompt=system_prompt, **kwargs)


ctx = harness.FakeContext()
ctx.provider = Model()
config = {'member_aliases': ['10002:小柠']} if CASE in ('views', 'anon') else {}
plugin = main.BioCorePlugin(ctx, config=config)
plugin._ipv4_json = harness.fake_ipv4_json
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def turn(text, sender, name, group=None, reply=None, advance=60, msg_id=None):
    clock.advance(advance)
    event = harness.FakeEvent(text, sender=sender, name=name, group=group)
    event.message_obj.message_id = msg_id or ('m-%s-%d' % (sender, int(clock.now)))
    loop.run_until_complete(plugin.on_message(event))
    harness.drain(loop)
    if reply is None:
        return None
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
    harness.drain(loop)
    text_parts = '\n'.join(p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts)
    return next((ln for ln in text_parts.splitlines() if ln.startswith('[认识的人]')), '')


result = {}

if CASE == 'views':
    result['her_group'] = turn('小爱 在吗', '10002', '柠檬', group=G1, reply='在呀')
    result['other_group_present'] = turn('小爱 晚上好', '10002', '柠檬', group=G2, reply='晚上好')
    result['other_group_absent'] = turn('小爱 你好', '10004', '桃子', group=G3, reply='你好呀')
    turn('最近副本好难打', '10002', '柠檬')
    result['her_private'] = turn('小爱 陪我聊聊', '10002', '柠檬', reply='好呀')
    result['someone_elses_private'] = turn('小爱 你好', '10001', '芒果', reply='你好')

if CASE == 'nightly':
    for i in range(12):
        turn('今天抽卡又歪了 %d' % i, '10002', '柠檬', group=G1, advance=30, msg_id='a%d' % i)
        turn('@柠檬 柠柠别灰心' if i < 2 else '我也是 %d' % i, '10001', '芒果', group=G1, advance=30)
        turn('阿星路过 %d' % i, '10003', '阿星', group=G1, advance=30)
    late = EVENING + 3.5 * 3600   # 23:30
    off = loop.run_until_complete(plugin._maybe_update_impressions(now=late))
    result['off'] = {'answer': off, 'calls': Model.impressions_calls}
    plugin.llm_functions = dict(plugin.llm_functions or {}, group_impressions={'enabled': True, 'provider': 'follow_llm'})
    first = loop.run_until_complete(plugin._maybe_update_impressions(now=late))
    again = loop.run_until_complete(plugin._maybe_update_impressions(now=late + 600))
    result['on'] = {'first': first, 'again': again, 'calls': Model.impressions_calls}
    result['prompt_has'] = {w: w in getattr(ctx.provider, 'last', '') for w in ('柠檬', '芒果', '阿星', '柠柠', '10002')}
    store = plugin._impression_store()
    result['people'] = store.load('group:' + G1)['people']
    status = loop.run_until_complete(plugin.page_status())
    result['page'] = status['data']['impressions']
    result['delete'] = loop.run_until_complete(plugin.page_impression_delete('10002'))
    result['after_delete'] = sorted(store.load('group:' + G1)['people'])
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        result['registry_kinds'] = sorted((r['kind'], r['qq']) for r in reg.rows())
    # the next night: she does not write one of him again
    clock.now = EVENING + 86400
    for i in range(12):
        turn('今天又抽卡 %d' % i, '10002', '柠檬', group=G1, advance=30)
    loop.run_until_complete(plugin._maybe_update_impressions(now=EVENING + 86400 + 3.5 * 3600))
    result['next_night'] = sorted(store.load('group:' + G1)['people'])
    # deleting the person takes his impressions too
    loop.run_until_complete(plugin.page_forget_person('10001'))
    result['after_person'] = sorted(store.load('group:' + G1)['people'])

if CASE == 'anon':
    result['names'] = plugin._known_names(['10002'])
    result['text'] = plugin._anonymized('柠柠说周末去爬山，小柠也去', ['10002'])
    ev = {'title': '爬山', 'event': '柠柠约大家周末去爬山', 'ts': clock.now,
          'origin': {'where': 'group:' + G1, 'people': ['10002'], 'source_ids': ['m1'], 'visibility': 'public'}}
    elsewhere = harness.FakeEvent('x', sender='10004', name='桃子', group=G2)
    result['event_elsewhere'] = plugin._visible_events(elsewhere, [ev])[0]['event']

for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), 'utf-8')
