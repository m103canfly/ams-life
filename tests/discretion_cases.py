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
NOW = clock.now  # her old replies were written within the last day, so the phone keeps them

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
                    'history': [{'ts': NOW - 3600, 'emotion': 'joy', 'v': 0.1, 'text': '爬山记得带水哦'}]},
                   ensure_ascii=False), 'utf-8')
    (DATA / 'states' / 'default_FriendMessage_10001.json').write_text(
        json.dumps({'v': 0.4, 'history': [{'ts': NOW - 7200, 'emotion': 'joy', 'v': 0.4, 'text': '蛋糕的事我帮你保密'}],
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
        'history': [{'ts': NOW - 3000, 'emotion': 'joy', 'v': 0.2, 'text': '蛋糕的事我帮你保密', 'origin': PRIVATE_ORIGIN},
                    {'ts': NOW - 2000, 'emotion': 'joy', 'v': 0.2, 'text': '爬山记得带水哦', 'origin': GROUP_ORIGIN},
                    {'ts': NOW - 1000, 'emotion': 'joy', 'v': 0.2, 'text': '不知道从哪来的一句话'}],
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


class Heard(harness.FakeEvent):
    """A message that only reaches on_message; counts anything done to the event."""
    done = {'send': 0, 'stop': 0, 'result': 0}

    def __init__(self, *a, parts=None, **k):
        super().__init__(*a, **k)
        self._parts = parts

    def get_messages(self):
        return self._parts if self._parts is not None else super().get_messages()

    async def send(self, chain):
        Heard.done['send'] += 1

    def stop_event(self):
        Heard.done['stop'] += 1

    def set_result(self, result):
        Heard.done['result'] += 1


def hear(plugin, loop, delay, text, sender, name, group=None, parts=None):
    """A message in a chat that does not wake her: AstrBot only calls on_message."""
    clock.advance(delay)
    event = Heard(text, sender=sender, name=name, group=group, parts=parts)
    loop.run_until_complete(plugin.on_message(event))
    harness.drain(loop)
    return event


def turn(plugin, loop, delay, text, sender, name, group=None, reply='嗯嗯', parts=None):
    clock.advance(delay)
    event = (Heard(text, sender=sender, name=name, group=group, parts=parts) if parts is not None
             else harness.FakeEvent(text, sender=sender, name=name, group=group))
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_message(event))  # AstrBot calls it for every message first
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
    harness.drain(loop)
    prompt = '\n'.join(p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts)
    return {'session': event.unified_msg_origin, 'prompt': prompt, 'refs': plugin._source_ids(event)}


def run():
    config = {}
    if CASE in ('forget', 'strong_event', 'consolidate', 'wait_event', 'wait_embed',
                'wait_archive', 'wait_consolidate', 'turn_event', 'summary_origin',
                'picture_event', 'picture_only'):  # summaries on, as in the golden 'full' run
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
    elif CASE == 'listen':
        t(0, '小爱 早上好', '10002', '柠檬', A, reply='早呀')
        core = plugin._core(None)
        calls = {'provider': 0, 'embed': 0, 'network': 0}
        real_provider, real_embed, real_net = plugin._provider_for, plugin._embed_text, plugin._ipv4_json

        async def count_provider(*a, **k):
            calls['provider'] += 1
            return await real_provider(*a, **k)

        async def count_embed(*a, **k):
            calls['embed'] += 1
            return await real_embed(*a, **k)

        def count_net(*a, **k):
            calls['network'] += 1
            return real_net(*a, **k)
        plugin._provider_for, plugin._embed_text, plugin._ipv4_json = count_provider, count_embed, count_net
        body_before = json.dumps(core.snapshot(), sort_keys=True)
        from astrbot.api.message_components import Image, Plain
        hear(plugin, loop, 0, '我家猫今天学会开冰箱了', '10003', '阿星', A)
        hear(plugin, loop, 0, '看', '10003', '阿星', A, parts=[Plain('看'), Image(url='x')])
        hear(plugin, loop, 0, '小爱你看过冰箱猫吗', '20002', '小爱', A)  # her own account: not stored here
        out['body_same'] = json.dumps(core.snapshot(), sort_keys=True) == body_before
        out['listen_calls'] = dict(calls)
        out['event_done'] = dict(Heard.done)
        plugin._provider_for, plugin._embed_text, plugin._ipv4_json = real_provider, real_embed, real_net
        t(30, '小爱 晚上好', '10004', '桃子', B)
        t(30, '小爱 在吗', '10001', '芒果')
        out['phone_heard'] = snapshot(plugin)['phone']
        out['forgot'] = plugin._forget(person='10003')
        out['phone_after_forget'] = snapshot(plugin)['phone']
        for i in range(1005):  # more than a window holds
            hear(plugin, loop, 1, '刷屏第%d条' % i, '10005', '路人', A)
        out['phone_full'] = snapshot(plugin)['phone']
        hear(plugin, loop, 23 * 3600, '快一天了', '10002', '柠檬', A)
        out['phone_23h'] = snapshot(plugin)['phone']
        hear(plugin, loop, 3600 + 60, '过了好久', '10002', '柠檬', A)
        out['phone_later'] = snapshot(plugin)['phone']
    elif CASE == 'wait_reply':
        # he says "forget me" while she is still waiting for the model's answer to him
        t(0, '小爱 早上好', '10002', '柠檬', A)
        event = harness.FakeEvent('小爱 我周末要去爬山', sender='10001', name='芒果', group=A)
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')

        async def one_message():  # AstrBot runs one message, request to reply, in one task
            await plugin.on_message(event)
            await plugin.on_llm_request(event, req)
            out['forgot'] = plugin._forget(person='10001')
            await plugin.on_llm_response(event, LLMResponse('爬山记得带水哦'))
        loop.run_until_complete(one_message())
        harness.drain(loop)
        out['after'] = snapshot(plugin)
    elif CASE == 'wait_lock':
        # his message is in (on_message), then waits for the session lock while she is still
        # answering the one before; meanwhile he says "forget me"
        t(0, '小爱 早上好', '10002', '柠檬', A)
        event = harness.FakeEvent('小爱 记得提醒我明天交报告', sender='10001', name='芒果', group=A)
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')

        async def one_message():  # AstrBot runs one message, in to reply, in one task
            await plugin.on_message(event)
            await asyncio.sleep(0)  # the session lock
            out['forgot'] = plugin._forget(person='10001')
            await plugin.on_llm_request(event, req)
            await plugin.on_llm_response(event, LLMResponse('好的，明天提醒你'))
        loop.run_until_complete(one_message())
        harness.drain(loop)
        out['after'] = snapshot(plugin)
    elif CASE == 'merge_event':
        # a strong event in group A, then a duplicate of it made of what 阿星 said there
        place = 'group:' + A
        plugin._begin_job()
        first = {'id': 'evt_a', 'ts': clock.now, 'session': 'default:GroupMessage:' + A,
                 'title': '周末去看海', 'event': '周末去看海', 'event_key': '周末去看海',
                 'source_texts': ['我们周末去看海吧'],
                 'provenance': {'sender_id': '10002', 'session': 'default:GroupMessage:' + A,
                                'message_refs': ['m_lemon'], 'sources': []},
                 'origin': main.discretion.make_origin(place, ['10002'], ['m_lemon'])}
        dup = {'id': 'evt_b', 'ts': clock.now + 60, 'session': 'default:GroupMessage:' + A,
               'title': '周末去看海', 'event': '周末去看海', 'event_key': '周末去看海2',
               'source_texts': ['看海我也要去，我带相机'],
               'provenance': {'sender_id': '10003', 'session': 'default:GroupMessage:' + A,
                              'message_refs': ['m_star'],
                              'sources': [{'sender_id': '10003', 'message_refs': ['m_star']}]},
               'origin': main.discretion.make_origin(place, ['10003'], ['m_star'])}
        plugin._append_event_archive(dict(first))
        plugin._merge_archive_duplicate(dict(first), dup)
        out['merged'] = snapshot(plugin)['events']
        out['merged_raw'] = [json.loads(x) for x in (DATA / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()
                             if x.strip()]
        out['forgot_by_id'] = plugin._forget(source_ids=['m_star'])
        out['after_by_id'] = snapshot(plugin)['events']
        plugin._begin_job()
        plugin._append_event_archive(dict(first))
        plugin._merge_archive_duplicate(dict(first), dup)
        out['forgot_person'] = plugin._forget(person='10003')
        out['after_person'] = snapshot(plugin)['events']
    elif CASE == 'cleanup_merge':
        # BioCore's one-time cleanup folds a poorer duplicate row into a richer one
        session = 'default:FriendMessage:10001'
        place = 'private:10001'
        rows = [{'id': 'evt_rich', 'ts': clock.now, 'session': session, 'summary_status': 'llm',
                 'title': '约好周六去看海', 'event': '约好周六去看海', 'event_key': '看海',
                 'source_texts': ['我们约好周六去看海'],
                 'origin': main.discretion.make_origin(place, ['10001'], ['m_one'])},
                {'id': 'evt_poor', 'ts': clock.now + 30, 'session': session,
                 'title': '约好周六去看海', 'event': '约好周六去看海', 'event_key': '看海2',
                 'source_texts': ['我们约好周六去看海', '记得带相机'],
                 'origin': main.discretion.make_origin(place, ['10001'], ['m_two'])}]
        (DATA / 'archives').mkdir(parents=True, exist_ok=True)
        (DATA / 'archives' / 'events.jsonl').write_text(
            ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), 'utf-8')
        out['merged_count'] = plugin._cleanup_duplicate_events(force=True)
        out['merged_raw'] = [json.loads(x) for x in (DATA / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()
                             if x.strip()]
        out['forgot'] = plugin._forget(source_ids=['m_two'])
        out['after'] = snapshot(plugin)['events']
    elif CASE == 'turn_event':
        # the per-turn archive makes an event of an older stretch (阿星's three lines);
        # the 27 later lines are 柠檬's small talk, too unimportant for an event
        place = 'group:' + A
        entries = []
        for i, text in enumerate(('我答应你以后一定去看海', '以后我们永远一起去看海，我承诺', '别害怕，我答应过你的')):
            entries.append({'id': 's%d' % i, 'text': text, 'role': 'user', 'ts': clock.now - 9000 + 10 * i,
                            'importance': 0.9, 'sender_id': '10003', 'vector': [],
                            'provenance': {'sender_id': '10003', 'session': 'default:GroupMessage:' + A,
                                           'ts': clock.now - 9000 + 10 * i, 'message_refs': ['m_star%d' % i]},
                            'origin': main.discretion.make_origin(place, ['10003'], ['m_star%d' % i])})
        for i in range(27):
            entries.append({'id': 'l%d' % i, 'text': '嗯嗯好', 'role': 'user', 'ts': clock.now - 3000 + 10 * i,
                            'importance': 0.1, 'sender_id': '10002', 'vector': [],
                            'provenance': {'sender_id': '10002', 'session': 'default:GroupMessage:' + A,
                                           'ts': clock.now - 3000 + 10 * i, 'message_refs': ['m_lemon%d' % i]},
                            'origin': main.discretion.make_origin(place, ['10002'], ['m_lemon%d' % i])})
        lemon = harness.FakeEvent('嗯嗯好', sender='10002', name='柠檬', group=A)
        plugin._begin_job()
        loop.run_until_complete(plugin._archive_ranked_events_deterministic(lemon, plugin._core(None), entries))
        out['events'] = snapshot(plugin)['events']
        out['events_raw'] = [json.loads(x) for x in (DATA / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()
                             if x.strip()]
        out['forgot'] = plugin._forget(person='10003')
        out['after'] = snapshot(plugin)['events']
    elif CASE in ('picture_event', 'picture_only'):
        # the per-turn archive makes an event of a stretch with pictures in it (海鸥 sends
        # them; a picture's caption is added to its text when the stretch is cut)
        place = 'group:' + A
        if CASE == 'picture_event':
            lines = [('10003', '我答应你以后一定去看海', ''),
                     ('10006', '我答应你一定去看海，你看这张海', '海边的日落，天空是橙色的海'),
                     ('10003', '别害怕，我答应过你的', '')]
        else:
            lines = [('10006', '我答应你以后一定去看海', '海边的日落，天空是橙色的'),
                     ('10006', '以后我们永远一起去看海，我承诺', '沙滩上的两串脚印'),
                     ('10006', '别害怕，我答应过你的', '一只海鸥站在礁石上')]

        def entries_now():
            entries = []
            for i, (sid, text, caption) in enumerate(lines):
                ts = clock.now - 9000 + 10 * i
                entries.append({'id': 'p%d' % i, 'text': text, 'image_caption': caption, 'role': 'user',
                                'ts': ts, 'importance': 0.9, 'sender_id': sid, 'vector': [],
                                'provenance': {'sender_id': sid, 'session': 'default:GroupMessage:' + A,
                                               'ts': ts, 'message_refs': ['m_pic%d' % i]},
                                'origin': main.discretion.make_origin(place, [sid], ['m_pic%d' % i])})
            for i in range(27):
                ts = clock.now - 3000 + 10 * i
                entries.append({'id': 'l%d' % i, 'text': '嗯嗯好', 'role': 'user', 'ts': ts,
                                'importance': 0.1, 'sender_id': '10002', 'vector': [],
                                'provenance': {'sender_id': '10002', 'session': 'default:GroupMessage:' + A,
                                               'ts': ts, 'message_refs': ['m_lemon%d' % i]},
                                'origin': main.discretion.make_origin(place, ['10002'], ['m_lemon%d' % i])})
            return entries
        lemon = harness.FakeEvent('嗯嗯好', sender='10002', name='柠檬', group=A)

        def archive():
            plugin._begin_job()
            loop.run_until_complete(plugin._archive_ranked_events_deterministic(
                lemon, plugin._core(None), entries_now()))
            return snapshot(plugin)['events']
        out['events'] = archive()
        out['forgot_by_id'] = plugin._forget(source_ids=['m_pic1'])
        out['after_by_id'] = snapshot(plugin)['events']
        clock.advance(10)
        out['events_again'] = archive()
        out['forgot_person'] = plugin._forget(person='10006')
        out['after_person'] = snapshot(plugin)['events']
    elif CASE == 'summary_origin':
        # one of the memories a summary is made of had another message merged into it earlier
        for delay, text in ((0, '小爱，我们群周末要去爬山'), (20, '我们群周末要去爬山，小爱'),
                            (20, '周末我们群要去爬山')):
            t(delay, text, '10002', '柠檬', A, reply='好呀')
        path = DATA / 'memory' / 'library.json'
        lib = json.loads(path.read_text('utf-8'))
        for e in lib['entries']:
            if e.get('text') == '周末我们群要去爬山':
                e['origin']['people'].append('10003')
                e['origin']['source_ids'].append('m_star')
        path.write_text(json.dumps(lib, ensure_ascii=False), 'utf-8')
        lemon = harness.FakeEvent('x', sender='10002', name='柠檬', group=A)
        plugin._begin_job()
        loop.run_until_complete(plugin._consolidate_memory(lemon, plugin._core(None), force=True))
        harness.drain(loop)
        lib = json.loads(path.read_text('utf-8'))
        out['summaries'] = [{'text': e.get('text'), 'origin': e.get('origin')} for e in lib['entries']
                            if e.get('role') == 'summary' or e.get('candidate_origin') == 'llm']
        out['forgot'] = plugin._forget(source_ids=['m_star'])
        lib = json.loads(path.read_text('utf-8'))
        out['after'] = [e.get('text') for e in lib['entries']]
    elif CASE == 'quote':
        # 芒果 quotes 柠檬's message; forgetting by message id finds each by its own id only
        first = t(0, '周末一起去爬山吧', '10002', '柠檬', A)
        from astrbot.api.message_components import Plain, Reply
        quoted_id = first['refs'][0]
        second = t(30, '小爱 这个我也想去', '10001', '芒果', A,
                   parts=[Reply(id=quoted_id), Plain('小爱 这个我也想去')])
        out['ids'] = {'first': first['refs'], 'second': second['refs']}
        out['before'] = snapshot(plugin)
        out['forgot_quoted'] = plugin._forget(source_ids=[quoted_id])
        out['after_quoted'] = snapshot(plugin)
        out['forgot_own'] = plugin._forget(source_ids=second['refs'])
        out['after_own'] = snapshot(plugin)
    elif CASE == 'sweep':
        # windows nobody writes to any more: their lines still leave the disk after 24 hours
        t(0, '小爱 早上好', '10002', '柠檬', A, reply='早呀')
        t(10, '小爱 晚上好', '10004', '桃子', B, reply='晚上好')
        t(10, '小爱 在吗', '10001', '芒果', reply='在的')
        out['disk_start'] = disk_phone()
        clock.advance(24 * 3600 + 60)
        out['disk_day_later'] = disk_phone()
        plugin._read_window('private:10001')  # reading a window writes it back pruned
        out['disk_after_read'] = disk_phone()
        import mixin_autonomy
        task = plugin._autonomy_task
        out['loop_running'] = bool(task is not None and not task.done())
        task.cancel()
        mixin_autonomy.AUTONOMY_TICK_SECONDS = 0.01

        async def ticks():  # the plugin's own 5-minute loop, run fast
            plugin._ensure_autonomy_task()
            await asyncio.sleep(0.2)
        loop.run_until_complete(ticks())
        out['disk_after_tick'] = disk_phone()
        plugin._autonomy_task.cancel()
        mixin_autonomy.AUTONOMY_TICK_SECONDS = 300
        hear(plugin, loop, 0, '有人吗', '10002', '柠檬', A)
        plugin._autonomy_task.cancel()
        clock.advance(24 * 3600 + 60)
        out['disk_before_start'] = disk_phone()
        main.BioCorePlugin(harness.FakeContext(), config=config)  # start-up sweeps too
        out['disk_after_start'] = disk_phone()
    elif CASE == 'mtrace':
        # a heavy recall in group A must not colour group B's turn, whose recall returns early
        t(0, '小爱 早上好', '10002', '柠檬', A)
        heavy = {'count': 3, 'valence': -0.8, 'stress_delta': 0.03, 'entry_ids': [], 'ts': clock.now}
        plugin._core(None)._last_memory_trace = dict(heavy)  # as if A had just recalled it
        plugin._last_memory_trace = dict(heavy)
        real_embed = plugin._embed_text

        async def no_vector(*a, **k):  # the vector service does not answer: recall returns early
            return []
        plugin._embed_text = no_vector
        out['b'] = t(30, '小爱 晚上好', '10004', '桃子', B)['prompt']
        plugin._embed_text = real_embed
    elif CASE in ('wait_event', 'wait_embed', 'wait_archive', 'wait_consolidate'):
        # he says "forget me" while a request of his is still waiting somewhere;
        # nothing that request (or the work it started) holds may be written back
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '芒果')
        for delay, text, tag in ((400, '小爱 我好难过 想哭', '{"e":"sadness","i":0.9}'),
                                 (20, '今天被骂了 真的很委屈', '{"e":"sadness","i":0.85}'),
                                 (20, '气死我了！！！他凭什么这样说我', '{"e":"anger","i":0.8}'),
                                 (30, '真的受够了！！！气死了！！！', '{"e":"anger","i":0.9}')):
            t(delay, text, '10001', '芒果', reply='我陪着你<bc>%s</bc>' % tag)
        t(30, '小爱，我们群周末要去爬山', '10002', '柠檬', A)
        armed, fired = [False], []  # armed right before the wait under test

        def forget_now():
            if armed[0]:
                armed[0] = False
                fired.append(plugin._forget(person='10001'))
        if CASE == 'wait_event':  # while the strong event waits for its summary (mixin_events strong path)
            real = plugin._provider_for

            async def provider(kind, event=None):
                inner = await real(kind, event)

                class Meanwhile:
                    async def text_chat(self, *a, **k):
                        if kind == 'event_summary':
                            forget_now()
                        return await inner.text_chat(*a, **k)
                return Meanwhile() if inner is not None else None
            plugin._provider_for = provider
        else:  # while the request waits for the vector service
            real_embed = plugin._embed_text

            real_embedding_for = plugin._embedding_for

            async def embed(*a, **k):
                forget_now()
                return await real_embed(*a, **k)

            async def embedding_for(*a, **k):
                forget_now()
                return await real_embedding_for(*a, **k)
            plugin._embed_text, plugin._embedding_for = embed, embedding_for
        mango = harness.FakeEvent('我还是好生气！！！凭什么啊！！！', sender='10001', name='芒果')
        clock.advance(620)
        if CASE in ('wait_archive', 'wait_consolidate'):  # events archived from memory entries
            for text in ('小爱 谢谢你 我答应你以后别难过了', '对不起 以后我永远喜欢你'):  # promise words
                t(30, text, '10001', '芒果')
            lib = plugin._read_library()  # as if said with strong feelings: worth an event
            for e in lib['entries']:
                if e.get('sender_id') == '10001':
                    e['importance'] = 0.9
            plugin._write_library(lib)
            plugin._last_event_archive = 0.0
            loop.run_until_complete(plugin.on_message(mango))
            armed[0] = True
            if CASE == 'wait_archive':  # the per-turn archive (mixin_events _maybe_archive_events)
                plugin._begin_job()  # as on_llm_request does before it starts this task
                loop.run_until_complete(plugin._maybe_archive_events(mango, plugin._core(None)))
            else:  # consolidation with nothing to group: it archives events instead
                loop.run_until_complete(plugin._consolidate_memory(mango, plugin._core(None), force=True))
            harness.drain(loop)
        else:
            loop.run_until_complete(plugin.on_message(mango))
            armed[0] = True
            loop.run_until_complete(plugin.on_llm_request(mango, ProviderRequest(prompt=mango.message_str,
                                                                              system_prompt='你是小爱。')))
            harness.drain(loop)
        out['fired'] = fired
        out['after'] = snapshot(plugin)
        out['self_model'] = json.loads((DATA / 'self_model.json').read_text('utf-8')) \
            if (DATA / 'self_model.json').exists() else {}
    elif CASE == 'interleave':
        # two groups, each with its own people; then one request in each, interleaved
        for delay, text, sender, name in ((0, '小爱，我们周末去爬山吧', '10002', '柠檬'),
                                          (10, '小爱，爬山我也去', '10003', '阿星'),
                                          (10, '小爱，周末爬山带零食', '10002', '柠檬'),
                                          (10, '小爱，爬山要早起', '10003', '阿星')):
            t(delay, text, sender, name, A)
        for delay, text, sender, name in ((10, '小爱，今晚一起唱歌吧', '10004', '桃子'),
                                          (10, '小爱，唱歌我也来', '10005', '路人'),
                                          (10, '小爱，唱歌要点几首', '10004', '桃子'),
                                          (10, '小爱，唱歌唱到几点', '10005', '路人')):
            t(delay, text, sender, name, B)
        real_hints = plugin._maybe_llm_hints

        async def slow_hints(*a, **k):  # each request waits after its recall, the other one runs
            for _ in range(5):
                await asyncio.sleep(0)
            return await real_hints(*a, **k)
        plugin._maybe_llm_hints = slow_hints
        clock.advance(30)
        ea = harness.FakeEvent('小爱，爬山的事定了吗', sender='10002', name='柠檬', group=A)
        eb = harness.FakeEvent('小爱，唱歌的事定了吗', sender='10004', name='桃子', group=B)
        ra = ProviderRequest(prompt=ea.message_str, system_prompt='你是小爱。')
        rb = ProviderRequest(prompt=eb.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(asyncio.gather(plugin.on_llm_request(ea, ra), plugin.on_llm_request(eb, rb)))
        harness.drain(loop)
        out['prompt_a'] = '\n'.join(p.get('text') for p in ra.extra_user_content_parts)
        out['prompt_b'] = '\n'.join(p.get('text') for p in rb.extra_user_content_parts)
    elif CASE == 'files':
        # window names the first phone code mapped to one file ("other_a_b.json")
        one, two = 'other:a:b', 'other:a_b'
        plugin._write_window(one, {'recent': [{'ts': clock(), 'role': 'user', 'text': '一号窗口的话'}],
                                   'open_loops': []})
        plugin._write_window(two, {'recent': [{'ts': clock(), 'role': 'user', 'text': '二号窗口的话'}],
                                   'open_loops': []})
        out['files'] = sorted(p.name for p in (DATA / 'phone').glob('*.json'))
        out['one'] = [x['text'] for x in plugin._read_window(one)['recent']]
        out['two'] = [x['text'] for x in plugin._read_window(two)['recent']]
        # a file that says it belongs to another window is not read
        path = plugin._window_file('group:7')
        path.write_text(json.dumps({'place': 'group:8', 'recent': [{'ts': clock(), 'role': 'user',
                                                                   'text': '别的窗口的话'}]}, ensure_ascii=False),
                        'utf-8')
        out['mismatch'] = plugin._read_window('group:7')['recent']
        out['places'] = plugin._window_places()
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


def disk_phone():
    """What the window files on disk hold, read raw (not through the plugin's pruning)."""
    out = {}
    for path in sorted((DATA / 'phone').glob('*.json')):
        win = json.loads(path.read_text('utf-8'))
        out[win.get('place')] = [x.get('text') for x in win.get('recent') or []]
    return out


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
