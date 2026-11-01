# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Shared startup for the plugin and the platform-neutral shell."""
try:
    from .common import *  # noqa: F401,F403
    from .body import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
    from body import *  # noqa: F401,F403


# ams-life step 1-2: body fields of older state files that are gone.
_OLD_BODY_FIELDS = ("trust", "circadian_alertness", "user_trust_seeded", "user_trust_seed_delta",
                    "reflection_tree")
_OLD_HOMEOSTASIS_FIELDS = ("body", "need_pyramid", "interoception", "last_metabolic_cost")


class CoreMixin:
    def _core_init(self, context, config=None) -> None:
        """The plugin's own start: settings, migrations and the panel API."""
        self.context = context
        self.config = config or {}
        self.enabled = bool(self.config.get("enabled", True))
        self.inject_intent = bool(self.config.get("inject_intent", True))
        try:
            self.summary_max_chars = max(0, int(self.config.get("summary_max_chars", 0) or 0))
        except Exception:
            self.summary_max_chars = 0
        self.voice_transcription_enabled = bool(self.config.get("voice_transcription_enabled", True))
        # ams-life step 1-2: when she writes her notebook (local time; switch: the
        # "notebook" LLM function, off by default)
        self.notebook_time = str(self.config.get("notebook_time", "23:30") or "23:30").strip()
        # ams-life step 1-3: when the group members she knows are updated (switch: the
        # "group_impressions" LLM function, off by default); what they are called joins
        # the names made anonymous elsewhere
        self.impressions_time = str(self.config.get("impressions_time", "23:15") or "23:15").strip()
        # ams-life: when she goes over what happened today in each window (switch: the
        # "daily_digest" LLM function, off by default); before the impressions and the notebook
        self.digest_time = str(self.config.get("digest_time", "23:05") or "23:05").strip()
        # the red lines: one switch, off by default (the owner, 10-28: nothing is held back in
        # the first version; the hits are counted by line for the owner to look at)
        self.redline_filter = bool(self.config.get("redline_filter", False))
        # step 2: one memory everywhere, each thing labelled with what she may say of it
        # where she is (off by default; the owner turns it on after the third replay)
        self.global_memory = bool(self.config.get("global_memory", False))
        # step 2 (甲): she decides herself whether to answer (off by default; off, AstrBot decides
        # as before: an @ of her, "/", every private message)
        self.self_decide = bool(self.config.get("self_decide", False))
        self.reply_in_pieces = bool(self.config.get("reply_in_pieces", True))
        self.mood_events_enabled = bool(self.config.get("mood_events_enabled", False))
        # step 2 (丙): her stickers -- she keeps the ones she likes and sends them (off by default;
        # looking at pictures, image_caption, has to be on too)
        self.stickers_enabled = bool(self.config.get("stickers_enabled", False))
        self.browse_groups_enabled = bool(self.config.get("browse_groups_enabled", False))
        # step 2 (丁): her browser -- in a reply, two read-only tools of the plugin's own (off by default)
        self.browse_enabled = bool(self.config.get("browse_enabled", False))
        self.browser_enabled = bool(self.config.get("browser_enabled", False))
        self.browser_interactive_enabled = bool(self.config.get("browser_interactive_enabled", False))
        self.browse_trips_enabled = bool(self.config.get("browse_trips_enabled", False))
        self.register_name_source(self._impression_names)
        try:
            self.event_summary_delay_hours = max(0, int(self.config.get("event_summary_delay_hours", 6) or 6))
        except Exception:
            self.event_summary_delay_hours = 6
        self.proactive_reply = bool(self.config.get("proactive_reply", False))
        # Task-15: noise -> autonomy. Both default false; when off no readiness
        # is computed, no background task starts, and no message can be sent.
        self.proactive_autonomy = bool(self.config.get("proactive_autonomy", False))
        self.proactive_send = bool(self.config.get("proactive_send", False))
        # Task-28: minimal autonomy loop (default OFF; private-only; token-only).
        self.autonomy_loop_enabled = bool(self.config.get("autonomy_loop_enabled", False))
        self.autonomy_loop_theta_ig = self._loop_cfg_float(
            "autonomy_loop_theta_ig", AUTONOMY_LOOP_THETA_IG,
            AUTONOMY_LOOP_THETA_MIN, AUTONOMY_LOOP_THETA_MAX)
        self.autonomy_loop_margin = self._loop_cfg_float(
            "autonomy_loop_margin", AUTONOMY_LOOP_MARGIN,
            AUTONOMY_LOOP_MARGIN_MIN, AUTONOMY_LOOP_MARGIN_MAX)
        self.autonomy_loop_k_delay = self._loop_cfg_float(
            "autonomy_loop_k_delay", AUTONOMY_LOOP_K_DELAY,
            AUTONOMY_LOOP_K_MIN, AUTONOMY_LOOP_K_MAX)
        self.autonomy_loop_ior_seconds = self._loop_cfg_float(
            "autonomy_loop_ior_seconds", AUTONOMY_LOOP_IOR_SECONDS,
            AUTONOMY_LOOP_IOR_MIN, AUTONOMY_LOOP_IOR_MAX)
        self.autonomy_loop_c0 = self._loop_cfg_float(
            "autonomy_loop_c0", AUTONOMY_LOOP_C0, 0.0, 1.0)
        self.autonomy_loop_c1 = self._loop_cfg_float(
            "autonomy_loop_c1", AUTONOMY_LOOP_C1, 0.0, 1.0)
        self.autonomy_loop_c2 = self._loop_cfg_float(
            "autonomy_loop_c2", AUTONOMY_LOOP_C2, 0.0, 1.0)
        self.autonomy_loop_token_only = bool(
            self.config.get("autonomy_loop_token_only", True))
        # Stage-2: C8+C9 goal<->appraisal closed loop (default OFF = 1.2.98).
        self.bio_feedback_loops = bool(self.config.get("bio_feedback_loops", False))
        # Task-20: L1 learning defaults ON with small steps + hard bounds.
        self.bio_learning = bool(self.config.get("bio_learning", True))
        _rm = str(self.config.get("retention_model", "single") or "single")
        self.retention_model = _rm if _rm in LEARNING_RETENTION_MODELS else "single"
        # Batch4 attention flags: all default OFF = pure 1.2.98 no-op.
        self.attention_gate_enabled = bool(self.config.get("attention_gate_enabled", False))
        try:
            self.attention_gate_s = max(0.20, min(0.40, float(self.config.get("attention_gate_s", 0.30) or 0.30)))
        except Exception:
            self.attention_gate_s = 0.30
        try:
            self.attention_gate_shift = max(-0.20, min(0.20, float(self.config.get("attention_gate_shift", 0.0) or 0.0)))
        except Exception:
            self.attention_gate_shift = 0.0
        self.fan_penalty_enabled = bool(self.config.get("fan_penalty_enabled", False))
        try:
            self.fan_cap = max(1, min(64, int(self.config.get("fan_cap", 32) or 32)))
        except Exception:
            self.fan_cap = 32
        try:
            self.fan_gain = max(0.05, min(0.20, float(self.config.get("fan_gain", 0.10) or 0.10)))
        except Exception:
            self.fan_gain = 0.10
        try:
            self.fan_floor = max(0.50, min(0.85, float(self.config.get("fan_floor", 0.70) or 0.70)))
        except Exception:
            self.fan_floor = 0.70
        self.cowan_capacity_enabled = bool(self.config.get("cowan_capacity_enabled", False))
        try:
            self.cowan_capacity = max(3, min(6, int(self.config.get("cowan_capacity", 4) or 4)))
        except Exception:
            self.cowan_capacity = 4
        self.attention_topk_cap_enabled = bool(self.config.get("attention_topk_cap_enabled", False))
        try:
            self.attention_topk_cap = max(3, min(6, int(self.config.get("attention_topk_cap", 4) or 4)))
        except Exception:
            self.attention_topk_cap = 4
        # Batch5 H2: event chain (default OFF; H2-3 multi-hop also OFF).
        self.attention_gate_mode = str(self.config.get("attention_gate_mode", "hard") or "hard").lower()
        if self.attention_gate_mode not in ("hard", "probabilistic"):
            self.attention_gate_mode = "hard"
        try:
            self.attention_seed = int(self.config.get("attention_seed", 0) or 0)
        except Exception:
            self.attention_seed = 0
        # H2-2 budget is independent of the H2-1 edge switch.
        self.chain_budget_enabled = bool(self.config.get("chain_budget_enabled", False))
        self.memory_chain_enabled = bool(self.config.get("memory_chain_enabled", False))
        self.salience_boost_enabled = bool(self.config.get("salience_boost_enabled", False))
        self.sentence_dedup_enabled = bool(self.config.get("sentence_dedup_enabled", False))
        self.embedding_cache_enabled = bool(self.config.get("embedding_cache_enabled", True))
        try:
            self.embedding_timeout_ms = max(100, min(15000, int(
                self.config.get("embedding_timeout_ms", EMBED_TIMEOUT_MS_DEFAULT)
                or EMBED_TIMEOUT_MS_DEFAULT)))
        except Exception:
            self.embedding_timeout_ms = EMBED_TIMEOUT_MS_DEFAULT
        self.memory_chain_multihop = bool(self.config.get("memory_chain_multihop", False))
        try:
            self.chain_hops = max(1, min(2, int(self.config.get("chain_hops", 2) or 2)))
        except Exception:
            self.chain_hops = 2
        try:
            self.chain_fan_out = max(1, min(3, int(self.config.get("chain_fan_out", 3) or 3)))
        except Exception:
            self.chain_fan_out = 3
        try:
            self.chain_decay = max(0.4, min(0.6, float(self.config.get("chain_decay", 0.5) or 0.5)))
        except Exception:
            self.chain_decay = 0.5
        try:
            self.chain_max_new = max(1, min(6, int(self.config.get("chain_max_new", 6) or 6)))
        except Exception:
            self.chain_max_new = 6
        try:
            self.noise_seed = int(self.config.get("noise_seed", 0) or 0)
        except Exception:
            self.noise_seed = 0
        self._autonomy_task = None
        self._autonomy_private_sessions = {}
        # A1: event ranking is deterministic by default; the optional LLM rerank
        # follows the global rerank provider only when this switch is turned on.
        self.event_ranking_llm = bool(self.config.get("event_ranking_llm", False))
        # D5: stable default shape even before the first recall fills it.
        self._last_memory_trace = dict(DEFAULT_MEMORY_TRACE)
        self.memory_dedup_embedding = bool(self.config.get("memory_dedup_embedding", True))
        # task-33: deterministic memory-point worthiness gate (default ON).
        # OFF = exact legacy behaviour (archive every candidate, no new fields).
        self.memory_worthiness_enabled = bool(
            self.config.get("memory_worthiness_enabled", True))
        # Safety switch: default OFF for private use. When OFF, no masking,
        # no cross-session isolation, no forced abstention, no poison filter.
        self.safety_enabled = bool(self.config.get("safety_enabled", False))
        # ams-life: recall from other groups/private chats no longer follows
        # safety_enabled; every item goes through the discretion table instead.
        self.sensitive_memory_protection = self.safety_enabled
        # Hybrid lexical+MMR retrieval and LLM-proposed write candidates.
        self.hybrid_retrieval = bool(self.config.get("hybrid_retrieval", True))
        self.llm_memory_candidates = bool(self.config.get("llm_memory_candidates", True))
        # B-T02 we-memory is evidence-gated and OFF by default (needs real
        # shared-ritual evidence before it writes relationship state).
        self.we_memory_enabled = bool(self.config.get("we_memory_enabled", False))
        # L-T02..L-T12 bounded runtime state. Only the last trace/hint is kept
        # in memory; no prompt text is stored and no reply is generated.
        self._last_cause_trace = []
        self._last_strategy_hint = ""
        self._last_memory_entries = []
        self._llm_v2_last = {}
        # LLM scope: user requirement is "LLM only for reply + summary".
        # When true, BioCore only calls the LLM for event/memory summaries;
        # persona compile / event ranking / reflection / image caption are
        # skipped (deterministic fallbacks where available).
        self.llm_only_reply_summary = bool(
            self.config.get("llm_only_reply_summary", True))
        self.llm_functions = {
            _name: {"enabled": LLM_FUNCTION_DEFAULTS[_name],
                    "provider": "follow_llm"}
            for _name in LLM_FUNCTIONS
        }
        self.first_run_persona_compile = bool(self.config.get("first_run_persona_compile", True))
        self.kb_enabled = bool(self.config.get("kb_enabled", False))
        _names = self.config.get("kb_names", [])
        self.kb_names = [str(x).strip() for x in _names] if isinstance(_names, (list, tuple)) else []
        self.cores = {}
        self._consolidating = False
        self._last_consolidation = 0.0
        self._last_event_archive = 0.0
        self._last_reflection = 0.0
        try:
            self.reflection_interval_hours = max(1, int(self.config.get("reflection_interval_hours", 6) or 6))
        except Exception:
            self.reflection_interval_hours = 6
        # Event-driven insight trigger: fallback is a 24h ultra-long safety net,
        # not a periodic 6h main trigger anymore.
        self._insight_fallback_hours = max(INSIGHT_FALLBACK_HOURS, int(self.reflection_interval_hours))
        # Tunable thresholds (defaults match the constants above; AstrBot plugin
        # config exposes insight_min_new_events / insight_cooldown_minutes).
        try:
            self._insight_min_new_events = max(
                1, int(self.config.get("insight_min_new_events", INSIGHT_MIN_NEW_EVENTS)
                       or INSIGHT_MIN_NEW_EVENTS))
        except Exception:
            self._insight_min_new_events = INSIGHT_MIN_NEW_EVENTS
        try:
            self._insight_cooldown_minutes = max(
                1, int(self.config.get("insight_cooldown_minutes", INSIGHT_COOLDOWN_SECONDS // 60)
                       or (INSIGHT_COOLDOWN_SECONDS // 60)))
        except Exception:
            self._insight_cooldown_minutes = INSIGHT_COOLDOWN_SECONDS // 60
        # Long-term pattern insight: main entry is the manual dashboard button;
        # automatic generation is opt-in and OFF by default.
        self.insight_auto_enabled = bool(self.config.get("insight_auto_enabled", False))
        try:
            self.stimulus_decay_seconds = max(30, int(self.config.get("stimulus_decay_seconds", 300) or 300))
            self.stimulus_habituation = max(0.0, float(self.config.get("stimulus_habituation", 0.75) or 0.75))
        except Exception:
            self.stimulus_decay_seconds = 300
            self.stimulus_habituation = 0.75
        self.image_recognition_enabled = bool(self.config.get("image_recognition_enabled", True))
        try:
            self.image_service_idle_seconds = max(30, int(self.config.get("image_service_idle_seconds", 120) or 120))
        except Exception:
            self.image_service_idle_seconds = 120
        try:
            self.image_cache_max_entries = max(20, int(self.config.get("image_cache_max_entries", 500) or 500))
        except Exception:
            self.image_cache_max_entries = 500
        def _configured_path(key):
            raw = str(self.config.get(key, "") or "").strip()
            return Path(raw) if raw else None
        self.image_llama_server = _configured_path("image_llama_server")
        self.image_llama_model = _configured_path("image_llama_model")
        self.image_llama_mmproj = _configured_path("image_llama_mmproj")
        try:
            _raw_port = int(self.config.get("image_service_port", 0) or 0)
            self.image_service_port = _raw_port if _raw_port > 0 else 0
        except Exception:
            self.image_service_port = 0
        # Lazy image-service process/lock state (initialized here so the
        # first image request does not AttributeError).
        self._image_proc = None
        self._image_last_used = 0.0
        self._image_service_lock = None
        _triggers = self.config.get("image_trigger_words", [])
        self.image_trigger_words = ([str(x).strip() for x in _triggers if str(x).strip()]
                                    if isinstance(_triggers, (list, tuple)) else [])
        try:
            self.valence_decay_minutes = max(1.0, float(self.config.get("valence_decay_minutes", 120) or 120))
        except Exception:
            self.valence_decay_minutes = 120.0
        try:
            self.arousal_decay_minutes = max(1.0, float(self.config.get("arousal_decay_minutes", 30) or 30))
        except Exception:
            self.arousal_decay_minutes = 30.0
        try:
            self.social_decay_minutes = max(1.0, float(self.config.get("social_decay_minutes", 180) or 180))
        except Exception:
            self.social_decay_minutes = 180.0
        self.stimuli = []
        self.profile = None
        self.persona_text = ""
        # Persona selection: empty = follow AstrBot default persona.
        self.persona_id = str(self.config.get("persona_id") or "").strip()
        # Hash of the persona text whose numeric profile was compiled; lets
        # strict LLM mode still compile ONCE on first run / persona change.
        self._persona_compiled_hash = ""
        # Schema slots proposed once by the persona compiler (bounded strings).
        self.schema_texts = []
        # L-T07: bounded persona style slots proposed by the compiler (never
        # prompt text; the interpretation layer stays the only prompt owner).
        self.persona_style = {"intimacy_style": "neutral", "address_terms": []}
        self.self_model = self._load_self_model()
        if not isinstance(self.self_model.get("diary"), list):
            self.self_model["diary"] = []
        if not isinstance(self.self_model.get("relationship_narratives"), list):
            self.self_model["relationship_narratives"] = []
        self.api_config = {}
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        try:
            self._migrate_state_files()
            self._migrate_body_fields()
            self._migrate_memory_library()
        except Exception as exc:
            logger.warning("[ams-life] one-her migration failed: %s", exc)
        try:
            self._migrate_memory_ids()  # an id of its own for every memory; vectors out of the library
        except Exception as exc:
            logger.warning("[ams-life] memory id / vector migration failed: %s", exc)
        try:
            self._remove_gone_at_start()  # someone deleted is taken out of what she keeps (copies archived first)
        except Exception as exc:
            logger.warning("[ams-life] number migration failed: %s", exc)
        try:
            self._sweep_red_lines()  # the switch on: what crosses a red line goes (copies archived first)
        except Exception as exc:
            logger.warning("[ams-life] red-line sweep failed: %s", exc)
        try:
            self._sweep_windows()  # expired phone lines leave the disk at start-up
            self._ensure_autonomy_task()  # and every tick after (the 5-minute loop)
        except Exception as exc:
            logger.warning("[ams-life] phone sweep failed: %s", exc)
        self._load_profile()
        self._load_settings()
        if "kb_enabled" in self.config:
            self.kb_enabled = bool(self.config.get("kb_enabled"))
        if "kb_names" in self.config:
            _n = self.config.get("kb_names")
            if isinstance(_n, (list, tuple)):
                self.kb_names = [str(x).strip() for x in _n if str(x).strip()]
        self._load_api_config()
        self._register_page_api()
        try:
            self._cleanup_duplicate_events()
        except Exception as exc:
            logger.warning("[biocore] dedupe init failed: %s", exc)
        try:
            _d = self._public_api_config()
            logger.info("[biocore] api defaults llm=%s embedding=%s rerank=%s",
                        (_d.get("llm") or {}).get("provider_id"),
                        (_d.get("embedding") or {}).get("provider_id"),
                        (_d.get("rerank") or {}).get("provider_id"))
        except Exception as exc:
            logger.warning("[biocore] api defaults probe failed: %s", exc)

    def _migrate_state_files(self) -> None:
        """ams-life: start the single body from the most recently updated per-session state.

        Every old states/<session>.json is moved into STATE_ARCHIVE_DIR, never deleted.
        What was said in a session (reply lines, open loops) goes into that
        session's window in her phone; the body keeps no text. A one-body state
        written before the phone existed is split the same way, its old file
        kept in the archive as her.before_phone.json.
        """
        if HER_STATE_PATH.exists():
            state = json.loads(HER_STATE_PATH.read_text(encoding="utf-8"))
            if not self._body_state_has_text(state):
                return
            STATE_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            kept = STATE_ARCHIVE_DIR / "her.before_phone.json"
            if not kept.exists():
                shutil.copy2(str(HER_STATE_PATH), str(kept))
            self._move_body_texts_to_phone(state)
            HER_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
            logger.info("[ams-life] phone: moved the texts kept in the body into their windows")
            return
        old = sorted((f for f in STATE_DIR.glob("*.json") if f.is_file()),
                     key=lambda f: f.stat().st_mtime, reverse=True)
        if not old:
            return
        state = None
        for f in old:
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            self._move_body_texts_to_phone(d, f.stem)
            if state is None:
                state = d
        HER_STATE_PATH.write_text(json.dumps(state if isinstance(state, dict) else {}, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
        STATE_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        for f in old:
            shutil.move(str(f), str(STATE_ARCHIVE_DIR / f.name))
        logger.info("[ams-life] one body: started from %s, archived %d per-session states", old[0].name, len(old))

    def _migrate_body_fields(self) -> None:
        """ams-life step 1-2: an electronic ghost's body. A state file written before it
        still has the day-night rhythm, the global trust, the virtual body (energy,
        hydration, warmth, fatigue), the need pyramid, interoception and the insight
        tree; they are dropped. The old file is kept as her.before_body.json."""
        if not HER_STATE_PATH.exists():
            return
        state = json.loads(HER_STATE_PATH.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            return
        homeo = state.get("homeostasis") if isinstance(state.get("homeostasis"), dict) else {}
        if not (any(k in state for k in _OLD_BODY_FIELDS) or any(k in homeo for k in _OLD_HOMEOSTASIS_FIELDS)):
            return
        STATE_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        kept = STATE_ARCHIVE_DIR / "her.before_body.json"
        if not kept.exists():
            shutil.copy2(str(HER_STATE_PATH), str(kept))
        for k in _OLD_BODY_FIELDS:
            state.pop(k, None)
        if homeo:
            state["homeostasis"] = homeostasis.normalize_state(homeo)
        HER_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        logger.info("[ams-life] body: dropped the old physiology, global trust and insight tree")

    def _core(self, event=None) -> BioCore:
        try:
            from . import life_loop
        except ImportError:
            import life_loop
        # ams-life: one her. Every group and private chat shares this one body.
        key = "her"
        if key not in self.cores:
            core = BioCore(self.profile or DEFAULT_PROFILE)
            try:
                core.valence_decay_minutes = float(getattr(self, "valence_decay_minutes", 120.0))
                core.arousal_decay_minutes = float(getattr(self, "arousal_decay_minutes", 30.0))
                core.social_decay_minutes = float(getattr(self, "social_decay_minutes", 180.0))
            except Exception:
                pass
            try:
                if HER_STATE_PATH.exists():
                    core.load_state(json.loads(HER_STATE_PATH.read_text(encoding="utf-8")))
            except Exception:
                pass
            # Task-15: readiness is owned by plugin config, never restored from
            # state; the optional noise seed is applied only when autonomy is on.
            core.autonomy_enabled = bool(getattr(self, "proactive_autonomy", False))
            # Task-28: loop switch + tuning are config-owned, never restored from
            # the state file; re-applied on every core build/config reload.
            core.autonomy_loop_enabled = bool(
                getattr(self, "autonomy_loop_enabled", False))
            core.autonomy_loop_theta_ig = self._loop_cfg_float(
                "autonomy_loop_theta_ig", AUTONOMY_LOOP_THETA_IG,
                AUTONOMY_LOOP_THETA_MIN, AUTONOMY_LOOP_THETA_MAX)
            core.autonomy_loop_margin = self._loop_cfg_float(
                "autonomy_loop_margin", AUTONOMY_LOOP_MARGIN,
                AUTONOMY_LOOP_MARGIN_MIN, AUTONOMY_LOOP_MARGIN_MAX)
            core.autonomy_loop_k_delay = self._loop_cfg_float(
                "autonomy_loop_k_delay", AUTONOMY_LOOP_K_DELAY,
                AUTONOMY_LOOP_K_MIN, AUTONOMY_LOOP_K_MAX)
            core.autonomy_loop_ior_seconds = self._loop_cfg_float(
                "autonomy_loop_ior_seconds", AUTONOMY_LOOP_IOR_SECONDS,
                AUTONOMY_LOOP_IOR_MIN, AUTONOMY_LOOP_IOR_MAX)
            core.autonomy_loop_c0 = self._loop_cfg_float(
                "autonomy_loop_c0", AUTONOMY_LOOP_C0, 0.0, 1.0)
            core.autonomy_loop_c1 = self._loop_cfg_float(
                "autonomy_loop_c1", AUTONOMY_LOOP_C1, 0.0, 1.0)
            core.autonomy_loop_c2 = self._loop_cfg_float(
                "autonomy_loop_c2", AUTONOMY_LOOP_C2, 0.0, 1.0)
            core.autonomy_loop_token_only = bool(
                getattr(self, "autonomy_loop_token_only", True))
            core.bio_feedback_loops = bool(
                getattr(self, "bio_feedback_loops", False))
            core.bio_learning = bool(getattr(self, "bio_learning", True))
            core.retention_model = str(
                getattr(self, "retention_model", "power_law") or "power_law")
            if core.autonomy_enabled or core.autonomy_loop_enabled:
                try:
                    _seed = int(getattr(self, "noise_seed", 0) or 0)
                    core._noise_seed = max(0, _seed)
                    if _seed > 0:
                        core._rng = __import__("random").Random(_seed)
                except Exception:
                    pass
            self._refresh_loop_pressure(core)
            self.cores[key] = core
        core = self.cores[key]
        if life_loop.enabled(self):
            life_loop.bind_body(core)
        else:
            core.__dict__.pop('_life_now_path', None)
            core.__dict__.pop('_life_state_path', None)
        return core
