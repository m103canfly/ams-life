# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What she calls him: setting owner_name, default 家人. Every name and number here is made up."""
import asyncio
import base64
import json
import shutil
import struct
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import app_config  # noqa: E402
import harness  # noqa: E402
import impressions  # noqa: E402
import interpretation  # noqa: E402
import life_loop  # noqa: E402
import mixin_impressions  # noqa: E402
import mixin_phone  # noqa: E402
import mixin_selfie  # noqa: E402
import mixin_stickers  # noqa: E402
import mixin_turn  # noqa: E402
import stickers  # noqa: E402
import turn  # noqa: E402

RULE = '别在群里提我的工作'
NAMED = '阿柚'          # a made-up name: the setting's value in these tests
DEFAULT = '家人'        # the neutral default the card gives
OWNER_QQ = '10001'      # a made-up number


def png(tail=b''):
    return (b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\rIHDR' + struct.pack('>II', 8, 8)
            + b'\x08\x06\x00\x00\x00' + tail)


def phone_line(plugin, sender, role='user', text='你好'):
    line = {'ts': 1_793_000_000.0, 'role': role, 'sender_id': sender,
            'sender_name': '小雨', 'text': text}
    return mixin_phone._phone_line(plugin, None, line)


def owner_plugin(**config):
    """The few things life_loop.materials wants from the plugin; three lines still unanswered."""
    rows = [{'role': 'user'}] + [{'role': 'assistant'} for _ in range(3)]
    settings = dict({'owner_qq': OWNER_QQ, 'proactive_owner_enabled': True}, **config)
    return SimpleNamespace(config=settings, self_model={},
                           _read_window=lambda place: {'recent': rows})


def materials_text(plugin):
    core = SimpleNamespace(sleepiness=0, hunger=0, physical_fatigue=0, last_sleep_end=0, last_meal=0)
    with patch.object(life_loop.weather, 'weather_line', return_value=''), \
            patch.object(life_loop.her_days, 'Store') as store:
        store.return_value.day.return_value = []
        return life_loop.materials(plugin, {}, {}, core, 'test', 100, ['休息'], False)


def tool_description(config):
    """The remember_day tool's description, from the mixin without a whole plugin."""
    fake = SimpleNamespace(enabled=True, config=dict({'owner_qq': OWNER_QQ}, **config),
                           _phone_context=lambda event: '',
                           _speaker=lambda event: (OWNER_QQ, '小雨'),
                           _here=lambda event: 'private:' + OWNER_QQ,
                           _tool_set_now=Mock(), _tool_remember_day=Mock())
    tools = {tool.name: tool.description for tool in mixin_selfie.SelfieMixin._phone_tools(fake, None)}
    return tools['remember_day']


READING = {'title': '假标题', 'text': '假正文', 'comments': ['假评论']}


class TheSetting(unittest.TestCase):
    def test_the_default_is_what_the_schema_gives(self):
        schema = app_config.load_schema()
        self.assertEqual(schema['owner_name']['description'], '她怎么称呼你')
        self.assertEqual(schema['owner_name']['default'], DEFAULT)

    def test_read_from_the_setting(self):
        self.assertEqual(interpretation.owner_name({'owner_name': NAMED}), NAMED)
        self.assertEqual(interpretation.owner_name({}), DEFAULT)
        self.assertEqual(interpretation.owner_name(None), DEFAULT)

    def test_blank_or_too_long_is_the_default(self):
        for value in ('', '   ', '\n\t ', '字' * 13, None):
            self.assertEqual(interpretation.owner_name({'owner_name': value}), DEFAULT, repr(value))
        self.assertEqual(interpretation.owner_name({'owner_name': '字' * 12}), '字' * 12)
        self.assertEqual(interpretation.owner_name({'owner_name': ' ' + NAMED + ' '}), NAMED)


