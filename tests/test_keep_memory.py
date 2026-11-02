# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""No memory is ever cut for room; the hot/cold tier is worked out again on every recall;
and memories that fell out of the library can be put back from a copy of her data folder.

Every case runs in a fresh interpreter on a made-up data folder (this file, run with
`_case`), so the module-level paths point at a temporary folder. All names, numbers and
memories are made up; no network, no model, no real data.

Case scripts also serve as the `_case` runner of this same file, so there is one test file:
    python -m unittest tests.test_keep_memory
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_CACHE = {}


def run_case(case):
    """Run one case in a fresh interpreter; the result is its JSON."""
    if case not in _CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            data, out = Path(tmp) / 'data', Path(tmp) / 'out.json'
            data.mkdir()
            env = dict(os.environ, PYTHONHASHSEED='0')
            env.pop('AMS_LIFE_DATA_DIR', None)
            proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), '_case', case,
                                   str(data), str(out)],
                                  env=env, capture_output=True, text=True, encoding='utf-8',
                                  timeout=900)
            if proc.returncode != 0:
                raise AssertionError('case %s failed:\n%s\n%s' % (case, proc.stdout, proc.stderr))
            _CACHE[case] = json.loads(out.read_text('utf-8'))
    return _CACHE[case]


# ---------------------------------------------------------------------------
# One case, run by the spawned interpreter
# ---------------------------------------------------------------------------
def run_script(case, data, out):
    import asyncio
    import contextlib
    import io
    import math
    import time

    import harness
    clock = harness.prepare(data)
    G1 = '900001'
    now = clock.now

    def vec(text):
        return harness.fake_vector(text)

    def entry(eid, text, *, ts=None, importance=0.5, hits=1, tier='hot', people=('10002',),
              with_vector=True, vector=None):
        item = {'id': eid, 'text': text, 'role': 'user',
                'ts': now if ts is None else float(ts), 'hits': int(hits),
                'importance': float(importance),
                'last_used': now if ts is None else float(ts),
                'sender_id': people[0] if people else '',
                'sender_name': '柠檬',
                'provenance': {'sender_id': people[0] if people else '', 'sender_name': '柠檬',
                               'session': 'group:' + G1, 'ts': now, 'message_refs': []},
                'origin': {'where': 'group:' + G1, 'people': list(people), 'source_ids': [],
                           'visibility': 'public'},
                'memory_source': 'direct', 'memory_confidence': 0.7,
                'memory_tier': tier, 'conflict': False, 'inhibition': 0.0,
                'suppression_count': 0}
        if with_vector:
            item['vector'] = list(vector) if vector is not None else vec(text)
        return item

    def write_json(rel, obj):
        path = Path(data) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding='utf-8')

    def library():
        return json.loads((Path(data) / 'memory' / 'library.json').read_text('utf-8'))

    def memory_tree():
        root = Path(data) / 'memory'
        return {p.relative_to(root).as_posix(): p.read_bytes()
                for p in sorted(root.rglob('*')) if p.is_file()}

    def write_backup(name, entries, vectors=None):
        """A fake copy of her data folder: library.json plus, unless given, its vectors."""
        import vector_store
        folder = Path(data).parent / 'backups' / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'library.json').write_text(
            json.dumps({'schema_version': 2, 'rooms': {}, 'entries': entries}, ensure_ascii=False),
            encoding='utf-8')
        if vectors is None:
            vectors = {e['id']: vec(e['text']) for e in entries}
        store = vector_store.VectorStore(folder / vector_store.FILE_NAME)
        try:
            store.put_many(vectors)
        finally:
            store.close()
        return folder

    result = {}

    # ---------------------------------------------------------------- data written before the plugin starts
    base = '山坡上的日出很好看'
    if case == 'tiers':
        # One shared vector, and a query vector at a worked-out cosine to it (0.7): high
        # enough to be a candidate, low enough never to read as the same memory. So the
        # test is about the tiers, not about how close two sentences happen to be.
        v = harness.fake_vector('共用的方向')
        u = harness.fake_vector('另外一个方向')
        _dot = sum(a * b for a, b in zip(u, v))
        perp = [b - _dot * a for a, b in zip(v, u)]
        _n = math.sqrt(sum(x * x for x in perp)) or 1.0
        perp = [x / _n for x in perp]
        cos, sin = 0.7, math.sqrt(1.0 - 0.49)
        query = '你还记得那天的日出吗'
        query_vec = [cos * a + sin * b for a, b in zip(v, perp)]
        rows = []
        for i in (1, 2):
            rows.append(entry('w%d' % i, base + '第%d次说起这件事' % i, ts=now - 3600,
                              importance=0.6, vector=v))
        for i in (1, 2, 3, 4):
            rows.append(entry('c%d' % i, base + '第%d次说起这件事' % i, ts=now - 30 * 86400,
                              importance=0.3, hits=0, vector=v))
        rows.append(entry('high', base + '第9次说起这件事', ts=now - 30 * 86400, importance=0.8,
                          hits=0, vector=v))
        summarized = entry('sum', base + '第7次说起这件事', ts=now - 3600, importance=0.6, vector=v)
        summarized['summarized'] = True
        summarized['summary_id'] = 'sum_x'
        rows.append(summarized)
        write_json('memory/library.json', {'schema_version': 2, 'rooms': {}, 'entries': rows})
    if case == 'unusable':
        bad_one = entry('sys1', '[BioCore] 你正在扮演小爱', ts=now - 100, with_vector=False)
        bad_two = entry('sys2', '注意，你正在社交媒体上和人聊天', ts=now - 90, with_vector=False)
        write_json('memory/library.json', {'schema_version': 2, 'rooms': {}, 'entries': [
            entry('good', '今天阳光很好', ts=now - 200), bad_one, bad_two]})
    if case in ('restore_dry', 'restore_apply'):
        write_json('memory/library.json', {'schema_version': 2, 'rooms': {}, 'entries': [
            entry('have', '这是现在库里就有的一条', ts=now - 200)]})
    if case in ('restore_forget', 'restore_redline', 'restore_vectors'):
        write_json('memory/library.json', {'schema_version': 2, 'rooms': {}, 'entries': [
            entry('have', '这是现在库里就有的一条', ts=now - 200)]})
    if case == 'perf':
        write_json('memory/library.json', {'schema_version': 2, 'rooms': {}, 'entries': [
            entry('p%04d' % i, '记忆里的第%d件小事，说给你听' % i,
                  ts=now - 30 * 86400 + i, importance=0.6) for i in range(5000)]})

    import main
    config = {'redline_filter': True} if case == 'restore_redline' else {}
    ctx = harness.FakeContext()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    plugin = main.BioCorePlugin(ctx, config=config)
    plugin._ipv4_json = harness.fake_ipv4_json
    event = harness.FakeEvent('小爱 今天在干嘛', sender='10002', name='柠檬', group=G1)

    # ---------------------------------------------------------------- 1/2: nothing is cut for room
    if case in ('keep120', 'keep250'):
        number = 120 if case == 'keep120' else 250
        if case == 'keep250':
            plugin.api_config = {'compression': {'enabled': True, 'threshold': 6000}}
        doc = plugin._load_memory(event)
        for i in range(number):
            doc['entries'].append(entry('k%04d' % i, '认识你的第%d天，天气很好' % i,
                                        ts=now - (number - i) * 60))
        plugin._trim_memory(doc)
        plugin._save_memory(event, doc)
        lib = library()
        store = plugin._vector_store()
        result = {'count': len(lib['entries']),
                  'stored': len(store.ids()),
                  'all_vectors': all(bool(store.get(e.get('id'))) for e in lib['entries']),
                  'in_json': sum(1 for e in lib['entries'] if e.get('vector'))}

    # ---------------------------------------------------------------- 3/4: the tier is worked out again
    if case == 'tiers':
        result['stored_before'] = {e['id']: e.get('memory_tier') for e in library()['entries']}
        import mixin_memory
        mixin_memory.RETRIEVAL_THRESHOLD = 0.0   # so an old memory is a candidate: the tiers, not the score, are on trial
        turn = {}
        loop.run_until_complete(plugin._memory_recall(event, query, vec=query_vec, turn=turn))
        lib = library()
        tiers = {e['id']: e.get('memory_tier') for e in lib['entries']}
        top = list(turn.get('memory_entries') or [])
        result['tiers'] = tiers
        result['top'] = top
        result['top_cold'] = [i for i in top if tiers.get(i) == 'cold']
        result['summarized'] = {e['id']: bool(e.get('summarized')) for e in lib['entries']
                                if e.get('id') == 'sum'}

    # ---------------------------------------------------------------- 5: what was set aside comes back
    if case == 'unusable':
        doc = plugin._load_memory(event)
        result['loaded'] = sorted(e['id'] for e in doc['entries'])
        result['aside'] = sorted(e['id'] for e in doc.get('_unusable_entries') or [])
        loop.run_until_complete(plugin._remember(event, '新记下来的一句话', 'user'))
        lib = library()
        result['after'] = sorted(e['id'] for e in lib['entries'])
        result['rooms_keys'] = sorted((lib.get('rooms') or {}).get('group:' + G1) or {})
        result['texts'] = {e['id']: e.get('text') for e in lib['entries'] if e.get('id') in ('sys1', 'sys2')}

    # ---------------------------------------------------------------- 6: deliberate deletes still delete
    if case == 'deletes':
        import forget_registry
        with forget_registry.ForgetRegistry(Path(data) / forget_registry.FILE_NAME) as reg:
            reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=now - 100, note='test')
        # written after the plugin is up, and after the person was registered
        write_json('memory/library.json', {'schema_version': 2, 'rooms': {}, 'entries': [
            entry('his', '他悄悄告诉我的事', ts=now - 5000, people=('10003',))]})
        plugin._known_memory_ids = None
        plugin._known_memory_texts = None
        loop.run_until_complete(plugin._remember(event, '新的一句话要记住', 'user'))
        result['after_forget'] = sorted(e.get('id') for e in library()['entries'])
        loop.run_until_complete(plugin._remember(event, '这句话要记两遍', 'user'))
        loop.run_until_complete(plugin._remember(event, '这句话要记两遍', 'user'))
        lib = library()
        same = [e for e in lib['entries'] if e.get('text') == '这句话要记两遍']
        result['merged'] = len(same)
        result['merged_hits'] = [int(e.get('hits', 0)) for e in same]
        # the owner's delete in the panel: it stays deleted after the next memory is stored
        target = same[0]['id'] if same else ''
        answer = loop.run_until_complete(plugin.page_memory_delete('library', target))
        loop.run_until_complete(plugin._remember(event, '面板删掉以后再记一条', 'user'))
        result['panel_status'] = answer.get('status')
        result['panel_gone'] = target not in {e.get('id') for e in library()['entries']}

    # ---------------------------------------------------------------- 7-11: the restore tool
    if case.startswith('restore_'):
        from tools import restore_memory
        if case == 'restore_dry':
            first = write_backup('backup-a', [
                entry('have', '这是现在库里就有的一条', ts=now - 200),
                entry('r1', '补回来的第一条', ts=now - 900, people=('10004',)),
                entry('r2', '补回来的第二条', ts=now - 800),
                entry('r3', '补回来的第三条', ts=now - 700)])
            second = write_backup('backup-b', [entry('have', '这是现在库里就有的一条', ts=now - 200)])
            before = memory_tree()
            text_out = io.StringIO()
            with contextlib.redirect_stdout(text_out):
                report = restore_memory.scan(plugin, [first, second])
                restore_memory.print_report(report)
            result = {'rows': [[r['restorable'], r['registry'], r['redline'], r['no_vector']]
                               for r in report['backups']],
                      'total': report['restorable'],
                      'unchanged': before == memory_tree(),
                      'out': text_out.getvalue(),
                      'library_rows': len(library()['entries'])}
        if case == 'restore_apply':
            backup_rows = [entry('r1', '补回来的第一条', ts=now - 900, people=('10004',)),
                           entry('r2', '补回来的第二条', ts=now - 800),
                           entry('r3', '补回来的第三条', ts=now - 700)]
            folder = write_backup('backup-a', backup_rows)
            before_json = json.loads((Path(data) / 'memory' / 'library.json').read_text('utf-8'))
            report = restore_memory.restore(plugin, [folder])
            lib = library()
            after = {e['id']: e for e in lib['entries'] if e.get('id') in ('r1', 'r2', 'r3')}
            store = plugin._vector_store()
            copy_dir = report.get('copy')
            result = {'written': report['written'],
                      'ids': sorted(after),
                      'ts_same': all(after[e['id']]['ts'] == e['ts'] for e in backup_rows),
                      'origin_same': all(after[e['id']]['origin'] == e['origin'] for e in backup_rows),
                      'provenance_same': all(after[e['id']]['provenance'] == e['provenance']
                                             for e in backup_rows),
                      'importance_same': all(after[e['id']]['importance'] == e['importance']
                                             for e in backup_rows),
                      'vectors': {e['id']: store.get(e['id']) == vec(e['text']) for e in backup_rows},
                      'copy_name': copy_dir.name if copy_dir is not None else '',
                      'copy_library_same': (json.loads((copy_dir / 'library.json').read_text('utf-8'))
                                            == before_json) if copy_dir is not None else False,
                      'copy_vectors': bool((copy_dir / 'vectors.sqlite3').is_file()) if copy_dir is not None else False,
                      'entries_before': len(before_json['entries'])}
        if case == 'restore_forget':
            import forget_registry
            with forget_registry.ForgetRegistry(Path(data) / forget_registry.FILE_NAME) as reg:
                reg.forget_person('10003', forget_registry.EVERYWHERE, stamp=now - 100, note='test')
            folder = write_backup('backup-a', [
                entry('gone', '他悄悄告诉我的事', ts=now - 5000, people=('10003',)),
                entry('keep', '另一个人说的话', ts=now - 400)])
            report = restore_memory.scan(plugin, [folder])
            applied = restore_memory.restore(plugin, [folder])
            ids_after = sorted(e.get('id') for e in library()['entries'])
            result = {'registry': report['registry'], 'restorable': report['restorable'],
                      'applied': applied['written'], 'ids_after': ids_after}
        if case == 'restore_redline':
            folder = write_backup('backup-a', [
                entry('bad', '我最近生病了，很难受', ts=now - 900),
                entry('ok', '周末一起去看展览吧', ts=now - 800)])
            report = restore_memory.scan(plugin, [folder])
            applied = restore_memory.restore(plugin, [folder])
            result = {'redline': report['redline'], 'restorable': report['restorable'],
                      'applied': applied['written'],
                      'ids_after': sorted(e.get('id') for e in library()['entries'])}
        if case == 'restore_vectors':
            plugin.api_config = {'embedding': {'source': 'custom', 'base_url': 'http://127.0.0.1:1/v1',
                                              'model': 'bge-m3'}}
            folder = write_backup('backup-a', [
                entry('m1', '向量维度对不上的一条', ts=now - 900, with_vector=False),
                entry('m2', '备份里没有向量的一条', ts=now - 800, with_vector=False)],
                vectors={'m1': [0.5, 0.5, 0.5]})
            report = restore_memory.scan(plugin, [folder])
            applied = restore_memory.restore(plugin, [folder])
            store = plugin._vector_store()

            async def no_vector(text, sensitive=False):
                return None
            plugin._embed_text = no_vector
            other = write_backup('backup-b', [
                entry('m3', '重算失败的一条', ts=now - 700, with_vector=False)],
                vectors={'m3': [0.25, 0.25, 0.25]})
            failed = restore_memory.scan(plugin, [other])
            failed_write = restore_memory.restore(plugin, [other])
            result = {'restorable': report['restorable'], 'recomputed': report['recomputed'],
                      'written': applied['written'],
                      'vectors': {eid: store.get(eid) == vec(text) for eid, text in
                                  (('m1', '向量维度对不上的一条'), ('m2', '备份里没有向量的一条'))},
                      'failed_no_vector': failed['no_vector'],
                      'failed_restorable': failed['restorable'],
                      'failed_written': failed_write['written'],
                      'ids_after': sorted(e.get('id') for e in library()['entries'])}

    # ---------------------------------------------------------------- 12: how long one recall takes at 5000
    if case == 'perf':
        query = '记忆里的第1234件小事，说给你听'
        started = time.perf_counter()
        turn = {}
        loop.run_until_complete(plugin._memory_recall(event, query,
                                                      vec=harness.fake_vector(query), turn=turn))
        elapsed = time.perf_counter() - started
        result = {'ms': round(elapsed * 1000.0, 1), 'kept': len(library()['entries']),
                  'top': len(turn.get('memory_entries') or [])}

    for task in asyncio.all_tasks(loop):
        task.cancel()
    try:
        loop.run_until_complete(asyncio.gather(*[t for t in asyncio.all_tasks(loop)
                                                 if not t.done()], return_exceptions=True))
    except Exception:
        pass
    for name in ('_forget_reg', '_vectors_db'):
        store = getattr(plugin, name, None)
        close = getattr(store, 'close', None)
        if callable(close):
            try:
                close()
            except Exception:
                pass
            setattr(plugin, name, None)
    out.write_text(json.dumps(result, ensure_ascii=False, default=str), encoding='utf-8')


