"""Scripted turns for test_selfie (her camera and her voice, mixin_selfie.py); prints a JSON
result. Run in a fresh interpreter:
    PYTHONHASHSEED=0 python tests/media_cases.py <empty data dir> <out.json> <case>

The two services are replaced by fakes that write a small file; nothing goes to the network.
All words and numbers are made up.
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
import mixin_selfie  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

ASK = '发张自拍看看你，再发语音说句话'
REPLY = '我在窗边看书呢'


class Event(harness.FakeEvent):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.sent = []
        self.stopped = False

    async def send(self, chain):
        self.sent.append([type(c).__name__ for c in chain.chain])

    def stop_event(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped


def run():
    if CASE in ('on', 'limit', 'held'):
        settings = {'selfie_enabled': True, 'voice_enabled': True}
        if CASE == 'limit':
            settings.update(selfie_daily_limit=1, voice_daily_limit=1)
        DATA.mkdir(parents=True, exist_ok=True)
        mixin_selfie.SETTINGS_PATH.write_text(json.dumps(settings), 'utf-8')
    ctx = harness.FakeContext()
    plugin = main.BioCorePlugin(ctx, config={'global_memory': True} if CASE == 'held' else {})
    plugin._ipv4_json = harness.fake_ipv4_json
    asked = {'selfie': [], 'voice': []}

    async def selfie(scene):
        asked['selfie'].append(scene)
        mixin_selfie.SELFIE_DIR.mkdir(parents=True, exist_ok=True)
        path = mixin_selfie.SELFIE_DIR / ('s%d.png' % len(asked['selfie']))
        path.write_bytes(b'png')
        return path

    async def voice(text):
        asked['voice'].append(text)
        mixin_selfie.SELFIE_DIR.mkdir(parents=True, exist_ok=True)
        path = mixin_selfie.SELFIE_DIR / ('v%d.wav' % len(asked['voice']))
        path.write_bytes(b'wav')
        return path

    plugin._make_selfie, plugin._make_voice = selfie, voice
    if CASE == 'held':   # the last look held the reply back: nothing is sent, so nothing is said aloud
        async def held(event, response, reply):
            event.stop_event()
            return ''
        plugin._look_at_reply = held
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    out = {'turns': []}
    for i in range(2 if CASE == 'limit' else 1):
        clock.advance(60)
        event = Event(ASK + str(i), sender='10001', name='芒果')
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_message(event))
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(REPLY)))
        harness.drain(loop)
        out['turns'].append(event.sent)
    out['asked'] = asked
    out['counters'] = json.loads(mixin_selfie.COUNTER_PATH.read_text('utf-8')) if mixin_selfie.COUNTER_PATH.exists() else {}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), 'utf-8')


run()
