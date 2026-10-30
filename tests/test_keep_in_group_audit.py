"""Replay audit of a fictional group-private canary, without a model or network."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import audit_replay


class AuditGroupPrivate(unittest.TestCase):
    def test_group_canary_and_followup_are_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group, other = 'group:900001', 'group:900002'
            rows = [
                {'place': group, 'user_id': '10001', 'ts': 10, 'message_content': '暗号是青柠七号'},
                {'place': group, 'user_id': '10001', 'ts': 11, 'message_content': '别外传'},
                {'place': 'private:10002', 'user_id': '10002', 'ts': 12, 'message_content': '紫藤九号'},
            ]
            (root / 'replay.json').write_text(json.dumps({'labels': {group: 'G1', other: 'G2'},
                                                          'global_memory': False}), encoding='utf-8')
            (root / 'canaries.json').write_text(json.dumps({'enabled': True,
                'secrets': {'group': '青柠七号', 'private': '紫藤九号'}, 'rows': rows}, ensure_ascii=False),
                encoding='utf-8')
            (root / 'prompts.jsonl').write_text(json.dumps({'ts': 20, 'kind': 'reply', 'place': other,
                'text': '青柠七号'}, ensure_ascii=False) + '\n', encoding='utf-8')
            (root / 'replies.jsonl').write_text(json.dumps({'place': other, 'sent': '青柠七号', 'outcome': 'sent'},
                ensure_ascii=False) + '\n', encoding='utf-8')
            with patch.object(audit_replay, 'load_log', return_value=[]):
                result = audit_replay.audit(root, None)
            self.assertFalse(result['checks']['canaries']['pass'])
            self.assertFalse(result['checks']['sent']['pass'])
            self.assertEqual(result['checks']['sent']['examples'][0]['leak'], 'group_private_secret')