# ---------------------------------------------------------------------------
# 1/2: never cut for room
# ---------------------------------------------------------------------------
class NothingIsCutForRoom(unittest.TestCase):
    def test_120_memories_in_one_place_are_all_kept(self):
        r = run_case('keep120')
        self.assertEqual(r['count'], 120)              # an old cut kept only the last 80
        self.assertEqual(r['stored'], 120)             # and their vectors
        self.assertTrue(r['all_vectors'])
        self.assertEqual(r['in_json'], 0)              # vectors live in the vector store

    def test_250_memories_with_compression_on_are_all_kept(self):
        r = run_case('keep250')
        self.assertEqual(r['count'], 250)              # an old cut kept only the last 200
        self.assertEqual(r['stored'], 250)
        self.assertTrue(r['all_vectors'])


# ---------------------------------------------------------------------------
# 3/4: the tier is worked out again when a memory is looked for
# ---------------------------------------------------------------------------
class TiersWorkedOutOnRecall(unittest.TestCase):
    def test_an_old_one_stored_as_hot_is_cold_when_recalled(self):
        r = run_case('tiers')
        for eid in ('c1', 'c2', 'c3', 'c4'):
            self.assertEqual(r['stored_before'][eid], 'hot')   # what was written when it was made
            self.assertEqual(r['tiers'][eid], 'cold')          # what the recall worked out, and wrote back

    def test_a_very_important_old_one_stays_hot(self):
        r = run_case('tiers')
        self.assertEqual(r['tiers']['high'], 'hot')
        self.assertIn('high', r['top'])

    def test_at_most_two_cold_ones_fill_a_read(self):
        r = run_case('tiers')
        self.assertLessEqual(len(r['top_cold']), 2)
        self.assertNotEqual(r['top_cold'], [])         # the cold ones are candidates, just few get read

    def test_a_summary_mark_still_keeps_it_out_of_recall(self):
        r = run_case('tiers')
        self.assertIn('sum', r['tiers'])               # the memory itself is still kept
        self.assertTrue(r['summarized']['sum'])
        self.assertNotIn('sum', r['top'])              # a marked entry is not read any more