class ShownToHer(unittest.TestCase):
    """Every place the card names, with the setting empty and with it set. No 主人 anywhere."""

    def test_default_name_everywhere_and_no_owner_word(self):
        plugin = owner_plugin()
        rules = interpretation.render_compact(None, owner_rules=[RULE])
        materials = materials_text(plugin)
        heybox = life_loop.heybox_ask_prompt(plugin, [READING])
        remember = '这里只能在和%s的私聊里记。' % interpretation.owner_name(plugin.config)
        tool = tool_description(plugin.config)
        texts = [rules, materials, heybox, remember, tool,
                 phone_line(SimpleNamespace(config=plugin.config), OWNER_QQ),
                 phone_line(SimpleNamespace(config=plugin.config), '10003')]
        for text in texts:
            self.assertNotIn('主人', text)
        self.assertIn('[%s定的规矩] ' % DEFAULT, rules)
        self.assertIn('%s还没回的有 3 条' % DEFAULT, materials)
        self.assertIn('想和%s说什么就在 tell 写一句' % DEFAULT, materials)
        self.assertNotIn('tell_owner', materials)
        self.assertIn('对%s说' % DEFAULT, heybox)
        self.assertIn('{"thought":"心得","tell":""}', heybox)
        self.assertIn('和%s的私聊' % DEFAULT, remember)
        self.assertIn('你和%s之间' % DEFAULT, tool)
        self.assertIn('小雨（%s）：' % DEFAULT, texts[5])
        self.assertIn('小雨（别人）：', texts[6])

    def test_the_setting_is_used_everywhere(self):
        plugin = owner_plugin(owner_name=NAMED)
        rules = interpretation.render_compact(None, owner_rules=[RULE], owner_name=NAMED)
        materials = materials_text(plugin)
        heybox = life_loop.heybox_ask_prompt(plugin, [READING])
        self.assertIn('[%s定的规矩] ' % NAMED, rules)
        self.assertIn('%s还没回的有 3 条' % NAMED, materials)
        self.assertIn('想和%s说什么' % NAMED, materials)
        self.assertIn('对%s说' % NAMED, heybox)
        self.assertIn('你和%s之间' % NAMED, tool_description(plugin.config))
        owned = SimpleNamespace(config=plugin.config)
        self.assertIn('小雨（%s）：' % NAMED, phone_line(owned, OWNER_QQ))
        self.assertIn('小雨（别人）：', phone_line(owned, '10003'))
        for text in (rules, materials, heybox):
            self.assertNotIn('主人', text)
            self.assertNotIn(DEFAULT, text)

    def test_the_wishes_line_speaks_of_tell_too(self):
        plugin = owner_plugin()
        plugin.self_model = {'share_wishes': [{'id': 'a' * 8, 'what': '想说的事', 'ts': 99}]}
        text = materials_text(plugin)
        self.assertIn('tell 用到想分享的事时', text)
        self.assertNotIn('tell_owner', text)


class RulesLineWithoutASetting(unittest.TestCase):
    def test_nothing_is_shown_without_rules(self):
        self.assertNotIn(DEFAULT, interpretation.render_compact(None, owner_rules=[]))
        self.assertNotIn('主人', interpretation.render_compact(None, owner_rules=[]))


class TellBothKeys(unittest.TestCase):
    def test_choices_parse_tell_and_tell_owner(self):
        self.assertEqual(life_loop.parse('{"do":"休息","tell":"想跟你说"}', ['休息'])['tell_owner'],
                         '想跟你说')
        self.assertEqual(life_loop.parse('{"do":"休息","tell_owner":"老话"}', ['休息'])['tell_owner'],
                         '老话')
        self.assertEqual(life_loop.parse('{"do":"休息","tell":"新的","tell_owner":"老的"}',
                                         ['休息'])['tell_owner'], '新的')

    def test_heybox_parses_tell_and_tell_owner(self):
        self.assertEqual(life_loop.heybox_impression('{"thought":"好","tell":"一句"}')['tell_owner'],
                         '一句')
        self.assertEqual(life_loop.heybox_impression('{"thought":"好","tell_owner":"旧句"}')['tell_owner'],
                         '旧句')
        self.assertEqual(life_loop.heybox_impression('{"thought":"好","tell_owner":5}'), None)


