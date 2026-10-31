# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Hearing a voice: AstrBot's speech-to-text when it has a provider, else QQ's own words.

Every number, word and file name here is made up (10001, 900001, 明天几点出门); nothing
connects to AstrBot, NapCat or a real account. ``OldMedia`` keeps the old ``_voice_context``
from ``d20f2fa`` beside the new one, so the AstrBot path stays the same. The last class goes
through the fake NapCat; it needs aiohttp and is skipped without it, as ``test_fakes`` does.
"""
import asyncio
import logging
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot_turn
import harness
import main
import messenger
from adapter_onebot_messenger import ActionFailed, OneBotMessenger
from astrbot.api.message_components import Record
from fake_napcat import FakeNapCat, PTT_TEXT

try:
    import aiohttp
except ImportError:
    aiohttp = None

if aiohttp is not None:
    from onebot_server import OneBotServer  # noqa: E402

logger = logging.getLogger(__name__)

HIM = '10001'           # someone, made up
GROUP = '900001'        # a group, made up
VOICE = 'voice.amr'     # a file name, made up; nothing is read
WORDS = '听见了'         # what the fake AstrBot provider says
TOKEN = 'fake-secret'   # the token of the fake NapCat, made up


class OldMedia:
    """The old ``_voice_context``, copied as it was from mixin_media.py 266-290 at d20f2fa."""

    def __init__(self, plugin):
        self.context = plugin.context
        self.voice_transcription_enabled = getattr(plugin, "voice_transcription_enabled", True)

    async def _voice_context(self, event) -> str:
        if not getattr(self, "voice_transcription_enabled", True):
            return ""
        try:
            provider = await self.context.get_using_stt_provider_async(
                getattr(event, "unified_msg_origin", "") or "")
            if provider is None:
                return ""
            texts = []
            for m in adapter_astrbot_turn.incoming_of(event).segments:
                if m.type != "record":
                    continue
                ref = str(m.data.get("url") or m.data.get("file") or m.data.get("path") or "").strip()
                if not ref:
                    continue
                try:
                    txt = await provider.get_text(ref)
                    if str(txt or "").strip():
                        texts.append(str(txt).strip()[:300])
                except Exception as exc:
                    logger.warning("[biocore] voice transcribe failed: %s", exc)
            return "；".join(texts)[:600]
        except Exception as exc:
            logger.warning("[biocore] voice context failed: %s", exc)
            return ""


class FakeMessenger:
    """A messenger that keeps every call, and answers it as the test set or raises it."""

    def __init__(self, answer=None, error=None):
        self.answer = answer
        self.error = error
        self.calls = []

    async def send(self, place, segments):
        raise AssertionError('a voice is heard, never sent')

    async def call(self, action, **params):
        self.calls.append((action, params))
        if self.error is not None:
            raise self.error
        return self.answer


class Words:
    """A speech-to-text provider that says the same made-up words for every voice."""

    def __init__(self, words=WORDS):
        self.words = words
        self.refs = []

    async def get_text(self, ref):
        self.refs.append(ref)
        return self.words


class BrokenStt:
    """A context with the method, but it cannot give a provider."""

    async def get_using_stt_provider_async(self, umo=None):
        raise RuntimeError('no speech-to-text here')


def with_provider(provider):
    """The harness context, giving this speech-to-text provider."""
    context = harness.FakeContext()

    async def get_provider(umo=None):
        return provider

    context.get_using_stt_provider_async = get_provider
    return context


def a_plugin(context, fake):
    """A plugin with just what _voice_context reads: its context, the switch and a messenger."""
    plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
    plugin.context = context
    plugin.voice_transcription_enabled = True
    plugin._messenger = lambda event=None, **kwargs: fake
    return plugin


def a_voice(message_id='m900001'):
    """An AstrBot-shaped event whose message is one made-up voice."""
    event = harness.FakeEvent('', sender=HIM, name='柠檬', group=GROUP, self_id='20002')
    event.message_obj.message_id = message_id
    event.get_messages = lambda: [Record(file=VOICE)]
    return event


def a_text():
    """An AstrBot-shaped event with no voice in it."""
    return harness.FakeEvent('明天见', sender=HIM, name='柠檬', group=GROUP, self_id='20002')


class WithAstrBot(unittest.TestCase):
    """1. A provider from AstrBot: the old body's words, and QQ is not asked."""

    def test_same_words_as_the_old_body(self):
        for words in (WORDS, ' 听见了 ', ''):
            with self.subTest(words=words):
                plugin = a_plugin(with_provider(Words(words)), FakeMessenger({'text': PTT_TEXT}))
                event = a_voice()
                self.assertEqual(asyncio.run(plugin._voice_context(event)),
                                 asyncio.run(OldMedia(plugin)._voice_context(event)))
                self.assertEqual(plugin._messenger(None).calls, [])


class WithoutAstrBot(unittest.TestCase):
    """2. No provider from AstrBot: QQ's own speech-to-text is asked once for this voice."""

    def test_none_from_astrbot_asks_qq_once(self):
        fake = FakeMessenger({'text': PTT_TEXT})   # the harness context gives no provider
        plugin = a_plugin(harness.FakeContext(), fake)
        event = a_voice()
        self.assertEqual(adapter_astrbot_turn.incoming_of(event).message_id, 'm900001')
        self.assertEqual(asyncio.run(plugin._voice_context(event)), PTT_TEXT)
        self.assertEqual(fake.calls, [('fetch_ptt_text', {'message_id': 'm900001'})])

    def test_a_context_without_the_method_or_that_fails(self):
        for context in (types.SimpleNamespace(), BrokenStt(), None):
            with self.subTest(context=context):
                fake = FakeMessenger(PTT_TEXT)
                plugin = a_plugin(context, fake)
                self.assertEqual(asyncio.run(plugin._voice_context(a_voice())), PTT_TEXT)
                self.assertEqual(fake.calls, [('fetch_ptt_text', {'message_id': 'm900001'})])


