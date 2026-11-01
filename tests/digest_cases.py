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
    group_answer = None   # a case's own answer for a group

    async def text_chat(self, prompt='', system_prompt=None, **kwargs):
        p = str(prompt)
        if '今天在这里发生的几件事' in p:
            Model.digests.append(p)
            if Model.group_answer is not None and '一个群' in p:
                return harness.FakeResponse(json.dumps({'events': Model.group_answer}, ensure_ascii=False))
            if '一个私聊' in p:
                return harness.FakeResponse(json.dumps({'events': [
                    {'title': 'P1说了蓝莓计划', 'what': 'P1跟她说起蓝莓计划的安排', 'who': ['P1'], 'lines': [1, 2]}]},
                    ensure_ascii=False))
            return harness.FakeResponse(json.dumps({'events': [
                # P1 is 柠檬 (spoke first), P2 阿橙; Q codes are people only mentioned
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
    plugin = main.BioCorePlugin(ctx, config={'owner_qq': '10001', 'reply_private': ['10002', '10003', '10004', '10005']})
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
    turn('我来我来 @柠檬', '10001', '阿橙', group=G1, msg_id='g2')
    turn('今天抽卡又歪了', '10002', '柠檬', group=G1, msg_id='g3')
    turn('阿星今天没来', '10001', '阿橙', group=G1, msg_id='g4')
    turn('我的手机号是13812345678', '10001', '阿橙', group=G1, msg_id='g5')
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

def add_event(title, what, where, people, digest_kind=True, importance=0.5, n=[0], **more):
    n[0] += 1
    clock.advance(60)
    rec = dict({'id': 'e%d' % n[0], 'ts': clock.now, 'session': where, 'title': title, 'event': what,
                'event_key': title, 'importance': importance, 'centrality': 0.5,
                'origin': {'where': where, 'people': people, 'source_ids': ['s%d' % n[0]],
                           'visibility': 'private' if where.startswith('private:') else 'public'}}, **more)
    if digest_kind:
        rec['kind'] = 'daily_digest'
    plugin._append_event_archive(rec)


if CASE == 'fair':
    # six groups, four things each, in order; one strong event in the last group, about three people
    for g in range(6):
        for i in range(4):
            add_event('第%d群的事%d' % (g + 1, i), '经过%d' % i, 'group:90010%d' % g, ['1000%d' % i])
    add_event('大事', '三个人的大事', 'group:900105', ['10001', '10002', '10003'], digest_kind=False, importance=0.9)
    clock.now = EVENING + 3.5 * 3600
    mats = plugin._notebook_materials(plugin._core(None), 'group', clock.now)
    result['texts'] = [m['text'] for m in mats]
    result['windows'] = sorted({m['origin']['where'] for m in mats if m['ref'] != 'body'})

if CASE == 'reply':
    add_event('柠檬的生日聚会', '柠檬请大家去她家过生日', 'group:' + G1, ['10002'], digest_kind=False, importance=0.9)
    add_event('柠檬约周末打副本', '柠檬约大家周末一起打副本', 'group:' + G1, ['10002', '10001'])
    add_event('大家聊抽卡', '几个人在聊今天抽卡的运气', 'group:' + G1, ['10002', '10001'])
    add_event('阿橙的副本攻略', '阿橙分享了周末副本的打法', 'group:' + G1, ['10001'])
    add_event('副本开荒', '大家约好周末副本开荒', 'group:' + G1, ['10001'])
    add_event('桃子也想打副本', '桃子说周末也想打副本', 'group:' + G2, ['10004'])
    for name, text in (('related', '周末的副本几点开始'), ('unrelated', '你好呀')):
        ev = harness.FakeEvent(text, sender='10002', name='柠檬', group=G1)
        result[name] = plugin._event_context(ev)


def digest_on():
    plugin.llm_functions = dict(plugin.llm_functions or {}, daily_digest={'enabled': True, 'provider': 'follow_llm'})


def phone(place):
    return [x['text'] for x in plugin._read_window(place)['recent']]


if CASE == 'merge_gone':
    # 阿星 is ruled out but his words are still in her phone (an imported registry, a restored
    # backup); the note of the day is the same as an event she has, and names him
    turn('大家好', '10003', '阿星', group=G1, msg_id='g0')
    turn('周末一起打副本吗 阿星来不来', '10002', '柠檬', group=G1, msg_id='g1')
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')
    add_event('柠檬约周末打副本', '柠檬约大家周末打副本', 'default:GroupMessage:' + G1, ['10002'], digest_kind=False)
    Model.group_answer = [{'title': 'P1约周末打副本', 'what': 'P1约周末打副本，Q1也被叫上了', 'who': ['P1', 'Q1'],
                           'lines': [1]}]
    digest_on()
    result['night'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE))
    result['prompt'] = Model.digests[-1]
    result['events'] = [{'title': e.get('title'), 'origin': e.get('origin')} for e in plugin._event_archive(100, read_only=True)]
    files = [p for p in (DATA / 'archives').rglob('*') if p.is_file()]
    result['files_with_him'] = sorted(str(p.relative_to(DATA)) for p in files if '10003' in p.read_text('utf-8'))

if CASE == 'gone_names':
    turn('大家好', '10003', '阿星', group=G1, msg_id='g0')
    turn('周末打副本 阿星来不来', '10002', '柠檬', group=G1, msg_id='g1')
    turn('好呀', '10001', '阿橙', group=G1, msg_id='g2')
    result['phone_before_delete'] = phone('group:' + G1)
    result['deleted'] = loop.run_until_complete(plugin.page_forget_person('10003'))   # the owner, from the panel
    result['phone_at_once'] = phone('group:' + G1)
    turn('阿星今天在吗', '10002', '柠檬', group=G1, msg_id='g3')
    result['phone_before_restart'] = phone('group:' + G1)
    # a line that still has his name (a window file put back as it was): the material has a code
    win = plugin._read_window('group:' + G1)
    win['recent'].insert(0, dict(win['recent'][0], text='阿星说他周末有空', msg_id='g1b'))
    plugin._write_window('group:' + G1, win)
    # the night, before a restart: his name, said by others before he was deleted, is a code
    result['material_names'] = plugin._material_names('group:' + G1, plugin._read_window('group:' + G1)['recent'])
    digest_on()
    Model.group_answer = [{'title': 'P1约打副本', 'what': 'P1约大家打副本，Q1也被叫上了', 'who': ['P1', 'Q1'],
                           'lines': [1]},
                          {'title': 'P2答应了', 'what': 'P2说好呀', 'who': ['P2'], 'lines': [2]}]
    result['night'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE))
    result['prompt'] = Model.digests[-1]
    result['events'] = [e.get('event') for e in events()]
    plugin = new_plugin()                                          # a restart: nothing in memory
    clock.now = LATE + 600
    turn('阿星呢', '10001', '阿橙', group=G1, msg_id='g4')
    result['phone_after_restart'] = phone('group:' + G1)
    result['registry_has_name'] = '阿星'.encode('utf-8') in (DATA / forget_registry.FILE_NAME).read_bytes()

def ask(text, sender, name, group=None, reply='嗯嗯', msg_id=None):
    """A turn that wakes her; what the reply model is given."""
    clock.advance(60)
    event = harness.FakeEvent(text, sender=sender, name=name, group=group)
    event.message_obj.message_id = msg_id or ('m-%s-%d' % (sender, int(clock.now)))
    loop.run_until_complete(plugin.on_message(event))
    harness.drain(loop)
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
    harness.drain(loop)
    return '\n'.join([str(req.prompt or '')] + [p.get('text') if isinstance(p, dict) else str(p)
                                                for p in req.extra_user_content_parts])


def files_with(word, archive):
    out = []
    for p in sorted(DATA.rglob('*')):
        if not p.is_file() or p.name == forget_registry.FILE_NAME:
            continue
        if ('archive' in p.relative_to(DATA).parts) != archive:
            continue
        if word.encode('utf-8') in p.read_bytes():
            out.append(str(p.relative_to(DATA)).replace('\\', '/'))
    return out


if CASE == 'everywhere':
    # what the reviewer did (made-up): others speak of him to her; then the owner deletes him
    turn('大家好', '10003', '阿星', group=G1, msg_id='w0')
    ask('小爱 阿星周末想去打副本 你也来吗', '10002', '柠檬', group=G1, reply='好呀', msg_id='w1')
    ask('小爱 记得阿星说的那个副本吗', '10001', '阿橙', group=G1, reply='记得', msg_id='w2')
    # an event about it, of 柠檬's alone: its key names him, and a key merged into it too
    add_event('柠檬约阿星打副本', '柠檬约阿星周末一起打副本', 'default:GroupMessage:' + G1, ['10002'],
              digest_kind=False, merged_event_keys=['阿星的副本局'])
    # and a note of the night, its names framed (the owner, 10-29)
    add_event('「阿星」约「柠檬」打副本', '「柠檬」答应了「阿星」', 'default:GroupMessage:' + G1, ['10002'], id='framed')
    result['before'] = files_with('阿星', archive=False)
    result['keys_before'] = [(e.get('event_key'), e.get('merged_event_keys'))
                             for e in plugin._event_archive(100, read_only=True)]
    result['deleted'] = loop.run_until_complete(plugin.page_forget_person('10003'))
    result['at_once'] = files_with('阿星', archive=False)
    result['keys_at_once'] = [(e.get('event_key'), e.get('merged_event_keys'))
                              for e in plugin._event_archive(100, read_only=True)]
    result['framed_at_once'] = [(e.get('title'), e.get('event')) for e in plugin._event_archive(100, read_only=True)
                                if e.get('id') == 'framed']
    result['framed_somebody'] = files_with('「某人」', archive=False) + files_with('「有人」', archive=False)
    result['prompt'] = ask('小爱 周末的副本谁去', '10001', '阿橙', group=G1, reply='还不知道', msg_id='w3')
    result['after_a_turn'] = files_with('阿星', archive=False)
    plugin = new_plugin()                                      # a restart
    result['prompt_after_restart'] = ask('小爱 副本几点开始', '10001', '阿橙', group=G1, reply='八点', msg_id='w4')
    result['after_restart'] = files_with('阿星', archive=False)
    result['archives'] = files_with('阿星', archive=True)

if CASE == 'everyday':
    # someone whose card is an everyday word
    turn('我也来', '10006', '周末', group=G1, msg_id='e0')
    turn('周末一起打副本', '10002', '柠檬', group=G1, msg_id='e1')
    turn('@周末 来不来', '10002', '柠檬', group=G1, msg_id='e2')
    turn('周末说他不来', '10001', '阿橙', group=G1, msg_id='e3')
    loop.run_until_complete(plugin.page_forget_person('10006'))
    result['at_once'] = phone('group:' + G1)
    plugin = new_plugin()
    turn('周末去哪玩', '10001', '阿橙', group=G1, msg_id='e4')
    turn('周末：我也不来了', '10002', '柠檬', group=G1, msg_id='e5')
    result['after_restart'] = phone('group:' + G1)[-2:]

if CASE == 'marks':
    chat()
    # something in her notebook, and the registry unreadable while tonight's mark is saved
    plugin.self_model['notebook'] = [{'id': 'n1', 'text': '今天下雨了', 'ts': clock.now,
                                      'origin': {'where': 'self', 'people': [], 'source_ids': [], 'visibility': 'self'}}]

    def unreadable(item):
        raise forget_registry.Unreadable('locked')
    plugin._origin_kept = unreadable
    digest_on()
    plugin.llm_functions = dict(plugin.llm_functions or {}, notebook={'enabled': True, 'provider': 'follow_llm'})
    result['first'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE))
    loop.run_until_complete(plugin._maybe_write_notebook(now=EVENING + 3.5 * 3600))
    plugin = new_plugin()
    digest_on()
    result['after_restart'] = loop.run_until_complete(plugin._maybe_daily_digest(now=LATE + 600))
    result['calls'] = len(Model.digests)
    saved = json.loads((DATA / 'self_model.json').read_text('utf-8'))
    result['notebook_tried'] = saved.get('notebook_night', {}).get('tried')


for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), 'utf-8')
