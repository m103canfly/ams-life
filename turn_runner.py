# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Run one turn using her neutral model, tools, history and messenger."""
import logging

try:
    from . import turn, messenger, model_client, tool_loop, adapter_astrbot_turn
except ImportError:
    import turn
    import messenger
    import model_client
    import tool_loop
    import adapter_astrbot_turn


logger = logging.getLogger(__name__)


def messages_of(turn_request):
    """(system, messages) for the model: the history, then the person's line with the plugin's text blocks."""
    parts = [turn_request.prompt]
    parts.extend(part.get('text', '') for part in turn_request.extra_user_content_parts or []
                 if isinstance(part, dict) and part.get('type') == 'text')
    messages = list(turn_request.contexts)
    messages.append({'role': 'user', 'content': '\n\n'.join(parts)})
    return turn_request.system_prompt or None, messages


def loop_tools_of(turn_request, event):
    """Her tools for the tool loop; each handler gets this event first, and None becomes ""."""
    entries = []
    for item in turn_request.tools:
        if item.handler is None:
            continue

        def wrap(handler):
            async def run(**args):
                result = await handler(event, **args)
                return '' if result is None else str(result)
            return run

        entries.append(tool_loop.LoopTool(model_client.Tool(item.name, item.description,
                                                            item.parameters), wrap(item.handler)))
    return entries


def reply_of(result):
    """The tool loop's result as her reply (no quote prefix in the new program yet)."""
    return turn.TurnReply(text=result.text, tool_calls=tuple(result.calls), usage=dict(result.usage))


async def run_turn(her, event, *, history_limit=20, max_rounds=tool_loop.MAX_ROUNDS):
    """One turn in the new program, in the order AstrBot's pipeline goes; None when she does not answer."""
    await her._on_message(event)
    if event.is_stopped():
        return None
    if await her._decide_turn(event) != 'reply':
        return None
    if her._ignored_sender(event):
        event.stop_event()
        return None
    if her.enabled:
        her._group_reply_open(event)
    history = getattr(her, '_history', None)
    contexts = history.recent(her._here(event), history_limit) if history is not None else []
    request = turn.TurnRequest(prompt=adapter_astrbot_turn.incoming_of(event).text,
                               system_prompt=str(getattr(her, '_neutral_persona', '') or ''),
                               contexts=contexts,
                               image_urls=[], extra_user_content_parts=[], tools=[])
    await her._prepare_tools(event, request)
    if her.enabled:
        await her._prepare_turn(event, request)
    system, messages = messages_of(request)
    result = await tool_loop.run(her._neutral_model, system=system, messages=messages,
                                 tools=loop_tools_of(request, event), max_rounds=max_rounds)
    reply = reply_of(result)
    await her._after_reply(event, reply)
    her._group_reply_after(event)
    sent = False
    if not event.is_stopped() and (reply.first_message or reply.text):
        try:
            result = await her._messenger(event).send(her._here(event),
                                                       reply.first_message or messenger.text_segments(reply.text))
            sent = bool(result.ok)
        except Exception as exc:
            logger.warning('[ams-life] first message send failed: %s', type(exc).__name__)
    her._keep_turn(event, request, reply)
    if sent:
        her._keep_likeness(event, reply)
    return reply
