# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""AstrBot BioCore plugin: a standalone biological emotion layer.

Independent copy. It does not import the Desktop companion project.
First run: read the current AstrBot persona, compile it once with the current
provider into a numeric profile, store it under this plugin's data dir.
Then on every LLM request: append a compact intent, on response: feedback.

Noise -> autonomy boundary (task-15): proactive_autonomy/proactive_send default
false. When off, readiness is not computed, no background task starts, no message
is sent, and the legacy noise/state trajectory is unchanged. All readiness math
lives in the L1 BioCore (autonomy_state); the plugin only feeds raw module deltas
and reads the resulting state for the command/UI. Group chats never trigger.
"""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403
try:
    from .mixin_llm import LLMMixin
except ImportError:
    from mixin_llm import LLMMixin
try:
    from .mixin_autonomy import AutonomyMixin
except ImportError:
    from mixin_autonomy import AutonomyMixin
try:
    from .mixin_settings import SettingsMixin
except ImportError:
    from mixin_settings import SettingsMixin
try:
    from .mixin_media import MediaMixin
except ImportError:
    from mixin_media import MediaMixin
try:
    from .mixin_people import PeopleMixin
except ImportError:
    from mixin_people import PeopleMixin
try:
    from .mixin_impressions import ImpressionsMixin
    from .mixin_digest import DigestMixin
except ImportError:
    from mixin_impressions import ImpressionsMixin
    from mixin_digest import DigestMixin
try:
    from .mixin_events import EventsMixin
except ImportError:
    from mixin_events import EventsMixin
try:
    from .mixin_brain import BrainMixin
except ImportError:
    from mixin_brain import BrainMixin
try:
    from .mixin_pages import PagesMixin
except ImportError:
    from mixin_pages import PagesMixin
try:
    from .mixin_memory import MemoryMixin
except ImportError:
    from mixin_memory import MemoryMixin
try:
    from .mixin_discretion import DiscretionMixin
except ImportError:
    from mixin_discretion import DiscretionMixin
try:
    from .mixin_phone import PhoneMixin, _phone_line, _history_original, _expand_forward
except ImportError:
    from mixin_phone import PhoneMixin, _phone_line, _history_original, _expand_forward
try:
    from .mixin_send_check import SendCheckMixin
except ImportError:
    from mixin_send_check import SendCheckMixin
try:
    from .mixin_attention import AttentionMixin
    from . import attention
except ImportError:
    from mixin_attention import AttentionMixin
    import attention
try:
    from .mixin_browse import BrowseMixin
except ImportError:
    from mixin_browse import BrowseMixin
try:
    from .mixin_stickers import StickersMixin
    from . import stickers
except ImportError:
    from mixin_stickers import StickersMixin
    import stickers
try:
    from .mixin_group_browse import GroupBrowseMixin
except ImportError:
    from mixin_group_browse import GroupBrowseMixin
try:
    from .mixin_selfie import SelfieMixin
except ImportError:
    from mixin_selfie import SelfieMixin
try:
    from .mixin_slang import SlangMixin
except ImportError:
    from mixin_slang import SlangMixin
try:
    from .mixin_ports import PortsMixin
except ImportError:
    from mixin_ports import PortsMixin
try:
    from .mixin_turn import TurnMixin
    from . import adapter_astrbot_tools, adapter_astrbot_turn
except ImportError:
    from mixin_turn import TurnMixin
    import adapter_astrbot_tools
    import adapter_astrbot_turn


try:
    from .mixin_core import CoreMixin
except ImportError:
    from mixin_core import CoreMixin



@register("astrbot_plugin_ams_life", "m103canfly", "ams-life：小爱的生命层（基于 BioCore）", "0.1.0")
class BioCorePlugin(LLMMixin, AutonomyMixin, SettingsMixin, MediaMixin, PeopleMixin, ImpressionsMixin, DigestMixin, EventsMixin, BrainMixin, PagesMixin, MemoryMixin, DiscretionMixin, PhoneMixin, SendCheckMixin, AttentionMixin, GroupBrowseMixin, StickersMixin, BrowseMixin, SelfieMixin, SlangMixin, TurnMixin, PortsMixin, CoreMixin, Star):
    def __init__(self, context: Context, config=None):
        super().__init__(context)
        self._core_init(context, config)

    # ams-life: BioCore's /biocore command (readiness, learning, learning reset) is gone:
    # anyone in any chat could reset what she learned or have her inner numbers posted.

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        """AstrBot's hook for every message: her phone (TurnMixin._on_message)."""
        await self._on_message(event)

    @filter.event_message_type(filter.EventMessageType.ALL, priority=-5)
    async def on_message_decide(self, event: AstrMessageEvent):
        """AstrBot's hook after on_message: when she answers, AstrBot is asked for the reply."""
        if await self._decide_turn(event) != "reply":
            return
        try:
            request = await self._ask_for_reply(event)
        except Exception as exc:   # as before: asking failing is the decision failing
            logger.warning("[ams-life] attention: the decision failed (%s)", type(exc).__name__)
            return
        if request is not None:
            yield request

    async def terminate(self):
        """AstrBot calls this when the plugin is unloaded or reloaded: stop the 5-minute loop
        (it now runs whenever the plugin is on)."""
        task = getattr(self, "_autonomy_task", None)
        if task is not None and not task.done():
            task.cancel()

    # after every other plugin's (AstrBot's own is priority 0): the tools are taken out
    # last, and the numbers come out of the group context lines it adds (step 2)
    @filter.on_llm_request(priority=-10)
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        if self._ignored_sender(event):   # on_message stopped it already; should it get this far
            event.stop_event()
            return
        if self.enabled:
            self._group_reply_open(event)
        try:
            turn_request = adapter_astrbot_turn.request_from_astrbot(req)
        except Exception as exc:   # failing, she gets none rather than all of them (PR #27)
            req.func_tool = None
            logger.warning("[ams-life] reply tools could not be taken out, none given: %s", exc)
            turn_request = adapter_astrbot_turn.request_from_astrbot(req)
            prepare_tools = False
        else:
            prepare_tools = True
        try:
            if prepare_tools:
                await self._prepare_tools(event, turn_request, build=adapter_astrbot_tools.available())
            if self.enabled:
                await self._prepare_turn(event, turn_request)
        finally:
            adapter_astrbot_turn.request_into_astrbot(turn_request, req, tools=False)
            try:
                adapter_astrbot_turn.tools_into_astrbot(turn_request, req)
            except Exception as exc:   # failing, she gets none rather than all of them (PR #27)
                req.func_tool = None
                logger.warning("[ams-life] reply tools could not be taken out, none given: %s", exc)
            # Asking once more uses AstrBot's request, after it prepares the images.
            note = getattr(event, "_ams_check", None)
            if isinstance(note, dict) and note.get("req") is turn_request:
                note["req"] = req

    @filter.on_agent_done()
    async def on_agent_done(self, event: AstrMessageEvent, run_context, response: LLMResponse):
        """Step 2 (global_memory): AstrBot saves this turn after this hook (4.29.3,
        internal.py _save_to_history, from run_context.messages): make it hold what was sent
        -- the words said once more, not the first ones -- and none of the model's thinking."""
        if self.enabled:
            if (getattr(self, "global_memory", False) or getattr(event, "_ams_sticker_sent", False)
                    or getattr(event, "_ams_reply_was_split", False)):
                self._settle_history(event, run_context)

    @filter.on_llm_response()
    async def on_llm_response(self, event: AstrMessageEvent, response: LLMResponse):
        await self._after_reply(event, adapter_astrbot_turn.reply_handle(response))
        self._group_reply_after(event)
