"""Import, identity and licence checks that need no conversation."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DATA = Path(tempfile.mkdtemp(prefix='ams-life-basics-'))
CLOCK = harness.prepare(DATA)
import main  # noqa: E402
import interpretation  # noqa: E402


class Identity(unittest.TestCase):
    def test_data_dir_follows_env(self):
        self.assertEqual(main.DATA_DIR, DATA)

    def test_default_data_dir_name(self):
        self.assertEqual(main._PERSIST_DATA_DIR.name, 'astrbot_plugin_ams_life')

    def test_routes_use_new_name(self):
        ctx = harness.FakeContext()
        main.BioCorePlugin(ctx, config={})
        self.assertTrue(ctx.web_routes)
        self.assertTrue(all(r.startswith('/astrbot_plugin_ams_life/page/') for r in ctx.web_routes), ctx.web_routes)

    def test_metadata(self):
        text = (ROOT / 'metadata.yaml').read_text('utf-8')
        self.assertIn('name: astrbot_plugin_ams_life', text)
        self.assertIn('repo: https://github.com/m103canfly/ams-life', text)

    def test_licence_and_attribution(self):
        self.assertIn('GNU AFFERO GENERAL PUBLIC LICENSE', (ROOT / 'LICENSE').read_text('utf-8'))
        notice = (ROOT / 'NOTICE.md').read_text('utf-8')
        self.assertIn('b3c214c80c85f3e35d82fdb5e04c1809dfac9b28', notice)
        self.assertIn('Johnhmzm', notice)
        self.assertIn('NOTICE.md', (ROOT / 'main.py').read_text('utf-8').splitlines()[2])


class Interpretation(unittest.TestCase):
    def test_reply_tag_is_stripped(self):
        # no tag is asked for; one the model writes anyway is cut out, parsed or not
        self.assertEqual(interpretation.strip_state_tags('好呀~<bc>{"e":"joy","i":0.6}</bc>'), '好呀~')
        self.assertEqual(interpretation.strip_state_tags('好呀~<bc>{坏掉的'), '好呀~')
        self.assertEqual(interpretation.strip_state_tags('<biocore>{}</biocore>好呀<BC>{}</BC>~'), '好呀~')

    def test_no_tag(self):
        self.assertEqual(interpretation.strip_state_tags('好呀~'), '好呀~')


class Split(unittest.TestCase):
    """main.py was split into modules; AstrBot must still find the plugin and its handlers in main.py."""

    def test_handlers_defined_in_main(self):
        for name in ('__init__', 'on_message', 'on_llm_request', 'on_llm_response'):
            self.assertIn(name, vars(main.BioCorePlugin), name)
        # step 1-3: the /biocore chat command is gone (anyone could reset what she learned)
        self.assertNotIn('biocore_command', vars(main.BioCorePlugin))

    def test_all_methods_reachable(self):
        methods = set()
        for klass in main.BioCorePlugin.__mro__[:-2]:  # drop Star, object
            methods |= {k for k in vars(klass) if not k.startswith('__')}
        # 210 upstream methods minus __init__, plus 10 for one-her (library, migration, discretion, forgetting)
        # and 18 for her phone (on_message, windows, open loops per window, moving old body texts)
        # and 3 for the forget count (_forget_count, _begin_job, _job_stale)
        # step 1-3: -1 for /biocore, +18 for the forget registry, the owner's deletes, what
        # else holds people's words, unique memory ids and the vector store;
        # review of PR #9: -6 for the old rollback / restore endpoints and their helpers,
        # +4 (_new_item_kept, _record_mentions, _EVERYDAY_WORDS, _library_ids);
        # +11 for the group members she knows (mixin_impressions, the panel's delete);
        # +1 for counting the backups a delete leaves alone;
        # review of PR #10: +2 (_material_names, _forget_registered);
        # step 1-3-5, no numbers and no red lines in what she keeps: +11 (_note_her, _gone_people,
        # _known_numbers, _scrubber, _scrub, _SCRUB_KEYS, _scrub_tree, _migrate_numbers, _red_line,
        # _KEPT_TEXT_KEYS, _keep_record_text); the red-line switch and its counts: +3 (_red_lines_for,
        # _red_line_counts, _count_red_line), and judgements of people under it too: +1 (_judgements_for)
        # brain map stage 2: +14 (mixin_brain: three read-only pages, noting each turn's recall)
        # review of PR #11: +3 (_brain_build in a worker thread, _registry_keeps, _origin_args);
        # main merged into PR #11: -1 for _brain_person_kept, no one called it
        # what happened today in each window: +6 (mixin_digest); review of PR #15: +2
        # (_gone_names_in: names of people the owner deleted; _save_night_marks), then +1
        # (_scrub_stores: what others said of him, 某人 everywhere as soon as he is deleted)
        # numbers kept (10-29): the scrub methods renamed, none more; review of PR #20: +2
        # (_note_at, _note_ats: someone only @'d is known by his number)
        # senders she ignores (the owner, 10-29): +1 (_ignored_sender)
        self.assertEqual(len(methods), 338)

    def test_backup_lists_every_module(self):
        import mixin_pages
        src = Path(mixin_pages.__file__).read_text('utf-8')
        self.assertIn('root.glob("*.py")', src)


if __name__ == '__main__':
    unittest.main()
