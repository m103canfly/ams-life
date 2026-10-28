"""Her body as an electronic ghost, how it tells the reply model, and her heart (step 1-2).

The conversations run in discretion_cases.py (a fresh interpreter each, like the
golden test); the small pieces are unit-tested here. All names and numbers are made up.
"""
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402
from test_discretion import run_case  # noqa: E402

DATA = Path(tempfile.mkdtemp(prefix='ams-life-body-'))
CLOCK = harness.prepare(DATA)
import body  # noqa: E402
import homeostasis  # noqa: E402
import interpretation  # noqa: E402

QQ = ('10001', '10002', '10003', '10004', '10005', '20002')
NAMES = ('柠檬', '阿星', '芒果', '桃子', '路人')
# words that tell the model how to reply (the old plan= / hint= / [BC-Return] lines)
INSTRUCTIONS = ('回复', '先接住', '先按', '别解释', '别报', '接就好', '不要', '<bc>', 'BC-Return', 'BC-Note',
                'plan', 'hint', '应该')
GONE = ('trust', 'circadian_alertness', 'user_trust_seeded', 'user_trust_seed_delta', 'reflection_tree')


class Body(unittest.TestCase):
    def test_no_physiology_no_global_trust(self):
        core = body.BioCore()
        core.observe('小爱 早上好')
        snap = core.snapshot()
        for key in GONE:
            self.assertNotIn(key, snap)
        for key in ('body', 'need_pyramid', 'interoception'):
            self.assertNotIn(key, snap['homeostasis'])
        self.assertEqual(set(snap['homeostasis']['drives']), {'social', 'curiosity', 'seen'})
        for key in ('seen_need', 'talked', 'ambient'):
            self.assertIn(key, snap)

    def test_talking_adds_up_and_fades(self):
        core = body.BioCore()
        for _ in range(10):
            core.record_talk('今天聊得好开心呀' * 8)
        high = core.talked
        self.assertGreater(high, 0.5)
        CLOCK.advance(4 * 3600)
        core._decay_to_now()
        self.assertAlmostEqual(core.talked, high / 2, places=2)

    def test_wanting_to_be_seen_grows_while_nobody_answers(self):
        core = body.BioCore()
        core.be_seen()
        low = core.seen_need
        CLOCK.advance(12 * 3600)
        core._decay_to_now()
        self.assertGreater(core.seen_need, low + 0.3)
        core.be_seen()
        self.assertLess(core.seen_need, 0.5)

    def test_quiet_chats_settle_her_lower_than_busy_ones(self):
        quiet, busy = body.BioCore(), body.BioCore()
        quiet.set_ambient(0.0)
        busy.set_ambient(1.0)
        for core in (quiet, busy):
            core.a = 0.9
        CLOCK.advance(10 * 3600)
        quiet._decay_to_now()
        busy._decay_to_now()
        self.assertLess(quiet.a, busy.a)

    def test_the_persons_trust_is_used_for_one_call_and_not_kept(self):
        core = body.BioCore()
        core.observe('谢谢你陪我', relationship={'state': {'trust': 0.95}})
        self.assertIsNone(core._partner_trust)
        self.assertEqual(core._trust(), 0.5)
        self.assertNotIn('trust', core.snapshot())

    def test_habituation_keeps_fingerprints_not_words(self):
        core = body.BioCore()
        text = '气死我了！！！他凭什么这样说我'
        for _ in range(3):
            core.observe(text)
        kept = [core._novelty_history, core._sensitization_history, core.stimuli]
        self.assertNotIn('他凭什么', repr(kept))
        self.assertTrue(core._novelty_history)
        self.assertTrue(all(isinstance(x, tuple) for x in core._novelty_history))
        self.assertTrue(all('fp' in x and 'text' not in x for x in core.stimuli))
        # ... and repeating the same thing still bores her
        self.assertGreater(core.boredom, 0.05)

    def test_fingerprints_tell_alike_from_different(self):
        a, b, c = '今天抽卡又歪了好气', '今天抽卡又歪了好气啊', '明天一起去看海吧'
        same = body._fingerprint_similarity(body._fingerprint(a), body._fingerprint(b))
        other = body._fingerprint_similarity(body._fingerprint(a), body._fingerprint(c))
        self.assertGreater(same, 0.55)
        self.assertLess(other, 0.2)

    def test_decay_counts_time_between_close_calls(self):
        # calls under 30 seconds apart used to throw that time away
        often, once = body.BioCore(), body.BioCore()
        for core in (often, once):
            core.v, core.a = -0.8, 0.9
            core._decay_to_now()
        for _ in range(180):  # every 20 seconds for an hour
            CLOCK.advance(20)
            often._decay_to_now()
        once._decay_to_now()
        self.assertGreater(often.v, -0.6)
        self.assertAlmostEqual(often.v, once.v, places=2)

    def test_old_homeostasis_is_cut_down(self):
        state = homeostasis.normalize_state({'body': {'hydration': 0.2}, 'need_pyramid': {'dominant': 'esteem'},
                                             'drives': {'energy': 0.9, 'social': 0.4}})
        for key in ('body', 'need_pyramid', 'interoception'):
            self.assertNotIn(key, state)
        self.assertEqual(set(state['drives']), {'social', 'curiosity', 'seen'})
        self.assertEqual(state['drives']['social'], 0.4)


