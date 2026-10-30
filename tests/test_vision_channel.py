"""Offline tests for vision routing, spending, counting and caption cache."""
import asyncio
import base64
import json
import sys
import tempfile
import types
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import call, mock_open, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))
import vision

PNG = b'\x89PNG\r\n\x1a\n' + b'fictional picture'

def fake_bytes(ref):
    return PNG + str(ref).encode('utf-8')

import mixin_attention
import mixin_discretion
import mixin_llm


class Plugin(mixin_llm.LLMMixin, mixin_attention.AttentionMixin):
    def __init__(self):
        self.config = {'vision_price_per_call': '0'}
        self.llm_functions = {'image_caption': {'provider': 'image_api'}}
        self.api_config = {'image': {'base_url': 'https://vision.invalid/v1', 'api_key': 'made-up-test-key'}}
        self.cache = {}
        self.self_decide = True

    def _load_image_cache(self):
        return dict(self.cache)

    def _save_image_cache(self, cache):
        self.cache = dict(cache)

    def _speaker(self, event):
        return ('10005', 'Example')

    def _here(self, event):
        return 'group:900001'

    def _why_called(self, event):
        return 'at'

    def _job_stale(self):
        return False


class FakeProvider:
    def __init__(self):
        self.calls = 0

    async def text_chat(self, **kwargs):
        self.calls += 1
        return types.SimpleNamespace(completion_text='a small drawing', usage=types.SimpleNamespace(
            input_other=1000000, input_cached=0, output=1000000))


class VisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name)
        self.patches = [patch.object(vision, 'DATA_DIR', self.data),
                        patch.object(mixin_attention, 'SPEND_PATH', self.data / 'spend.json')]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def test_selected_image_api_and_empty_model(self):
        plugin = Plugin()
        plugin.config['vision_image_api_model'] = 'made-up-model'
        provider = plugin._vision_provider_for()
        self.assertIsInstance(provider.provider._provider, vision.ImageAPI)
        self.assertTrue(plugin._sees_images(provider))
        plugin.config['vision_image_api_model'] = ''
        self.assertIsNone(plugin._vision_provider_for())

    def test_key_sent_but_never_in_logs_or_exception(self):
        plugin = Plugin()
        plugin.config['vision_image_api_model'] = 'made-up-model'
        seen = []
        def fail(req, timeout):
            seen.append(req.get_header('Authorization'))
            raise urllib.error.HTTPError(req.full_url, 401, plugin.api_config['image']['api_key'], {}, None)
        vision.logger.records.clear()
        with patch('urllib.request.urlopen', fail):
            with self.assertRaises(RuntimeError) as error:
                asyncio.run(vision.ImageAPI(plugin).text_chat(prompt='describe', image_urls=['data:image/png;base64,' + base64.b64encode(PNG).decode('ascii')]))
        self.assertEqual(seen, ['Bearer made-up-test-key'])
        self.assertNotIn('made-up-test-key', str(error.exception))
        self.assertNotIn('made-up-test-key', str(vision.logger.records))

    def test_local_text_file_is_not_read_past_header_or_sent(self):
        path = self.data / 'not-image.txt'
        path.write_text('not a picture and private text', encoding='utf-8')
        plugin = Plugin()
        provider = FakeProvider()
        gate = vision.VisionGate(plugin, provider, object())
        opened = mock_open(read_data=b'not a picture and private text')
        with patch.object(Path, 'open', opened):
            with self.assertRaisesRegex(RuntimeError, 'image unavailable'):
                asyncio.run(gate.text_chat(prompt='describe', image_urls=[str(path)]))
        self.assertEqual(opened().read.call_args_list, [call(16)])
        self.assertEqual(provider.calls, 0)

    def test_local_image_is_checked_by_header_not_extension(self):
        path = self.data / 'picture.dat'
        path.write_bytes(PNG)
        self.assertEqual(vision._bytes(str(path)), PNG)

    def test_local_picture_headers_accept_the_four_supported_formats(self):
        headers = (b'\xff\xd8\xffrest', b'\x89PNG\r\n\x1a\nrest', b'GIF89arest', b'RIFF1234WEBPrest')
        for index, data in enumerate(headers):
            path = self.data / ('picture-' + str(index))
            path.write_bytes(data)
            self.assertEqual(vision._bytes(str(path)), data)

    def test_openai_request_receives_data_url_not_qq_address(self):
        plugin = Plugin()
        plugin.config['vision_image_api_model'] = 'made-up-model'
        sent = []
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return b'{"choices":[{"message":{"content":"picture"}}]}'
        def fake_open(req, timeout):
            sent.append(json.loads(req.data.decode('utf-8')))
            return Response()
        gate = vision.VisionGate(plugin, vision.ImageAPI(plugin), object())
        with patch.object(vision.stickers, 'fetch_picture', return_value=PNG), \
                patch('urllib.request.urlopen', side_effect=fake_open):
            asyncio.run(gate.text_chat(prompt='describe', image_urls=['https://gchat.qpic.cn/made-up.png']))
        image_url = sent[0]['messages'][0]['content'][1]['image_url']['url']
        self.assertEqual(image_url, 'data:image/png;base64,' + base64.b64encode(PNG).decode('ascii'))
        self.assertNotIn('gchat.qpic.cn', json.dumps(sent))

    def test_qq_image_is_sent_as_data_and_non_qq_is_not_fetched(self):
        plugin = Plugin()
        provider = FakeProvider()
        received = []
        gate = vision.VisionGate(plugin, provider, object())
        fake = FakeProvider()
        async def capture_image(**kwargs):
            received.extend(kwargs['image_urls'])
            return await fake.text_chat(**kwargs)
        provider.text_chat = capture_image
        with patch.object(vision.stickers, 'fetch_picture', return_value=PNG) as fetch:
            asyncio.run(gate.text_chat(prompt='describe', image_urls=['https://gchat.qpic.cn/made-up.png']))
            self.assertEqual(fetch.call_count, 1)
            with self.assertRaisesRegex(RuntimeError, 'image unavailable'):
                asyncio.run(gate.text_chat(prompt='describe', image_urls=['https://image.invalid/not-qq.png']))
            self.assertEqual(fetch.call_count, 1)
        self.assertEqual(received, ['data:image/png;base64,' + base64.b64encode(PNG).decode('ascii')])
        self.assertEqual(fake.calls, 1)

    def test_zero_price_counts_calls_without_increasing_spending(self):
        plugin = Plugin()
        provider = FakeProvider()
        gate = vision.VisionGate(plugin, plugin._spending('vision', provider), object())
        async def run():
            for n in range(2):
                await gate.text_chat(prompt='describe', image_urls=[f'https://image.invalid/{n}'])
        with patch.object(vision, '_bytes', side_effect=fake_bytes):
            asyncio.run(run())
        self.assertEqual(provider.calls, 2)
        self.assertEqual(plugin._spent_today(), 0)
        day = next(iter(json.loads((self.data / 'spend.json').read_text('utf-8')).values()))
        self.assertEqual(day['calls'], 2)
        self.assertEqual(day['vision_calls'], 2)

    def test_thirty_first_and_hundredth_picture_call_model(self):
        plugin = Plugin()
        plugin._why_called = lambda event: ''
        provider = FakeProvider()
        gate = vision.VisionGate(plugin, plugin._spending('vision', provider), object())
        async def run():
            for n in range(100):
                await gate.text_chat(prompt='describe', image_urls=[f'https://image.invalid/{n}'])
                if n in (30, 99):
                    self.assertEqual(provider.calls, n + 1)
        with patch.object(vision, '_bytes', side_effect=fake_bytes):
            asyncio.run(run())
        self.assertEqual(vision.vision_for_panel(plugin.config)['calls'], 100)
        self.assertEqual(plugin._spent_today(), 0)

    def test_existing_daily_count_is_carried_into_ledger(self):
        plugin = Plugin()
        day = vision.time.strftime('%Y-%m-%d')
        (self.data / 'vision_counts.json').write_text(json.dumps({'day': day, 'calls': 30}), 'utf-8')
        provider = FakeProvider()
        gate = vision.VisionGate(plugin, provider, object())
        with patch.object(vision, '_bytes', side_effect=fake_bytes):
            asyncio.run(gate.text_chat(prompt='describe', image_urls=['https://image.invalid/new']))
        ledger = json.loads((self.data / 'spend.json').read_text('utf-8'))
        self.assertEqual(ledger[day]['vision_calls'], 31)
        shown = vision.vision_for_panel(plugin.config)
        self.assertEqual((shown['reply'], shown['unattributed']), (1, 30))
        self.assertEqual(provider.calls, 1)

    def test_browse_source_is_available_to_future_callers(self):
        plugin = Plugin()
        plugin.config['vision_image_api_model'] = 'made-up-model'
        fake = FakeProvider()
        async def answer(_provider, **kwargs):
            return await fake.text_chat(**kwargs)
        with patch.object(vision, '_bytes', side_effect=fake_bytes), \
                patch.object(vision.ImageAPI, 'text_chat', answer):
            gate = plugin._vision_provider_for(object(), source='browse')
            asyncio.run(gate.text_chat(prompt='describe', image_urls=['https://image.invalid/new']))
        shown = vision.vision_for_panel(plugin.config)
        self.assertEqual((shown['calls'], shown['reply'], shown['browse'], shown['owner_add']), (1, 0, 1, 0))
        self.assertEqual(plugin._spent_today(), 0)

    def test_accounting_failure_does_not_block_vision(self):
        plugin = Plugin()
        provider = FakeProvider()
        gate = vision.VisionGate(plugin, provider, object())
        with patch.object(vision, '_bytes', side_effect=fake_bytes), \
                patch.object(mixin_attention, '_write_json', side_effect=OSError('unavailable')):
            asyncio.run(gate.text_chat(prompt='describe', image_urls=['https://image.invalid/new']))
        self.assertEqual(provider.calls, 1)

    def test_private_caption_is_not_shared_with_group(self):
        plugin = Plugin()
        provider = FakeProvider()
        gate = vision.VisionGate(plugin, provider, object())
        async def run():
            plugin._here = lambda event: 'private:10005'
            await gate.text_chat(prompt='describe', image_urls=['https://image.invalid/one'])
            plugin._here = lambda event: 'group:900001'
            await gate.text_chat(prompt='describe', image_urls=['https://image.invalid/two'])
        with patch.object(vision, '_bytes', return_value=PNG):
            asyncio.run(run())
        self.assertEqual(provider.calls, 2)

    def test_same_content_cached_and_forgotten_with_sender(self):
        plugin = Plugin()
        provider = FakeProvider()
        gate = vision.VisionGate(plugin, provider, object())
        async def run():
            first = await gate.text_chat(prompt='describe', image_urls=['https://image.invalid/one'])
            plugin._speaker = lambda event: ('10006', 'Another')
            second = await gate.text_chat(prompt='describe', image_urls=['https://image.invalid/two'])
            self.assertEqual(first.completion_text, second.completion_text)
        with patch.object(vision, '_bytes', return_value=PNG):
            asyncio.run(run())
        self.assertEqual(provider.calls, 1)
        cache_path = self.data / 'image_cache.json'
        cache_path.write_text(json.dumps(plugin.cache), encoding='utf-8')
        class Forgetter(mixin_discretion.DiscretionMixin):
            def _load_image_cache(self):
                return json.loads(cache_path.read_text(encoding='utf-8'))
        with patch.object(mixin_discretion, 'IMAGE_CACHE_PATH', cache_path):
            self.assertEqual(Forgetter()._forget_pictures_of('10006'), 1)
        self.assertEqual(json.loads(cache_path.read_text(encoding='utf-8')), {})


if __name__ == '__main__':
    unittest.main()
