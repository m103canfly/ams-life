"""Offline tests for her phone. All services and pages are fake."""
import asyncio
import base64
import json
import sys
import tempfile
import types
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import AsyncMock, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402
import test_basics  # noqa: E402,F401  # reuse its AstrBot setup without replacing the clock


class FunctionTool:
    def __init__(self, name, description='', parameters=None, handler=None):
        self.name, self.description, self.parameters, self.handler = name, description, parameters, handler


class ToolSet:
    def __init__(self, tools=None):
        self.tools = list(tools or [])

    def names(self):
        return [tool.name for tool in self.tools]

    def add_tool(self, tool):
        self.tools.append(tool)

    def remove_tool(self, name):
        self.tools = [tool for tool in self.tools if tool.name != name]

    def __bool__(self):
        return bool(self.tools)


import main  # noqa: E402
import mixin_selfie as phone  # noqa: E402
import mixin_browse  # noqa: E402
from astrbot.api.message_components import Image, Record  # noqa: E402
from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402


class Event(harness.FakeEvent):
    def __init__(self, components=()):
        super().__init__('虚构消息', sender='10005', name='小甲')
        self.components = list(components)
        self.sent = []
        self.stopped = False

    def get_messages(self):
        return self.components

    def stop_event(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    async def send(self, chain):
        self.sent.append(chain)


class Phone(phone.SelfieMixin):
    def __init__(self):
        self.enabled = True
        self.config = {'photo_enabled': True, 'screenshot_enabled': True, 'say_aloud_enabled': True}
        self.api_config = {'image': {'base_url': 'https://image.invalid/v1'},
                           'tts': {'base_url': 'https://voice.invalid/v1'}}
        self._check_reply = AsyncMock(return_value={'leak': False})
        self.browse_enabled = True

    def _browse_on(self):
        return self.enabled and self.browse_enabled

    def _browse_names(self):
        return []

    def _speaker(self, event):
        return ('10005', '小甲')

    def _familiarity(self, person):
        return 0.9

    def _core(self, event):
        return types.SimpleNamespace(snapshot=lambda: {'v': 0.3, 'energy': 0.2})

    def _phone_seen_pages(self, event):
        return {'https://example.invalid/page': '虚构网页'}

    def _note_she_sent(self, event, kind):
        pass


class PhoneTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        modules = {}
        for name, attrs in [('astrbot.core', {}), ('astrbot.core.agent', {}),
                            ('astrbot.core.agent.tool', {'FunctionTool': FunctionTool, 'ToolSet': ToolSet})]:
            mod = types.ModuleType(name)
            mod.__dict__.update(attrs)
            modules[name] = mod
        missing = object()
        previous = {name: sys.modules.get(name, missing) for name in modules}
        sys.modules.update(modules)
        def restore_modules():
            for name, old in previous.items():
                if old is missing:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = old
        self.addCleanup(restore_modules)
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.old_dir, self.old_refs, self.old_spend, self.old_delay = phone.SELFIE_DIR, phone.REF_DIR, phone.SPEND_PATH, phone.SEND_DELAY
        phone.SELFIE_DIR = root / 'selfie'
        phone.REF_DIR = phone.SELFIE_DIR / 'refs'
        phone.SPEND_PATH = root / 'states' / 'spend.json'
        phone.SEND_DELAY = 0
        self.p, self.event = Phone(), Event()

    async def asyncTearDown(self):
        phone.SELFIE_DIR, phone.REF_DIR, phone.SPEND_PATH, phone.SEND_DELAY = self.old_dir, self.old_refs, self.old_spend, self.old_delay
        self.temp.cleanup()

    async def test_switches_off_no_tools_or_descriptions(self):
        self.p.config = {}
        req = ProviderRequest()
        self.p._give_phone_tools(req, self.event)
        self.assertFalse(hasattr(req, 'func_tool'))

    async def test_tool_descriptions_include_context_and_counts(self):
        self.p._phone_account('selfie', sent=True)
        req = ProviderRequest()
        self.p._give_phone_tools(req, Event([Image(), Record()]))
        self.assertEqual(set(req.func_tool.names()), {'take_photo', 'share_screenshot', 'say_aloud'})
        for tool in req.func_tool.tools:
            for value in ('很熟', '现在', '心情好', '困倦', '自拍1张', '随手拍0张', '截图0张', '语音0条', '最近一次', '发了语音', '发了照片'):
                self.assertIn(value, tool.description)

    async def test_each_switch_only_exposes_its_tool(self):
        for setting, name in [('photo_enabled', 'take_photo'), ('screenshot_enabled', 'share_screenshot'),
                              ('say_aloud_enabled', 'say_aloud')]:
            self.p.config = {setting: True}
            req = ProviderRequest()
            self.p._give_phone_tools(req, self.event)
            self.assertEqual(req.func_tool.names(), [name])

    async def test_one_of_each_tool_per_turn(self):
        self.assertEqual(await self.p._tool_take_photo(self.event, 'snap', '窗外的天空'), '排上了')
        self.assertEqual(await self.p._tool_take_photo(self.event, 'selfie', '在家'), '这次已经有了')
        self.assertEqual(await self.p._tool_say_aloud(self.event, '晚安'), '排上了')
        self.assertEqual(await self.p._tool_say_aloud(self.event, '早安'), '这次已经有了')
        self.assertEqual(await self.p._tool_share_screenshot(self.event, 'https://example.invalid/page', '看看'), '排上了')
        self.assertEqual(await self.p._tool_share_screenshot(self.event, 'https://example.invalid/page', '看看'), '这次已经有了')
        self.assertEqual(self.event.sent, [])

    async def test_tool_text_length_limits(self):
        self.assertEqual(await self.p._tool_take_photo(self.event, 'snap', '天' * 61), '不能拍这张')
        self.assertEqual(await self.p._tool_say_aloud(self.event, '话' * 101), '这句话不能说')
        self.assertEqual(self.p._phone_queue(self.event), {})

    async def test_screenshot_only_seen_pages(self):
        self.assertEqual(await self.p._tool_share_screenshot(self.event, 'https://invented.invalid/', '看看'), '只能分享看过的网页')
        await self.p._tool_share_screenshot(self.event, 'https://example.invalid/page', '看看')
        await self.p._media_after_reply(self.event, dict(self.event._ams_phone_queue))
        self.assertEqual(self.event.sent[0].get_plain_text(), '虚构网页\nhttps://example.invalid/page\n看看')
        self.assertEqual(self.p._phone_counts()['screenshot'], 1)

    async def test_screenshot_tool_absent_when_browser_off(self):
        self.p.browse_enabled = False
        req = ProviderRequest()
        self.p._give_phone_tools(req, self.event)
        self.assertNotIn('share_screenshot', req.func_tool.names())
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'screenshot_enabled': True})
        req = ProviderRequest()
        plugin._give_phone_tools(req, self.event)
        self.assertFalse(hasattr(req, 'func_tool'))

    async def test_screenshot_only_search_results_and_successfully_read_pages_this_turn(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'browse_enabled': True, 'screenshot_enabled': True})
        ledger = types.SimpleNamespace(money_left=lambda: True, add=lambda **kw: None)
        plugin._browse_ledger = lambda: ledger
        plugin._browse_names = lambda: []
        search_url = 'https://example.org/search-result'
        read_url = 'https://example.org/read-page'
        search = types.SimpleNamespace(call=AsyncMock(return_value=json.dumps({'results': [
            {'title': '搜索标题', 'url': search_url, 'snippet': '虚构摘要'}]}, ensure_ascii=False)))
        read = types.SimpleNamespace(call=AsyncMock(return_value='URL: ' + read_url + '\nTitle: 阅读标题\nContent: 虚构内容'))
        plugin._builtin_web_tool = lambda kind: search if kind == 'search' else read
        plugin._browse_urls(self.event).add(read_url)
        self.assertEqual(await plugin._tool_share_screenshot(self.event, read_url, '看看'), '只能分享看过的网页')
        await plugin._tool_search(self.event, query='猫咖')
        self.assertEqual(await plugin._tool_share_screenshot(self.event, search_url + 'x', '看看'), '只能分享看过的网页')
        self.assertEqual(await plugin._tool_share_screenshot(self.event, search_url, '看看'), '排上了')
        self.assertEqual(self.event._ams_phone_queue['screenshot'][1], '搜索标题')
        self.event._ams_phone_queue.clear()
        with patch.object(mixin_browse, 'resolve_host', return_value=[]):
            await plugin._tool_read(self.event, url=read_url)
        self.assertEqual(await plugin._tool_share_screenshot(self.event, read_url, '看看'), '排上了')
        self.assertEqual(self.event._ams_phone_queue['screenshot'][1], '阅读标题')
        other = Event()
        self.assertEqual(await plugin._tool_share_screenshot(other, search_url, '看看'), '只能分享看过的网页')

    async def test_failed_read_does_not_allow_screenshot(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'browse_enabled': True, 'screenshot_enabled': True})
        plugin._browse_ledger = lambda: types.SimpleNamespace(money_left=lambda: True, add=lambda **kw: None)
        plugin._builtin_web_tool = lambda kind: types.SimpleNamespace(call=AsyncMock(return_value='Error: fake failure'))
        url = 'https://example.org/failed'
        plugin._browse_urls(self.event).add(url)
        with patch.object(mixin_browse, 'resolve_host', return_value=[]):
            await plugin._tool_read(self.event, url=url)
        self.assertEqual(await plugin._tool_share_screenshot(self.event, url, '看看'), '只能分享看过的网页')

    async def test_phone_check_blocks_private_photo_voice_and_caption_before_services(self):
        self.p._check_reply.side_effect = lambda event, text: {'leak': '私事' in text}
        self.p._make_photo = AsyncMock()
        self.p._make_voice = AsyncMock()
        await self.p._media_after_reply(self.event, {'photo': ('snap', '私事'), 'voice': '私事',
            'screenshot': ('https://example.invalid/page', '虚构网页', '私事')})
        self.p._make_photo.assert_not_awaited()
        self.p._make_voice.assert_not_awaited()
        self.assertEqual(self.event.sent, [])

    async def test_real_send_check_blocks_private_media_text(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'global_memory': True})
        secret = '芒果私下说我的暗号是蓝鲸三号下周三去医院复查'
        plugin._check_note(self.event)['forbidden'] = [
            {'id': 'synthetic', 'text': secret, 'private': True, 'names': [], 'vec': None}]
        plugin._embed_text = AsyncMock(return_value=None)
        plugin._common_pieces = lambda: set()
        plugin._make_photo = AsyncMock()
        plugin._make_voice = AsyncMock()
        await plugin._media_after_reply(self.event, {'photo': ('snap', secret), 'voice': secret})
        plugin._make_photo.assert_not_awaited()
        plugin._make_voice.assert_not_awaited()
        self.assertEqual(self.event.sent, [])

    async def test_check_failure_cancels_media(self):
        self.p._check_reply.side_effect = RuntimeError('fake failure')
        self.p._make_photo = AsyncMock()
        await self.p._media_after_reply(self.event, {'photo': ('snap', '天空')})
        self.p._make_photo.assert_not_awaited()

    async def test_voice_speakable_before_bridge(self):
        await self.p._tool_say_aloud(self.event, '[表情:微笑]你好[表情包:挥手]【下一条】晚安')
        self.assertEqual(self.event._ams_phone_queue['voice'], '你好 晚安')
        self.p._post_json = AsyncMock(return_value=(b'fake audio', 'audio/wav'))
        await self.p._media_after_reply(self.event, dict(self.event._ams_phone_queue))
        self.assertEqual(self.p._post_json.await_args.args[1]['input'], '你好 晚安')
        self.assertIsInstance(self.event.sent[0].chain[0], Record)

    async def test_selfie_edits_one_reference_snap_generations_without_reference(self):
        phone.REF_DIR.mkdir(parents=True)
        (phone.REF_DIR / 'her_base.png').write_bytes(b'fake png')
        raw = json.dumps({'data': [{'b64_json': base64.b64encode(b'png').decode()}]}).encode()
        self.p._post_selfie = AsyncMock(return_value=raw)
        self.p._post_json = AsyncMock(return_value=(raw, 'application/json'))
        self.assertIsNotNone(await self.p._make_photo('selfie', '在家穿毛衣侧身看窗'))
        args = self.p._post_selfie.await_args.args
        self.assertTrue(args[0].endswith('/images/edits'))
        self.assertEqual(args[4], phone.REF_DIR / 'her_base.png')
        self.assertIsNotNone(await self.p._make_photo('snap', '窗边的天空'))
        args = self.p._post_json.await_args.args
        self.assertTrue(args[0].endswith('/images/generations'))
        self.assertNotIn('image', args[1])
        self.assertEqual(args[1]['size'], '1080x1440')

    async def test_photo_prompt_removes_known_names_and_numbers_before_service(self):
        self.p._browse_names = lambda: ['小甲', '小别名', '乙']
        raw = json.dumps({'data': [{'b64_json': 'cG5n'}]}).encode()
        self.p._post_json = AsyncMock(return_value=(raw, 'application/json'))
        await self.p._media_after_reply(self.event, {'photo': ('snap', '小甲和小别名和乙在窗边看天空 900001')})
        prompt = self.p._post_json.await_args.args[1]['prompt']
        for forbidden in ('小甲', '小别名', '乙', '900001'):
            self.assertNotIn(forbidden, prompt)
        self.assertIn('窗边看天空', prompt)
        phone.REF_DIR.mkdir(parents=True)
        (phone.REF_DIR / 'her_base.png').write_bytes(b'fake png')
        self.p._post_selfie = AsyncMock(return_value=raw)
        await self.p._make_photo('selfie', '小甲和小别名和乙在窗边看天空 900001')
        edit_prompt = self.p._post_selfie.await_args.args[1]
        for forbidden in ('小甲', '小别名', '乙', '900001'):
            self.assertNotIn(forbidden, edit_prompt)
        self.assertIn('窗边看天空', edit_prompt)

    async def test_photo_description_empty_after_cleaning_calls_no_service(self):
        self.p._browse_names = lambda: ['小甲']
        self.p._post_json = AsyncMock()
        self.assertIsNone(await self.p._make_photo('snap', '小甲 900001'))
        self.p._post_json.assert_not_awaited()

    async def test_missing_reference_blocks_only_selfie(self):
        raw = json.dumps({'data': [{'b64_json': 'cG5n'}]}).encode()
        self.p._post_json = AsyncMock(return_value=(raw, 'application/json'))
        self.p._post_selfie = AsyncMock()
        self.assertIsNone(await self.p._make_photo('selfie', '在家'))
        self.assertIsNotNone(await self.p._make_photo('snap', '天空'))
        self.p._post_selfie.assert_not_awaited()

    async def test_429_retries_then_cancels(self):
        error = urllib.error.HTTPError('https://image.invalid/', 429, 'busy', {}, None)
        self.p._post_json = AsyncMock(side_effect=error)
        with patch.object(phone.asyncio, 'sleep', new=AsyncMock()) as sleep:
            self.assertIsNone(await self.p._make_photo('snap', '天空'))
        self.assertEqual(self.p._post_json.await_count, 3)
        self.assertEqual([call.args[0] for call in sleep.await_args_list], [1, 2])

    async def test_429_retry_can_succeed(self):
        error = urllib.error.HTTPError('https://image.invalid/', 429, 'busy', {}, None)
        raw = json.dumps({'data': [{'b64_json': 'cG5n'}]}).encode()
        self.p._post_json = AsyncMock(side_effect=[error, (raw, 'application/json')])
        with patch.object(phone.asyncio, 'sleep', new=AsyncMock()):
            self.assertIsNotNone(await self.p._make_photo('snap', '天空'))
        self.assertEqual(self.p._post_json.await_count, 2)

    async def test_photo_queue_full(self):
        self.p._phone_photo_pending = 4
        self.p._post_json = AsyncMock()
        self.assertIsNone(await self.p._make_photo('snap', '天空'))
        self.p._post_json.assert_not_awaited()

    async def test_retention_of_generated_files_only(self):
        phone.REF_DIR.mkdir(parents=True)
        ref = phone.REF_DIR / 'her_base.png'
        ref.write_bytes(b'ref')
        for kind, ext in [('photo', '.png'), ('voice', '.wav')]:
            for _ in range(52):
                self.p._phone_path(kind, ext).write_bytes(b'x')
        other = phone.SELFIE_DIR / 'counters.json'
        other.write_text('{}', encoding='utf-8')
        async def make(kind, *args):
            path = self.p._phone_path(kind, '.png' if kind == 'photo' else '.wav')
            path.write_bytes(b'x')
            return path
        self.p._make_photo = lambda *args: make('photo')
        self.p._make_voice = lambda *args: make('voice')
        await self.p._media_after_reply(self.event, {'photo': ('snap', '天空'), 'voice': '晚安'})
        self.assertEqual(len(list(phone.SELFIE_DIR.glob('ams-phone-photo-*'))), 50)
        self.assertEqual(len(list(phone.SELFIE_DIR.glob('ams-phone-voice-*'))), 50)
        self.assertTrue(ref.exists())
        self.assertTrue(other.exists())

    async def test_text_then_media_and_accounting(self):
        path = self.p._phone_path('voice', '.wav')
        path.write_bytes(b'audio')
        self.p._make_voice = AsyncMock(return_value=path)
        self.event.sent.append('text')
        await self.p._media_after_reply(self.event, {'voice': '晚安'})
        self.assertEqual(self.event.sent[0], 'text')
        self.assertIsInstance(self.event.sent[1].chain[0], Record)
        self.assertEqual(self.p._phone_counts()['voice'], 1)
        self.p._phone_account('voice', 0.5)
        self.assertEqual(json.loads(phone.SPEND_PATH.read_text('utf-8'))[__import__('time').strftime('%Y-%m-%d')]['phone_voice'], 0.5)

    async def test_stopped_event_discards_queue(self):
        self.event.stop_event()
        self.p._make_photo = AsyncMock()
        self.p._make_voice = AsyncMock()
        await self.p._media_after_reply(self.event, {'photo': ('snap', '天空'), 'voice': '晚安'})
        self.p._make_photo.assert_not_awaited()
        self.p._make_voice.assert_not_awaited()

    async def test_silent_reply_discards_queued_media(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'self_decide': True, 'photo_enabled': True})
        plugin._media_after_reply = AsyncMock()
        await plugin._tool_take_photo(self.event, 'snap', '天空')
        await plugin.on_llm_response(self.event, LLMResponse('【不说】'))
        await asyncio.sleep(0)
        plugin._media_after_reply.assert_not_awaited()

    async def test_held_reply_discards_queued_media(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'global_memory': True, 'say_aloud_enabled': True})
        plugin._media_after_reply = AsyncMock()
        async def held(event, response, reply):
            event.stop_event()
            return ''
        plugin._look_at_reply = held
        await plugin._tool_say_aloud(self.event, '晚安')
        await plugin.on_llm_response(self.event, LLMResponse('普通回复'))
        await asyncio.sleep(0)
        plugin._media_after_reply.assert_not_awaited()

    async def test_approved_reply_schedules_media_after_words(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'say_aloud_enabled': True, 'global_memory': True})
        plugin._ipv4_json = harness.fake_ipv4_json
        plugin._look_at_reply = AsyncMock(return_value='普通回复')
        plugin._check_reply = AsyncMock(return_value={'leak': False})
        path = self.p._phone_path('voice', '.wav')
        path.write_bytes(b'audio')
        plugin._make_voice = AsyncMock(return_value=path)
        await plugin._tool_say_aloud(self.event, '晚安')
        await plugin.on_llm_response(self.event, LLMResponse('普通回复'))
        self.assertEqual(self.event.sent, [])
        self.event.sent.append('text')
        for _ in range(5):
            await asyncio.sleep(0)
        self.assertEqual(self.event.sent[0], 'text')
        self.assertIsInstance(self.event.sent[1].chain[0], Record)

    async def test_request_keeps_only_enabled_phone_tool_and_allowed_tools(self):
        plugin = main.BioCorePlugin(harness.FakeContext(), config={'photo_enabled': True, 'allowed_tools': ['kept']})
        req = ProviderRequest(prompt='虚构消息', system_prompt='虚构人设')
        req.func_tool = ToolSet([FunctionTool('builtin'), FunctionTool('kept')])
        plugin._ipv4_json = harness.fake_ipv4_json
        await plugin.on_message(self.event)
        await plugin.on_llm_request(self.event, req)
        self.assertEqual(set(req.func_tool.names()), {'kept', 'take_photo'})

    async def test_photo_generation_is_serial_and_waiting_queue_is_bounded(self):
        entered, release = asyncio.Event(), asyncio.Event()
        active = 0
        peak = 0
        async def post(*args, **kwargs):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            entered.set()
            await release.wait()
            active -= 1
            return json.dumps({'data': [{'b64_json': 'cG5n'}]}).encode(), 'application/json'
        self.p._post_json = post
        tasks = [asyncio.create_task(self.p._make_photo('snap', '天空')) for _ in range(4)]
        await entered.wait()
        await asyncio.sleep(0)
        self.assertIsNone(await self.p._make_photo('snap', '天空'))
        release.set()
        self.assertTrue(all(await asyncio.gather(*tasks)))
        self.assertEqual(peak, 1)


if __name__ == '__main__':
    unittest.main()
