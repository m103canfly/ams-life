# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Step 2 (甲, setting self_decide, off by default): she decides herself whether to answer
(attention.py has the rules as pure functions).

on_message_decide (main.py, after on_message has kept the message in her phone):
1. called? (an @, a quote, her name, a private chat, someone taking up what she just said);
2. at night, called once she sleeps on; called again and again she is woken;
3. wait a few seconds: when more comes into this window meanwhile, this one is not judged
   (it is kept all the same: on_message ran first); the last one carries "called" on;
4. the two safety nets: about 30 of hers an hour in a group; the money of the day;
5. called: AstrBot answers as before, or -- the last message did not wake AstrBot -- the plugin
   asks for a reply (request_llm, in the conversation, so with her persona and the history);
   not called (groups): a score over the threshold of the level asks for a reply too.

on_llm_response: what she picked: 【不说】 (nothing sent, nothing kept), QQ faces, several messages
(【下一条】; the first sent by AstrBot, the rest by the plugin to the same chat, a pause between).
Every model call's cost goes into states/spend.json (numbers only).
"""
from __future__ import annotations

try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403

try:
    from . import adapter_astrbot_turn, attention, model_client, turn
except ImportError:
    import adapter_astrbot_turn
    import attention
    import model_client
    import turn
try:
    from . import discretion, messenger
except ImportError:
    import discretion
    import messenger

ATTENTION_PATH = STATE_DIR / "attention.json"
TIES_PATH = STATE_DIR / "ties.json"
SPEND_PATH = STATE_DIR / "spend.json"
MOOD_NIGHT_PATH = STATE_DIR / "mood" / "night.json"
WAIT_SECONDS = {"group": 6.0, "called": 2.0, "private": 3.0}
# yuan a million tokens (deepseek-flash, the price page's numbers of 10-29 at its peak hours, at
# 7.2 yuan a dollar; set in the config, checked again on install)
DEFAULT_PRICES = {"input_miss": 2.2, "input_hit": 0.05, "output": 8.7}


def _read_json(path, default):
    try:
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
        return data if isinstance(data, type(default)) else default
    except Exception:
        return default


def _write_json(path, data) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    atomic_file.replace(tmp, path)


class _Spending:
    """A provider whose answers are counted into the day's spending (step 2, the money of the day).
    Everything else is the provider's own."""

    def __init__(self, plugin, kind, provider):
        self._plugin, self._kind, self._provider = plugin, str(kind or "other"), provider

    def __getattr__(self, name):
        return getattr(self._provider, name)

    async def text_chat(self, *args, **kwargs):
        resp = await self._provider.text_chat(*args, **kwargs)
        self._plugin._note_spend(self._kind, resp)
        return resp


class _SpendingModel(model_client.ModelClient):
    """Our own model client whose answers are counted into the day's spending, as _Spending
    counts AstrBot's provider."""
    def __init__(self, plugin, kind, model):
        self._plugin, self._kind, self._model = plugin, str(kind or "other"), model

    async def chat(self, **kwargs):
        reply = await self._model.chat(**kwargs)
        self._plugin._note_spend(self._kind, reply)
        return reply


