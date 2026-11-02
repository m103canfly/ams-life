# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The trust in a person follows what she felt while hearing that person.

The step under test is `_touch_user` with the reaction `_prepare_turn` reads off the core
right after `core.observe`: the impulse this one sentence itself made (`core.last_impulse`,
{'v': ...}), not the difference in v/stress before and after. This person's record is
kept in a dict, so no test data is written and nothing of hers is touched.
"""
import json
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import body  # noqa: E402
import memory_meta  # noqa: E402
import mixin_people  # noqa: E402


class _Record:
    """One person's JSON file, kept in a dict instead of on disk."""

    def __init__(self, doc):
        self.doc = doc

    def exists(self):
        return bool(self.doc)

    def read_text(self, encoding='utf-8'):
        return json.dumps(self.doc)

    def write_text(self, text, encoding='utf-8'):
        self.doc.clear()
        self.doc.update(json.loads(text))


class _Dir:
    def mkdir(self, parents=False, exist_ok=False):
        return None


class _Event:
    def __init__(self, sender, name='阿橙'):
        self.sender, self.name = sender, name


class FakeCore:
    """Only the numbers the trust step reads; nothing else of her is simulated."""

    def __init__(self, social=0.5, stress=0.5, bio_learning=False):
        self.social, self.stress = social, stress
        self.bio_learning = bio_learning

    def integrate_noise(self, kind, **kwargs):
        return None


class FakePlugin(mixin_people.PeopleMixin):
    """`_touch_user` alone, with each person's record in memory."""

    we_memory_enabled = False

    def __init__(self):
        self.records = {}

    def _speaker(self, event):
        return event.sender, event.name

    def _user_path(self, event):
        return _Record(self.records.setdefault(event.sender, {}))

    def _here(self, event):
        return ''

    def _load_memory(self, event):
        return {'entries': []}

    def _event_archive(self, limit):
        return []

    def _visible_events(self, events, archive):
        return []

    def _job_stale(self):
        return False


