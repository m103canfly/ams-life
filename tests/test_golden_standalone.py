# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Compare the standalone trace with the AstrBot golden traces."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from golden_script import SCRIPT  # noqa: E402

MISSING = object()

# Each row is a path pattern, category and reason. Stars match one list index only.
GOLDEN_A = [
    ('$["asked_uncalled"]', 'self-decision', 'A records uncalled model requests.'),
    ('$["sent"]', 'wiring', 'The golden trace does not record sends.'),
    ('$["files"]["states/attention.json"]["private:10001"]', 'self-decision', 'A records attention state.'),
]
for index in range(24):
    GOLDEN_A.append((f'$["turns"][{index}]["inject"][0]', 'self-decision',
                     'A adds the self-decision guidance and retains addressed text.'))
for field in ('hard', 'left', 'level', 'soft', 'spent', 'state'):
    GOLDEN_A.append((f'$["page_status"]["data"]["spend"]["{field}"]', 'self-decision',
                     'A exposes the self-decision spending state.'))
for field in ('calls', 'event_summary', 'reply'):
    GOLDEN_A.append((f'$["files"]["states/spend.json"]["2026-10-31"]["{field}"]', 'self-decision',
                     'A counts model calls when self-decision is enabled.'))
for person, days in (('10001', ('20752', '20753', '20755')), ('10002', ('20752', '20753', '20755')),
                     ('10003', ('20752', '20755')), ('10004', ('20752', '20755')),
                     ('10005', ('20753',)), ('10006', ())):
    root = f'$["files"]["states/ties.json"]["{person}"]'
    for day in days:
        GOLDEN_A.append((root + f'["calls"]["{day}"]', 'self-decision', 'A records calls by day.'))
    if not days:
        GOLDEN_A.append((root + '["calls"]', 'self-decision', 'A records the empty call history.'))
    for field in ('last', 'private'):
        GOLDEN_A.append((root + f'["{field}"]', 'self-decision', 'A records familiarity with this person.'))
    day_count = {'10001': 3, '10002': 3, '10003': 2, '10004': 2, '10005': 2, '10006': 1}[person]
    for index in range(day_count):
        GOLDEN_A.append((root + f'["days"][{index}]', 'self-decision', 'A records days seen.'))

PHONE_FILES = ('phone/group_900001-e7c9f21c4c9d.json', 'phone/group_900002-d817415687ae.json',
               'phone/private_10001-fd9c6576bc5b.json')
for name, indexes in zip(PHONE_FILES, ((0, 2, 4, 6, 8), (0, 2), (0, 2, 4, 6, 8))):
    for index in indexes:
        GOLDEN_A.append((f'$["files"]["{name}"]["recent"][{index}]["text"]', 'wiring',
                         'A now includes the addressed At segment in the phone text.'))

FULL_ONLY = [('$["provider_prompts"][24]', 'wiring', 'Addressed phone text can change event prompts.'),
             ('$["provider_prompts"][26]', 'wiring', 'Addressed phone text can change event prompts.')]
for field in ('persona_compile', 'tom_probe'):
    FULL_ONLY.append((f'$["files"]["states/spend.json"]["2026-10-31"]["{field}"]', 'self-decision',
                      'A counts this enabled model function.'))

# These event fields are provisional until the post-At trace is produced.
EVENT_FIELDS = ('event', 'big_summary', 'small_summary', 'title', 'event_key', 'source_texts')
for name in ('archives/events.jsonl', 'archives/sessions/group_900001/events.jsonl',
             'archives/sessions/private_10001/events.jsonl'):
    for field in EVENT_FIELDS:
        suffix = '[*]' if field == 'source_texts' else ''
        FULL_ONLY.append((f'$["files"]["{name}"][*]["{field}"]{suffix}', 'wiring',
                         'The addressed phone text can change event summaries.'))
for field in EVENT_FIELDS:
    suffix = '[*]' if field == 'source_texts' else ''
    FULL_ONLY.append((f'$["page_status"]["data"]["events"][*]["{field}"]{suffix}', 'wiring',
                     'The panel exposes events derived from the addressed phone text.'))

A_B0 = [('$["files"]["states/spend.json"]["2026-10-31"]["calls"]', 'wiring', 'The two model routes count calls differently.')]
for index in range(24):
    A_B0.extend([(f'$["turns"][{index}]["session"]', 'wiring', 'AstrBot sessions and neutral places differ.'),
                 (f'$["sent"][{index}][0]', 'wiring', 'The standalone messenger records the destination.'),
                 (f'$["sent"][{index}][1][0]["type"]', 'wiring', 'The standalone messenger records the segment type.'),
                 (f'$["sent"][{index}][1][0]["data"]["text"]', 'wiring', 'The standalone messenger records segment text.')])
for name in PHONE_FILES:
    A_B0.append((f'$["files"]["{name}"]["umo"]', 'wiring', 'Only AstrBot keeps its session string.'))
