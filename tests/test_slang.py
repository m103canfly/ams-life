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

