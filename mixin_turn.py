# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Prepare one platform-neutral turn."""
try:
    from .common import *  # noqa: F401,F403
    from .body import *  # noqa: F401,F403
    from .mixin_phone import _expand_forward, _phone_line, _history_original
    from . import attention
except ImportError:
    from common import *  # noqa: F401,F403
    from body import *  # noqa: F401,F403
    from mixin_phone import _expand_forward, _phone_line, _history_original
    import attention


class TurnMixin:
    """Getting one turn ready: what she knows, feels and recalls, put into the request.
    Works on turn.TurnRequest only; AstrBot's hook converts to it and back (main.py)."""

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
        self._numbers_out_of_request(turn_request, event)
        if not self.inject_intent:
            _now = self._now_line(event)
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
        text = str(getattr(event, "message_str", "") or "").strip()
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
        if text:
            # the trust in this person is passed in for this call only (no global trust)
            core.observe(text, embedding=_query_vec,
                         relationship=self._relationship_of(self._user_record(event)))
            # ams-life: open loops are matched, merged and closed in this window only.
            self._window_update_loops(event, text, core)
        _user_data = self._touch_user(event, core)
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
            self._record_continuity_feedback(event, _continuity)
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
        if getattr(self, "kb_enabled", False) and getattr(self, "kb_names", None) and self._usable_memory_text(text):
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
        ).strip()
        # ams-life: the names she wrote back framed ("「柠檬」") are kept so, for the owner to read;
        # the reply model sees them without the frames, so as not to take to writing them in QQ
        _compact = discretion.unframe(_compact)
        _now = self._now_line(event)
        if _now:
            _compact = (_compact + "\n" + _now).strip()
        _slang = self._slang_prompt(event)
        if _slang:
            _compact = (_compact + "\n" + _slang).strip()
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
        if _global:
            self._note_allowed(event, turn_request, _compact)
            if _offer:   # offered sticker labels are not words said here
                _note = self._check_note(event)
                _note["allowed"] = str(_note.get("allowed") or "").replace(self._for_model(_offer, event), "")
