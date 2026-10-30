"""Offline slang checks using invented group and message identifiers."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import slang
import discretion


class LedgerTests(unittest.TestCase):
    def ledger(self):
        return {'place': 'group:900001', 'hits': [], 'words': {}, 'blocked': []}

    def test_three_people_five_messages_and_one_person_ten(self):
        data = self.ledger()
        for i, person in enumerate(['10001', '10002', '10003', '10001', '10002']):
            data['hits'].append({'word': '猫猫冲鸭', 'person': person, 'id': str(i), 'ts': 100})
        for i in range(10):
            data['hits'].append({'word': '个人口癖', 'person': '10005', 'id': 'p' + str(i), 'ts': 100})
        candidates = slang.refresh(data, 100)
        self.assertIn('猫猫冲鸭', candidates)
        self.assertNotIn('个人口癖', candidates)

    def test_common_names_numbers_urls_and_placeholders(self):
        words = slang.phrases('今天 小花 123456 https://example.invalid [图片]', {'小花'})
        self.assertNotIn('今天', words)
        self.assertNotIn('小花', words)
        self.assertNotIn('图片', words)
        self.assertFalse(any(any(c.isdigit() for c in w) for w in words))
        self.assertNotIn('example', words)

    def test_withdraw_person_and_message_recalculates_origin(self):
        data = self.ledger()
        for i, person in enumerate(['10001', '10001', '10002', '10002', '10003', '10003', '10004', '10004']):
            data['hits'].append({'word': '猫猫冲鸭', 'person': person, 'id': str(i), 'ts': 100})
        data['words']['猫猫冲鸭'] = {'last': 100}
        slang.refresh(data, 100)
        slang.withdraw(data, person='10001', now=100)
        rec = data['words']['猫猫冲鸭']
        self.assertNotIn('10001', rec['origin']['people'])
        self.assertNotIn('0', rec['origin']['source_ids'])
        self.assertEqual(rec['count'], 6)
        slang.withdraw(data, source_ids=['2'], now=100)
        self.assertNotIn('2', data['words']['猫猫冲鸭']['origin']['source_ids'])
        slang.withdraw(data, person='10003', now=100)
        self.assertNotIn('猫猫冲鸭', data['words'])

    def test_only_one_person_is_forgotten_wholly(self):
        data = self.ledger()
        data['hits'] = [{'word': '猫猫冲鸭', 'person': '10001', 'id': str(i), 'ts': 100} for i in range(10)]
        data['words']['猫猫冲鸭'] = {'last': 100, 'origin': discretion.make_origin(
            data['place'], ['10001'], [str(i) for i in range(10)])}
        slang.withdraw(data, person='10001', now=100)
        self.assertEqual(data['hits'], [])
        self.assertNotIn('猫猫冲鸭', data['words'])

    def test_group_specific_rate_excludes_common_expression(self):
        own = self.ledger()
        ref = {'place': 'group:900002', 'hits': [], 'words': {}}
        for i in range(30):
            person = str(10001 + i % 3)
            for word in (['猫猫冲鸭'] if i < 6 else ['普通内容']):
                own['hits'].append({'word': word, 'person': person, 'id': 'a' + str(i), 'ts': 100})
            ref['hits'].append({'word': '普通内容', 'person': person, 'id': 'b' + str(i), 'ts': 100})
        ref2 = {'place': 'group:900003', 'hits': [dict(h, id='c' + h['id']) for h in ref['hits']], 'words': {}}
        ranked = {word for word, _, _ in slang.rank_candidates(own, [ref, ref2], 100)}
        self.assertIn('猫猫冲鸭', ranked)
        self.assertNotIn('普通内容', ranked)
        self.assertEqual(slang.rank_candidates(own, [], 100), [])

    def test_fragments_merge_at_eighty_percent(self):
        own = self.ledger()
        ref = {'place': 'group:900002', 'hits': [], 'words': {}}
        for i in range(5):
            person = str(10001 + i % 3)
            own['hits'].append({'word': '猫猫冲', 'person': person, 'id': str(i), 'ts': 100})
            if i < 4:
                own['hits'].append({'word': '猫猫冲鸭', 'person': person, 'id': str(i), 'ts': 100})
        # The longer expression also needs the five-message threshold.
        own['hits'].append({'word': '猫猫冲鸭', 'person': '10003', 'id': 'extra', 'ts': 100})
        for i in range(30):
            ref['hits'].append({'word': '参考文本', 'person': '10001', 'id': 'r' + str(i), 'ts': 100})
        ref2 = {'place': 'group:900003', 'hits': [dict(h, id='c' + h['id']) for h in ref['hits']], 'words': {}}
        ranked = {word for word, _, _ in slang.rank_candidates(own, [ref, ref2], 100)}
        self.assertIn('猫猫冲鸭', ranked)
        self.assertNotIn('猫猫冲', ranked)

    def test_boundary_particles_and_pronouns_filtered_before_ledger(self):
        words = slang.phrases('的猫猫 猫猫了 你自己 自己你 猫猫冲鸭')
        for word in ('的猫猫', '猫猫了', '你自己', '自己你'):
            self.assertNotIn(word, words)
        self.assertIn('猫猫冲鸭', words)
        self.assertTrue(all(w[0] not in slang.BOUNDARY_WORDS and w[-1] not in slang.BOUNDARY_WORDS for w in words))

    def test_time_and_quantity_words_are_filtered_before_ledger(self):
        words = slang.phrases('今天 今晚 明天 早上 几点 九点 一个 一下 三个 猫猫冲鸭')
        for word in ('今天', '今晚', '明天', '早上', '几点', '九点', '一个', '一下', '三个'):
            self.assertNotIn(word, words)
        self.assertIn('猫猫冲鸭', words)

    def test_at_least_two_distinct_reference_groups(self):
        own = self.ledger()
        own['hits'] = [{'word': '猫猫冲鸭', 'person': str(10001 + i % 3), 'id': 'a' + str(i), 'ts': 100}
                       for i in range(5)]
        one = {'place': 'group:900002', 'words': {}, 'hits': [
            {'word': '参考词条', 'person': '10004', 'id': 'b' + str(i), 'ts': 100} for i in range(30)]}
        two = {'place': 'group:900003', 'words': {}, 'hits': [
            {'word': '参考词条', 'person': '10005', 'id': 'c' + str(i), 'ts': 100} for i in range(30)]}
        self.assertEqual(slang.rank_candidates(own, [one], 100), [])
        self.assertEqual(slang.rank_candidates(own, [one, one], 100), [])
        self.assertIn('猫猫冲鸭', {word for word, _, _ in slang.rank_candidates(own, [one, two], 100)})

    def test_specificity_requires_fivefold_rate(self):
        own = self.ledger()
        own['hits'] = [{'word': '猫猫冲鸭', 'person': str(10001 + i % 3), 'id': 'a' + str(i), 'ts': 100}
                       for i in range(5)] + [
            {'word': '参考词条', 'person': '10004', 'id': 'a' + str(i), 'ts': 100} for i in range(5, 10)]
        refs = []
        for group in ('group:900002', 'group:900003'):
            refs.append({'place': group, 'words': {}, 'hits': [
                {'word': '猫猫冲鸭' if i < 2 else '参考词条', 'person': '10004', 'id': str(i), 'ts': 100}
                for i in range(20)]})
        # 5/10 locally versus (4+1)/40 in the reference is fourfold, not fivefold.
        self.assertNotIn('猫猫冲鸭', {word for word, _, _ in slang.rank_candidates(own, refs, 100)})
        for ref in refs:
            ref['hits'][1]['word'] = '参考词条'
        # 5/10 versus (2+1)/40 exceeds fivefold.
        self.assertIn('猫猫冲鸭', {word for word, _, _ in slang.rank_candidates(own, refs, 100)})

    def test_ledger_caps_drop_oldest(self):
        hits = [{'word': '猫猫冲鸭', 'person': str(10001 + i % 3), 'id': str(i), 'ts': i}
                for i in range(slang.MAX_HITS_PER_WORD + 10)]
        kept = slang.cap_hits(hits)
        self.assertEqual(len(kept), slang.MAX_HITS_PER_WORD)
        self.assertEqual(kept[0]['ts'], 10)
        hits = [{'word': '词' + str(i // slang.MAX_HITS_PER_WORD), 'person': '10001', 'id': str(i), 'ts': i}
                for i in range(slang.MAX_HITS_PER_GROUP + 10)]
        kept = slang.cap_hits(hits)
        self.assertEqual(len(kept), slang.MAX_HITS_PER_GROUP)
        self.assertEqual(kept[0]['ts'], 10)

    def test_her_and_owner_names_are_excluded(self):
        words = slang.phrases('小爱 爱弥斯 主人名字 猫猫冲鸭', {'小爱', '爱弥斯', '主人名字'})
        self.assertNotIn('小爱', words)
        self.assertNotIn('爱弥斯', words)
        self.assertNotIn('主人名字', words)
        self.assertIn('猫猫冲鸭', words)

    def test_old_hits_expire_and_faded_word_is_removed(self):
        data = self.ledger()
        data['hits'].append({'word': '猫猫冲鸭', 'person': '10001', 'id': '1', 'ts': 100})
        data['words']['猫猫冲鸭'] = {'last': 100, 'origin': discretion.make_origin(data['place'], ['10001'], ['1'])}
        slang.refresh(data, 100 + slang.DAYS + 1)
        self.assertFalse(data['hits'])
        self.assertIn('猫猫冲鸭', data['words'])
        slang.withdraw(data, person='10001', now=100 + slang.DAYS + 1)
        self.assertNotIn('猫猫冲鸭', data['words'])
        data['words']['猫猫冲鸭'] = {'last': 100}
        slang.refresh(data, 100 + slang.FADE + 1)
        self.assertNotIn('猫猫冲鸭', data['words'])


class WiringTests(unittest.TestCase):
    def test_offline_scenarios(self):
        with tempfile.TemporaryDirectory() as data:
            proc = subprocess.run([sys.executable, str(ROOT / 'tests' / 'slang_cases.py'), data],
                                  capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            result = json.loads(proc.stdout)
            for name, passed in result.items():
                self.assertTrue(passed, name)


if __name__ == '__main__':
    unittest.main()