class PhoneHistory(unittest.TestCase):
    """Old and new framed records are kept as they are; anything else is marked unverified."""

    HISTORY = '（历史消息，发言人和时间未核实）'
    LINE = {'ts': 1_793_000_000.0, 'role': 'user', 'sender_id': OWNER_QQ,
            'sender_name': '小雨', 'text': '你好'}

    def framed(self, label):
        return '[10-30 21:05] 小雨（%s）：（原文）说了一句' % label

    def test_old_and_new_labels_are_kept(self):
        for label in ('主人', '非主人', '别人'):
            self.assertEqual(mixin_phone._history_original(self.framed(label), ''), self.framed(label))
        self.assertEqual(mixin_phone._history_original(self.framed(NAMED), NAMED), self.framed(NAMED))
        self.assertEqual(mixin_phone._history_original(self.framed(DEFAULT), ''), self.framed(DEFAULT))

    def test_anything_else_is_marked_unverified(self):
        text = self.framed('随便谁')
        self.assertEqual(mixin_phone._history_original(text, NAMED), self.HISTORY + '（原文）' + text)
        # a name that is not the setting's is not one of our labels either
        self.assertEqual(mixin_phone._history_original(self.framed(NAMED), ''),
                         self.HISTORY + '（原文）' + self.framed(NAMED))
        self.assertTrue(mixin_phone._history_original('小雨：说了一句').startswith(self.HISTORY))

    def test_the_phone_line_keeps_the_name_the_check_has_no_config_for(self):
        mixin_phone._phone_line(SimpleNamespace(config={'owner_qq': OWNER_QQ, 'owner_name': NAMED}),
                                None, self.LINE)
        self.assertEqual(mixin_phone._history_original(self.framed(NAMED)), self.framed(NAMED))
        mixin_phone._phone_line(SimpleNamespace(config={'owner_qq': OWNER_QQ}), None, self.LINE)
        self.assertTrue(mixin_phone._history_original(self.framed(NAMED)).startswith(self.HISTORY))

    def tearDown(self):
        mixin_phone._phone_line(SimpleNamespace(config={'owner_qq': OWNER_QQ}), None, self.LINE)


class MemoryPeopleStore:
    """What impressions.nightly wants of a store, in memory: no files, no data."""

    def __init__(self):
        self.places, self.names = {}, {}

    def load(self, place):
        return self.places.setdefault(place, {'people': {}, 'tried': ''})

    def save(self, place, data):
        self.places[place] = data

    def keep_names(self, qq, names):
        kept = self.names.setdefault(str(qq), [])
        kept.extend(n for n in names if n and n not in kept)


GROUP = 'group:900001'


def day_lines(qq='10003', name='小雨', count=12):
    start = time.mktime(time.strptime('2026-10-04 20:00:00', '%Y-%m-%d %H:%M:%S'))
    return [{'ts': start + i * 60, 'role': 'user', 'sender_id': qq, 'sender_name': name,
             'text': '今天也说两句 %d' % i} for i in range(count)]


class NightAliases(unittest.IsolatedAsyncioTestCase):
    async def test_the_setting_is_never_kept_as_someones_alias(self):
        store = MemoryPeopleStore()
        answer = json.dumps({'P1': {'style': '说话很轻', 'aliases': [NAMED, '小雨']}}, ensure_ascii=False)

        async def ask(prompt):
            return answer

        # keep whatever the night asked to verify, so the alias check alone decides
        with patch.object(impressions, 'verify_aliases', side_effect=lambda proposed, *a, **k: proposed):
            result = await impressions.nightly(store, GROUP, day_lines(), ask, '2026-10-04',
                                               owner_name=NAMED)
        self.assertEqual(result['written'], 1)
        aliases = store.load(GROUP)['people']['10003']['aliases']
        self.assertNotIn(NAMED, aliases)
        self.assertIn('小雨', aliases)        # the night still keeps the names it may