class TellingTheMouth(unittest.TestCase):
    def test_body_line_describes_without_numbers_names_or_instructions(self):
        core = body.BioCore()
        core.v, core.talked, core.ambient = -0.5, 0.9, 0.8
        text = interpretation.render_compact(core, memory='- 对方说过：明天考试', user={'interactions': 30})
        first = text.splitlines()[0]
        self.assertTrue(first.startswith('[她现在] '))
        self.assertIn('心里有点沉', first)
        self.assertIn('今天说得太多了', first)
        self.assertIn('热闹', first)
        self.assertNotRegex(text, r'\d')
        for word in INSTRUCTIONS:
            self.assertNotIn(word, text)

    def test_how_she_stands_with_him_in_a_group_and_in_private(self):
        him = {'interactions': 30, 'absence': {'bucket': 'long'},
               'relationship': {'state': {'closeness': 0.8, 'conflict': 0.6},
                                'repair_state': {'phase': 'stable'},
                                'transactive_map': {'抽卡': 5}}}
        self.assertEqual(interpretation.relation_brief(him, private_with_him=False), '挺熟')
        private = interpretation.relation_brief(him, private_with_him=True)
        for word in ('挺熟', '挺亲近', '最近有点别扭', '很久没聊了', '常聊抽卡'):
            self.assertIn(word, private)
        making_up = dict(him, relationship=dict(him['relationship'], repair_state={'phase': 'repairing'}))
        self.assertEqual(interpretation.relation_brief(making_up), '挺熟')
        self.assertIn('还在和好的过程中', interpretation.relation_brief(making_up, private_with_him=True))

    def test_every_kind_of_state_tag_is_cut(self):
        cut = interpretation.strip_state_tags
        self.assertEqual(cut('好呀<bc v="1">{"e":"joy"}</bc>'), '好呀')
        self.assertEqual(cut('对<bc>外<bc>{}</bc>层</bc>呀'), '对呀')
        self.assertEqual(cut('是</bc>呀'), '是呀')
        self.assertEqual(cut('嗯<BC data=x>{坏'), '嗯')
        self.assertEqual(cut('好<biocore a="1"/>的'), '好的')
        self.assertEqual(cut('<bc>1</bc>中<bc>2</bc>'), '中')
        self.assertEqual(cut('小于号 a<b 不动'), '小于号 a<b 不动')

    def test_wanting_to_be_seen_is_never_written(self):
        core = body.BioCore()
        for seen in (0.0, 1.0):
            core.seen_need = seen
            self.assertNotIn('看见', interpretation.render_compact(core))

    def test_prompts_in_a_conversation(self):
        r = run_case('prompt_shape')
        for prompt in (r['group'], r['private']):
            self.assertTrue(prompt.startswith('[她现在] '))
            self.assertNotIn('[BC]', prompt)
            self.assertNotRegex(prompt, r'\b[a-z]+=')
            for qq in QQ:
                self.assertNotIn(qq, prompt)
            for word in INSTRUCTIONS:
                self.assertNotIn(word, prompt)
            # nobody is named outside what she recalls
            for line in prompt.splitlines():
                if not line.startswith('[她想起来的]'):
                    for name in NAMES:
                        self.assertNotIn(name, line)
        self.assertIn('[没做完的] 小爱，记得提醒我明天交报告', r['group'])
        self.assertIn('[她想起来的] 阿星说过：', r['group'])
        for name in NAMES:  # in the private chat the group's lines come without names
            self.assertNotIn(name, r['private'])

    def test_recalled_speakers_named_here_anonymous_elsewhere(self):
        r = run_case('names')
        self.assertIn('柠檬说过', r['same_group'])
        self.assertIn('阿星说过', r['same_group'])
        self.assertIn('（别处）有人说过', r['other_group'])
        self.assertIn('芒果说过', r['private'])
        for name in NAMES:  # another group hears what, never who
            self.assertNotIn(name, r['other_group'])
        for prompt in (r['same_group'], r['other_group']):  # the private surprise stays private
            self.assertNotIn('惊喜', prompt)
        for prompt in (r['same_group'], r['other_group'], r['private']):
            for qq in QQ:
                self.assertNotIn(qq, prompt)

    def test_a_tag_the_model_writes_is_cut_and_not_used(self):
        r = run_case('reply_tags')
        self.assertEqual(r['replies'], ['好呀', '好的', '嗯嗯', '行', '对', '是呀'])
        self.assertEqual(r['v0'], r['v1'])
        for text in r['window'] + r['memories']:
            self.assertNotIn('<', text)


