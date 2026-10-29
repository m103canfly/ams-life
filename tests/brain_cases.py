"""Scripted runs for the brain map's data (pages/brain, mixin_brain.py); prints a JSON result.

Run in a fresh interpreter (test_brain_data does this):
    PYTHONHASHSEED=0 python tests/brain_cases.py <empty data dir> <out.json> <case>

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
G1, G2 = '900001', '900002'


def write(rel, obj):
    path = DATA / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if rel.endswith('.jsonl'):
        path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in obj), 'utf-8')
    else:
        path.write_text(json.dumps(obj, ensure_ascii=False), 'utf-8')


def origin(where, people, sids, vis):
    return {'where': where, 'people': people, 'source_ids': sids, 'visibility': vis}


# ---------------------------------------------------------------- written before the plugin starts
import forget_registry  # noqa: E402
with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
    reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')   # 阿星: never kept
    reg.stop_impression('10004', note='owner:panel')                                         # 桃子: no impression
write('self_model.json', {'notebook': [
    {'id': 'n-self', 'text': '想多听听大家在聊什么', 'ts': clock.now - 50, 'origin': origin('self', [], [], 'self')},
    {'id': 'n-priv', 'text': '芒果好像在准备惊喜', 'ts': clock.now - 40,
     'origin': origin('private:10001', ['10001'], ['m-secret'], 'private')},
    {'id': 'n-star', 'text': '阿星说下雨了', 'ts': clock.now - 30,
     'origin': origin('group:' + G2, ['10003'], ['m-star'], 'public')}]})
write('archives/events.jsonl', [
    {'id': 'evt_hike', 'title': '爬山的约定', 'event': '柠檬约大家周末爬山', 'ts': clock.now - 20, 'emotion': 'joy',
     'importance': 0.7, 'origin': origin('group:' + G1, ['10002'], ['m-hike'], 'public')},
    {'id': 'evt_star', 'title': '阿星的雨天', 'event': '阿星说下雨了', 'ts': clock.now - 10,
     'origin': origin('group:' + G2, ['10003'], ['m-star'], 'public')}])

import main  # noqa: E402
import brain_graph  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

ctx = harness.FakeContext()
plugin = main.BioCorePlugin(ctx, config={})
plugin._ipv4_json = harness.fake_ipv4_json
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def turn(text, sender, name, group=None, reply=None, msg_id=None, advance=60):
    clock.advance(advance)
    event = harness.FakeEvent(text, sender=sender, name=name, group=group)
    event.message_obj.message_id = msg_id or ('m-' + sender + '-' + str(int(clock.now)))
    loop.run_until_complete(plugin.on_message(event))
    harness.drain(loop)
    if reply is None:
        return event
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
    harness.drain(loop)
    return event


def run(coro):
    return loop.run_until_complete(coro)


def graph():
    """page/brain, every part of it joined."""
    first = run(plugin.page_brain({}))
    if first['status'] != 'ok':
        return first
    data = dict(first['data'])
    for k in range(1, data['parts']):
        part = run(plugin.page_brain({'part': str(k), 'snap': data['snap']}))
        assert part['status'] == 'ok', part
        data['nodes'] = data['nodes'] + part['data']['nodes']
        data['edges'] = data['edges'] + part['data']['edges']
    return {'status': 'ok', 'data': data}


def node(pid, reveal=''):
    return run(plugin.page_brain_node({'id': pid, 'reveal': reveal}))


def search(q):
    return run(plugin.page_brain_search({'q': q}))['data']['ids']


def turns_file():
    path = DATA / 'brain_turns.json'
    return json.loads(path.read_text('utf-8'))['turns'] if path.exists() else []


def library_ids():
    return {e['id'] for e in json.loads((DATA / 'memory' / 'library.json').read_text('utf-8'))['entries']}


def chat():
    turn('小爱 我最近在学弹吉他', '10001', '芒果', group=G1, reply='好厉害！', msg_id='m-guitar')
    turn('小爱 周末去爬山吗', '10002', '柠檬', group=G1, reply='好呀，记得带水~', msg_id='m-hike')
    turn('小爱，跟你说个悄悄话，我在准备一个惊喜', '10001', '芒果', reply='我帮你保密~', msg_id='m-secret')
    turn('小爱 今天下雨了', '10003', '阿星', group=G2, reply='记得带伞', msg_id='m-star')
    turn('小爱 晚上好', '10004', '桃子', group=G2, reply='晚上好呀', msg_id='m-hi')
    # the same words again: the private one is recalled in his private chat, held back in the group
    turn('小爱 惊喜准备得怎么样了', '10001', '芒果', reply='快好了吗', msg_id='m-secret-2')
    turn('小爱 惊喜准备得怎么样了', '10002', '柠檬', group=G1, reply='什么惊喜呀', msg_id='m-ask')
    turn('小爱 周末去爬山吗 还去吗', '10002', '柠檬', group=G1, reply='去呀', msg_id='m-hike-2')
    store = plugin._impression_store()
    for place, people in (('group:' + G1, {'10001': ('芒果', '爱分享', 9), '10002': ('柠檬', '很照顾人', 4)}),
                          ('group:' + G2, {'10003': ('阿星', '总是半夜出现', 5), '10004': ('桃子', '话不多', 3)})):
        data = store.load(place)
        for qq, (name, style, msgs) in people.items():
            data['people'][qq] = {'name': name, 'aliases': [], 'style': style, 'topics': ['爬山'],
                                  'stats': {'msgs': msgs, 'days': 1}, 'updated': '2026-10-28'}
        store.save(place, data)


result = {}
chat()

def files():
    return {p.relative_to(DATA).as_posix(): p.read_bytes() for p in sorted(DATA.rglob('*')) if p.is_file()}


if CASE == 'graph':
    on_disk = files()
    g = graph()
    result['graph'] = g
    result['text'] = json.dumps(g, ensure_ascii=False)
    nodes = g['data']['nodes']
    by_kind = {}
    for n in nodes:
        by_kind.setdefault(n['kind'], []).append(n)
    people = {}
    for p in by_kind.get('person', []):
        d = node(p['id'])['data']
        people[d['title']] = {'id': p['id'], 'detail': d, 'qq': node(p['id'], 'qq')['data']}
    result['people'] = people
    result['memory_detail'] = node(next(n['id'] for n in by_kind['memory'] if n['cat'] == '私下'))
    result['window_titles'] = sorted(node(w['id'])['data']['title'] for w in by_kind['window'])
    result['search'] = {q: search(q) for q in ('吉他', '阿星', '下雨', '芒果', '想多听听')}
    result['node_ids'] = [n['id'] for n in nodes]
    result['turns_file'] = turns_file()
    result['library_ids'] = sorted(library_ids())
    result['missing'] = node('m:0000000000')
    result['routes'] = [r for r in ctx.web_routes if '/page/brain' in r]
    result['changed_on_disk'] = sorted(k for k in set(on_disk) | set(files()) if on_disk.get(k) != files().get(k))
    result['said'] = [t for t in ('我最近在学弹吉他', '周末去爬山吗', '悄悄话', '准备一个惊喜', '今天下雨了', '晚上好',
                                  '好厉害', '记得带水', '我帮你保密', '想多听听', '爱分享', '很照顾人')]
    result['numbers'] = ['10001', '10002', '10003', '10004', G1, G2]
    result['names'] = ['芒果', '柠檬', '阿星', '桃子']

if CASE == 'number_card':
    # someone whose group card is a string of digits (made up): the title is not that string
    turn('小爱 我也想去爬山', '10006', '10006', group=G1, reply='一起呀', msg_id='m-number')
    store = plugin._impression_store()
    data = store.load('group:' + G1)
    data['people']['10006'] = {'name': '10006', 'aliases': [], 'style': '刚来', 'topics': ['爬山'],
                               'stats': {'msgs': 1, 'days': 1}, 'updated': '2026-10-28'}
    store.save('group:' + G1, data)
    g = graph()
    result['text'] = json.dumps(g, ensure_ascii=False)
    people = {}
    for p in (n for n in g['data']['nodes'] if n['kind'] == 'person'):
        d = node(p['id'])['data']
        people[d['title']] = {'detail': json.dumps(d, ensure_ascii=False), 'qq': node(p['id'], 'qq')['data']}
    result['people'] = people
    result['search'] = search('10006')

if CASE == 'numbers_in_words':
    # numbers are kept in what she keeps (the owner, 10-29); the page still shows none of them
    turn('小爱 我的号是 10002 我们群号是 %s 周末去爬山' % G1, '10002', '柠檬', group=G1, reply='一起呀', msg_id='m-num')
    g = graph()
    result['text'] = json.dumps(g, ensure_ascii=False)
    result['kept'] = [e['text'] for e in plugin._read_library(vectors=False)['entries']]
    mem = [n for n in g['data']['nodes'] if n['kind'] == 'memory']
    result['details'] = [node(n['id'])['data'] for n in mem]
    result['search'] = {q: search(q) for q in ('10002', G1, '我的号是')}
    lemon = [p for p in g['data']['nodes'] if p['kind'] == 'person' and node(p['id'])['data']['title'] == '柠檬']
    result['qq'] = node(lemon[0]['id'], 'qq')['data'] if lemon else None

if CASE == 'frames':
    # what she keeps keeps the frames round names (the owner, 10-29): so does the page
    turn('小爱 周末爬山吗', '10002', '柠檬', group=G1, reply='好呀', msg_id='m-fr')
    plugin._append_event_archive({
        'id': 'fr', 'ts': clock.now, 'session': 'default:GroupMessage:' + G1, 'title': '「柠檬」约「芒果」爬山',
        'event': '「柠檬」约「芒果」周末爬山', 'event_key': 'fr',
        'origin': main.discretion.make_origin('group:' + G1, ['10002'], ['m-fr'])})
    g = graph()
    ev = [n for n in g['data']['nodes'] if n['kind'] == 'event']
    result['details'] = [node(n['id'])['data']['text'] for n in ev]

if CASE == 'memories':
    # "她记住了什么": the same snapshot as a list (memory_list.py)
    import time as _time
    turn('小爱 我的游戏号是 12345678 记得加我', '10002', '柠檬', group=G1, reply='好呀', msg_id='m-number')
    on_disk = files()

    def mem(**args):
        return run(plugin.page_memories(args))
    first = mem()
    result['first'] = first
    result['places'] = first['data']['places']
    # every page of three, joined
    pages, after = [], ''
    while True:
        d = mem(limit='3', after=after)['data']
        pages.append([r['id'] for r in d['items']])
        after = d['next']
        if not after or len(pages) > 50:
            break
    result['pages'] = pages
    result['by_kind'] = {k: [r['text'] for r in mem(kind=k)['data']['items']] for k in ('memory', 'event', 'note', 'impression')}
    result['private'] = [r['vis'] for r in mem(vis='private')['data']['items']]
    g1 = next(p['id'] for p in first['data']['places'] if p['label'] == '群1')
    result['in_g1'] = sorted({r['where'] for r in mem(place=g1)['data']['items']})
    result['q'] = [r['text'] for r in mem(q='爬山')['data']['items']]
    result['q_number'] = len(mem(q='12345678')['data']['items'])
    today = _time.strftime('%Y-%m-%d', _time.localtime(clock.now))
    result['today'] = len(mem(**{'from': today, 'to': today})['data']['items'])
    result['long_ago'] = len(mem(**{'from': '2001-01-01', 'to': '2001-01-02'})['data']['items'])
    numbered = [r for r in first['data']['items'] if r['has_number']]
    result['numbered'] = numbered
    result['number'] = run(plugin.page_memories_number({'id': numbered[0]['id']})) if numbered else None
    result['number_missing'] = run(plugin.page_memories_number({'id': 'm:0000000000'}))
    result['changed_on_disk'] = sorted(k for k in set(on_disk) | set(files()) if on_disk.get(k) != files().get(k))
    result['routes'] = [r for r in ctx.web_routes if '/page/memories' in r]

if CASE == 'paging':
    brain_graph.PART_NODES, brain_graph.PART_EDGES = 4, 5
    whole = graph()
    first = run(plugin.page_brain({}))
    result['parts'] = first['data']['parts']
    result['whole_nodes'] = len(whole['data']['nodes'])
    result['whole_edges'] = len(whole['data']['edges'])
    result['unique_nodes'] = len({n['id'] for n in whole['data']['nodes']})
    result['dangling'] = [e for e in whole['data']['edges']
                          if e['s'] not in {n['id'] for n in whole['data']['nodes']}
                          or e['t'] not in {n['id'] for n in whole['data']['nodes']}]
    result['wrong_snap'] = run(plugin.page_brain({'part': '1', 'snap': 'nope'}))
    snap = first['data']['snap']
    run(plugin.page_forget_person('10002'))                                     # deleted meanwhile
    result['after_delete'] = run(plugin.page_brain({'part': '1', 'snap': snap}))

if CASE == 'deletes':
    before = graph()['data']
    result['before_search'] = {q: search(q) for q in ('吉他', '惊喜', '爬山')}
    guitar_ids = search('吉他')
    before_turns = turns_file()
    result['before_turns'] = before_turns
    hike = next(e for e in json.loads((DATA / 'memory' / 'library.json').read_text('utf-8'))['entries']
                if e.get('text', '') == '小爱 周末去爬山吗')
    result['hike_id'] = hike['id']
    hike_pid = brain_graph.PageIds(plugin._brain_key())('m', hike['id'])
    result['hike_open_before'] = node(hike_pid)['status']
    result['answer_memory'] = run(plugin.page_memory_delete('library', hike['id']))
    result['hike_open_after'] = node(hike_pid)['status']
    result['turns_after_memory'] = turns_file()
    result['search_hike'] = search('周末去爬山吗')
    result['answer_person'] = run(plugin.page_forget_person('10001'))
    after = graph()['data']
    result['after_text'] = json.dumps(after, ensure_ascii=False)
    result['after_search'] = {q: search(q) for q in ('吉他', '惊喜', '芒果')}
    result['old_ids_open'] = [node(i)['status'] for i in guitar_ids]
    result['turns_after_person'] = turns_file()
    result['library_ids'] = sorted(library_ids())

if CASE == 'registry_broken':
    import sqlite3

    class Broken:
        def __getattr__(self, name):
            def fail(*a, **k):
                raise sqlite3.OperationalError('database is locked')
            return fail
    real = plugin._registry()
    plugin._forget_reg, plugin._forget_snap = Broken(), None          # the whole registry
    result['page'] = run(plugin.page_brain({}))
    result['node'] = run(plugin.page_brain_node({'id': 'x'}))
    result['search'] = run(plugin.page_brain_search({'q': '吉他'}))
    result['memories'] = run(plugin.page_memories({}))
    result['memories_number'] = run(plugin.page_memories_number({'id': 'x'}))
    n_before = len(turns_file())
    turn('小爱 吉他练得怎么样', '10002', '柠檬', group=G1, reply='还在练呢', msg_id='m-later')
    result['turns_noted_while_broken'] = len(turns_file()) - n_before
    plugin._forget_reg, plugin._forget_snap = real, None

    def rows_fail(since=0):                                          # only its rows
        raise sqlite3.OperationalError('database is locked')
    plugin._brain_cache = None
    real.rows, real_rows = rows_fail, real.rows
    result['page_rows'] = run(plugin.page_brain({}))
    real.rows = real_rows
    result['page_after'] = run(plugin.page_brain({}))['status']

if CASE == 'errors':
    # an error that names a path on this computer: the page gets a short reason, the log the rest
    def boom():
        raise OSError(2, 'No such file', 'D:/made-up-folder/x.json')
    plugin._brain_sources = boom
    result['page'] = run(plugin.page_brain({}))
    result['node'] = run(plugin.page_brain_node({'id': 'x'}))
    result['search'] = run(plugin.page_brain_search({'q': 'x'}))
    result['memories'] = run(plugin.page_memories({}))

if CASE == 'threads':
    # files are read on the event loop's thread (where she writes them); only the build runs elsewhere
    import threading
    seen = {}
    real_sources, real_build = plugin._brain_sources, plugin._brain_build

    def sources():
        seen['read'] = threading.get_ident()
        return real_sources()

    def build(*a):
        seen['build'] = threading.get_ident()
        return real_build(*a)
    plugin._brain_sources, plugin._brain_build = sources, build
    result['status'] = run(plugin.page_brain({}))['status']
    result['read_on_loop'] = seen.get('read') == threading.get_ident()
    result['built_elsewhere'] = seen.get('build') not in (None, threading.get_ident())
    seen.clear()
    plugin._brain_cache = None
    result['memories_status'] = run(plugin.page_memories({}))['status']
    result['memories_read_on_loop'] = seen.get('read') == threading.get_ident()
    result['memories_built_elsewhere'] = seen.get('build') not in (None, threading.get_ident())

if CASE == 'stale':
    # something is deleted between the message coming in and the turn being noted: not noted
    event = harness.FakeEvent('小爱 惊喜', sender='10002', name='柠檬', group=G1)
    plugin._begin_job()
    plugin._forget(source_ids=['m-nothing-like-this'])        # the forget count moves on
    n_before = len(turns_file())
    lib = sorted(library_ids())
    result['noted'] = plugin._note_turn(event, {'recall_order': lib[:2], 'recall_held': [], 'recall_path': []})
    result['n'] = len(turns_file()) - n_before
    plugin._begin_job()
    result['noted_fresh'] = plugin._note_turn(event, {'recall_order': lib[:2] + ['not-a-memory'],
                                                      'recall_held': [], 'recall_path': [[lib[0], lib[1]]]})

if CASE == 'restore':
    backup = run(plugin.page_backup())['data']['base64']
    run(plugin.page_forget_person('10001'))
    # a row added after the backup that is not one of the owner's deletes (an import, say):
    # the restored library leaves out 柠檬's words in group 1, and so must the turns
    plugin._registry().forget_person('10002', 'group:' + G1, note='legacy:test')
    result['lemon_turn_ids_before'] = sorted({x for t in turns_file() for x in t['recalled'] + t['held']})
    import types

    async def get_json(silent=True):
        return {'filename': 'b.zip', 'base64': backup}
    sys.modules['quart'] = types.SimpleNamespace(request=types.SimpleNamespace(get_json=get_json))
    result['restore'] = run(plugin.page_restore())
    turns = turns_file()
    lib = library_ids()
    result['private_turns'] = [t for t in turns if t['where'] == 'private:10001']
    result['unknown_ids'] = sorted({x for t in turns for x in t['recalled'] + t['held'] if x not in lib})
    result['search'] = {q: search(q) for q in ('吉他', '惊喜')}
    result['turns'] = len(turns)

for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), 'utf-8')
