# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Compare tool preparation with the frozen AstrBot route."""
import inspect
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import adapter_astrbot_tools
import adapter_astrbot_turn
import main
import mixin_turn
import turn


class FunctionTool:
    def __init__(self, name, description='', parameters=None, handler=None, active=True):
        self.name, self.description, self.parameters = name, description, parameters
        self.handler, self.active = handler, active


class ToolSet:
    def __init__(self, tools=None):
        self.tools = list(tools or [])

    def names(self):
        return [tool.name for tool in self.tools]

    def add_tool(self, tool):
        for index, existing in enumerate(self.tools):
            if existing.name == tool.name:
                if tool.active or not existing.active:
                    self.tools[index] = tool
                return
        self.tools.append(tool)

    def remove_tool(self, name):
        self.tools = [tool for tool in self.tools if tool.name != name]

    def __bool__(self):
        return bool(self.tools)


class FakeAstrBotTools:
    names = ('astrbot.core', 'astrbot.core.agent', 'astrbot.core.agent.tool')

    def __enter__(self):
        self.saved = {name: sys.modules.get(name) for name in self.names}
        for name in self.names:
            sys.modules[name] = types.ModuleType(name)
        sys.modules[self.names[-1]].FunctionTool = FunctionTool
        sys.modules[self.names[-1]].ToolSet = ToolSet

    def __exit__(self, *args):
        for name, module in self.saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


# main.py 629-652 at 8f124ea.
async def old_tools(self, event, req):
    try:
        self._reply_tools_off(req)
    except Exception as exc:
        req.func_tool = None
        main.logger.warning("[ams-life] reply tools could not be taken out, none given: %s", exc)
    else:
        try:
            _tools = getattr(req, "func_tool", None)
            if _tools:
                for _name in ("take_photo", "share_screenshot", "say_aloud", "set_now"):
                    if _name in _tools.names():
                        _tools.remove_tool(_name)
                if not _tools:
                    req.func_tool = None
            if self.enabled:
                await self._ensure_profile(event)
            self._give_phone_tools(req, event)
        except Exception as exc:
            req.func_tool = None
            main.logger.warning("[ams-life] phone tools unavailable: %s", type(exc).__name__)
        try:
            self._give_browse_tools(req, event)
        except Exception as exc:
            main.logger.warning("[ams-life] browse: tools not given (%s)", type(exc).__name__)


class Plugin(main.BioCorePlugin):
    def __init__(self, enabled=True, switches=(), browse=False, money=True, allowed=(), failure=None):
        self.enabled, self.config = enabled, {'allowed_tools': list(allowed)}
        self.switches, self.browse, self.money, self.failure = switches, browse, money, failure
        self.phone_calls = 0

    async def _ensure_profile(self, event):
        pass

    def _turn_tools_off(self, request):
        if self.failure == 'filter':
            raise ValueError('filter')
        return super()._turn_tools_off(request)

    def _reply_tools_off(self, req):
        if self.failure == 'filter':
            raise ValueError('filter')
        return super()._reply_tools_off(req)

    def _phone_tools(self, event):
        self.phone_calls += 1
        if self.failure == 'phone':
            raise ValueError('phone')
        return [turn.TurnTool(name, 'phone ' + name, {'name': name}) for name in ('set_now', *self.switches)]

    def _browse_on(self):
        return self.browse

    def _browse_ledger(self):
        return types.SimpleNamespace(money_left=lambda: self.money)

    def _browse_tools(self, event):
        return [turn.TurnTool(name, 'browse ' + name, {'name': name}) for name in ('search', 'read')]


def request(names):
    tools = [FunctionTool(name, 'native ' + name, {'name': name}) for name in names]
    return types.SimpleNamespace(func_tool=ToolSet(tools) if names else None)


def table(req):
    if req.func_tool is None:
        return None
    return [(t.name, t.description, t.parameters) for t in req.func_tool.tools]