class TheWords(unittest.TestCase):
    """3. QQ's answer as a string, or as a dict with the words in one of its fields."""

    def test_a_string_or_a_dict(self):
        for answer in (PTT_TEXT, {'text': PTT_TEXT}, {'content': PTT_TEXT},
                       {'result': PTT_TEXT}, {'text': ' ', 'content': PTT_TEXT}):
            with self.subTest(answer=answer):
                fake = FakeMessenger(answer)
                plugin = a_plugin(harness.FakeContext(), fake)
                self.assertEqual(asyncio.run(plugin._voice_context(a_voice())), PTT_TEXT)


class NothingHeard(unittest.TestCase):
    """4. No words in the answer, or the call fails: "", and nothing is raised."""

    def test_an_answer_without_words(self):
        for answer in ('', '   ', {}, {'text': ''}, {'text': None}, {'other': 1}, None, []):
            with self.subTest(answer=answer):
                fake = FakeMessenger(answer)
                plugin = a_plugin(harness.FakeContext(), fake)
                self.assertEqual(asyncio.run(plugin._voice_context(a_voice())), '')
                self.assertEqual(len(fake.calls), 1)

    def test_a_failed_call_is_not_raised(self):
        for error in (ActionFailed('fetch_ptt_text', 1200), RuntimeError('offline')):
            with self.subTest(error=type(error).__name__):
                fake = FakeMessenger(error=error)
                plugin = a_plugin(harness.FakeContext(), fake)
                self.assertEqual(asyncio.run(plugin._voice_context(a_voice())), '')
                self.assertEqual(len(fake.calls), 1)


class NoVoiceToHear(unittest.TestCase):
    """5. No voice in the message, the switch off, or no message id: QQ is not asked."""

    def test_a_message_without_a_voice(self):
        fake = FakeMessenger({'text': PTT_TEXT})
        plugin = a_plugin(harness.FakeContext(), fake)
        self.assertEqual(asyncio.run(plugin._voice_context(a_text())), '')
        self.assertEqual(fake.calls, [])

    def test_the_switch_off(self):
        fake = FakeMessenger({'text': PTT_TEXT})
        plugin = a_plugin(with_provider(Words()), fake)
        plugin.voice_transcription_enabled = False
        self.assertEqual(asyncio.run(plugin._voice_context(a_voice())), '')
        self.assertEqual(fake.calls, [])

    def test_a_voice_without_a_message_id(self):
        fake = FakeMessenger({'text': PTT_TEXT})
        plugin = a_plugin(harness.FakeContext(), fake)
        self.assertEqual(asyncio.run(plugin._voice_context(a_voice(''))), '')
        self.assertEqual(fake.calls, [])


class ThroughTheFakeNapCat(unittest.TestCase):
    """6. The action is allowed, and the fake NapCat answers with QQ's made-up words."""

    def test_the_action_is_allowed(self):
        self.assertIn('fetch_ptt_text', messenger.ALLOWED_ACTIONS)

    def test_the_fake_answers_with_words(self):
        fake = FakeNapCat(url='ws://127.0.0.1:6199/ws', token=TOKEN)

        async def call_api(action, params):
            fake.calls.append((action, dict(params)))
            return fake._answer(action, dict(params))   # the frame it sends over a socket

        self.assertEqual(asyncio.run(OneBotMessenger(call_api, roots=()).call(
            'fetch_ptt_text', message_id='900001-1')), {'text': PTT_TEXT})
        self.assertEqual(fake.calls, [('fetch_ptt_text', {'message_id': '900001-1'})])


@unittest.skipUnless(aiohttp is not None, 'aiohttp is not installed')
class OverTheServer(unittest.IsolatedAsyncioTestCase):
    """6. The same action over 2d's server and the fake NapCat's own socket."""

    async def asyncSetUp(self):
        self.events = []

        async def on_event(frame):
            self.events.append(frame)

        self.server = OneBotServer(token=TOKEN, on_event=on_event, port=0, call_seconds=1)
        self.port = await self.server.start()
        self.addAsyncCleanup(self.server.stop)
        self.napcat = FakeNapCat(url='ws://127.0.0.1:%d/ws' % self.port, token=TOKEN)
        await self.napcat.__aenter__()
        self.addAsyncCleanup(self.napcat.__aexit__, None, None, None)
        for _ in range(2000):
            if self.server.connected:
                return
            await asyncio.sleep(0.001)
        self.fail('the fake NapCat did not finish the handshake')

    async def test_fetch_ptt_text_over_the_server(self):
        words = await asyncio.wait_for(
            self.server.messenger(()).call('fetch_ptt_text', message_id='900001-1'), 2)
        self.assertEqual(words, {'text': PTT_TEXT})
        self.assertEqual(self.napcat.calls[-1],
                         ('fetch_ptt_text', {'message_id': '900001-1'}))


if __name__ == '__main__':
    unittest.main()
