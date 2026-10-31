# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline tests for her tools as turn.TurnTool (move 5i-1): the three mixins make the neutral
list, and the old methods are AstrBot shells over it. AstrBot's tool classes are stand-ins put
into sys.modules for one test; nothing here writes a file or opens a network."""
import ast
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402,F401
import test_basics  # noqa: E402,F401  # reuse its AstrBot setup without replacing the clock

import adapter_astrbot_tools  # noqa: E402
import browse  # noqa: E402
import mixin_browse  # noqa: E402
import mixin_settings  # noqa: E402
import mixin_selfie as phone  # noqa: E402
import turn  # noqa: E402
from astrbot.api.provider import ProviderRequest  # noqa: E402


class FunctionTool:
    def __init__(self, name, description='', parameters=None, handler=None):
        self.name, self.description, self.parameters, self.handler = name, description, parameters, handler


class ToolSet:
    def __init__(self, tools=None):
        self.tools = list(tools or [])

    def names(self):
        return [tool.name for tool in self.tools]

    def add_tool(self, tool):
        self.tools.append(tool)


class FakeAstrBotTools:
    """AstrBot's tool classes in sys.modules for one test, then out again."""

    names = ('astrbot.core', 'astrbot.core.agent', 'astrbot.core.agent.tool')

    def __enter__(self):
        self.saved = {name: sys.modules.get(name) for name in self.names}
        for name in self.names:
            sys.modules[name] = types.ModuleType(name)
        module = sys.modules[self.names[-1]]
        module.FunctionTool, module.ToolSet = FunctionTool, ToolSet
        return module

    def __exit__(self, *args):
        for name, module in self.saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


class NoAstrBotTools:
    """The tool classes cannot be imported for this test (whatever an earlier test left behind)."""

    names = FakeAstrBotTools.names

    def __enter__(self):
        self.saved = {name: sys.modules.pop(name, None) for name in self.names}
        return self

    def __exit__(self, *args):
        for name, module in self.saved.items():
            if module is not None:
                sys.modules[name] = module


class Phone(phone.SelfieMixin):
    """Her phone, with the parts that read the clock or the disk kept still."""

    def __init__(self):
        self.enabled = True
        self.config = {'photo_enabled': True, 'screenshot_enabled': True, 'say_aloud_enabled': True}
        self.browse_enabled = True
        self.context_calls = 0

    def _browse_on(self):
        return self.enabled and self.browse_enabled

    def _phone_context(self, event):
        self.context_calls += 1
        return '虚构的近况。'

    def _window_replies(self, event, n=6):
        return [{'text': '刚才说的话%d' % i} for i in (1, 2, 3)][-n:]

    def _now_line(self, event):
        return '此刻：在家，正在看书。'


class Browser(mixin_browse.BrowseMixin):
    """Her browser with a stand-in ledger, so no money file is made."""

    def __init__(self, on=True, money=True):
        self.enabled = True
        self.browse_enabled = on
        self.config = {}
        self.money = money

    def _browse_ledger(self):
        return types.SimpleNamespace(money_left=lambda: self.money)


class PhoneTools(unittest.TestCase):
    def setUp(self):
        self.p = Phone()
        self.event = harness.FakeEvent('虚构消息', sender='10005', name='小甲')

    def _both_routes(self, config):
        self.p.config = config
        neutral = self.p._phone_tools(self.event)
        req = ProviderRequest()
        with FakeAstrBotTools():
            self.p._give_phone_tools(req, self.event)
        return neutral, req.func_tool.tools

    def test_both_routes_make_the_same_tools(self):
        switches = (({'photo_enabled': True, 'screenshot_enabled': True, 'say_aloud_enabled': True},
                     ['set_now', 'take_photo', 'share_screenshot', 'say_aloud']),
                    ({}, ['set_now']),
                    ({'say_aloud_enabled': True}, ['set_now', 'say_aloud']))
        for config, expected in switches:
            neutral, placed = self._both_routes(config)
            self.assertEqual([tool.name for tool in neutral], expected, config)
            self.assertEqual([tool.name for tool in placed], expected, config)
            for one, other in zip(neutral, placed):
                self.assertIsInstance(one, turn.TurnTool)
                self.assertIsInstance(other, FunctionTool)
                self.assertEqual(one.name, other.name)
                self.assertEqual(one.description, other.description)
                self.assertEqual(one.parameters, other.parameters)
                self.assertEqual(one.handler, other.handler)

    def test_switched_off_no_tools_and_no_tool_set(self):
        self.p.enabled = False
        self.assertEqual(self.p._phone_tools(self.event), [])
        req = ProviderRequest()
        with FakeAstrBotTools():
            self.p._give_phone_tools(req, self.event)
        self.assertFalse(hasattr(req, 'func_tool'))

    def test_missing_tool_classes_warned_before_the_tools_are_made(self):
        with NoAstrBotTools():
            self.assertFalse(adapter_astrbot_tools.available())
            req = ProviderRequest()
            with patch.object(phone.logger, 'warning') as log:
                self.p._give_phone_tools(req, self.event)
            self.assertTrue(any('[ams-life] phone tools unavailable' in str(call) for call in log.call_args_list))
            self.assertEqual(self.p.context_calls, 0)
            self.assertFalse(hasattr(req, 'func_tool'))

    def test_missing_tool_classes_no_browse_tools_no_quota_no_addresses(self):
        event = harness.FakeEvent('小爱 看看 https://example.invalid/page', sender='10005', name='小甲')
        with NoAstrBotTools():
            self.assertFalse(adapter_astrbot_tools.available())
            self.assertFalse(Browser()._give_browse_tools(ProviderRequest(), event))
            self.assertIsNone(getattr(event, mixin_browse.QUOTA_ATTR, None))
            self.assertEqual(getattr(event, mixin_browse.URLS_ATTR, set()), set())


