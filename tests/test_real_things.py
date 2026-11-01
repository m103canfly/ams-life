# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What she really made: a song, a reading note, dazing, and her wish list.

The card's tests 1-7: a choice must leave something she can show, or the day says
it was not done; a made work is remembered; the private chat is never in the call
that writes it.
"""
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import body  # noqa: E402
import discretion  # noqa: E402
import harness  # noqa: E402
import her_days  # noqa: E402
import life_loop as life  # noqa: E402
import mixin_selfie as phone  # noqa: E402
import works  # noqa: E402

OWNER = '10001'           # made-up
OWNER_NAME = '虚构小甲'    # made-up
OTHER = '10003'           # made-up
OTHER_NAME = '虚构小乙'    # made-up
SECRET = '私聊里的暗号'     # made-up: only ever in his private window
PAGE = 'https://example.invalid/a'
PRIVATE_PAGE = 'https://example.invalid/b'


def web_entry(ident, url, title, ts, shared_in=''):
    origin = discretion.make_origin('web:' + url)
    if shared_in:
        origin['shared_in'] = shared_in
    return {'id': ident, 'ts': ts, 'role': 'web', 'text': '%s：一句话（%s）' % (title, url),
            'origin': origin, 'web': {'url': url, 'title': title}}


class Person(phone.SelfieMixin):
    """The few things life_loop wants from the plugin; all files stay in the test's folder."""

    def __init__(self):
        self.enabled = True
        self.config = {'life_loop_enabled': True, 'owner_qq': OWNER}
        self._neutral_model = object()
        self.browse_groups_enabled = self.browse_trips_enabled = False
        self.core = body.BioCore()
        self.core.sleepiness = self.core.hunger = self.core.physical_fatigue = .1
        self.core._life_now_path = phone.NOW_PATH
        self.core._life_state_path = life.STATE_DIR / 'life.json'
        self.windows = {}
        self.self_model = {'notebook': []}
        self.library = {'entries': [], 'rooms': {}}
        self.spent = 0
        self.allowed = True
        self.calls = []
        self.answers = []
        self.answer = {'do': '休息', 'detail': '在家里坐着', 'minutes': 30}
        self._save_self_model = Mock()
        self._maybe_write_notebook = AsyncMock(return_value=True)

    def _core(self, event=None): return self.core
    def _attention_cfg(self): return {'soft': 8, 'hard': 10}
    def _spent_today(self): return self.spent
    def _browse_on(self): return self.config.get('browse_enabled', False)
    def _browse_names(self): return self._known_names(self._names_index())
    def _names_index(self): return {OWNER: {OWNER_NAME}, OTHER: {OTHER_NAME}}
    def _known_names(self, people):
        return [name for person in people for name in [str(person), *self._names_index()[person]]]
    def _here(self, event): return event.place if event else ''
    def _addresses_her(self, event): return event.at_me
    def _window_places(self): return list(self.windows)
    def _read_window(self, here): return {'recent': self.windows[here]}
    def _llm_allowed(self, kind): return self.allowed
    def _red_line(self, text, where): return ''
    def _read_library(self, vectors=True): return self.library
    def _write_library(self, lib):
        self.library = lib
        return True
    def _new_memory_id(self, *seed): return 'memory-%d' % len(self.library['entries'])
    async def _embed_text(self, text): return [0.1, 0.2]
    async def _persona_text(self, event): return 'A fictional persona.'

    async def _llm_v2_call(self, kind, prompt, parser, **kwargs):
        self.calls.append((kind, prompt))
        raw = self.answers.pop(0) if self.answers else json.dumps(self.answer, ensure_ascii=False)
        return parser(raw)


class RealThingsTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'states').mkdir()
        self.clock = harness.Clock(datetime(2026, 11, 1, 10).timestamp())
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

    def rows(self):
        return her_days.Store(self.root).recent(20)

    def chat(self, rows):
        self.p.windows['private:' + OWNER] = rows

    async def tick(self, minutes=0):
        self.clock.advance(minutes * 60)
        return await life.tick(self.p)

    def choice(self, action, **changes):
        value = {'do': action, 'detail': '在家里坐着', 'minutes': 30}
        value.update(changes)
        return json.dumps(value, ensure_ascii=False)

    # 1. A song: one work, one memory of her own, and no private chat in that call.
    async def test_a_song_choice_keeps_a_song_and_one_self_memory(self):
        self.chat([{'role': 'user', 'ts': self.clock() - 60, 'text': SECRET}])
        self.p.answers = [self.choice('写歌', detail='在窗边写歌', minutes=40),
                          json.dumps({'title': '窗边', 'lyrics': '风从窗外来\n灯在桌上亮'}, ensure_ascii=False)]
        self.assertTrue(await self.tick())
        made = works.read(self.root)
        self.assertEqual([item['kind'] for item in made], ['song'])
        self.assertEqual(made[0]['title'], '窗边')
        self.assertEqual(made[0]['url'], '')
        self.assertEqual(made[0]['origin']['where'], 'self')
        self.assertEqual(self.rows()[0]['do'], '写歌')
        self.assertEqual(self.rows()[0]['work'], made[0]['id'])
        self.assertEqual([item['memory_source'] for item in self.p.library['entries']], ['self'])
        remembered = self.p.library['entries'][0]['text']
        self.assertIn('我写了首歌《窗边》', remembered)
        self.assertIn('风从窗外来', remembered)
        self.assertIn(SECRET, self.p.calls[0][1])        # the chat was there when she picked
        song_prompt = self.p.calls[1][1]
        self.assertNotIn(SECRET, song_prompt)            # and not when she wrote the song
        self.assertIn('写一首歌', song_prompt)

    # 2. A red line means nothing is kept and the day says it was not done.
    async def test_a_song_over_a_red_line_is_not_kept_and_the_day_says_so(self):
        self.p.answers = [self.choice('写歌', detail='在家里写歌'),
                          json.dumps({'title': '今天', 'lyrics': '写到一半去医院了'}, ensure_ascii=False)]
        self.assertTrue(await self.tick())
        self.assertEqual(works.read(self.root), [])
        self.assertEqual(self.p.library['entries'], [])
        row = self.rows()[0]
        self.assertEqual(row['do'], '写歌')
        self.assertEqual(row['detail'], '想写歌，没写出来')
        self.assertEqual(row['work'], '')
        self.assertEqual(life.current()['doing'], '想写歌，没写出来')

    # 2 again: a name is taken out, his too, and the song is still kept.
    async def test_a_song_with_names_in_it_keeps_the_names_out(self):
        self.p.answers = [self.choice('写歌', detail='在窗边写歌'),
                          json.dumps({'title': '写给%s' % OTHER_NAME,
                                      'lyrics': '%s和%s在窗边' % (OTHER_NAME, OWNER_NAME)},
                                     ensure_ascii=False)]
        self.assertTrue(await self.tick())
        made = works.read(self.root)
        self.assertEqual(len(made), 1)
        for name in (OTHER_NAME, OWNER_NAME):
            self.assertNotIn(name, made[0]['title'])
            self.assertNotIn(name, made[0]['text'])
        self.assertIn('有人', made[0]['text'])
        self.assertEqual(len(self.p.library['entries']), 1)

    # 3. A reading note: only pages she may say anywhere are offered, and she picks one.
    async def test_a_reading_note_comes_from_a_page_she_may_say_anywhere(self):
        self.p.config['browse_enabled'] = True
        self.p.library['entries'] = [web_entry('open-page', PAGE, '能公开的标题', 200.0),
                                     web_entry('private-page', PRIVATE_PAGE, '私聊给的标题', 300.0,
                                               shared_in='private:' + OWNER)]
        self.p.answers = [self.choice(life.REVIEW_WORDS, detail='在桌前看文章'),
                          json.dumps({'read': '1'}, ensure_ascii=False),
                          json.dumps({'review': '这篇讲得挺有意思。'}, ensure_ascii=False)]
        self.assertTrue(await self.tick())
        pick_prompt = self.p.calls[1][1]
        self.assertIn('能公开的标题', pick_prompt)
        self.assertNotIn('私聊给的标题', pick_prompt)
        self.assertNotIn(SECRET, pick_prompt)
        made = works.read(self.root)
        self.assertEqual([item['kind'] for item in made], ['review'])
        self.assertEqual(made[0]['title'], '能公开的标题')
        self.assertEqual(made[0]['url'], PAGE)
        self.assertEqual(self.rows()[0]['work'], made[0]['id'])
        remembered = [item['text'] for item in self.p.library['entries'] if item.get('memory_source') == 'self']
        self.assertEqual(len(remembered), 1)
        self.assertIn('我读了《能公开的标题》', remembered[0])

    # 3 again: nothing of hers to read, so she goes for a look first.
    async def test_a_reading_note_with_nothing_to_read_goes_for_a_look_first(self):
        self.p.config['browse_enabled'] = True
        self.p.answers = [self.choice(life.REVIEW_WORDS, detail='想写读后感')]
        self.assertTrue(await self.tick())
        self.assertEqual(len(self.p.calls), 1)          # nobody was asked to pick
        self.assertTrue(life.read_state()['pending']['go_browse'])
        self.assertEqual(works.read(self.root), [])
        self.assertEqual(self.rows()[0]['detail'], '想写读后感，没有能读的文章')

    # 4. Dazing: no call of its own, no detail, and "此刻" says 发呆.
    async def test_dazing_calls_no_model_and_says_so(self):
        self.p.answers = [self.choice('发呆', detail='在家里发呆')]
        self.assertTrue(await self.tick())
        self.assertEqual(len(self.p.calls), 1)          # only the pick itself
        self.assertEqual(life.current()['doing'], '发呆')
        self.assertEqual(life.current()['kind'], '发呆')
        self.assertIn('正在发呆', self.p._now_line(None))
        self.assertEqual(self.rows()[0]['detail'], '')
        self.assertEqual(self.p.library['entries'], [])
        self.assertEqual(works.read(self.root), [])

    async def test_the_old_name_for_dazing_is_still_dazing(self):
        self.p.answers = [json.dumps({'do': '什么都不干', 'minutes': 30}, ensure_ascii=False)]
        self.assertTrue(await self.tick())
        self.assertEqual(life.current()['kind'], '发呆')

    # 5. A notebook already written today is not offered again.
    def test_a_written_notebook_is_not_offered_again(self):
        self.assertIn(life.NOTEBOOK_WORDS, life.menu(self.p))
        life.save_state(dict(life.read_state(), notebook_done=life.notebook_day(self.clock())))
        self.assertNotIn(life.NOTEBOOK_WORDS, life.menu(self.p))

    async def test_the_notebook_choice_writes_it_once(self):
        self.p.answers = [self.choice(life.NOTEBOOK_WORDS, detail='在桌边整理本子')]
        self.assertTrue(await self.tick())
        self.p._maybe_write_notebook.assert_awaited_once()
        self.assertEqual(self.rows()[0]['do'], life.NOTEBOOK_WORDS)

    # 6. A wish goes into the notebook's "想做的", once.
    async def test_a_wish_goes_into_the_notebook_once(self):
        self.p.answers = [self.choice('休息', detail='在沙发上坐着', wish='想学弹吉他')]
        self.assertTrue(await self.tick())
        wanted = her_days.notebook_sections(self.p.self_model['notebook'])['想做的']
        self.assertEqual([item['text'] for item in wanted], ['想学弹吉他'])
        self.assertEqual(wanted[0]['origin']['where'], 'self')
        value = {'do': '休息', 'detail': '在沙发上坐着', 'minutes': 30, 'liked_last': '',
                 'post': '', 'look': '', 'wish': '想学弹吉他'}
        await life.apply_choice(self.p, value, self.p.core, self.clock(), '')
        self.assertEqual(len(her_days.notebook_sections(self.p.self_model['notebook'])['想做的']), 1)

    async def test_a_wish_over_a_red_line_is_not_kept(self):
        self.p.answers = [self.choice('休息', wish='想请假去医院看看')]
        await self.tick()
        self.assertEqual(her_days.notebook_sections(self.p.self_model['notebook'])['想做的'], [])

    # 7. The public-line call is shown the works she made lately.
    async def test_the_public_line_is_shown_what_she_made(self):
        works.add(self.root, 'song', '窗边的歌', '风从窗外来\n灯在桌上亮', now=self.clock())
        self.p.answers = [json.dumps({'post': '今天写了首歌'}, ensure_ascii=False)]
        self.assertEqual(await life.write_post(self.p, self.p.core, self.clock(), 'test'), '今天写了首歌')
        prompt = self.p.calls[-1][1]
        self.assertIn('最近的作品', prompt)
        self.assertIn('窗边的歌', prompt)
        self.assertIn('风从窗外来', prompt)
        self.assertIn('灯在桌上亮', prompt)

    def test_a_work_shows_its_first_two_lines(self):
        work = {'kind': 'song', 'title': '窗边', 'text': '第一句\n第二句\n第三句'}
        self.assertIn('第一句', works.memory_line(work))


