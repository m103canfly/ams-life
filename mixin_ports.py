# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The plugin's entry points to its ports."""
try:
    from . import adapter_astrbot, adapter_astrbot_messenger, adapter_astrbot_model, discretion
except ImportError:
    import adapter_astrbot
    import adapter_astrbot_messenger
    import adapter_astrbot_model
    import discretion


class PortsMixin:
    """Where the plugin gets its ports: today over AstrBot, later over our own layers."""

    def _umo_of(self, place, event=None) -> str:
        """The event's session for its place, else the window's session, else empty."""
        if not place:
            return ""
        if event is not None:
            umo = getattr(event, "unified_msg_origin", "")
            if discretion.place_of(umo) == place:
                return umo
        try:
            return str(self._read_window(place).get("umo") or "")
        except Exception:
            return ""

    def _messenger(self, event=None):
        """A messenger for this event and the plugin's context."""
        return adapter_astrbot_messenger.AstrBotMessenger(
            self.context, lambda place: self._umo_of(place, event), lambda: getattr(event, "bot", None))

    def _model(self, provider):
        """A model client over this provider."""
        return adapter_astrbot_model.AstrBotModel(provider)

    def _incoming(self, event):
        """The incoming message represented by this event."""
        return adapter_astrbot.from_astrbot(event)
