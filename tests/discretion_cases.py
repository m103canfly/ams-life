"""Scripted conversations for the discretion tests; prints a JSON result.

Run in a fresh interpreter (test_discretion does this):
    PYTHONHASHSEED=0 python tests/discretion_cases.py <empty data dir> <out.json> <case>

All numbers and names are made up. No network, no model, no messages sent.
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

if CASE == 'migrate':
    # BioCore's per-session layout, written before the plugin starts.
    (DATA / 'memory').mkdir(parents=True)
    (DATA / 'states').mkdir(parents=True)
    old = {
        'default_FriendMessage_10001': [{'id': 'p1', 'text': '我在偷偷准备一个惊喜蛋糕给大家', 'role': 'user',
                                         'sender_id': '10001', 'sender_name': '芒果', 'vector': [], 'ts': 1.0,
                                         'provenance': {'session': 'default:FriendMessage:10001',
                                                        'sender_id': '10001', 'message_refs': ['r1']}}],
        'default_GroupMessage_900001': [{'id': 'g1', 'text': '周末一起去爬山吧', 'role': 'user',
                                         'sender_id': '10002', 'sender_name': '柠檬', 'vector': [], 'ts': 2.0},
                                        {'id': 'c1', 'text': '复制过来的', 'role': 'user', 'vector': [], 'ts': 3.0,
                                         'shared_from_session': 'default:FriendMessage:10001'}],
    }
    for stem, entries in old.items():
        (DATA / 'memory' / (stem + '.json')).write_text(
            json.dumps({'entries': entries, 'working_set': ['x']}, ensure_ascii=False), 'utf-8')
    import os
    (DATA / 'states' / 'default_GroupMessage_900001.json').write_text(
        json.dumps({'v': 0.1, 'open_loops': [{'text': '记得提醒我交报告', 'status': 'open'}]}), 'utf-8')
    (DATA / 'states' / 'default_FriendMessage_10001.json').write_text(json.dumps({'v': 0.4}), 'utf-8')
    os.utime(DATA / 'states' / 'default_FriendMessage_10001.json', (1000, 1000))
    os.utime(DATA / 'states' / 'default_GroupMessage_900001.json', (2000, 2000))  # the most recent one

import main  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

A, B = '900001', '900002'
JOY = '<bc>{"e":"joy","i":0.95}</bc>'


def turn(plugin, loop, delay, text, sender, name, group=None, reply='嗯嗯'):
    clock.advance(delay)
    event = harness.FakeEvent(text, sender=sender, name=name, group=group)
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
    harness.drain(loop)
    prompt = '\n'.join(p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts)
    return {'session': event.unified_msg_origin, 'prompt': prompt, 'refs': plugin._message_refs(event)}


def run():
    config = {}
    if CASE == 'forget':  # summaries on, as in the golden 'full' run, so events are archived
        config = {'llm_only_reply_summary': False, 'memory_worthiness_enabled': False}
    plugin = main.BioCorePlugin(harness.FakeContext(), config=config)
    plugin._ipv4_json = harness.fake_ipv4_json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    out = {'turns': []}
    t = lambda *a, **k: out['turns'].append(turn(plugin, loop, *a, **k)) or out['turns'][-1]  # noqa: E731

    if CASE == 'private':
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '芒果', reply='好呀，我帮你保密')
        t(30, '惊喜蛋糕的事你还记得吗', '10001', '芒果')                      # control: same chat
        t(60, '小爱，惊喜蛋糕是什么情况', '10002', '柠檬', A)
        t(30, '有没有人在准备惊喜蛋糕', '10001', '芒果', A)
        t(30, '小爱 惊喜蛋糕', '10004', '桃子', B)
        out['private_texts'] = ['我在偷偷准备一个惊喜蛋糕给大家', '好呀，我帮你保密']
    elif CASE == 'anon':
        t(0, '小爱，我们群周末要去爬山', '10002', '柠檬', A, reply='爬山好呀')
        t(30, '周末爬山记得带水', '10003', '阿星', A)
        t(60, '小爱 周末爬山的事你听说了吗', '10004', '桃子', B)
    elif CASE == 'echo':
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '芒果')
        t(60, '跟大家说下，我在偷偷准备一个惊喜蛋糕', '10001', '芒果', A)
        t(30, '小爱 惊喜蛋糕准备得怎么样了', '10001', '芒果', A)
        t(30, '小爱 惊喜蛋糕的事', '10004', '桃子', B)
    elif CASE == 'one_body':
        out['v_start'] = plugin._core(None).v
        for i in range(4):
            t(5, '太开心了！！！我终于抽到了！！！', '10002', '柠檬', A, reply='恭喜恭喜！' + JOY)
        out['v_after_a'] = plugin._core(None).v
        t(0, '小爱 晚上好', '10004', '桃子', B)
        out['cores'] = list(plugin.cores)
    elif CASE == 'forget':
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '芒果')
        # the strong-feeling stretch of the golden scenario, so events get archived
        for delay, text, tag in ((400, '小爱 我好难过 想哭', '{"e":"sadness","i":0.9}'),
                                 (20, '今天被骂了 真的很委屈', '{"e":"sadness","i":0.85}'),
                                 (20, '气死我了！！！他凭什么这样说我', '{"e":"anger","i":0.8}'),
                                 (30, '真的受够了！！！气死了！！！', '{"e":"anger","i":0.9}'),
                                 (620, '我还是好生气！！！凭什么啊！！！', '{"e":"anger","i":0.9}')):
            t(delay, text, '10001', '芒果', reply='我陪着你<bc>%s</bc>' % tag)
        t(60, '小爱 我今天也在群里', '10001', '芒果', A)
        lemon = t(30, '小爱，我们群周末要去爬山', '10002', '柠檬', A)
        t(30, '小爱，周末爬山带什么好', '10002', '柠檬', A)
        out['before'] = snapshot(plugin)
        out['forgot_person'] = plugin._forget(person='10001')
        out['after_person'] = snapshot(plugin)
        out['forgot_source'] = plugin._forget(source_ids=lemon['refs'])
        out['after_source'] = snapshot(plugin)
    elif CASE == 'migrate':
        lib = json.loads((DATA / 'memory' / 'library.json').read_text('utf-8'))
        out['library'] = [{'id': e.get('id'), 'origin': e.get('origin')} for e in lib['entries']]
        out['rooms'] = sorted(lib['rooms'])
        out['legacy'] = sorted(p.name for p in (DATA / 'memory' / 'per_session_legacy').glob('*.json'))
        out['memory_dir'] = sorted(p.name for p in (DATA / 'memory').glob('*.json'))
        out['states_dir'] = sorted(p.name for p in (DATA / 'states').glob('*.json'))
        out['states_archive'] = sorted(p.name for p in (DATA / 'states' / 'per_session_archive').glob('*.json'))
        core = plugin._core(None)
        out['v'] = core.v
        out['loops'] = [dict(x) for x in core.open_loops]
        t(0, '小爱 晚上好', '10004', '桃子', B)
        t(10, '小爱 交报告的事', '10002', '柠檬', A)
        t(10, '惊喜蛋糕', '10001', '芒果')
    for task in asyncio.all_tasks(loop):
        task.cancel()
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), 'utf-8')


def snapshot(plugin):
    lib = json.loads((DATA / 'memory' / 'library.json').read_text('utf-8'))
    events = []
    path = DATA / 'archives' / 'events.jsonl'
    if path.exists():
        events = [json.loads(x) for x in path.read_text('utf-8').splitlines() if x.strip()]
    return {
        'memories': [{'text': e.get('text'), 'sender_id': e.get('sender_id'), 'origin': e.get('origin')}
                     for e in lib['entries']],
        'events': [{'origin': main.discretion.origin_of(e), 'text': ' '.join(str(e.get(k) or '') for k in
                                                                              ('title', 'event', 'big_summary'))}
                   for e in events],
        'event_files': {str(p.relative_to(DATA)): len([x for x in p.read_text('utf-8').splitlines() if x.strip()])
                        for p in sorted((DATA / 'archives').rglob('events.jsonl'))},
        'users': sorted(p.stem for p in (DATA / 'users').glob('*.json')),
        'rooms': sorted(lib['rooms']),
        'body': [x.get('text') for name in main.CORE_TEXT_LISTS
                 for x in (getattr(plugin._core(None), name, None) or []) if isinstance(x, dict)],
    }


run()
