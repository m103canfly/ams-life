# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Card E2: a thing that matters comes in, she weighs it herself; a later answer; a make-up on waking.

Three marks she writes at the end of a reply and never sends, the due table they fill, a
thing put down for another calling her while she is busy, going on with what she had, the
tell when he spoke first, and what she sees when she wakes up."""
import asyncio
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import attention  # noqa: E402
import body  # noqa: E402
import harness  # noqa: E402
import her_days  # noqa: E402
import life_loop as life  # noqa: E402
import mixin_turn  # noqa: E402
import mixin_selfie as phone  # noqa: E402

OWNER = '10001'          # a made-up number: his private chat
OTHER = '10003'          # a made-up number: someone she knows
NAMED = '虚构主人'        # a made-up name of his
OTHER_NAME = '虚构小乙'   # a made-up name of someone else
PUT_DOWN_WHY = '他说电脑坏了要我帮忙看'


class Words:
    """A reply handle: her words, as the plugin takes the marks out of them."""

    def __init__(self, text):
        self.text = text

    def map_words(self, fn):
        self.text = fn(self.text)
        return self.text

    def set_text(self, text):
        self.text = str(text or '')


class ReplyPlugin:
    """The little of the plugin _after_reply needs for a reply that carries marks."""

    def __init__(self, here='private:' + OWNER, life_loop_enabled=True):
        self.enabled = True
        self.config = {'owner_qq': OWNER, 'life_loop_enabled': life_loop_enabled}
        self.self_decide = True
        self.note = {}
        self.sent = []
        self.window = []
        self.queue = {}
        self.core = body.BioCore()
        self.here = here
        self.red = ()
        self.names = {OWNER: {NAMED}, OTHER: {OTHER_NAME}}

    # the ports _after_reply asks for
    def _ignored_sender(self, event): return False
    def _browse_on(self): return False
    def _note_spend(self, kind, reply): pass
    def _continue_job(self, here): pass
    def _check_registry(self, event): pass
    def _core(self, event): return self.core
    def _here(self, event): return self.here
    def _sticker_named(self, event, reply, text): return text, ''
    def _stickers_on(self): return False
    def _check_note(self, event): return self.note
    def _phone_queue(self, event): return self.queue
    def _owner_rules(self): return []
    def _stop(self, event): event.stopped = True
    def _names_index(self): return self.names
    def _known_names(self, people):
        return [name for person in people
                for name in [str(person), *self.names.get(str(person), ())]]
    def _red_line(self, text, where): return 'health' if any(bad in text for bad in self.red) else ''
    def _shape_reply(self, event, reply, text, then=None, sticker_part=None):
        self.sent.append(text)
        return text
    def _window_add_reply(self, event, text): self.window.append(text)
    def _slang_note_reply(self, event, text): pass

    async def _look_at_reply(self, event, reply, text): return text
    async def _remember(self, event, text, role, core): pass
    async def _maybe_relationship_impression(self, event, core): pass
    async def _maybe_relationship_narrative(self, event, core): pass


class ReplyMarksTests(unittest.IsolatedAsyncioTestCase):
    """The marks are taken out of her reply before anything is sent or kept."""

    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 2, 10).timestamp())
        for target, name, value in ((life, 'STATE_DIR', self.root / 'states'),
                                    (life, 'DATA_DIR', self.root),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json'),
                                    (phone, 'LOOK_PATH', self.root / 'states' / 'look.json'),
                                    (phone, 'STATE_DIR', self.root / 'states'),
                                    (mixin_turn, 'STATE_DIR', self.root / 'states'),
                                    (mixin_turn, 'HER_STATE_PATH', self.root / 'states' / 'her.json'),
                                    (mixin_turn, 'time', SimpleNamespace(time=self.clock))):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = ReplyPlugin()
        self.event = SimpleNamespace(stopped=False)

    def state(self):
        return json.loads((self.root / 'states' / 'life.json').read_text(encoding='utf-8'))

    async def reply(self, text, plugin=None):
        words = Words(text)
        await mixin_turn.TurnMixin._after_reply(plugin or self.p, self.event, words)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        return words

    # 1. her words go out, the mark does not
    async def test_1_only_her_words_are_sent_and_kept(self):
        words = await self.reply('好的【%s：%s】' % (attention.PUT_DOWN, PUT_DOWN_WHY))
        self.assertEqual(self.p.note.get('sent'), '好的')
        self.assertEqual(self.p.sent, ['好的'])
        self.assertEqual(self.p.window, ['好的'])
        self.assertEqual(words.text, '好的')
        kept = self.state()['put_down']
        self.assertEqual(kept['why'], PUT_DOWN_WHY)
        self.assertEqual(kept['here'], 'private:' + OWNER)
        self.assertEqual(kept['ts'], self.clock())
        self.assertTrue(kept['id'])

    # 2. 【不说】 wins over the mark, and the mark is kept all the same
    async def test_2_silence_plus_a_mark_sends_nothing_and_keeps_it(self):
        await self.reply('%s【%s：%s】' % (attention.SILENT, attention.PUT_DOWN, PUT_DOWN_WHY))
        self.assertEqual(self.p.note.get('outcome'), 'silent')
        self.assertEqual(self.p.note.get('sent'), '')
        self.assertEqual(self.p.sent, [])
        self.assertEqual(self.p.window, [])
        self.assertTrue(self.event.stopped)
        self.assertEqual(self.state()['put_down']['why'], PUT_DOWN_WHY)

    # 3. the two marks about him count in his private chat only
    async def test_3a_in_a_group_the_two_marks_about_him_are_cut_out_and_not_kept(self):
        self.p.here = 'group:900001'
        await self.reply('好的【%s：30，他在修电脑】' % attention.OWNER_LATER)
        await self.reply('好的【%s：30】' % attention.OWNER_REPLY_LATER)
        self.assertEqual(self.p.note.get('sent'), '好的')
        self.assertFalse((self.root / 'states' / 'life.json').exists())

    async def test_3b_in_his_private_chat_both_marks_fill_the_due_table(self):
        await self.reply('好的【%s：30，他在修电脑】' % attention.OWNER_LATER)
        await self.reply('好的【%s：30】' % attention.OWNER_REPLY_LATER)
        self.assertEqual(self.p.sent, ['好的', '好的'])
        later, back = self.state()['due']
        self.assertEqual((later['kind'], later['why'], later['ts']),
                         ('owner_later', '他在修电脑', self.clock() + 30 * 60))
        self.assertEqual((back['kind'], back['ts']), ('owner_reply_later', self.clock() + 30 * 60))
        self.assertEqual(later['set_at'], self.clock())

    # 4. a name in the why is taken out; a red line drops the mark
    async def test_4_names_are_taken_out_and_a_red_line_drops_the_mark(self):
        await self.reply('好的【%s：%s说电脑坏了】' % (attention.PUT_DOWN, OTHER_NAME))
        self.assertEqual(self.state()['put_down']['why'], '有人说电脑坏了')
        await self.reply('好的【%s：他说在医院等我】' % attention.PUT_DOWN)   # a red line of redline.hit
        self.assertEqual(self.state()['put_down']['why'], '有人说电脑坏了')
        self.p.red = ('修电脑',)
        await self.reply('好的【%s：他要我修电脑】' % attention.PUT_DOWN)     # held by the plugin's own line
        self.assertEqual(self.state()['put_down']['why'], '有人说电脑坏了')

    # 10 (first half). an answer later sends nothing and comes due in twenty minutes
    async def test_10a_an_answer_later_sends_nothing_and_comes_due(self):
        await self.reply('【%s：20】' % attention.OWNER_REPLY_LATER)
        self.assertEqual(self.p.note.get('outcome'), 'silent')
        self.assertEqual(self.p.sent, [])
        self.assertTrue(self.event.stopped)
        self.assertEqual([(row['kind'], row['ts']) for row in self.state()['due']],
                         [('owner_reply_later', self.clock() + 20 * 60)])

    # 14. with her loop off nothing is kept, and the marks still do not go out
    async def test_14_with_the_loop_off_the_marks_are_cut_out_and_not_kept(self):
        plugin = ReplyPlugin(life_loop_enabled=False)
        await self.reply('好的【%s：%s】' % (attention.PUT_DOWN, PUT_DOWN_WHY), plugin=plugin)
        self.assertEqual(plugin.note.get('sent'), '好的')
        self.assertEqual(plugin.sent, ['好的'])
        self.assertFalse((self.root / 'states' / 'life.json').exists())

    # 15. a mark written badly is cut out too, and nothing of it is kept
    async def test_15_a_broken_mark_is_cut_out_and_nothing_is_taken(self):
        words = await self.reply('【%s：没有右括号' % attention.PUT_DOWN)
        self.assertEqual(words.text, '')
        self.assertEqual(self.p.sent, [])
        self.assertEqual(self.p.window, [])
        self.assertFalse((self.root / 'states' / 'life.json').exists())


class Person(phone.SelfieMixin):
    """The few things life_loop wants from the plugin; a queue of answers, no network."""

    def __init__(self):
        self.enabled = True
        self.config = {'life_loop_enabled': True, 'owner_qq': OWNER, 'proactive_owner_enabled': False}
        self._neutral_model = object()
        self._neutral_messenger = None
        self.browse_groups_enabled = self.browse_trips_enabled = False
        self.core = body.BioCore()
        self.core.sleepiness = self.core.hunger = self.core.physical_fatigue = .1
        self.core.last_sleep_end = self.core.last_meal = 0
        self.core._life_now_path = phone.NOW_PATH
        self.core._life_state_path = life.STATE_DIR / 'life.json'
        self.windows = {}
        self.self_model = {}
        self.spent = 0
        self.allowed = True
        self.calls = []
        self.answer = {'do': '休息', 'detail': '在家里歇着', 'minutes': 30}
        self._make_photo = AsyncMock(return_value=None)
        self._save_self_model = Mock()
        self._maybe_write_notebook = AsyncMock(return_value=True)
        self.replies = []
        self.forbidden = []

    def _core(self, event=None): return self.core
    def _attention_cfg(self): return {'soft': 8, 'hard': 10}
    def _spent_today(self): return self.spent
    def _browse_on(self): return self.config.get('browse_enabled', False)
    def _browse_names(self): return self._known_names(self._names_index())
    def _names_index(self): return {OWNER: {NAMED}, OTHER: {OTHER_NAME}}
    def _known_names(self, people):
        return [name for person in people
                for name in [str(person), *self._names_index().get(str(person), ())]]
    def _here(self, event): return event.place if event else ''
    def _addresses_her(self, event): return event.at_me
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows.get(here, [])}
    def _llm_allowed(self, kind): return self.allowed
    def _red_line(self, text, where): return ''
    def _owner_rules(self): return []
    def _read_library(self, vectors=True): return {'entries': []}
    def _write_library(self, lib): return True
    def _window_add_reply(self, event, text): self.replies.append(text)
    def _forbid(self, event, ident, text, people, vec=None): self.forbidden.append(text)
    def _history_store(self): return None
    async def _check_reply(self, event, text): return {'leak': False}
    async def _persona_text(self, event): return 'A fictional persona.'
    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answer if isinstance(self.answer, str) else json.dumps(self.answer, ensure_ascii=False)
        return parser(raw)


class LifeLoopMarksTests(unittest.IsolatedAsyncioTestCase):
    """What the tick makes of a thing put down, a plan come due and a waking."""

    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 2, 10).timestamp())
        for target, name, value in ((life, 'STATE_DIR', self.root / 'states'),
                                    (life, 'DATA_DIR', self.root),
                                    (phone, 'NOW_PATH', self.root / 'states' / 'now.json'),
                                    (phone, 'LOOK_PATH', self.root / 'states' / 'look.json'),
                                    (phone, 'STATE_DIR', self.root / 'states'),
                                    (life.time, 'time', self.clock)):
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)
        self.p = Person()

    async def asyncTearDown(self):
        await life.stop(self.p)

    def now(self): return datetime.fromtimestamp(self.clock())

    def today(self): return self.now().date().isoformat()

    def chosen(self, action='休息', minutes=30, detail='在家里歇着'):
        self.p._set_now('家里', detail, now=self.now(), minutes=minutes, source='her', kind=action)

    def rows(self): return her_days.Store(self.root).recent(20)

    async def tick(self, minutes=0):
        self.clock.advance(minutes * 60)
        return await life.tick(self.p)

    def thinking(self):
        """A reason to think now, without waiting for a thing of hers to end."""
        state = life.read_state()
        state.update({'crossed_pending': True, 'last_think_ts': self.clock() - 7200})
        life.save_state(state)

    def asleep(self, minutes=60, detail='在床上睡觉'):
        """Put her to bed now, the sleeping item and the sleep ending together."""
        self.chosen(action='睡觉', minutes=minutes, detail=detail)
        start = self.clock()
        state = life.read_state()
        state['sleep'] = {'start': int(start), 'end': int(start + minutes * 60)}
        life.save_state(state)
        return start

    async def test_5_a_put_down_thing_wakes_her_busy_and_inside_the_quiet_gate(self):
        self.chosen(action='写歌', minutes=40, detail='写歌')
        start = self.clock()
        life.save_state({'last_think_ts': start - 120, 'today': {'date': self.today(), 'count': 0},
                         'put_down': {'id': 'pd1', 'why': PUT_DOWN_WHY, 'ts': start,
                                      'here': 'private:' + OWNER}})
        # Two minutes since her last thinking: inside the 600 seconds, and still it calls her.
        self.assertTrue(await self.tick())
        prompt = self.p.calls[-1][1]
        until = (self.now() + timedelta(minutes=40)).strftime('%H:%M')
        self.assertIn('聊天里有件事你觉得要紧：' + PUT_DOWN_WHY, prompt)
        self.assertIn('你手上在做：写歌，打算到 ' + until, prompt)
        self.assertEqual(life.read_state()['handled_put_down'], 'pd1')
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)      # the same one never calls her twice

    async def test_6_while_asleep_nothing_calls_her_and_the_put_down_waits(self):
        start = self.asleep(minutes=60)
        state = life.read_state()
        state['put_down'] = {'id': 'pd1', 'why': PUT_DOWN_WHY, 'ts': start, 'here': 'private:' + OWNER}
        life.save_state(state)
        self.assertFalse(await self.tick(30))
        self.assertEqual(self.p.calls, [])
        self.assertEqual(life.read_state()['put_down']['why'], PUT_DOWN_WHY)
        self.assertTrue(await self.tick(30))        # the waking
        self.assertIn('你睡着的时候：', self.p.calls[-1][1])
        # Still waiting, and the next minute brings it
        self.assertTrue(await self.tick(1))
        self.assertIn(PUT_DOWN_WHY, self.p.calls[-1][1])

    async def test_7_going_on_with_what_she_had_keeps_it_and_its_end_still_calls_her(self):
        self.chosen(action='写歌', minutes=30, detail='写歌')
        item = dict(life.current())
        life.save_state({'handled_item': item['start'], 'today': {'date': self.today(), 'count': 0},
                         'last_think_ts': self.clock() - 7200})
        self.p.answer = {'do': life.CONTINUE_WORDS}
        self.thinking()
        self.assertTrue(await self.tick())
        self.assertIn(life.CONTINUE_WORDS, self.p.calls[-1][1])
        self.assertEqual(life.current(), item)      # the same thing, the same end
        self.assertEqual(self.rows(), [])           # and no line in her day
        self.assertNotIn('handled_item', life.read_state())
        self.p.answer = {'do': '休息', 'detail': '在家里歇着', 'minutes': 30}
        self.assertTrue(await self.tick(30))        # its own end calls her again
        self.assertIn('刚才那件事到时候了', self.p.calls[-1][1])

    async def test_8_going_on_is_offered_only_while_the_thing_lasts(self):
        self.chosen(action='写歌', minutes=30, detail='写歌')
        self.assertIn(life.CONTINUE_WORDS, life.menu(self.p))
        self.clock.advance(30 * 60)
        self.assertNotIn(life.CONTINUE_WORDS, life.menu(self.p))
        self.chosen(action='发呆', minutes=30, detail='发呆')     # dazing is not work
        self.assertNotIn(life.CONTINUE_WORDS, life.menu(self.p))
        self.thinking()
        self.assertTrue(await self.tick())
        self.assertNotIn(life.CONTINUE_WORDS, self.p.calls[-1][1])

    async def test_9_a_later_look_at_him_comes_due_once(self):
        self.chosen(action='发呆', minutes=180, detail='发呆')
        start = self.clock()
        life.save_state({'last_think_ts': start - 7200, 'today': {'date': self.today(), 'count': 0},
                         'due': [{'id': 'later1', 'ts': start + 30 * 60, 'kind': 'owner_later',
                                  'why': '他在修电脑', 'set_at': start}]})
        for _ in range(29):
            await self.tick(1)
        self.assertEqual(self.p.calls, [])
        self.assertTrue(await self.tick(1))
        self.assertIn('之前想过会儿再找他：他在修电脑', self.p.calls[-1][1])
        self.assertIn('那会儿想的', self.p.calls[-1][1])
        await self.tick(1)
        self.assertEqual(len(self.p.calls), 1)

    async def test_10b_a_later_answer_comes_due_with_the_tell_and_goes_out(self):
        self.chosen(action='发呆', minutes=180, detail='发呆')
        start = self.clock()
        life.save_state({'last_think_ts': start - 7200, 'today': {'date': self.today(), 'count': 0},
                         'due': [{'id': 'reply1', 'ts': start + 20 * 60,
                                  'kind': 'owner_reply_later', 'set_at': start}]})
        self.p.answer = {'do': '发呆', 'minutes': 180, 'tell': '想' * 300}
        sent = AsyncMock(return_value=SimpleNamespace(ok=True))
        self.p._neutral_messenger = SimpleNamespace(send=sent)
        for _ in range(19):
            await self.tick(1)
        self.assertEqual(self.p.calls, [])
        self.assertFalse(sent.await_count)
        self.assertTrue(await self.tick(1))
        prompt = self.p.calls[-1][1]
        self.assertIn('他 %s 找过你，你说过会儿再回'
                      % datetime.fromtimestamp(start).strftime('%H:%M'), prompt)
        self.assertIn('"tell"', prompt)
        self.assertIn('最多300字', prompt)
        self.assertEqual(sent.await_count, 1)       # it went out through tell_owner
        self.assertEqual(len(sent.await_args.args[1][0].data['text']), 300)

    async def test_11_the_tell_is_shown_only_when_he_spoke_first(self):
        self.chosen(action='发呆', minutes=180, detail='发呆')
        self.p.windows['private:' + OWNER] = [{'role': 'user', 'ts': self.clock(), 'text': '在吗'}]
        self.thinking()
        self.assertTrue(await self.tick())
        self.assertIn('"tell"', self.p.calls[-1][1])
        self.assertIn('最多300字', self.p.calls[-1][1])
        self.p.windows['private:' + OWNER] = [{'role': 'user', 'ts': self.clock(), 'text': '在吗'},
                                              {'role': 'assistant', 'ts': self.clock(), 'text': '在的'}]
        self.thinking()
        self.assertTrue(await self.tick(1))
        self.assertNotIn('tell', self.p.calls[-1][1])

    async def test_12_what_he_said_while_she_slept_is_marked(self):
        start = self.asleep(minutes=60)
        self.p.windows['private:' + OWNER] = [
            {'role': 'user', 'ts': start - 60, 'text': '睡前那句'},
            {'role': 'user', 'ts': start + 600, 'text': '睡着时第一句'},
            {'role': 'user', 'ts': start + 1200, 'text': '睡着时第二句'}]
        self.assertTrue(await self.tick(60))
        prompt = self.p.calls[-1][1]
        self.assertIn('睡着时第一句' + life.ASLEEP_MARK, prompt)
        self.assertIn('睡着时第二句' + life.ASLEEP_MARK, prompt)
        self.assertIn('睡前那句', prompt)
        self.assertNotIn('睡前那句' + life.ASLEEP_MARK, prompt)
        self.assertIn('你睡着的时候：', prompt)

    async def test_13_the_now_line_says_when_she_means_to_be_done(self):
        self.chosen(action='写歌', minutes=40, detail='写歌')
        until = (self.now() + timedelta(minutes=40)).strftime('%H:%M')
        line = self.p._now_line(None)
        self.assertIn('正在写歌', line)
        self.assertIn('打算到 ' + until, line)
        self.clock.advance(24 * 3600)       # the day's own schedule again: no end of hers
        self.assertNotIn('打算到', self.p._now_line(None))


class MarkWordsTests(unittest.TestCase):
    """The three marks as she is given them, and what she is told about them."""

    def test_the_note_says_what_she_may_write(self):
        self.assertEqual(attention.MARKS_NOTE,
                         '这件事要是比你手上在做的要紧，可以在最后写【放下手上的：为什么】。')
        self.assertIn('【过会儿再回：大概几分钟】', attention.MARKS_NOTE_OWNER)
        self.assertIn('【过会儿再找他：大概几分钟，为什么】', attention.MARKS_NOTE_OWNER)
        self.assertIn('这些不会发出去，不需要就别写。', attention.MARKS_NOTE_OWNER)
        self.assertNotIn('过会儿', attention.MARKS_NOTE)

    def test_the_marks_are_cut_out_and_read(self):
        clean, marks = attention.take_marks('好的【放下手上的：他要我看电脑】')
        self.assertEqual(clean, '好的')
        self.assertEqual(marks, [{'kind': 'put_down', 'why': '他要我看电脑', 'minutes': 0}])
        clean, marks = attention.take_marks('好的【过会儿再找他：30，他要我看电脑】', private=True)
        self.assertEqual(clean, '好的')
        self.assertEqual(marks, [{'kind': 'owner_later', 'why': '他要我看电脑', 'minutes': 30}])
        self.assertEqual(attention.take_marks('好的【过会儿再回：20】', private=True)[1],
                         [{'kind': 'owner_reply_later', 'why': '', 'minutes': 20}])
        # outside his private chat the two about him count as not written
        self.assertEqual(attention.take_marks('好的【过会儿再回：20】')[1], [])
        # minutes out of range, a why too long, or no closing bracket: cut out, not taken
        for text in ('【过会儿再回：0】', '【过会儿再回：1441】',
                     '【放下手上的：' + '为' * 41 + '】', '【放下手上的：没有右括号'):
            self.assertEqual(attention.take_marks(text, private=True)[1], [])


if __name__ == '__main__':
    unittest.main()
