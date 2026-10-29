# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: private-chat autonomy: readiness, gate, proactive send, background tick."""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403


class AutonomyMixin:
    def _is_private_event(self, event) -> bool:
        """Task-15: only private chats can ever trigger autonomy output."""
        try:
            umo = str(getattr(event, "unified_msg_origin", "") or "")
            if "GroupMessage" in umo or "GuildMessage" in umo:
                return False
            check = getattr(event, "is_private_chat", None)
            if callable(check):
                return bool(check())
            return False
        except Exception:
            return False

    def _loop_cfg_float(self, key: str, default: float,
                        lo: float, hi: float) -> float:
        """Read one numeric autonomy-loop config value (finite + clamped)."""
        try:
            value = float(self.config.get(key, default))
        except Exception:
            return float(default)
        if value != value or value in (float("inf"), float("-inf")):
            return float(default)
        return max(float(lo), min(float(hi), value))

    def _update_autonomy_readiness(self, core, user_data=None) -> dict:
        """Task-15: ask L1 to compute readiness only when autonomy is enabled."""
        if not getattr(self, "proactive_autonomy", False) or core is None:
            return {}
        try:
            return core.autonomy_state(self._relationship_of(user_data))
        except Exception:
            return {}

    def _autonomy_template(self, core, relationship=None) -> str:
        """Task-15: state-style deterministic proactive text (no summaries/LLM).

        Uses only need + current emotion + closeness band, so the send cannot
        leak event titles or stale summaries and stays reproducible.
        """
        labels = getattr(core, "labels", {}) or {}
        need = str(labels.get("need") or "talk")
        emotion = str(labels.get("emotion") or "neutral")
        need_txt = {"space": "你先忙，我不打扰。",
                    "share": "想听听你今天的碎片。",
                    "vent": "要是想说，我在。",
                    "be_heard": "我在听。",
                    "talk": "想和你说两句。"}.get(need, "想和你说两句。")
        emotion_txt = {"joy": "心情还算轻",
                       "sadness": "心里有点沉",
                       "anger": "有点憋着火",
                       "fear": "有点不安",
                       "loneliness": "有点想人陪",
                       "neutral": "情绪平稳"}.get(emotion, "情绪平稳")
        try:
            rel = relationship if isinstance(relationship, dict) else {}
            closeness = float((rel.get("state") or {}).get("closeness", 0.5) or 0.5)
        except Exception:
            closeness = 0.5
        if closeness >= 0.65:
            close_txt = "和你还挺亲近"
        elif closeness <= 0.35:
            close_txt = "和你有点距离"
        else:
            close_txt = "和你平常"
        return ("%s%s，%s。" % (need_txt, emotion_txt, close_txt))[:AUTONOMY_MAX_CHARS_MAX]

    def _autonomy_gate(self, core, relationship, now=None):
        """Task-15: L3 applies send gates to an L1 readiness result."""
        if core is None:
            return None, {"enabled": False}
        try:
            current = float(now if now is not None else time.time())
            state = core.autonomy_state(relationship, now=current)
            if not state.get("enabled") or not state.get("ready"):
                return None, state or {}
            # Stage-2: refusal_protocol is now a real gate, not a posture token.
            rel_state = relationship.get("state") if isinstance(relationship, dict) else {}
            rel_state = rel_state if isinstance(rel_state, dict) else {}
            try:
                protocol = relationship_meta.refusal_protocol({
                    "boundary_pressure": float(getattr(core, "boundary_pressure", 0.0) or 0.0),
                    "trust": float(rel_state.get("trust", 0.5) or 0.5),
                    "conflict": float(rel_state.get("conflict", 0.0) or 0.0),
                })
            except Exception:
                protocol = {"mode": "comply"}
            if str(protocol.get("mode") or "comply") == "decline":
                return None, state
            if str(protocol.get("mode") or "comply") == "negotiate":
                state = dict(state)
                state["max_chars"] = min(int(state.get("max_chars") or 120), 90)
            hour = time.localtime(current).tm_hour
            if AUTONOMY_QUIET_START_HOUR <= hour < AUTONOMY_QUIET_END_HOUR:
                return None, state
            last_ts = float(state.get("last_sent_ts", 0.0) or 0.0)
            if last_ts > 0 and (current - last_ts) < AUTONOMY_COOLDOWN_SECONDS:
                return None, state
            day = time.strftime("%Y-%m-%d", time.localtime(current))
            sent_count = int(state.get("sent_count", 0) or 0)
            if str(state.get("sent_day") or "") != day:
                sent_count = 0
            if sent_count >= AUTONOMY_DAILY_CAP:
                return None, state
            max_chars = int(state.get("max_chars") or 120)
            text = self._autonomy_template(core, {"state": rel_state})[:max(1, max_chars)].strip()
            return (text or None), state
        except Exception:
            return None, {"enabled": False}

    async def _maybe_proactive_send(self, event, core, now=None) -> bool:
        """Task-15: private-only send of the deterministic template."""
        if not getattr(self, "proactive_autonomy", False):
            return False
        if not getattr(self, "proactive_send", False) or core is None:
            return False
        if not self._is_private_event(event):
            return False
        try:
            current = float(now if now is not None else time.time())
            try:
                user_data = self._user_record(event)
            except Exception:
                user_data = {}
            text, state = self._autonomy_gate(
                core, self._relationship_of(user_data), now=current)
            if not text:
                return False
            await event.send(MessageChain([Plain(text)]))
            day = time.strftime("%Y-%m-%d", time.localtime(current))
            sent_count = int(state.get("sent_count", 0) or 0)
            if str(state.get("sent_day") or "") != day:
                sent_count = 0
            core._proactive_autonomy.update({
                "last_sent_ts": round(current, 3),
                "sent_day": day,
                "sent_count": sent_count + 1,
                "last_sent_chars": len(text),
            })
            return True
        except Exception as exc:
            logger.warning("[biocore] proactive send failed: %s", exc)
            return False

    def _register_autonomy_session(self, event) -> None:
        """Task-15: remember one private session for the background generator."""
        try:
            umo = str(getattr(event, "unified_msg_origin", "") or "").strip()
            if not umo:
                return
            sid, sname = self._speaker(event)
            self._autonomy_private_sessions[umo] = {
                "umo": umo, "sender_id": sid, "sender_name": sname,
                "ts": round(time.time(), 3),
            }
            if len(self._autonomy_private_sessions) > 20:
                _items = sorted(self._autonomy_private_sessions.items(),
                                key=lambda kv: float(kv[1].get("ts", 0.0) or 0.0),
                                reverse=True)[:20]
                self._autonomy_private_sessions = dict(_items)
        except Exception:
            pass

    def _ensure_autonomy_task(self) -> None:
        """P0-1: start the plugin's 5-minute loop. ams-life: it runs whenever the plugin is
        on, because every tick also sweeps her phone; the autonomy tick inside it still
        runs only when task-15 or task-28 is on."""
        if not getattr(self, "enabled", True):
            return
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return  # not inside AstrBot's loop yet; the next message starts it
        try:
            task = getattr(self, "_autonomy_task", None)
            if task is None or task.done():
                self._autonomy_task = asyncio.create_task(self._autonomy_loop())
        except Exception:
            pass

    async def _autonomy_loop(self) -> None:
        """P0-1: 5-minute deterministic tick; exits when the plugin is turned off.
        ams-life: each tick sweeps expired lines out of her phone; the autonomy tick
        runs only when task-15 or task-28 is on."""
        try:
            while getattr(self, "enabled", True):
                await asyncio.sleep(AUTONOMY_TICK_SECONDS)
                if not getattr(self, "enabled", True):
                    break
                try:
                    self._sweep_windows()
                    self._core(None).set_ambient(self._ambient_level())
                    if getattr(self, "mood_events_enabled", False):
                        self._mood_clock()
                except Exception:
                    pass
                try:
                    self._begin_job()
                    await self._maybe_daily_digest()
                except Exception as exc:
                    logger.warning("[ams-life] daily digest failed: %s", exc)
                try:
                    self._begin_job()
                    await self._maybe_write_notebook()
                except Exception as exc:
                    logger.warning("[ams-life] notebook failed: %s", exc)
                try:
                    self._begin_job()
                    await self._maybe_update_impressions()
                except Exception as exc:
                    logger.warning("[ams-life] impressions failed: %s", exc)
                try:
                    await self._group_browse_tick()
                except Exception as exc:
                    logger.warning("[ams-life] group browse failed (%s)", type(exc).__name__)
                if not (getattr(self, "proactive_autonomy", False)
                        or getattr(self, "autonomy_loop_enabled", False)):
                    continue
                try:
                    self._begin_job()
                    await self._autonomy_tick()
                except Exception:
                    pass
        except asyncio.CancelledError:
            return
        except Exception:
            return

    @staticmethod
    def _autonomy_exit_plan(acted: bool, loop_on: bool, proactive_on: bool,
                            proactive_send: bool, token_only: bool) -> str:
        """Single-exit decision for one autonomy tick (spec §7.1 / S20).

        Returns "token" (loop broadcast only; nothing is sent), "send" (the
        existing task-15 send gate may run) or "none". It can never return two
        exits for the same session/tick.
        """
        if not proactive_on or not proactive_send:
            return "token" if acted else "none"
        if acted and loop_on and token_only:
            return "token"
        return "send"

    async def _autonomy_tick(self, now=None) -> list:
        """One autonomous tick over remembered PRIVATE sessions (task-15+task-28).

        Task-28 adds the candidate/arbitration token broadcast. Exit mutual
        exclusion (S20): per session per tick, either the loop broadcasts one
        token (token-only => nothing sent) or the existing task-15 send gate may
        send at most once -- never both.
        """
        sent = []
        loop_on = bool(getattr(self, "autonomy_loop_enabled", False))
        proactive_on = bool(getattr(self, "proactive_autonomy", False))
        if not (loop_on or proactive_on):
            return sent
        try:
            current = float(now if now is not None else time.time())
        except Exception:
            current = time.time()
        for umo, info in list(getattr(self, "_autonomy_private_sessions", {}).items()):
            try:
                if current - float(info.get("ts", 0.0) or 0.0) > 86400:
                    continue
                cores = getattr(self, "cores", None)
                core = cores.get(umo) if isinstance(cores, dict) else None
                if core is None or not (getattr(core, "autonomy_enabled", False)
                                        or getattr(core, "autonomy_loop_enabled", False)):
                    continue
                # Unified noise model: one update point per tick.
                try:
                    core.noise_tick(now=current)
                except Exception:
                    pass
                target = _AutonomySendTarget(
                    self, umo, info.get("sender_id", ""),
                    info.get("sender_name", ""), private=True)
                acted = False
                if loop_on and getattr(core, "autonomy_loop_enabled", False):
                    try:
                        user_data = self._user_record(target)
                        loop_result = core.autonomy_loop_tick(
                            self._relationship_of(user_data), now=current,
                            private_chat=True)
                        acted = bool(loop_result.get("ignition"))
                    except Exception as exc:
                        logger.warning("[biocore] autonomy loop tick failed: %s", exc)
                        acted = False
                plan = self._autonomy_exit_plan(
                    acted, loop_on, proactive_on,
                    bool(getattr(self, "proactive_send", False)),
                    bool(getattr(self, "autonomy_loop_token_only", True)))
                if plan == "send":
                    if await self._maybe_proactive_send(target, core, now=current):
                        sent.append(umo)
            except Exception:
                continue
        return sent

    def _readiness_text(self, event) -> str:
        """Task-15: read-only /biocore readiness report (no side effects when off)."""
        if not getattr(self, "proactive_autonomy", False):
            return ("[BioCore] readiness: disabled (proactive_autonomy=false)\n"
                    "proactive_send=%s" % bool(getattr(self, "proactive_send", False)))
        try:
            core = self._core(event)
            try:
                user_data = self._user_record(event)
            except Exception:
                user_data = {}
            state = core.autonomy_state(self._relationship_of(user_data), persist=False)
            sources = state.get("sources") or {}
            noise = sources.get("noise") or {}
            return ("[BioCore] readiness: threshold=%.3f max_chars=%d impulse=%.3f "
                    "ema=%.3f ready=%s enabled=true send=%s\n"
                    "sources: chaos=%.3f echo=%.3f stress_load=%.3f drive_dev=%.3f "
                    "trust=%.3f closeness=%.3f gain=%.3f noise_seed=%s "
                    "noise(st=%s en=%s so=%s at=%s va=%s)" % (
                        float(state.get("threshold", 0.0)),
                        int(state.get("max_chars", 0)),
                        float(state.get("impulse", 0.0)),
                        float(state.get("impulse_ema", 0.0)),
                        bool(state.get("ready")),
                        bool(getattr(self, "proactive_send", False)),
                        float(state.get("chaos", 0.0)),
                        float(sources.get("echo_trace", 0.0)),
                        float(sources.get("stress_load", 0.0)),
                        float(sources.get("drive_dev", 0.0)),
                        float(sources.get("trust", 0.5)),
                        float(sources.get("closeness", 0.5)),
                        float(sources.get("autonomy_gain", 1.0)),
                        state.get("noise_seed", 0),
                        noise.get("stress", 0.0), noise.get("energy", 0.0),
                        noise.get("social", 0.0), noise.get("attention", 0.0),
                        noise.get("valence", 0.0)))
        except Exception as exc:
            logger.warning("[biocore] readiness report failed: %s", exc)
            return "[BioCore] readiness: error"
