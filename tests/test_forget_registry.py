"""The forget registry (step 1, part 3): who and what she must not keep. All numbers are made up."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import fake_old_data as fake  # noqa: E402
import forget_registry as fr  # noqa: E402

G1, G2 = 'group:900001', 'group:900002'


class Rows(unittest.TestCase):
    def setUp(self):
        self.reg = fr.ForgetRegistry()

    def tearDown(self):
        self.reg.close()

    def test_forget_person_hides_everything_before(self):
        self.reg.forget_person('10001', G1, stamp=100)
        self.assertEqual(self.reg.why_not('10001', G1, at=50), 'forgotten')
        self.assertEqual(self.reg.why_not('10001', G1, at=100), 'forgotten')
        self.assertTrue(self.reg.may_keep('10001', G2, at=50))       # only in that group
        self.assertTrue(self.reg.may_keep('10002', G1, at=50))       # only him

    def test_later_messages_depend_on_the_reading(self):
        self.reg.forget_person('10001', G1, stamp=100)
        self.assertEqual(self.reg.why_not('10001', G1, at=200), 'optout')                  # default: not again
        self.assertEqual(self.reg.why_not('10001', G1, at=200, forget_me=fr.FORGET_ME_CUTOFF), '')

    def test_optout_and_optin(self):
        self.reg.opt_out('10001', stamp=100)
        self.assertTrue(self.reg.may_keep('10001', G1, at=50))
        self.assertFalse(self.reg.may_keep('10001', G2, at=150))     # everywhere
        self.reg.opt_in('10001', stamp=300)
        self.assertTrue(self.reg.may_keep('10001', G1, at=350))
        self.assertFalse(self.reg.may_keep('10001', G1, at=250))

    def test_optin_does_not_bring_back_what_was_forgotten(self):
        self.reg.forget_person('10001', fr.EVERYWHERE, stamp=100)
        self.reg.opt_in('10001', stamp=300)
        self.assertEqual(self.reg.why_not('10001', G1, at=50), 'forgotten')
        self.assertEqual(self.reg.why_not('10001', G1, at=200), 'optout')
        self.assertEqual(self.reg.why_not('10001', G1, at=400), '')

    def test_forget_a_message(self):
        self.reg.forget_message('m1', G1)
        self.assertEqual(self.reg.why_not(source_id='m1', place=G1), 'source')
        self.assertEqual(self.reg.why_not(source_id='m1', place=''), 'source')
        self.assertEqual(self.reg.why_not(source_id='m1', place=G2), '')
        self.reg.forget_message('m2')
        self.assertEqual(self.reg.why_not(source_id='m2', place=G2), 'source')

    def test_everyone_in_a_place(self):
        self.reg.forget_person('*', G1, stamp=100)
        self.assertFalse(self.reg.may_keep('10009', G1, at=50))
        self.assertTrue(self.reg.may_keep('10009', G1, at=150))
        self.assertTrue(self.reg.may_keep('10009', G2, at=50))

    def test_several_people_and_messages(self):
        self.reg.forget_message('m1', G1)
        self.reg.opt_out('10002', stamp=0)
        self.assertTrue(self.reg.may_keep_all(['10001'], G1, 10, ['m9']))
        self.assertFalse(self.reg.may_keep_all(['10001'], G1, 10, ['m9', 'm1']))
        self.assertFalse(self.reg.may_keep_all(['10001', '10002'], G1, 10, []))

    def test_places_are_normalised_and_rows_not_doubled(self):
        self.assertTrue(self.reg.forget_message('m1', 'default:GroupMessage:900001'))
        self.assertEqual(self.reg.forget_message('m1', G1), 0)
        self.assertEqual(self.reg.rows()[0]['place'], G1)
        self.assertEqual(self.reg.stats()['source'], 1)

    def test_owner_deletes_from_the_panel(self):
        seqs = self.reg.owner_delete(person='10001', stamp=100)
        self.assertEqual(len(seqs), 1)
        self.assertFalse(self.reg.may_keep('10001', G2, at=50))      # a person: everywhere
        self.assertFalse(self.reg.may_keep('10001', G2, at=150))     # and not again (default reading)
        self.reg.owner_delete(source_ids=['m1', 'm2', ''], place=G1, stamp=200)
        self.assertEqual(self.reg.why_not(source_id='m2', place=G1), 'source')
        self.assertEqual({r['note'] for r in self.reg.rows()}, {'owner:panel'})
        self.assertEqual(self.reg.owner_delete(source_ids=['m1'], place=G1), [0])

    def test_no_impression_only_stops_impressions(self):
        self.reg.stop_impression('10002')
        self.assertFalse(self.reg.impression_allowed('10002', G1))
        self.assertTrue(self.reg.impression_allowed('10001', G1))
        self.assertTrue(self.reg.may_keep('10002', G1, at=50))       # what she remembers of him: untouched
        self.assertEqual(self.reg.people(), set())
        self.reg.stop_impression('10001', G2)
        self.assertTrue(self.reg.impression_allowed('10001', G1))
        self.assertFalse(self.reg.impression_allowed('10001', G2))

    def test_bad_rows(self):
        with self.assertRaises(ValueError):
            self.reg.add('nope', qq='1')
        with self.assertRaises(ValueError):
            self.reg.add('source')
        with self.assertRaises(ValueError):
            self.reg.add('qq')

    def test_on_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / fr.FILE_NAME
            with fr.ForgetRegistry(path) as reg:
                reg.forget_person('10001', stamp=100)
            with fr.ForgetRegistry(path) as reg:
                self.assertEqual(reg.people(), {'10001'})
                self.assertEqual(reg.last_seq(), 1)


class Names(unittest.TestCase):
    """What a person deleted from the panel was called: salted hashes, found in what others say."""

    def test_found_and_never_stored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / fr.FILE_NAME
            with fr.ForgetRegistry(path) as reg:
                self.assertEqual(reg.names_in('阿星来不来'), {})
                self.assertEqual(reg.remember_names('10003', ['阿星', '星', '10003', '12345', 'Tom', '阿星']), 2)
                self.assertEqual(reg.remember_names('10003', ['阿星']), 0)
                self.assertEqual(reg.names_in('周末 阿星来不来'), {'阿星': '10003'})
                self.assertEqual(reg.names_in('Tom 来了'), {'Tom': '10003'})
                self.assertEqual(reg.names_in('Tomorrow 见'), {})       # letters only as a word of their own
                self.assertEqual(reg.names_in('星星'), {})               # one character is not kept
            with fr.ForgetRegistry(path) as again:                      # reopened: still found
                self.assertEqual(again.names_in('阿星呢'), {'阿星': '10003'})
            raw = path.read_bytes()
            for name in ('阿星', 'Tom'):
                self.assertNotIn(name.encode('utf-8'), raw)

    def test_each_registry_its_own_salt(self):
        with fr.ForgetRegistry(None) as one, fr.ForgetRegistry(None) as two:
            one.remember_names('10003', ['阿星'])
            two.remember_names('10003', ['阿星'])
            digests = [r.execute('SELECT digest FROM names').fetchone()[0] for r in (one._db, two._db)]
            self.assertNotEqual(digests[0], digests[1])


class Legacy(unittest.TestCase):
    def test_old_registries(self):
        with tempfile.TemporaryDirectory() as tmp:
            snow = fake.build_old(tmp)
            with fr.ForgetRegistry() as reg:
                a = fr.import_notebook_tombstones(reg, snow / 'notebook-forget.sqlite3')
                b = fr.import_ledger_registry(reg, snow / 'ledger' / 'forget-registry.sqlite3')
                self.assertEqual(a, {'rows': 3, 'added': 3, 'already': 0, 'skipped': 0})
                # marker row skipped, -5001 already there, 5003 new, entry-only row, cutoff for the same moment already there
                self.assertEqual(b, {'rows': 5, 'added': 1, 'already': 2, 'skipped': 1, 'entry_rows': 1})
                self.assertEqual(reg.stats(), {'qq': 1, 'source': 3, 'optout': 0, 'optin': 0, 'impression': 0, 'people': 1})
                self.assertEqual(reg.why_not(fake.STAR, 'group:' + fake.G_BUSY, at=fake.T0 + 10), 'forgotten')
                self.assertEqual(reg.why_not(source_id='5003', place='group:' + fake.G_BUSY), 'source')
                self.assertTrue(reg.may_keep(fake.LEMON, 'group:' + fake.G_TEST, at=fake.T0 + 200))


if __name__ == '__main__':
    unittest.main()
