# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The plugin's entry points to its ports."""
try:
    from . import adapter_astrbot, adapter_astrbot_messenger, adapter_astrbot_model, adapter_astrbot_turn, discretion, model_client
except ImportError:
    import adapter_astrbot
    import adapter_astrbot_messenger
    import adapter_astrbot_model
    import adapter_astrbot_turn
    import discretion
    import model_client


def model_for(provider):
    """A model client over this provider: one already (ours, e.g. DeepSeekModel), as it is."""
    if isinstance(provider, model_client.ModelClient):
        return provider
    return adapter_astrbot_model.AstrBotModel(provider)


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

    def _messenger(self, event=None, *, as_event=False):
        """A messenger for this event and the plugin's context."""
        neutral = getattr(self, "_neutral_messenger", None)
        if neutral is not None:   # the new program's OneBot messenger (5e-5): it sends by place
            return neutral
        send = getattr(event, "send", None)
        kwargs = {}
        if as_event and callable(send):
            kwargs = {"event_send": send, "event_place": discretion.place_of(getattr(event, "unified_msg_origin", "") or "")}
        return adapter_astrbot_messenger.AstrBotMessenger(
            getattr(self, "context", None), lambda place: self._umo_of(place, event), lambda: getattr(event, "bot", None), **kwargs)

    def _model(self, provider):
        """A model client over this provider."""
        return model_for(provider)

    def _incoming(self, event):
        """The incoming message represented by this event."""
        return adapter_astrbot_turn.incoming_of(event)
