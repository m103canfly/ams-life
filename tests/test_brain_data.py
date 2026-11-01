"""The brain map's real data (stage 2): the read-only pages page/brain, page/brain/node and
page/brain/search (mixin_brain.py, brain_graph.py), and what each reply recalled (ids only).
The plugin cases run in a fresh interpreter (tests/brain_cases.py). All numbers, names and
messages are made up.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
_CACHE = {}


def run_case(case):
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(HERE / 'brain_cases.py'), str(data), str(out), case],
                                  env=env, capture_output=True, text=True, encoding='utf-8', timeout=300)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


def kinds(graph, kind):
    return [n for n in graph['nodes'] if n['kind'] == kind]


class TheGraph(unittest.TestCase):
    def test_format_and_every_kind(self):
        g = run_case('graph')['graph']
        self.assertEqual(g['status'], 'ok')
        d = g['data']
        self.assertEqual((d['schema'], d['sample']), ('ams-life.brain/1', False))
        self.assertEqual(set(d['body']), {'social', 'curiosity', 'boredom', 'seen', 'talked', 'stress', 'valence'})
        self.assertEqual({n['kind'] for n in d['nodes']}, {'window', 'person', 'memory', 'event', 'note'})
        self.assertEqual({e['kind'] for e in d['edges']}, {'origin', 'about', 'impression', 'link'})
        ids = {n['id'] for n in d['nodes']}
        self.assertFalse([e for e in d['edges'] if e['s'] not in ids or e['t'] not in ids])
        for t in d['turns']:
            self.assertTrue(set(t['recalled']) | set(t['held']) <= ids)
            self.assertIn(t['where'], ids)

    def test_no_words_names_or_numbers(self):
        r = run_case('graph')
        for word in r['said'] + r['names'] + r['numbers']:
            self.assertNotIn(word, r['text'], word)
        for n in r['graph']['data']['nodes']:
            self.assertRegex(n['id'], r'^[wpmen]:[0-9a-f]{10}$')
            self.assertRegex(n['label'], r'^(群\d+|私聊\d+|人\d+|本子|听来的|她说的|私下|总结|[一-鿿]{1,4})$')

    def test_what_the_registry_rules_out_never_appears(self):
        r = run_case('graph')
        # 阿星 (10003) was forgotten everywhere: no star, no event, no notebook entry, no search hit
        self.assertNotIn('阿星', r['people'])
        self.assertEqual(r['search']['阿星'], [])
        self.assertEqual(r['search']['下雨'], [])
        self.assertEqual(len(kinds(r['graph']['data'], 'event')), 1)
        self.assertEqual(len(kinds(r['graph']['data'], 'note')), 2)
        # 桃子 (10004): her impression was deleted by the owner; she is there, the impression is not
        self.assertEqual([k for k, _v in r['people']['桃子']['detail']['lines']], ['跟这个人有关的'])
        self.assertEqual(len([e for e in r['graph']['data']['edges'] if e['kind'] == 'impression']), 2)

    def test_words_only_when_opened_and_qq_on_a_second_click(self):
        r = run_case('graph')
        orange = r['people']['阿橙']
        self.assertTrue(orange['detail']['has_qq'])
        self.assertNotIn('10001', json.dumps(orange['detail'], ensure_ascii=False))
        self.assertEqual(orange['qq'], {'qq': '10001'})
        self.assertIn(['她在群1的印象', '爱分享，常聊爬山'], orange['detail']['lines'])
        m = r['memory_detail']['data']
        self.assertEqual(m['text'], '小爱，跟你说个悄悄话，我在准备一个惊喜')
        self.assertIn(['能在哪说', '私下：只在那个私聊里'], m['lines'])
        self.assertEqual(r['window_titles'], ['群1', '群2', '跟阿橙的私聊'])
        self.assertEqual(r['missing']['status'], 'error')

    def test_a_card_of_digits_is_no_name(self):
        r = run_case('number_card')
        him = [t for t, p in r['people'].items() if p['qq'] == {'qq': '10006'}]
        self.assertEqual(len(him), 1)
        self.assertRegex(him[0], r'^人\d+$')                 # "人N", not the digits
        self.assertNotIn('10006', r['people'][him[0]]['detail'])
        self.assertNotIn('10006', r['text'])
        self.assertEqual(r['search'], [])                      # nor found by them
        self.assertIn('阿橙', r['people'])                      # others keep their names

    def test_numbers_kept_in_her_words_are_not_shown(self):
        # what she keeps keeps its numbers (the owner, 10-29); the page as before: a QQ number
        # only on a second click, a group's number never
        r = run_case('numbers_in_words')
        self.assertTrue([t for t in r['kept'] if '10002' in t and '900001' in t])
        said = [d for d in r['details'] if '我的号是' in d['text']]
        self.assertEqual([d['text'] for d in said], ['小爱 我的号是 [号码] 我们群号是 [号码] 周末去爬山'])
        for d in r['details']:
            self.assertNotIn('10002', json.dumps(d, ensure_ascii=False))
            self.assertNotIn('900001', json.dumps(d, ensure_ascii=False))
        self.assertNotIn('10002', r['text'])
        self.assertEqual(r['search']['10002'], [])                 # nor found by them
        self.assertEqual(r['search']['900001'], [])
        self.assertEqual(len(r['search']['我的号是']), 1)
        self.assertEqual(r['qq'], {'qq': '10002'})

    def test_frames_round_names_are_shown_as_kept(self):
        r = run_case('frames')
        self.assertTrue([t for t in r['details'] if '「柠檬」约「阿橙」' in t], r['details'])

    def test_search_gives_ids_only(self):
        r = run_case('graph')
        self.assertEqual(len(r['search']['吉他']), 1)
        self.assertTrue(all(x.startswith(('m:', 'p:', 'n:', 'e:')) for q in r['search'] for x in r['search'][q]))

    def test_read_only_and_behind_the_panel(self):
        r = run_case('graph')
        self.assertEqual(r['changed_on_disk'], [])           # opening the map writes nothing
        self.assertEqual(r['routes'], ['/astrbot_plugin_ams_life/page/brain', '/astrbot_plugin_ams_life/page/brain/node',
                                       '/astrbot_plugin_ams_life/page/brain/search'])
        src = (ROOT / 'mixin_pages.py').read_text('utf-8')
        for route in ('page/brain"', 'page/brain/node"', 'page/brain/search"'):
            line = next(x for x in src.splitlines() if route in x)
            self.assertIn('register(', line)                 # the dashboard's own routes: its login
            self.assertIn('["GET"]', line)


class Turns(unittest.TestCase):
    def test_ids_only_in_order_with_what_was_held(self):
        r = run_case('graph')
        turns = r['turns_file']
        text = json.dumps(turns, ensure_ascii=False)
        for word in r['said'] + r['names']:
            self.assertNotIn(word, text)
        for t in turns:
            self.assertEqual(set(t), {'ts', 'where', 'recalled', 'held', 'path', 'body'})
            self.assertTrue(set(t['recalled']) | set(t['held']) <= set(r['library_ids']))
        # the private secret: recalled in his private chat, held back in the group
        secret = [t for t in turns if t['where'] == 'private:10001'][0]['recalled'][0]
        self.assertTrue(any(secret in t['held'] for t in turns if t['where'] == 'group:900001'))
        self.assertFalse(any(secret in t['recalled'] for t in turns if t['where'] != 'private:10001'))

    def test_owner_deletes_take_them_out(self):
        r = run_case('deletes')
        before = r['before_turns']
        self.assertTrue(any(r['hike_id'] in t['recalled'] for t in before))
        self.assertEqual((r['hike_open_before'], r['hike_open_after']), ('ok', 'error'))
        self.assertFalse(any(r['hike_id'] in t['recalled'] + t['held'] + sum(t['path'], [])
                             for t in r['turns_after_memory']))
        self.assertEqual(r['answer_memory']['data']['counts']['turns'], 1)
        # the person: his private chat's turns and every memory of his
        after = r['turns_after_person']
        self.assertFalse([t for t in after if t['where'] == 'private:10001'])
        self.assertTrue(all(x in r['library_ids'] for t in after for x in t['recalled'] + t['held']))
        self.assertEqual(r['after_search']['吉他'], [])
        self.assertEqual(r['after_search']['阿橙'], [])
        self.assertEqual(r['old_ids_open'], ['error'])
        self.assertNotIn('阿橙', r['after_text'])

    def test_not_noted_when_something_was_forgotten_meanwhile(self):
        r = run_case('stale')
        self.assertEqual((r['noted'], r['n']), ({}, 0))
        self.assertEqual(len(r['noted_fresh']['recalled']), 2)            # 'not-a-memory' left out

    def test_a_restore_deletes_again(self):
        r = run_case('restore')
        self.assertEqual(r['restore']['status'], 'ok')
        self.assertEqual(r['private_turns'], [])
        self.assertEqual(r['unknown_ids'], [])
        self.assertTrue(r['lemon_turn_ids_before'])
        self.assertEqual(r['search']['吉他'], [])


class RegistryUnreadable(unittest.TestCase):
    def test_nothing_is_given_and_nothing_noted(self):
        r = run_case('registry_broken')
        for key in ('page', 'node', 'search'):
            self.assertEqual(r[key]['status'], 'error', key)
        self.assertNotIn('nodes', r['page']['data'])
        self.assertEqual(r['search']['data']['ids'], [])
        self.assertEqual(r['turns_noted_while_broken'], 0)
        self.assertEqual(r['page_rows']['status'], 'error')
        self.assertNotIn('nodes', r['page_rows']['data'])
        self.assertEqual(r['page_after'], 'ok')
        # the list too: nothing, and the one short reason
        for key in ('memories', 'memories_number'):
            self.assertEqual(r[key]['status'], 'error', key)
            self.assertIn('遗忘登记读不出来', r[key]['message'])
        self.assertEqual(r['memories']['data']['items'], [])


class Errors(unittest.TestCase):
    def test_only_a_short_reason(self):
        r = run_case('errors')
        for key in ('page', 'node', 'search', 'memories'):
            self.assertEqual(r[key]['status'], 'error', key)
            self.assertNotIn('made-up-folder', r[key]['message'], key)
            self.assertNotIn('x.json', r[key]['message'], key)
            self.assertIn('日志', r[key]['message'], key)


class Memories(unittest.TestCase):
    """"她记住了什么" (page/memories, memory_list.py): the map's snapshot as a list, read only."""

    @classmethod
    def setUpClass(cls):
        cls.r = run_case('memories')
        cls.items = cls.r['first']['data']['items']

    def test_four_kinds_newest_first(self):
        kinds = {k: len(v) for k, v in self.r['by_kind'].items()}
        self.assertEqual(kinds, {'memory': 14, 'event': 1, 'note': 2, 'impression': 2})
        self.assertEqual(self.r['first']['data']['total'], 19)
        ts = [i['ts'] for i in self.items]
        self.assertEqual(ts, sorted(ts, reverse=True))
        self.assertEqual(self.r['routes'], ['/astrbot_plugin_ams_life/page/memories',
                                            '/astrbot_plugin_ams_life/page/memories/number'])

    def test_where_when_who_and_where_it_may_be_said(self):
        by_text = {i['text']: i for i in self.items}
        note = by_text['阿橙好像在准备惊喜']
        self.assertEqual((note['kind'], note['where'], note['vis'], note['who']), ('note', '私聊1', 'private', ['阿橙']))
        self.assertEqual(note['may'], '私下：只在那个私聊里')
        own = by_text['想多听听大家在聊什么']
        self.assertEqual((own['where'], own['vis'], own['who']), ('她自己', 'self', []))
        imp = by_text['叫“阿橙”；说话：爱分享；常聊：爬山']
        self.assertEqual((imp['kind'], imp['where'], imp['vis']), ('impression', '群1', 'public'))
        self.assertTrue(all(i['date'] for i in self.items))
        self.assertEqual([p['label'] for p in self.r['places']], ['群1', '群2', '私聊1'])
        self.assertTrue(all(set(i) == {'id', 'kind', 'kind_name', 'place', 'where', 'ts', 'date', 'vis', 'may', 'who',
                                       'text', 'has_number', 'entry'} for i in self.items))   # not the whole record

    def test_what_the_registry_rules_out_never_appears(self):
        text = json.dumps(self.r['first'], ensure_ascii=False)
        for word in ('阿星', '下雨', '总是半夜出现', '话不多'):   # forgotten; impression stopped
            self.assertNotIn(word, text)
        for number in ('10001', '10002', '10003', '10004', '900001', '900002'):
            self.assertNotIn(number, text)

    def test_pages_and_filters(self):
        pages = self.r['pages']
        self.assertEqual([len(p) for p in pages], [3, 3, 3, 3, 3, 3, 1])
        joined = [i for p in pages for i in p]
        self.assertEqual(joined, [i['id'] for i in self.items])                  # every row once, in order
        self.assertEqual(set(self.r['private']), {'private'})
        self.assertEqual(len(self.r['private']), 5)
        self.assertEqual(self.r['in_g1'], ['群1'])
        self.assertTrue(self.r['q'] and all('爬山' in t for t in self.r['q']))
        self.assertEqual(self.r['today'], 17)                                    # the impressions are dated by day
        self.assertEqual(self.r['long_ago'], 0)

    def test_numbers_hidden_until_asked(self):
        [row] = self.r['numbered']
        self.assertEqual(row['text'], '小爱 我的游戏号是 [号码] 记得加我')
        self.assertNotIn('12345678', json.dumps(self.r['first'], ensure_ascii=False))
        self.assertEqual(self.r['q_number'], 0)                                  # not found by the hidden number
        self.assertEqual(self.r['number'], {'status': 'ok', 'data': {'id': row['id'], 'text': '小爱 我的游戏号是 12345678 记得加我'}})
        self.assertEqual(self.r['number_missing']['status'], 'error')

    def test_only_memories_can_be_deleted_and_nothing_written(self):
        self.assertTrue(all(bool(i['entry']) == (i['kind'] == 'memory') for i in self.items))
        self.assertEqual(self.r['changed_on_disk'], [])


