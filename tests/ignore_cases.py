"""Scripted runs for the ignore_senders tests; prints a JSON result.

Run in a fresh interpreter (test_ignore_senders does this):
    PYTHONHASHSEED=0 python tests/ignore_cases.py <empty data dir> <out.json> <case>

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
OTHER_BOT = '10099'   # made up: another bot in the group, on the list

import main  # noqa: E402
from astrbot.api.message_components import At, Plain  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402

config = {'ignore_senders': [OTHER_BOT, ' 10098 ', 'not a number']} if CASE == 'listed' else {}
config['reply_groups'] = [G1]
plugin = main.BioCorePlugin(harness.FakeContext(), config=config)
plugin._ipv4_json = harness.fake_ipv4_json
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class Event(harness.FakeEvent):
    """A message as AstrBot hands it over, with AstrBot's stop flag."""

    def __init__(self, parts, text, sender, name, woken):
        super().__init__(text, sender=sender, name=name, group=G1, self_id=HER)
        self._parts, self.stopped = parts, False
        self.is_at_or_wake_command = woken
        self.message_obj.message_id = 'm-%s-%d' % (sender, int(clock.now))

    def get_messages(self):
        return self._parts

    def stop_event(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped


model_calls = []


def message(parts, text, sender, name, woken):
    """AstrBot's order: the plugins' handlers; then, if woken and not stopped, the model."""
    clock.advance(60)
    event = Event(parts, text, sender, name, woken)
    loop.run_until_complete(plugin.on_message(event))
    harness.drain(loop)
    if woken and not event.is_stopped():
        req = ProviderRequest(prompt=text, system_prompt='你是小爱。')
        loop.run_until_complete(plugin.on_llm_request(event, req))
        if not event.is_stopped():
            model_calls.append(sender)
            loop.run_until_complete(plugin.on_llm_response(event, LLMResponse('你好呀')))
        harness.drain(loop)
    return event


def phone():
    return [(x.get('sender_id'), x['text']) for x in plugin._read_window('group:' + G1)['recent']]


result = {}
a = message([At(qq=HER, name='小爱bot'), Plain(text=' 欢迎新人！')], '@小爱bot(20002) 欢迎新人！', OTHER_BOT, '机器人',
            True)
b = message([Plain(text='今天天气不错')], '今天天气不错', OTHER_BOT, '机器人', False)
c = message([At(qq=HER, name='小爱bot'), Plain(text=' 你好')], '@小爱bot(20002) 你好', '10002', '柠檬', True)
d = message([Plain(text='问问 '), At(qq=OTHER_BOT, name='机器人'), Plain(text=' 在吗')], '问问 @机器人(10099) 在吗',
            '10002', '柠檬', False)
e = message([Plain(text='我也在')], '我也在', '10098', '另一个', False)
result['stopped'] = [x.stopped for x in (a, b, c, d, e)]
result['model_calls'] = model_calls
result['phone'] = phone()
result['names'] = sorted(plugin._names_index())
result['seen'] = plugin._core(c).seen_need if hasattr(plugin._core(c), 'seen_need') else None
# the later hooks stop him too, should AstrBot ever get that far
late = Event([Plain(text='在吗')], '在吗', OTHER_BOT, '机器人', True)
req = ProviderRequest(prompt='在吗', system_prompt='你是小爱。')
loop.run_until_complete(plugin.on_llm_request(late, req))
result['late_request_stopped'] = late.stopped
result['late_request_untouched'] = req.system_prompt == '你是小爱。' and not req.extra_user_content_parts
late2 = Event([Plain(text='在吗')], '在吗', OTHER_BOT, '机器人', True)
loop.run_until_complete(plugin.on_llm_response(late2, LLMResponse('嗯')))
harness.drain(loop)
result['late_response_stopped'] = late2.stopped
result['phone_after'] = phone()

for task in asyncio.all_tasks(loop):
    task.cancel()
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), 'utf-8')