class BrowseTools(unittest.TestCase):
    URL = 'https://example.invalid/page'

    def event(self):
        return harness.FakeEvent('小爱 看看 ' + self.URL, sender='10005', name='小甲')

    def test_off_or_no_money_no_tools_and_no_quota(self):
        for on, money in ((False, True), (True, False)):
            event = self.event()
            self.assertEqual(Browser(on=on, money=money)._browse_tools(event), [], (on, money))
            self.assertIsNone(getattr(event, mixin_browse.QUOTA_ATTR, None), (on, money))
            self.assertEqual(getattr(event, mixin_browse.URLS_ATTR, set()), set(), (on, money))

    def test_on_gives_search_and_read_and_keeps_the_messages_addresses(self):
        browser, event = Browser(), self.event()
        tools = browser._browse_tools(event)
        self.assertEqual([tool.name for tool in tools], [browse.SEARCH_TOOL, browse.READ_TOOL])
        self.assertTrue(all(isinstance(tool, turn.TurnTool) for tool in tools))
        self.assertEqual(tools[0].handler, browser._tool_search)
        self.assertEqual(tools[1].handler, browser._tool_read)
        self.assertIsNotNone(getattr(event, mixin_browse.QUOTA_ATTR, None))
        self.assertEqual(browser._browse_urls(event), {self.URL})


class Settings(unittest.TestCase):
    def settings(self, allowed):
        stub = mixin_settings.SettingsMixin()
        stub.config = {} if allowed is None else {'allowed_tools': allowed}
        return stub

    def test_allowed_tools_as_list_as_text_and_empty(self):
        self.assertEqual(self.settings(['kept'])._tools_not_allowed(['a', 'kept', 'b']), ['a', 'b'])
        self.assertEqual(self.settings('kept\n  other  \n')._tools_not_allowed(['x', 'kept', 'other']), ['x'])
        self.assertEqual(self.settings([])._tools_not_allowed(['a', 'b']), ['a', 'b'])
        self.assertEqual(self.settings(None)._tools_not_allowed(['a']), ['a'])
        self.assertEqual(self.settings(['kept'])._tools_not_allowed([]), [])

    def test_turn_request_keeps_order_and_logs_one_line(self):
        stub = self.settings(['kept'])
        request = turn.TurnRequest(tools=[turn.TurnTool('future_task', '', {}), turn.TurnTool('kept', '', {}),
                                          turn.TurnTool('send_message_to_user', '', {})])
        with patch.object(mixin_settings.logger, 'info') as log:
            gone = stub._turn_tools_off(request)
        self.assertEqual(gone, ['future_task', 'send_message_to_user'])
        self.assertEqual(request.tool_names(), ['kept'])
        log.assert_called_once_with("[ams-life] tools taken out of the reply: %s", 'future_task, send_message_to_user')

    def test_turn_request_nothing_to_take_out_no_line(self):
        stub = self.settings(['kept'])
        request = turn.TurnRequest(tools=[turn.TurnTool('kept', '', {})])
        with patch.object(mixin_settings.logger, 'info') as log:
            self.assertEqual(stub._turn_tools_off(request), [])
        log.assert_not_called()
        self.assertEqual(request.tool_names(), ['kept'])


class NeutralCode(unittest.TestCase):
    def test_the_four_methods_do_not_name_astrbot(self):
        targets = (('_phone_tools', phone.__file__), ('_browse_tools', mixin_browse.__file__),
                   ('_tools_not_allowed', mixin_settings.__file__), ('_turn_tools_off', mixin_settings.__file__))
        for name, path in targets:
            source = Path(path).read_text(encoding='utf-8')
            found = next(node for node in ast.walk(ast.parse(source))
                         if isinstance(node, ast.FunctionDef) and node.name == name)
            body = ast.get_source_segment(source, found)
            for word in ('astrbot', 'FunctionTool', 'ToolSet'):
                self.assertNotIn(word, body, name)


if __name__ == '__main__':
    unittest.main()
