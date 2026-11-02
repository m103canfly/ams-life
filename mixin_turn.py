# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""One platform-neutral turn: getting it ready, and her reply after the model."""
import unicodedata
from datetime import datetime

try:
    from .common import *  # noqa: F401,F403
    from .body import *  # noqa: F401,F403
    from .mixin_phone import _expand_forward, _phone_line, _history_original
    from . import adapter_astrbot_turn, attention, stickers, likeness, mixin_selfie, weather, calendar_cn
except ImportError:
    from common import *  # noqa: F401,F403
    from body import *  # noqa: F401,F403
    from mixin_phone import _expand_forward, _phone_line, _history_original
    import adapter_astrbot_turn
    import attention
    import stickers
    import likeness
    import mixin_selfie
    import weather
    import calendar_cn


def _copies_owner_rule(reply, rules):
    """Find twelve consecutive characters after removing whitespace and punctuation."""
    def clean(text):
        return "".join(c for c in str(text or "")
                       if not c.isspace() and not unicodedata.category(c).startswith("P"))

    if not rules:
        return False
    words = clean(reply)
    for rule in rules:
        text = clean(rule)
        if any(text[i:i + 12] in words for i in range(len(text) - 11)):
            return True
    return False


def _one_line_history(contexts):
    """Join assistant history while preserving code and list blocks."""
    for message in contexts or []:
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        content = message.get("content")
        if isinstance(content, str):
            message["content"] = " ".join(attention.split(content, most=10**6))
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    part["text"] = " ".join(attention.split(part["text"], most=10**6))


def _has_non_sticker_image(event):
    """Whether this message or its quote contains an image other than a QQ sticker."""
    segments = adapter_astrbot_turn.incoming_of(event).segments
    def is_image(segment):
        return segment.type == "image" and not stickers.stickers_in_segments((segment,))

    return any(is_image(segment) or
               (segment.type == "reply" and any(is_image(child) for child in
                                                 (segment.data.get("chain") or ())))
               for segment in segments)


