"""Offline harness: fake AstrBot context, events, model and embeddings, a frozen clock and seeded randomness.

Everything here is deterministic so a scripted conversation produces the same trace on every run. The trace is the
safety net for refactoring: `tests/golden/*.json` holds the trace of the unmodified code, and the golden test re-runs the
scenario in a fresh interpreter (fixed PYTHONHASHSEED) and compares.
"""
import asyncio
import hashlib
import json
import math
import os
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STUBS = HERE / 'stubs'


class Clock:
    def __init__(self, start):
        self.now = float(start)

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += float(seconds)


def prepare(data_dir, start=1_793_000_000.0):
    """Call before importing main: data dir, time zone, frozen clock, seeded random. Returns the clock."""
    os.environ['AMS_LIFE_DATA_DIR'] = str(data_dir)
    if hasattr(time, 'tzset'):
        os.environ['TZ'] = 'Asia/Shanghai'
        time.tzset()
    else:
        # Windows: the C runtime reads TZ on the first localtime() call but only understands POSIX-style values;
        # 'Asia/Shanghai' would silently mean UTC. 'CST-8' is the same UTC+8 (no DST in China since 1991).
        os.environ['TZ'] = 'CST-8'
    for path in (str(STUBS), str(ROOT)):
        if path not in sys.path:
            sys.path.insert(0, path)
    clock = Clock(start)
    time.time = clock

    original = random.Random

    class SeededRandom(original):
        made = 0

        def __init__(self, x=None):
            if x is None:
                SeededRandom.made += 1
                x = 7919 * SeededRandom.made
            super().__init__(x)

    random.Random = SeededRandom
    return clock


def astrbot_user_message(req):
    """What AstrBot (4.29.3) makes of this turn's user message from a ProviderRequest: what
    the model is sent, and what the conversation history keeps. A part marked "_no_save"
    is sent (without the mark: provider/sources/openai_source.py) but not kept
    (agent/message.py, dump_messages_with_checkpoints)."""
    blocks = [{'type': 'text', 'text': req.prompt}] if getattr(req, 'prompt', None) else []
    for part in getattr(req, 'extra_user_content_parts', None) or []:
        blocks.append(dict(part) if isinstance(part, dict) else {'type': 'text', 'text': str(part)})
    sent = [{k: v for k, v in b.items() if k != '_no_save'} for b in blocks]
    kept = [{k: v for k, v in b.items() if k != '_no_save'} for b in blocks if not b.get('_no_save')]
    return sent, kept


def fake_vector(text, dims=24):
    """Deterministic bag-of-characters embedding: similar texts get similar vectors."""
    vec = [0.0] * dims
    for ch in str(text):
        h = int(hashlib.md5(ch.encode('utf-8')).hexdigest(), 16)
        vec[h % dims] += 1.0 if (h >> 8) % 2 else -1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [round(v / norm, 6) for v in vec]


def fake_ipv4_json(url, headers, payload, timeout=None):
    if str(url).endswith('/embeddings'):
        return {'data': [{'embedding': fake_vector(t)} for t in payload.get('input') or []]}
    raise OSError('network disabled in tests: ' + str(url))


class FakeResponse:
    def __init__(self, text):
        self.completion_text = text
        self.result_chain = None


