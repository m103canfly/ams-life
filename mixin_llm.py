# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: persona, model function switches, provider choice, proposal-only LLM hints, user records."""
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
    from . import digest
except ImportError:
    import digest
try:
    from .vision import ImageAPI, VisionGate
except ImportError:
    from vision import ImageAPI, VisionGate


def _counted(plugin, kind, provider):
    """step 2 (甲): the provider, its answers counted into the day's spending when the plugin
    counts them (AttentionMixin._spending); as it is otherwise."""
    count = getattr(plugin, "_spending", None)
    return count(kind, provider) if count else provider


class LLMMixin:
    def _load_profile(self):
        try:
            if PROFILE_PATH.exists():
                d = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
                self.profile = dict(d.get("profile") or {})
                self.persona_text = str(d.get("persona") or "")
                _ph = str(d.get("persona_hash") or "")
                self._persona_compiled_hash = _ph or (_sha256(self.persona_text) if self.persona_text else "")
                _schema = d.get("schema")
                if isinstance(_schema, list):
                    self.schema_texts = [str(x).strip()[:60] for x in _schema
                                         if str(x).strip()][:6]
                _style = d.get("style")
                if isinstance(_style, dict):
                    _tag = str(_style.get("intimacy_style") or "neutral")
                    if _tag not in ("neutral", "playful", "gentle", "reserved"):
                        _tag = "neutral"
                    _terms = [str(x).strip()[:12] for x in (_style.get("address_terms") or [])
                              if str(x).strip()][:3]
                    self.persona_style = {"intimacy_style": _tag, "address_terms": _terms}
                logger.info("[biocore] loaded profile %s", PROFILE_PATH)
        except Exception as exc:
            logger.warning("[biocore] profile load failed: %s", exc)

    async def _persona_text(self, event) -> str:
        try:
            pm = self.context.persona_manager
            _pid = str(getattr(self, "persona_id", "") or self.config.get("persona_id") or "").strip()
            if _pid:
                try:
                    _p = pm.get_persona_v3_by_id(_pid)
                except Exception:
                    _p = None
                if _p:
                    if isinstance(_p, dict):
                        return str(_p.get("prompt") or _p.get("system_prompt") or "")
                    return str(getattr(_p, "prompt", "") or getattr(_p, "system_prompt", "") or "")
            p = await pm.get_default_persona_v3(getattr(event, "unified_msg_origin", None))
            if isinstance(p, dict):
                return str(p.get("prompt") or p.get("system_prompt") or "")
            return str(getattr(p, "prompt", "") or getattr(p, "system_prompt", "") or "")
        except Exception as exc:
            logger.warning("[biocore] persona read failed: %s", exc)
            return ""

    def _function_cfg(self, kind: str) -> dict:
        _name = LLM_FUNCTION_ALIASES.get(str(kind or ""), str(kind or ""))
        _all = getattr(self, "llm_functions", None)
        if not isinstance(_all, dict):
            return {"enabled": True, "provider": "follow_llm"}
        _cfg = _all.get(_name)
        if not isinstance(_cfg, dict):
            _cfg = {}
        return {
            "enabled": bool(_cfg.get("enabled", LLM_FUNCTION_DEFAULTS.get(_name, True))),
            "provider": str(_cfg.get("provider") or "follow_llm"),
        }

    def _llm_allowed(self, kind: str) -> bool:
        """Per-function LLM switch (replaces the old global strict flag)."""
        _all = getattr(self, "llm_functions", None)
        if not isinstance(_all, dict):
            # Test harness / legacy object created before this feature: keep
            # the old llm_only_reply_summary semantics when present.
            _strict = getattr(self, "llm_only_reply_summary", None)
            if _strict is None:
                return True
            return (not bool(_strict)) or str(kind or "") in ("reply", "summary")
        return self._function_cfg(kind)["enabled"]

    def _provider_kind(self, provider) -> str:
        """Classify a provider by id/model/type (chat / vision / embedding / tts / rerank)."""
        try:
            cfg = getattr(provider, "provider_config", {}) or {}
            raw = " ".join(str(x or "") for x in (
                cfg.get("id"), cfg.get("model"),
                cfg.get("provider_type"), type(provider).__name__,
            )).lower()
        except Exception:
            raw = ""
        if any(x in raw for x in ("img", "image", "vision", "t2i", "dall", "stable", "midjourney", "exusiai-img")):
            return "vision"
        if any(x in raw for x in ("tts", "speech", "voice")):
            return "tts"
        if any(x in raw for x in ("embed", "bge", "text-embedding")):
            return "embedding"
        if "rerank" in raw:
            return "rerank"
        return "chat"

    async def _provider_for(self, kind: str, event=None):
        """Resolve the LLM provider for one function.

        Default ("follow_llm") uses AstrBot's current chat provider. A configured
        provider_id is looked up via get_provider_by_id; if it is missing we log
        a warning and fall back to the main LLM instead of failing the feature.
        """
        _cfg = self._function_cfg(kind)
        _override = _cfg["provider"]
        _umo = str(getattr(event, "unified_msg_origin", "") or "") if event is not None else ""
        if _override and _override not in ("follow_llm", "main", "default", ""):
            _p = None
            try:
                _p = self.context.get_provider_by_id(_override)
            except Exception as exc:
                logger.warning("[biocore] provider lookup failed for %s (%s): %s", kind, _override, exc)
                _p = None
            if _p is not None:
                if self._provider_kind(_p) == "chat":
                    return _counted(self, kind, _p)
                logger.warning("[biocore] llm function %s provider %s is not a chat provider; fallback to main LLM",
                               kind, _override)
            else:
                logger.warning("[biocore] llm function %s provider %s not found; fallback to main LLM", kind, _override)
        try:
            return _counted(self, kind, await self.context.get_using_provider_async(_umo))
        except Exception as exc:
            logger.warning("[biocore] main LLM provider lookup failed for %s: %s", kind, exc)
            return None

    # ------------------------------------------------------------------
    # LLM v2 (L-T01..L-T12): proposal-only model calls.
    #
    # Contract:
    #   * every function is registered in LLM_FUNCTIONS and defaults to OFF;
    #   * prompt text + output parsing only live in interpretation.py;
    #   * a model output is validated before storage (relationship_meta);
    #   * no function writes core v/a/d/trust/goals or generates a reply;
    #   * strict/legacy mode (_llm_allowed) skips every extra call.
    # ------------------------------------------------------------------
    async def _llm_v2_call(self, kind, prompt, parser, event=None, system_prompt=None):
        if not self._llm_allowed(kind):
            return None
        try:
            provider = await self._provider_for(kind, event)
        except Exception as exc:
            logger.warning("[biocore] llm v2 provider failed (%s): %s", kind, exc)
            return None
        if provider is None:
            return None
        try:
            if system_prompt:
                resp = await provider.text_chat(prompt=prompt, system_prompt=system_prompt)
            else:
                resp = await provider.text_chat(prompt=prompt)
            raw = str(getattr(resp, "completion_text", "") or "").strip()
            if not raw:
                return None
            return parser(raw)
        except Exception as exc:
            logger.warning("[biocore] llm v2 call/paser failed (%s): %s", kind, exc)
            return None

    def _llm_v2_cooldown_ok(self, kind):
        try:
            last = float((getattr(self, "_llm_v2_last", {}) or {}).get(kind, 0.0) or 0.0)
        except Exception:
            last = 0.0
        return (time.time() - last) >= float(LLM_V2_COOLDOWNS.get(kind, 600))

    def _llm_v2_mark(self, kind):
        if not isinstance(getattr(self, "_llm_v2_last", None), dict):
            self._llm_v2_last = {}
        self._llm_v2_last[kind] = time.time()

    def _user_record(self, event):
        try:
            path = self._user_path(event)
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {}

    def _save_user_record(self, event, data):
        try:
            if not isinstance(data, dict) or self._job_stale():
                return
            path = self._user_path(event)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as exc:
            logger.warning("[biocore] user record save failed: %s", exc)

    def _record_calibration(self, event, source, predicted, correct) -> None:
        """Persist one calibration sample in the user relationship doc.

        Record-only: writes relationship.calibration (EWMA/Brier per evidence
        source) via the single user-file writer; it never rewrites trust or any
        other biological field. Called from the memory-conflict branch.
        """
        path = self._user_path(event)
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return
        if not isinstance(data, dict):
            return
        rel = dict(data.get("relationship")) if isinstance(data.get("relationship"), dict) else {}
        rel["calibration"] = relationship_meta.calibration_update(
            rel.get("calibration"), source, predicted, correct)
        data["relationship"] = rel
        self._save_user_record(event, data)

    def _relationship_of(self, user_data):
        rel = (user_data or {}).get("relationship") if isinstance(user_data, dict) else None
        return rel if isinstance(rel, dict) else {}

    def _deterministic_hint(self, text, user_data, events_raw, memory_meta, core=None, cause_trace=None):
        """One bounded deterministic token; interpretation owns the wording."""
        rel = self._relationship_of(user_data)
        repair_state = rel.get("repair_state") if isinstance(rel.get("repair_state"), dict) else {}
        hint = interpretation.repair_strategy_block(repair_state)
        if not hint:
            # G2/L9: refusal is a posture token derived from boundary state. It
            # is not a gate and never decides whether a reply is sent.
            try:
                _state = rel.get("state") if isinstance(rel.get("state"), dict) else {}
                _protocol = relationship_meta.refusal_protocol({
                    "boundary_pressure": float(getattr(core, "boundary_pressure", 0.0) or 0.0),
                    "trust": float(_state.get("trust", 0.5) or 0.5),
                    "conflict": float(_state.get("conflict", 0.0) or 0.0),
                })
                hint = interpretation.refusal_strategy_block(_protocol)
            except Exception:
                hint = ""
        if not hint:
            # A4: deterministic empathy token from core affect (no LLM call).
            try:
                hint = interpretation.empathy_strategy_block(core)
            except Exception:
                hint = ""
        if not hint and interpretation.cause_question(text):
            hint = interpretation.cause_trace_block(cause_trace or [])
        if not hint:
            hint = interpretation.memory_receipt_block(memory_meta, text)
        if not hint:
            hint = interpretation.grounding_check_block(memory_meta, text)
        if not hint:
            hint = interpretation.response_strategy_block(events_raw)
        return hint

    async def _maybe_llm_hints(self, event, core, user_data, events_raw, memory_meta, text, cause_trace=None):
        """Optional per-turn strategy refinement; only when a function is ON."""
        parts = [self._deterministic_hint(text, user_data, events_raw, memory_meta, core, cause_trace)]
        rel = self._relationship_of(user_data)
        state = rel.get("state") if isinstance(rel.get("state"), dict) else {}
        repair_state = rel.get("repair_state") if isinstance(rel.get("repair_state"), dict) else {}
        phase = str(repair_state.get("phase") or "stable")
        gate = str((memory_meta or {}).get("gate") or "none")
        try:
            conflict = float(state.get("conflict", 0.5) or 0.5)
            trust = float(state.get("trust", 0.5) or 0.5)
        except Exception:
            conflict, trust = 0.5, 0.5
        try:
            if phase != "stable" and self._llm_v2_cooldown_ok("repair_hint"):
                tag = await self._llm_v2_call(
                    "repair_hint", interpretation.repair_hint_prompt(repair_state),
                    interpretation.parse_repair_hint, event)
                if tag:
                    parts.append("llm_repair=" + tag)
                    self._llm_v2_mark("repair_hint")
            elif events_raw and self._llm_v2_cooldown_ok("empathy_hint"):
                tag = await self._llm_v2_call(
                    "empathy_hint", interpretation.empathy_hint_prompt(events_raw),
                    interpretation.parse_empathy_hint, event)
                if tag:
                    parts.append("llm_empathy=" + tag)
                    self._llm_v2_mark("empathy_hint")
            elif gate in ("semi", "force") and self._llm_v2_cooldown_ok("pragmatics_hint"):
                tag = await self._llm_v2_call(
                    "pragmatics_hint", interpretation.pragmatics_hint_prompt(memory_meta),
                    interpretation.parse_pragmatics_hint, event)
                if tag:
                    parts.append("llm_pragma=" + tag)
                    self._llm_v2_mark("pragmatics_hint")
            elif (conflict < 0.45 and trust > 0.5 and self._llm_v2_cooldown_ok("humor_hint")):
                tag = await self._llm_v2_call(
                    "humor_hint", interpretation.humor_hint_prompt(rel),
                    interpretation.parse_humor_hint, event)
                if tag and tag != "none":
                    parts.append("humor=" + tag)
                    self._llm_v2_mark("humor_hint")
        except Exception as exc:
            logger.warning("[biocore] llm v2 hint failed: %s", exc)
        hint = interpretation.combine_strategy_hint(*parts)
        self._last_strategy_hint = hint
        return hint

    async def _maybe_tom_probe(self, event, core, text, user_data, memory_meta, memory_entries=None):
        """L-T06: optional bounded ToM annotation; never changes core state."""
        if not self._llm_allowed("tom_probe") or not self._llm_v2_cooldown_ok("tom_probe"):
            return
        try:
            recent = [str(h.get("text") or "") for h in self._window_lines(event, 6)]
            refs = [str(x) for x in (memory_entries or []) if str(x)][:6]
            proposal = await self._llm_v2_call(
                "tom_probe",
                interpretation.tom_prompt(user_data, recent, memory_lines=refs),
                lambda raw: interpretation.parse_tom_update(raw, allowed_refs=refs),
                event)
            if not proposal:
                return
            updated = relationship_meta.apply_tom_update(user_data, proposal, allowed_refs=refs)
            if updated:
                self._save_user_record(event, updated)
                self._llm_v2_mark("tom_probe")
        except Exception as exc:
            logger.warning("[biocore] tom probe failed: %s", exc)

    async def _maybe_relationship_impression(self, event, core):
        """L-T01/A3: bounded impression writing; deterministic by default.

        The LLM path stays available behind the per-function switch (default
        OFF). With the switch off, the relation numbers are mapped to a short
        deterministic template. Neither path touches trust or core state.
        """
        if not self._llm_v2_cooldown_ok("relationship_impression"):
            return
        try:
            events = [e for e in self._visible_events(event, self._event_archive(12)) if isinstance(e, dict)]
            important = [e for e in events
                         if float(e.get("importance", 0.0) or 0.0) >= 0.6]
            if len(important) < 3:
                return
            allowed = [str(e.get("id") or "") for e in important if str(e.get("id") or "")]
            if len(allowed) < 3:
                return
            user_data = self._user_record(event)
            current = self._relationship_of(user_data)
            if self._llm_allowed("relationship_impression"):
                proposal = await self._llm_v2_call(
                    "relationship_impression",
                    interpretation.relationship_impression_prompt(important, current),
                    lambda raw: interpretation.parse_relationship_impression(
                        raw, allowed_refs=allowed),
                    event)
                if not proposal:
                    return
            else:
                proposal = interpretation.relationship_impression_template(
                    current, len(important))
                if not proposal.get("traits"):
                    return
                proposal["evidence_refs"] = allowed[:6]
            updated = relationship_meta.apply_relationship_impression(
                current, proposal, allowed_refs=allowed)
            if not updated:
                return
            user_data["relationship"] = updated
            self._save_user_record(event, user_data)
            self._llm_v2_mark("relationship_impression")
        except Exception as exc:
            logger.warning("[biocore] relationship impression failed: %s", exc)

    # ------------------------------------------------------------------
    # Her notebook (step 1-2): only she writes it, once a night, in separate
    # sittings so that what she knows from a private chat stays there by
    # construction (the owner, PR #4 round 3):
    #   * "group": her body's day and what was said openly in the groups;
    #     nothing of any private chat is in its material;
    #   * one sitting per private chat talked in today (at most
    #     NOTEBOOK_PRIVATE_MAX, the busiest): her body's day and that chat's
    #     events; what she writes there belongs to that chat.
    # An entry's origin is all the material of its sitting merged (her own
    # only when that material is her body alone); the model's "uses" never
    # narrows it. Her own "private / can be told" mark is kept, not used.
    # ------------------------------------------------------------------
    def _notebook_time_reached(self, now=None) -> bool:
        if not self._llm_allowed("notebook"):
            return False
        local = time.localtime(time.time() if now is None else now)
        try:
            hh, mm = [int(x) for x in str(getattr(self, "notebook_time", "23:30") or "23:30").split(":")[:2]]
        except Exception:
            hh, mm = 23, 30
        return (local.tm_hour, local.tm_min) >= (hh, mm)

    def _notebook_night(self, now=None) -> dict:
        """Tonight's record: which sittings were tried (marked before each call) and how
        many changes were made, kept in self_model.json so a restart does not call again."""
        date = time.strftime("%Y-%m-%d", time.localtime(time.time() if now is None else now))
        night = (self.self_model or {}).get("notebook_night")
        if not isinstance(night, dict) or night.get("date") != date:
            night = {"date": date, "tried": [], "changes": 0}
            self.self_model["notebook_night"] = night
        return night

    def _today_events(self, now=None) -> list:
        local = time.localtime(time.time() if now is None else now)
        midnight = time.mktime((local.tm_year, local.tm_mon, local.tm_mday, 0, 0, 0, 0, 0, -1))
        return [e for e in reversed(self._event_archive(120))
                if isinstance(e, dict) and float(e.get("ts", 0) or 0) >= midnight]

    def _notebook_sittings(self, now=None) -> list:
        """Tonight's sittings: "group" first, then the busiest private chats with events today."""
        now = time.time() if now is None else now
        places = {}
        for e in self._today_events(now):
            where = discretion.origin_of(e)["where"]
            if where.startswith("private:"):
                places[where] = 0
        local = time.localtime(now)
        midnight = time.mktime((local.tm_year, local.tm_mon, local.tm_mday, 0, 0, 0, 0, 0, -1))
        for place in places:
            places[place] = len([x for x in self._read_window(place)["recent"]
                                 if float(x.get("ts", 0) or 0) >= midnight])
        busiest = sorted(places, key=lambda p: (-places[p], p))[:NOTEBOOK_PRIVATE_MAX]
        return ["group"] + busiest

    def _notebook_materials(self, core, sitting, now=None) -> list:
        """The material of one sitting, each with an id and an origin: her body's day (her
        own), and today's events that belong to it: the groups' open ones for "group"
        (nothing private, nothing of unknown origin), or that private chat's own. At most 13 in
        all, fairly between windows (digest.pick_fairly): each window's weightiest event first."""
        mats = []
        trend = self._body_trend_text(core)
        if trend:
            mats.append({"id": "m1", "text": "身体：" + trend,
                         "origin": discretion.make_origin(discretion.SELF), "names": [], "ref": "body"})
        mine = []
        for e in self._today_events(now):
            origin = discretion.origin_of(e)
            if sitting == "group":
                if origin["visibility"] != discretion.PUBLIC:
                    continue
            elif origin["where"] != sitting or origin["visibility"] != discretion.PRIVATE:
                continue
            mine.append(dict(e, origin=origin))
        for e in digest.pick_fairly(mine, 13 - len(mats)):
            origin = e["origin"]
            body = str(e.get("meaning_to_her") or e.get("reflection") or e.get("small_summary")
                       or e.get("event") or "")
            text = ("%s：%s" % (str(e.get("title") or "一件事"), body)).strip("：")
            mats.append({"id": "m%d" % (len(mats) + 1), "text": "事件：" + text[:160],
                         "origin": origin, "names": discretion.names_in(e), "ref": str(e.get("id") or "")})
        return mats

    @staticmethod
    def _body_trend_text(core) -> str:
        """Today's body in a sentence or two, from the day's running averages (no text kept)."""
        acc = getattr(core, "_daily_accum", None) if core is not None else None
        acc = acc if isinstance(acc, dict) else {}
        n = int(acc.get("n", 0) or 0)
        parts = []
        if n <= 0:
            parts.append("今天没什么人找她说话")
        else:
            v = float(acc.get("v", 0.0) or 0.0) / n
            stress = float(acc.get("stress", 0.0) or 0.0) / n
            parts.append("今天心情不错" if v >= 0.3 else ("今天心里有点沉" if v <= -0.2 else "今天心情平平"))
            if stress >= 0.5:
                parts.append("压力不小")
        talked = float(getattr(core, "talked", 0.0) or 0.0) if core is not None else 0.0
        if talked >= 0.5:
            parts.append("说了不少话")
        return "，".join(parts) + "。"

    @staticmethod
    def _sitting_origin(sitting, materials) -> dict:
        """All the material of the sitting merged; her own only when that is her body alone.
        A private chat's sitting belongs to that chat whatever it was given."""
        others = [m["origin"] for m in materials if m["origin"].get("visibility") != discretion.SELF]
        if sitting != "group":
            people = [p for o in others for p in o.get("people") or []] + [sitting.split(":", 1)[1]]
            ids = [i for o in others for i in o.get("source_ids") or []]
            return discretion.make_origin(sitting, people, ids, discretion.PRIVATE)
        if not others:
            return discretion.make_origin(discretion.SELF)
        return discretion.merge(others)

    @staticmethod
    def _notebook_shown(entries, sitting) -> list:
        """Which entries a sitting sees, as (index, may change it): in "group" her own and
        the open ones, all changeable; in a private chat's, that chat's (changeable) and her
        own, which it only reads: a private chat never takes one of her own thoughts in."""
        shown = []
        for i, x in enumerate(entries):
            o = discretion.origin_of(x)
            own = o["visibility"] == discretion.SELF or o["where"] == discretion.SELF
            if sitting == "group" and (own or o["visibility"] == discretion.PUBLIC):
                shown.append((i, True))
            elif sitting != "group" and o["where"] == sitting:
                shown.append((i, True))
            elif sitting != "group" and own:
                shown.append((i, False))
        return shown

    async def _maybe_write_notebook(self, now=None) -> bool:
        """Tonight's sittings after notebook_time (local), each at most once a day: a sitting
        is marked as tried before its call, so a failure or a restart does not call again.
        At most NOTEBOOK_EDITS changes a night and NOTEBOOK_MAX entries in all."""
        if not self._notebook_time_reached(now):
            return False
        now = time.time() if now is None else now
        night = self._notebook_night(now)
        core = self._core(None)
        persona = await self._persona_text(None)
        wrote = False
        for sitting in self._notebook_sittings(now):
            budget = NOTEBOOK_EDITS - int(night.get("changes", 0) or 0)
            if sitting in night["tried"] or budget <= 0:
                continue
            if sitting != "group" and len([s for s in night["tried"] if s != "group"]) >= NOTEBOOK_PRIVATE_MAX:
                break
            night["tried"].append(sitting)
            self._save_self_model()
            entries = [x for x in (self.self_model.get("notebook") or []) if isinstance(x, dict)]
            shown = self._notebook_shown(entries, sitting)
            materials = self._notebook_materials(core, sitting, now)
            changes = await self._llm_v2_call(
                "notebook",
                interpretation.notebook_prompt([(entries[i].get("text"), may) for i, may in shown], materials,
                                               sitting != "group", NOTEBOOK_MAX, NOTEBOOK_CHARS, budget),
                lambda raw: interpretation.parse_notebook_changes(
                    raw, len(shown), [m["id"] for m in materials], NOTEBOOK_CHARS, budget),
                None, system_prompt=persona or None)
            if not changes or self._job_stale():
                continue
            origin = self._sitting_origin(sitting, materials)
            names = sorted({n for m in materials for n in (m.get("names") or [])})
            refs = {m["id"]: m["ref"] for m in materials}
            entries = [x for x in (self.self_model.get("notebook") or []) if isinstance(x, dict)]
            gone = set()
            for change in changes:
                mark = {"private_mark": change.get("private")}
                # what she writes is kept like the rest: someone deleted is 某人
                text = self._without_gone(change.get("text")) if change["op"] != "delete" else ""
                uses = [refs[x] for x in (change.get("uses") or []) if x in refs]
                if change["op"] in ("edit", "delete"):
                    i, may = shown[change["no"] - 1]
                    if not may:
                        continue  # one of her own thoughts, seen from a private chat: read only
                if change["op"] == "delete":
                    gone.add(i)
                elif change["op"] == "edit":
                    old = entries[i]
                    entries[i] = dict(old, text=text, ts=now, uses=uses, sitting=sitting,
                                      origin=self._sitting_origin_with(origin, old),
                                      names=sorted(set(names) | set(old.get("names") or [])), **mark)
                elif len(entries) - len(gone) < NOTEBOOK_MAX:
                    entries.append({"id": _sha256("%s|%s|%s" % (now, sitting, change["text"]))[:12],
                                    "text": text, "ts": now, "origin": origin, "names": names,
                                    "uses": uses, "sitting": sitting, **mark})
                else:
                    continue
                night["changes"] = int(night.get("changes", 0) or 0) + 1
            self.self_model["notebook"] = [x for i, x in enumerate(entries) if i not in gone][:NOTEBOOK_MAX]
            self._save_self_model()
            logger.info("[ams-life] notebook (%s): %d change(s)", "group" if sitting == "group" else "private",
                        len(changes))
            wrote = True
        return wrote

    @staticmethod
    def _sitting_origin_with(origin, old) -> dict:
        """An edited entry: this sitting's origin and the entry's own, merged (her own part
        never widens it)."""
        both = [o for o in (origin, discretion.origin_of(old)) if o.get("visibility") != discretion.SELF]
        return discretion.merge(both) if both else discretion.make_origin(discretion.SELF)

    async def _maybe_relationship_narrative(self, event, core):
        """L-T12: manual/periodic bounded relationship narrative (default OFF)."""
        if not self._llm_allowed("relationship_narrative"):
            return
        if not self._llm_v2_cooldown_ok("relationship_narrative"):
            return
        try:
            user_data = self._user_record(event)
            rel = self._relationship_of(user_data)
            marks = [m for m in (rel.get("milestones") or []) if isinstance(m, dict)]
            allowed = [str(m.get("key") or m.get("type") or "") for m in marks
                       if str(m.get("key") or m.get("type") or "")]
            if not allowed:
                return
            parsed = await self._llm_v2_call(
                "relationship_narrative",
                interpretation.relationship_narrative_prompt(rel),
                lambda raw: interpretation.parse_relationship_narrative(
                    raw, allowed_refs=allowed), event)
            if not parsed:
                return
            if self._job_stale():
                return
            items = self.self_model.get("relationship_narratives")
            if not isinstance(items, list):
                items = []
            _sid, _name = self._speaker(event)
            # its sources: those of the milestones it was written from
            _used = set(parsed["evidence_refs"] or [])
            _sources = [s for m in marks if str(m.get("key") or m.get("type") or "") in _used
                        for s in (m.get("source_ids") or [])]
            _source_origins = [discretion.origin_of(x) for x in self._read_window(self._here(event))["recent"]
                               if discretion.is_about(discretion.origin_of(x), source_ids=_sources)]
            _source_origins += [discretion.origin_of(x) for x in self._read_library().get("entries", [])
                                if discretion.is_about(discretion.origin_of(x), source_ids=_sources)]
            _source_origins += [discretion.origin_of(x) for x in self._event_archive(1000)
                                if discretion.is_about(discretion.origin_of(x), source_ids=_sources)]
            _visibility = (discretion.PRIVATE if any(o["visibility"] == discretion.PRIVATE
                                                     for o in _source_origins) else None)
            items.append({"ts": time.time(), "text": parsed["narrative"],
                          "evidence_refs": parsed["evidence_refs"],
                          "origin": discretion.make_origin(self._here(event), [_sid], _sources, _visibility)})
            self.self_model["relationship_narratives"] = items[-5:]
            self._save_self_model()
            self._llm_v2_mark("relationship_narrative")
        except Exception as exc:
            logger.warning("[biocore] relationship narrative failed: %s", exc)

    def _sees_images(self, provider) -> bool:
        """Check configured modalities, or guess by name when they are absent."""
        cfg = getattr(provider, "provider_config", None)
        mods = cfg.get("modalities") if isinstance(cfg, dict) else None
        if isinstance(mods, (list, tuple)):
            return "image" in [str(m).strip().lower() for m in mods]
        return self._provider_kind(provider) == "vision"

    def _vision_provider_for(self, event=None):
        """Use the selected vision provider, then AstrBot defaults, then capable chat."""
        _cfg = self._function_cfg("image_caption")
        _override = _cfg["provider"]
        if _override == "image_api":
            if not str((getattr(self, "config", {}) or {}).get("vision_image_api_model") or "").strip():
                return None
            return VisionGate(self, _counted(self, "vision", ImageAPI(self)), event)
        _tried = []
        if _override and _override not in ("follow_llm", "main", "default", ""):
            _tried.append(_override)
        try:
            _cfg_all = self.context.get_config()
            _ps = _cfg_all.get("provider_settings", {}) if isinstance(_cfg_all, dict) else {}
            _def = str(_ps.get("default_image_caption_provider_id") or "")
        except Exception:
            _def = ""
        if _def and _def not in _tried:
            _tried.append(_def)
        for _pid in _tried:
            try:
                _vp = self.context.get_provider_by_id(_pid)
            except Exception as exc:
                logger.warning("[biocore] vision provider lookup failed (%s): %s", _pid, exc)
                continue
            if _vp is not None and self._sees_images(_vp):
                return VisionGate(self, _counted(self, "vision", _vp), event) if hasattr(self, "_load_image_cache") else _counted(self, "vision", _vp)
            if _vp is not None:
                logger.warning("[biocore] image_caption provider %s is not a vision provider; ignored", _pid)
        try:
            _umo = str(getattr(event, "unified_msg_origin", "") or "") if event is not None else None
            _chat = self.context.get_using_provider(_umo)
        except Exception:
            _chat = None
        if _chat is not None and self._sees_images(_chat):
            return VisionGate(self, _counted(self, "vision", _chat), event) if hasattr(self, "_load_image_cache") else _counted(self, "vision", _chat)
        return None

    async def _compile_profile(self, event):
        text = await self._persona_text(event)
        if not text:
            self.profile = dict(DEFAULT_PROFILE)
            self.persona_text = ""
            self.schema_texts = []
            try:
                PROFILE_PATH.write_text(json.dumps(
                    {"persona": "", "profile": self.profile, "schema": [],
                     "style": dict(getattr(self, "persona_style", {}) or {})},
                    ensure_ascii=False, indent=1), encoding="utf-8")
            except Exception:
                pass
            return
        if not self._llm_allowed("persona_compile"):
            self.persona_text = text
            logger.info("[biocore] persona_compile disabled; keep saved profile")
            return
        _ph = _sha256(text)
        if getattr(self, "_persona_compiled_hash", "") == _ph and getattr(self, "profile", None):
            # Already compiled for this persona: no extra LLM call.
            self.persona_text = text
            logger.info("[biocore] persona already compiled; skip")
            return
        try:
            provider = await self._provider_for("persona_compile", event)
            if provider is None:
                self.profile = dict(DEFAULT_PROFILE)
                return
            # Prompt construction and output validation belong to the
            # interpretation layer; this wiring only calls it.
            system = interpretation.persona_compile_system()
            prompt = interpretation.persona_compile_prompt(text)
            resp = await provider.text_chat(prompt=prompt, system_prompt=system)
            raw = str(getattr(resp, "completion_text", "") or "")
            _compiled = interpretation.parse_persona_compile(raw, DEFAULT_PROFILE)
            self.profile = _compiled.get("profile") or dict(DEFAULT_PROFILE)
            self.schema_texts = list(_compiled.get("schema") or [])
            _style = _compiled.get("style") if isinstance(_compiled.get("style"), dict) else {}
            self.persona_style = {"intimacy_style": str(_style.get("intimacy_style") or "neutral"),
                                  "address_terms": list(_style.get("address_terms") or [])[:3]}
            logger.info("[biocore] persona schema slots=%s style=%s", len(self.schema_texts),
                        self.persona_style.get("intimacy_style"))
        except Exception as exc:
            logger.warning("[biocore] persona compile failed: %s", exc)
            self.profile = dict(DEFAULT_PROFILE)
        self.persona_text = text
        try:
            PROFILE_PATH.write_text(json.dumps(
                {"persona": self.persona_text, "profile": self.profile,
                 "schema": list(getattr(self, "schema_texts", []) or []),
                 "style": dict(getattr(self, "persona_style", {}) or {}),
                 "persona_hash": _sha256(self.persona_text or text)},
                ensure_ascii=False, indent=1), encoding="utf-8")
            self._persona_compiled_hash = _sha256(self.persona_text or text)
            logger.info("[biocore] first-run profile written: %s", PROFILE_PATH)
        except Exception as exc:
            logger.warning("[biocore] profile save failed: %s", exc)