class TurnMixin:
    """Getting one turn ready: what she knows, feels and recalls, put into the request.
    Works on turn.TurnRequest only; AstrBot's hook converts to it and back (main.py).
    The reply works through a reply handle only."""

    async def _prepare_tools(self, event, turn_request, build=True) -> None:
        """Her reply's tools, on a turn.TurnRequest: none of the platform's but those allowed,
        then her phone's tools and her browser's. build=False: the platform cannot make tools
        now (AstrBot's tool classes cannot be imported), so hers are not made."""
        try:   # no tools in her reply, whatever else is on (the owner, 10-29)
            self._turn_tools_off(turn_request)
        except Exception as exc:   # failing, she gets none rather than all of them
            turn_request.tools[:] = []
            logger.warning("[ams-life] reply tools could not be taken out, none given: %s", exc)
        else:
            try:
                for name in ("take_photo", "share_screenshot", "say_aloud", "set_now", "set_look"):
                    turn_request.remove_tool(name)
                if self.enabled:
                    await self._ensure_profile(event)
                    if not build:
                        logger.warning("[ams-life] phone tools unavailable")
                    else:
                        for tool in self._phone_tools(event):
                            turn_request.add_tool(tool)
            except Exception as exc:
                turn_request.tools[:] = []
                logger.warning("[ams-life] phone tools unavailable: %s", type(exc).__name__)
            try:   # step 2 (丁): then her browser's two tools, only those (browse_enabled)
                if self._browse_on() and self._browse_ledger().money_left() and build:
                    for tool in self._browse_tools(event):
                        turn_request.add_tool(tool)
            except Exception as exc:
                logger.warning("[ams-life] browse: tools not given (%s)", type(exc).__name__)

    async def _on_message(self, event):
        """ams-life: her phone. Every message that reaches the plugin goes into its own
        chat window, whether it wakes her or not. Ignored senders and unapproved private
        messages are stopped before storage; other groups are stored before the speaking gate.
        (AstrBot stops an event whose handler raises, so nothing may escape here.)"""
        if not self._private_allowed(event):
            logger.info("[ams-life] 别人的私聊，没收")
            event.stop_event()
            return
        if self._ignored_sender(event):
            logger.info("[ams-life] a message from a sender on ignore_senders: not answered, not kept")
            event.stop_event()
            return
        if not self.enabled:
            if not self._may_speak_in(self._here(event)):
                event.stop_event()
            return
        try:
            self._begin_job(self._here(event))
            self._check_registry(event)  # someone (or a message) she may not keep: nothing is stored
            self._window_add_message(event)
            self._listen_body(event)
            if getattr(self, "mood_events_enabled", False):
                self._mood_clock()
                _sid = str(self._speaker(event)[0] or "")
                _self_id = adapter_astrbot_turn.incoming_of(event).self_id
                if not (_self_id and _sid == _self_id):
                    _why = self._why_called(event)
                    setattr(event, "_mood_direct", bool(_why))
                    _core = self._core(None)
                    for _kind in mood_kinds(adapter_astrbot_turn.incoming_of(event).text, bool(_why)):
                        _familiar = self._familiarity(_sid)
                        _weight = (.6 + .4 * _familiar) if _kind == "criticism" else 1.0
                        if not _why and _familiar < .3:
                            _weight *= MOOD_BYSTANDER_WEIGHT
                        _core.mood_event(_kind, _weight)
                    if self._mood_note_answer(event, _why):
                        _core.mood_event("answered")
                    if not getattr(self, "self_decide", False) and not _why:
                        self._hear_mood(event)
            self._ensure_autonomy_task()  # the 5-minute loop also sweeps her phone
            self._group_heard(event)
            self._sticker_in_passing(event)  # queue an uncalled QQ sticker for a later opening
        except Exception as exc:
            logger.warning("[ams-life] window store failed (%s)", type(exc).__name__)
        finally:
            if not self._message_may_speak(event):
                event.stop_event()

    async def _decide_turn(self, event):
        """Step 2 (甲, self_decide): after _on_message has kept the message, whether she answers it:
        "reply" or None. The platform asks for the reply itself (AstrBot: _ask_for_reply)."""
        if not self.enabled or not getattr(self, "self_decide", False) or self._ignored_sender(event):
            return None
        if not self._private_allowed(event) or not self._message_may_speak(event):
            event.stop_event()
            return None
        try:
            return await self._decision(event)
        except Exception as exc:   # the decision failing: as before, AstrBot decides
            logger.warning("[ams-life] attention: the decision failed (%s)", type(exc).__name__)
            return None

    async def _prepare_turn(self, event, turn_request) -> None:
        _forward = await _expand_forward(self, event)
        _sid, _name = self._speaker(event)
        _stamp = getattr(getattr(event, "message_obj", None), "timestamp", None) or time.time()
        _plain_prompt = str(getattr(turn_request, "prompt", "") or "")
        _plain_history = next((item.get("content") for item in reversed(getattr(turn_request, "contexts", []) or [])
                               if isinstance(item, dict) and item.get("role") == "user"
                               and isinstance(item.get("content"), str)), "")
        _incoming = str(getattr(turn_request, "prompt", "") or self._message_text(event))
        if _forward:
            _incoming += "\n" + _forward
        turn_request.prompt = self._for_model(_phone_line(self, event, {
            "ts": _stamp, "role": "user", "sender_id": _sid,
            "sender_name": _name, "text": _incoming}), event)
        for _message in getattr(turn_request, "contexts", None) or []:
            if not isinstance(_message, dict) or _message.get("role") != "user":
                continue
            _content = _message.get("content")
            if isinstance(_content, str):
                _message["content"] = _history_original(_content)
            elif isinstance(_content, list):
                for _part in _content:
                    if isinstance(_part, dict) and isinstance(_part.get("text"), str):
                        _part["text"] = _history_original(_part["text"])
        if bool(self.config.get("history_one_line", True)):
            _one_line_history(getattr(turn_request, "contexts", None))
        self._numbers_out_of_request(turn_request, event)
        if not self.inject_intent:
            _now = self._now_line(event)
            _day = calendar_cn.today_line(datetime.now().date())
            if _day:
                _now = (_now + "\n[日子] " + _day).strip()
            _our_days = mixin_selfie._our_days_line(self, event, datetime.now().date())
            if _our_days:
                _now = (_now + "\n" + _our_days).strip()
            if _now:
                # The system prompt is not stored in AstrBot's conversation history.
                turn_request.system_prompt = (str(getattr(turn_request, "system_prompt", "") or "") + "\n\n" + _now).strip()
            return
        # the mark on_message set when the message came in: AstrBot may hold the message
        # for the session lock (the previous one still waiting for the model) before this
        self._continue_job(self._here(event))
        self._check_registry(event)
        await self._ensure_profile(event)
        core = self._core(event)
        # ams-life: how lively the chats are. That she was called (woken) was counted as
        # being seen when the message came in (on_message), once.
        try:
            core.set_ambient(self._ambient_level())
        except Exception:
            pass
        # A4: capture open loops from *before* this turn so the continuity
        # opener cannot echo a loop created by the current message.
        _prior_open_loops = [dict(x) for x in self._window_loops(event)]
        text = adapter_astrbot_turn.incoming_of(event).text.strip()
        if not text:
            text = _plain_prompt
        if not text:
            text = _plain_history
        # ams-life: what she keeps of it (memory, open loops), and what AstrBot sends the model
        # of this message, keep it as it was said -- "@名字(号码)", numbers too -- but someone
        # deleted is 某人 and an @ of her is her name (_without_gone). What AstrBot keeps in
        # its own history is step 2's.
        text = self._without_gone(text, event)
        if isinstance(getattr(turn_request, "prompt", None), str) and turn_request.prompt:
            turn_request.prompt = self._without_gone(turn_request.prompt, event)
        # The core must observe the incoming message; otherwise v/a/stress and
        # fallback labels only change when the model emits a hidden <biocore> tag.
        _query_vec = None
        if text and self.memory_dedup_embedding:
            try:
                _query_vec = await self._embed_text(text)
            except Exception:
                _query_vec = None
        _reaction = None
        if text:
            # ams-life K1: what she felt while hearing it, i.e. how observe() moves her.
            # The trust in this person follows that change (see _touch_user).
            try:
                _pre_v = float(getattr(core, "v", 0.0) or 0.0)
                _pre_stress = float(getattr(core, "stress", 0.0) or 0.0)
            except Exception:
                _pre_v, _pre_stress = 0.0, 0.0
            # the trust in this person is passed in for this call only (no global trust)
            core.observe(text, embedding=_query_vec,
                         relationship=self._relationship_of(self._user_record(event)))
            try:
                _reaction = {"v": float(getattr(core, "v", 0.0) or 0.0) - _pre_v,
                             "stress": float(getattr(core, "stress", 0.0) or 0.0) - _pre_stress}
            except Exception:
                _reaction = None
            # ams-life: open loops are matched, merged and closed in this window only.
            self._window_update_loops(event, text, core)
        _user_data = self._touch_user(event, core, reaction=_reaction)
        # Task-15: readiness is computed by L1 only when autonomy is enabled;
        # remember private sessions and start the P0-1 generator lazily.
        if (getattr(self, "proactive_autonomy", False)
                or getattr(self, "autonomy_loop_enabled", False)):
            try:
                self._update_autonomy_readiness(core, _user_data)
                if self._is_private_event(event):
                    self._register_autonomy_session(event)
                    self._ensure_autonomy_task()
            except Exception:
                pass
        _continuity = {}
        try:
            _continuity = self._continuity_context(event, core, _user_data,
                                                   prior_loops=_prior_open_loops)
        except Exception as exc:
            logger.warning("[biocore] continuity context failed: %s", exc)
            _continuity = {}
        try:
            _feedback = {key: _continuity.get(key) for key in ("summary", "loops", "relationship")}
            if any(_feedback.values()):
                self._record_continuity_feedback(event, _feedback)
        except Exception:
            pass
        _img = await self._image_context(event)
        _voice = await self._voice_context(event)
        # ams-life: this request's recall results, passed on instead of read back from self
        _turn = {}
        _mem = await self._memory_recall(event, text, core, _img, vec=_query_vec, voice=_voice,
                                         user_data=_user_data, turn=_turn)
        _memory_meta = _turn.get("memory_meta") or {}
        # ams-life: what this reply recalled, as ids only, for the brain map (pages/starmap)
        self._note_turn(event, _turn, core)
        try:
            asyncio.create_task(self._maybe_archive_events(event, core))
            asyncio.create_task(self._maybe_archive_strong_event(event, core, text))
        except Exception:
            pass
        _self_model = self._self_model_for(event)
        try:
            _own_lines = [str(h.get("text") or "") for h in self._window_replies(event, 12)]
            _recent_lines = [str(h.get("text") or "") for h in self._window_lines(event, 6)]
            core.bind_goal_context(memory_text=_mem, self_model=_self_model,
                                   recent=_recent_lines, text=text, own_lines=_own_lines)
        except Exception:
            pass
        _events = self._event_context(event)
        try:
            await self._maybe_tom_probe(event, core, text, _user_data, _memory_meta,
                                        memory_entries=_turn.get("memory_entries"))
        except Exception as exc:
            logger.warning("[biocore] tom probe call failed: %s", exc)
        _kb = ""
        if (getattr(self, "_neutral_model", None) is None and getattr(self, "kb_enabled", False)
                and getattr(self, "kb_names", None) and self._usable_memory_text(text)):
            try:
                _r = await asyncio.wait_for(
                    self.context.kb_manager.retrieve(query=text, kb_names=self.kb_names, top_m_final=3),
                    timeout=10.0)
                _kb = str((_r or {}).get("context_text") or "").strip()
            except Exception as exc:
                logger.warning("[biocore] kb retrieve failed: %s", exc)
        _base = str(getattr(turn_request, "system_prompt", "") or "")
        # ams-life step 1-2: descriptive lines only (no numbers, no QQ numbers, no "how
        # to reply"); the strategy hints were instructions and are no longer asked for.
        _sid, _sname = self._speaker(event)
        _global = bool(getattr(self, "global_memory", False))   # step 2, off by default
        _compact = interpretation.render_compact(
            core,
            _mem.replace("[BioCore Memory]", "").strip(),
            _events.replace("[BioCore Events]", "").strip(),
            self._labeled_notebook(event) if _global else self._notebook_for(event),
            self._user_view(event, _user_data),
            _img.replace("[BioCore Image]", "").strip(),
            _kb,
            _voice,
            memory_meta=_memory_meta,
            open_loops=[x for x in self._window_loops(event)
                        if not self._here(event).startswith("group:") or
                        (bool(_sid) and discretion.origin_of(x, self._here(event))["people"] == [str(_sid)])],
            answer_confidence=_memory_meta.get("answer_confidence"),
            continuity=_continuity,
            owner_rules=self._owner_rules(),
            private_with_him=bool(_sid) and self._here(event) == "private:" + str(_sid),
            people=self._people_lines(event),
            labeled=_global,
            owner_name=interpretation.owner_name(getattr(self, "config", None)),
        ).strip()
        # ams-life: the names she wrote back framed ("「柠檬」") are kept so, for the owner to read;
        # the reply model sees them without the frames, so as not to take to writing them in QQ
        _compact = discretion.unframe(_compact)
        _now = self._now_line(event)
        if _now:
            _compact = (_compact + "\n" + _now).strip()
        _day = calendar_cn.today_line(datetime.now().date())
        if _day:
            _compact = (_compact + "\n[日子] " + _day).strip()
        _our_days = mixin_selfie._our_days_line(self, event, datetime.now().date())
        if _our_days:
            _compact = (_compact + "\n" + _our_days).strip()
        _slang = self._slang_prompt(event)
        if _slang:
            _compact = (_compact + "\n" + _slang).strip()
        if not _img.replace("[BioCore Image]", "").strip() and _has_non_sticker_image(event):
            _compact = (_compact + "\n[图] " + attention.UNSEEN_IMAGE_NOTE).strip()
        _weather = weather.weather_line(STATE_DIR / 'weather.json', self.config or {})
        if (self.config or {}).get("photo_enabled", False):
            _outfit = mixin_selfie.look.read_look(mixin_selfie.LOOK_PATH, datetime.now().date())
            _compact = (_compact + "\n" + mixin_selfie.look.look_line(
                datetime.now().date(), _outfit, getattr(self, "self_model", {}) or {}, _weather)).strip()
        elif _weather:
            _compact = (_compact + "\n" + _weather).strip()
        if getattr(self, "self_decide", False):
            # step 2 (甲): what she may pick (nothing, a face, a short line, an answer, several)
            _compact = (_compact + "\n[她可以] " + attention.CHOICES_NOTE).strip()
        if getattr(self, "reply_in_pieces", True):
            _compact = (_compact + "\n" + attention.PIECES_NOTE).strip()
        _offer = ""
        if self._stickers_on():
            # step 2 (丙): a few of her stickers to pick from (none is sent unless she names it)
            try:
                _offer = await self._sticker_offer(event, core, _query_vec)
            except Exception as exc:
                _offer = ""
                logger.warning("[ams-life] stickers: none offered (%s)", type(exc).__name__)
            if _offer:
                _compact = (_compact + "\n" + _offer).strip()
        if _global:
            # step 2: no QQ number and no group number reaches the model (the owner, 10-29: 31)
            _compact = self._for_model(_compact, event)
            self._numbers_out_of_request(turn_request, event)
        if _compact:
            # Keep the system prompt stable (prefix-cache friendly) and attach
            # the transient intent to this user turn instead of persisting it.
            # ams-life: "_no_save" makes it this turn's only: AstrBot (4.29.3,
            # agent/message.py) sends it to the model but leaves it out of the
            # conversation history, so old blocks do not pile up and come back.
            # (The system prompt below is never saved either.)
            parts = getattr(turn_request, "extra_user_content_parts", None)
            if isinstance(parts, list):
                parts.append({"type": "text", "text": _compact, "_no_save": True})
            else:
                turn_request.system_prompt = (_base + "\n\n" + _compact).strip()
        self._note_allowed(event, turn_request, _compact)
        if _offer:
            _note = self._check_note(event)
            _note["allowed"] = str(_note.get("allowed") or "").replace(self._for_model(_offer, event), "")

    async def _after_reply(self, event, reply):
        """Her reply after the model: kept, checked, shaped and sent. Works through a reply handle only (adapter_astrbot_turn.reply_handle)."""
        if self._ignored_sender(event):   # nothing of an answer to him is kept
            self._phone_queue(event).clear()
            event.stop_event()
            return
        if not self.enabled:
            self._phone_queue(event).clear()
            return
        if getattr(self, "self_decide", False):
            self._note_spend("reply", reply)   # step 2: the money of the day
        if self._browse_on():
            try:   # step 2 (丁): the rounds her tools took, into the browser's own money
                self._browse_after_reply(event, reply)
            except Exception as exc:
                logger.warning("[ams-life] browse: not counted (%s)", type(exc).__name__)
        self._continue_job(self._here(event))
        self._check_registry(event)  # her reply to someone she may not keep is not kept either
        core = self._core(event)
        # ams-life: no state tag is asked for any more. If the model writes one anyway
        # it is cut out (whether it parses or not) and what it says is not used.
        _reply = reply.map_words(interpretation.strip_state_tags)
        # step 2 (丙): the sticker she named ([表情包:n], only an offered one), sent after her words. Marks
        # are taken out with stickers off too: her history may hold [表情包：标签] from before
        _sticker_source = _reply
        _reply, _sticker = self._sticker_named(event, reply, _reply)
        _before_check = _reply
        if not self._stickers_on():
            _sticker = ""
        if getattr(self, "self_decide", False) and attention.silent(_reply) \
                and not (_sticker and attention.SILENT not in _reply):   # a sticker alone is not silence
            if self._browse_on():
                try:
                    await self._browse_keep_reply(event)
                except Exception as exc:
                    logger.warning("[ams-life] browse: pages not kept (%s)", type(exc).__name__)
            # step 2 (甲): she chose to say nothing (【不说】): nothing is sent, nothing kept
            logger.info("[ams-life] attention: she said nothing")
            self._check_note(event).update(sent="", outcome="silent")
            self._phone_queue(event).clear()
            self._stop(event)
            return
        if _reply.strip():
            # step 2: the last look before it is sent; "" = nothing is sent and nothing kept.
            # If the look itself fails, the reply is held back as if it leaked.
            try:
                _reply = await self._look_at_reply(event, reply, _reply)
            except Exception as exc:
                _reply = self._check_failed(event, exc, reply)
            if self._browse_on():
                try:
                    await self._browse_keep_reply(event)
                except Exception as exc:
                    logger.warning("[ams-life] browse: pages not kept (%s)", type(exc).__name__)
            if not _reply:
                self._phone_queue(event).clear()
                self._stop(event)
                return
            # said once more: a mark in the new words is taken out too
            if _reply != _before_check:
                _sticker_source = _reply
                _sticker = ""
            _reply, _again = self._sticker_named(event, reply, _reply)
            _sticker = _sticker or (_again if self._stickers_on() else "")
            self._check_note(event)["sent"] = _reply
        elif self._browse_on():
            try:
                await self._browse_keep_reply(event)
            except Exception as exc:
                logger.warning("[ams-life] browse: pages not kept (%s)", type(exc).__name__)
        if getattr(self, "self_decide", False):
            if attention.silent(_reply) and not (_sticker and attention.SILENT not in _reply):
                self._check_note(event).update(sent="", outcome="silent")
                self._phone_queue(event).clear()
                self._stop(event)
                return
            _reply = _reply.replace(attention.SILENT, "")
            if not getattr(self, "reply_in_pieces", True):
                reply.set_text(_reply)
        if _copies_owner_rule(_reply, self._owner_rules()):
            logger.info("[ams-life] reply held: owner rule copied")
            self._check_note(event).update(sent="", outcome="rule_copy")
            self._phone_queue(event).clear()
            self._stop(event)
            return
        if _sticker and not await self._sticker_cleared(event, _sticker):
            _sticker = ""
        _queue = self._phone_queue(event)
        _voice_only_event = None
        if (isinstance(event, adapter_astrbot_turn.turn.TurnEvent) and _queue.get("voice")
                and _reply.strip()):
            _parts = attention.split(_reply)
            _kept = []
            for _part in _parts:
                if await mixin_selfie._same_as_voice(self, _part, _queue["voice"]):
                    logger.info("[ams-life] reply text dropped: same as voice")
                else:
                    _kept.append(_part)
            if len(_kept) != len(_parts):
                _reply = "\n".join(_kept)
                reply.set_text(_reply)
                self._check_note(event)["sent"] = _reply
                if not _reply.strip():
                    from copy import copy
                    event._ams_voice_history = {"text": _queue["voice"]}
                    _voice_only_event = copy(event)
                    self._stop(event)
        if _reply.strip() and "photo" in _queue:
            await mixin_selfie._prepare_photo(self, event, _queue)
        _then = self._sticker_after(event, _sticker) if _sticker else None
        if _then is not None and not _reply.strip():
            # a sticker and no words: AstrBot sends nothing, the plugin sends the sticker
            self._stop(event)
            asyncio.create_task(self._after_words(_then))
        elif _then is not None and not getattr(self, "reply_in_pieces", True):
            asyncio.create_task(self._after_words(_then))
        if getattr(self, "reply_in_pieces", True) and _reply.strip():
            # Her messages as she wrote them, with the sticker after its piece.
            _sticker_part = None
            if _then is not None:
                _offered = getattr(event, "_ams_stickers_offered", None) or []
                for _mark in stickers._MARK.finditer(_sticker_source):
                    if stickers.pick_from_reply(_mark.group(), _offered)[1] == _sticker:
                        _marked = stickers.pick_from_reply(
                            _sticker_source[:_mark.start()] + "\ue000" + _sticker_source[_mark.end():],
                            _offered)[0]
                        _marked_parts = attention.split(_marked)
                        _index = next((i for i, p in enumerate(_marked_parts) if "\ue000" in p), 0)
                        _sticker_part = min(sum(bool(p.replace("\ue000", "").strip())
                                                for p in _marked_parts[:_index + 1]) - 1,
                                            len(attention.split(_reply)) - 1)
                        _sticker_part = max(0, _sticker_part)
                        break
            _reply = self._shape_reply(event, reply, _reply, then=_then, sticker_part=_sticker_part)
            self._check_note(event)["sent"] = _reply
        if _sticker:
            # kept in her phone and AstrBot's history as what was sent
            _reply = (_reply + "\n" + stickers.phone_line(self._sticker_lib().rows.get(_sticker))).strip()
            self._check_note(event)["sent"] = _reply
            try:
                setattr(event, "_ams_sticker_sent", True)
            except Exception:
                pass
        try:
            core.observe_own(_reply)
            core.record_reply(_reply)
        except Exception:
            pass
        try:
            self._window_add_reply(event, _reply)
        except Exception as exc:
            logger.warning("[ams-life] window write failed: %s", exc)
        try:
            self._slang_note_reply(event, _reply)
        except Exception:
            logger.warning("[ams-life] slang status update failed")
        try:
            core.record_talk(_reply)
        except Exception:
            pass
        try:
            if _reply:
                asyncio.create_task(self._remember(event, _reply, "assistant", core))
        except Exception:
            pass
        try:
            STATE_DIR.mkdir(parents=True, exist_ok=True)
            HER_STATE_PATH.write_text(
                json.dumps(core.snapshot(), ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception:
            pass
        # L-T01/L-T08/L-T12: background proposal-only tasks. They self-check
        # the per-function switch + cooldown, so default OFF means zero calls.
        try:
            asyncio.create_task(self._maybe_relationship_impression(event, core))
            asyncio.create_task(self._maybe_relationship_narrative(event, core))
        except Exception:
            pass
        # Her queued media follows a cleared reply.
        try:
            _queue = self._phone_queue(event)
            _stopped = bool(event.is_stopped()) if hasattr(event, "is_stopped") else False
            if _queue and _voice_only_event is not None:
                asyncio.create_task(self._media_after_reply(_voice_only_event, dict(_queue)))
            elif _queue and _reply.strip() and not attention.silent(_reply) and not _stopped:
                asyncio.create_task(self._media_after_reply(event, dict(_queue)))
            _queue.clear()
        except Exception:
            pass

    def _keep_likeness(self, event, reply) -> None:
        """Keep only a successfully sent reply in the new program."""
        try:
            place = self._here(event)
            if not self._private_allowed(event) or not self._message_may_speak(event):
                return
            if place.startswith('private:'):
                owner = str((getattr(self, 'config', None) or {}).get('owner_qq') or '').strip()
                if not owner or str(self._speaker(event)[0]) != owner:
                    return
            elif not place.startswith('group:'):
                return
            incoming = adapter_astrbot_turn.incoming_of(event)
            if not incoming.sender_id or not self._may_keep([incoming.sender_id], place, time.time(),
                                                             [incoming.message_id] if incoming.message_id else []):
                return
            sent = self._check_note(event).get('sent')
            text = str(sent if sent is not None else reply.text or '').strip()
            if not text:
                return
            lines = []
            recent = self._read_window(place).get('recent', [])
            for row in recent:
                if row.get('role') != 'user':
                    continue
                sid = str(row.get('sender_id') or '')
                if not sid or not self._may_keep([sid], place, row.get('ts'), [row.get('msg_id')] if row.get('msg_id') else []):
                    continue
                lines.append({'sender_id': sid, 'name': str(row.get('sender_name') or ''),
                              'text': str(row.get('text') or '')})
            if not any(row.get('role') == 'user' and str(row.get('msg_id') or '') == incoming.message_id
                       for row in recent if incoming.message_id):
                lines.append({'sender_id': str(incoming.sender_id), 'name': str(incoming.sender_name or ''),
                              'text': str(incoming.text or '')})
            likeness.Store(DATA_DIR).add(place, text, lines[-5:])
        except Exception as exc:
            logger.warning('[ams-life] likeness not kept (%s)', type(exc).__name__)

    def _keep_turn(self, event, turn_request, reply) -> None:
        """The new program's history (AstrBot keeps its own): this turn's line from the person and
        what she sent, as AstrBot keeps it after _settle_history. Nothing when the turn was
        stopped (she said nothing, or the look before sending held it back)."""
        store = self._history_store()
        if store is None:
            return
        try:
            if event.is_stopped():
                pending = getattr(event, "_ams_voice_history", None)
                if pending is not None:
                    pending["request"] = turn_request
                    pending["reply"] = reply
                return
            pending = getattr(event, "_ams_voice_history", None)
            sent = "[语音] " + pending["text"] if pending is not None else self._check_note(event).get("sent")
            text = sent if sent is not None else reply.text
            if not str(text or "").strip():
                return
            place = self._here(event)
            inc = adapter_astrbot_turn.incoming_of(event)
            store.append(place, "user", turn_request.prompt, sender_id=inc.sender_id,
                         sender_name=inc.sender_name, message_id=inc.message_id,
                         sources=self._source_ids(event))
            store.append(place, "assistant", text,
                         about=(inc.sender_id,) if inc.sender_id else (),
                         sources=self._source_ids(event))
        except Exception as exc:   # a broken file, a full disk: the reply is already sent
            logger.warning("[ams-life] history not kept (%s)", type(exc).__name__)
