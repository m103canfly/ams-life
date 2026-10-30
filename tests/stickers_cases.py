"""Scripted runs for test_stickers_wire (step 2, 丙: her stickers in the plugin); prints a JSON result.
Run in a fresh interpreter:
    PYTHONHASHSEED=0 python tests/stickers_cases.py <empty data dir> <out.json> <case>
All made up: group 900001, the owner 10009, Mango 10001, Lemon 10002; the pictures are a few bytes
made here; the model, NapCat's client and QQ's picture server are stand-ins. No network.
"""
import asyncio
import json
import struct
import sys
import time
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA, OUT, CASE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
clock = harness.prepare(DATA)

import main  # noqa: E402
import attention  # noqa: E402
import mixin_attention  # noqa: E402
import mixin_stickers  # noqa: E402
import stickers  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

attention.typing_seconds = lambda text: 0.01   # quick
mixin_attention.WAIT_SECONDS = {"group": 0.05, "called": 0.02, "private": 0.03}
A = '900001'
OWNER = '10009'


def png(w, h, seed=0):
    """A real (tiny) PNG: its header says w x h."""
    raw = b''.join(b'\x00' + bytes([seed % 256]) * (w * 3) for _ in range(h))

    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


PICTURES = {'https://gchat.qpic.cn/a.png': png(4, 4, 1), 'https://gchat.qpic.cn/b.png': png(5, 5, 2),
            'https://gchat.qpic.cn/c.png': png(6, 6, 3), 'https://gchat.qpic.cn/d.png': png(7, 7, 4)}
fetched = []


def fake_fetch(url, timeout=15):
    fetched.append(url)
    return PICTURES.get(url, b'') if stickers.check_image_url(url)[0] else b''


stickers.fetch_picture = fake_fetch

LOOKS = {   # what the stand-in model says of each picture
    'https://gchat.qpic.cn/a.png': {'caption': '一只在笑的猫', 'kind': 'sticker', 'personal': False, 'group_meme': False,
                                    'emotion': '开心', 'scene': '夸人', 'keep': True, 'why': '好可爱'},
    'https://gchat.qpic.cn/b.png': {'caption': '一张证件照', 'kind': 'photo', 'personal': True, 'group_meme': False,
                                    'emotion': '', 'scene': '', 'keep': True, 'why': ''},
    'https://gchat.qpic.cn/c.png': {'caption': '写着群友名字的图', 'kind': 'sticker', 'personal': False,
                                    'group_meme': True, 'emotion': '搞笑', 'scene': '', 'keep': True, 'why': ''},
    'https://gchat.qpic.cn/d.png': {'caption': '一只跳舞的兔子', 'kind': 'sticker', 'personal': False,
                                    'group_meme': False, 'emotion': '开心', 'scene': '庆祝', 'keep': True, 'why': '好玩'},
}


class Provider(harness.FakeProvider):
    def __init__(self):
        super().__init__()
        self.provider_config['modalities'] = ['text', 'image']   # deepseek-flash sees pictures
        self.looks = []

    async def text_chat(self, prompt='', system_prompt=None, **kwargs):
        if str(prompt).startswith('看看这张图'):
            ref = (kwargs.get('image_urls') or [''])[0]
            self.looks.append(ref)
            return harness.FakeResponse(json.dumps(LOOKS.get(ref, {}), ensure_ascii=False))
        return await super().text_chat(prompt, system_prompt, **kwargs)


class Bot:
    """NapCat's client of the adapter, as call_action sees it."""

    def __init__(self, fail=False):
        self.calls, self.fail = [], fail

    async def call_action(self, action, **params):
        if self.fail:
            raise RuntimeError('napcat says no')
        self.calls.append({'action': action, 'params': params})


