"""Scripted runs for the no-numbers tests (step 1-3-5); prints a JSON result.

Run in a fresh interpreter (test_no_numbers does this):
    PYTHONHASHSEED=0 python tests/numbers_cases.py <empty data dir> <out.json> <case>

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
HER = '20002'

import forget_registry  # noqa: E402
with forget_registry.ForgetRegistry(DATA / forget_registry.FILE_NAME) as reg:
    reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=1.0, note='legacy:test')

import main  # noqa: E402
from astrbot.api.message_components import At, Plain  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

ctx = harness.FakeContext()
plugin = main.BioCorePlugin(ctx, config={})
plugin._ipv4_json = harness.fake_ipv4_json
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class Event(harness.FakeEvent):
    """A message as AstrBot hands it over: its parts, and message_str as AstrBot writes it."""

    def __init__(self, parts, message_str, sender, name, group=G1, msg_id=None):
        super().__init__(message_str, sender=sender, name=name, group=group, self_id=HER)
        self._parts = parts
        self.message_obj.message_id = msg_id or 'm-%s-%d' % (sender, int(clock.now))

    def get_messages(self):
        return self._parts


def turn(parts, message_str, sender, name, reply=None, advance=60):
    clock.advance(advance)
    event = Event(parts, message_str, sender, name)
    loop.run_until_complete(plugin.on_message(event))
    harness.drain(loop)
    if reply is not None:
        req = ProviderRequest(prompt=message_str, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
        harness.drain(loop)


def phone():
    return [x['text'] for x in plugin._read_window('group:' + G1)['recent']]


def library():
    return [e['text'] for e in plugin._read_library(vectors=False)['entries']]


result = {}

if CASE == 'at':
    turn([At(qq=HER, name='小爱bot'), Plain(text=' 你好呀')], '你好呀', '10002', '柠檬')
    turn([Plain(text='问问 '), At(qq='10004', name='桃子'), Plain(text=' 在吗')], '问问 @桃子(10004) 在吗',
         '10002', '柠檬')
    turn([At(qq='10005', name=''), Plain(text=' 快来')], '@(10005) 快来', '10002', '柠檬')
    turn([Plain(text='我的号是 10002 加我 游戏里的分是 123456')], '我的号是 10002 加我 游戏里的分是 123456',
         '10002', '柠檬')
    turn([At(qq='10003', name='阿星'), Plain(text=' 阿星你还在吗')], '@阿星(10003) 阿星你还在吗', '10002', '柠檬')
    turn([Plain(text='阿星昨天也这么说')], '阿星昨天也这么说', '10004', '桃子')
    # a request: what she remembers of it, her open loops
    turn([At(qq=HER, name='小爱bot'), Plain(text=' 记得提醒我 @桃子(10004) 明天要还我书 我号 10002')],
         '记得提醒我 @桃子(10004) 明天要还我书 我号 10002 @小爱bot(20002)', '10002', '柠檬', reply='好的，我记住啦')
    result['phone'] = phone()
    result['library'] = library()
    result['loops'] = [x.get('text') for x in plugin._read_window('group:' + G1).get('open_loops') or []]

if CASE == 'redline':
    turn([Plain(text='小爱 我最近失眠好严重 每天都睡不着')], '小爱 我最近失眠好严重 每天都睡不着', '10002', '柠檬',
         reply='抱抱你')
    turn([Plain(text='小爱 我周末想去海边看日落')], '小爱 我周末想去海边看日落', '10002', '柠檬', reply='好呀')
    result['phone'] = phone()
    result['library'] = library()

if CASE == 'migrate':
    # kept before this change: numbers in the library, her phone and a relationship record
    plugin._write_window('group:' + G1, {'recent': [
        {'ts': clock.now, 'role': 'user', 'sender_id': '10002', 'sender_name': '柠檬', 'msg_id': 'a1',
         'text': '@桃子(10004) 明天见 我号 10002', 'origin': {'where': 'group:' + G1, 'people': ['10002'],
                                                          'source_ids': ['a1'], 'visibility': 'public'}},
        {'ts': clock.now, 'role': 'user', 'sender_id': '10004', 'sender_name': '桃子', 'msg_id': 'a2',
         'text': '@阿星(10003) 你还在吗', 'origin': {'where': 'group:' + G1, 'people': ['10004'],
                                                 'source_ids': ['a2'], 'visibility': 'public'}}]})
    lib = plugin._read_library(vectors=False)
    lib['entries'].append({'id': 'x1', 'text': '@桃子(10004) 明天见 我号 10002', 'role': 'user', 'ts': clock.now,
                           'sender_id': '10002',
                           'origin': {'where': 'group:' + G1, 'people': ['10002'], 'source_ids': ['a1'],
                                      'visibility': 'public'}})
    (DATA / 'memory').mkdir(exist_ok=True)
    (DATA / 'memory' / 'library.json').write_text(json.dumps(lib, ensure_ascii=False), 'utf-8')
    (DATA / 'users').mkdir(exist_ok=True)
    (DATA / 'users' / '10002.json').write_text(json.dumps({
        'sender_id': '10002', 'sender_name': '柠檬', 'relationship': {'destination_map': {
            '10004': {'sender_id': '10004', 'count': 1, 'latest_text': '@桃子(10004) 明天见'}}}},
        ensure_ascii=False), 'utf-8')
    plugin._name_index = None
    result['counts'] = plugin._migrate_numbers()
    result['again'] = plugin._migrate_numbers()
    result['phone'] = phone()
    result['library'] = library()
    rel = json.loads((DATA / 'users' / '10002.json').read_text('utf-8'))['relationship']
    result['user'] = rel['destination_map']['10004']
    archive = DATA / 'memory' / 'archive'
    result['archived'] = sorted(p.relative_to(archive).as_posix().split('/')[0].split('-')[0]
                                for p in archive.rglob('*') if p.is_file())
    result['ids_kept'] = [x['sender_id'] for x in plugin._read_window('group:' + G1)['recent']]

for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), 'utf-8')