class NightCall(unittest.IsolatedAsyncioTestCase):
    async def test_the_night_is_given_the_setting(self):
        plugin = SimpleNamespace(
            config={'owner_name': NAMED},
            _impressions_time_reached=lambda now=None: True,
            _provider_for=AsyncMock(return_value=object()),
            _model=Mock(),
            _window_places=lambda: [GROUP],
            _read_window=lambda place: {'recent': day_lines()},
            _impression_store=Mock(),
            _registry=lambda: None,
            _material_names=lambda place, lines: {},
            _red_lines_for=Mock(),
            _judgements_for=Mock())
        night = AsyncMock(return_value={})
        with patch.object(mixin_impressions.impressions, 'nightly', night):
            await mixin_impressions.ImpressionsMixin._maybe_update_impressions(plugin)
        self.assertEqual(night.call_args.kwargs.get('owner_name'), NAMED)


class FakeTurn(mixin_turn.TurnMixin):
    """The plugin's own turn mixin with only the parts around it: no disk, model or platform.

    Every method it would ask the plugin for answers "nothing"; the code under test is the
    real _prepare_turn, the path every reply's prompt takes."""

    inject_intent = True
    memory_dedup_embedding = False
    global_memory = False
    self_decide = False
    reply_in_pieces = False
    kb_enabled = False
    proactive_autonomy = False
    autonomy_loop_enabled = False
    _neutral_model = None

    def __init__(self, config, rules):
        self.config, self.rules = dict(config), list(rules)

    def _speaker(self, event):
        return (str(self.config.get('owner_qq') or ''), '小雨')

    def _for_model(self, text, event):
        return text

    def _without_gone(self, text, event):
        return text

    def _message_text(self, event):
        return '你好'

    def _here(self, event):
        return GROUP

    def _core(self, event):
        return MagicMock()

    def _ambient_level(self):
        return 0.0

    def _window_loops(self, event):
        return []

    def _window_lines(self, event, n=6):
        return []

    def _window_replies(self, event, n=6):
        return []

    def _window_update_loops(self, event, text, core=None):
        return None

    def _user_record(self, event):
        return {}

    def _relationship_of(self, record):
        return None

    def _touch_user(self, event, core=None):
        return {}

    def _continuity_context(self, *args, **kwargs):
        return {}

    def _record_continuity_feedback(self, event, feedback):
        return None

    async def _image_context(self, event):
        return ''

    async def _voice_context(self, event):
        return ''

    async def _memory_recall(self, *args, **kwargs):
        return ''

    def _note_turn(self, *args):
        return None

    async def _maybe_archive_events(self, *args):
        return None

    async def _maybe_archive_strong_event(self, *args):
        return None

    def _self_model_for(self, event):
        return {}

    def _event_context(self, event):
        return ''

    async def _maybe_tom_probe(self, *args, **kwargs):
        return None

    def _notebook_for(self, event):
        return []

    def _labeled_notebook(self, event):
        return []

    def _user_view(self, event, user_data):
        return {}

    def _owner_rules(self):
        return list(self.rules)

    def _people_lines(self, event):
        return []

    def _now_line(self, event):
        return ''

    def _slang_prompt(self, event):
        return ''

    def _stickers_on(self):
        return False

    def _check_note(self, event):
        return {}

    def _note_allowed(self, *args):
        return None

    def _numbers_out_of_request(self, request, event):
        return None

    def _continue_job(self, here):
        return None

    def _check_registry(self, event):
        return None

    async def _ensure_profile(self, event):
        return None

    def _is_private_event(self, event):
        return False


class ReplyPrompt(unittest.IsolatedAsyncioTestCase):
    """The rules line in the prompt a reply is built from, through mixin_turn itself."""

    async def block(self, config):
        plugin = FakeTurn(config, [RULE])
        request = turn.TurnRequest(prompt='你好')
        await plugin._prepare_turn(harness.FakeEvent('你好', sender='10003'), request)
        await asyncio.sleep(0)     # let the turn's background tasks finish
        return ''.join(str(part.get('text') or '') for part in request.extra_user_content_parts)

    async def test_the_rules_line_uses_the_setting(self):
        block = await self.block({'owner_qq': OWNER_QQ, 'owner_name': NAMED})
        self.assertIn('[%s定的规矩] %s' % (NAMED, RULE), block)
        self.assertNotIn(DEFAULT, block)
        self.assertNotIn('主人', block)

    async def test_the_default_is_the_rules_line_without_the_setting(self):
        block = await self.block({'owner_qq': OWNER_QQ})
        self.assertIn('[%s定的规矩] %s' % (DEFAULT, RULE), block)
        self.assertNotIn('主人', block)


