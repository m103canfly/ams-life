# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""AstrBot BioCore plugin: a standalone biological emotion layer.

Independent copy. It does not import the Desktop companion project.
First run: read the current AstrBot persona, compile it once with the current
provider into a numeric profile, store it under this plugin's data dir.
Then on every LLM request: append a compact intent, on response: feedback.

Noise -> autonomy boundary (task-15): proactive_autonomy/proactive_send default
false. When off, readiness is not computed, no background task starts, no message
is sent, and the legacy noise/state trajectory is unchanged. All readiness math
lives in the L1 BioCore (autonomy_state); the plugin only feeds raw module deltas
and reads the resulting state for the command/UI. Group chats never trigger.
"""
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
    from . import attention
except ImportError:
    from mixin_attention import AttentionMixin
    import attention
try:
    from .mixin_browse import BrowseMixin
except ImportError:
    from mixin_browse import BrowseMixin


# ams-life step 1-2: body fields of older state files that are gone.
_OLD_BODY_FIELDS = ("trust", "circadian_alertness", "user_trust_seeded", "user_trust_seed_delta",
                    "reflection_tree")
_OLD_HOMEOSTASIS_FIELDS = ("body", "need_pyramid", "interoception", "last_metabolic_cost")


@register("astrbot_plugin_ams_life", "m103canfly", "ams-life：小爱的生命层（基于 BioCore）", "0.1.0")
class BioCorePlugin(LLMMixin, AutonomyMixin, SettingsMixin, MediaMixin, PeopleMixin, ImpressionsMixin, DigestMixin, EventsMixin, BrainMixin, PagesMixin, MemoryMixin, DiscretionMixin, PhoneMixin, SendCheckMixin, AttentionMixin, BrowseMixin, Star):
    def __init__(self, context: Context, config=None):
        super().__init__(context)
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
        # step 2 (丁): her browser -- in a reply, two read-only tools of the plugin's own (off by default)
        self.browse_enabled = bool(self.config.get("browse_enabled", False))
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
        return self.cores[key]

    # ams-life: BioCore's /biocore command (readiness, learning, learning reset) is gone:
    # anyone in any chat could reset what she learned or have her inner numbers posted.

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        """ams-life: her phone. Every message that reaches the plugin goes into its own
        chat window, whether it wakes her or not. Store only: no model, no vector
        service, no reply, no body change; the event is never changed, and stopped only
        for a sender on ignore_senders (the owner, 10-29: e.g. the old companion): then
        nothing at all is done with it, and AstrBot calls no model for it.
        (AstrBot stops an event whose handler raises, so nothing may escape here.)"""
        if self._ignored_sender(event):
            logger.info("[ams-life] a message from a sender on ignore_senders: not answered, not kept")
            event.stop_event()
            return
        if not self.enabled:
            return
        try:
            self._begin_job()
            self._check_registry(event)  # someone (or a message) she may not keep: nothing is stored
            self._window_add_message(event)
            self._listen_body(event)
            self._ensure_autonomy_task()  # the 5-minute loop also sweeps her phone
        except Exception as exc:
            logger.warning("[ams-life] window store failed: %s", exc)

    @filter.event_message_type(filter.EventMessageType.ALL, priority=-5)
    async def on_message_decide(self, event: AstrMessageEvent):
        """Step 2 (甲, self_decide): after on_message has kept the message, she decides whether
        to answer it (mixin_attention._decide): a request for a reply, a stop, or nothing."""
        if not self.enabled or not getattr(self, "self_decide", False) or self._ignored_sender(event):
            return
        try:
            request = await self._decide(event)
        except Exception as exc:   # the decision failing: as before, AstrBot decides
            logger.warning("[ams-life] attention: the decision failed (%s)", type(exc).__name__)
            return
        if request is not None:
            yield request

    async def terminate(self):
        """AstrBot calls this when the plugin is unloaded or reloaded: stop the 5-minute loop
        (it now runs whenever the plugin is on)."""
        task = getattr(self, "_autonomy_task", None)
        if task is not None and not task.done():
            task.cancel()

    # after every other plugin's (AstrBot's own is priority 0): the tools are taken out
    # last, and the numbers come out of the group context lines it adds (step 2)
    @filter.on_llm_request(priority=-10)
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        if self._ignored_sender(event):   # on_message stopped it already; should it get this far
            event.stop_event()
            return
        try:   # no tools in her reply, whatever else is on (the owner, 10-29)
            self._reply_tools_off(req)
        except Exception as exc:   # failing, she gets none rather than all of them
            req.func_tool = None
            logger.warning("[ams-life] reply tools could not be taken out, none given: %s", exc)
        else:
            try:   # step 2 (丁): then her browser's two tools, only those (browse_enabled)
                self._give_browse_tools(req, event)
            except Exception as exc:
                logger.warning("[ams-life] browse: tools not given (%s)", type(exc).__name__)
        if not self.enabled or not self.inject_intent:
            return
        # the mark on_message set when the message came in: AstrBot may hold the message
        # for the session lock (the previous one still waiting for the model) before this
        self._continue_job()
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
            text = str(getattr(req, "prompt", "") or "")
        if not text:
            for item in reversed(getattr(req, "contexts", []) or []):
                if isinstance(item, dict) and item.get("role") == "user":
                    c = item.get("content")
                    if isinstance(c, str):
                        text = c
                        break
        # ams-life: what she keeps of it (memory, open loops), and what AstrBot sends the model
        # of this message, keep it as it was said -- "@名字(号码)", numbers too -- but someone
        # deleted is 某人 and an @ of her is her name (_without_gone). What AstrBot keeps in
        # its own history is step 2's.
        text = self._without_gone(text, event)
        if isinstance(getattr(req, "prompt", None), str) and req.prompt:
            req.prompt = self._without_gone(req.prompt, event)
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
        _base = str(getattr(req, "system_prompt", "") or "")
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
            open_loops=self._window_loops(event),
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
        if getattr(self, "self_decide", False):
            # step 2 (甲): what she may pick (nothing, a face, a short line, an answer, several)
            _compact = (_compact + "\n[她可以] " + attention.CHOICES_NOTE).strip()
        if _global:
            # step 2: no QQ number and no group number reaches the model (the owner, 10-29: 31)
            _compact = self._for_model(_compact, event)
            self._numbers_out_of_request(req, event)
        if _compact:
            # Keep the system prompt stable (prefix-cache friendly) and attach
            # the transient intent to this user turn instead of persisting it.
            # ams-life: "_no_save" makes it this turn's only: AstrBot (4.29.3,
            # agent/message.py) sends it to the model but leaves it out of the
            # conversation history, so old blocks do not pile up and come back.
            # (The system prompt below is never saved either.)
            parts = getattr(req, "extra_user_content_parts", None)
            if isinstance(parts, list):
                parts.append({"type": "text", "text": _compact, "_no_save": True})
            else:
                req.system_prompt = (_base + "\n\n" + _compact).strip()
        if _global:
            # step 2: what may be said here, for the last look at the reply (send_check)
            self._note_allowed(event, req, _compact)

    @filter.on_agent_done()
    async def on_agent_done(self, event: AstrMessageEvent, run_context, response: LLMResponse):
        """Step 2 (global_memory): AstrBot saves this turn after this hook (4.29.3,
        internal.py _save_to_history, from run_context.messages): make it hold what was sent
        -- the words said once more, not the first ones -- and none of the model's thinking."""
        if self.enabled and getattr(self, "global_memory", False):
            self._settle_history(event, run_context)

    @filter.on_llm_response()
    async def on_llm_response(self, event: AstrMessageEvent, response: LLMResponse):
        if self._ignored_sender(event):   # nothing of an answer to him is kept
            event.stop_event()
            return
        if not self.enabled:
            return
        if getattr(self, "self_decide", False):
            self._note_spend("reply", response)   # step 2: the money of the day
        if self._browse_on():
            try:   # step 2 (丁): the rounds her tools took, into the browser's own money
                self._browse_after_reply(event, response)
            except Exception as exc:
                logger.warning("[ams-life] browse: not counted (%s)", type(exc).__name__)
        self._continue_job()
        self._check_registry(event)  # her reply to someone she may not keep is not kept either
        core = self._core(event)
        _reply = str(getattr(response, "completion_text", "") or "")
        # ams-life: no state tag is asked for any more. If the model writes one anyway
        # it is cut out (whether it parses or not) and what it says is not used.
        _clean = interpretation.strip_state_tags(_reply)
        if _clean != _reply:
            try:
                response.completion_text = _clean
                chain = getattr(response, "result_chain", None)
                if chain is not None and getattr(chain, "chain", None):
                    for comp in chain.chain:
                        if hasattr(comp, "text"):
                            comp.text = interpretation.strip_state_tags(str(comp.text or ""))
            except Exception:
                pass
        _reply = _clean
        if getattr(self, "self_decide", False) and attention.silent(_reply):
            # step 2 (甲): she chose to say nothing (【不说】): nothing is sent, nothing kept
            logger.info("[ams-life] attention: she said nothing")
            self._check_note(event).update(sent="", outcome="silent")
            self._stop(event)
            return
        if getattr(self, "global_memory", False) and _reply.strip():
            # step 2: the last look before it is sent; "" = nothing is sent and nothing kept.
            # If the look itself fails, the reply is held back as if it leaked.
            try:
                _reply = await self._look_at_reply(event, response, _reply)
            except Exception as exc:
                _reply = self._check_failed(event, exc)
            if not _reply:
                return
        if getattr(self, "self_decide", False):
            # step 2 (甲): her messages as she wrote them -- QQ faces, several messages
            _reply = self._shape_reply(event, response, _reply)
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