class TrustFollowsHerTests(unittest.TestCase):
    def setUp(self):
        item = patch.object(mixin_people, 'USER_DIR', _Dir())
        item.start()
        self.addCleanup(item.stop)
        self.plugin = FakePlugin()

    def touch(self, sender='10001', core=None, reaction=None):
        return self.plugin._touch_user(_Event(sender), core or FakeCore(), reaction=reaction)

    def trust_of(self, sender):
        return self.plugin.records.get(sender, {}).get('trust')

    def set_trust(self, sender, value):
        self.plugin.records[sender] = {'trust': value}

    def test_1_a_line_that_lifts_her_raises_this_persons_trust(self):
        self.set_trust('10001', 0.5)
        self.touch(reaction={'v': 0.20, 'stress': -0.02})
        self.assertGreater(self.trust_of('10001'), 0.5)

    def test_2_a_line_that_sinks_her_lowers_this_persons_trust(self):
        self.set_trust('10001', 0.5)
        self.touch(reaction={'v': -0.20, 'stress': 0.15})
        self.assertLess(self.trust_of('10001'), 0.5)

    def test_3_ordinary_sentences_leave_the_trust_where_it_was(self):
        # the old behaviour pulled it 30% of the way to 0.5 every time, which 20 ordinary
        # sentences would have moved a long way
        self.set_trust('10001', 0.38)
        self.touch(reaction={'v': 0.02, 'stress': 0.0})
        self.assertEqual(self.trust_of('10001'), 0.38)
        for _ in range(20):
            self.touch(reaction={'v': 0.01, 'stress': 0.0})
        self.assertEqual(self.trust_of('10001'), 0.38)

    def test_4_trust_stays_between_the_two_limits(self):
        self.set_trust('10001', 0.9)
        self.touch('10001', reaction={'v': 0.40, 'stress': 0.0})
        self.assertLessEqual(self.trust_of('10001'), mixin_people.TRUST_MAX)
        self.set_trust('10002', 0.1)
        self.touch('10002', reaction={'v': -0.40, 'stress': 0.30})
        self.assertGreaterEqual(self.trust_of('10002'), mixin_people.TRUST_MIN)

    def test_5_the_same_good_words_lift_a_low_trust_more_than_a_high_one(self):
        self.set_trust('10001', 0.9)
        self.set_trust('10002', 0.2)
        for sender in ('10001', '10002'):
            self.touch(sender, reaction={'v': 0.20, 'stress': 0.0})
        self.assertGreater(self.trust_of('10002') - 0.2, self.trust_of('10001') - 0.9)

    def test_6_no_reaction_leaves_the_trust_alone(self):
        # e.g. a picture with no words: there was nothing for observe() to answer
        self.set_trust('10001', 0.31)
        self.touch(reaction=None)
        self.assertEqual(self.trust_of('10001'), 0.31)

    def test_7_closeness_follows_the_trust(self):
        core = FakeCore(social=0.5, stress=0.5)
        self.set_trust('10001', 0.5)
        before = self.touch('10001', core=core, reaction=None)
        before = before['relationship']['state']['closeness']
        after = self.touch('10001', core=core, reaction={'v': 0.25, 'stress': 0.0})
        after = after['relationship']['state']['closeness']
        self.assertGreater(self.trust_of('10001'), 0.5)
        self.assertGreater(after, before)

    def test_8_bio_learning_uses_nassar_alpha(self):
        seen = []
        real = memory_meta.nassar_alpha

        def recorded(evidence):
            seen.append(evidence)
            return real(evidence)

        self.set_trust('10001', 0.5)
        with patch.object(mixin_people.memory_meta, 'nassar_alpha', recorded):
            self.touch(core=FakeCore(bio_learning=True), reaction={'v': 0.25, 'stress': 0.0})
        self.assertEqual(len(seen), 1)
        self.assertAlmostEqual(seen[0], 1.0, places=3)
        # the rate it gave is the one taken in: 0.31 of the room above 0.5
        self.assertAlmostEqual(self.trust_of('10001'), 0.655, places=3)

    def test_9_each_persons_trust_follows_her_reaction_to_that_person(self):
        self.set_trust('10001', 0.5)
        self.set_trust('10002', 0.5)
        self.touch('10001', reaction={'v': 0.25, 'stress': 0.0})
        self.touch('10002', reaction={'v': -0.25, 'stress': 0.20})
        self.assertGreater(self.trust_of('10001'), 0.5)
        self.assertLess(self.trust_of('10002'), 0.5)

    def react(self, text, v=0.0, hours_ago=0.0):
        """The real observe() on a fresh core in this mood; its impulse is the reaction."""
        core = body.BioCore()
        core.v = v
        core.last_tick = time.time() - float(hours_ago) * 3600.0
        core.observe(text)
        return core, core.last_impulse

    def test_10_an_ordinary_line_moves_no_trust_whatever_her_mood(self):
        # the old difference before/after read the hours of decay and the pull back to her
        # baseline as her reaction: at v=0.8 a plain line read as dv=-0.36 after half an
        # hour, still dv=-0.23 right after _decay_to_now(); two hours is further off still
        for v in (0.8, -0.6):
            core, reaction = self.react('今天天气还行', v=v, hours_ago=2)
            self.assertIsNone(reaction)
            self.set_trust('10001', 0.5)
            self.touch('10001', core=core, reaction=reaction)
            self.assertEqual(self.trust_of('10001'), 0.5)

    def test_11_the_same_good_words_lift_trust_at_either_mood(self):
        gains = {}
        for v in (0.8, -0.6):
            core, reaction = self.react('谢谢你，你真好，最喜欢你了', v=v, hours_ago=2)
            self.assertIsNotNone(reaction)
            self.assertGreater(reaction['v'], 0)
            self.set_trust('10001', 0.5)
            self.touch('10001', core=core, reaction=reaction)
            gains[v] = self.trust_of('10001') - 0.5
        self.assertGreater(gains[0.8], 0)
        self.assertGreater(gains[-0.6], 0)
        self.assertAlmostEqual(gains[0.8], gains[-0.6], places=3)

    def test_12_the_same_bad_words_sink_trust_at_either_mood(self):
        for v in (0.8, -0.6):
            core, reaction = self.react('你真讨厌，快滚', v=v, hours_ago=2)
            self.assertIsNotNone(reaction)
            self.assertLess(reaction['v'], 0)
            self.set_trust('10001', 0.5)
            self.touch('10001', core=core, reaction=reaction)
            self.assertLess(self.trust_of('10001'), 0.5)

    def test_13_the_impulse_is_not_saved_with_her_state(self):
        core, reaction = self.react('谢谢你，你真好，最喜欢你了', v=0.2)
        self.assertIsNotNone(reaction)
        saved = core.snapshot()
        self.assertNotIn('last_impulse', saved)
        self.assertNotIn('last_impulse', json.dumps(saved, ensure_ascii=False))
        # a state file that carried one would not restore it either
        fresh = body.BioCore()
        fresh.load_state(dict(saved, last_impulse={'v': 0.9}))
        self.assertIsNone(fresh.last_impulse)


if __name__ == '__main__':
    unittest.main()
