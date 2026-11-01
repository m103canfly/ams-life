"""Scripted runs for test_attention (step 2, 甲: she decides herself whether to answer); prints a
JSON result. Run in a fresh interpreter:
    PYTHONHASHSEED=0 python tests/attention_cases.py <empty data dir> <out.json> <case>
All made up: group 900001, the owner 10009, Mango 10001, Lemon 10002. No network, no model.
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

import main  # noqa: E402
import attention  # noqa: E402
import mixin_attention  # noqa: E402
real_typing_seconds = attention.typing_seconds
attention.typing_seconds = lambda text: 0.01   # quick
from astrbot.api import logger  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

mixin_attention.WAIT_SECONDS = {"group": 0.05, "called": 0.02, "private": 0.03}   # quick, same order
A = '900001'


class Event(harness.FakeEvent):
    def __init__(self, text, sender='10001', name='阿橙', group=A, wake=False):
        super().__init__(text, sender=sender, name=name, group=group)
        self.is_at_or_wake_command = wake
        self.stopped = False

    def stop_event(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    def get_platform_id(self):
        return 'default'

    def request_llm(self, prompt, conversation=None, **kw):
        return {'request_llm': prompt, 'conversation': getattr(conversation, 'cid', None)}


class Conversations:
    def __init__(self):
        self.made = []

    async def get_curr_conversation_id(self, umo):
        return None

    async def new_conversation(self, umo, platform_id=None):
        self.made.append(umo)
        return 'cid-1'

    async def get_conversation(self, umo, cid):
        return type('Conv', (), {'cid': cid})()


class Usage:
    def __init__(self, miss, hit, out):
        self.input_other, self.input_cached, self.output = miss, hit, out


def run():
    config = {'self_decide': CASE != 'off', 'owner_qq': '10009', 'attention_level': 'normal'}
    config.update(reply_groups=[A], reply_private=['10001', '10002'])
    ctx = harness.FakeContext()
    ctx.conversation_manager = Conversations()
    sent = []

    async def send_message(umo, chain):
        sent.append({'umo': umo, 'chain': [(type(c).__name__, getattr(c, 'text', getattr(c, 'id', None)))
                                           for c in chain.chain]})
    ctx.send_message = send_message
    plugin = main.BioCorePlugin(ctx, config=config)
    plugin._ipv4_json = harness.fake_ipv4_json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    out = {}

    async def decide(event):
        await plugin.on_message(event)
        got = [x async for x in plugin.on_message_decide(event)]
        return {'stopped': event.stopped, 'requests': got}

    def one(event):
        return loop.run_until_complete(decide(event))

    if CASE in ('called_at', 'off'):
        out['r'] = one(Event('小爱 你好', wake=True))
    elif CASE == 'burst':
        async def both():
            first = asyncio.ensure_future(decide(Event('小爱', wake=True)))
            await asyncio.sleep(0.005)
            second = asyncio.ensure_future(decide(Event('周末一起去爬山吗', wake=False)))
            return await first, await second
        a, b = loop.run_until_complete(both())
        out['first'], out['second'] = a, b
        out['conversations'] = ctx.conversation_manager.made
    elif CASE == 'not_called':
        async def low(event):
            return 0.1
        plugin._score = low
        out['low'] = one(Event('今天天气不错', sender='10002', name='柠檬'))

        async def high(event):
            return 0.9
        plugin._score = high
        out['high'] = one(Event('那个游戏出新角色了', sender='10002', name='柠檬'))
    elif CASE == 'named':
        out['named'] = one(Event('小爱，周末去哪玩', sender='10002', name='柠檬'))
        out['not_a_call'] = one(Event('看到她我心里小爱乱撞', sender='10002', name='柠檬'))
    elif CASE == 'continue':
        one(Event('小爱 在吗', wake=True))
        plugin._window_add_reply(Event('小爱 在吗', wake=True), '在呀')
        out['his'] = one(Event('想问你个事', sender='10001', wake=False))
        out['other'] = one(Event('我也想问', sender='10002', name='柠檬', wake=False))
    elif CASE == 'night':
        attention.is_night = lambda *a, **k: True
        calls = []
        for _ in range(3):
            clock.advance(60)
            calls.append(one(Event('小爱 醒醒', wake=True)))
        out['calls'] = calls
        out['woken'] = bool(getattr(plugin, '_woken_at', 0))
        out['not_called_at_night'] = one(Event('随便聊聊', sender='10002', name='柠檬'))
    elif CASE == 'hour':
        plugin._window_state('group:' + A)['sent'] = [clock.now - 10] * 30
        out['r'] = one(Event('小爱 你好', wake=True))
        out['private'] = one(Event('小爱 你好', group=None, wake=True))
    elif CASE == 'money':
        (DATA / 'states').mkdir(parents=True, exist_ok=True)
        day = __import__('time').strftime('%Y-%m-%d')
        mixin_attention.SPEND_PATH.write_text(json.dumps({day: {'reply': 8.5}}), 'utf-8')
        out['soft_group'] = one(Event('小爱 你好', wake=True))
        out['soft_owner_private'] = one(Event('小爱 你好', sender='10009', name='主人', group=None, wake=True))
        out['soft_other_private'] = one(Event('小爱 你好', sender='10002', name='柠檬', group=None, wake=True))
        mixin_attention.SPEND_PATH.write_text(json.dumps({day: {'reply': 10.0}}), 'utf-8')
        out['hard_owner_private'] = one(Event('小爱 你好', sender='10009', name='主人', group=None, wake=True))
    elif CASE == 'pieces':
        plugin.self_decide = False

        async def reply(text, enabled=True):
            plugin.reply_in_pieces = enabled
            event = Event('hello', wake=True)
            response = LLMResponse(text)
            await plugin.on_llm_response(event, response)
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()
                     and '_send_rest' in repr(t.get_coro())]
            if tasks:
                await asyncio.gather(*tasks)
            chain = getattr(response, 'result_chain', None)
            return {'chain': [(type(c).__name__, getattr(c, 'text', getattr(c, 'id', None)))
                              for c in (chain.chain if chain else [])],
                    'text': response.completion_text, 'stopped': event.stopped}

        out['on'] = loop.run_until_complete(reply('one\ntwo[表情:微笑]\nthree'))
        out['sent'] = list(sent)
        out['off'] = loop.run_until_complete(reply('one\ntwo', False))
        win = next(iter((DATA / 'phone').glob('group_*.json')))
        out['phone'] = [x.get('text') for x in json.loads(win.read_text('utf-8'))['recent']
                        if x.get('role') == 'assistant']
        calls = []

        async def fail_send(umo, chain):
            calls.append(chain.get_plain_text())
            raise RuntimeError('send failed')

        ctx.send_message = fail_send
        loop.run_until_complete(reply('first\nsecond\nthird'))
        out['failed_calls'] = calls
    elif CASE == 'pieces_contract':
        from types import SimpleNamespace
        from unittest.mock import patch
        from astrbot.api.event import MessageChain
        from astrbot.api.message_components import At, Plain, Reply

        plugin.self_decide = False
        events = []
        delays = []

        async def fake_sleep(seconds):
            delays.append(seconds)

        async def outlet(umo, chain):
            events.append(['text', [(type(c).__name__, getattr(c, 'text', None)) for c in chain.chain]])

        ctx.send_message = outlet

        async def turn(text, chain=None, offered=None):
            event = Event('hello', wake=True)
            if offered is not None:
                event._ams_stickers_offered = offered
            response = LLMResponse(text, chain)
            await plugin.on_llm_response(event, response)
            first = [(type(c).__name__, getattr(c, 'text', None))
                     for c in (response.result_chain.chain if response.result_chain else [])]
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()
                     and '_send_rest' in repr(t.get_coro())]
            if tasks:
                await asyncio.gather(*tasks)
            return event, response, first

        async def exercise():
            attention.typing_seconds = real_typing_seconds
            fake_asyncio = SimpleNamespace(sleep=fake_sleep, create_task=asyncio.create_task)
            with patch.object(mixin_attention, 'asyncio', fake_asyncio):
                initial = MessageChain([Reply(id='fake-message'), At(qq='10005'), Plain('first\nsecond\nthird')])
                event, response, first = await turn('first\nsecond\nthird', initial)
                out['first'], out['rest'], out['delays'] = first, list(events), list(delays)
                part = lambda kind, text: SimpleNamespace(type=kind, text=text)
                context = SimpleNamespace(messages=[SimpleNamespace(role='assistant',
                                          content=[part('think', 'thinking'), part('text', 'first')])])
                await plugin.on_agent_done(event, context, response)
                out['history'] = [[p.type, p.text] for p in context.messages[0].content]

                events.clear()
                plugin.global_memory = True
                async def hold(event, response, reply):
                    plugin._stop(event)
                    return ''
                with patch.object(plugin, '_look_at_reply', hold):
                    held, _, _ = await turn('first\nsecond')
                plugin.global_memory = False
                plugin.self_decide = True
                silent, _, _ = await turn('【不说】')
                out['held'] = [held.stopped, silent.stopped, list(events)]

                plugin.self_decide = False
                plugin._stickers_on = lambda: True
                plugin._sticker_lib = lambda: SimpleNamespace(rows={'fake': {'caption': 'cat'}})
                async def clear(event, sid):
                    return True
                plugin._sticker_cleared = clear
                def after(event, sid):
                    async def send():
                        events.append(['sticker', sid])
                        return True
                    return send
                plugin._sticker_after = after
                events.clear()
                sticker_event, _, sticker_first = await turn('first\nsecond[表情包:1]\nthird', offered=['fake'])
                out['sticker_first'] = sticker_first
                out['sticker_order'] = list(events)

                def failed_after(event, sid):
                    async def send():
                        events.append(['sticker_failed', sid])
                        return False
                    return send
                plugin._sticker_after = failed_after
                events.clear()
                _, _, first = await turn('first\nsecond[表情包:1]\nthird', offered=['fake'])
                out['failed_sticker_first'] = first
                out['failed_sticker_order'] = list(events)

        loop.run_until_complete(exercise())
    elif CASE == 'pieces_voice':
        from types import SimpleNamespace
        from unittest.mock import patch
        import mixin_selfie

        plugin.self_decide = False
        order = []
        gate = asyncio.Event()

        async def wait_to_type(seconds):
            await gate.wait()

        async def delay_media(seconds):
            order.append(['delay', seconds])

        async def send_message(umo, chain):
            order.append(['text', chain.get_plain_text()])

        async def clear(event, text):
            return True

        async def voice(text):
            return 'fake-voice'

        ctx.send_message = send_message
        plugin._phone_clear = clear
        plugin._make_voice = voice
        plugin._phone_account = lambda *args, **kwargs: None
        plugin._note_she_sent = lambda *args, **kwargs: None
        plugin._phone_prune = lambda *args, **kwargs: None

        async def exercise_voice():
            event = Event('hello', wake=True)
            async def send_media(chain):
                order.append(['voice', type(chain.chain[0]).__name__])
            event.send = send_media
            plugin._phone_queue(event)['voice'] = 'hello'
            response = LLMResponse('first\nsecond\nthird')
            attention_asyncio = SimpleNamespace(sleep=wait_to_type, create_task=asyncio.create_task)
            selfie_asyncio = SimpleNamespace(sleep=delay_media)
            with patch.object(mixin_attention, 'asyncio', attention_asyncio), \
                    patch.object(mixin_selfie, 'asyncio', selfie_asyncio):
                await plugin.on_llm_response(event, response)
                order.append(['text', response.result_chain.get_plain_text()])
                await asyncio.sleep(0)
                await asyncio.sleep(0)
                out['before_release'] = list(order)
                gate.set()
                tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()
                         and ('_send_rest' in repr(t.get_coro()) or '_media_after_reply' in repr(t.get_coro()))]
                if tasks:
                    await asyncio.gather(*tasks)
                out['order'] = list(order)

        loop.run_until_complete(exercise_voice())
    elif CASE == 'replies':
        def reply(text, usage=None, chain=False):
            event = Event('小爱 周末去哪玩', wake=True)
            req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')
            loop.run_until_complete(plugin.on_message(event))
            loop.run_until_complete(plugin.on_llm_request(event, req))
            resp = LLMResponse(text)
            if chain:   # as DeepSeek's answers come back (openai_source.py 875): with a chain
                from astrbot.api.event import MessageChain
                resp = LLMResponse(text, MessageChain().message(text))
            resp.usage = usage
            loop.run_until_complete(plugin.on_llm_response(event, resp))
            harness.drain(loop)
            loop.run_until_complete(asyncio.sleep(0))
            rest = [t for t in asyncio.all_tasks(loop) if not t.done() and '_send_rest' in repr(t.get_coro())]
            if rest:   # the next messages, a pause before each
                loop.run_until_complete(asyncio.gather(*rest))
            chain = getattr(resp, 'result_chain', None)
            return {'prompt_has_choices': '[她可以]' in '\n'.join(
                        p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts),
                    'stopped': event.stopped, 'text': resp.completion_text,
                    'chain': [(type(c).__name__, getattr(c, 'text', getattr(c, 'id', None)))
                              for c in (chain.chain if chain is not None else [])]}
        out['silent'] = reply('【不说】', Usage(1000, 0, 200))
        out['multi'] = reply('周末去爬山吧\n【下一条】\n记得带水[表情:微笑]\n【下一条】\n[表情:赞]', Usage(2000, 1000, 500))
        out['face_first'] = reply('[表情:呲牙]', None)
        out['with_chain'] = reply('第一句\n【下一条】\n第二句', None, chain=True)
        out['silent_inside'] = reply('嗯【不说】', None)
        out['sent'] = sent
        win = next(iter((DATA / 'phone').glob('group_*.json')))
        out['phone'] = [x.get('text') for x in json.loads(win.read_text('utf-8'))['recent'] if x.get('role') == 'assistant']
        out['spend'] = json.loads(mixin_attention.SPEND_PATH.read_text('utf-8'))
        out['panel'] = plugin._spend_for_panel()
    out['log'] = [t for _lvl, t in logger.records if 'attention' in t]
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), 'utf-8')


run()