# ---------------------------------------------------------------------------
# 5: an entry set aside by the load comes back on save
# ---------------------------------------------------------------------------
class NothingIsLostOnSave(unittest.TestCase):
    def test_an_unusable_text_is_set_aside_not_dropped(self):
        r = run_case('unusable')
        self.assertEqual(r['loaded'], ['good'])                  # not offered to recall
        self.assertEqual(r['aside'], ['sys1', 'sys2'])           # but kept
        self.assertEqual(len(r['after']), 4)                     # good, sys1, sys2 and the new one
        self.assertIn('good', r['after'])
        self.assertIn('sys1', r['after'])
        self.assertIn('sys2', r['after'])
        self.assertEqual(r['texts']['sys1'], '[BioCore] 你正在扮演小爱')
        self.assertEqual(r['texts']['sys2'], '注意，你正在社交媒体上和人聊天')
        self.assertNotIn('_unusable_entries', r['rooms_keys'])   # the bookkeeping is not written to rooms


# ---------------------------------------------------------------------------
# 6: what is meant to go still goes
# ---------------------------------------------------------------------------
class DeliberateDeletesStillDelete(unittest.TestCase):
    def test_a_forgotten_person_does_not_come_back(self):
        r = run_case('deletes')
        self.assertNotIn('his', r['after_forget'])               # the registry still takes it out
        self.assertTrue(r['after_forget'])                       # and the new memory is kept

    def test_duplicates_still_merge(self):
        r = run_case('deletes')
        self.assertEqual(r['merged'], 1)
        self.assertEqual(r['merged_hits'], [2])

    def test_a_panel_delete_stays_deleted(self):
        r = run_case('deletes')
        self.assertEqual(r['panel_status'], 'ok')
        self.assertTrue(r['panel_gone'])


