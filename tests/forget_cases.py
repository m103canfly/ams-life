"""Scripted runs for the forget wiring tests (step 1-3-2); prints a JSON result.

Run in a fresh interpreter (test_forget_wiring does this):
    PYTHONHASHSEED=0 python tests/forget_cases.py <empty data dir> <out.json> <case>

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
PICTURE = 'http://img.test/cat.jpg'


def vec(seed):
    return harness.fake_vector('seed%d' % seed)


def write(rel, obj):
    path = DATA / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if rel.endswith('.jsonl'):
        path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in obj), 'utf-8')
    else:
        path.write_text(json.dumps(obj, ensure_ascii=False), 'utf-8')


# ---------------------------------------------------------------- written before the plugin starts
if CASE == 'registered':
    import forget_registry
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')
        reg.forget_message('m-gone', 'group:' + G1, note='legacy:test')

if CASE == 'restore':
    # rows narrower than a whole delete: forgotten in one group only; an optout that ended
    import forget_registry
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        reg.forget_person('10003', 'group:' + G1, stamp=1.0, note='legacy:test')
        reg.opt_out('10004', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')
        reg.opt_in('10004', forget_registry.EVERYWHERE, stamp=2.0, note='legacy:test')

if CASE in ('migrate', 'recall_before', 'recall_after'):
    # a library as written before step 1-3: her replies without ids, the same words in two
    # groups sharing an id (a hash of the text), vectors in the JSON
    def entry(eid, text, role, where, who, seed, ts):
        e = {'text': text, 'role': role, 'vector': vec(seed), 'ts': clock.now - ts, 'hits': 1, 'importance': 0.6,
             'origin': {'where': where, 'people': [who], 'source_ids': [], 'visibility': 'public'}}
        if eid:
            e['id'] = eid
        return e
    write('memory/library.json', {'schema_version': 3, 'rooms': {}, 'entries': [
        entry('same', '早安呀大家', 'user', 'group:' + G1, '10002', 1, 900),
        entry('same', '早安呀大家', 'user', 'group:' + G2, '10004', 2, 800),
        entry('', '早安~', 'assistant', 'group:' + G1, '10002', 3, 700),
        entry('m9', '周末一起去爬山吧', 'user', 'group:' + G1, '10002', 4, 600),
        entry('', '好呀，爬山记得带水', 'assistant', 'group:' + G1, '10002', 5, 500)]})

if CASE == 'other_stores':
    write('memory/library.json', {'schema_version': 3, 'rooms': {}, 'entries': [
        {'id': 'pic1', 'text': '芒果发了一张猫的照片', 'role': 'user', 'vector': vec(1), 'ts': clock.now - 100,
         'attachments': [{'type': 'image', 'ref': PICTURE}],
         'origin': {'where': 'group:' + G1, 'people': ['10001'], 'source_ids': ['m-pic'], 'visibility': 'public'}},
        {'id': 'keep1', 'text': '柠檬说周末去爬山', 'role': 'user', 'vector': vec(2), 'ts': clock.now - 90,
         'origin': {'where': 'group:' + G1, 'people': ['10002'], 'source_ids': ['m-hike'], 'visibility': 'public'}}]})
    import hashlib
    write('image_cache.json', {hashlib.sha256(PICTURE.encode('utf-8')).hexdigest(): {
        'ref': PICTURE, 'caption': '一只橘猫趴在键盘上', 'ts': clock.now}})
    write('archives/events.jsonl', [
        {'id': 'evt_cat', 'title': '芒果的猫', 'event': '芒果发了猫的照片', 'ts': clock.now - 100,
         'origin': {'where': 'group:' + G1, 'people': ['10001'], 'source_ids': ['m-pic'], 'visibility': 'public'}},
        {'id': 'evt_hike', 'title': '爬山', 'event': '柠檬约爬山', 'ts': clock.now - 90,
         'origin': {'where': 'group:' + G1, 'people': ['10002'], 'source_ids': ['m-hike'], 'visibility': 'public'}}])
    write('archives/dedupe_log.jsonl', [
        {'action': 'dedupe_merge', 'kept_id': 'evt_cat', 'kept_title': '芒果的猫', 'dropped_id': 'evt_x'},
        {'action': 'dedupe_merge', 'kept_id': 'evt_hike', 'kept_title': '爬山', 'dropped_id': 'evt_y'}])
    write('users/10002.json', {'sender_id': '10002', 'sender_name': '柠檬', 'interactions': 7, 'trust': 0.6,
                               'relationship': {
                                   'state': {'trust': 0.6, 'closeness': 0.5},
                                   'trajectory': [{'ts': 1.0, 'trust': 0.6}],
                                   'we_memory': [{'type': 'ritual', 'text': '每周末一起爬山', 'confidence': 0.6}],
                                   'annotations': [{'kind': 'trait', 'text': '爱爬山', 'evidence_refs': ['keep1']},
                                                   {'kind': 'trait', 'text': '爱拍照', 'evidence_refs': ['other']}],
                                   'milestones': [{'type': 'first_meet', 'key': '第一次一起爬山',
                                                   'source_ids': ['m-hike']}],
                                   'transactive_map': {'爬山': 3}}})

if CASE == 'registry_broken':
    write('self_model.json', {'notebook': [{'id': 'n1', 'text': '今天群里很热闹', 'ts': clock.now - 50,
                                            'origin': {'where': 'self', 'people': [], 'source_ids': [],
                                                       'visibility': 'self'}}]})

if CASE == 'mention':
    # someone who has nothing to do with the person deleted: his number only inside a timestamp,
    # his (everyday) name only inside ordinary words
    write('users/10009.json', {'sender_id': '10009', 'sender_name': '路人甲', 'interactions': 3,
                               'relationship': {
                                   'state': {'trust': 0.5}, 'trajectory': [{'ts': 179310001.5, 'trust': 0.5}],
                                   'we_memory': [{'type': 'ritual', 'text': '哈哈哈每天打卡', 'confidence': 0.6}],
                                   'transactive_map': {'哈哈': 2, '打卡': 3}}})
    # records that draw from him only in a latest line or in evidence
    write('users/10011.json', {'sender_id': '10011', 'sender_name': '路人乙', 'interactions': 3,
                               'relationship': {'state': {'trust': 0.5}, 'destination_map': {
                                   '10002': {'sender_id': '10002', 'count': 1, 'latest_text': '刚才10001说他在学吉他'}}}})
    write('users/10012.json', {'sender_id': '10012', 'sender_name': '路人丙', 'interactions': 3,
                               'relationship': {'state': {'trust': 0.5}, 'social_world': [
                                   {'name': '同学', 'role': 'friend', 'evidence': [{'ts': 1.0, 'text': '我和10001一起上课'}]}]}})
    # someone whose record does draw from him
    write('users/10002.json', {'sender_id': '10002', 'sender_name': '柠檬', 'interactions': 3,
                               'relationship': {
                                   'state': {'trust': 0.5},
                                   'destination_map': {'10001': {'sender_id': '10001', 'sender_name': '哈哈', 'count': 2}},
                                   'transactive_map': {'吉他': 2}}})

if CASE == 'migrate_many':
    write('memory/library.json', {'schema_version': 3, 'rooms': {}, 'entries': [
        {'text': '回复 %d' % i, 'role': 'assistant', 'vector': vec(i), 'ts': clock.now - 1000 + i,
         'origin': {'where': 'group:' + G1, 'people': ['10002'], 'source_ids': [], 'visibility': 'public'}}
        for i in range(30)]})

import main  # noqa: E402
if CASE == 'migrate_many':
    _reads = {'n': 0}
    _read = main.BioCorePlugin._read_library

    def _counting(self, vectors=True):
        _reads['n'] += 1
        return _read(self, vectors)
    main.BioCorePlugin._read_library = _counting
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402


class FakeConversations:
    def __init__(self):
        self.deleted = []
        self.histories = {'default:GroupMessage:' + G1: [{'role': 'user', 'content': 'first'}],
                          'default:GroupMessage:' + G2: [{'role': 'user', 'content': 'second'}]}
        self.fail = False

    async def get_curr_conversation_id(self, umo):
        return umo if umo in self.histories else None

    async def update_conversation(self, umo, conversation_id=None, history=None):
        if self.fail:
            raise RuntimeError('synthetic failure')
        assert conversation_id == umo
        self.histories[umo] = history

    async def delete_conversations_by_user_id(self, umo):
        self.deleted.append(umo)


class FakeHistory:
    def __init__(self):
        self.rows = [type('Row', (), {'id': i, 'sender_id': s})() for i, s in
                     enumerate(['10001', '10002', '10001', '10004'])]
        self.deleted = []

    async def get(self, platform_id, user_id, page=1, page_size=200):
        start = (page - 1) * page_size
        return self.rows[start:start + page_size]

    async def delete_by_id(self, message_id):
        self.deleted.append(message_id)
        self.rows = [r for r in self.rows if r.id != message_id]


ctx = harness.FakeContext()
ctx.conversation_manager = FakeConversations()
ctx.message_history_manager = FakeHistory()
if CASE == 'recall_before':
    main.BioCorePlugin._migrate_memory_ids = lambda self: None   # the old layout, as it was
plugin = main.BioCorePlugin(ctx, config={'owner_qq': '10001', 'reply_private': ['10002', '10003', '10004', '10005', '10006']})
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
        return None
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
    harness.drain(loop)
    return '\n'.join(p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts)


def all_text():
    """Every data file as text (the vector store and registry are binary: their ids only)."""
    out = {}
    for path in sorted(p for p in DATA.rglob('*') if p.is_file()):
        rel = path.relative_to(DATA).as_posix()
        if path.suffix == '.sqlite3' or '/archive/' in '/' + rel:
            continue
        out[rel] = path.read_text('utf-8', errors='replace')
    return out


def library():
    return json.loads((DATA / 'memory' / 'library.json').read_text('utf-8'))


result = {}

if CASE == 'registered':
    turn('今天的晚霞好漂亮', '10003', '阿星', group=G1, reply='是呀好漂亮~', msg_id='m-star-1')
    turn('这条后来被要求忘掉了', '10002', '柠檬', group=G1, reply='嗯嗯', msg_id='m-gone')
    turn('小爱 周末去爬山吗', '10002', '柠檬', group=G1, reply='好呀~', msg_id='m-hike')
    result['files'] = all_text()
    result['users'] = sorted(p.name for p in (DATA / 'users').glob('*.json')) if (DATA / 'users').exists() else []

if CASE in ('group_missing_api', 'group_update_error'):
    turn('hello', '10001', 'Person A', group=G1, reply='hello', msg_id='m-one')
    if CASE == 'group_missing_api':
        ctx.conversation_manager.update_conversation = None
    else:
        ctx.conversation_manager.fail = True
    result['answer'] = loop.run_until_complete(plugin.page_forget_person('10001'))
    result['after'] = all_text()
    with plugin._registry() as reg:
        result['registry'] = reg.rows()
    result['history'] = ctx.conversation_manager.histories['default:GroupMessage:' + G1]

if CASE in ('owner_person', 'owner_memory'):
    turn('小爱 我最近在学弹吉他', '10001', '芒果', group=G1, reply='好厉害！', msg_id='m-guitar')
    turn('小爱 周末去爬山吗', '10002', '柠檬', group=G1, reply='好呀，记得带水~', msg_id='m-hike')
    turn('小爱，跟你说个悄悄话，我在准备一个惊喜', '10001', '芒果', reply='我帮你保密~', msg_id='m-secret')
    turn('小爱 晚上好', '10004', '桃子', group=G2, reply='晚上好呀', msg_id='m-hi')
    result['before'] = all_text()
    if CASE == 'owner_person':
        out = loop.run_until_complete(plugin.page_forget_person('10001'))
        result['answer'] = out
        result['after'] = all_text()
        result['astrbot'] = {'conversations': ctx.conversation_manager.deleted,
                             'history_left': [r.sender_id for r in ctx.message_history_manager.rows],
                             'group_histories': ctx.conversation_manager.histories}
        turn('小爱 我又回来啦 还在学吉他', '10001', '芒果', group=G1, reply='欢迎回来', msg_id='m-back')
        result['later'] = all_text()
        bad = loop.run_until_complete(plugin.page_forget_person('芒果'))
        result['bad_person'] = bad
    else:
        lib = library()
        target = next(e for e in lib['entries'] if e.get('text', '').startswith('小爱 周末去爬山'))
        result['target_id'] = target['id']
        result['answer'] = loop.run_until_complete(plugin.page_memory_delete('library', target['id']))
        result['after'] = all_text()
        result['missing'] = loop.run_until_complete(plugin.page_memory_delete('library', 'no-such-id'))
    import forget_registry
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        result['registry'] = [{k: r[k] for k in ('kind', 'place', 'qq', 'source_id', 'note')} for r in reg.rows()]

if CASE == 'chat_commands':
    turn('小爱 周末一起去爬山吧', '10002', '柠檬', group=G1, reply='好呀~', msg_id='m-hike')
    before = [e['text'] for e in library()['entries']]
    injects = []
    for i, text in enumerate(['小爱 删除记忆 周末一起去爬山', '确认删除', '小爱 撤销修改', '小爱 恢复记忆',
                              '小爱 回滚', '小爱 其实是周日去爬山 改成周日']):
        injects.append(turn(text, '10002', '柠檬', group=G1, reply='嗯？', msg_id='m-cmd-%d' % i))
    turn('小爱 忘掉我说的', '10005', '路人', reply='嗯？', msg_id='m-cmd-private')
    after = library()['entries']
    result['before'] = before
    result['after'] = [e['text'] for e in after]
    result['deleted_flags'] = [e for e in after if e.get('deleted')]
    result['injects'] = injects

if CASE == 'same_words':
    turn('小爱 早安呀', '10002', '柠檬', group=G1, reply='早安~', msg_id='m-a')
    turn('小爱 早安呀', '10004', '桃子', group=G2, reply='早安~', msg_id='m-b')
    entries = library()['entries']
    result['entries'] = [{'id': e.get('id'), 'text': e.get('text'), 'role': e.get('role'),
                          'where': (e.get('origin') or {}).get('where'),
                          'source_ids': (e.get('origin') or {}).get('source_ids'),
                          'has_vector_in_json': bool(e.get('vector'))} for e in entries]
    store = plugin._vector_store()
    result['stored'] = sorted(store.ids())

if CASE == 'migrate':
    entries = library()['entries']
    result['ids'] = [e.get('id') for e in entries]
    result['vectors_in_json'] = sum(1 for e in entries if e.get('vector'))
    result['archive'] = sorted(p.name.split('-')[0] for p in (DATA / 'memory' / 'archive').glob('*.json'))
    back = plugin._read_library()['entries']
    result['vectors_back'] = [e.get('vector') == vec(i + 1) for i, e in enumerate(back)]
    plugin2 = main.BioCorePlugin(ctx, config={})    # starting again changes nothing
    result['archive_again'] = len(list((DATA / 'memory' / 'archive').glob('*.json')))
    result['ids_again'] = [e.get('id') for e in library()['entries']]

if CASE in ('recall_before', 'recall_after'):
    result['inject'] = turn('小爱 周末爬山还去吗', '10002', '柠檬', group=G1, reply='去呀', msg_id='m-ask')

if CASE == 'other_stores':
    loop.run_until_complete(plugin.page_forget_person('10001'))
    result['image_cache'] = json.loads((DATA / 'image_cache.json').read_text('utf-8'))
    result['dedupe'] = (DATA / 'archives' / 'dedupe_log.jsonl').read_text('utf-8')
    lib = library()
    keep = next(e for e in lib['entries'] if e['id'] == 'keep1')
    result['by_message'] = loop.run_until_complete(plugin.page_memory_delete('library', 'keep1'))
    result['user_10002'] = json.loads((DATA / 'users' / '10002.json').read_text('utf-8'))
    result['events'] = (DATA / 'archives' / 'events.jsonl').read_text('utf-8')
    result['vector_ids'] = sorted(plugin._vector_store().ids())

if CASE == 'registry_broken':
    turn('小爱 周末去爬山吗', '10002', '柠檬', group=G1, reply='好呀~', msg_id='m-hike')
    turn('小爱 我在学吉他', '10001', '芒果', group=G1, reply='好厉害', msg_id='m-guitar')
    before_lib = library()['entries']
    before_vec = sorted(plugin._vector_store().ids())
    import sqlite3

    def broken():
        raise sqlite3.OperationalError('database is locked')
    plugin._registry_sets = broken                      # the registry cannot be read
    turn('小爱 今天吃什么', '10004', '桃子', group=G1, reply='吃火锅~', msg_id='m-food')
    plugin._save_self_model()
    loop.run_until_complete(plugin._remember(harness.FakeEvent('x', sender='10004', name='桃子', group=G1),
                                             '这是新的一条记忆内容', 'user'))
    harness.drain(loop)
    after_lib = library()['entries']
    result['before'] = sorted(e['text'] for e in before_lib)
    result['after'] = sorted(e['text'] for e in after_lib)
    result['vectors'] = (before_vec, sorted(plugin._vector_store().ids()))
    result['notebook'] = [x['text'] for x in json.loads((DATA / 'self_model.json').read_text('utf-8')).get('notebook') or []]
    result['phone_food'] = '今天吃什么' in ''.join(all_text().values())

if CASE == 'mention':
    turn('小爱 我在学吉他', '10001', '哈哈', group=G1, reply='好厉害', msg_id='m-guitar')
    before = (DATA / 'users' / '10009.json').read_text('utf-8')
    loop.run_until_complete(plugin.page_forget_person('10001'))
    result['untouched'] = (DATA / 'users' / '10009.json').read_text('utf-8') == before
    result['user_10002'] = json.loads((DATA / 'users' / '10002.json').read_text('utf-8'))['relationship']
    for who in ('10011', '10012'):
        result['user_' + who] = json.loads((DATA / 'users' / (who + '.json')).read_text('utf-8'))['relationship']

if CASE == 'forget_broken':
    turn('小爱 周末去爬山吗', '10002', '柠檬', group=G1, reply='好呀~', msg_id='m-hike')   # what is left is checked
    turn('小爱 我在学吉他', '10001', '芒果', group=G1, reply='好厉害', msg_id='m-guitar')
    import sqlite3
    real = plugin._registry_sets

    def broken():
        raise sqlite3.OperationalError('database is locked')
    plugin._registry_sets = broken                      # read right after the row is written
    result['page'] = loop.run_until_complete(plugin.page_forget_person('10001'))
    result['still_there'] = any('吉他' in e['text'] for e in library()['entries'])
    plugin._registry_sets = real
    result['retry'] = loop.run_until_complete(plugin.page_forget_person('10001'))['status']
    result['gone_after_retry'] = not any('吉他' in e['text'] for e in library()['entries'])

if CASE == 'restore':
    turn('小爱 我在学吉他', '10001', '芒果', group=G1, reply='好厉害', msg_id='m-guitar')
    turn('小爱 周末去爬山吗', '10002', '柠檬', group=G1, reply='好呀~', msg_id='m-hike')
    turn('小爱 我做了蛋糕', '10002', '柠檬', group=G1, reply='看起来好好吃', msg_id='m-cake')
    turn('小爱 今天下雨了', '10003', '阿星', group=G2, reply='记得带伞', msg_id='m-rain')
    turn('小爱 我回来啦', '10004', '桃子', group=G2, reply='欢迎回来', msg_id='m-back')
    backup = loop.run_until_complete(plugin.page_backup())['data']['base64']
    loop.run_until_complete(plugin.page_forget_person('10001'))                 # the owner deletes a person
    hike = next(e for e in library()['entries'] if e.get('text', '').startswith('小爱 周末去爬山'))
    loop.run_until_complete(plugin.page_memory_delete('library', hike['id']))   # ... and one memory
    import types

    async def get_json(silent=True):
        return {'filename': 'b.zip', 'base64': backup}
    sys.modules['quart'] = types.SimpleNamespace(request=types.SimpleNamespace(get_json=get_json))
    result['restore'] = loop.run_until_complete(plugin.page_restore())
    texts = [e['text'] for e in library()['entries']]
    result['guitar'] = any('吉他' in t for t in texts)
    result['hike'] = any('爬山' in t for t in texts)
    result['kept'] = {w: any(w in t for t in texts) for w in ('蛋糕', '下雨', '我回来啦')}
    result['users'] = {who: (DATA / 'users' / (who + '.json')).exists() for who in ('10002', '10003', '10004')}
    result['user_10001'] = (DATA / 'users' / '10001.json').exists()
    result['phone_guitar'] = '吉他' in ''.join(all_text().values())
    import forget_registry
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        result['registry'] = sorted((r['kind'], r['qq']) for r in reg.rows())

if CASE == 'old_endpoints':
    result['routes'] = [r for r in ctx.web_routes if 'memory/rollback' in r or 'memory/restore' in r]
    result['backup_restore_kept'] = any(r.endswith('/page/restore') for r in ctx.web_routes)
    result['methods'] = [m for m in ('page_memory_rollback', 'page_memory_restore') if hasattr(plugin, m)]

if CASE == 'picture':
    import forget_registry
    with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
        reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')

    async def describe(sender):
        plugin._begin_job()
        plugin._check_registry(harness.FakeEvent('[图片]', sender=sender, name='x', group=G1))
        plugin._save_image_cache({'k-' + sender: {'ref': 'http://img.test/' + sender, 'caption': '一只猫', 'ts': 1.0}})
    loop.run_until_complete(describe('10003'))
    result['blocked'] = (DATA / 'image_cache.json').exists()
    loop.run_until_complete(describe('10002'))
    result['allowed'] = sorted(json.loads((DATA / 'image_cache.json').read_text('utf-8')))

if CASE == 'migrate_many':
    result['reads_at_start'] = _reads['n']
    ids = [e.get('id') for e in library()['entries']]
    result['ids'] = (len(ids), len(set(ids)), all(ids))

for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), 'utf-8')