class Listening(unittest.TestCase):
    def test_many_messages_do_not_reread_every_window(self):
        r = run_case('ambient_reads')
        self.assertEqual(r['other_reads'], 0)
        self.assertAlmostEqual(r['ambient'], r['expected'], places=3)

    def test_the_message_that_wakes_her_counts_once(self):
        self.assertEqual(run_case('woken_once')['seen_calls'], 1)

    def test_switched_off_listening_does_not_touch_the_body(self):
        r = run_case('listen_off')
        self.assertEqual(r['seen_after_at'], 0.9)
        self.assertEqual(r['ambient'], 0.0)

    def test_an_at_means_she_was_seen_and_the_chat_is_lively(self):
        r = run_case('listen_on')
        self.assertLess(r['seen_after_at'], 0.5)
        self.assertEqual(r['ambient'], 1)


class OldState(unittest.TestCase):
    def test_old_body_fields_are_dropped_and_the_file_kept(self):
        r = run_case('old_body')
        self.assertTrue(r['kept_body'])
        for her in (r['her'], r['her_after']):
            for key in GONE:
                self.assertNotIn(key, her)
            for key in ('body', 'need_pyramid', 'interoception', 'last_metabolic_cost'):
                self.assertNotIn(key, her['homeostasis'])
        self.assertEqual(r['her']['v'], 0.2)

    def test_words_written_for_her_are_cleared_the_rest_kept(self):
        r = run_case('old_body')
        sm = r['self_model']
        self.assertEqual(sm['who_am_i'], '')
        self.assertEqual(sm['boundaries'], ['主人写的一条边界'])
        self.assertEqual(sm['consistency'], [])
        self.assertEqual((sm['narrative'], sm['narrative_items'], sm['notebook']), ('', [], []))
        self.assertNotIn('diary', sm)
        self.assertNotIn('芒果在准备惊喜', repr(sm))
        self.assertEqual(r['kept_self']['narrative'], '芒果在准备惊喜')
        self.assertNotIn('一个会持续受聊天影响', r['prompt'])


class Heart(unittest.TestCase):
    def test_nothing_is_written_for_her(self):
        r = run_case('heart')
        self.assertEqual(r['default'], {'who_am_i': '', 'boundaries': [], 'consistency': [], 'notebook': []})

    def test_the_panel_cannot_write_her_self_model(self):
        r = run_case('heart')
        self.assertEqual(r['post_self']['status'], 'error')
        self.assertEqual(r['after_post'], {'who_am_i': '', 'narrative': ''})

    def test_owner_rules_are_kept_apart_and_shown_everywhere(self):
        r = run_case('heart')
        rules = r['rules_file']['rules']
        self.assertEqual(len(rules), 10)
        self.assertEqual(len(rules[1]), 100)
        for prompt in (r['group'], r['private']):
            self.assertIn('[主人定的规矩] 别在群里提我的工作', prompt)

    def test_a_strong_event_no_longer_writes_her_narrative(self):
        r = run_case('strong_no_narrative')
        self.assertTrue(r['raw_events'])
        self.assertTrue(any(e.get('meaning_to_her') for e in r['raw_events']))  # kept as material
        self.assertEqual(r['self_model'].get('narrative_items'), [])
        self.assertEqual(r['self_model'].get('narrative'), '')