for field in ('api_key', 'base_url', 'model', 'source'):
    A_B0.append((f'$["files"]["api_config.json"]["embedding"]["{field}"]', 'wiring',
                 'Standalone supplies the fake embedding provider in its config.'))
for field in ('enabled', 'provider_id', 'source'):
    A_B0.append((f'$["page_status"]["data"]["api_config"]["embedding"]["{field}"]', 'wiring',
                 'The panel reports the selected embedding source.'))
for field in ('base_url', 'has_key', 'model', 'provider_id'):
    A_B0.append((f'$["page_status"]["data"]["astrbot_embedding"]["{field}"]', 'wiring',
                 'Only AstrBot exposes its embedding provider.'))
for field in ('id', 'model', 'type'):
    A_B0.append((f'$["page_status"]["data"]["llm_providers"][0]["{field}"]', 'wiring',
                 'Only AstrBot exposes its chat provider.'))
for index in range(24):
    A_B0.append((f'$["log"][{index}][1]', 'wiring',
                 'AstrBot reports unavailable phone tools; standalone reports its missing speech-provider context.'))
for field in (0, 1):
    A_B0.append((f'$["log"][24][{field}]', 'wiring', 'Standalone has no AstrBot knowledge-base manager.'))

B0_B = [(f'$["files"]["history.sqlite3"]["history"][{index}][{column}]', 'history',
         'Only standalone with history creates this conversation database.') for index in range(48) for column in range(10)]



def differences(want, got, path='$'):
    """Compare dictionaries by key and lists by position down to their leaves."""
    if isinstance(want, dict) and isinstance(got, dict):
        for key in sorted(want.keys() | got.keys()):
            yield from differences(want.get(key, MISSING), got.get(key, MISSING),
                                   path + '[' + json.dumps(key, ensure_ascii=False) + ']')
    elif isinstance(want, list) and isinstance(got, list):
        for index in range(max(len(want), len(got))):
            yield from differences(want[index] if index < len(want) else MISSING,
                                   got[index] if index < len(got) else MISSING, path + f'[{index}]')
    elif want is MISSING and isinstance(got, (dict, list)) and got:
        yield from differences({} if isinstance(got, dict) else [], got, path)
    elif got is MISSING and isinstance(want, (dict, list)) and want:
        yield from differences(want, {} if isinstance(want, dict) else [], path)
    elif want != got or type(want) is not type(got):
        yield path, want, got


def run_scenario(mode, path='standalone'):
    with tempfile.TemporaryDirectory() as tmp:
        data, out = Path(tmp) / 'data', Path(tmp) / 'trace.json'
        data.mkdir()
        env = dict(os.environ, PYTHONHASHSEED='0')
        env.pop('AMS_LIFE_DATA_DIR', None)
        proc = subprocess.run([sys.executable, str(HERE / 'scenario_standalone.py'), str(data), str(out), mode,
                               '--path', path],
                              env=env, capture_output=True, text=True, timeout=300)
        if proc.returncode:
            raise AssertionError(f'scenario {mode} failed:\n{proc.stdout}\n{proc.stderr}')
        return json.loads(out.read_text('utf-8'))


def compare(mode):
    want = json.loads((HERE / 'golden' / f'{mode}.json').read_text('utf-8'))
    got = run_scenario(mode)
    return got, list(differences(want, got))


def matches(pattern, path):
    return re.fullmatch(re.escape(pattern).replace(r'\*', r'\d+'), path) is not None


class GoldenStandalone(unittest.TestCase):
    def check(self, mode):
        golden = json.loads((HERE / 'golden' / f'{mode}.json').read_text('utf-8'))
        a = run_scenario(mode, 'astrbot')
        b0 = run_scenario(mode, 'nohistory')
        b = run_scenario(mode, 'standalone')
        tables = (('golden -> A', golden, a, GOLDEN_A + (FULL_ONLY if mode == 'full' else [])),
                  ('A -> B0', a, b0, A_B0), ('B0 -> B', b0, b, B0_B))
        problems = []
        for stage, left, right, allowed in tables:
            found = list(differences(left, right))
            paths = {item[0] for item in found}
            extra = sorted(path for path in paths if not any(matches(row[0], path) for row in allowed))
            missing = sorted(row[0] for row in allowed if not any(matches(row[0], path) for path in paths))
            if extra or missing:
                problems.append(f'{stage}: extra paths: {extra}\nmissing paths: {missing}')
        # The approved log paths are limited to these messages, not arbitrary warnings.
        phone = '[ams-life] phone tools unavailable'
        voice = "[biocore] voice context failed: 'RouteCollector' object has no attribute 'get_using_stt_provider_async'"
        for index in range(24):
            if (a['log'][index] if index < len(a['log']) else None) != ['warning', phone] or \
                    (b0['log'][index] if index < len(b0['log']) else None) != ['warning', voice]:
                problems.append(f'A -> B0: unexpected log entry at index {index}')
        kb = "[biocore] kb list failed: 'RouteCollector' object has no attribute 'kb_manager'"
        if len(a['log']) != 24 or len(b0['log']) != 25 or b0['log'][24] != ['warning', kb]:
            problems.append('A -> B0: unexpected knowledge-base warning or log length')
        self.assertFalse(problems, '\n'.join(problems))

    def test_basic(self):
        self.check('basic')

    def test_full(self):
        self.check('full')


