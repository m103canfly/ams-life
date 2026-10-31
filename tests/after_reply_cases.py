# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Compare the two reply paths in a fresh offline process."""
import asyncio
import json
import sys
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA, OUT, MODE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
harness.prepare(DATA)
import main  # noqa: E402
import attention  # noqa: E402
import events  # noqa: E402
import mixin_attention  # noqa: E402
import turn  # noqa: E402
from astrbot.api.event import MessageChain  # noqa: E402
from astrbot.api.message_components import Face, Plain, Reply  # noqa: E402
from astrbot.api.provider import LLMResponse, ProviderRequest  # noqa: E402


async def run():
    plugin = main.BioCorePlugin(harness.FakeContext(), config={'self_decide': True})
    plugin._ipv4_json = harness.fake_ipv4_json
    results = []
    texts = ['hello[表情:微笑]', 'first【下一条】second', 'hello<bc>{}</bc>',
             'ok', '【不说】', '普通回复', 'ok']
    for index, text in enumerate(texts):
        event = harness.FakeEvent('test ' + str(index), sender='10001')
        rest = []

        async def send_rest(event, umo, parts, then=None, sticker_part=None):
            rest.extend(parts)
            return True

        plugin._send_rest = send_rest
        await plugin.on_message(event)
        await plugin.on_llm_request(event, ProviderRequest(prompt=event.message_str))
        plugin.global_memory = index == 5
        if index == 5:
            async def fail(event, reply):
                raise RuntimeError('test')
            plugin._check_reply = fail
        if MODE == 'astrbot':
            response = (LLMResponse('', MessageChain([Reply(id='900001'), Plain('ok')]))
                        if index == 3 else LLMResponse(text))
            if index == 6:
                response.raw_completion = types.SimpleNamespace(usage=types.SimpleNamespace(
                    prompt_cache_hit_tokens=300, prompt_cache_miss_tokens=500, completion_tokens=200))
            before = response.result_chain
            await plugin.on_llm_response(event, response)
            chain = response.result_chain if response.result_chain is not before else None
            first = None if chain is None else [('text', c.text) if isinstance(c, Plain) else
                                                 ('face', c.id) if isinstance(c, Face) else ('reply', c.id)
                                                 for c in chain.chain]
            cleared = not response.completion_text
        else:
            response = turn.TurnReply(text=text, chain_prefix=[events.Segment('reply', {'id': '900001'})]
                                      if index == 3 else [], usage={'input_hit': 300, 'input_miss': 500,
                                      'output': 200} if index == 6 else {})
            await plugin._after_reply(event, response)
            plugin._group_reply_after(event)
            first = None if response.first_message is None else [
                (segment.type, segment.data.get('text', segment.data.get('id'))) for segment in response.first_message]
            cleared = not response.text
        await asyncio.sleep(0)
        note = plugin._check_note(event)
        recent = plugin._read_window(plugin._here(event))['recent']
        ledger = json.loads(mixin_attention.SPEND_PATH.read_text('utf-8'))
        results.append({'sent': note.get('sent'), 'outcome': note.get('outcome'), 'stopped': event.stopped,
                        'first': first, 'rest': rest, 'cleared': cleared,
                        'kept': recent[-1]['text'] if recent else None,
                        'spend': ledger.get(time.strftime('%Y-%m-%d'), {}).get('reply', 0)})
    return {'rounds': results, 'price': plugin._attention_cfg()['prices']}


OUT.write_text(json.dumps(asyncio.run(run()), ensure_ascii=False), encoding='utf-8')