class FakeProvider:
    """Answers the plugin's summary prompts with fixed JSON; records every prompt."""

    def __init__(self):
        self.prompts = []
        self.provider_config = {'id': 'fake-chat', 'model': 'fake-chat', 'provider_type': 'chat_completion'}

    def meta(self):
        return type('Meta', (), {'id': 'fake-chat', 'model': 'fake-chat', 'type': 'chat_completion'})()

    async def text_chat(self, prompt='', system_prompt=None, **kwargs):
        self.prompts.append(str(prompt)[:80])
        p = str(prompt)
        if '聊天记录总结成一个 JSON' in p:
            # summarise by echoing the source lines, so the plugin's source check finds them
            lines = [ln[2:].strip() for ln in p.splitlines() if ln.startswith('- ')]
            body = '；'.join(lines)
            return FakeResponse(json.dumps({
                'title': (lines[-1] if lines else '一件事')[:12], 'event': body, 'meaning_to_her': '她很在意这件事',
                'reflection': '要好好记住', 'big_summary': body, 'small_summary': body[:60],
                'emotion_nuance': ['委屈'],
                'emotion_layers': [{'emotion': 'anger', 'intensity': 0.8, 'confidence': 0.9,
                                    'centrality': 0.8, 'evidence': (lines[-1] if lines else '')[:20]}]},
                ensure_ascii=False))
        if '长期记忆整理成一个 JSON' in p:
            return FakeResponse(json.dumps({'summary': '常和群友聊游戏', 'candidates': [
                {'text': '喜欢聊抽卡', 'source': 'told', 'confidence': 0.8, 'kind': 'add'}]}, ensure_ascii=False))
        return FakeResponse('{}')


class FakeEmbeddingProvider:
    provider_config = {'id': 'fake-embed', 'provider_type': 'embedding', 'embedding_api_base': 'http://embed.test/v1',
                       'embedding_model': 'fake-embed', 'embedding_api_key': ''}


class FakePersonaManager:
    def get_persona_v3_by_id(self, pid):
        return None

    async def get_default_persona_v3(self, umo=None):
        return {'name': 'xiaoai', 'prompt': '你是小爱。'}

    personas_v3 = []


class FakeKB:
    async def list_kbs(self):
        return []

    async def retrieve(self, **kwargs):
        return {'context_text': ''}


class FakeContext:
    def __init__(self):
        self.kb_manager = FakeKB()
        self.provider = FakeProvider()
        self.persona_manager = FakePersonaManager()
        self.web_routes = []
        self.config = {'provider_settings': {'enable': True}}

    def get_config(self, umo=None):
        return self.config

    def get_all_providers(self):
        return [self.provider]

    def get_all_embedding_providers(self):
        return [FakeEmbeddingProvider()]

    def get_all_tts_providers(self):
        return []

    def get_provider_by_id(self, pid):
        return self.provider if pid == 'fake-chat' else None

    async def get_using_provider_async(self, umo=None):
        return self.provider

    def get_using_provider(self, umo=None):
        return self.provider

    async def get_using_stt_provider_async(self, umo=None):
        return None

    def register_web_api(self, route, handler, methods, desc):
        self.web_routes.append(route)


class FakeEvent:
    def __init__(self, text, sender='10001', name='柠檬', group=None, self_id='20002'):
        self.message_str = text
        self._sender, self._name, self._group = str(sender), name, group
        self.unified_msg_origin = (f'default:GroupMessage:{group}' if group else f'default:FriendMessage:{sender}')
        self.message_obj = type('Obj', (), {'self_id': self_id, 'message_id': 'm' + text[:6]})()
        self.result = None
        self.stopped = False
        self.is_at_or_wake_command = True  # a turn wakes her (AstrBot's wake check)

    def get_sender_id(self):
        return self._sender

    def stop_event(self):
        self.stopped = True

    def get_sender_name(self):
        return self._name

    def get_group_id(self):
        return self._group or ''

    def is_private_chat(self):
        return not self._group

    def get_messages(self):
        from astrbot.api.message_components import Plain
        return [Plain(self.message_str)]

    def get(self, key, default=None):
        return default

    def set_result(self, result):
        self.result = result

    async def send(self, chain):
        return None


FOREVER = ('_autonomy_loop',)   # background loops that never finish on their own; the scenario ticks them by hand


def drain(loop):
    """Run the loop until every background task the plugin created has finished (endless loops excluded)."""
    for _ in range(20):
        pending = [t for t in asyncio.all_tasks(loop)
                   if not t.done() and getattr(t.get_coro(), '__name__', '') not in FOREVER]
        if not pending:
            return
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