class Threads(unittest.TestCase):
    def test_files_read_where_she_writes_them(self):
        r = run_case('threads')
        self.assertEqual(r['status'], 'ok')
        self.assertTrue(r['read_on_loop'])
        self.assertTrue(r['built_elsewhere'])
        self.assertEqual(r['memories_status'], 'ok')
        self.assertTrue(r['memories_read_on_loop'])
        self.assertTrue(r['memories_built_elsewhere'])


class Parts(unittest.TestCase):
    def test_in_parts_of_one_build(self):
        r = run_case('paging')
        self.assertGreater(r['parts'], 1)
        self.assertEqual(r['unique_nodes'], r['whole_nodes'])
        self.assertEqual(r['dangling'], [])
        # not an error (AstrBot's bridge would drop the flag): the page starts again
        self.assertEqual(r['wrong_snap'], {'status': 'ok', 'data': {'stale': True}})
        self.assertEqual(r['after_delete'], {'status': 'ok', 'data': {'stale': True}})


class TurnLogRules(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(HERE / 'stubs'))
        sys.path.insert(0, str(ROOT))
        import brain_graph
        self.bg = brain_graph
        self.tmp = tempfile.TemporaryDirectory()
        self.log = brain_graph.TurnLog(Path(self.tmp.name) / 'turns.json')

    def tearDown(self):
        self.tmp.cleanup()

    def test_last_200_only(self):
        for i in range(210):
            self.log.add({'ts': i, 'where': 'group:1', 'recalled': ['m%d' % i]})
        turns = self.log.read()
        self.assertEqual(len(turns), 200)
        self.assertEqual(turns[0]['recalled'], ['m10'])

    def test_only_ids_kept(self):
        self.log.add({'ts': 1, 'where': 'group:1', 'recalled': ['a', 'b'], 'held': ['c', 'a'],
                      'path': [['a', 'b'], ['a', 'zz']], 'text': '不该存的话', 'body': {'stress': 0.5, 'note': 'x'}})
        row = self.log.read()[0]
        self.assertEqual(row, {'ts': 1.0, 'where': 'group:1', 'recalled': ['a', 'b'], 'held': ['c'],
                               'path': [['a', 'b']], 'body': {'stress': 0.5}})

    def test_prune(self):
        self.log.add({'ts': 1, 'where': 'private:7', 'recalled': ['a']})
        self.log.add({'ts': 2, 'where': 'group:1', 'recalled': ['a', 'b'], 'path': [['a', 'b']]})
        self.log.add({'ts': 3, 'where': 'group:1', 'held': ['a']})
        self.assertEqual(self.log.prune(gone_ids=['a'], gone_places=['private:7']), 3)
        self.assertEqual(self.log.read(), [{'ts': 2.0, 'where': 'group:1', 'recalled': ['b'], 'held': [], 'path': []}])
        self.assertEqual(self.log.prune(keep_ids=['x']), 1)
        self.assertEqual(self.log.read(), [])

    def test_ids_do_not_give_numbers_away(self):
        ids = self.bg.PageIds(b'k' * 16)
        a, b = ids('p', '10001'), self.bg.PageIds(b'j' * 16)('p', '10001')
        self.assertNotEqual(a, b)                       # a new key, new ids
        self.assertEqual(a, ids('p', '10001'))          # the same person, the same id
        self.assertNotIn('10001', a)


if __name__ == '__main__':
    unittest.main()
