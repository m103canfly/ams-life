# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: dashboard pages, API defaults, backup/restore, memory pages, status."""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403


class PagesMixin:
    def _astrbot_tts_default(self):
        try:
            provs = self.context.get_all_tts_providers()
        except Exception:
            provs = []
        p = provs[0] if provs else None
        if p:
            cfg = getattr(p, "provider_config", {}) or {}
            base = str(cfg.get("api_base") or cfg.get("tts_api_base") or "").strip()
            model = str(cfg.get("model") or cfg.get("tts_model") or getattr(p, "model", "") or "").strip()
            key = str(cfg.get("api_key") or cfg.get("tts_api_key") or "").strip()
            if base:
                return {"provider_id": str(cfg.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        for item in self._config_providers():
            if str(item.get("provider_type") or "") != "tts" or item.get("enable") is False:
                continue
            base = str(item.get("api_base") or item.get("tts_api_base") or "").strip()
            model = str(item.get("model") or item.get("tts_model") or "").strip()
            key = str(item.get("api_key") or item.get("tts_api_key") or "").strip()
            if base:
                return {"provider_id": str(item.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        return None

    def _astrbot_image_default(self):
        try:
            provs = self.context.get_all_providers()
        except Exception:
            provs = []
        sources = {str(x.get("id") or ""): x for x in self._config_provider_sources()}
        candidates = []
        for p in provs:
            cfg = getattr(p, "provider_config", {}) or {}
            pid = str(cfg.get("id") or "").lower()
            model = str(getattr(p, "get_model", lambda: "")() or cfg.get("model") or "").lower()
            if "img" in pid or "image" in pid or "img" in model or "image" in model:
                candidates.append((p, cfg))
        if candidates:
            p, cfg = candidates[0]
            src = sources.get(str(cfg.get("provider_source_id") or ""), {})
            base = str(cfg.get("api_base") or src.get("api_base") or "").strip()
            model = str(getattr(p, "get_model", lambda: "")() or cfg.get("model") or "").strip()
            raw = src.get("key") or cfg.get("key") or ""
            if isinstance(raw, list):
                raw = raw[0] if raw else ""
            key = str(raw or "").strip()
            if base:
                return {"provider_id": str(cfg.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        for item in self._config_providers():
            pid = str(item.get("id") or "").lower()
            if item.get("enable") is False or ("img" not in pid and "image" not in pid):
                continue
            src = sources.get(str(item.get("provider_source_id") or ""), {})
            base = str(item.get("api_base") or src.get("api_base") or "").strip()
            model = str(item.get("model") or item.get("id") or "").strip()
            raw = src.get("key") or item.get("key") or ""
            if isinstance(raw, list):
                raw = raw[0] if raw else ""
            key = str(raw or "").strip()
            if base:
                return {"provider_id": str(item.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        return None

    def _astrbot_llm_default(self):
        try:
            provs = self.context.get_all_providers()
        except Exception:
            provs = []
        p = provs[0] if provs else None
        if p:
            cfg = getattr(p, "provider_config", {}) or {}
            base = str(cfg.get("api_base") or "").strip()
            model = str(getattr(p, "get_model", lambda: "")() or cfg.get("model") or "").strip()
            try:
                key = str(p.get_current_key() or "").strip()
            except Exception:
                key = ""
            if base:
                return {"provider_id": str(cfg.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        # fall back to the AstrBot config table (+ provider source)
        sources = {str(x.get("id") or ""): x for x in self._config_provider_sources()}
        for item in self._config_providers():
            if item.get("enable") is False:
                continue
            ptype = str(item.get("provider_type") or "")
            if ptype and ptype != "chat_completion":
                continue
            src = sources.get(str(item.get("provider_source_id") or ""), {})
            base = str(item.get("api_base") or src.get("api_base") or "").strip()
            model = str(item.get("model") or item.get("id") or "").strip()
            raw_key = src.get("key") or item.get("key") or ""
            if isinstance(raw_key, list):
                raw_key = raw_key[0] if raw_key else ""
            key = str(raw_key or "").strip()
            if base:
                return {"provider_id": str(item.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        return None

    def _astrbot_embedding_default(self):
        try:
            provs = self.context.get_all_embedding_providers()
        except Exception:
            provs = []
        p = provs[0] if provs else None
        if p:
            cfg = getattr(p, "provider_config", {}) or {}
            base = str(cfg.get("embedding_api_base") or "").strip()
            model = str(cfg.get("embedding_model") or getattr(p, "model", "") or "").strip()
            key = str(cfg.get("embedding_api_key") or "").strip()
            if base:
                return {"provider_id": str(cfg.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        # fall back to the AstrBot config table
        for item in self._config_providers():
            if str(item.get("provider_type") or "") != "embedding":
                continue
            if item.get("enable") is False:
                continue
            base = str(item.get("embedding_api_base") or "").strip()
            model = str(item.get("embedding_model") or "").strip()
            key = str(item.get("embedding_api_key") or "").strip()
            if base:
                return {"provider_id": str(item.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        return None

    def _astrbot_rerank_default(self):
        try:
            provs = getattr(getattr(self.context, "provider_manager", None),
                            "rerank_provider_insts", []) or []
        except Exception:
            provs = []
        p = provs[0] if provs else None
        if p:
            cfg = getattr(p, "provider_config", {}) or {}
            base = str(cfg.get("rerank_api_base") or "").strip()
            suffix = str(cfg.get("rerank_api_suffix") or "")
            if suffix and base and not base.endswith(suffix):
                base = base.rstrip("/") + "/" + suffix.lstrip("/")
            model = str(cfg.get("rerank_model") or getattr(p, "model", "") or "").strip()
            key = str(cfg.get("rerank_api_key") or "").strip()
            if base:
                return {"provider_id": str(cfg.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        for item in self._config_providers():
            if str(item.get("provider_type") or "") != "rerank":
                continue
            if item.get("enable") is False:
                continue
            base = str(item.get("rerank_api_base") or "").strip()
            suffix = str(item.get("rerank_api_suffix") or "")
            if suffix and base and not base.endswith(suffix):
                base = base.rstrip("/") + "/" + suffix.lstrip("/")
            model = str(item.get("rerank_model") or "").strip()
            key = str(item.get("rerank_api_key") or "").strip()
            if base:
                return {"provider_id": str(item.get("id") or ""), "base_url": base,
                        "model": model, "has_key": bool(key), "_key": key}
        return None

    def _public_api_config(self):
        llm = self._astrbot_llm_default()
        emb = self._astrbot_embedding_default()
        rrk = self._astrbot_rerank_default()
        tts = self._astrbot_tts_default()
        img = self._astrbot_image_default()
        def one(kind, default):
            saved = self.api_config.get(kind) if isinstance(self.api_config.get(kind), dict) else {}
            source = saved.get("source") or ("astrbot" if default else "custom")
            base = saved.get("base_url")
            model = saved.get("model")
            if not base:
                base = (default or {}).get("base_url", "")
            if not model:
                model = (default or {}).get("model", "")
            enabled = saved.get("enabled")
            if enabled is None:
                enabled = bool(default) if kind != "llm" else True
            return {
                "source": source if source in ("astrbot", "custom") else "custom",
                "base_url": base,
                "model": model,
                "key_saved": bool(saved.get("api_key")) or bool((default or {}).get("has_key")),
                "provider_id": (default or {}).get("provider_id", ""),
                "enabled": bool(enabled),
                "voice": str(saved.get("voice") or ""),
                "size": str(saved.get("size") or ""),
                "format": str(saved.get("format") or ""),
            }
        compression = self.api_config.get("compression") if isinstance(self.api_config.get("compression"), dict) else {}
        return {
            "functions": self._functions_public(),
            "llm": one("llm", llm),
            "embedding": one("embedding", emb),
            "rerank": one("rerank", rrk),
            "tts": one("tts", tts),
            "image": one("image", img),
            "compression": {
                "enabled": bool(compression.get("enabled", False)),
                "threshold": int(compression.get("threshold", 6000) or 6000),
                "max_chars": int(compression.get("max_chars", 800) or 800),
            },
        }

    def _functions_public(self) -> dict:
        out = {}
        for _name in LLM_FUNCTIONS:
            _cfg = self._function_cfg(_name)
            out[_name] = {
                "enabled": bool(_cfg["enabled"]),
                "provider": str(_cfg["provider"]),
                "default_enabled": bool(LLM_FUNCTION_DEFAULTS[_name]),
            }
        return out

    def _llm_provider_options(self) -> list:
        out = []
        try:
            for _p in self.context.get_all_providers():
                _cfg = getattr(_p, "provider_config", {}) or {}
                _pid = str(_cfg.get("id") or getattr(_p, "provider_id", "") or "")
                if not _pid:
                    continue
                try:
                    _model = str(getattr(_p, "get_model", lambda: "")() or _cfg.get("model") or "")
                except Exception:
                    _model = str(_cfg.get("model") or "")
                _ptype = str(_cfg.get("provider_type") or getattr(_p, "provider_type", "") or "")
                out.append({"id": _pid, "model": _model, "type": _ptype})
        except Exception:
            out = []
        return out

    @staticmethod
    def _models_url(base: str) -> str:
        b = str(base or "").strip().rstrip("/")
        if b.endswith("/rerank"):
            b = b[:-7].rstrip("/")
        if not b.endswith("/v1"):
            b = b + "/v1"
        return b + "/models"

    async def _fetch_models(self, kind: str, source: str, base_url: str, api_key: str):
        if kind == "llm":
            default = self._astrbot_llm_default()
        elif kind == "embedding":
            default = self._astrbot_embedding_default()
        elif kind == "tts":
            default = self._astrbot_tts_default()
        elif kind == "image":
            default = self._astrbot_image_default()
        else:
            default = self._astrbot_rerank_default()
        if source == "astrbot" and default:
            base_url = default.get("base_url") or base_url
            api_key = default.get("_key") or api_key
        if not base_url:
            return {"status": "error", "message": "no api base"}
        url = self._models_url(base_url)
        def do_request():
            headers = {"Accept": "application/json"}
            if api_key:
                headers["Authorization"] = "Bearer " + api_key
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8", "replace"))
        try:
            payload = await asyncio.to_thread(do_request)
        except Exception as exc:
            return {"status": "error", "message": "%s: %s" % (type(exc).__name__, exc)}
        items = payload.get("data") if isinstance(payload, dict) else payload
        if isinstance(items, dict):
            items = items.get("models") or items.get("data") or []
        models = []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    mid = item.get("id") or item.get("model") or item.get("name")
                else:
                    mid = item
                if mid:
                    models.append(str(mid))
        return {"status": "ok", "data": {"models": sorted(set(models))}}

    def _register_page_api(self):
        try:
            register = getattr(self.context, "register_web_api", None)
            if register:
                register("/astrbot_plugin_ams_life/page/status", self.page_status, ["GET"],
                         "BioCore dashboard status")
                register("/astrbot_plugin_ams_life/page/self_model", self.page_self_model,
                         ["GET"], "her self model and notebook (read-only)")
                register("/astrbot_plugin_ams_life/page/owner_rules", self.page_owner_rules,
                         ["GET", "POST"], "the owner's rules")
                register("/astrbot_plugin_ams_life/page/toggle", self.page_toggle, ["POST"],
                         "BioCore dashboard toggle")
                register("/astrbot_plugin_ams_life/page/api_config", self.page_api_config, ["POST"],
                         "BioCore API config")
                register("/astrbot_plugin_ams_life/page/models", self.page_models, ["POST"],
                         "BioCore model list")
                register("/astrbot_plugin_ams_life/page/kb_config", self.page_kb_config, ["POST"],
                         "BioCore knowledge base config")
                register("/astrbot_plugin_ams_life/page/backup", self.page_backup, ["GET"],
                         "BioCore core backup")
                register("/astrbot_plugin_ams_life/page/restore", self.page_restore, ["POST"],
                         "BioCore core restore")
                register("/astrbot_plugin_ams_life/page/insight", self.page_insight, ["POST"],
                         "BioCore manual cross-event insight")
                register("/astrbot_plugin_ams_life/page/consolidate", self.page_consolidate, ["POST"],
                         "BioCore memory consolidation")
                register("/astrbot_plugin_ams_life/page/event_summary",
                         self.page_event_summary, ["POST"],
                         "BioCore event summary regenerate/edit")
                register("/astrbot_plugin_ams_life/page/memory_point_feedback",
                         self.page_memory_point_feedback, ["POST"],
                         "BioCore memory-point feedback (important/unimportant/edit/restore)")
                # ams-life step 1-3: BioCore's memory rollback / restore endpoints are gone: they
                # wrote around the forget registry and the vector store, and restore could bring
                # deleted words back from a tombstone. Deleting is for real. (The whole-folder
                # backup / restore above stays: it is the owner's tool.)
                register("/astrbot_plugin_ams_life/page/memory/delete/<path:session>/<entry_id>",
                         self.page_memory_delete, ["POST"],
                         "the owner deletes one memory and everything from its messages")
                register("/astrbot_plugin_ams_life/page/forget/person", self.page_forget_person, ["POST"],
                         "the owner deletes a person everywhere")
        except Exception as exc:
            logger.warning("[biocore] page api register failed: %s", exc)

    def _memory_stats(self):
        sessions = 0
        entries = 0
        try:
            for f in MEMORY_DIR.glob("*.json"):
                sessions += 1
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    entries += len(d.get("entries") or [])
                except Exception:
                    pass
        except Exception:
            pass
        return {"sessions": sessions, "entries": entries}

    async def _kb_available(self):
        try:
            kbs = await self.context.kb_manager.list_kbs()
            return [{"kb_id": str(getattr(k, "kb_id", "")), "kb_name": str(getattr(k, "kb_name", "")),
                     "description": str(getattr(k, "description", "") or "")} for k in (kbs or [])]
        except Exception as exc:
            logger.warning("[biocore] kb list failed: %s", exc)
            return []

    async def page_backup(self):
        import datetime
        buf = io.BytesIO()
        try:
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
                root = PLUGIN_DIR
                # ams-life: the plugin is split over several modules now, so back up every .py file
                for name in sorted({f.name for f in root.glob("*.py")} | {
                        "metadata.yaml", "README.md", "NOTICE.md", "LICENSE",
                        "_conf_schema.json", "preview.png"}):
                    f = root / name
                    if f.is_file():
                        z.write(f, "astrbot_plugin_ams_life/" + name)
                pages = root / "pages"
                if pages.is_dir():
                    for f in pages.rglob("*"):
                        if f.is_file() and "__pycache__" not in f.parts:
                            z.write(f, "astrbot_plugin_ams_life/pages/" + str(f.relative_to(pages)))
                for f in DATA_DIR.rglob("*"):
                    if f.is_file() and "__pycache__" not in f.parts:
                        z.write(f, "data/" + str(f.relative_to(DATA_DIR)))
                info = ("BioCore core backup\n"
                        "Contains plugin code + data/ (persona, memory, states, API config).\n"
                        "Do not share: api_config.json may contain API keys.\n")
                z.writestr("BACKUP_INFO.txt", info)
        except Exception as exc:
            logger.warning("[biocore] backup failed: %s", exc)
            return {"status": "error", "message": str(exc)}
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        return {"status": "ok", "data": {
            "filename": "biocore_core_" + stamp + ".zip",
            "mime": "application/zip",
            "base64": base64.b64encode(buf.getvalue()).decode("ascii"),
        }}

    async def page_restore(self):
        from quart import request
        import datetime
        body = await request.get_json(silent=True) or {}
        raw_b64 = str(body.get("base64") or "")
        if not raw_b64:
            return {"status": "error", "message": "empty backup"}
        try:
            raw = base64.b64decode(raw_b64)
            z = zipfile.ZipFile(io.BytesIO(raw))
        except Exception as exc:
            return {"status": "error", "message": "invalid zip: %s" % exc}
        names = [n for n in z.namelist() if n.startswith("data/") and not n.endswith("/")]
        if not names:
            return {"status": "error", "message": "backup has no data/ entries"}
        # automatic safety backup of current data before overwrite
        try:
            backup_dir = DATA_DIR.parent / "restore_backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safety = backup_dir / ("before_restore_" + stamp + ".zip")
            with zipfile.ZipFile(safety, "w", zipfile.ZIP_DEFLATED) as bz:
                for f in DATA_DIR.rglob("*"):
                    if f.is_file() and "__pycache__" not in f.parts:
                        bz.write(f, str(f.relative_to(DATA_DIR)))
        except Exception as exc:
            logger.warning("[biocore] restore safety backup failed: %s", exc)
        count = 0
        try:
            for name in names:
                rel = name[len("data/"):]
                parts = [x for x in rel.split("/") if x not in ("", ".", "..")]
                if not parts:
                    continue
                dest = DATA_DIR.joinpath(*parts)
                dest.parent.mkdir(parents=True, exist_ok=True)
                with z.open(name) as src, open(dest, "wb") as out:
                    shutil.copyfileobj(src, out)
                count += 1
        except Exception as exc:
            logger.warning("[biocore] restore failed: %s", exc)
            return {"status": "error", "message": "restore failed: %s" % exc}
        try:
            self._load_profile()
            self._load_settings()
            self._load_api_config()
            self.cores = {}
        except Exception:
            pass
        logger.info("[biocore] restored %s data files", count)
        return {"status": "ok", "data": {"files": count}}

    async def page_memory_delete(self, session: str, entry_id: str):
        """The owner deletes one memory (panel only; the page asks to confirm first): the
        memory and everything else that came from the messages it came from, for real (no
        tombstone), and registered so it is not kept again. `session` is not used: there
        is one library."""
        try:
            counts = self._owner_forget_memory(entry_id)
            if counts is None:
                return {"status": "error", "message": "memory entry not found", "data": {}}
            return {"status": "ok", "data": {"id": entry_id, "deleted": True, "counts": counts}}
        except Exception as exc:
            return {"status": "error", "message": str(exc)[:180], "data": {}}

    async def page_forget_person(self, person=None):
        """The owner deletes a person everywhere (panel only; the page asks to confirm
        first): {"person": "<qq>"}. Registered, so nothing of his is kept again; what
        AstrBot keeps of him goes too, as far as AstrBot lets a plugin."""
        if person is None:
            try:
                from quart import request
                body = await request.get_json(silent=True) or {}
            except Exception:
                body = {}
            person = body.get("person") if isinstance(body, dict) else ""
        person = str(person or "").strip()
        if not person or not person.isdigit():
            return {"status": "error", "message": "person must be a QQ number", "data": {}}
        try:
            umos = self._place_umos()
            counts = self._owner_forget_person(person)
            counts["astrbot"] = await self._forget_in_astrbot(person, umos)
            return {"status": "ok", "data": {"person": person, "counts": counts}}
        except Exception as exc:
            return {"status": "error", "message": str(exc)[:180], "data": {}}

    async def page_consolidate(self):
        """Force one memory consolidation pass over all local sessions."""
        results = []
        try:
            # ams-life: one library; consolidate each place's entries separately.
            files = self._library_places()
        except Exception:
            files = []
        if getattr(self, "_consolidating", False):
            return {"status": "ok", "data": {"files": 0, "message": "already running"}}
        self._consolidating = True
        try:
            for key in files:
                ev = types.SimpleNamespace(unified_msg_origin=key)
                try:
                    core = self._core(ev)
                    await self._consolidate_memory(ev, core, force=True)
                    results.append(key)
                except Exception as exc:
                    logger.warning("[biocore] manual consolidation failed: %s", exc)
        finally:
            self._consolidating = False
            self._last_consolidation = time.time()
        return {"status": "ok", "data": {"files": len(results), "sessions": len(files)}}

    def _working_set_preview(self, key: str) -> dict:
        """Bounded working-set exposure for the dashboard/evals (no new mechanism).

        S3: also exposes the read-time TTL (G12) and how many ids are still
        fresh (touched within the TTL), so the UI never has to guess.
        """
        try:
            doc = self._load_memory(types.SimpleNamespace(unified_msg_origin=str(key or "")))
            doc = doc if isinstance(doc, dict) else {}
            ws = doc.get("working_set") if isinstance(doc.get("working_set"), list) else []
            ids = [str(x) for x in (ws or []) if str(x)][-8:]
            fresh = 0
            if ids:
                by_id = {str(e.get("id") or ""): e for e in (doc.get("entries") or [])
                         if isinstance(e, dict) and str(e.get("id") or "")}
                _now = time.time()
                for _id in ids:
                    entry = by_id.get(_id)
                    if entry is None:
                        continue
                    try:
                        anchor = max(float(entry.get("last_recall", 0) or 0),
                                     float(entry.get("last_used", 0) or 0),
                                     float(entry.get("ts", 0) or 0))
                    except Exception:
                        anchor = 0.0
                    # Legacy entries without timestamps are treated as fresh.
                    if anchor <= 0 or (_now - anchor) <= memory_meta.WORKING_SET_TTL_SECONDS:
                        fresh += 1
            return {"capacity": 8, "count": len(ids), "ids": ids,
                    "ttl_seconds": int(memory_meta.WORKING_SET_TTL_SECONDS),
                    "fresh_count": fresh}
        except Exception:
            return {"capacity": 8, "count": 0, "ids": [],
                    "ttl_seconds": int(memory_meta.WORKING_SET_TTL_SECONDS),
                    "fresh_count": 0}

    async def page_status(self):
        _personas = []
        try:
            _pm = getattr(self.context, "persona_manager", None)
            if _pm is not None:
                for _p in (await _pm.get_all_personas()):
                    _pid = str(getattr(_p, "persona_id", "") or "")
                    _pname = str(getattr(_p, "name", "") or _pid)
                    if _pid:
                        _personas.append({"id": _pid, "name": _pname})
        except Exception:
            _personas = []
        cores = []
        for key, core in list(self.cores.items())[:20]:
            cores.append({
                "key": key,
                "snapshot": core.snapshot(),
                "intent": {**core.intent(), "plan": interpretation.plan(core)},
                "working_set": self._working_set_preview(key),
            })
        if not cores:
            # The in-memory cache is empty after a restart. Load persisted
            # states so the dashboard does not silently fall back to demo data.
            try:
                files = sorted(STATE_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)[:20]
            except Exception:
                files = []
            for path in files:
                try:
                    state = json.loads(path.read_text(encoding="utf-8"))
                    core = BioCore(self.profile)
                    core.load_state(state)
                    cores.append({
                        "key": path.stem,
                        "snapshot": core.snapshot(),
                        "intent": {**core.intent(), "plan": interpretation.plan(core)},
                        "working_set": self._working_set_preview(path.stem),
                    })
                except Exception:
                    continue
        return {"status": "ok", "data": {
            "enabled": self.enabled,
            "inject_intent": self.inject_intent,
            "proactive_reply": self.proactive_reply,
            "memory_dedup_embedding": self.memory_dedup_embedding,
            "memory_worthiness_enabled": bool(
                getattr(self, "memory_worthiness_enabled", True)),
            "hybrid_retrieval": bool(getattr(self, "hybrid_retrieval", True)),
            "safety_enabled": bool(getattr(self, "safety_enabled", False)),
            "llm_memory_candidates": bool(
                getattr(self, "llm_memory_candidates", True)),
            "we_memory_enabled": bool(getattr(self, "we_memory_enabled", False)),
            "summary_max_chars": int(getattr(self, "summary_max_chars", 0) or 0),
            "llm_only_reply_summary": bool(
                getattr(self, "llm_only_reply_summary", True)),
            "insight_auto_enabled": bool(getattr(self, "insight_auto_enabled", False)),
            "persona_loaded": bool(self.persona_text),
            "persona_id": str(getattr(self, "persona_id", "") or ""),
            "personas": _personas,
            "llm_functions": self._functions_public(),
            "llm_providers": self._llm_provider_options(),
            "profile": self.profile or dict(DEFAULT_PROFILE),
            "api_config": self._public_api_config(),
            "memory": self._memory_stats(),
            # Read-only dashboard contract (bounded): memory entries per
            # session with provenance/confidence/write-op metadata, tombstone
            # audit rows, and per-user relationship state/trajectory/maps.
            "memory_index": _memory_index_rows(MEMORY_DIR),
            "relationships": _relationship_rows(USER_DIR),
            "last_memory_meta": {
                "calibration_delta": 0.0, "calibration_sources": 0,
                **dict(getattr(self, "_last_memory_meta", {}) or {})},
            "last_memory_trace": {**DEFAULT_MEMORY_TRACE,
                                  **dict(getattr(self, "_last_memory_trace", {}) or {})},
            # Paper mechanisms also at top level for dashboard/API consumers.
            "allostatic_load": round(float(getattr(cores[0], "allostatic_load", 0.0)), 3) if cores else 0.0,
            "homeostasis": dict(getattr(cores[0], "homeostasis", {}) or {}) if cores else {},
            # L-T02/L-T03..L-T12 read-only runtime surface (bounded, no prompt text)
            "last_cause_trace": [dict(x) for x in (getattr(self, "_last_cause_trace", []) or [])[:8]
                                 if isinstance(x, dict)],
            "last_strategy_hint": str(getattr(self, "_last_strategy_hint", "") or "")[:140],
            "kb_config": {"enabled": bool(getattr(self, "kb_enabled", False)),
                          "names": list(getattr(self, "kb_names", []))},
            "kb_available": await self._kb_available(),
            "astrbot_llm": {k: v for k, v in (self._astrbot_llm_default() or {}).items() if not k.startswith("_")},
            "astrbot_embedding": {k: v for k, v in (self._astrbot_embedding_default() or {}).items() if not k.startswith("_")},
            "astrbot_rerank": {k: v for k, v in (self._astrbot_rerank_default() or {}).items() if not k.startswith("_")},
            "astrbot_tts": {k: v for k, v in (self._astrbot_tts_default() or {}).items() if not k.startswith("_")},
            "astrbot_image": {k: v for k, v in (self._astrbot_image_default() or {}).items() if not k.startswith("_")},
            "cores": cores,
            "self_model": dict(self.self_model or {}),
            "events": [dict(_ev,
                            effective_merge_count=self._decayed_merge_count(_ev))
                       for _ev in self._event_archive(30, read_only=True)
                       if isinstance(_ev, dict)],
            "insights": self._insights(5),
        }}

    async def page_self_model(self):
        """ams-life step 1-2: read-only. Her heart is only what she writes herself."""
        from quart import request
        if request.method != "GET":
            return {"status": "error", "message": "她的自我描述只由她自己写，面板只能看"}
        return {"status": "ok", "data": {"self_model": self.self_model}}

    async def page_owner_rules(self):
        """The owner's rules: kept apart from her self model, shown in every chat's reply."""
        from quart import request
        if request.method == "POST":
            body = await request.get_json(silent=True) or {}
            raw = body.get("rules")
            if isinstance(raw, str):
                raw = raw.splitlines()
            rules = [str(x).strip()[:OWNER_RULES_CHARS] for x in (raw or []) if str(x or "").strip()]
            OWNER_RULES_PATH.parent.mkdir(parents=True, exist_ok=True)
            tmp = OWNER_RULES_PATH.with_suffix(".tmp")
            tmp.write_text(json.dumps({"rules": rules[:OWNER_RULES_MAX]}, ensure_ascii=False, indent=1),
                           encoding="utf-8")
            os.replace(str(tmp), str(OWNER_RULES_PATH))
        return {"status": "ok", "data": {"rules": self._owner_rules(),
                                         "max": OWNER_RULES_MAX, "chars": OWNER_RULES_CHARS}}

    async def page_toggle(self):
        from quart import request
        data = await request.get_json(silent=True) or {}
        key = str(data.get("key") or "").strip()
        _fn_enabled = {("%s_enabled" % _name): _name for _name in LLM_FUNCTIONS}
        _fn_provider = {("%s_provider" % _name): _name for _name in LLM_FUNCTIONS}
        if key in _fn_enabled or key in _fn_provider:
            _name = _fn_enabled.get(key) or _fn_provider.get(key)
            _cur = dict(self.llm_functions.get(_name) or {})
            if key in _fn_enabled:
                _cur["enabled"] = bool(data.get("value"))
            else:
                _cur["provider"] = str(data.get("value") or "follow_llm").strip() or "follow_llm"
            _cur.pop("embedding_provider", None)
            _cur.pop("rerank_provider", None)
            self.llm_functions[_name] = _cur
            self.api_config["functions"] = dict(self.llm_functions)
            self._save_api_config()
            return {"status": "ok", "data": {"key": key, "value": _cur.get("enabled") if key in _fn_enabled else _cur.get("provider")}}
        if key not in ("proactive_reply", "memory_dedup_embedding", "inject_intent",
                       "hybrid_retrieval", "safety_enabled", "llm_memory_candidates",
                       "llm_only_reply_summary", "persona_id",
                       "insight_auto_enabled"):
            return {"status": "error", "message": "unknown setting"}
        if key == "persona_id":
            _val = str(data.get("value") or "").strip()
            self.persona_id = _val
            self._save_settings()
            await self._persist_plugin_config({key: _val})
            return {"status": "ok", "data": {"key": key, "value": _val}}
        if key == "llm_only_reply_summary":
            # Legacy master switch: keep it readable, but migrate all per-function
            # routes once instead of treating it as the only switch.
            self.llm_only_reply_summary = bool(data.get("value"))
            _legacy = bool(self.llm_only_reply_summary)
            for _name in LLM_FUNCTIONS:
                self.llm_functions[_name] = {
                    "enabled": (LLM_FUNCTION_DEFAULTS[_name] if _legacy else True),
                    "provider": str((self.llm_functions.get(_name) or {}).get("provider") or "follow_llm"),
                }
            self.api_config["functions"] = dict(self.llm_functions)
            self._save_api_config()
            self._save_settings()
            await self._persist_plugin_config({key: bool(self.llm_only_reply_summary)})
            return {"status": "ok", "data": {"key": key, "value": self.llm_only_reply_summary}}
        if key == "safety_enabled":
            self.safety_enabled = bool(data.get("value"))
            self.sensitive_memory_protection = self.safety_enabled
            self._save_settings()
            await self._persist_plugin_config({key: self.safety_enabled})
            logger.info("[biocore] safety_enabled=%s", self.safety_enabled)
            return {"status": "ok", "data": {"key": key, "value": self.safety_enabled}}
        setattr(self, key, bool(data.get("value")))
        self._save_settings()
        await self._persist_plugin_config({key: bool(getattr(self, key))})
        logger.info("[biocore] setting %s=%s", key, getattr(self, key))
        return {"status": "ok", "data": {"key": key, "value": getattr(self, key)}}

    async def generate_manual_insight(self) -> dict:
        """Manual long-term insight (dashboard button), bypass threshold once.

        Never writes a deterministic fallback: when the insight LLM switch is
        off it only returns a message telling the user to enable it.
        """
        if not self._llm_allowed("insight"):
            return {"generated": False, "insight": "",
                    "message": "请先开启「长期模式洞察」LLM 开关再生成"}
        events = self._event_archive(12)
        if not events:
            return {"generated": False, "insight": "", "message": "还没有归档事件"}
        core = next(iter(self.cores.values()), None)
        if core is None:
            core = BioCore(dict(DEFAULT_PROFILE))
        key = next(iter(self.cores), "") or ""
        ev = types.SimpleNamespace(unified_msg_origin=key)
        ok = await self._generate_insight(ev, core, events[:6])
        insight = ""
        try:
            if INSIGHT_ARCHIVE_PATH.exists():
                lines = [x for x in INSIGHT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
                if lines:
                    insight = str(json.loads(lines[-1]).get("insight") or "")
        except Exception:
            insight = ""
        if ok:
            try:
                # A manual generation also advances the auto dedupe state so
                # the background trigger does not immediately duplicate it.
                now = time.time()
                latest_ts = max([float(e.get("ts", 0) or 0) for e in events] or [0.0])
                seen = [str(e.get("id") or "") for e in events if str(e.get("id") or "")]
                self._save_insight_state({"last_run_ts": now, "last_event_ts": latest_ts,
                                          "seen_ids": seen[-100:]})
            except Exception:
                pass
        return {"generated": bool(ok), "insight": insight, "events": len(events),
                "message": "" if ok else "生成失败，请查看日志"}

    async def page_insight(self):
        """Manual '生成长期洞察' button: bypass threshold/cooldown once."""
        from quart import request
        _ = await request.get_json(silent=True) or {}
        return {"status": "ok", "data": await self.generate_manual_insight()}

    async def page_api_config(self):
        from quart import request
        body = await request.get_json(silent=True) or {}
        for kind in ("llm", "embedding", "rerank", "tts", "image"):
            incoming = body.get(kind)
            if not isinstance(incoming, dict):
                continue
            source = str(incoming.get("source") or "custom").strip()
            if source not in ("astrbot", "custom"):
                source = "custom"
            old = self.api_config.get(kind) if isinstance(self.api_config.get(kind), dict) else {}
            key = str(incoming.get("api_key") or "").strip()
            if not key:
                key = str(old.get("api_key") or "")
            entry = {
                "source": source,
                "base_url": str(incoming.get("base_url") or "").strip(),
                "api_key": key,
                "model": str(incoming.get("model") or "").strip(),
                "enabled": bool(incoming.get("enabled", True)),
            }
            for extra in ("voice", "size", "format"):
                if extra in incoming:
                    entry[extra] = str(incoming.get(extra) or "").strip()
            self.api_config[kind] = entry
        _incoming_functions = body.get("functions")
        if isinstance(_incoming_functions, dict):
            for _name in LLM_FUNCTIONS:
                _item = _incoming_functions.get(_name)
                if not isinstance(_item, dict):
                    continue
                _cur = dict(self.llm_functions.get(_name) or {})
                if "enabled" in _item:
                    _cur["enabled"] = bool(_item.get("enabled"))
                if "provider" in _item:
                    _cur["provider"] = str(_item.get("provider") or "follow_llm").strip() or "follow_llm"
                _cur.pop("embedding_provider", None)
                _cur.pop("rerank_provider", None)
                self.llm_functions[_name] = _cur
            self.api_config["functions"] = dict(self.llm_functions)
        comp = body.get("compression")
        if isinstance(comp, dict):
            self.api_config["compression"] = {
                "enabled": bool(comp.get("enabled", False)),
                "threshold": max(1000, int(comp.get("threshold", 6000) or 6000)),
                "max_chars": max(120, int(comp.get("max_chars", 800) or 800)),
            }
        self._save_api_config()
        logger.info("[biocore] api config saved")
        return {"status": "ok", "data": self._public_api_config()}

    async def page_kb_config(self):
        from quart import request
        body = await request.get_json(silent=True) or {}
        self.kb_enabled = bool(body.get("enabled", False))
        names = body.get("names") if isinstance(body.get("names"), list) else []
        self.kb_names = [str(x).strip() for x in names if str(x).strip()]
        self._save_settings()
        await self._persist_plugin_config({"kb_enabled": self.kb_enabled,
                                           "kb_names": self.kb_names})
        logger.info("[biocore] kb config enabled=%s names=%s", self.kb_enabled, self.kb_names)
        return {"status": "ok", "data": {"enabled": self.kb_enabled, "names": self.kb_names}}

    async def page_models(self):
        from quart import request
        body = await request.get_json(silent=True) or {}
        kind = str(body.get("kind") or "embedding").strip()
        source = str(body.get("source") or "custom").strip()
        return await self._fetch_models(kind, source,
                                        str(body.get("base_url") or ""),
                                        str(body.get("api_key") or ""))
