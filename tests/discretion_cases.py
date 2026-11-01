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
                                         'sender_id': '10001', 'sender_name': '阿橙', 'vector': [], 'ts': 1.0,
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

if CASE == 'old_body':
    # her state and self model as written before step 1-2 (electronic-ghost body, her own heart)
    (DATA / 'states').mkdir(parents=True)
    (DATA / 'states' / 'her.json').write_text(json.dumps({
        'v': 0.2, 'a': 0.5, 'trust': 0.81, 'circadian_alertness': 0.3, 'user_trust_seeded': True,
        'user_trust_seed_delta': 0.01, 'boredom': 0.2,
        'reflection_tree': {'roots': [{'ts': 1.0, 'insight': '被认真对待会安心', 'children': []}], 'count': 1},
        'homeostasis': {'drives': {'energy': 0.7, 'social': 0.6, 'safety': 0.5, 'curiosity': 0.4},
                        'body': {'energy': 0.7, 'hydration': 0.5, 'warmth': 0.6, 'fatigue': 0.3},
                        'need_pyramid': {'dominant': 'belonging'}, 'interoception': {'label': 'low'},
                        'last_metabolic_cost': 0.02, 'readiness': 0.5}}, ensure_ascii=False), 'utf-8')
    (DATA / 'self_model.json').write_text(json.dumps({
        'who_am_i': '一个会持续受聊天影响、但不会被单条消息完全定义的角色。',
        'boundaries': ['不接受被当作没有感受的工具', '不会被一次互动改写全部立场', '主人写的一条边界'],
        'consistency': ['情绪会变，但核心立场不因单次互动翻转'],
        'narrative': '阿橙在准备惊喜', 'narrative_items': [{'text': '阿橙在准备惊喜', 'origin': {}}],
        'diary': [{'text': '今天的日记'}], 'version': 3,
        '_history': [{'who_am_i': 'x', 'narrative': '阿橙在准备惊喜'}]}, ensure_ascii=False), 'utf-8')

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
        'autobiography': [{'key': 'k', 'title': '惊喜蛋糕', 'meaning': '阿橙在准备惊喜'}],
        'self_timeline': {'past': ['惊喜蛋糕'], 'present': '阿橙在准备惊喜', 'future': []},
        'core_self': '惊喜蛋糕', 'narrative_self': '阿橙在准备惊喜',
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
        self.is_at_or_wake_command = False

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
    event.is_at_or_wake_command = True  # a turn is a message that wakes her
    req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
    loop.run_until_complete(plugin.on_message(event))  # AstrBot calls it for every message first
    loop.run_until_complete(plugin.on_llm_request(event, req))
    harness.drain(loop)
    loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(reply)))
    harness.drain(loop)
    prompt = '\n'.join(p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts)
    sent, kept = harness.astrbot_user_message(req)
    return {'session': event.unified_msg_origin, 'prompt': prompt, 'refs': plugin._source_ids(event),
            'sent': [b.get('text') for b in sent], 'history': [b.get('text') for b in kept]}


