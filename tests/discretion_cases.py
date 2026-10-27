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
        json.dumps({'v': 0.1, 'open_loops': [{'text': '记得提醒我交报告', 'status': 'open'}],
                    'history': [{'ts': 1.0, 'emotion': 'joy', 'v': 0.1, 'text': '爬山记得带水哦'}]},
                   ensure_ascii=False), 'utf-8')
    (DATA / 'states' / 'default_FriendMessage_10001.json').write_text(
        json.dumps({'v': 0.4, 'history': [{'ts': 0.5, 'emotion': 'joy', 'v': 0.4, 'text': '蛋糕的事我帮你保密'}],
                    'stimuli': [{'labels': ['joy'], 'text': '我在偷偷准备一个惊喜蛋糕给大家', 'n': 1, 'ts': 0.5}]},
                   ensure_ascii=False), 'utf-8')
    os.utime(DATA / 'states' / 'default_FriendMessage_10001.json', (1000, 1000))
    os.utime(DATA / 'states' / 'default_GroupMessage_900001.json', (2000, 2000))  # the most recent one

if CASE == 'migrate_her':
    # a one-body state written by the first step-1 code, before her phone existed
    (DATA / 'states').mkdir(parents=True)
    GROUP_ORIGIN = {'where': 'group:900001', 'people': ['10002'], 'source_ids': [], 'visibility': 'public'}
    PRIVATE_ORIGIN = {'where': 'private:10001', 'people': ['10001'], 'source_ids': ['r1'], 'visibility': 'private'}
    (DATA / 'states' / 'her.json').write_text(json.dumps({
        'v': 0.2,
        'history': [{'ts': 1.0, 'emotion': 'joy', 'v': 0.2, 'text': '蛋糕的事我帮你保密', 'origin': PRIVATE_ORIGIN},
                    {'ts': 2.0, 'emotion': 'joy', 'v': 0.2, 'text': '爬山记得带水哦', 'origin': GROUP_ORIGIN},
                    {'ts': 3.0, 'emotion': 'joy', 'v': 0.2, 'text': '不知道从哪来的一句话'}],
        'open_loops': [{'text': '记得提醒我交报告', 'status': 'open', 'origin': GROUP_ORIGIN},
                       {'text': '记得提醒我买蛋糕', 'status': 'open'}],
        'event_anchors': [{'key': 'k', 'title': '惊喜蛋糕'}],
        'autobiography': [{'key': 'k', 'title': '惊喜蛋糕', 'meaning': '芒果在准备惊喜'}],
        'self_timeline': {'past': ['惊喜蛋糕'], 'present': '芒果在准备惊喜', 'future': []},
        'core_self': '惊喜蛋糕', 'narrative_self': '芒果在准备惊喜',
    }, ensure_ascii=False), 'utf-8')

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
    if CASE in ('forget', 'strong_event', 'consolidate'):  # summaries on, as in the golden 'full' run
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
    elif CASE == 'strong_event':
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '芒果', reply='好呀，惊喜蛋糕我帮你保密')
        t(30, '蛋糕要做草莓味的', '10001', '芒果', reply='草莓味的惊喜蛋糕听起来好甜')
        # strong feelings in a group right after: an event gets archived there
        group_lines = (('小爱 我好难过 想哭', '{"e":"sadness","i":0.9}'),
                       ('今天被骂了 真的很委屈', '{"e":"sadness","i":0.85}'),
                       ('气死我了！！！他凭什么这样说我', '{"e":"anger","i":0.8}'),
                       ('真的受够了！！！气死了！！！', '{"e":"anger","i":0.9}'))
        for text, tag in group_lines:
            t(20, text, '10002', '柠檬', A, reply='我陪着你<bc>%s</bc>' % tag)
        # past the per-chat cooldown; her last six replies still include the two private ones
        group_lines += (('我还是好生气！！！凭什么啊！！！', '{"e":"anger","i":0.9}'),)
        t(620, group_lines[-1][0], '10002', '柠檬', A, reply='我陪着你<bc>%s</bc>' % group_lines[-1][1])
        out['private_texts'] = ['小爱，我在偷偷准备一个惊喜蛋糕给大家', '好呀，惊喜蛋糕我帮你保密',
                                '蛋糕要做草莓味的', '草莓味的惊喜蛋糕听起来好甜']
        out['all_texts'] = out['private_texts'] + [x[0] for x in group_lines] + ['我陪着你']
        out.update(snapshot(plugin))
    elif CASE == 'loops':
        t(0, '记得提醒我明天交报告', '10001', '芒果', reply='记下啦')              # private loop
        t(30, '小爱 报告我交了', '10002', '柠檬', A)                              # settles nothing in private
        t(30, '记得提醒我明天交报告', '10003', '阿星', A, reply='记下啦')         # group A's own loop
        t(30, '小爱 报告的事', '10004', '桃子', B)
        t(30, '报告的事你还记得吗', '10001', '芒果')
        out['windows_after_talk'] = snapshot(plugin)['phone']
        core = plugin._core(None)
        for thing in ('去买菜', '浇花草', '还图书', '寄快递', '修单车', '交水费', '订机票', '拿外卖', '洗被子',
                      '换灯泡', '剪头发', '看牙医', '收衣服', '喂小鱼', '充话费', '倒垃圾', '擦窗户', '买牛奶',
                      '取包裹', '烤面包', '写日记', '练吉他', '背单词', '跑三圈', '读小说'):
            text = '记得提醒我明天' + thing
            plugin._window_update_loops(harness.FakeEvent(text, sender='10003', name='阿星', group=A), text, core)
        out['windows_after_many'] = snapshot(plugin)['phone']
    elif CASE == 'consolidate':
        # (texts close enough for the offline vectors to group them for a summary)
        for delay, text in ((0, '小爱，我在偷偷准备一个惊喜蛋糕给大家'), (20, '惊喜蛋糕给大家，我在偷偷准备一个'),
                            (20, '我在准备一个惊喜蛋糕偷偷给大家'), (20, '惊喜蛋糕要做草莓味的'),
                            (20, '草莓味的惊喜蛋糕要做')):
            t(delay, text, '10001', '芒果', reply='好呀')
        real = plugin._provider_for
        calls = []

        async def provider_that_forgets(kind, event=None):
            inner = await real(kind, event)

            class Meanwhile:  # he says "forget me" while she waits for the model
                async def text_chat(self, *a, **k):
                    if not calls:
                        calls.append(plugin._forget(person='10001'))
                    return await inner.text_chat(*a, **k)
            return Meanwhile() if inner is not None else None
        plugin._provider_for = provider_that_forgets
        mango = harness.FakeEvent('x', sender='10001', name='芒果')
        loop.run_until_complete(plugin._consolidate_memory(mango, plugin._core(None), force=True))
        harness.drain(loop)
        out['forgot_meanwhile'] = calls
        out['after'] = snapshot(plugin)
        # control: with nothing forgotten meanwhile, the same consolidation does save
        plugin._provider_for = real
        for delay, text in ((20, '小爱，我们群周末要去爬山'), (20, '我们群周末要去爬山，小爱'),
                            (20, '周末我们群要去爬山')):
            t(delay, text, '10002', '柠檬', A, reply='好呀')
        lemon = harness.FakeEvent('x', sender='10002', name='柠檬', group=A)
        loop.run_until_complete(plugin._consolidate_memory(lemon, plugin._core(None), force=True))
        harness.drain(loop)
        out['after_control'] = snapshot(plugin)
    elif CASE == 'migrate_her':
        out['her'] = json.loads((DATA / 'states' / 'her.json').read_text('utf-8'))
        out['archive'] = sorted(p.name for p in (DATA / 'states' / 'per_session_archive').glob('*.json'))
        out['phone'] = snapshot(plugin)['phone']
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
        out['phone'] = snapshot(plugin)['phone']
        out['her'] = json.loads((DATA / 'states' / 'her.json').read_text('utf-8'))
        t(0, '小爱 晚上好', '10004', '桃子', B)
        t(10, '小爱 交报告的事', '10002', '柠檬', A)
        t(10, '惊喜蛋糕', '10001', '芒果')
    for task in asyncio.all_tasks(loop):
        task.cancel()
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), 'utf-8')


def snapshot(plugin):
    path = DATA / 'memory' / 'library.json'
    lib = json.loads(path.read_text('utf-8')) if path.exists() else {'entries': [], 'rooms': {}}
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
        'phone': {place: plugin._read_window(place) for place in plugin._window_places()},
        'her_state': (DATA / 'states' / 'her.json').read_text('utf-8')
        if (DATA / 'states' / 'her.json').exists() else '',
    }


run()
