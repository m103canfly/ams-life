# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Compare event reads with the frozen AstrBot behavior."""
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot
import harness
import main
import mixin_browse
import mixin_group_browse
import mixin_media
import turn
from astrbot.api.message_components import Image


# mixin_phone.py 262-265 at 8763a44.
def old_message_id(event):
    try:
        return str(getattr(getattr(event, "message_obj", None), "message_id", "") or "")
    except Exception:
        return ""


# mixin_autonomy.py 26-35 at 8763a44.
def old_private_event(event):
    try:
        umo = str(getattr(event, "unified_msg_origin", "") or "")
        if "GroupMessage" in umo or "GuildMessage" in umo:
            return False
        check = getattr(event, "is_private_chat", None)
        if callable(check):
            return bool(check())
        return False
    except Exception:
        return False


# mixin_media.py 52, 83, 296; mixin_selfie.py 187; mixin_browse.py 526;
# mixin_group_browse.py 67-68 at 8763a44.
def old_reads(event):
    obj = getattr(event, 'message_obj', None)
    return (event.is_private_chat(), bool(getattr(event, 'is_private_chat', lambda: False)()),
            event.is_private_chat(), str(getattr(obj, 'self_id', '') or ''),
            str(getattr(obj, 'message_id', '') or ''))


def fake(event):
    p = MagicMock()
    p._here.return_value = 'group:900001'
    p._speaker.return_value = (event.get_sender_id(), 'Alice')
    p._job_stale.return_value = False
    p._source_ids.return_value = ['source']
    p._may_keep.return_value = True
    p._addresses_her.return_value = False
    p.image_recognition_enabled = True
    p._recent_images = {}
    p._group_state.return_value = {}
    p._phone_counts.return_value = {}
    p._familiarity.return_value = 0.5
    p._core.return_value.snapshot.return_value = {'v': 0, 'energy': 0.5}
    return p


class EventReads(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin.__new__(main.BioCorePlugin)
        self.cases = []
        for group, sender, self_id, has_id in [('900001', '10001', '20002', True),
                                                (None, '10001', '20002', False),
                                                ('900001', '20002', '20002', True)]:
            ev = harness.FakeEvent('hello', sender=sender, group=group, self_id=self_id)
            if not has_id:
                ev.message_obj.message_id = ''
            ev.get_messages = lambda: [Image(file='example.png')]
            self.cases.append(ev)

    async def check_readers(self, ev, target):
        private_refs, private_context, private_phone, self_id, message_id = old_reads(ev)
        self.assertEqual(self.plugin._message_id(target), old_message_id(ev))
        self.assertEqual(self.plugin._is_private_event(target), old_private_event(ev))
        p = fake(ev)
        refs = mixin_media.MediaMixin._image_refs(p, target)
        self.assertEqual(bool(refs), private_refs)
        p._llm_allowed.return_value = True
        p._image_refs.return_value = []
        p._quoted_image_refs = AsyncMock(return_value=[])
        p._stickers_on.return_value = False
        await mixin_media.MediaMixin._image_context(p, target)
        self.assertEqual(p._quoted_image_refs.await_count, int(private_context))
        context = self.plugin._phone_context.__func__(p, target)
        self.assertIn('私聊' if private_phone else '群聊', context)
        mixin_group_browse.GroupBrowseMixin._group_heard(p, target)
        self.assertEqual(bool(p._group_state.return_value), ev.get_sender_id() != self_id)
        mixin_media.MediaMixin._remember_images(p, target)
        self.assertEqual(bool(p._recent_images), ev.get_sender_id() != self_id)
        p._remember_web = AsyncMock(return_value=True)
        setattr(target, mixin_browse.READ_ATTR, [{}])
        await mixin_browse.BrowseMixin._browse_keep_reply(p, target)
        self.assertEqual(p._remember_web.await_args.args[1], 'reply:' + message_id)

    async def test_astrbot_readers_match_frozen_lines(self):
        for ev in self.cases:
            with self.subTest(origin=ev.unified_msg_origin, sender=ev.get_sender_id()):
                await self.check_readers(ev, ev)

    async def test_turn_event_readers_match_frozen_lines(self):
        for ev in self.cases:
            with self.subTest(origin=ev.unified_msg_origin, sender=ev.get_sender_id()):
                wrapped = turn.TurnEvent(adapter_astrbot.from_astrbot(ev), unified_msg_origin=ev.unified_msg_origin)
                await self.check_readers(ev, wrapped)

    async def test_missing_origin_intentionally_is_not_private(self):
        ev = harness.FakeEvent('hello', group=None)
        del ev.unified_msg_origin
        ev.get_messages = lambda: [Image(file='example.png')]
        private_refs, private_context, private_phone, _, _ = old_reads(ev)
        self.assertTrue(private_refs)
        self.assertTrue(private_context)
        self.assertTrue(private_phone)
        self.assertTrue(old_private_event(ev))
        p = fake(ev)
        # The four missing-origin reads intentionally no longer treat this as private.
        self.assertEqual(mixin_media.MediaMixin._image_refs(p, ev), [])
        p._llm_allowed.return_value = True
        p._image_refs.return_value = []
        p._quoted_image_refs = AsyncMock(return_value=[])
        p._stickers_on.return_value = False
        await mixin_media.MediaMixin._image_context(p, ev)
        self.assertEqual(p._quoted_image_refs.await_count, 0)
        self.assertIn('群聊', self.plugin._phone_context.__func__(p, ev))
        self.assertFalse(self.plugin._is_private_event(ev))

    def test_session_string_and_window_fallback(self):
        ev = turn.TurnEvent(adapter_astrbot.from_astrbot(self.cases[0]))
        self.assertEqual(ev.unified_msg_origin, '')
        ev.unified_msg_origin = self.cases[0].unified_msg_origin
        self.plugin._read_window = MagicMock(return_value={'umo': 'default:FriendMessage:10003'})
        self.assertEqual(self.plugin._umo_of('group:900001', ev), ev.unified_msg_origin)
        self.assertEqual(self.plugin._umo_of('private:10003', ev), 'default:FriendMessage:10003')

    def test_event_source_reads_are_limited(self):
        root = Path(__file__).resolve().parent.parent
        found = []
        for path in [root / 'main.py', *root.glob('mixin_*.py')]:
            for line in path.read_text(encoding='utf-8').splitlines():
                self.assertNotIn('is_private_chat(', line, path.name)
                if 'message_obj' in line:
                    found.append((path.name, line.strip()))
        self.assertEqual({name for name, _ in found},
                         {'mixin_turn.py', 'mixin_stickers.py', 'mixin_group_browse.py', 'mixin_browse.py'})
        self.assertEqual(len(found), 4)


if __name__ == '__main__':
    unittest.main()