def run():
    config = {}
    if CASE in ('forget', 'strong_event', 'consolidate', 'wait_event', 'wait_embed',
                'wait_archive', 'wait_consolidate', 'turn_event', 'summary_origin',
                'picture_event', 'picture_only', 'strong_no_narrative', 'prompt_shape'):  # summaries on, as in the golden 'full' run
        config = {'llm_only_reply_summary': False, 'memory_worthiness_enabled': False}
    if CASE.startswith('global_'):   # step 2: one memory everywhere, labelled
        config = {'global_memory': True}
    config.update(owner_qq='10001', reply_private=['10002', '10003', '10004', '10005'])
    if CASE == 'listen':
        config['reply_groups'] = [A, B]
    plugin = main.BioCorePlugin(harness.FakeContext(), config=config)
    plugin._ipv4_json = harness.fake_ipv4_json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    out = {'turns': []}
    t = lambda *a, **k: out['turns'].append(turn(plugin, loop, *a, **k)) or out['turns'][-1]  # noqa: E731

    if CASE == 'keep_in_group':
        import impressions
        async def fake_vectors(text, *args, **kwargs):
            return harness.fake_vector(text)
        plugin._embed_text = fake_vectors
        hear(plugin, loop, 0, '较早以前的消息', '10001', '甲', A)
        hear(plugin, loop, 121, '第四条不应收窄', '10001', '甲', A)
        secret = hear(plugin, loop, 1, '青柠七号是今晚的暗号', '10001', '阿橙', A)
        loop.run_until_complete(plugin._remember(secret, secret.message_str, 'user', plugin._core(secret)))
        sid = plugin._source_ids(secret)
        origin = plugin._event_origin(secret)
        main.EVENT_ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        main.EVENT_ARCHIVE_PATH.write_text(json.dumps({'id': 'event1', 'origin': origin}) + '\n', 'utf-8')
        plugin.self_model['notebook'] = [{'text': '一条笔记', 'origin': dict(origin)}]
        plugin._save_self_model()
        store = plugin._impression_store()
        data = store.load('group:' + A)
        data['people']['10002'] = dict(impressions._record('group:' + A, '10002'), name='柠檬')
        store.save('group:' + A, data)
        hear(plugin, loop, 1, '第二个前文', '10001', '甲', A)
        hear(plugin, loop, 1, '另一个人的消息', '10002', '乙', A)
        hear(plugin, loop, 1, '另一个群的消息', '10001', '甲', B)
        hear(plugin, loop, 1, '第三个前文', '10001', '甲', A)
        marked = hear(plugin, loop, 1, '这件事别外传', '10001', '甲', A)
        loop.run_until_complete(plugin._remember(marked, marked.message_str, 'user', plugin._core(marked)))
        out['phone'] = plugin._read_window('group:' + A)['recent']
        out['other_phone'] = plugin._read_window('group:' + B)['recent']
        out['memory'] = plugin._read_library()['entries']
        out['event'] = json.loads(main.EVENT_ARCHIVE_PATH.read_text('utf-8').splitlines()[0])
        out['note'] = plugin.self_model['notebook'][0]
        out['source_ids'] = sid
        out['marked_ids'] = plugin._source_ids(marked)
        other_impression = store.load('group:' + A)['people']['10002']
        out['other_impression'] = other_impression
        out['other_impression_elsewhere'] = impressions.view(other_impression, 'group:' + A,
                                                             'group:' + B, present_here=True)
        out['labels'] = {place: main.discretion.label(plugin._event_origin(marked), place, '10001')['may']
                         for place in ('group:' + A, 'group:' + B, 'private:10001', 'private:10002')}
        relation = {'relationship': {'we_memory': [{'text': '一件旧事'}], 'transactive_map': {'旧话题': 1}}}
        out['private_user_view'] = plugin._user_view(harness.FakeEvent('问候', sender='10001'), relation)
        for phrase in main.discretion.NOT_KEEP_IN_GROUP_PHRASES:
            hear(plugin, loop, 1, phrase, '10003', '丙', A)
        out['negated'] = plugin._read_window('group:' + A)['recent'][-len(main.discretion.NOT_KEEP_IN_GROUP_PHRASES):]
        day_lines = plugin._read_window('group:' + A)['recent']
        item = {'title': '代号', 'what': '一件群里的事'}
        out['digest'] = plugin._digest_event('group:' + A, 'group:' + A, item, {}, day_lines,
                                              ['10001'], sid, False, clock.now)
        import time
        day = time.strftime('%Y-%m-%d', time.localtime(clock.now))
        impression_lines = [dict(lines, ts=clock.now + i) for i, lines in enumerate(
            [next(x for x in day_lines if x['text'] == secret.message_str)] * 12)]
        async def empty_answer(prompt):
            return '{}'
        store = plugin._impression_store()
        loop.run_until_complete(impressions.nightly(store, 'group:' + A, impression_lines, empty_answer, day))
        rec = store.load('group:' + A)['people']['10001']
        out['impression'] = rec
        out['impression_elsewhere'] = impressions.view(rec, 'group:' + A, 'private:10001')
        clock.advance(1801)  # the speaker's earlier line in group B is no longer present
        plugin.global_memory = True
        ask = harness.FakeEvent('最近怎么样', sender='10004', name='丁', group=B)
        out['present'] = sorted(plugin._present_people(ask))
        out['without_recall'] = list(plugin._check_note(ask)['forbidden'])
        original = next(x for x in out['memory'] if sid[0] in x['origin']['source_ids'])
        real_score = plugin._memory_score
        plugin._memory_score = lambda core, entry, cosine: 1.0
        out['recalled'] = plugin._labeled_elsewhere(ask, original['vector'], plugin._core(ask), [])
        plugin._memory_score = real_score
        async def no_vectors(text, *args, **kwargs):
            return None
        plugin._embed_text = no_vectors
        out['name_check'] = loop.run_until_complete(plugin._check_reply(ask, '阿橙最近好像挺忙的'))
        out['check'] = loop.run_until_complete(plugin._check_reply(ask, '青柠七号是今晚的暗号'))
        out['forbidden'] = plugin._check_note(ask)['forbidden']
        response = LLMResponse('青柠七号是今晚的暗号')
        out['sent'] = loop.run_until_complete(plugin._look_at_reply(ask, response, response.completion_text))
        plugin.global_memory = False
        hear(plugin, loop, 0, '恰好两分钟前', '10005', '戊', '900003')
        hear(plugin, loop, 120, '保密', '10005', '戊', '900003')
        out['boundary'] = plugin._read_window('group:900003')['recent'][0]['origin']
        calls = []
        async def look(event, response, reply):
            calls.append('look')
            return reply
        plugin._look_at_reply = look
        plugin._note_allowed = lambda *args: calls.append('allowed')
        plugin._settle_history = lambda *args: calls.append('history')
        plain = harness.FakeEvent('随便聊聊', sender='10004', name='丁', group=B)
        request = ProviderRequest(prompt=plain.message_str, system_prompt='小爱')
        loop.run_until_complete(plugin.on_message(plain))
        loop.run_until_complete(plugin.on_llm_request(plain, request))
        answer = LLMResponse('阿橙最近好像挺忙的')
        loop.run_until_complete(plugin.on_llm_response(plain, answer))
        loop.run_until_complete(plugin.on_agent_done(plain, object(), answer))
        harness.drain(loop)
        out['off_calls'] = calls
        out['off_reply'] = answer.completion_text
        async def epochs():
            ready_a, ready_b, release = asyncio.Event(), asyncio.Event(), asyncio.Event()
            async def waiting(place, ready):
                plugin._begin_job(place)
                ready.set()
                await release.wait()
                return plugin._job_stale()
            a = asyncio.create_task(waiting('group:' + A, ready_a))
            b = asyncio.create_task(waiting('group:' + B, ready_b))
            await ready_a.wait()
            await ready_b.wait()
            plugin._narrow_group_sources('group:' + A, sid)
            release.set()
            return [await a, await b]
        out['epochs'] = loop.run_until_complete(epochs())
    elif CASE == 'private':
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '阿橙', reply='好呀，我帮你保密')
        t(30, '惊喜蛋糕的事你还记得吗', '10001', '阿橙')                      # control: same chat
        t(60, '小爱，惊喜蛋糕是什么情况', '10002', '柠檬', A)
        t(30, '有没有人在准备惊喜蛋糕', '10001', '阿橙', A)
        t(30, '小爱 惊喜蛋糕', '10004', '桃子', B)
        out['private_texts'] = ['我在偷偷准备一个惊喜蛋糕给大家', '好呀，我帮你保密']
    elif CASE == 'anon':
        t(0, '小爱，我们群周末要去爬山', '10002', '柠檬', A, reply='爬山好呀')
        t(30, '周末爬山记得带水', '10003', '阿星', A)
        t(60, '小爱 周末爬山的事你听说了吗', '10004', '桃子', B)
    elif CASE == 'strong_event':
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '阿橙', reply='好呀，惊喜蛋糕我帮你保密')
        t(30, '蛋糕要做草莓味的', '10001', '阿橙', reply='草莓味的惊喜蛋糕听起来好甜')
        # strong feelings in a group right after: an event gets archived there
        group_lines = (('小爱 我好难过 想哭', '{"e":"sadness","i":0.9}'),
                       ('今天被骂了 真的很委屈', '{"e":"sadness","i":0.85}'),
                       ('气死我了！！！他凭什么这样说我', '{"e":"anger","i":0.8}'),
                       ('真的受够了！！！气死了！！！', '{"e":"anger","i":0.9}'))
        for text, tag in group_lines:
            t(20, text, '10002', '柠檬', A, reply='我陪着你，听着也好难过')
        # past the per-chat cooldown; her last six replies still include the two private ones
        group_lines += (('我还是好生气！！！凭什么啊！！！', '{"e":"anger","i":0.9}'),)
        t(620, group_lines[-1][0], '10002', '柠檬', A, reply='我陪着你，听着也好难过')
        out['private_texts'] = ['小爱，我在偷偷准备一个惊喜蛋糕给大家', '好呀，惊喜蛋糕我帮你保密',
                                '蛋糕要做草莓味的', '草莓味的惊喜蛋糕听起来好甜']
        out['all_texts'] = out['private_texts'] + [x[0] for x in group_lines] + ['我陪着你']
        out.update(snapshot(plugin))
    elif CASE == 'loops_by_person':
        t(0, '记得明天提醒我交报告', '10002', '小林', A)
        out['first'] = plugin._read_window('group:' + A)['open_loops']
        t(1, '你好呀', '10003', '小周', A)
        t(1, '你好呀', '10002', '小林', A)
        t(1, '记得明天提醒我交报告', '10003', '小周', A)
        out['both'] = plugin._read_window('group:' + A)['open_loops']
        t(1, '交报告不用了', '10003', '小周', A)
        out['settled'] = plugin._read_window('group:' + A)['open_loops']
        win = plugin._read_window('group:' + A)
        win['open_loops'] = [{'text': '旧群提醒', 'status': 'open'}]
        plugin._write_window('group:' + A, win)
        t(1, '再说一句', '10002', '小林', A)
        private = 'private:10001'
        plugin._write_window(private, {'recent': [], 'open_loops': [{'text': '旧私聊提醒', 'status': 'open'}]})
        t(1, '再说一句', '10001', '小陈')
    elif CASE == 'loops':
        t(0, '记得提醒我明天交报告', '10001', '阿橙', reply='记下啦')              # private loop
        t(30, '小爱 报告我交了', '10002', '柠檬', A)                              # settles nothing in private
        t(30, '记得提醒我明天交报告', '10003', '阿星', A, reply='记下啦')         # group A's own loop
        t(30, '小爱 报告的事', '10004', '桃子', B)
        t(30, '报告的事你还记得吗', '10001', '阿橙')
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
            t(delay, text, '10001', '阿橙', reply='好呀')
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
        orange = harness.FakeEvent('x', sender='10001', name='阿橙')
        loop.run_until_complete(plugin._consolidate_memory(orange, plugin._core(None), force=True))
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
        _two = ('seen_need', 'ambient')  # the only numbers listening may move (step 1-2)
        body_before = json.dumps({k: v for k, v in core.snapshot().items() if k not in _two}, sort_keys=True)
        from astrbot.api.message_components import Image, Plain
        hear(plugin, loop, 0, '我家猫今天学会开冰箱了', '10003', '阿星', A)
        hear(plugin, loop, 0, '看', '10003', '阿星', A, parts=[Plain('看'), Image(url='x')])
        hear(plugin, loop, 0, '小爱你看过冰箱猫吗', '20002', '小爱', A)  # her own account: not stored here
        out['body_same'] = json.dumps({k: v for k, v in core.snapshot().items() if k not in _two},
                                      sort_keys=True) == body_before
        out['listen_calls'] = dict(calls)
        out['event_done'] = dict(Heard.done)
        plugin._provider_for, plugin._embed_text, plugin._ipv4_json = real_provider, real_embed, real_net
        t(30, '小爱 晚上好', '10004', '桃子', B)
        t(30, '小爱 在吗', '10001', '阿橙')
        out['phone_heard'] = snapshot(plugin)['phone']
        out['forgot'] = plugin._owner_forget_person('10003')
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
        event = harness.FakeEvent('小爱 我周末要去爬山', sender='10001', name='阿橙', group=A)
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
        event = harness.FakeEvent('小爱 记得提醒我明天交报告', sender='10001', name='阿橙', group=A)
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
        out['forgot'] = plugin._owner_forget_person('10003')
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
    elif CASE == 'old_body':
        # a state and a self model written before step 1-2 (see the top of this file)
        plugin._core(None)
        out['her'] = json.loads((DATA / 'states' / 'her.json').read_text('utf-8'))
        out['kept_body'] = (DATA / 'states' / 'per_session_archive' / 'her.before_body.json').exists()
        out['self_model'] = json.loads((DATA / 'self_model.json').read_text('utf-8'))
        out['kept_self'] = json.loads((DATA / 'self_model.before_heart.json').read_text('utf-8'))
        t(0, '小爱 早上好', '10002', '柠檬', A, reply='早呀')
        out['her_after'] = json.loads((DATA / 'states' / 'her.json').read_text('utf-8'))
        out['prompt'] = out['turns'][-1]['prompt']
    elif CASE == 'prompt_shape':
        # the reply prompt as the model sees it: a recalled memory, a loop, strong feelings
        t(0, '小爱，记得提醒我明天交报告', '10002', '柠檬', A, reply='记下啦')
        t(10, '我抽卡又歪了，好难过', '10003', '阿星', A, reply='抱抱，下次一定出')
        t(10, '小爱 我好难过 想哭，抽卡又歪了', '10003', '阿星', A, reply='我陪着你，听着也好难过')
        t(10, '小爱 在吗 我好难过', '10001', '阿橙', reply='在呢')
        out['group'] = out['turns'][2]['prompt']
        out['private'] = out['turns'][3]['prompt']
    elif CASE == 'reply_tags':
        # the model writes a state tag although none is asked for
        t(0, '小爱 早上好', '10002', '柠檬', A, reply='早呀')
        core = plugin._core(None)
        out['v0'] = core.v
        replies = []
        for raw in ('好呀<bc>{"e":"joy","i":1.0}</bc>', '好的<bc>{坏掉的', '<biocore>{"e":"anger"}</biocore>嗯嗯',
                    '行<bc v="1">{"e":"joy"}</bc>', '对<bc>外<bc>{"e":"joy"}</bc>层</bc>', '是</bc>呀'):
            event = harness.FakeEvent('小爱 好不好', sender='10002', name='柠檬', group=A)
            resp = LLMResponse(raw)
            loop.run_until_complete(plugin.on_llm_response(event, resp))
            harness.drain(loop)
            replies.append(resp.completion_text)
        out['replies'] = replies
        out['v1'] = core.v
        out['window'] = [x['text'] for x in plugin._read_window('group:' + A)['recent']]
        out['memories'] = [m['text'] for m in snapshot(plugin)['memories']]
    elif CASE == 'heart':
        import types
        req = types.SimpleNamespace(method='GET', body={})

        async def get_json(silent=True):
            return req.body
        req.get_json = get_json
        sys.modules['quart'] = types.SimpleNamespace(request=req)
        out['default'] = {k: plugin.self_model.get(k) for k in ('who_am_i', 'boundaries', 'consistency', 'notebook')}
        req.method, req.body = 'POST', {'who_am_i': '我是被写好的', 'narrative': '替她写的'}
        out['post_self'] = loop.run_until_complete(plugin.page_self_model())
        out['after_post'] = {k: plugin.self_model.get(k) for k in ('who_am_i', 'narrative')}
        req.body = {'rules': ['别在群里提我的工作', '长' * 150] + ['规矩%d' % i for i in range(12)]}
        out['post_rules'] = loop.run_until_complete(plugin.page_owner_rules())
        out['rules_file'] = json.loads((DATA / 'owner_rules.json').read_text('utf-8'))
        t(0, '小爱 早上好', '10002', '柠檬', A)
        t(10, '小爱 在吗', '10001', '阿橙')
        out['group'] = out['turns'][0]['prompt']
        out['private'] = out['turns'][1]['prompt']
    elif CASE == 'strong_no_narrative':
        t(0, '小爱 我好难过 想哭', '10001', '阿橙', reply='我陪着你，听着也好难过')
        for delay, text in ((20, '今天被骂了 真的很委屈'), (20, '气死我了！！！他凭什么这样说我'),
                            (30, '真的受够了！！！气死了！！！')):
            t(delay, text, '10001', '阿橙', reply='我陪着你，听着也好难过')
        t(620, '我还是好生气！！！凭什么啊！！！', '10001', '阿橙', reply='我陪着你，听着也好难过')
        snap = snapshot(plugin)
        out['events'] = [e['text'] for e in snap['events']]
        out['raw_events'] = [json.loads(x) for x in (DATA / 'archives' / 'events.jsonl').read_text('utf-8').splitlines()
                             if x.strip()] if (DATA / 'archives' / 'events.jsonl').exists() else []
        out['self_model'] = json.loads((DATA / 'self_model.json').read_text('utf-8'))
    elif CASE in ('notebook', 'notebook_full', 'notebook_many', 'notebook_body', 'notebook_scrub'):
        plugin.llm_functions = {'notebook': {'enabled': True}}
        plugin.notebook_time = '00:00'
        plugin._begin_job()
        A_PLACE = 'group:' + A

        def event(eid, place, people, title, meaning, n_lines=0):
            session = ('default:GroupMessage:' + place.split(':')[1] if place.startswith('group:')
                       else 'default:FriendMessage:' + place.split(':')[1])
            plugin._append_event_archive({
                'id': eid, 'ts': clock.now, 'session': session, 'title': title, 'event': meaning,
                'meaning_to_her': meaning, 'event_key': eid, 'summary_status': 'digest',
                'origin': main.discretion.make_origin(place, people, ['m_' + eid])})
            if n_lines:  # how busy the chat was today
                plugin._write_window(place, {'recent': [{'ts': clock.now, 'role': 'user', 'text': '…'}] * n_lines,
                                             'open_loops': []})
        if CASE in ('notebook', 'notebook_full'):
            event('cake', 'private:10001', ['10001'], '偷偷准备惊喜蛋糕', '阿橙在偷偷准备一个惊喜蛋糕给大家', 5)
            event('move', 'private:10007', ['10007'], '小鹿要搬家', '小鹿下周要搬家，还没告诉别人', 3)
            event('hike', A_PLACE, ['10002'], '周末去爬山', '柠檬说群里周末一起去爬山')
        if CASE == 'notebook_many':
            for i, n in enumerate((2, 9, 1, 7)):  # four private chats; the three busiest are written
                event('p%d' % i, 'private:1010%d' % i, ['1010%d' % i], '私事%d' % i, '第%d个人的私事' % i, n)
        calls = []
        answers = {}

        class NotebookModel:
            async def text_chat(self, prompt='', system_prompt=None, **k):
                sitting = 'group' if '各个群' in prompt else (
                    'private:10001' if '惊喜蛋糕' in prompt else ('private:10007' if '搬家' in prompt else 'other'))
                calls.append({'sitting': sitting, 'prompt': prompt, 'system': system_prompt})
                answer = answers.get(sitting, '{}')
                if isinstance(answer, Exception):
                    raise answer
                return harness.FakeResponse(answer)
        real_provider = plugin._provider_for

        async def provider(kind, event=None):
            return NotebookModel() if kind == 'notebook' else await real_provider(kind, event)
        plugin._provider_for = provider
        out['sittings'] = plugin._notebook_sittings()

        def changes(*items):
            return json.dumps({'changes': list(items)}, ensure_ascii=False)
        if CASE == 'notebook':
            answers['group'] = changes({'op': 'add', 'text': '周末大家要去爬山', 'private': False, 'uses': ['m2']})
            answers['private:10001'] = changes(
                # the review's case: the private thing said another way, marked "can be told", no uses
                {'op': 'add', 'text': '朋友在准备一个甜甜的秘密', 'private': False, 'uses': []},
                {'op': 'add', 'text': '阿橙在准备惊喜蛋糕，要保密', 'private': True, 'uses': ['m2']})
            answers['private:10007'] = changes(
                {'op': 'add', 'text': '小鹿要搬家了', 'private': True, 'uses': ['m2']},
                {'op': 'add', 'text': '这一条超过了一晚三处', 'private': True})
            out['wrote'] = loop.run_until_complete(plugin._maybe_write_notebook())
            out['again_same_night'] = loop.run_until_complete(plugin._maybe_write_notebook())
            out['calls_first_night'] = [c['sitting'] for c in calls]
            out['prompts'] = {c['sitting']: c['prompt'] for c in calls}
            out['notebook'] = [{k: x.get(k) for k in ('text', 'origin', 'private_mark', 'sitting')}
                               for x in plugin.self_model['notebook']]
            t(0, '小爱 早上好', '10002', '柠檬', A)
            t(10, '小爱 晚上好', '10004', '桃子', B)
            t(10, '小爱 在吗', '10001', '阿橙')
            t(10, '小爱 在吗', '10007', '小鹿')
            out['group_a'], out['group_b'], out['private_orange'], out['private_deer'] = [
                x['prompt'] for x in out['turns'][-4:]]
            # a restart the same day does not call again; a failed call next day counts as that day's
            plugin2 = main.BioCorePlugin(harness.FakeContext(), config=config)
            plugin2.llm_functions = {'notebook': {'enabled': True}}
            plugin2.notebook_time = '00:00'
            plugin2._provider_for = provider
            plugin2._ipv4_json = harness.fake_ipv4_json
            out['restart_same_day'] = loop.run_until_complete(plugin2._maybe_write_notebook())
            clock.advance(86400)
            event('cake2', 'private:10001', ['10001'], '蛋糕做好了', '阿橙把惊喜蛋糕做好了', 2)
            answers.clear()
            answers['group'] = RuntimeError('model down')
            answers['private:10001'] = RuntimeError('model down')
            out['next_day_failed'] = loop.run_until_complete(plugin2._maybe_write_notebook())
            out['after_failure_same_day'] = loop.run_until_complete(plugin2._maybe_write_notebook())
            out['calls_total'] = len(calls)
            out['system_prompt'] = calls[0]['system']
            out['forgot'] = plugin2._forget(person='10001')
            out['notebook_after_forget'] = [x['text'] for x in plugin2.self_model['notebook']]
        elif CASE == 'notebook_full':
            plugin.self_model['notebook'] = [
                {'id': 'n%d' % i, 'text': '旧的第%d条' % i, 'ts': 0, 'origin': main.discretion.make_origin('self')}
                for i in range(20)]
            answers['group'] = changes(
                {'op': 'add', 'text': '本子满了这条加不进去', 'uses': ['m1']},
                {'op': 'edit', 'no': 2, 'text': '改过的第二条' + '很长' * 30, 'uses': ['m2']},
                {'op': 'delete', 'no': 3})
            loop.run_until_complete(plugin._maybe_write_notebook())
            out['notebook'] = [{'text': x['text'], 'origin': x['origin']} for x in plugin.self_model['notebook']]
        elif CASE == 'notebook_many':
            loop.run_until_complete(plugin._maybe_write_notebook())
            out['calls'] = len(calls)
        elif CASE == 'notebook_scrub':
            # what she writes in her notebook is kept like the rest: numbers stay (10-29), and
            # someone deleted is 某人 (not only at the next start)
            t(0, '小爱 早上好', '10002', '柠檬', A)
            t(10, '小爱 我也在', '10003', '阿星', A)
            plugin._owner_forget_person('10003')   # the owner deletes him (panel)
            plugin._begin_job()   # tonight's job starts after the delete
            event('hike', A_PLACE, ['10002'], '周末去爬山', '柠檬说群里周末一起去爬山')
            answers['group'] = changes({'op': 'add', 'text': '阿星说柠檬 10002 也想去爬山', 'private': False,
                                        'uses': ['m1']})
            plugin.self_model['notebook'] = [{'id': 'n1', 'text': '旧的一条', 'ts': 0,
                                              'origin': main.discretion.make_origin('self')}]
            loop.run_until_complete(plugin._maybe_write_notebook())
            out['notebook'] = [x['text'] for x in plugin.self_model['notebook']]
            out['saved'] = [x['text'] for x in json.loads((DATA / 'self_model.json').read_text('utf-8'))['notebook']]
        else:  # notebook_body: nothing happened anywhere today; only her body to look at
            answers['group'] = changes({'op': 'add', 'text': '今天很安静', 'private': False, 'uses': ['m1']})
            loop.run_until_complete(plugin._maybe_write_notebook())
            out['notebook'] = [{'text': x['text'], 'origin': x['origin']} for x in plugin.self_model['notebook']]
            t(0, '小爱 早上好', '10002', '柠檬', A)
            t(10, '小爱 在吗', '10001', '阿橙')
            out['prompts'] = [x['prompt'] for x in out['turns'][-2:]]
    elif CASE == 'notebook_readonly':
        # a private chat's sitting tries to change one of her own thoughts
        plugin.llm_functions = {'notebook': {'enabled': True}}
        plugin.notebook_time = '00:00'
        plugin._begin_job()
        plugin.self_model['notebook'] = [{'id': 'own', 'text': '我喜欢看海', 'ts': 0,
                                          'origin': main.discretion.make_origin('self')}]
        plugin._append_event_archive({
            'id': 'cake', 'ts': clock.now, 'session': 'default:FriendMessage:10001', 'title': '偷偷准备惊喜蛋糕',
            'event': '阿橙在偷偷准备一个惊喜蛋糕', 'meaning_to_her': '阿橙在偷偷准备一个惊喜蛋糕', 'event_key': 'cake',
            'summary_status': 'digest',
            'origin': main.discretion.make_origin('private:10001', ['10001'], ['m_cake'])})
        prompts = {}

        class NotebookModel:
            async def text_chat(self, prompt='', system_prompt=None, **k):
                if '惊喜蛋糕' in prompt:
                    prompts['private'] = prompt
                    return harness.FakeResponse(json.dumps({'changes': [
                        {'op': 'edit', 'no': 1, 'text': '我喜欢看海，也想吃蛋糕', 'private': True},
                        {'op': 'delete', 'no': 1}]}, ensure_ascii=False))
                return harness.FakeResponse('{}')
        real_provider = plugin._provider_for

        async def provider(kind, event=None):
            return NotebookModel() if kind == 'notebook' else await real_provider(kind, event)
        plugin._provider_for = provider
        loop.run_until_complete(plugin._maybe_write_notebook())
        out['private_prompt'] = prompts.get('private', '')
        out['notebook'] = [{'text': x['text'], 'origin': x['origin']} for x in plugin.self_model['notebook']]
        out['changes'] = plugin.self_model['notebook_night']['changes']
        t(0, '小爱 早上好', '10002', '柠檬', A)
        out['group'] = out['turns'][-1]['prompt']
    elif CASE == 'numbers_elsewhere':
        # the owner, 10-29: numbers are kept; what was said openly in group A comes up in group B
        # without names -- and without the numbers she knows (his, group A's); a group she is not
        # in she cannot tell from any number, so its number stays
        said = '小爱，我们群周末要去爬山 我的号是 10002 群号 900001 隔壁群 900077'
        out['a'] = t(0, said, '10002', '柠檬', A, reply='爬山好呀')
        plugin._begin_job()
        origin = main.discretion.make_origin('group:' + A, ['10002'], ['m_hike'])
        plugin._append_event_archive({
            'id': 'hike', 'ts': clock.now, 'session': 'default:GroupMessage:' + A, 'title': '周末爬山',
            'event': '柠檬（10002）约群 900001 周末爬山，隔壁群 900077 也去', 'event_key': 'hike', 'origin': origin})
        plugin.self_model['notebook'] = [{'id': 'n1', 'text': '柠檬 10002 约群 900001 爬山，隔壁群 900077 也去', 'ts': 0,
                                          'origin': origin}]
        out['b'] = t(60, '小爱，我们群周末要去爬山 我的号是 群号 隔壁群 你听说了吗', '10004', '桃子', B)
        out['same'] = t(30, '小爱 爬山的事你还记得吗', '10002', '柠檬', A)
        out['kept'] = [e['text'] for e in plugin._read_library(vectors=False)['entries']]
    elif CASE == 'silent_at':
        # someone who never writes, only @'d in group A: elsewhere neither his number nor his name
        from astrbot.api.message_components import At, Plain
        out['a'] = t(0, '@小爱bot(20002) @阿默(10066) 周末一起去爬山吗', '10004', '桃子', A, reply='好呀',
                     parts=[At(qq='20002', name='小爱bot'), Plain(' '), At(qq='10066', name='阿默'),
                            Plain(' 周末一起去爬山吗')])
        out['known'] = sorted(plugin._known_numbers())
        plugin._begin_job()
        plugin._append_event_archive({
            'id': 'hike', 'ts': clock.now, 'session': 'default:GroupMessage:' + A, 'title': '周末爬山',
            'event': '桃子约 10066 周末一起去爬山', 'event_key': 'hike',
            'origin': main.discretion.make_origin('group:' + A, ['10004'], ['m_hike'])})
        out['b'] = t(60, '小爱 周末一起去爬山吗 你听说了吗', '10001', '阿橙', B)
        out['kept'] = [e['text'] for e in plugin._read_library(vectors=False)['entries']]
        plugin._name_index = None   # as after a restart: the index is built again from what she keeps
        out['known_after_restart'] = sorted(plugin._known_numbers())
    elif CASE == 'frames':
        # the owner, 10-29: names she writes back are framed in what she keeps; the reply model
        # sees them bare; a quote someone typed with 「」 stays as typed
        hear(plugin, loop, 0, '我说过「周末 一起去吧」，记得吗', '10002', '柠檬', A)
        plugin._begin_job()
        plugin._append_event_archive({
            'id': 'hike', 'ts': clock.now, 'session': 'default:GroupMessage:' + A, 'title': '「柠檬」约「阿星」爬山',
            'event': '「柠檬」说「周末 一起去吧」，「阿星」答应了', 'event_key': 'hike',
            'origin': main.discretion.make_origin('group:' + A, ['10002', '10003'], ['m_hike'])})
        hear(plugin, loop, 1, '我也去', '10003', '阿星', A)
        out['a'] = t(10, '小爱 爬山的事你还记得吗', '10004', '桃子', A)
        out['b'] = t(10, '小爱 爬山的事你听说了吗', '10001', '阿橙', B)
        out['kept'] = [(e['title'], e['event']) for e in plugin._event_archive(10, read_only=True)]
    elif CASE == 'names_everywhere':
        # 阿星 goes by another group card in group B; a thing said openly in both comes up
        # in a third group: every name he goes by is taken out
        from astrbot.api.message_components import Plain
        hear(plugin, loop, 0, '周末去爬山吧', '10003', '阿星', A)
        hear(plugin, loop, 10, '我也去，带水', '10003', '星仔', B)
        plugin._begin_job()
        both = main.discretion.merge([main.discretion.make_origin('group:' + A, ['10003'], ['m_a']),
                                      main.discretion.make_origin('group:' + B, ['10003'], ['m_b'])])
        plugin._append_event_archive({
            'id': 'hike', 'ts': clock.now, 'session': 'default:GroupMessage:' + A, 'title': '周末爬山',
            'event': '阿星约大家周末爬山，星仔说他带水', 'event_key': 'hike', 'origin': both})
        t(10, '小爱 晚上好', '10004', '桃子', '900003')
        out['third_group'] = out['turns'][-1]['prompt']
    elif CASE == 'insight':
        plugin.llm_functions = {'insight': {'enabled': True}}
        plugin._begin_job()
        events = [{'id': 'e%d' % i, 'ts': clock.now, 'title': '私下的事%d' % i, 'event': '阿橙说的私事',
                   'origin': main.discretion.make_origin('private:10001', ['10001'], ['m%d' % i])}
                  for i in range(3)]
        real_provider = plugin._provider_for

        class InsightModel:
            async def text_chat(self, prompt='', **k):
                return harness.FakeResponse('{"insight":"被认真对待会安心"}')

        async def provider(kind, event=None):
            return InsightModel() if kind == 'insight' else await real_provider(kind, event)
        plugin._provider_for = provider
        out['made'] = loop.run_until_complete(plugin._generate_insight(None, plugin._core(None), events))
        path = DATA / 'archives' / 'insights.jsonl'
        out['insights'] = [json.loads(x) for x in path.read_text('utf-8').splitlines() if x.strip()]
        out['her'] = plugin._core(None).snapshot()
        out['forgot'] = plugin._forget(person='10001')
        out['insights_after'] = [json.loads(x) for x in path.read_text('utf-8').splitlines() if x.strip()]
    elif CASE in ('listen_off', 'listen_on'):
        import mixin_phone
        mixin_phone.LISTEN_MOVES_BODY = CASE == 'listen_on'
        core = plugin._core(None)
        core.seen_need, core.ambient = 0.9, 0.0
        from astrbot.api.message_components import At, Plain
        hear(plugin, loop, 0, '小爱 你看', '10002', '柠檬', A, parts=[At(qq='20002'), Plain('你看')])
        out['seen_after_at'] = core.seen_need
        for i in range(30):
            hear(plugin, loop, 1, '闲聊%d' % i, '10005', '路人', A)
        out['ambient'] = core.ambient
        mixin_phone.LISTEN_MOVES_BODY = True
    elif CASE == 'ambient_reads':
        # many messages in one group: she does not reread every window for each of them
        t(0, '小爱 早上好', '10002', '柠檬', A)
        t(10, '小爱 晚上好', '10004', '桃子', B)
        t(10, '小爱 在吗', '10001', '阿橙')
        real_read = plugin._read_window
        reads = []

        def counting_read(place):
            reads.append(place)
            return real_read(place)
        plugin._read_window = counting_read
        for i in range(20):
            hear(plugin, loop, 1, '闲聊%d' % i, '10005', '路人', A)
        plugin._read_window = real_read
        out['other_reads'] = len([p for p in reads if p != 'group:' + A])
        out['ambient'] = plugin._core(None).ambient
        out['expected'] = min(1.0, 23 / 30.0)  # 20 now, 3 earlier, all within 30 minutes
    elif CASE == 'woken_once':
        # a message that wakes her: seen once, not once in on_message and again in the request
        t(0, '小爱 早上好', '10002', '柠檬', A)
        core = plugin._core(None)
        calls = []
        real_seen = core.be_seen

        def counting_seen():
            calls.append(1)
            return real_seen()
        core.be_seen = counting_seen
        event = harness.FakeEvent('小爱 在吗', sender='10002', name='柠檬', group=A)
        event.is_at_or_wake_command = True
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_message(event))
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        out['seen_calls'] = len(calls)
    elif CASE == 'names':
        # who said a recalled memory: the nickname in the same place, nobody elsewhere
        t(0, '小爱，我们周末去爬山吧', '10002', '柠檬', A)
        t(10, '小爱，爬山我也去', '10003', '阿星', A)
        t(10, '小爱，我偷偷准备了爬山的惊喜', '10001', '阿橙')
        t(10, '小爱，爬山要带水吗', '10002', '柠檬', A)
        t(10, '小爱，爬山好玩吗', '10004', '桃子', B)
        t(10, '小爱，爬山的惊喜准备好了', '10001', '阿橙')
        out['same_group'] = out['turns'][3]['prompt']
        out['other_group'] = out['turns'][4]['prompt']
        out['private'] = out['turns'][5]['prompt']
    elif CASE == 'quote':
        # 阿橙 quotes 柠檬's message; forgetting by message id finds each by its own id only
        first = t(0, '周末一起去爬山吧', '10002', '柠檬', A)
        from astrbot.api.message_components import Plain, Reply
        quoted_id = first['refs'][0]
        second = t(30, '小爱 这个我也想去', '10001', '阿橙', A,
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
        t(10, '小爱 在吗', '10001', '阿橙', reply='在的')
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
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '阿橙')
        for delay, text, tag in ((400, '小爱 我好难过 想哭', '{"e":"sadness","i":0.9}'),
                                 (20, '今天被骂了 真的很委屈', '{"e":"sadness","i":0.85}'),
                                 (20, '气死我了！！！他凭什么这样说我', '{"e":"anger","i":0.8}'),
                                 (30, '真的受够了！！！气死了！！！', '{"e":"anger","i":0.9}')):
            t(delay, text, '10001', '阿橙', reply='我陪着你，听着也好难过')
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
        orange = harness.FakeEvent('我还是好生气！！！凭什么啊！！！', sender='10001', name='阿橙')
        clock.advance(620)
        if CASE in ('wait_archive', 'wait_consolidate'):  # events archived from memory entries
            for text in ('小爱 谢谢你 我答应你以后别难过了', '对不起 以后我永远喜欢你'):  # promise words
                t(30, text, '10001', '阿橙')
            lib = plugin._read_library()  # as if said with strong feelings: worth an event
            for e in lib['entries']:
                if e.get('sender_id') == '10001':
                    e['importance'] = 0.9
            plugin._write_library(lib)
            plugin._last_event_archive = 0.0
            loop.run_until_complete(plugin.on_message(orange))
            armed[0] = True
            if CASE == 'wait_archive':  # the per-turn archive (mixin_events _maybe_archive_events)
                plugin._begin_job()  # as on_llm_request does before it starts this task
                loop.run_until_complete(plugin._maybe_archive_events(orange, plugin._core(None)))
            else:  # consolidation with nothing to group: it archives events instead
                loop.run_until_complete(plugin._consolidate_memory(orange, plugin._core(None), force=True))
            harness.drain(loop)
        else:
            loop.run_until_complete(plugin.on_message(orange))
            armed[0] = True
            loop.run_until_complete(plugin.on_llm_request(orange, ProviderRequest(prompt=orange.message_str,
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
        real_tom = plugin._maybe_tom_probe
        order = []

        async def slow_tom(event, *a, **k):  # each request waits after its recall, the other one runs
            order.append(event.message_str)
            for _ in range(5):
                await asyncio.sleep(0)
            order.append(event.message_str)
            return await real_tom(event, *a, **k)
        plugin._maybe_tom_probe = slow_tom
        real_render = main.interpretation.render_compact
        metas = {}

        def render(core, *a, **k):  # what each request hands its own prompt
            metas[len(metas)] = dict(k.get('memory_meta') or {})
            return real_render(core, *a, **k)
        main.interpretation.render_compact = render
        clock.advance(30)
        ea = harness.FakeEvent('小爱，爬山的事定了吗', sender='10002', name='柠檬', group=A)
        eb = harness.FakeEvent('小爱，唱歌的事定了吗', sender='10004', name='桃子', group=B)
        ra = ProviderRequest(prompt=ea.message_str, system_prompt='你是小爱。')
        rb = ProviderRequest(prompt=eb.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(asyncio.gather(plugin.on_llm_request(ea, ra), plugin.on_llm_request(eb, rb)))
        harness.drain(loop)
        main.interpretation.render_compact = real_render
        out['prompt_a'] = '\n'.join(p.get('text') for p in ra.extra_user_content_parts)
        out['prompt_b'] = '\n'.join(p.get('text') for p in rb.extra_user_content_parts)
        out['interleaved'] = order[:2] == [ea.message_str, eb.message_str]
        # the request that renders first is the one that started first (A)
        out['who_a'] = list((metas.get(0, {}).get('destinations') or {}).keys())
        out['who_b'] = list((metas.get(1, {}).get('destinations') or {}).keys())
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
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '阿橙')
        t(60, '跟大家说下，我在偷偷准备一个惊喜蛋糕', '10001', '阿橙', A)
        t(30, '小爱 惊喜蛋糕准备得怎么样了', '10001', '阿橙', A)
        t(30, '小爱 惊喜蛋糕的事', '10004', '桃子', B)
    elif CASE == 'same_words':
        # he says it in a group, then the very same words to her in private
        t(0, '我中午吃了一碗牛肉面', '10001', '阿橙', A, reply='听起来好香')
        t(30, '我中午吃了一碗牛肉面', '10001', '阿橙')
        # someone tells her something in private, then someone says the same words in a group
        t(30, '我下午要去剪头发了', '10005', '栗子')
        t(30, '我下午要去剪头发了', '10002', '柠檬', B)
    elif CASE == 'same_words_known':
        # the private chat had these very words before; then a group, then private again
        t(0, '我中午吃了一碗牛肉面', '10001', '阿橙')
        t(30, '我中午吃了一碗牛肉面', '10003', '阿星', A)
        t(30, '我中午吃了一碗牛肉面', '10001', '阿橙')
    elif CASE == 'global_own':
        # step 2, global_memory on: he said it openly in group A ...
        t(0, '我中午吃了一碗牛肉面', '10001', '阿橙', A, reply='听起来好香')
        # ... asks about it in his private chat, then in group B, then someone else asks in B
        t(30, '我中午吃了一碗牛肉面，你还记得吗', '10001', '阿橙')
        t(30, '小爱 我中午吃了一碗牛肉面，你知道吗', '10001', '阿橙', B)
        t(30, '小爱 谁中午吃了一碗牛肉面', '10004', '桃子', B)
    elif CASE == 'global_private':
        # told her in private; then in a group with him there; then someone else's private chat
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '阿橙', reply='好呀，我帮你保密')
        t(30, '小爱 我在偷偷准备一个惊喜蛋糕给大家的事', '10001', '阿橙', A)
        t(30, '我在偷偷准备一个惊喜蛋糕给大家，听说了吗', '10002', '柠檬')
        t(30, '我在偷偷准备一个惊喜蛋糕给大家，还记得吗', '10001', '阿橙')
        out['turn_log'] = json.loads((DATA / 'brain_turns.json').read_text('utf-8')) \
            if (DATA / 'brain_turns.json').exists() else {}
    elif CASE == 'global_numbers':
        # an @ with a number, a group's number, another group's number in what she keeps
        t(0, '@柠檬(10002) 周末一起去爬山吧 群900002也去', '10001', '阿橙', A)
        t(30, '小爱 周末一起去爬山吗 @柠檬(10002)', '10003', '阿星', A)
        t(30, '小爱 周末爬山的事 900001 那边定了吗', '10003', '阿星', B)
    elif CASE == 'global_notebook':
        t(0, '小爱 早上好', '10001', '阿橙', A)
        t(0, '小爱 早上好', '10002', '柠檬')
        plugin.self_model = dict(plugin.self_model or {}, notebook=[
            {'text': '想多听听大家在聊什么', 'origin': main.discretion.make_origin('self')},
            {'text': '群里周末要去爬山', 'origin': main.discretion.make_origin('group:' + A, ['10001'], ['n1'])},
            {'text': '柠檬在偷偷学画画', 'origin': main.discretion.make_origin('private:10002', ['10002'], ['n2'])},
            {'text': '来历不明的一条', 'origin': main.discretion.make_origin('')},
        ])
        t(30, '小爱 你最近在想什么', '10004', '桃子', B)
    elif CASE == 'global_gone':
        t(0, '小爱 我和阿星周末去爬山', '10001', '阿橙', A)
        t(10, '小爱 对，我也去爬山', '10003', '阿星', A)
        out['forgot'] = plugin._owner_forget_person('10003')
        t(30, '小爱 周末去爬山的事你还记得吗', '10001', '阿橙')
    elif CASE == 'one_body':
        out['v_start'] = plugin._core(None).v
        for text in ('太开心了！！！我终于抽到了！！！', '好耶！十连出金了', '笑死，运气也太好了吧', '真的好高兴啊',
                     '谢谢小爱，你太可爱了', '喜欢喜欢，今天真开心'):
            t(5, text, '10002', '柠檬', A, reply='恭喜恭喜！真为你开心')
        out['v_after_a'] = plugin._core(None).v
        t(0, '小爱 晚上好', '10004', '桃子', B)
        out['v_b'] = plugin._core(None).v
        out['cores'] = list(plugin.cores)
    elif CASE == 'forget':
        t(0, '小爱，我在偷偷准备一个惊喜蛋糕给大家', '10001', '阿橙')
        # the strong-feeling stretch of the golden scenario, so events get archived
        for delay, text, tag in ((400, '小爱 我好难过 想哭', '{"e":"sadness","i":0.9}'),
                                 (20, '今天被骂了 真的很委屈', '{"e":"sadness","i":0.85}'),
                                 (20, '气死我了！！！他凭什么这样说我', '{"e":"anger","i":0.8}'),
                                 (30, '真的受够了！！！气死了！！！', '{"e":"anger","i":0.9}'),
                                 (620, '我还是好生气！！！凭什么啊！！！', '{"e":"anger","i":0.9}')):
            t(delay, text, '10001', '阿橙', reply='我陪着你，听着也好难过')
        t(60, '小爱 我今天也在群里', '10001', '阿橙', A)
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
        t(10, '惊喜蛋糕', '10001', '阿橙')
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