class AttentionMixin:
    def _spending(self, kind, provider):
        """Count vision always; with self_decide, count the other plugin calls too."""
        if provider is None or (kind != "vision" and not getattr(self, "self_decide", False)) or isinstance(provider, (_Spending, _SpendingModel)):
            return provider
        if isinstance(provider, model_client.ModelClient):
            return _SpendingModel(self, kind, provider)
        return _Spending(self, kind, provider)

    # ------------------------------------------------------------------
    # settings
    # ------------------------------------------------------------------
    def _attention_cfg(self) -> dict:
        cfg = getattr(self, "config", None) or {}

        def num(key, default):
            try:
                return float(cfg.get(key, default))
            except (TypeError, ValueError):
                return float(default)
        prices = dict(DEFAULT_PRICES)
        for k in prices:
            prices[k] = num("price_" + k, prices[k])
        names = cfg.get("her_names")
        if isinstance(names, str):
            names = [x for x in re.split(r"[\s,，、]+", names) if x]
        return {"names": [str(x) for x in (names or attention.HER_NAMES) if str(x).strip()],
                "level": str(cfg.get("attention_level", "normal") or "normal"),
                "owner": str(cfg.get("owner_qq", "") or "").strip(),
                "hard": num("day_budget_yuan", 10.0), "soft": num("day_budget_soft_yuan", 8.0),
                "prices": prices, "group_hour_max": int(num("group_hour_max", attention.GROUP_HOUR_MAX)),
                "night_start": str(cfg.get("night_start", "01:00") or "01:00"),
                "night_end": str(cfg.get("night_end", "08:25") or "08:25")}

    # ------------------------------------------------------------------
    # the money of the day (numbers only)
    # ------------------------------------------------------------------
    @staticmethod
    def _usage_of(resp) -> dict:
        """Tokens of one answer: DeepSeek's own cache numbers when the raw answer has them, else
        AstrBot's; with neither, every input token counts as not cached (more, not less)."""
        if isinstance(resp, (adapter_astrbot_turn.AstrBotReply, turn.TurnReply)):
            return resp.spend_usage()
        if isinstance(resp, model_client.ModelReply):
            u = resp.usage or {}
            return {"input_hit": int(u.get("input_hit", 0) or 0), "input_miss": int(u.get("input_miss", 0) or 0),
                    "output": int(u.get("output", 0) or 0)}
        raw = getattr(getattr(resp, "raw_completion", None), "usage", None)
        hit = getattr(raw, "prompt_cache_hit_tokens", None) if raw is not None else None
        miss = getattr(raw, "prompt_cache_miss_tokens", None) if raw is not None else None
        if isinstance(hit, int) and isinstance(miss, int):
            return {"input_hit": hit, "input_miss": miss, "output": int(getattr(raw, "completion_tokens", 0) or 0)}
        u = getattr(resp, "usage", None)
        if u is None:
            return {}
        return {"input_hit": int(getattr(u, "input_cached", 0) or 0),
                "input_miss": int(getattr(u, "input_other", 0) or 0), "output": int(getattr(u, "output", 0) or 0)}

    def _note_spend(self, kind, resp) -> float:
        """Add one model call to the day's spending (yuan, by kind). Never fails the call."""
        try:
            yuan = attention.cost(self._usage_of(resp), self._attention_cfg()["prices"])
            price = (getattr(self, "config", {}) or {}).get("vision_price_per_call", "")
            if kind in ("vision", "slang") and str(price).strip():
                yuan = max(0.0, float(price))
            data = _read_json(SPEND_PATH, {})
            day = data.setdefault(time.strftime("%Y-%m-%d"), {})
            day[str(kind)] = round(float(day.get(str(kind), 0) or 0) + yuan, 6)
            day["calls"] = int(day.get("calls", 0) or 0) + 1
            for old in sorted(data)[:-30]:
                data.pop(old, None)
            _write_json(SPEND_PATH, data)
            return yuan
        except Exception as exc:
            logger.warning("[ams-life] spending not noted: %s", exc)
            return 0.0

    def _spent_today(self) -> float:
        day = _read_json(SPEND_PATH, {}).get(time.strftime("%Y-%m-%d")) or {}
        return round(sum(float(v or 0) for k, v in day.items() if k not in ("calls", "vision_calls", "slang_calls")), 4)

    # ------------------------------------------------------------------
    # who she knows (the owner, 10-29: by the dealings; he himself the closest)
    # ------------------------------------------------------------------
    def _familiarity(self, person) -> float:
        person = str(person or "")
        owner = self._attention_cfg()["owner"]
        return attention.familiarity(_read_json(TIES_PATH, {}).get(person), owner=bool(owner) and person == owner)

    def _note_tie(self, person, called_her=False, private=False) -> None:
        person = str(person or "")
        if not person:
            return
        try:
            ties = _read_json(TIES_PATH, {})
            ties[person] = attention.note_tie(ties.get(person), called_her=called_her, private=private)
            _write_json(TIES_PATH, ties)
        except Exception as exc:
            logger.warning("[ams-life] dealings not noted: %s", exc)

    # ------------------------------------------------------------------
    # each window's state: the stretch waited on, night calls, her messages of the hour
    # ------------------------------------------------------------------
    def _window_state(self, here) -> dict:
        data = getattr(self, "_attention_state", None)
        if not isinstance(data, dict):
            data = self._attention_state = _read_json(ATTENTION_PATH, {})
        return data.setdefault(here, {})

    def _save_attention(self) -> None:
        data = getattr(self, "_attention_state", None)
        if isinstance(data, dict):
            keep = {}
            for here, st in data.items():
                keep[here] = {k: v for k, v in st.items() if k in ("night_calls", "awake_until", "sent")}
            try:
                _write_json(ATTENTION_PATH, keep)
            except Exception as exc:
                logger.warning("[ams-life] attention state not saved: %s", exc)

    def _last_reply_here(self, here) -> tuple:
        """When she last spoke in this window, and to whom (her reply's origin people)."""
        for x in reversed(self._read_window(here)["recent"]):
            if x.get("role") == "assistant":
                return float(x.get("ts", 0) or 0), list((x.get("origin") or {}).get("people") or [])
        return 0.0, []

    def _why_called(self, event) -> str:
        here = self._here(event)
        sid = str(self._speaker(event)[0] or "")
        ts, to = self._last_reply_here(here)
        named = attention.names_her(adapter_astrbot_turn.incoming_of(event).text, self._attention_cfg()["names"])
        return attention.called(self._addresses_her(event) or named, here.startswith("private:"), sid, ts, to)

    def _hear_mood(self, event) -> None:
        if not getattr(self, "mood_events_enabled", False):
            return
        sid = str(self._speaker(event)[0] or "")
        self_id = adapter_astrbot_turn.incoming_of(event).self_id
        if self_id and sid == self_id:
            return
        self._core(None).mood_hear(adapter_astrbot_turn.incoming_of(event).text, self._familiarity(sid) >= .3)

    def _mood_clock(self, now=None) -> None:
        if not getattr(self, "mood_events_enabled", False):
            return
        now = time.time() if now is None else float(now)
        cfg = self._attention_cfg()
        state = _read_json(MOOD_NIGHT_PATH, {})
        night = attention.is_night(now, cfg["night_start"], cfg["night_end"])
        seen = float(state.get("night_seen", 0) or 0)
        try:
            if night and (not seen or now - seen >= 86400):
                MOOD_NIGHT_PATH.parent.mkdir(parents=True, exist_ok=True)
                _write_json(MOOD_NIGHT_PATH, {"night_seen": now})
            elif not night and seen:
                _write_json(MOOD_NIGHT_PATH, {})
                if 0 <= now - seen < 86400:
                    self._core(None).mood_event("sleep")
        except (OSError, ValueError, TypeError):
            logger.warning("[ams-life] mood night transition could not be saved")

    # ------------------------------------------------------------------
    # the decision
    # ------------------------------------------------------------------
    async def _decision(self, event):
        """Whether she answers this message: "reply", or None (nothing for the plugin to do: the
        platform answers, or nobody does). Stops the event when she does not answer it."""
        if not self._private_allowed(event) or not self._message_may_speak(event):
            self._stop(event)
            return None
        cfg = self._attention_cfg()
        here = self._here(event)
        sid = str(self._speaker(event)[0] or "")
        private = here.startswith("private:")
        why = self._why_called(event)
        self._note_tie(sid, called_her=bool(why), private=private)
        st = self._window_state(here)
        now = time.time()
        try:
            from . import life_loop
        except ImportError:
            import life_loop
        # Card E2s: with the life loop on, one sleep decides (her own); with it off, the clock.
        by_the_loop = life_loop.enabled(self)
        night = not by_the_loop and attention.is_night(now, cfg["night_start"], cfg["night_end"])
        asleep = life_loop.asleep(self, now) if by_the_loop else False
        if getattr(self, "mood_events_enabled", False):
            self._mood_clock(now)
        if asleep:
            if not why:
                self._hear_mood(event)
                return None   # asleep she never speaks up herself
            owner = bool(cfg["owner"]) and sid == cfg["owner"]
            familiar = self._familiarity(sid)
            weight = attention.wake_weight(familiar, owner=owner)
            calls = [c for c in attention.wake_calls(st.get("night_calls")) if now - c[0] < 3600] + [(now, weight)]
            st["night_calls"] = calls
            self._save_attention()
            core = self._core(None)
            woken = attention.wake_check(calls, float(getattr(core, "sleepiness", 0.0) or 0.0), now)
            if woken:
                self._woken_at = now   # (乙: woken up, a bit cross)
                if getattr(self, "mood_events_enabled", False):
                    core.mood_event("woken")
                life_loop.wake_up(self, now)
            else:
                # Card E2s: the calls she slept through are kept for her first thinking awake.
                life_loop.note_missed(self, here, attention.wake_tier(familiar), now)
                self._stop(event)
                return None
        elif night:
            if not why:
                self._hear_mood(event)
                return None   # at night she never speaks up herself
            calls = [t for t in st.get("night_calls") or [] if now - float(t) < 3600] + [now]
            st["night_calls"] = calls
            answer, woken, until = attention.night_gate(calls, now, st.get("awake_until", 0.0))
            st["awake_until"] = until
            self._save_attention()
            if woken:
                self._woken_at = now   # (乙: woken up, a bit cross)
                if getattr(self, "mood_events_enabled", False):
                    self._core(None).mood_event("woken")
            if not answer:
                self._stop(event)
                return None
        # wait a few seconds: only the last message of a stretch is judged
        st["seq"] = int(st.get("seq", 0) or 0) + 1
        st["called"] = st.get("called") or why
        mine = st["seq"]
        wait = WAIT_SECONDS["private" if private else "called" if why else "group"]
        if getattr(self, "mood_events_enabled", False):
            core = self._core(None)
            core._decay_to_now()
            wait = attention.mood_wait(wait, core.v, core.energy)
        await asyncio.sleep(wait)
        if st.get("seq") != mine:
            if not why:
                self._hear_mood(event)
            self._stop(event)   # more came meanwhile; that one decides (kept all the same)
            return None
        why = st.pop("called", "") or why
        # the two safety nets
        state = attention.budget(self._spent_today(), cfg["soft"], cfg["hard"])
        if state == "hard" or (state == "soft" and not (private and cfg["owner"] and sid == cfg["owner"])):
            logger.info("[ams-life] attention: the money of the day (%s), not answered", state)
            self._stop(event)
            if not why:
                self._hear_mood(event)
            return None
        if not private and not attention.hour_ok(st.get("sent") or [], now, cfg["group_hour_max"]):
            logger.info("[ams-life] attention: %d of hers in this group this hour, not answered", cfg["group_hour_max"])
            self._stop(event)
            if not why:
                self._hear_mood(event)
            return None
        if why:
            if getattr(event, "is_at_or_wake_command", False):
                return None   # AstrBot answers it as before
            return "reply"
        if night or private:
            return None
        s = await self._score(event)
        limit = attention.threshold(cfg["level"])
        if getattr(self, "mood_events_enabled", False):
            core = self._core(None)
            core._decay_to_now()
            limit = attention.mood_threshold(cfg["level"], core.v, core.energy)
        if s >= limit:
            logger.info("[ams-life] attention: not called, %.2f over the threshold: asked", s)
            return "reply"
        self._hear_mood(event)
        return None

    async def _decide(self, event):
        """None (nothing for the plugin to do: AstrBot answers, or nobody does) or a request
        for a reply (request_llm). Stops the event when she does not answer it."""
        if await self._decision(event) == "reply":
            return await self._ask_for_reply(event)
        return None

    @staticmethod
    def _stop(event) -> None:
        try:
            event.stop_event()
        except Exception:
            pass

    async def _score(self, event) -> float:
        """attention.score of this message (no model; the local vectors only)."""
        here = self._here(event)
        now = time.time()
        recent = [x for x in self._read_window(here)["recent"] if now - float(x.get("ts", 0) or 0) <= 600]
        speakers = {str(x.get("sender_id") or "") for x in recent if x.get("role") != "assistant"}
        known = max([self._familiarity(p) for p in speakers if p] or [0.0])
        her = sum(1 for x in recent if x.get("role") == "assistant")
        last, _to = self._last_reply_here(here)
        quiet = (now - last) / 60.0 if last else 600.0
        text = adapter_astrbot_turn.incoming_of(event).text
        topic = 0.0
        try:
            vec = await self._embed_text(text) if text.strip() else None
            if vec:
                entries = [e for e in self._read_library().get("entries") or [] if isinstance(e, dict)
                           and not e.get("deleted") and e.get("vector")][-400:]
                topic = max([self._cosine(vec, e["vector"]) for e in entries] or [0.0])
        except Exception:
            topic = 0.0
        return attention.score(topic, known, her, quiet)

    async def _ask_for_reply(self, event):
        """A request for a reply to this message, in its conversation (her persona, the history,
        and saved back), as AstrBot answers a message that woke it."""
        conv = None
        try:
            mgr = self.context.conversation_manager
            umo = str(getattr(event, "unified_msg_origin", "") or "")
            cid = await mgr.get_curr_conversation_id(umo)
            if not cid:
                cid = await mgr.new_conversation(umo, platform_id=event.get_platform_id())
            conv = await mgr.get_conversation(umo, cid)
        except Exception as exc:
            logger.warning("[ams-life] attention: no conversation for the reply (%s)", type(exc).__name__)
        return event.request_llm(prompt=str(getattr(event, "message_str", "") or ""), conversation=conv)

    # ------------------------------------------------------------------
    # what she sends
    # ------------------------------------------------------------------
    def _note_sent(self, event, n=1) -> None:
        here = self._here(event)
        if not here.startswith("group:"):
            return
        st = self._window_state(here)
        now = time.time()
        st["sent"] = [t for t in st.get("sent") or [] if now - float(t) < 3600] + [now] * int(n)
        self._save_attention()

    @staticmethod
    def _chain_of(text):
        """One message as a chain: words and QQ faces (attention.pieces)."""
        return adapter_astrbot_turn.chain_of(text)

    async def _send_rest(self, event, umo, parts, then=None, sticker_part=None) -> bool:
        """The second message on, to the same chat, a pause before each (as if typing); then
        `then` (a coroutine function: her sticker, step 2 丙), a pause before it too."""
        if then is not None and sticker_part == 0:
            await self._after_words(then)
        for index, part in enumerate(parts, 1):
            await asyncio.sleep(attention.typing_seconds(part))
            try:
                await self._messenger(event).send(discretion.place_of(umo) or self._here(event), messenger.text_segments(part))
                self._note_sent(event, 1)
            except Exception as exc:
                logger.warning("[ams-life] the next message was not sent: %s", type(exc).__name__)
                return False
            if then is not None and sticker_part == index:
                await self._after_words(then)
        return True

    @staticmethod
    async def _after_words(then) -> None:
        """A short pause, then `then()` (her sticker after her words)."""
        await asyncio.sleep(attention.typing_seconds(""))
        try:
            sent = await then()
            if sent is False:
                logger.warning("[ams-life] the sticker was not sent")
                return False
            return True
        except Exception as exc:
            logger.warning("[ams-life] the sticker was not sent: %s", type(exc).__name__)
            return False

    def _shape_reply(self, event, response, reply, then=None, sticker_part=None) -> str:
        """Her reply as she picked it: the first message for AstrBot (words and faces), the rest
        sent after it. Returns what she said, as it is kept (the messages, one a line)."""
        parts = attention.split(reply)
        if not parts:
            return reply
        first = parts[0]
        try:
            # a chain of the first message only: AstrBot sends the chain when there is one, and
            # reads the words from it (provider/entities.py 447-462; DeepSeek's answers come with a
            # chain, openai_source.py 875) -- setting the words alone would leave the whole reply
            adapter_astrbot_turn.reply_handle(response).shape_first(first)
        except Exception as exc:
            logger.warning("[ams-life] the reply was not shaped: %s", exc)
            return reply
        if len(parts) > 1:
            setattr(event, "_ams_reply_was_split", True)
        if len(parts) > 1 or then is not None:
            umo = str(getattr(event, "unified_msg_origin", "") or "")
            task = asyncio.create_task(
                self._send_rest(event, umo, parts[1:], then,
                                sticker_part if sticker_part is not None else len(parts) - 1))
            if len(parts) > 1:
                event._ams_rest_task = task
        self._note_sent(event, 1)
        return "\n".join(parts)

    def _spend_for_panel(self) -> dict:
        cfg = self._attention_cfg()
        spent = self._spent_today()
        return {"spent": spent, "left": round(max(0.0, cfg["hard"] - spent), 4), "soft": cfg["soft"],
                "hard": cfg["hard"], "state": attention.budget(spent, cfg["soft"], cfg["hard"]),
                "level": cfg["level"]}