class Event(harness.FakeEvent):
    def __init__(self, text, sender='10001', name='芒果', group=A, wake=False, raw_images=(), bot=None):
        super().__init__(text, sender=sender, name=name, group=group)
        self.is_at_or_wake_command = wake
        self.stopped = False
        self.bot = bot
        seg = [{'type': 'image', 'data': {'url': u, 'file': u.rsplit('/', 1)[-1], 'sub_type': 1,
                                          'summary': '[动画表情]'}} for u in raw_images]
        self.message_obj.raw_message = {'message': [{'type': 'text', 'data': {'text': text}}] + seg}

    def stop_event(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    def get_platform_id(self):
        return 'default'


def run():
    on = CASE != 'off'
    config = {'self_decide': True, 'stickers_enabled': on, 'owner_qq': OWNER, 'attention_level': 'normal',
              'global_memory': CASE == 'held'}
    ctx = harness.FakeContext()
    ctx.provider = Provider()
    sent = []

    async def send_message(umo, chain):
        sent.append({'umo': umo, 'chain': [(type(c).__name__, getattr(c, 'text', getattr(c, 'id', None)),
                                            str(getattr(c, 'file', ''))[:9]) for c in chain.chain]})
    ctx.send_message = send_message
    plugin = main.BioCorePlugin(ctx, config=config)
    plugin._ipv4_json = harness.fake_ipv4_json
    plugin.llm_functions = dict(getattr(plugin, 'llm_functions', {}) or {})
    plugin.llm_functions['image_caption'] = {'enabled': True, 'provider': 'follow_llm'}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    out = {}
    lib = plugin._sticker_lib()
    now = time.time()
    if CASE in ('reply', 'off', 'alone', 'fallback', 'forget', 'held'):
        lib.add(png(3, 3, 7), now, source='self', from_qq='10001', from_where='group:' + A,
                look={'caption': '一只在笑的猫', 'emotion': '开心', 'scene': '夸人'})
        lib.add(png(3, 3, 8), now, source='owner', from_qq=OWNER, note='主人给的兔子')
        lib.add(png(3, 3, 9), now, source='self', from_qq='10002', from_where='group:' + A,
                look={'caption': '一只在哭的狗', 'emotion': '难过', 'scene': '安慰'})
    by_caption = {r['caption']: sid for sid, r in lib.rows.items()}

    def reply(text, bot=None, words='小爱 夸夸我', forbid=''):
        event = Event(words, wake=True, bot=bot)
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_message(event))
        loop.run_until_complete(plugin.on_llm_request(event, req))
        if forbid:   # something labelled "这里不能讲" in this reply's prompt (made up)
            plugin._forbid(event, 'm-x', text=forbid, people=['10002'])
        prompt = '\n'.join(p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts)
        offered = list(getattr(event, mixin_stickers.OFFERED_ATTR, None) or [])
        resp = LLMResponse(text)
        loop.run_until_complete(plugin.on_llm_response(event, resp))
        harness.drain(loop)
        chain = getattr(resp, 'result_chain', None)
        return {'offer_in_prompt': '[她的表情包]' in prompt, 'offered': [lib.rows[s]['caption'] for s in offered],
                'prompt_offer': [ln for ln in prompt.splitlines() if ln[:2] in ('1.', '2.', '3.')],
                'stopped': event.stopped, 'text': resp.completion_text,
                'chain': [(type(c).__name__, getattr(c, 'text', getattr(c, 'id', None)))
                          for c in (chain.chain if chain is not None else [])],
                'sent_flag': bool(getattr(event, '_ams_sticker_sent', False))}

    if CASE == 'off':
        bot = Bot()
        out['r'] = reply('好呀[表情包:1]', bot)
        out['calls'] = bot.calls
        out['old_mark'] = reply('好呀[表情包：一只 在笑的猫]', bot)['text']   # from her history: never sent
    elif CASE == 'held':
        # the send check is on; the sticker's label is about something that may not be said here
        bot = Bot()
        out['r'] = reply('好呀，你最棒\n[表情包:1]', bot, forbid='一只在笑的猫')
        out['calls'] = len(bot.calls)
        out['sent'] = sent
    elif CASE == 'reply':
        bot = Bot()
        out['named'] = reply('好呀，你最棒\n[表情包:1]', bot)
        out['calls'] = [{'action': c['action'], 'group_id': c['params'].get('group_id'),
                         'segments': [(s['type'], s['data'].get('sub_type'), s['data'].get('summary'),
                                       str(s['data'].get('file', ''))[:9]) for s in c['params']['message']],
                         'keys': sorted(c['params'])} for c in bot.calls]
        first = lib.rows[by_caption[out['named']['offered'][0]]]
        out['uses_after'] = first['uses']
        out['not_offered'] = reply('嗯嗯[表情包:9]', bot)
        out['face_stays'] = reply('好的[表情:微笑]', bot)
        out['calls_total'] = len(bot.calls)
        win = next(iter((DATA / 'phone').glob('group_*.json')))
        out['phone'] = [x.get('text') for x in json.loads(win.read_text('utf-8'))['recent'] if x.get('role') == 'assistant']
        out['sent'] = sent
    elif CASE == 'alone':
        bot = Bot()
        out['r'] = reply('[表情包:1]', bot)
        out['calls'] = len(bot.calls)
        win = next(iter((DATA / 'phone').glob('group_*.json')))
        out['phone'] = [x.get('text') for x in json.loads(win.read_text('utf-8'))['recent'] if x.get('role') == 'assistant']
    elif CASE == 'fallback':
        out['r'] = reply('好呀[表情包:1]', Bot(fail=True))
        out['sent'] = sent
        out['r_nobot'] = reply('好呀[表情包:1]', None)
        out['sent_total'] = len(sent)
    elif CASE == 'look':
        # in passing: QQ stickers in a group, nobody called her
        ev = Event('哈哈哈', raw_images=['https://gchat.qpic.cn/a.png', 'https://gchat.qpic.cn/b.png',
                                        'https://gchat.qpic.cn/c.png', 'https://evil.example/x.png'])
        loop.run_until_complete(plugin.on_message(ev))
        harness.drain(loop)
        out['looks'] = list(ctx.provider.looks)
        out['fetched'] = list(fetched)
        out['kept'] = [(r['caption'], r['from_qq'], r['from_where'], r['source']) for r in lib.rows.values()]
        cache = json.loads((DATA / 'image_cache.json').read_text('utf-8'))
        out['cache'] = sorted((v['caption'], v.get('from_qq'), v.get('where')) for k, v in cache.items() if not k.startswith('content:'))
        out['content_cache'] = sorted(v['caption'] for k, v in cache.items() if k.startswith('content:'))
        # the same again: no second look
        loop.run_until_complete(plugin.on_message(Event('再来', raw_images=['https://gchat.qpic.cn/a.png'])))
        harness.drain(loop)
        out['looks_after'] = len(ctx.provider.looks)
        out['spend_kinds'] = sorted(json.loads(mixin_attention.SPEND_PATH.read_text('utf-8'))[time.strftime('%Y-%m-%d')])
        # someone deleted: his stickers are not looked at for keeping
        loop.run_until_complete(plugin.page_forget_person('10002'))
        loop.run_until_complete(plugin.on_message(Event('嘿', sender='10002', name='柠檬',
                                                        raw_images=['https://gchat.qpic.cn/d.png'])))
        harness.drain(loop)
        out['kept_after_gone'] = len(lib.rows)
        out['looks_after_gone'] = len(ctx.provider.looks)
    elif CASE == 'page':
        # the owner's page: list, one picture, add (a picture only), delete; nobody's number shown
        lib.add(png(3, 3, 7), now - 86400 * 2, source='self', from_qq='10001', from_where='group:' + A,
                look={'caption': '一只在笑的猫', 'emotion': '开心', 'scene': '夸人'})
        lib.add(png(3, 3, 9), now - 86400, source='self', from_qq='10002', from_where='private:10002',
                look={'caption': '一只在哭的狗', 'emotion': '难过', 'scene': '安慰'})
        lib.add(png(3, 3, 5), now - 86400 * 28, source='old', look={'caption': '旧的猫'})

        def go(coro):
            return loop.run_until_complete(coro)
        first = go(plugin.page_stickers({'sort': 'saved'}))['data']
        out['list'] = [(x['caption'], x['from'], x['owner'], x['days_left']) for x in first['items']]
        out['list_text'] = json.dumps(first, ensure_ascii=False)
        out['counts'] = first['counts']
        out['sources'] = first['sources']
        out['soon'] = [x['caption'] for x in go(plugin.page_stickers({'sort': 'soon'}))['data']['items']]
        out['only_sad'] = [x['caption'] for x in go(plugin.page_stickers({'emotion': '难过'}))['data']['items']]
        sid = first['items'][0]['id']
        img = go(plugin.page_sticker_image({'id': sid}))
        out['image'] = (img['status'], img['data']['url'][:22])
        out['image_missing'] = go(plugin.page_sticker_image({'id': '../index.json'}))['status']
        import base64
        b64 = base64.b64encode(png(8, 8, 1)).decode()
        out['add'] = go(plugin.page_sticker_add({'picture': 'data:image/png;base64,' + b64, 'note': '主人的小猫'}))['status']
        out['add_html'] = go(plugin.page_sticker_add({'picture': base64.b64encode(b'<html><script>x</script></html>').decode()}))
        out['add_svg_named_png'] = go(plugin.page_sticker_add({'picture': 'data:image/png;base64,' +
                                                               base64.b64encode(b'<svg onload=1></svg>').decode()}))['status']
        out['add_big'] = go(plugin.page_sticker_add({'picture': 'A' * (8 * 1024 * 1024)}))['status']
        out['add_huge_side'] = go(plugin.page_sticker_add({'picture': base64.b64encode(png(5000, 1, 1)).decode()}))['status']
        owner_row = next(r for r in lib.rows.values() if r['source'] == 'owner')
        out['owner_row'] = (owner_row['caption'], owner_row['from_qq'], owner_row['from_where'])
        # the owner's gift: never swept, not counted; she sweeps a year later, it stays
        lib.sweep(now + 86400 * 365)
        out['after_sweep'] = sorted(r['caption'] for r in lib.rows.values())
        gift = next(sid for sid, r in lib.rows.items() if r['source'] == 'owner')
        out['delete_gift'] = go(plugin.page_sticker_delete({'id': gift}))['status']
        out['delete_again'] = go(plugin.page_sticker_delete({'id': gift}))['status']
        out['left'] = sorted(r['caption'] for r in lib.rows.values())
        # deleted on the page: its fingerprint alone is remembered; she does not keep it again
        out['dropped_file'] = json.loads((DATA / 'stickers' / 'dropped.json').read_text('utf-8'))
        out['gift_id'] = gift
        again = stickers.Library(DATA / 'stickers')
        out['keep_again'] = list(again.add(png(8, 8, 1), now, source='self', from_qq='10001'))
        out['owner_again'] = go(plugin.page_sticker_add({'picture': b64}))['status']
    elif CASE == 'vision_status':
        def status():
            return loop.run_until_complete(plugin.page_status())['data']
        plugin.llm_functions['image_caption']['enabled'] = False
        out['off_empty'] = 'vision' in status()
        plugin.llm_functions['image_caption']['enabled'] = True
        out['on_empty'] = 'vision' in status()
        event = Event('look', wake=True)
        plugin._image_refs = lambda _event: ['https://gchat.qpic.cn/b.png']
        loop.run_until_complete(plugin._image_context(event))
        out['on_used'] = status().get('vision')
        plugin.llm_functions['image_caption']['enabled'] = False
        out['off_used'] = status().get('vision')
    elif CASE in ('count_astrbot', 'count_api'):
        import base64
        import vision
        from unittest.mock import patch

        plugin.config.update(vision_price_per_call='0', vision_image_api_model='made-up-model')
        calls = []
        async def answer(*args, **kwargs):
            calls.append((kwargs.get('image_urls') or [''])[0])
            return harness.FakeResponse(json.dumps({'caption': 'a made-up picture', 'kind': 'photo', 'keep': False}))
        ctx.provider.text_chat = answer
        vision.ImageAPI.text_chat = answer
        plugin._image_refs = lambda event: [event.vision_ref]
        date = ['2026-10-30']
        def fake_date(fmt, *args):
            return date[0] if fmt == '%Y-%m-%d' else '00:00'
        def go(coro):
            return loop.run_until_complete(coro)
        def reply_picture(index):
            ev = Event('reply', wake=True)
            ev.vision_ref = 'https://gchat.qpic.cn/reply%s.png' % index
            return go(plugin._image_context(ev))
        def passing_picture(index):
            ref = 'https://gchat.qpic.cn/passing%s.png' % index
            return go(plugin._look_at_sticker_in_passing(Event('talk', raw_images=[ref])))
        def owner_picture(index):
            data = base64.b64encode(png(3, 3, index + 100)).decode()
            return go(plugin.page_sticker_add({'picture': data}))
        with patch.object(vision.time, 'strftime', side_effect=fake_date):
            offset = 1 if CASE == 'count_api' else 0
            marks = {}
            for i in range(34):
                plugin.llm_functions['image_caption']['provider'] = 'image_api' if (i + offset) % 2 else 'follow_llm'
                reply_picture(i)
                if len(calls) in (31, 100):
                    marks[str(len(calls))] = len(calls)
                plugin.llm_functions['image_caption']['provider'] = 'follow_llm' if (i + offset) % 2 else 'image_api'
                passing_picture(i)
                if len(calls) in (31, 100):
                    marks[str(len(calls))] = len(calls)
                gift = owner_picture(i)
                if len(calls) in (31, 100):
                    marks[str(len(calls))] = len(calls)
            out['marks'] = marks
            out['calls'] = len(calls)
            out['last_gift'] = {'status': gift['status'], 'labelled': gift['data']['labelled']}
            out['panel'] = go(plugin.page_status())['data']['vision']
            plugin.self_decide = False
            out['panel_without_decide'] = go(plugin.page_status())['data']['vision']
            out['spent'] = plugin._spent_today()
            date[0] = '2026-10-31'
            out['panel_next_day'] = 'vision' in go(plugin.page_status())['data']
            reply_picture(35)
            out['calls_next_day'] = len(calls)
            out['panel_after_next'] = go(plugin.page_status())['data']['vision']
    elif CASE == 'forget':
        cache = {'k1': stickers.cache_entry('https://gchat.qpic.cn/m.png', {'caption': '芒果的图'}, '10001', 'group:' + A, now),
                 'k2': stickers.cache_entry('https://gchat.qpic.cn/l.png', {'caption': '柠檬的图'}, '10002', 'group:' + A, now)}
        (DATA / 'image_cache.json').write_text(json.dumps(cache, ensure_ascii=False), 'utf-8')
        got = loop.run_until_complete(plugin.page_forget_person('10001'))
        out['result'] = got.get('data') if isinstance(got, dict) else got
        out['left'] = sorted(r['caption'] for r in plugin._sticker_lib().rows.values())
        out['cache_left'] = sorted(v['caption'] for v in json.loads((DATA / 'image_cache.json').read_text('utf-8')).values())
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), 'utf-8')


run()
