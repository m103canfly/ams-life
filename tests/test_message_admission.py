"""Offline admission and speaking policy; all identities are fictional."""
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_body_heart import CLOCK  # noqa: F401,E402
import harness  # noqa: E402
import main  # noqa: E402


class MessageAdmission(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = main.BioCorePlugin(harness.FakeContext(), config={
            'owner_qq': '10001', 'reply_groups': ['900001']})
        self.saved = []
        for name in ('_begin_job', '_check_registry', '_listen_body', '_ensure_autonomy_task',
                     '_group_heard', '_sticker_in_passing'):
            setattr(self.plugin, name, Mock())
        self.plugin._window_add_message = Mock(side_effect=lambda event: self.saved.append(event))

    async def deliver(self, event):
        await self.plugin.on_message(event)
        model = Mock()
        if event.is_at_or_wake_command and not event.stopped:
            model()
        return model.call_count

    async def test_other_group_saved_and_stopped_even_when_called(self):
        for called in (False, True):
            event = harness.FakeEvent('sample', group='900002')
            event.is_at_or_wake_command = called
            self.assertEqual(await self.deliver(event), 0)
            self.assertTrue(event.stopped)
            self.assertIn(event, self.saved)

    async def test_other_group_writes_phone_window_before_stop(self):
        event = harness.FakeEvent('sample', group='900002')
        window = {'recent': []}
        stopped_at_write = []
        self.plugin._window_add_message = main.BioCorePlugin._window_add_message.__get__(self.plugin)
        with patch.object(self.plugin, '_job_stale', return_value=False), \
             patch.object(self.plugin, '_remember_images'), \
             patch.object(self.plugin, '_message_text', return_value='sample'), \
             patch.object(self.plugin, '_read_window', return_value=window), \
             patch.object(self.plugin, '_write_window', side_effect=lambda *args: stopped_at_write.append(event.stopped)) as write, \
             patch.object(self.plugin, '_event_origin', return_value={}), \
             patch.object(self.plugin, '_reply_to', return_value=None), \
             patch.object(self.plugin, '_note_name'):
            self.assertEqual(await self.deliver(event), 0)
        self.assertTrue(event.stopped)
        self.assertEqual(stopped_at_write, [False])
        self.assertEqual(window['recent'][0]['text'], 'sample')
        write.assert_called_once_with('group:900002', window)

    async def test_allowed_group_continues(self):
        event = harness.FakeEvent('sample', group='900001')
        self.assertEqual(await self.deliver(event), 1)
        self.assertFalse(event.stopped)
        self.assertIn(event, self.saved)

    async def test_allowed_group_not_called_is_not_stopped(self):
        event = harness.FakeEvent('sample', group='900001')
        event.is_at_or_wake_command = False
        self.assertEqual(await self.deliver(event), 0)
        self.assertFalse(event.stopped)
        self.assertIn(event, self.saved)

    async def test_disabled_other_group_stops_without_storing(self):
        self.plugin.enabled = False
        for allow_called in (False, True):
            self.plugin.config['reply_other_groups_when_called'] = allow_called
            event = harness.FakeEvent('sample', group='900002')
            self.assertEqual(await self.deliver(event), 0)
            self.assertTrue(event.stopped)
        for name in ('_begin_job', '_check_registry', '_window_add_message', '_listen_body',
                     '_ensure_autonomy_task', '_group_heard', '_sticker_in_passing'):
            getattr(self.plugin, name).assert_not_called()
        self.assertEqual(self.saved, [])

    async def test_disabled_allowed_group_continues_without_storing(self):
        self.plugin.enabled = False
        event = harness.FakeEvent('sample', group='900001')
        self.assertEqual(await self.deliver(event), 1)
        self.assertFalse(event.stopped)
        for name in ('_begin_job', '_check_registry', '_window_add_message', '_listen_body',
                     '_ensure_autonomy_task', '_group_heard', '_sticker_in_passing'):
            getattr(self.plugin, name).assert_not_called()

    async def test_empty_reply_groups_stops_all_groups(self):
        self.plugin.config['reply_groups'] = []
        for group in ('900001', '900002'):
            event = harness.FakeEvent('sample', group=group)
            self.assertEqual(await self.deliver(event), 0)
            self.assertTrue(event.stopped)
            self.assertIn(event, self.saved)

    async def test_private_admission_and_empty_owner(self):
        self.plugin.config['reply_private'] = ['10002']
        for sender, allowed in (('10001', True), ('10002', True), ('10003', False)):
            event = harness.FakeEvent('sample', sender=sender)
            self.assertEqual(await self.deliver(event), int(allowed))
            self.assertEqual(event.stopped, not allowed)
            self.assertEqual(event in self.saved, allowed)
        self.plugin.config['owner_qq'] = ''
        for sender in ('10001', '10002'):
            event = harness.FakeEvent('sample', sender=sender)
            self.assertEqual(await self.deliver(event), 0)
            self.assertTrue(event.stopped)
            self.assertNotIn(event, self.saved)
        self.assertEqual(self.plugin._check_registry.call_count, 2)
        self.assertEqual(self.plugin._sticker_in_passing.call_count, 2)

    async def test_self_decide_cannot_answer_other_group(self):
        self.plugin.self_decide = True
        event = harness.FakeEvent('sample', group='900002')
        await self.deliver(event)
        with patch.object(self.plugin, '_decide', new=AsyncMock()) as decide:
            self.assertEqual([x async for x in self.plugin.on_message_decide(event)], [])
            decide.assert_not_awaited()
        self.assertIsNone(await self.plugin._decide(event))
        self.assertTrue(event.stopped)

    async def test_other_group_called_switch(self):
        self.plugin.config['reply_other_groups_when_called'] = True
        for called in (False, True):
            event = harness.FakeEvent('sample', group='900002')
            event.is_at_or_wake_command = called
            self.assertEqual(await self.deliver(event), int(called))
            self.assertEqual(event.stopped, not called)
            self.assertIn(event, self.saved)

    async def test_sticker_never_sent_to_other_group(self):
        event = harness.FakeEvent('sample', group='900002')
        with patch.object(self.plugin, '_sticker_lib') as library:
            self.assertFalse(await self.plugin._send_sticker(event, 'sample', '', 'group:900002'))
            library.assert_not_called()

    async def test_group_browse_chooses_only_allowed_groups(self):
        self.plugin.browse_groups_enabled = True
        self.plugin._group_open_state = {'group:900002': {'unread': 100, 'first_unread': 0}}
        with patch('mixin_group_browse.attention.is_night', return_value=False), \
             patch.object(self.plugin, '_core', return_value=type('Core', (), {'v': 0})()):
            self.assertNotEqual(self.plugin._group_action()[0], 'group')
