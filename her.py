# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The plugin's shared behavior without the AstrBot base class."""
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
    from .mixin_phone import PhoneMixin
except ImportError:
    from mixin_phone import PhoneMixin
try:
    from .mixin_send_check import SendCheckMixin
except ImportError:
    from mixin_send_check import SendCheckMixin
try:
    from .mixin_attention import AttentionMixin
except ImportError:
    from mixin_attention import AttentionMixin
try:
    from .mixin_browse import BrowseMixin
except ImportError:
    from mixin_browse import BrowseMixin
try:
    from .mixin_stickers import StickersMixin
except ImportError:
    from mixin_stickers import StickersMixin
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
except ImportError:
    from mixin_turn import TurnMixin

try:
    from .mixin_core import CoreMixin
except ImportError:
    from mixin_core import CoreMixin


class Her(LLMMixin, AutonomyMixin, SettingsMixin, MediaMixin, PeopleMixin, ImpressionsMixin, DigestMixin, EventsMixin, BrainMixin, PagesMixin, MemoryMixin, DiscretionMixin, PhoneMixin, SendCheckMixin, AttentionMixin, GroupBrowseMixin, StickersMixin, BrowseMixin, SelfieMixin, SlangMixin, TurnMixin, PortsMixin, CoreMixin):
    """The same startup and turn steps without AstrBot hooks."""

    def __init__(self, context, config=None):
        self._core_init(context, config)
