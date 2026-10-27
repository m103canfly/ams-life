"""A scripted conversation driven through the plugin's hooks; prints a JSON trace of everything observable.

Run in a fresh interpreter with a fixed hash seed (the golden test does this):
    PYTHONHASHSEED=0 python3 tests/scenario.py <empty data dir> <trace.json> [basic|full]

basic = default config. full = every optional LLM function on, safety on, autonomy on with a fixed noise seed,
so the proposal-only paths and the private autonomy bookkeeping run too.
"""
import asyncio
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA, OUT = Path(sys.argv[1]), Path(sys.argv[2])
MODE = sys.argv[3] if len(sys.argv) > 3 else 'basic'
clock = harness.prepare(DATA)

import main  # noqa: E402
from astrbot.api import logger  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

GROUP_A, GROUP_B = '900001', '900002'
TAG_JOY = '<bc>{"e":"joy","i":0.6}</bc>'
TAG_SAD = '<bc>{"e":"sadness","i":0.4,"n":"be_heard"}</bc>'

# (seconds since previous turn, event, model reply)
SCRIPT = [
    (0, dict(text='小爱早呀，今天想听你唱歌', sender='10001', name='芒果'), '早呀~ 想听哪首？' + TAG_JOY),
    (90, dict(text='就唱上次那首吧', sender='10001', name='芒果'), '好嘞，哼哼' + TAG_JOY),
    (600, dict(text='小爱 你说今天抽卡会不会歪', sender='10002', name='柠檬', group=GROUP_A), '别灰心嘛'),
    (40, dict(text='我已经歪了三次了 心态崩了', sender='10003', name='阿星', group=GROUP_A), '抱抱，下次一定出' + TAG_SAD),
    (40, dict(text='小爱帮我们算算保底还差多少', sender='10002', name='柠檬', group=GROUP_A), '我算算哦' + TAG_JOY),
    (3600, dict(text='小爱 晚上好', sender='10004', name='桃子', group=GROUP_B), '晚上好~'),
    (120, dict(text='最近工作好累啊', sender='10004', name='桃子', group=GROUP_B), '辛苦啦，快去歇会儿' + TAG_SAD),
    (7200, dict(text='明天要考试了 好紧张', sender='10001', name='芒果'), '你可以的！' + TAG_JOY),
    (30, dict(text='你还记得我早上让你唱什么吗', sender='10001', name='芒果'), '上次那首嘛~'),
    (86400, dict(text='小爱 我考完了', sender='10001', name='芒果'), '考得怎么样？' + TAG_JOY),
    (300, dict(text='小爱 今天群里好安静', sender='10002', name='柠檬', group=GROUP_A), '是诶，大家都去哪了'),
    (60, dict(text='小爱 你是AI吗', sender='10005', name='路人', group=GROUP_A), '是呀，按爱弥斯的设定在聊~'),
    (172800, dict(text='好久不见小爱', sender='10004', name='桃子', group=GROUP_B), '好久不见！' + TAG_JOY),
    (20, dict(text='我换工作了 现在轻松多了', sender='10004', name='桃子', group=GROUP_B), '太好了！' + TAG_JOY),
    # strong feelings: should push the core over the archive thresholds
    (30, dict(text='太开心了！！！我终于抽到了！！！', sender='10002', name='柠檬', group=GROUP_A),
     '恭喜恭喜！<bc>{"e":"joy","i":0.95}</bc>'),
    (20, dict(text='啊啊啊啊 好激动 小爱快夸我', sender='10002', name='柠檬', group=GROUP_A),
     '超厉害的！<bc>{"e":"joy","i":0.9,"x":"open"}</bc>'),
    (400, dict(text='小爱 我好难过 想哭', sender='10001', name='芒果'),
     '我在呢<bc>{"e":"sadness","i":0.9,"n":"be_heard"}</bc>'),
    (20, dict(text='今天被骂了 真的很委屈', sender='10001', name='芒果'), '抱抱你<bc>{"e":"sadness","i":0.85}</bc>'),
    (20, dict(text='气死我了！！！他凭什么这样说我', sender='10001', name='芒果'), '太过分了<bc>{"e":"anger","i":0.8}</bc>'),
    (30, dict(text='真的受够了！！！气死了！！！', sender='10001', name='芒果'), '先别气坏自己<bc>{"e":"anger","i":0.9}</bc>'),
    (620, dict(text='我还是好生气！！！凭什么啊！！！', sender='10001', name='芒果'), '我陪着你<bc>{"e":"anger","i":0.9}</bc>'),
    (400, dict(text='小爱 我们约好下周一起打副本吧', sender='10003', name='阿星', group=GROUP_A), '好呀，说定了~'),
    (30, dict(text='记得提醒我明天交报告', sender='10003', name='阿星', group=GROUP_A), '记下啦'),
    (3600, dict(text='小爱 报告我交了', sender='10003', name='阿星', group=GROUP_A), '太好了~' + TAG_JOY),
]