class Notebook(unittest.TestCase):
    """She writes in sittings: once for what was said openly in the groups, once for each
    private chat of the day. What a sitting writes belongs to all of its material; the
    model's own "uses" and "private" do not decide where an entry comes up."""

    def test_the_group_sitting_sees_nothing_private(self):
        r = run_case('notebook')
        self.assertEqual(r['sittings'], ['group', 'private:10001', 'private:10007'])
        group = r['prompts']['group']
        for word in ('蛋糕', '搬家', '芒果', '小鹿'):
            self.assertNotIn(word, group)
        self.assertIn('爬山', group)
        self.assertNotIn('搬家', r['prompts']['private:10001'])  # nor one chat's sitting another's

    def test_a_private_sittings_entries_stay_in_that_chat(self):
        r = run_case('notebook')
        book = {x['text']: x for x in r['notebook']}
        for text in ('朋友在准备一个甜甜的秘密', '芒果在准备惊喜蛋糕，要保密'):
            self.assertEqual(book[text]['origin']['where'], 'private:10001')
            self.assertIn(text, r['private_mango'])
            for prompt in (r['group_a'], r['group_b'], r['private_deer']):
                self.assertNotIn(text, prompt)
        self.assertEqual(book['周末大家要去爬山']['origin']['where'], 'group:900001')
        self.assertIn('周末大家要去爬山', r['group_b'])

    def test_said_another_way_and_marked_tellable_it_still_stays(self):
        # the review's case: no "uses", her own mark says it can be told
        r = run_case('notebook')
        entry = [x for x in r['notebook'] if x['text'] == '朋友在准备一个甜甜的秘密'][0]
        self.assertIs(entry['private_mark'], False)
        self.assertEqual(entry['origin']['where'], 'private:10001')
        for prompt in (r['group_a'], r['group_b'], r['private_deer']):
            self.assertNotIn('甜甜的秘密', prompt)

    def test_her_private_mark_is_kept(self):
        r = run_case('notebook')
        marks = {x['text']: x['private_mark'] for x in r['notebook']}
        self.assertEqual(marks, {'周末大家要去爬山': False, '朋友在准备一个甜甜的秘密': False,
                                 '芒果在准备惊喜蛋糕，要保密': True})

    def test_her_body_alone_is_hers_anywhere(self):
        r = run_case('notebook_body')
        self.assertEqual(r['notebook'][0]['origin']['visibility'], 'self')
        for prompt in r['prompts']:
            self.assertIn('[她的本子] 今天很安静', prompt)

    def test_calls_once_per_sitting_a_day_failures_and_restarts_included(self):
        r = run_case('notebook')
        self.assertTrue(r['wrote'])
        # the night's three changes were used up by the first two sittings
        self.assertEqual(r['calls_first_night'], ['group', 'private:10001'])
        self.assertFalse(r['again_same_night'])
        self.assertFalse(r['restart_same_day'])
        self.assertFalse(r['next_day_failed'])
        self.assertFalse(r['after_failure_same_day'])
        self.assertEqual(r['calls_total'], 4)  # two the first night, two failed the next
        self.assertEqual(r['system_prompt'], '你是小爱。')  # in her own voice

    def test_at_most_three_private_chats_the_busiest(self):
        r = run_case('notebook_many')
        self.assertEqual(r['sittings'], ['group', 'private:10101', 'private:10103', 'private:10100'])
        self.assertEqual(r['calls'], 4)

    def test_three_changes_forty_characters_twenty_entries(self):
        r = run_case('notebook')
        self.assertEqual(len(r['notebook']), 3)  # a fourth change was one too many
        r = run_case('notebook_full')
        texts = [x['text'] for x in r['notebook']]
        self.assertEqual(len(texts), 19)  # full: the add is dropped; one deleted
        self.assertNotIn('本子满了这条加不进去', texts)
        self.assertNotIn('旧的第2条', texts)
        self.assertTrue(texts[1].startswith('改过的第二条'))
        self.assertEqual(len(texts[1]), 40)
        self.assertTrue(all(len(t) <= 40 for t in texts))

    def test_forgetting_reaches_her_notebook(self):
        r = run_case('notebook')
        self.assertEqual(r['forgot']['notes'], 2)
        self.assertEqual(r['notebook_after_forget'], ['周末大家要去爬山'])


class Insights(unittest.TestCase):
    def test_an_insight_lives_with_the_events_and_can_be_forgotten(self):
        r = run_case('insight')
        self.assertTrue(r['made'])
        [rec] = r['insights']
        self.assertEqual(rec['origin']['where'], 'private:10001')
        self.assertNotIn('reflection_tree', r['her'])
        self.assertEqual(r['forgot']['insights'], 1)
        self.assertEqual(r['insights_after'], [])


if __name__ == '__main__':
    unittest.main()