class PrepareTools(unittest.IsolatedAsyncioTestCase):
    async def test_hook_tool_read_error_gives_none(self):
        class BrokenRead:
            @property
            def tools(self):
                raise RuntimeError('made-up failure')

        plugin = Plugin()
        plugin._ignored_sender = lambda event: False
        plugin._group_reply_open = lambda event: None
        plugin._prepare_turn = AsyncMock()
        event = types.SimpleNamespace()
        req = types.SimpleNamespace(func_tool=BrokenRead())
        with patch.object(main.logger, 'warning') as log:
            await plugin.on_llm_request(event, req)
        self.assertIsNone(req.func_tool)
        self.assertEqual(plugin.phone_calls, 0)
        plugin._prepare_turn.assert_awaited_once()
        log.assert_called_once()
        self.assertEqual(log.call_args.args[0],
                         '[ams-life] reply tools could not be taken out, none given: %s')

    async def test_hook_tool_write_error_gives_none(self):
        class BrokenWrite(ToolSet):
            @property
            def tools(self):
                return self._tools

            @tools.setter
            def tools(self, value):
                if hasattr(self, '_tools'):
                    raise RuntimeError('made-up failure')
                self._tools = value

        plugin = Plugin(allowed=('kept',))
        plugin._ignored_sender = lambda event: False
        plugin._group_reply_open = lambda event: None
        plugin._prepare_turn = AsyncMock()
        event = types.SimpleNamespace()
        req = types.SimpleNamespace(func_tool=BrokenWrite([FunctionTool('kept')]))
        with FakeAstrBotTools(), patch.object(main.logger, 'warning') as log:
            await plugin.on_llm_request(event, req)
        self.assertIsNone(req.func_tool)
        log.assert_called_once()
        self.assertEqual(log.call_args.args[0],
                         '[ams-life] reply tools could not be taken out, none given: %s')

    async def test_matches_frozen_and_direct_turn(self):
        cases = [
            ({}, ()), ({}, ('native',)), ({'allowed': ('kept',)}, ('removed', 'kept')),
            ({'allowed': ('take_photo',)}, ('take_photo',)),
            ({'enabled': False, 'allowed': ('kept',)}, ('kept',)),
            ({'switches': ('take_photo', 'share_screenshot', 'say_aloud')}, ()),
            ({'switches': ('say_aloud',)}, ()),
            ({'browse': True}, ()), ({'browse': True, 'money': False}, ()),
            ({'browse': True, 'failure': 'filter'}, ('native',)),
            ({'browse': True, 'failure': 'phone'}, ('native',)),
        ]
        with FakeAstrBotTools():
            for options, names in cases:
                for build in (False, True):
                    with self.subTest(options=options, names=names, build=build):
                        plugin, event = Plugin(**options), object()
                        old, new = request(names), request(names)
                        with patch.object(adapter_astrbot_tools, 'available', return_value=build):
                            with patch.object(mixin_turn.logger, 'warning') as log:
                                await old_tools(plugin, event, old)
                                plugin.phone_calls = 0
                                neutral = adapter_astrbot_turn.request_from_astrbot(new)
                                await plugin._prepare_tools(event, neutral, build=build)
                                if not build:
                                    self.assertEqual(plugin.phone_calls, 0)
                                    if plugin.enabled and plugin.failure != 'filter':
                                        self.assertTrue(any('[ams-life] phone tools unavailable' in str(c)
                                                            for c in log.call_args_list))
                                adapter_astrbot_turn.request_into_astrbot(neutral, new)
                        self.assertEqual(table(old), table(new))
                        direct = adapter_astrbot_turn.request_from_astrbot(request(names))
                        await plugin._prepare_tools(event, direct, build=build)
                        self.assertEqual(direct.tool_names(), [] if table(old) is None else [t[0] for t in table(old)])

    async def test_existing_toolset_is_preserved(self):
        with FakeAstrBotTools():
            req = request(('kept', 'removed'))
            original = req.func_tool
            neutral = adapter_astrbot_turn.request_from_astrbot(req)
            await Plugin(allowed=('kept',))._prepare_tools(object(), neutral)
            adapter_astrbot_turn.request_into_astrbot(neutral, req)
            self.assertIs(req.func_tool, original)

    async def test_unchanged_toolset_and_list_are_preserved(self):
        req = request(('kept',))
        original, tools = req.func_tool, req.func_tool.tools
        neutral = adapter_astrbot_turn.request_from_astrbot(req)
        await Plugin(enabled=False, allowed=('kept',))._prepare_tools(object(), neutral)
        adapter_astrbot_turn.request_into_astrbot(neutral, req)
        self.assertIs(req.func_tool, original)
        self.assertIs(req.func_tool.tools, tools)

    def test_hook_uses_neutral_preparation(self):
        source = inspect.getsource(main.BioCorePlugin.on_llm_request)
        for name in ('_give_phone_tools', '_give_browse_tools', '_reply_tools_off'):
            self.assertNotIn(name, source)
