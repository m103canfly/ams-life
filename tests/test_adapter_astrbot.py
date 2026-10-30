# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""What one received message looks like (events.py, adapter_astrbot.py), and that the
fields match what the plugin computes today. All numbers, names and links are made up."""
import copy
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE / 'stubs'))

import events  # noqa: E402
import adapter_astrbot  # noqa: E402
import harness  # noqa: E402
from adapter_astrbot import from_astrbot  # noqa: E402
from astrbot.api.message_components import At, Face, Image, Plain, Record, Reply  # noqa: E402

ME = '20002'          # her own account, made up
GROUP = '900001'      # a group, made up
HIM = '10001'         # someone in the group, made up
OTHER = '10003'       # someone else, made up


def event(text='你好', sender=HIM, name='柠檬', group=GROUP):
    return harness.FakeEvent(text, sender=sender, name=name, group=group, self_id=ME)


def with_parts(ev, *parts):
    """Give this event a different message (the harness itself is not changed)."""
    ev.get_messages = lambda: list(parts)
    return ev


class OneMessage(unittest.TestCase):
    """What the fields are, one case at a time."""

    def test_a_plain_message_in_a_group(self):
        one = from_astrbot(event('你好'))
        self.assertEqual(one.place, 'group:' + GROUP)
        self.assertFalse(one.is_private)
        self.assertEqual(one.segments, (events.Segment('text', {'text': '你好'}),))
        self.assertEqual(events.plain_text(one), '你好')
        self.assertEqual((one.sender_id, one.sender_name), (HIM, '柠檬'))
        self.assertEqual((one.self_id, one.message_id), (ME, 'm你好'))
        self.assertFalse(one.is_self)
        self.assertGreater(one.ts, 0)

    def test_a_message_in_a_private_chat(self):
        one = from_astrbot(event('在吗', group=None))
        self.assertEqual(one.place, 'private:' + HIM)
        self.assertTrue(one.is_private)

    def test_an_at_of_her_wakes_her(self):
        ev = with_parts(event(), At(qq=ME, name='小爱'), Plain(' 你好'))
        ev.is_at_or_wake_command = False
        one = from_astrbot(ev)
        self.assertTrue(one.at_me)
        self.assertEqual(one.segments, (events.Segment('at', {'qq': ME, 'name': '小爱'}),
                                        events.Segment('text', {'text': ' 你好'})))

    def test_an_at_of_someone_else_leaves_the_wake_check_to_the_platform(self):
        ev = with_parts(event(), At(qq=OTHER, name='阿星'), Plain(' 在吗'))
        ev.is_at_or_wake_command = False
        self.assertFalse(from_astrbot(ev).at_me)
        ev.is_at_or_wake_command = True
        self.assertTrue(from_astrbot(ev).at_me)

    def test_a_quote_of_her_message_wakes_her(self):
        ev = with_parts(event(), Reply(id='m-7001', sender_id=ME), Plain(' 嗯'))
        ev.is_at_or_wake_command = False
        one = from_astrbot(ev)
        self.assertTrue(one.at_me)
        self.assertEqual(one.reply_to, 'm-7001')
        self.assertEqual(one.segments[0], events.Segment('reply', {'id': 'm-7001', 'sender_id': ME}))

    def test_a_quote_of_someone_else_is_reply_to_only(self):
        ev = with_parts(event(), Reply(id='m-7002', sender_id=OTHER), Plain(' 嗯'))
        ev.is_at_or_wake_command = False
        one = from_astrbot(ev)
        self.assertFalse(one.at_me)
        self.assertEqual(one.reply_to, 'm-7002')
        ev.is_at_or_wake_command = True
        self.assertTrue(from_astrbot(ev).at_me)

    def test_a_long_quoted_id_is_cut_to_eighty(self):
        ev = with_parts(event(), Reply(id='x' * 100, sender_id=OTHER), Plain(' 嗯'))
        self.assertEqual(from_astrbot(ev).reply_to, 'x' * 80)

    def test_the_images_of_this_message_in_order_the_quoted_ones_left_out(self):
        ev = with_parts(event(), Image(url='http://img.test/a.png'), Plain('和'),
                        Image(file='b.png'),
                        Reply(id='m-7003', sender_id=OTHER,
                              chain=[Image(url='http://img.test/quoted.png')]))
        one = from_astrbot(ev)
        self.assertEqual(one.image_refs, ('http://img.test/a.png', 'b.png'))
        self.assertNotIn('http://img.test/quoted.png', one.image_refs)

    def test_an_image_with_a_url_and_a_file_takes_the_url(self):
        # a picture from QQ often carries both: the url is the reference, as _image_ref prefers
        ev = with_parts(event(), Plain('看'), Image(url='http://img.test/both.png', file='both.png'))
        self.assertEqual(from_astrbot(ev).image_refs, ('http://img.test/both.png',))

    def test_a_face_a_voice_and_a_part_nobody_knows(self):
        class Sticker:
            pass

        one = from_astrbot(with_parts(event(), Face(id='14'), Record(file='voice.amr'), Sticker()))
        self.assertEqual([seg.type for seg in one.segments], ['face', 'record', 'other'])
        self.assertEqual(one.segments[0].data, {'id': '14'})
        self.assertEqual(one.segments[1].data, {'url': '', 'file': 'voice.amr'})
        self.assertEqual(one.segments[2].data, {'kind': 'Sticker'})

    def test_her_own_message(self):
        one = from_astrbot(event('好', sender=ME, name='小爱'))
        self.assertTrue(one.is_self)

    def test_plain_text_leaves_out_everything_that_is_not_words(self):
        ev = with_parts(event(), Plain('看这个'), Image(url='http://img.test/a.png'),
                        At(qq=OTHER, name='阿星'), Plain(' 好看'))
        self.assertEqual(events.plain_text(from_astrbot(ev)), '看这个 好看')


class Broken(unittest.TestCase):
    """A field that cannot be read becomes empty; nothing is raised."""

    def test_without_a_message_object(self):
        ev = event()
        ev.message_obj = None
        ev.get_sender_id = None
        ev.get_sender_name = None
        one = from_astrbot(ev)
        self.assertEqual((one.self_id, one.message_id), ('', ''))
        self.assertEqual((one.sender_id, one.sender_name), ('', ''))
        self.assertFalse(one.is_self)

    def test_a_message_that_cannot_be_read(self):
        def unreadable():
            raise RuntimeError('offline failure')

        ev = event()
        ev.get_messages = unreadable
        one = from_astrbot(ev)
        self.assertEqual(one.segments, ())
        self.assertEqual(one.reply_to, '')
        self.assertEqual(one.image_refs, ())
        self.assertFalse(one.at_me)   # what the plugin's _addresses_her answers too

    def test_without_a_place(self):
        ev = event()
        del ev.unified_msg_origin
        one = from_astrbot(ev)
        self.assertEqual(one.place, '')
        self.assertFalse(one.is_private)
        self.assertEqual(events.plain_text(one), '你好')

    def test_nothing_is_written_and_the_event_is_not_changed(self):
        ev = with_parts(event(), At(qq=ME, name='小爱'), Plain(' 你好'),
                        Image(url='http://img.test/a.png'))
        before = copy.copy(ev.__dict__)
        from_astrbot(ev)
        self.assertEqual(ev.__dict__, before)


class SameAsThePlugin(unittest.TestCase):
    """The same events through the adapter and through the plugin's own methods."""

    @classmethod
    def setUpClass(cls):
        # The plugin mixins import common, which wants a data dir. Discovery has already
        # given it one; running this file alone gets a temporary one, outside the repository.
        cls.made = None
        if not os.environ.get('AMS_LIFE_DATA_DIR'):
            cls.made = tempfile.mkdtemp(prefix='ams-life-adapter-')
            os.environ['AMS_LIFE_DATA_DIR'] = cls.made
        import mixin_media
        import mixin_memory
        import mixin_phone
        cls.media = mixin_media.MediaMixin()
        cls.memory = mixin_memory.MemoryMixin()
        cls.phone = mixin_phone.PhoneMixin()
        at_her = with_parts(event(), At(qq=ME, name='小爱'), Plain(' 你好'))
        quoted_her = with_parts(event(), Reply(id='m-7001', sender_id=ME), Plain(' 嗯'))
        quoted_other = with_parts(event(), Reply(id='m-7002', sender_id=OTHER), Plain(' 嗯'))
        pictures = with_parts(event(), Image(url='http://img.test/a.png'), Image(file='b.png'))
        both = with_parts(event(), Image(url='http://img.test/both.png', file='both.png'))
        cls.cases = [event('你好'), event('在吗', group=None), at_her, quoted_her, quoted_other, pictures,
                     both]
        for ev in cls.cases:
            ev.is_at_or_wake_command = False

    @classmethod
    def tearDownClass(cls):
        if cls.made:
            os.environ.pop('AMS_LIFE_DATA_DIR', None)
            import shutil
            shutil.rmtree(cls.made, ignore_errors=True)

    def test_the_fields_follow_the_plugin(self):
        for ev in self.cases:
            one = from_astrbot(ev)
            self.assertEqual(one.place, self.memory._here(ev))
            self.assertEqual(one.at_me, self.phone._addresses_her(ev))
            self.assertEqual(one.reply_to, self.phone._reply_to(ev))
            self.assertEqual(one.message_id, self.phone._message_id(ev))
            self.assertEqual(one.image_refs,
                             tuple(self.media._image_ref(comp) for comp in ev.get_messages()
                                   if type(comp).__name__ == 'Image'))


if __name__ == '__main__':
    unittest.main()