class AstrBotScenario(unittest.TestCase):
    def check_shape(self, mode):
        got = run_scenario(mode, 'astrbot')
        golden = json.loads((HERE / 'golden' / f'{mode}.json').read_text('utf-8'))
        self.assertEqual(set(got), set(golden) | {'sent', 'asked_uncalled'})
        self.assertEqual(got['routes'], golden['routes'])
        self.assertTrue(got['turns'])
        for item in got['turns']:
            self.assertEqual(set(item), {'session', 'inject', 'system', 'clean'})

    def test_basic(self):
        self.check_shape('basic')

    def test_full(self):
        self.check_shape('full')


def render(value):
    if value is MISSING:
        return '<missing>'
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return text if len(text) <= 200 else text[:200] + '…'


def classify(stage, path, want, got):
    values = str(want) + str(got)
    if stage == 'A → B0' and 'voice context failed' in values and 'get_using_stt_provider_async' in values:
        return '接线', 'mixin_media.py:270-275 handles the missing AstrBot speech provider and uses the QQ path below.'
    if stage == 'A → B0' and path.endswith('["session"]'):
        return '接线', 'scenario_standalone.py uses the AstrBot session in A and her._here(event) in B0; mixin_memory.py:260-261 returns the place.'
    if stage == 'A → B0' and path.startswith('$["sent"]'):
        return '接线', 'turn_runner.py:81 sends through the standalone messenger; the AstrBot harness does not simulate platform delivery.'
    if stage == 'B0 → B' and path.startswith('$["files"]["history.sqlite3"]'):
        return '对话历史', 'scenario_standalone.py creates a HistoryStore only for B.'
    if stage == '金样 → A' and path.startswith(('$["asked_uncalled"]', '$["files"]["states/attention.json"]')):
        return '自己判断', 'A enables self_decide and records its decisions.'
    return '查不清', 'The trace differs; the responsible source line and cause still need investigation.'


def group_of(path):
    parts = re.findall(r'\[(?:"(?:[^"\\]|\\.)*"|\d+)\]', path)
    return '$' + ''.join(parts[:2])


def report(path):
    lines = ['## Appendix: difference report', '',
             'List positions are compared directly; missing turns can shift later positions.',
             'AstrBot sends are not simulated by the harness; its sent list is empty.', '']
    for mode in ('basic', 'full'):
        golden = json.loads((HERE / 'golden' / f'{mode}.json').read_text('utf-8'))
        a = run_scenario(mode, 'astrbot')
        b0 = run_scenario(mode, 'nohistory')
        b = run_scenario(mode, 'standalone')
        lines.extend([f'### {mode}', '',
                      f'Called turns expected: {sum(reply is not None for _, _, reply in SCRIPT)}; '
                      f'A/B0/B recorded: {len(a["turns"])}/{len(b0["turns"])}/{len(b["turns"])}. '
                      f'asked_uncalled (zero-based): A {a["asked_uncalled"]}, '
                      f'B0 {b0["asked_uncalled"]}, B {b["asked_uncalled"]}.', ''])
        for stage, left, right in (('金样 → A', golden, a), ('A → B0', a, b0), ('B0 → B', b0, b)):
            found = list(differences(left, right))
            table = (GOLDEN_A + (FULL_ONLY if mode == 'full' else []) if stage == '金样 → A'
                     else A_B0 if stage == 'A → B0' else B0_B)
            counts = Counter(group_of(location) for location, _, _ in found)
            groups = ', '.join(f'{key}: {count}' for key, count in sorted(counts.items())) or 'none'
            lines.extend([f'#### {stage}', '', f'{len(found)} differing paths. Groups: {groups}.', ''])
            lines.extend(f'- Allowed `{pattern}` | {category} | {why}' for pattern, category, why in table)
            lines.append('')
            for location, want, actual in found:
                kind, why = classify(stage, location, want, actual)
                lines.append(f'- `{location}` | {kind} | left: {render(want)} | right: {render(actual)} | {why}')
            lines.append('')
    target = Path(path)
    prefix = ''
    if target.exists():
        previous = target.read_text('utf-8')
        marker = '## Appendix: difference report'
        if marker in previous:
            prefix = previous.split(marker, 1)[0].rstrip() + '\n\n'
    target.write_text(prefix + '\n'.join(lines).rstrip() + '\n', 'utf-8')


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--report':
        report(sys.argv[2])
    else:
        unittest.main()