FULL_CONFIG = {'llm_only_reply_summary': False, 'safety_enabled': True, 'we_memory_enabled': True,
               'proactive_autonomy': True, 'autonomy_loop_enabled': True, 'noise_seed': 7,
               'bc_prompt_mode': 'semantic', 'memory_worthiness_enabled': False}


def files_snapshot(root):
    out = {}
    for path in sorted(p for p in root.rglob('*') if p.is_file()):
        rel = str(path.relative_to(root))
        text = path.read_text('utf-8', errors='replace')
        if path.suffix == '.json':
            try:
                out[rel] = json.loads(text)
                continue
            except ValueError:
                pass
        if path.suffix == '.jsonl':
            out[rel] = [json.loads(line) if line.strip().startswith('{') else line for line in text.splitlines()]
            continue
        out[rel] = text
    return out


def main_run():
    ctx = harness.FakeContext()
    plugin = main.BioCorePlugin(ctx, config=dict(FULL_CONFIG) if MODE == 'full' else {})
    plugin._ipv4_json = harness.fake_ipv4_json
    if MODE == 'full':
        plugin.llm_functions = {k: {'enabled': True, 'provider': 'follow_llm'} for k in main.LLM_FUNCTIONS}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    trace = {'routes': list(ctx.web_routes), 'turns': []}
    for delay, ev, reply in SCRIPT:
        clock.advance(delay)
        event = harness.FakeEvent(**ev)
        req = ProviderRequest(prompt=event.message_str, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        resp = LLMResponse(reply)
        loop.run_until_complete(plugin.on_llm_response(event, resp))
        harness.drain(loop)
        trace['turns'].append({
            'session': event.unified_msg_origin,
            'inject': [p.get('text') if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts],
            'system': req.system_prompt,
            'clean': resp.completion_text,
        })
    if MODE == 'full':
        ticks = []
        for _ in range(3):
            clock.advance(300)
            try:
                loop.run_until_complete(plugin._autonomy_tick())
                ticks.append('ok')
            except Exception as exc:
                ticks.append('error: ' + type(exc).__name__)
            harness.drain(loop)
        trace['autonomy_ticks'] = ticks
    for sub in ('readiness', 'learning'):
        event = harness.FakeEvent('/biocore ' + sub, sender='10001', name='芒果')
        loop.run_until_complete(plugin.biocore_command(event))
        chain = getattr(event.result, 'chain', [])
        trace['command_' + sub] = [getattr(c, 'text', '') for c in chain]
    clock.advance(3600)
    try:
        trace['page_status'] = loop.run_until_complete(plugin.page_status())
    except Exception as exc:  # recorded, not raised: the trace shows it either way
        trace['page_status'] = 'error: ' + type(exc).__name__
    harness.drain(loop)
    for task in asyncio.all_tasks(loop):
        task.cancel()
    trace['provider_prompts'] = ctx.provider.prompts
    trace['log'] = [r for r in logger.records if r[0] in ('warning', 'error')]
    trace['files'] = files_snapshot(DATA)
    OUT.write_text(json.dumps(trace, ensure_ascii=False, indent=1, sort_keys=True, default=str), 'utf-8')


main_run()