class WorkWords(unittest.TestCase):
    """The words of a choice and of a work: no plugin, no files."""

    def test_a_work_shows_only_its_opening_lines(self):
        work = {'kind': 'song', 'title': '窗边', 'text': '第一句\n第二句\n第三句'}
        self.assertEqual(works.head(work), '第一句；第二句')

    def test_the_old_name_for_dazing_is_read_as_dazing(self):
        for name in ('发呆', '什么都不干'):
            value = life.parse(json.dumps({'do': name, 'minutes': 30}), life.BASE_MENU)
            self.assertEqual(value['do'], life.DAZE)
        self.assertIsNone(life.parse(json.dumps({'do': '写歌', 'minutes': 30}), life.BASE_MENU[:4]))

    def test_a_wish_is_kept_short_and_a_non_text_one_is_refused(self):
        value = life.parse(json.dumps({'do': '休息', 'wish': '想' * 120}), life.BASE_MENU)
        self.assertEqual(len(value['wish']), 100)
        self.assertEqual(life.parse(json.dumps({'do': '休息', 'wish': 5}), life.BASE_MENU), None)

    def test_a_song_needs_a_title_and_lyrics(self):
        self.assertEqual(life.parse_song(json.dumps({'title': '窗 边', 'lyrics': '一\n二'},
                                                    ensure_ascii=False)),
                         {'title': '窗 边', 'lyrics': '一\n二'})
        for raw in ('{}', '{"title":"窗边"}', '{"title":5,"lyrics":"一"}', '[]'):
            self.assertIsNone(life.parse_song(raw))

    def test_a_picked_page_is_one_of_the_numbers_shown(self):
        self.assertEqual(life.parse_pick(json.dumps({'read': '2'}), 3), 1)
        self.assertEqual(life.parse_pick(json.dumps({'read': ['1']}), 3), 0)
        for raw in ('{}', '{"read":"4"}', '{"read":"x"}', '{"read":"0"}'):
            self.assertIsNone(life.parse_pick(raw, 3))

    def test_a_reading_note_needs_its_text(self):
        self.assertEqual(life.parse_review(json.dumps({'review': ' 好 '})), {'review': '好'})
        for raw in ('{}', '{"review":5}', '{"review":"  "}'):
            self.assertIsNone(life.parse_review(raw))

    def test_a_work_memory_is_one_line_of_her_own(self):
        song = {'kind': 'song', 'title': '窗边', 'text': '风从窗外来\n灯在桌上亮'}
        self.assertEqual(works.memory_line(song), '我写了首歌《窗边》：风从窗外来；灯在桌上亮')
        review = {'kind': 'review', 'title': '一篇文章', 'text': '写得很好。后面还有'}
        self.assertEqual(works.memory_line(review), '我读了《一篇文章》，觉得写得很好')


class WorkStore(unittest.TestCase):
    def test_each_work_is_one_line_of_her_own(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = works.add(tmp, 'song', '窗边', '风从窗外来', now=100)
            self.assertEqual(set(row), {'id', 'ts', 'kind', 'title', 'text', 'url', 'origin'})
            self.assertEqual(row['origin']['where'], 'self')
            self.assertEqual(works.add(tmp, 'other', '窗边', '风从窗外来'), {})
            self.assertEqual(works.add(tmp, 'song', '', '风从窗外来'), {})
            self.assertEqual(len(works.read(tmp)), 1)
            later = works.add(tmp, 'review', '一篇文章', '写得很好', url=PAGE, now=200)
            self.assertEqual([item['id'] for item in works.recent(tmp, 1)], [later['id']])


if __name__ == '__main__':
    unittest.main()