class HerOwnWords(unittest.IsolatedAsyncioTestCase):
    async def test_private_anniversary_message_uses_the_setting(self):
        def plugin(name=None):
            config = {'owner_qq': OWNER_QQ}
            if name is not None:
                config['owner_name'] = name
            return SimpleNamespace(config=config, _speaker=lambda event: ('10003', '小雨'),
                                   _here=lambda event: 'group:900001')
        self.assertEqual(await mixin_selfie._remember_day(plugin(), None),
                         '这里只能在和%s的私聊里记。' % DEFAULT)
        self.assertEqual(await mixin_selfie._remember_day(plugin(NAMED), None),
                         '这里只能在和%s的私聊里记。' % NAMED)

    async def test_the_tool_description_uses_the_setting(self):
        self.assertEqual(tool_description({}), '记下你和%s之间重要的日子。' % DEFAULT)
        self.assertEqual(tool_description({'owner_name': NAMED}),
                         '记下你和%s之间重要的日子。' % NAMED)


class HerStickers(unittest.IsolatedAsyncioTestCase):
    def test_old_captions_are_left_alone_and_new_ones_use_the_name(self):
        made = tempfile.mkdtemp(prefix='ams-life-owner-')
        self.addCleanup(shutil.rmtree, made, True)
        library = stickers.Library(Path(made) / 'stickers')
        old, _why = library.add(png(b'old'), 1_793_000_000.0, source='owner', note='主人给的')
        self.assertEqual(library.rows[old]['caption'], '主人给的')      # old data: not migrated
        fresh, _why = library.add(png(b'new'), 1_793_000_000.0, source='owner', owner_name=NAMED)
        self.assertEqual(library.rows[fresh]['caption'], NAMED + '给的')
        self.assertEqual(stickers.source_label(library.rows[fresh], {}), '主人给的')   # the page's label

    def test_a_line_from_him_stays_his(self):
        made = tempfile.mkdtemp(prefix='ams-life-owner-')
        self.addCleanup(shutil.rmtree, made, True)
        library = stickers.Library(Path(made) / 'stickers')
        sid, _why = library.add(png(b'line'), 1_793_000_000.0, source='owner', note='你的小猫',
                                owner_name=NAMED)
        self.assertEqual(library.rows[sid]['caption'], '你的小猫')

    async def test_the_page_adds_what_he_gives_under_the_setting(self):
        library = Mock()
        library.add.return_value = ('made-up-id', '')
        page = SimpleNamespace(config={'owner_qq': OWNER_QQ, 'owner_name': NAMED},
                               _sticker_lib=lambda: library, _sticker_lock=asyncio.Lock,
                               _attention_cfg=lambda: {'owner': OWNER_QQ},
                               _llm_allowed=lambda kind: False,
                               _page_body=mixin_stickers.StickersMixin._page_body)
        picture = base64.b64encode(png(b'page')).decode()
        with patch.object(mixin_stickers, '_start_vector_worker'):
            result = await mixin_stickers.StickersMixin.page_sticker_add(page, {'picture': picture})
        self.assertEqual(result['status'], 'ok')
        kwargs = library.add.call_args.kwargs
        self.assertEqual(kwargs['note'], NAMED + '给的')
        self.assertEqual(kwargs['owner_name'], NAMED)
        self.assertEqual(kwargs['source'], 'owner')


class Stopwords(unittest.TestCase):
    def test_the_setting_name_and_the_old_word_are_both_generic(self):
        self.assertIn('主人', impressions.GENERIC_ALIASES)
        self.assertEqual(impressions.check_alias(DEFAULT), '')                 # the default name too
        self.assertEqual(impressions.check_alias(NAMED, owner_name=NAMED), '')
        self.assertEqual(impressions.check_alias(NAMED), NAMED)                # only when it is his name


if __name__ == '__main__':
    unittest.main()
