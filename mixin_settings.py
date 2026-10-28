# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: settings, API config, provider listing, speaker identity."""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403


class SettingsMixin:
    async def _ensure_profile(self, event):
        if not self.profile and self.first_run_persona_compile:
            await self._compile_profile(event)
        elif not self.profile:
            self.profile = dict(DEFAULT_PROFILE)
            self.persona_text = ""

    def _settings_path(self):
        return DATA_DIR / "settings.json"

    def _load_settings(self):
        try:
            p = self._settings_path()
            if p.exists():
                d = json.loads(p.read_text(encoding="utf-8"))
                # Single source of truth = AstrBot plugin config. Legacy dashboard
                # toggles in settings.json only apply when config does not define
                # the key (otherwise they silently overrode plugin config).
                for key in ("proactive_reply", "memory_dedup_embedding", "inject_intent",
                            "kb_enabled", "hybrid_retrieval", "safety_enabled",
                            "llm_memory_candidates", "llm_only_reply_summary",
                            "we_memory_enabled"):
                    if key in d and key not in self.config:
                        setattr(self, key, bool(d[key]))
                if "safety_enabled" in d and "safety_enabled" not in self.config:
                    self.safety_enabled = bool(d.get("safety_enabled"))
                    self.sensitive_memory_protection = self.safety_enabled
                if "persona_id" in d and "persona_id" not in self.config:
                    self.persona_id = str(d.get("persona_id") or "").strip()
                if isinstance(d.get("kb_names"), list) and "kb_names" not in self.config:
                    self.kb_names = [str(x) for x in d.get("kb_names") if str(x).strip()]
        except Exception as exc:
            logger.warning("[biocore] settings load failed: %s", exc)

    def _save_settings(self):
        try:
            self._settings_path().write_text(json.dumps({
                "proactive_reply": bool(self.proactive_reply),
                "memory_dedup_embedding": bool(self.memory_dedup_embedding),
                "hybrid_retrieval": bool(getattr(self, "hybrid_retrieval", True)),
                "safety_enabled": bool(getattr(self, "safety_enabled", False)),
                "llm_memory_candidates": bool(
                    getattr(self, "llm_memory_candidates", True)),
                "we_memory_enabled": bool(getattr(self, "we_memory_enabled", False)),
            "bc_prompt_mode": str(getattr(self, "bc_prompt_mode", "telemetry") or "telemetry"),
            "summary_max_chars": int(getattr(self, "summary_max_chars", 0) or 0),
            "llm_only_reply_summary": bool(
                    getattr(self, "llm_only_reply_summary", True)),
                "persona_id": str(getattr(self, "persona_id", "") or ""),
                "inject_intent": bool(self.inject_intent),
                "kb_enabled": bool(getattr(self, "kb_enabled", False)),
                "kb_names": list(getattr(self, "kb_names", [])),
            }, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as exc:
            logger.warning("[biocore] settings save failed: %s", exc)

    async def _persist_plugin_config(self, updates: dict):
        try:
            if isinstance(self.config, dict):
                self.config.update(updates)
                saver = getattr(self.config, "save_config_async", None)
                if saver:
                    await saver(updates)
                else:
                    saver2 = getattr(self.config, "save_config", None)
                    if saver2:
                        saver2(updates)
        except Exception as exc:
            logger.warning("[biocore] plugin config sync failed: %s", exc)

    def _load_api_config(self):
        try:
            if API_CONFIG_PATH.exists():
                d = json.loads(API_CONFIG_PATH.read_text(encoding="utf-8"))
                if isinstance(d, dict):
                    self.api_config = d
        except Exception as exc:
            logger.warning("[biocore] api config load failed: %s", exc)
            self.api_config = {}
        self._load_llm_functions()

    def _load_llm_functions(self):
        """Load per-function LLM switches and provider overrides.

        Embedding/rerank model selection is intentionally NOT per-function:
        the deterministic event-ranking pipeline always follows the API 接入
        defaults (global embedding, global rerank with deterministic local
        fallback). Legacy configs that stored embedding_provider/rerank_provider
        are migrated by dropping those keys.
        """
        _defaults = {
            _name: {"enabled": LLM_FUNCTION_DEFAULTS[_name],
                    "provider": "follow_llm"}
            for _name in LLM_FUNCTIONS
        }
        _saved = self.api_config.get("functions") if isinstance(self.api_config.get("functions"), dict) else None
        if _saved is None:
            # Legacy migration: strict=true meant "summaries only"; strict=false
            # meant all capabilities available.
            _legacy = bool(getattr(self, "llm_only_reply_summary", True))
            _defaults = {
                _name: {"enabled": (LLM_FUNCTION_DEFAULTS[_name] if _legacy else True),
                         "provider": "follow_llm"}
                for _name in LLM_FUNCTIONS
            }
            self.llm_functions = _defaults
            self.api_config["functions"] = _defaults
            self._save_api_config()
            return
        _merged = {}
        _dropped_legacy = False
        for _name in LLM_FUNCTIONS:
            _raw = _saved.get(_name)
            _item = _raw if isinstance(_raw, dict) else {}
            if isinstance(_raw, dict) and (
                    "embedding_provider" in _raw or "rerank_provider" in _raw):
                _dropped_legacy = True
            _merged[_name] = {
                "enabled": bool(_item.get("enabled", LLM_FUNCTION_DEFAULTS[_name])),
                "provider": str(_item.get("provider") or "follow_llm"),
            }
        self.llm_functions = _merged
        self.api_config["functions"] = _merged
        if _dropped_legacy:
            # Persist the migration once so the dead per-function model keys go
            # away from data/api_config.json.
            self._save_api_config()

    def _save_api_config(self):
        try:
            API_CONFIG_PATH.write_text(json.dumps(self.api_config, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
        except Exception as exc:
            logger.warning("[biocore] api config save failed: %s", exc)

    def _config_providers(self):
        try:
            cfg = self.context.get_config()
            if isinstance(cfg, dict):
                return list(cfg.get("provider") or [])
            getter = getattr(cfg, "get", None)
            if getter:
                return list(getter("provider") or [])
        except Exception:
            pass
        return []

    def _config_provider_sources(self):
        try:
            cfg = self.context.get_config()
            if isinstance(cfg, dict):
                return list(cfg.get("provider_sources") or [])
            getter = getattr(cfg, "get", None)
            if getter:
                return list(getter("provider_sources") or [])
        except Exception:
            pass
        return []

    def _speaker(self, event):
        """Return the current sender's (id, display name) if available."""
        sid = ""
        name = ""
        try:
            fn = getattr(event, "get_sender_id", None)
            if callable(fn):
                sid = str(fn() or "")
        except Exception:
            pass
        try:
            fn = getattr(event, "get_sender_name", None)
            if callable(fn):
                name = str(fn() or "")
        except Exception:
            pass
        try:
            obj = getattr(event, "message_obj", None)
            sender = getattr(obj, "sender", None) if obj is not None else None
            if sender is not None:
                if not sid:
                    sid = str(getattr(sender, "user_id", "") or "")
                if not name:
                    name = str(getattr(sender, "nickname", "") or "")
        except Exception:
            pass
        return sid.strip(), name.strip()