# ---------------------------------------------------------------------------
# 7-11: putting back what was lost, from a copy of the data folder
# ---------------------------------------------------------------------------
class RestoreTool(unittest.TestCase):
    def test_a_dry_run_counts_and_writes_nothing(self):
        r = run_case('restore_dry')
        self.assertEqual(r['rows'][0][0], 3)            # backup-a: 3 not in the library (1 already there)
        self.assertEqual(r['rows'][0][1], 0)
        self.assertEqual(r['rows'][0][2], 0)
        self.assertEqual(r['rows'][0][3], 0)
        self.assertEqual(r['total'], 3)
        self.assertIn('能补 3 条', r['out'])
        self.assertTrue(r['unchanged'])                 # nothing written
        self.assertEqual(r['library_rows'], 1)
        self.assertNotIn('补回来的第一条', r['out'])      # no words
        self.assertNotIn('10004', r['out'])             # no number
        self.assertNotIn('900001', r['out'])            # no place

    def test_apply_puts_back_three_and_copies_first(self):
        r = run_case('restore_apply')
        self.assertEqual(r['written'], 3)
        self.assertEqual(r['ids'], ['r1', 'r2', 'r3'])
        self.assertTrue(r['ts_same'])                    # each one's own time
        self.assertTrue(r['origin_same'])                # where it came from, as it was
        self.assertTrue(r['provenance_same'])
        self.assertTrue(r['importance_same'])
        self.assertTrue(all(r['vectors'].values()))      # vectors from the copy's vectors.sqlite3
        self.assertTrue(r['copy_name'].startswith('memory-备份-补回前-'))
        self.assertTrue(r['copy_library_same'])          # the copy is the memory folder as it was
        self.assertTrue(r['copy_vectors'])

    def test_the_forget_registry_still_keeps_people_out(self):
        r = run_case('restore_forget')
        self.assertEqual(r['registry'], 1)               # counted as kept out by the registry
        self.assertEqual(r['restorable'], 1)             # only the other one
        self.assertEqual(r['applied'], 1)
        self.assertNotIn('gone', r['ids_after'])
        self.assertIn('keep', r['ids_after'])

    def test_the_red_line_still_keeps_things_out(self):
        r = run_case('restore_redline')
        self.assertEqual(r['redline'], 1)
        self.assertEqual(r['restorable'], 1)
        self.assertEqual(r['applied'], 1)
        self.assertNotIn('bad', r['ids_after'])
        self.assertIn('ok', r['ids_after'])

    def test_a_vector_of_other_dimensions_is_worked_out_again(self):
        r = run_case('restore_vectors')
        self.assertEqual(r['restorable'], 2)
        self.assertEqual(r['recomputed'], 2)             # m1 wrong length, m2 missing
        self.assertEqual(r['written'], 2)
        self.assertTrue(all(r['vectors'].values()))
        self.assertEqual(r['failed_no_vector'], 1)       # the local service refused: not put back
        self.assertEqual(r['failed_restorable'], 0)
        self.assertEqual(r['failed_written'], 0)
        self.assertNotIn('m3', r['ids_after'])


# ---------------------------------------------------------------------------
# 12: the time of one recall at 5000 memories (counted, not asserted)
# ---------------------------------------------------------------------------
class Speed(unittest.TestCase):
    def test_one_recall_at_5000_memories(self):
        r = run_case('perf')
        self.assertEqual(r['kept'], 5000)
        print('5000 条记忆时，一次回话找记忆用了 %.1f ms' % r['ms'])


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '_case':
        run_script(sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]))
    else:
        unittest.main()
