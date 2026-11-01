# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: embeddings, memory store, scoring, recall, consolidation, continuity opener."""
from __future__ import annotations
try:
    from . import adapter_astrbot_turn
except ImportError:
    import adapter_astrbot_turn
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403


try:
    from .mixin_ports import PortsMixin
    from .mixin_discretion import recall_permission, recall_anonymize
except ImportError:
    from mixin_ports import PortsMixin
    from mixin_discretion import recall_permission, recall_anonymize


class MemoryMixin(PortsMixin):
    @staticmethod
    def _ipv4_json(url: str, headers: dict, payload: dict, timeout: float = 12.0) -> dict:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        if not host:
            raise ValueError("invalid url")
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        class _IPv4HTTPSConnection(http.client.HTTPSConnection):
            def connect(self):
                infos = socket.getaddrinfo(self.host, self.port, socket.AF_INET, socket.SOCK_STREAM)
                ip = infos[0][4][0]
                sock = socket.create_connection((ip, self.port), self.timeout)
                self.sock = self._context.wrap_socket(sock, server_hostname=self.host)

        if parsed.scheme == "https":
            conn = _IPv4HTTPSConnection(host, port, timeout=timeout,
                                         context=ssl.create_default_context())
        else:
            conn = http.client.HTTPConnection(host, port, timeout=timeout)
        try:
            conn.request("POST", path, body=body, headers=headers)
            resp = conn.getresponse()
            raw = resp.read()
            if resp.status >= 400:
                raise RuntimeError("http %s: %s" % (resp.status, raw[:300].decode("utf-8", "replace")))
            return json.loads(raw.decode("utf-8", "replace"))
        finally:
            conn.close()

    def _embedding_runtime_config(self):
        saved = self.api_config.get("embedding") if isinstance(self.api_config.get("embedding"), dict) else {}
        if saved.get("source") == "custom" and saved.get("base_url"):
            return {"base_url": saved.get("base_url"), "api_key": saved.get("api_key", ""),
                    "model": saved.get("model", "")}
        d = self._astrbot_embedding_default()
        if d and d.get("base_url"):
            return {"base_url": d.get("base_url"), "api_key": d.get("_key", ""),
                    "model": d.get("model", "")}
        if saved.get("base_url"):
            return {"base_url": saved.get("base_url"), "api_key": saved.get("api_key", ""),
                    "model": saved.get("model", "")}
        return None

    def _embed_skip_sensitive(self, sensitive) -> bool:
        """Whether a tagged-sensitive payload must be withheld from embedding.

        Privacy filtering belongs to the safety switch (default OFF), so the
        1.2.98 behaviour stays a bitwise no-op unless ``safety_enabled`` is on.
        """
        return bool(sensitive) and bool(getattr(self, "safety_enabled", False))

    async def _embed_text_guarded(self, text: str, sensitive: bool = False):
        """Embedding for already-stored memory/event text (M1 privacy gate).

        When safety is on and the payload is tagged sensitive the text is NEVER
        sent to the embedding provider: the caller receives ``None`` and keeps
        the entry/text untouched (it just has no vector). Default (safety off)
        is a no-op, identical to ``_embed_text(text)``. The TypeError fallback
        keeps one-argument ``_embed_text`` overrides used by legacy evals working.
        """
        try:
            return await self._embed_text(
                text, sensitive=self._embed_skip_sensitive(sensitive))
        except TypeError:
            return await self._embed_text(text)

    async def _embedding_for(self, kind: str, text: str, sensitive: bool = False):
        """Embedding for one function; always follows the API 接入 default.

        Per-function embedding model selection was removed by user request:
        every function uses the same global embedding configuration. ``kind``
        is kept for call-site clarity and tests.
        """
        try:
            return await self._embed_text(text, sensitive=sensitive)
        except TypeError:
            # Backward-compatible test/legacy override without the sensitive kwarg.
            return await self._embed_text(text)

    async def _rerank_scores(self, kind: str, query: str, documents: list):
        """Optional global rerank scores keyed by candidate index (None = local).

        Event ranking never asks the user to pick a model: it follows the
        API 接入 / AstrBot default rerank provider and falls back to the
        deterministic local ranking when no provider is configured or the call
        fails. ``kind`` is kept for call-site clarity and tests.
        """
        try:
            _provs = getattr(getattr(self.context, "provider_manager", None),
                             "rerank_provider_insts", []) or []
        except Exception:
            _provs = []
        _target = _provs[0] if _provs else None
        if _target is None:
            return None
        try:
            _results = await _target.rerank(query, [str(d) for d in documents], top_n=len(documents))
            out = {}
            for _r in (_results or []):
                try:
                    _idx = int(getattr(_r, "index", None))
                    _score = float(getattr(_r, "relevance_score", 0.0) or 0.0)
                except Exception:
                    continue
                out[_idx] = max(0.0, min(1.0, _score))
            return out or None
        except Exception as exc:
            logger.warning("[biocore] global rerank failed; fallback to local ranking: %s", exc)
            return None

    async def _embed_text(self, text: str, sensitive: bool = False):
        text = (text or "").strip()
        if not text or sensitive:
            return None
        conf = self._embedding_runtime_config()
        if not conf:
            return None
        model = str(conf.get("model") or "").strip()
        # M4: the cache key hashes exactly the payload that is sent (one
        # truncation constant for both), so two texts that only differ after the
        # truncation point can never share a stale vector.
        payload_text = text[:EMBED_TEXT_MAX_CHARS]
        cache_key = (model, _sha256(payload_text))
        _cache_on = bool(getattr(self, "embedding_cache_enabled", True))
        if _cache_on and cache_key in EMBED_CACHE:
            EMBED_CACHE.move_to_end(cache_key)
            return EMBED_CACHE[cache_key]
        base = str(conf.get("base_url") or "").rstrip("/")
        if base.endswith("/embeddings"):
            base = base[:-11]
        url = base + "/embeddings"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if conf.get("api_key"):
            headers["Authorization"] = "Bearer " + str(conf.get("api_key"))
        payload = {"model": model, "input": [payload_text], "encoding_format": "float"}
        try:
            # Embedding timeout is a config key (embedding_timeout_ms, default
            # 1500 ms) so a remote provider's real p95 can be accommodated;
            # a timed-out call returns None and never blocks the reply loop.
            _timeout_ms = getattr(self, "embedding_timeout_ms", EMBED_TIMEOUT_MS_DEFAULT)
            try:
                _timeout_s = max(0.1, min(15.0, float(_timeout_ms) / 1000.0))
            except Exception:
                _timeout_s = EMBED_TIMEOUT_S
            data = await asyncio.wait_for(
                asyncio.to_thread(self._ipv4_json, url, headers, payload, _timeout_s),
                timeout=_timeout_s)
            vec = data["data"][0]["embedding"]
            if not isinstance(vec, list) or not vec:
                return None
            if _cache_on:
                EMBED_CACHE[cache_key] = vec
                EMBED_CACHE.move_to_end(cache_key)
                while len(EMBED_CACHE) > EMBED_CACHE_MAX:
                    EMBED_CACHE.popitem(last=False)
            return vec
        except Exception as exc:
            logger.warning("[biocore] embedding failed: %s", exc)
            return None

    @staticmethod
    def _cosine(a, b) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if na and nb else 0.0

    def _dedupe_sentences(self, text: str) -> str:
        """C-S1 deterministic sentence dedup (char-bigram Jaccard >= 0.92).

        M5: only the deterministic fallback is implemented. The LIT/spec
        "embedding 0.90" + quote/code-block whitelist variants are NOT
        implemented and are no longer claimed in ACC/LIT.
        """
        if not getattr(self, "sentence_dedup_enabled", False):
            return text
        try:
            import re as _re
            parts = [p for p in _re.split(r"(?<=[。！？；！？;\n])", str(text or "")) if p.strip()]
            kept = []

            def _bigrams(s):
                s = "".join(_re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", s))
                return {s[i:i + 2] for i in range(max(0, len(s) - 1))} if len(s) >= 2 else {s}

            def _jac(a, b):
                if not a and not b:
                    return 1.0
                return len(a & b) / max(1, len(a | b))

            for sent in parts:
                must = bool(_re.search(r"[0-9０-９]|不|没|别|未|无", sent))
                dup = False
                if not must:
                    b = _bigrams(sent)
                    for prev in kept:
                        if _jac(b, _bigrams(prev)) >= SENTENCE_DEDUP_THRESHOLD:
                            dup = True
                            break
                if not dup:
                    kept.append(sent)
            out = "".join(kept).strip()
            return out or str(text or "")
        except Exception:
            return text

    @staticmethod
    def _usable_memory_text(text: str) -> bool:
        t = (text or "").strip()
        if not t:
            return False
        if t.startswith("注意，你正在社交媒体"):
            return False
        if t.startswith("[BioCore]"):
            return False
        return True

    # ------------------------------------------------------------------
    # ams-life: one memory library for every group and private chat.
    #
    # Every entry carries an origin (discretion.make_origin). Code that works
    # on "this session" gets a view holding only the entries that came from
    # this place, exactly like BioCore's old per-session file; saving the view
    # writes them back and leaves the other places untouched. Per-place
    # bookkeeping (working set, last recall trace, ...) lives in rooms[place].
    # ------------------------------------------------------------------
    def _here(self, event) -> str:
        return adapter_astrbot_turn.incoming_of(event).place

    def _vector_store(self):
        store = getattr(self, "_vectors_db", None)
        if store is None:
            store = self._vectors_db = vector_store.VectorStore(MEMORY_VECTOR_PATH)
        return store

    def _read_library(self, vectors=True) -> dict:
        """The whole library; each memory gets its vector back from the vector store
        (vectors=False: without, for code that only looks at ids or text)."""
        try:
            d = json.loads(MEMORY_LIBRARY_PATH.read_text(encoding="utf-8"))
            if isinstance(d, dict):
                if not isinstance(d.get("entries"), list):
                    d["entries"] = []
                if not isinstance(d.get("rooms"), dict):
                    d["rooms"] = {}
                if vectors:
                    self._vector_store().attach(d["entries"])
                return d
        except Exception:
            pass
        return {"entries": [], "rooms": {}}

    def _write_library(self, lib) -> bool:
        """Write the whole library: nothing the forget registry rules out is kept; vectors
        go to the vector store (memories whose id is their own), and the vectors of
        memories no longer in the library go with them. False: not written (the registry
        could not be read)."""
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        lib["schema_version"] = MEMORY_SCHEMA_VERSION
        try:
            # new memories only (the library is not gone over again on every write), and ones whose
            # words changed (merged, tidied up): numbers out, and not kept over a red line while
            # the switch is on
            old_ids = self._library_ids() if MEMORY_LIBRARY_PATH.exists() else set()
            old_text = getattr(self, "_known_memory_texts", None) or {}
            new = [e for e in lib.get("entries") or [] if isinstance(e, dict)
                   and (str(e.get("id") or "") not in old_ids or old_text.get(str(e.get("id") or "")) != e.get("text"))]
            red = {id(e) for e in new if self._red_line(e.get("text"), "memory")}
            kept = [e for e in lib.get("entries") or [] if self._origin_kept(e) and id(e) not in red]
            if new:
                scrub = self._gone_remover()
                for e in new:
                    if isinstance(e.get("text"), str):
                        e["text"] = scrub(e["text"])
        except forget_registry.Unreadable as exc:
            # never filter with a registry that cannot be read: nothing is written this time
            logger.warning("[ams-life] forget registry unreadable, library not written: %s", exc)
            return False
        lib["entries"] = kept
        store = self._vector_store()
        out = dict(lib, entries=store.detach(lib["entries"]))
        tmp = MEMORY_LIBRARY_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
        atomic_file.replace(tmp, MEMORY_LIBRARY_PATH)
        store.keep_only(str(e["id"]) for e in lib["entries"] if isinstance(e, dict) and e.get("id"))
        self._known_memory_texts = {str(e.get("id") or ""): e.get("text") for e in lib["entries"] if isinstance(e, dict)}
        self._known_memory_ids = set(self._known_memory_texts)
        return True

    def _library_ids(self) -> set:
        """The ids in the library: read once, then kept up to date by _write_library (with
        each one's words, _known_memory_texts, so that changed words are told apart)."""
        ids = getattr(self, "_known_memory_ids", None)
        if ids is None or getattr(self, "_known_memory_texts", None) is None:
            self._known_memory_texts = {str(e.get("id") or ""): e.get("text") for e in
                                        self._read_library(vectors=False)["entries"] if isinstance(e, dict)}
            ids = self._known_memory_ids = set(self._known_memory_texts)
        return ids

    def _new_memory_id(self, *seed, taken=()) -> str:
        """An id no other memory has: a hash of where, when and what, lengthened on the
        (unlikely) chance it is taken. `taken`: ids not written to the library yet."""
        used = self._library_ids() | {str(x) for x in taken}
        base = _sha256("|".join(str(x) for x in seed))[:12]
        eid, n = base, 1
        while eid in used:
            n += 1
            eid = "%s-%d" % (base, n)
        return eid

    def _migrate_memory_ids(self) -> None:
        """Give every memory an id of its own, then move the vectors out of the library.

        Memories without an id (her replies were written without one) or sharing one (an
        id used to be a hash of the text, so the same words in two places shared it) get
        a new one; the first of a shared id keeps it. The library is copied into
        MEMORY_ARCHIVE_DIR first (never deleted). Nothing to do: nothing is written."""
        if not MEMORY_LIBRARY_PATH.exists():
            return
        lib = self._read_library(vectors=False)
        seen, fixes = set(), []
        for e in lib["entries"]:
            if not isinstance(e, dict):
                continue
            eid = str(e.get("id") or "")
            if not eid or eid in seen:
                fixes.append(e)
            else:
                seen.add(eid)
        if fixes:
            MEMORY_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(MEMORY_LIBRARY_PATH), str(
                MEMORY_ARCHIVE_DIR / ("library.before-ids-%s.json" % time.strftime("%Y%m%d-%H%M%S"))))
            for e in fixes:
                e["id"] = self._new_memory_id(discretion.origin_of(e)["where"], e.get("ts"), e.get("role"),
                                              e.get("text"), taken=seen)
                seen.add(e["id"])
            tmp = MEMORY_LIBRARY_PATH.with_suffix(".tmp")
            tmp.write_text(json.dumps(lib, ensure_ascii=False), encoding="utf-8")
            atomic_file.replace(tmp, MEMORY_LIBRARY_PATH)
            self._known_memory_ids = set(seen)
            self._known_memory_texts = {str(e.get("id") or ""): e.get("text") for e in lib["entries"]
                                        if isinstance(e, dict)}
            logger.info("[ams-life] gave %d memories an id of their own", len(fixes))
        moved = vector_store.migrate_library(MEMORY_LIBRARY_PATH, MEMORY_VECTOR_PATH, MEMORY_ARCHIVE_DIR)
        if moved.get("moved"):
            logger.info("[ams-life] moved %d memory vectors out of the library", moved["moved"])

    def _library_places(self) -> list:
        lib = self._read_library()
        places = set(lib["rooms"]) | {discretion.origin_of(e)["where"] for e in lib["entries"]}
        return sorted(p for p in places if p)

    def _migrate_memory_library(self) -> None:
        """Fold BioCore's memory/<session>.json files into the library (once).

        The old files are moved into MEMORY_LEGACY_DIR, never deleted. BioCore's
        cross-session copies are skipped: the original is in its own file.
        """
        if MEMORY_LIBRARY_PATH.exists() or not MEMORY_DIR.exists():
            return
        old = sorted(f for f in MEMORY_DIR.glob("*.json") if f.is_file())
        if not old:
            return
        lib = {"entries": [], "rooms": {}}
        for f in old:
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(d, dict):
                continue
            here = discretion.place_of(f.stem)
            for e in d.get("entries") or []:
                if not isinstance(e, dict) or e.get("shared_from_session"):
                    continue
                o = discretion.origin_of(e, here)
                e["origin"] = discretion.make_origin(here, o["people"], o["source_ids"], o["visibility"])
                lib["entries"].append(e)
            lib["rooms"][here] = {k: v for k, v in d.items() if k not in ("entries", "schema_version")}
        self._write_library(lib)
        MEMORY_LEGACY_DIR.mkdir(parents=True, exist_ok=True)
        for f in old:
            shutil.move(str(f), str(MEMORY_LEGACY_DIR / f.name))
        logger.info("[ams-life] one memory library: %d entries from %d session files",
                    len(lib["entries"]), len(old))

    def _memory_path(self, event):
        return MEMORY_LIBRARY_PATH

    def _load_memory(self, event):
        try:
            here = self._here(event)
            lib = self._read_library()
            d = dict(lib["rooms"].get(here) or {})
            d["entries"] = [e for e in lib["entries"]
                            if isinstance(e, dict) and discretion.origin_of(e)["where"] == here]
            if isinstance(d, dict) and isinstance(d.get("entries"), list):
                d["entries"] = [e for e in d["entries"]
                                if isinstance(e, dict)
                                and self._usable_memory_text(str(e.get("text", "")))]
                try:
                    for entry in d["entries"]:
                        entry.setdefault("inhibition", 0.0)
                        entry.setdefault("suppression_count", 0)
                        entry.setdefault("memory_tier", "warm")
                        # Lazy migration: pre-provenance data is direct user/
                        # model input, not "unknown". This runs for every old
                        # entry on load, then persists on the next save.
                        if not entry.get("memory_source") and not entry.get("memory_confidence"):
                            entry["memory_source"] = "direct"
                            entry["memory_confidence"] = 0.7
                            entry["legacy_backfilled"] = True
                    if int(d.get("schema_version", 0) or 0) < MEMORY_SCHEMA_VERSION:
                        d["schema_version"] = MEMORY_SCHEMA_VERSION
                except Exception:
                    pass
                return d
        except Exception:
            pass
        return {"entries": []}

    def _merge_memory_doc(self, doc, latest) -> dict:
        """Merge concurrently-written entries into the consolidation doc (BUG-03)."""
        if not isinstance(doc, dict):
            return doc
        if not isinstance(latest, dict):
            return doc
        cur = doc.get("entries") if isinstance(doc.get("entries"), list) else []
        new = latest.get("entries") if isinstance(latest.get("entries"), list) else []
        known_ids = {str(x.get("id") or "") for x in cur if isinstance(x, dict)}
        known_keys = {(str(x.get("text") or ""), round(float(x.get("ts", 0) or 0), 3))
                      for x in cur if isinstance(x, dict)}
        for entry in new:
            if not isinstance(entry, dict):
                continue
            eid = str(entry.get("id") or "")
            key = (str(entry.get("text") or ""), round(float(entry.get("ts", 0) or 0), 3))
            if (eid and eid in known_ids) or (not eid and key in known_keys):
                continue
            cur.append(entry)
            if eid:
                known_ids.add(eid)
            known_keys.add(key)
        doc["entries"] = cur
        if isinstance(latest.get("write_log"), list):
            logs = doc.get("write_log") if isinstance(doc.get("write_log"), list) else []
            for row in latest["write_log"]:
                if isinstance(row, dict) and row not in logs:
                    logs.append(row)
            doc["write_log"] = logs[-200:]
        if isinstance(latest.get("working_set"), list):
            ws = doc.get("working_set") if isinstance(doc.get("working_set"), list) else []
            for item in latest["working_set"]:
                if str(item) and str(item) not in {str(x) for x in ws}:
                    ws.append(str(item))
            doc["working_set"] = ws[-32:]
        return doc

    def _save_memory(self, event, doc):
        try:
            if not isinstance(doc, dict) or self._job_stale():
                return
            doc["schema_version"] = MEMORY_SCHEMA_VERSION
            here = self._here(event)
            mine = [e for e in (doc.get("entries") or []) if isinstance(e, dict)]
            for e in mine:
                if not isinstance(e.get("origin"), dict):
                    o = discretion.origin_of(e, here)
                    e["origin"] = o if o["where"] else discretion.make_origin(here, o["people"], o["source_ids"])
            lib = self._read_library()
            lib["entries"] = [e for e in lib["entries"]
                              if not (isinstance(e, dict) and discretion.origin_of(e)["where"] == here)] + mine
            lib["rooms"][here] = {k: v for k, v in doc.items() if k not in ("entries", "schema_version")}
            self._write_library(lib)
        except Exception as exc:
            logger.warning("[biocore] memory save failed: %s", exc)

    def _memory_bio(self, core):
        if core is None:
            return None
        return core

    def _memory_importance(self, core, role: str) -> float:
        if core is None:
            return 0.5
        salience = 0.25 + 0.35 * float(getattr(core, "a", 0.5)) + 0.25 * abs(float(getattr(core, "v", 0.0)))
        salience += 0.15 * (1.0 - float(getattr(core, "trust", 0.5)))
        if role == "assistant":
            salience *= 0.9
        return max(0.15, min(1.0, salience))

    @staticmethod
    def _restabilize_if_expired(entry: dict, now=None) -> bool:
        """Nader reconsolidation: an expired labile window restabilizes.

        Recall is the moment the memory is re-touched, so it is also the
        moment a stale destabilized window must be closed and timestamped.
        """
        try:
            if not isinstance(entry, dict):
                return False
            if entry.get("reconsolidation_state") != "destabilized":
                return False
            _now = time.time() if now is None else float(now)
            if float(entry.get("destabilized_until", 0) or 0) >= _now:
                return False
            entry["reconsolidation_state"] = "restabilized"
            entry["restabilized_ts"] = _now
            return True
        except Exception:
            return False

    def _memory_score_parts(self, core, entry: dict, cosine: float, *,
                            query_text: str = "", hybrid: bool = False,
                            sensitive_protect: bool = False) -> dict:
        """Return the deterministic score plus its bounded component factors.

        L-T02/C-T01: storing the factors here lets the runtime expose an
        auditable retrieval-contribution trace without the LLM ever generating
        one and without changing the ranking math.
        """
        # G8: slow 30-day decay with a 0.15 floor, computed on read only.
        importance = memory_meta.effective_importance(entry)
        age = max(0.0, time.time() - float(entry.get("ts", 0) or 0))
        age_days = age / 86400.0
        _retention_model = getattr(core, "retention_model", "power_law") if core is not None else "power_law"
        # Task-20 P0-3: power law / multi-scale retention (both kept; single=legacy).
        if _retention_model in ("power_law", "multi_scale"):
            recency = memory_meta.retention_weight(age_days, _retention_model)
        else:
            recency = 1.0 / math.pow(1.0 + max(0.0, age_days) * 0.35, 0.55)
        try:
            recall_count = int(entry.get("recall_count", 0) or 0)
        except Exception:
            recall_count = 0
        # G7: co-recall counts are read through a 30-day half-life decay so
        # an old association cannot stay permanently boosted.
        assoc = memory_meta.decayed_assoc(entry)
        try:
            due = 1.15 if 0 < float(entry.get("next_review_ts", 0) or 0) <= time.time() else 1.0
        except Exception:
            due = 1.0
        try:
            stability = max(0.2, float(entry.get("stability_days", 1.0) or 1.0))
        except Exception:
            stability = 1.0
        retention = math.exp(-age_days / stability)
        try:
            _d = ACT_R_DECAY
            _b = math.log(max(1e-9, (age_days + 0.05) ** (-_d)))
            base = 1.0 / (1.0 + math.exp(-(_b + 1.0)))
        except Exception:
            base = 0.5
        try:
            # G9: read-time decay so an old self-model match cannot stay maxed.
            schema = memory_meta.effective_schema_congruence(entry)
        except Exception:
            schema = 0.0
        inhibition = memory_meta.retrieval_inhibition(entry)
        regulation = str(getattr(core, "regulation", "none") or "none") if core is not None else "none"
        regulation_mod = memory_meta.regulation_memory_modifier(entry, regulation)
        lexical_mod = 1.0
        if hybrid and query_text:
            try:
                entry_text = str(entry.get("text") or "")
                variants = memory_meta.expand_query(query_text)
                lexical = max(memory_meta.lexical_overlap(variant, entry_text)
                              for variant in variants) if variants else 0.0
                lexical_mod = 1.0 + 0.12 * lexical
            except Exception:
                lexical_mod = 1.0
        sensitive_mod = 1.0
        if sensitive_protect:
            sensitive_mod = memory_meta.sensitivity_weight(entry)
        source_weight = memory_meta.retrieval_weight(entry)
        score = (cosine * (0.40 + 0.60 * importance) * recency
                 * (0.65 + 0.35 * retention)
                 * (0.85 + 0.15 * base)
                 * (1.0 + 0.10 * math.log1p(max(0, recall_count)))
                 * due
                 * (1.0 + 0.05 * math.log1p(max(0, assoc)))
                 * source_weight
                 * (1.0 + 0.10 * schema)
                 * (1.0 - 0.15 * inhibition)
                 * regulation_mod
                 * lexical_mod
                 * sensitive_mod)
        # C-S2: retrieval salience 0.9-1.1 x mask (Seeley 2007 inspired; not attention).
        _sal_factor = 1.0
        if getattr(self, "salience_boost_enabled", False):
            try:
                _c = max(0.0, min(1.0, float(cosine)))
                if _c > 0.0:
                    _sal_factor = 0.90 + 0.20 * _c
                    score *= _sal_factor
            except Exception:
                _sal_factor = 1.0
        # Batch4 L18: Anderson & Reder 1999 (10.1037/0096-3445.128.2.186)
        # fan penalty S=S-ln(fan): score *= 1/(1+g*ln(1+assoc+links)), floor.
        if getattr(self, "fan_penalty_enabled", False):
            try:
                _links = entry.get("links") if isinstance(entry.get("links"), list) else []
                try:
                    _raw_assoc = sum(int(v) for v in (entry.get("assoc") or {}).values())
                except Exception:
                    _raw_assoc = 0
                _fan = min(int(getattr(self, "fan_cap", 32) or 32), _raw_assoc + len(_links))
                _pen = max(float(getattr(self, "fan_floor", 0.70)),
                           1.0 / (1.0 + float(getattr(self, "fan_gain", 0.10)) * math.log1p(max(0, _fan))))
                score *= _pen
            except Exception:
                pass
        return {
            "score": float(score),
            "salience": round(_sal_factor, 4),
            "cosine": round(float(cosine), 6),
            "importance": round(importance, 4),
            "recency": round(recency, 4),
            "retention": round(0.65 + 0.35 * retention, 4),
            "base": round(0.85 + 0.15 * base, 4),
            "recall_boost": round(1.0 + 0.10 * math.log1p(max(0, recall_count)), 4),
            "assoc_boost": round(1.0 + 0.05 * math.log1p(max(0, assoc)), 4),
            "due": round(due, 4),
            "source_weight": round(float(source_weight), 4),
            "schema": round(schema, 4),
            "inhibition": round(float(inhibition), 4),
            "regulation": round(float(regulation_mod), 4),
            "lexical": round(float(lexical_mod), 4),
            "sensitive": round(float(sensitive_mod), 4),
        }

    def _memory_trace_components(self, parts: dict) -> dict:
        """Read-only ranking factors for the retrieval trace (M6).

        ``salience`` is exposed only when C-S2 is enabled, so the default-off
        trace stays byte-identical to 1.2.98; the factor itself is always 1.0
        when the switch is off.
        """
        keys = ("recency", "retention", "schema", "inhibition", "regulation",
                "lexical", "sensitive", "source_weight")
        out = {k: parts[k] for k in keys if k in parts}
        if getattr(self, "salience_boost_enabled", False) and "salience" in parts:
            out["salience"] = parts["salience"]
        return out

    def _memory_score(self, core, entry: dict, cosine: float, *,
                      query_text: str = "", hybrid: bool = False,
                      sensitive_protect: bool = False) -> float:
        parts = self._memory_score_parts(
            core, entry, cosine, query_text=query_text,
            hybrid=hybrid, sensitive_protect=sensitive_protect)
        score = float(parts.get("score", 0.0))
        try:
            trace = getattr(core, "_last_memory_trace", None) if core is not None else None
            if isinstance(trace, dict):
                eid = str(entry.get("id") or "")
                if eid and eid in [str(x) for x in (trace.get("entry_ids") or [])]:
                    valence = max(-1.0, min(1.0, float(trace.get("valence", 0.0) or 0.0)))
                    score *= 1.0 + 0.04 * valence
        except Exception:
            pass
        return max(0.0, score)

    def _attention_gate_admit(self, score: float, entry_id: str = "") -> bool:
        """L17 hard/probabilistic gate (Anderson et al. 2004, 10.1037/0033-295X.111.4.1036)."""
        try:
            _a = math.log(max(1e-9, float(score)))
            _tau = math.log(RETRIEVAL_THRESHOLD) + float(getattr(self, "attention_gate_shift", 0.0) or 0.0)
            _s = max(1e-6, float(getattr(self, "attention_gate_s", 0.30) or 0.30))
            _p = 1.0 / (1.0 + math.exp(-((_a - _tau) / _s)))
            if str(getattr(self, "attention_gate_mode", "hard")) == "probabilistic":
                _seed = int(getattr(self, "attention_seed", 0) or 0)
                if _seed > 0:
                    _h = 0
                    for _ch in str(entry_id):
                        _h = (_h * 131 + ord(_ch)) % 2147483647
                    _rng = __import__("random").Random(_seed * 1000003 + _h)
                else:
                    _rng = __import__("random").Random()
                return float(_rng.random()) < _p
            return _p >= 0.5
        except Exception:
            return float(score) >= RETRIEVAL_THRESHOLD

    def _working_set_capacity(self, core) -> int:
        """Batch4 L19: Cowan 2001 capacity (default 8 legacy; flag -> cowan)."""
        if getattr(self, "cowan_capacity_enabled", False):
            return max(3, min(6, int(getattr(self, "cowan_capacity", 4) or 4)))
        return max(4, self._memory_top_k(core) * 2)

    def _memory_top_k(self, core, partner_trust=None) -> int:
        """ams-life: `partner_trust` is the trust in the person she is answering (passed in;
        there is no global trust); she recalls a little more for someone she trusts."""
        k = 4
        if partner_trust is not None and float(partner_trust) > 0.65:
            k += 1
        if core is not None:
            if float(getattr(core, "stress", 0.0)) > 0.65:
                k -= 1
            if float(getattr(core, "energy", 1.0)) < 0.35:
                k -= 1
            if float(getattr(core, "attention", 0.5)) > 0.7:
                k += 1
            elif float(getattr(core, "attention", 0.5)) < 0.3:
                k -= 1
        k = max(2, min(6, k))
        if getattr(self, "attention_topk_cap_enabled", False):
            k = min(k, int(getattr(self, "attention_topk_cap", 4) or 4))
        return k

    def _memory_thresholds(self, core):
        compression = self.api_config.get("compression") if isinstance(self.api_config.get("compression"), dict) else {}
        threshold = max(1000, int(compression.get("threshold", 6000) or 6000))
        limit = max(120, int(compression.get("max_chars", 800) or 800))
        if core is not None:
            stress = float(getattr(core, "stress", 0.0))
            threshold = int(threshold * (1.0 + 0.5 * stress))
            limit = int(limit * (1.0 + 0.2 * stress))
        return bool(compression.get("enabled")), threshold, limit

    def _trim_memory(self, doc, core=None):
        entries = doc.get("entries")
        if not isinstance(entries, list):
            entries = []
            doc["entries"] = entries
        if not entries:
            return
        enabled, threshold, summary_limit = self._memory_thresholds(core)
        if not enabled:
            entries[:] = entries[-80:]
            return
        # Keep summarized originals for provenance; only trim active entries.
        _archived = [e for e in entries if e.get("summarized")]
        _active = [e for e in entries if not e.get("summarized")]
        _active = _active[-200:]
        entries[:] = sorted(_archived + _active, key=lambda e: float(e.get("ts", 0) or 0))

    def _schedule_consolidation(self, event, core=None):
        enabled, threshold, _ = self._memory_thresholds(core)
        if not enabled:
            return
        try:
            doc = self._load_memory(event)
            total = sum(len(str(e.get("text", ""))) for e in (doc.get("entries") or []))
            if total <= threshold:
                return
        except Exception:
            return
        if getattr(self, "_consolidating", False):
            return
        if time.time() - float(getattr(self, "_last_consolidation", 0.0)) < 300:
            return
        self._last_consolidation = time.time()
        self._consolidating = True
        asyncio.create_task(self._consolidate_memory(event, core))

    async def _consolidate_memory(self, event, core=None, force=False):
        try:
            # ams-life: forgetting may happen while this waits for the model; if
            # it does, the copy held here is stale and must not be saved back.
            self._begin_job(self._here(event))
            doc = self._load_memory(event)
            entries = doc.get("entries")
            if not isinstance(entries, list) or len(entries) < 2:
                return
            enabled, threshold, _ = self._memory_thresholds(core)
            if not enabled and not force:
                return
            total = sum(len(str(e.get("text", ""))) for e in entries)
            if total <= threshold and not force:
                return
            _delay_s = int(getattr(self, "event_summary_delay_hours", 6) or 0) * 3600
            try:
                _last_summary = float(doc.get("last_event_summary_ts", 0) or 0)
            except Exception:
                _last_summary = 0.0
            if not force and _delay_s > 0 and (_last_summary <= 0 or time.time() - _last_summary < _delay_s):
                if _last_summary <= 0:
                    doc["last_event_summary_ts"] = time.time()
                    self._save_memory(event, doc)
                return
            doc["last_event_summary_ts"] = time.time()
            _summary_use_llm = self._llm_allowed("memory_summary")
            provider = await self._provider_for("memory_summary", event) if _summary_use_llm else None
            now = time.time()
            _attachments = []
            for _e in entries:
                try:
                    _attachments.extend(_e.get("attachments") or [])
                except Exception:
                    pass
            used = set()
            groups = []
            for i, e in enumerate(entries):
                if i in used or e.get("role") == "summary":
                    continue
                group = [i]
                used.add(i)
                for j in range(i + 1, len(entries)):
                    if j in used or entries[j].get("role") == "summary":
                        continue
                    if self._cosine(e.get("vector") or [], entries[j].get("vector") or []) >= 0.86:
                        group.append(j)
                        used.add(j)
                if len(group) >= 2:
                    # BUG-06: summarize in batches, never drop entries beyond 8.
                    for _off in range(0, len(group), 8):
                        _chunk = group[_off:_off + 8]
                        if len(_chunk) >= 2:
                            groups.append(_chunk)
                if len(groups) >= 9:
                    break
            if not groups:
                if time.time() - float(getattr(self, "_last_event_archive", 0.0)) > 300:
                    self._last_event_archive = time.time()
                    await self._archive_ranked_events(event, core, entries)
                    await self._maybe_archive_insight(event, core, "compression")
                return
            changed = False
            for group in groups:
                _raw_texts = [self._mask_if_safety(str(entries[i].get("text", "")).strip()) for i in group
                              if str(entries[i].get("text", "")).strip()]
                # Dedupe near-identical memories before spending summary tokens;
                # grouping above already uses embedding cosine (>=0.86).
                texts = memory_meta.dedupe_texts(_raw_texts, threshold=0.88, limit=0)
                if len(texts) < 2:
                    continue
                payload = {"summary": "", "candidates": []}
                if _summary_use_llm and provider is not None:
                    prompt = interpretation.memory_summary_prompt(texts)
                    try:
                        reply = await self._model(provider).chat(prompt=prompt)
                        payload = interpretation.parse_memory_summary_payload(
                            reply.text,
                            getattr(self, "summary_max_chars", 0))
                    except Exception as exc:
                        logger.warning("[biocore] memory summary failed: %s", exc)
                else:
                    # Deterministic extractive summary from embedding-grouped and
                    # deduped representatives; no LLM involved.
                    payload["summary"] = "；".join(texts[:5])
                summary = self._mask_if_safety(self._summary_cap(str(payload.get("summary") or "")))
                candidates = payload.get("candidates") or []
                if not getattr(self, "llm_memory_candidates", True):
                    candidates = []
                if not summary:
                    continue
                # M1: a summary of tagged-sensitive memories is withheld from
                # the provider when safety is on (default off => unchanged).
                _summary_sens = memory_meta.classify_sensitivity(summary)
                _group_sensitive = any(bool(entries[i].get("sensitive")) for i in group)
                vec = await self._embed_text_guarded(
                    summary, _group_sensitive or bool(_summary_sens.get("sensitive")))
                if not vec:
                    continue
                importance = max(float(entries[i].get("importance", 0.5) or 0.5) for i in group)
                _sum_id = "sum_" + self._new_memory_id(
                    "summary", self._here(event), now, len(entries),
                    taken=[str(x.get("id") or "") for x in entries if isinstance(x, dict)])
                for i in sorted(group, reverse=True):
                    _old = entries[i]
                    _old["summarized"] = True
                    _old["summary_id"] = _sum_id
                    _old["summarized_ts"] = now
                _src_prov = []
                for i in group:
                    _p = entries[i].get("provenance") if isinstance(entries[i], dict) else None
                    if isinstance(_p, dict):
                        _src_prov.append(_p)
                _summary_prov = {
                    "sender_id": "summary", "sender_name": "她",
                    "session": self._here(event),
                    "ts": now, "message_refs": [],
                    "sources": [{
                        "sender_id": str(_p.get("sender_id") or ""),
                        "sender_name": str(_p.get("sender_name") or ""),
                        "session": str(_p.get("session") or ""),
                        "ts": float(_p.get("ts", 0) or 0),
                        "message_refs": list(_p.get("message_refs") or [])[:6],
                    } for _p in _src_prov][-24:],
                }
                # ams-life: a summary (and any fact drawn from it) comes from every entry of
                # its group: all their people and source ids, not just each one's sender
                _go = discretion.merge([discretion.origin_of(entries[i]) for i in group])
                _group_origin = discretion.make_origin(self._here(event), _go["people"],
                                                       _go["source_ids"], _go["visibility"])
                _summary_source = "inferred"
                _summary_conf = memory_meta.initial_confidence(_summary_source, importance)
                entries.append({"id": _sum_id, "text": self._summary_cap(summary), "role": "summary",
                                "scope": "session",
                                "vector": vec, "ts": now, "hits": 1,
                                "importance": importance, "last_used": now,
                                "summary_id": _sum_id, "provenance": _summary_prov,
                                "origin": _group_origin,
                                "memory_source": _summary_source,
                                "memory_confidence": _summary_conf,
                                "memory_tier": "warm", "conflict": False,
                                "last_write_op": "ADD", "last_write_ts": now,
                                "write_ops": {"ADD": 1}, "schema_congruence": 0.0,
                                "self_defining": False, "inhibition": 0.0,
                                "suppression_count": 0,
                                "encoding_regulation": str(getattr(core, "regulation", "none") or "none"),
                                "encoding_emotion": str((getattr(core, "labels", {}) or {}).get("emotion") or "neutral"),
                                "encoding_emotion_secondary": self._secondary_emotion(core),
                                "sensitive": bool(_summary_sens.get("sensitive")),
                                "pii_types": list(_summary_sens.get("types") or []),
                                "sensitivity": float(_summary_sens.get("score") or 0.0)})
                memory_meta.append_write_log(doc, op="ADD", entry_id=_sum_id,
                                             reason="summary", ts=now)
                # LLM proposes candidate facts; the deterministic policy here
                # decides ADD/UPDATE/NOOP and can never DELETE. Confidence is
                # capped below direct-user confidence by memory_meta.
                _cand_applied = 0
                for _cand in (candidates or [])[:memory_meta.CANDIDATE_MAX]:
                    try:
                        _ctext = str(_cand.get("text") or "").strip()
                        if len(_ctext) < 4:
                            continue
                        _cvec = await self._embed_text(_ctext)
                        if not _cvec:
                            continue
                        _best, _best_cos = None, 0.0
                        for _ce in entries:
                            if not isinstance(_ce, dict) or _ce.get("deleted") or _ce.get("summarized"):
                                continue
                            _cos = self._cosine(_cvec, _ce.get("vector") or [])
                            if _cos > _best_cos:
                                _best, _best_cos = _ce, _cos
                        _res = memory_meta.apply_memory_candidate(
                            entries, _cand, match=_best, cosine=_best_cos,
                            vector=_cvec, now=now, provenance=_summary_prov)
                        _entry = _res.get("entry")
                        if _res.get("op") in ("ADD", "UPDATE") and isinstance(_entry, dict):
                            # ams-life: a new fact comes from the group; an updated one now
                            # holds words of the group as well as its own
                            _prev = [discretion.origin_of(_entry)] if _res.get("op") == "UPDATE" else []
                            _co = discretion.merge(_prev + [_group_origin])
                            _entry["origin"] = discretion.make_origin(self._here(event), _co["people"],
                                                                      _co["source_ids"], _co["visibility"])
                            self._apply_memory_encoding(_entry, core, now, _ctext)
                            memory_meta.append_write_log(
                                doc, op=_res["op"], entry_id=str(_entry.get("id") or ""),
                                reason="candidate", ts=now)
                            _cand_applied += 1
                    except Exception:
                        continue
                if _cand_applied:
                    logger.info("[biocore] llm memory candidates applied=%s", _cand_applied)
                changed = True
            if changed:
                if self._job_stale():
                    return
                await self._archive_ranked_events(event, core, entries)
                await self._maybe_archive_insight(event, core, "compression")
                if self._job_stale():
                    return
                try:
                    self._merge_memory_doc(doc, self._load_memory(event))
                except Exception:
                    pass
                self._trim_memory(doc, core)
                if core is not None:
                    try:
                        core.integrate_noise("memory_summary", attention=0.004,
                                             energy=-0.002)
                    except Exception:
                        pass
                self._save_memory(event, doc)
                logger.info("[biocore] memory consolidated groups=%s entries=%s", len(groups), len(entries))
        finally:
            self._consolidating = False

    @staticmethod
    def _memory_command_line(cmd: dict) -> str:
        """Deterministic one-line data hint describing an executed memory command."""
        cmd = cmd or {}
        op = str(cmd.get("op") or "NOOP")
        target = str(cmd.get("target") or "").strip()[:40]
        if op == "PENDING":
            return "- 待确认：用户要求删除关于「%s」的记忆；用户回复“确认”后才执行。" % target
        if op == "DELETE":
            return "- 已删除关于「%s」的记忆（软删除，可恢复）。" % target
        if op == "RESTORE":
            return "- 已恢复最近删除的一条记忆。"
        if op == "ROLLBACK":
            _text = str((cmd.get("entry") or {}).get("text") or "")[:40]
            return "- 已把一条记忆回滚到上一版本：%s" % _text
        reason = str(cmd.get("reason") or "")
        if reason == "ambiguous":
            return "- 删除请求匹配到多条记忆，未执行；需要用户说得更具体。"
        if reason == "vague_target":
            return "- 删除请求缺少具体对象，未执行；需要用户说明要删除哪条记忆。"
        if reason == "no_match":
            # Silent: ordinary sentences containing delete words must not inject
            # a fake memory line into the prompt.
            return ""
        if reason == "no_restore_target":
            return "- 没有可恢复的已删除记忆。"
        if reason == "no_rollback_target":
            return "- 没有可回滚的记忆修改。"
        return ""

    def _self_schema_texts(self, core) -> list:
        """Bounded self-schema corpus for deterministic schema congruence."""
        texts = list(getattr(self, "schema_texts", []) or [])
        try:
            model = self.self_model or {}
            for key in ("who_am_i", "narrative"):
                value = str(model.get(key) or "").strip()
                if value:
                    texts.append(value)
            for key in ("boundaries", "consistency"):
                for item in (model.get(key) or []):
                    item = str(item or "").strip()
                    if item:
                        texts.append(item)
            # ams-life: her notebook (a score only; nothing of it is shown here)
            for item in (model.get("notebook") or []):
                item = str((item or {}).get("text") if isinstance(item, dict) else "").strip()
                if item:
                    texts.append(item)
        except Exception:
            pass
        return texts[:24]

    def _apply_memory_encoding(self, entry, core, now, text="") -> None:
        """Store deterministic encoding context: schema, regulation, affect."""
        if not isinstance(entry, dict):
            return
        try:
            schema = memory_meta.schema_congruence(
                text or str(entry.get("text") or ""), self._self_schema_texts(core))
            previous = 0.0
            try:
                previous = float(entry.get("schema_congruence", 0.0) or 0.0)
            except Exception:
                previous = 0.0
            entry["schema_congruence"] = round(max(previous, schema), 4)
            entry["self_defining"] = bool(
                memory_meta.is_self_defining(entry, entry["schema_congruence"]))
        except Exception:
            pass
        if core is not None:
            try:
                entry["encoding_regulation"] = str(getattr(core, "regulation", "none") or "none")
                entry["encoding_emotion"] = str((getattr(core, "labels", {}) or {}).get("emotion") or "neutral")
                entry["encoding_emotion_secondary"] = self._secondary_emotion(core)
                entry["encoding_valence"] = round(float(getattr(core, "v", 0.0) or 0.0), 3)
                entry["encoding_arousal"] = round(float(getattr(core, "a", 0.5) or 0.5), 3)
            except Exception:
                pass
        _body = text or str(entry.get("text") or "")
        try:
            sensitivity = memory_meta.classify_sensitivity(_body)
            entry["sensitive"] = bool(sensitivity.get("sensitive"))
            entry["pii_types"] = list(sensitivity.get("types") or [])
            entry["sensitivity"] = float(sensitivity.get("score") or 0.0)
        except Exception:
            pass
        try:
            poison = memory_meta.detect_poisoning(_body)
            entry["poison_risk"] = bool(poison.get("poison_risk"))
            entry["poison_signals"] = list(poison.get("signals") or [])
            entry["poison_score"] = float(poison.get("risk") or 0.0)
            if entry["poison_risk"]:
                try:
                    entry["memory_confidence"] = min(
                        float(entry.get("memory_confidence", 0.5) or 0.5), 0.25)
                except Exception:
                    entry["memory_confidence"] = 0.25
        except Exception:
            pass
        # Memory permission scope: user facts may be shared across the same
        # sender's sessions; assistant summaries stay session-local.
        _role = str(entry.get("role") or "user")
        entry.setdefault("scope", "session" if _role in ("assistant", "summary") else "user")
        try:
            entry["verification"] = memory_meta.verify_entry(entry)
        except Exception:
            pass
        entry.setdefault("inhibition", 0.0)
        entry.setdefault("suppression_count", 0)

    # ------------------------------------------------------------------
    # Privacy / deletion semantics
    # ------------------------------------------------------------------
    def _redact_archive_text(self, needle: str, session: str = "") -> int:
        """Redact a deleted memory text from event archives and insights.

        Best-effort, bounded and atomic per file: matching event fields and
        source_texts are replaced/dropped, insight rows are replaced. Source
        ids/message refs are left intact because they carry no raw text.
        """
        needle = str(needle or "").strip()
        if len(needle) < 4:
            return 0
        replacement = "[已删除]"
        fields = ("title", "event", "central_details", "peripheral_details",
                  "meaning_to_her", "reflection", "event_key")
        total = 0

        def _mutate_event(obj):
            nonlocal total
            hit = False
            for field in fields:
                value = obj.get(field)
                if isinstance(value, str) and needle in value:
                    obj[field] = value.replace(needle, replacement)
                    hit = True
            sources = obj.get("source_texts")
            if isinstance(sources, list):
                kept = [str(x) for x in sources if needle not in str(x)]
                if len(kept) != len(sources):
                    obj["source_texts"] = kept
                    obj["source_redacted"] = True
                    hit = True
            if hit:
                total += 1
            return hit

        try:
            self._rewrite_jsonl_atomic(EVENT_ARCHIVE_PATH, _mutate_event)
            if session:
                safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(session))[:80]
                self._rewrite_jsonl_atomic(EVENT_SESSION_DIR / safe / "events.jsonl",
                                           _mutate_event)
        except Exception:
            pass

        def _mutate_insight(obj):
            nonlocal total
            value = obj.get("insight")
            if isinstance(value, str) and needle in value:
                obj["insight"] = value.replace(needle, replacement)
                total += 1
                return True
            return False

        try:
            self._rewrite_jsonl_atomic(INSIGHT_ARCHIVE_PATH, _mutate_insight)
        except Exception:
            pass
        return total

    def _propagate_memory_deletion(self, event, entry, doc, reason: str = "user_delete") -> None:
        """Propagate one memory deletion to derived summaries/events/insights."""
        try:
            if not isinstance(entry, dict) or not isinstance(doc, dict):
                return
            raw_text = str(entry.get("text") or "")
            needle = raw_text.split("\n[再巩固]")[0].strip()
            if len(needle) < 4:
                return
            now = time.time()
            # 1) summaries derived from the deleted entry in the same doc.
            for summary in (doc.get("entries") or []):
                if not isinstance(summary, dict) or summary.get("role") != "summary":
                    continue
                text = str(summary.get("text") or "")
                if needle not in text:
                    continue
                summary["text"] = text.replace(needle, "[已删除]")[:1200]
                summary["source_deleted"] = True
                try:
                    summary["memory_confidence"] = min(
                        float(summary.get("memory_confidence", 0.4) or 0.4), 0.25)
                except Exception:
                    summary["memory_confidence"] = 0.25
                memory_meta.append_write_log(doc, op="REDACT",
                                             entry_id=str(summary.get("id") or ""),
                                             reason="summary_derived", ts=now)
            # 2) event archive + insights.
            session = self._here(event)
            changed = self._redact_archive_text(needle, session)
            if changed:
                memory_meta.append_write_log(
                    doc, op="REDACT", entry_id=str(entry.get("id") or ""),
                    reason="%s:%d" % (reason, changed), ts=now)
        except Exception as exc:
            logger.warning("[biocore] deletion propagation failed: %s", exc)

    def _cross_session_memory_entries(self, event) -> list:
        """ams-life: active entries from every other place in the library.

        Returns [(place, entry), ...]; the caller decides with the discretion
        table what may be used here. Never mutates the library.
        """
        try:
            here = self._here(event)
            out = []
            for entry in self._read_library()["entries"]:
                if not isinstance(entry, dict) or entry.get("deleted") or entry.get("summarized"):
                    continue
                where = discretion.origin_of(entry)["where"]
                if where and where != here:
                    out.append((where, entry))
            return out
        except Exception:
            return []

    def _apply_memory_trace(self, core, entries) -> dict:
        """Bounded memory-trace -> body nudge from recalled entries; trace read-only."""
        if core is None:
            return {}
        selected = [e for e in (entries or []) if isinstance(e, dict)][:8]
        if not selected:
            return {}
        total_w = 0.0
        val_sum = 0.0
        loop_count = 0
        ids = []
        for entry in selected:
            try:
                imp = max(0.05, min(1.0, float(entry.get("importance", 0.5) or 0.5)))
            except Exception:
                imp = 0.5
            try:
                val = float(entry.get("encoding_valence", entry.get("valence", 0.0)) or 0.0)
            except Exception:
                val = 0.0
            val = max(-1.0, min(1.0, val))
            val_sum += val * imp
            total_w += imp
            try:
                loop_count += max(0, int(entry.get("open_loop", 0) or 0))
            except Exception:
                pass
            eid = str(entry.get("id") or "")[:20]
            if eid:
                ids.append(eid)
        avg_val = (val_sum / total_w) if total_w > 0 else 0.0
        v_delta = max(-0.05, min(0.05, 0.05 * avg_val))
        stress_delta = max(-0.02, min(0.05, 0.005 * abs(avg_val) + 0.01 * min(3, loop_count)))
        try:
            core.apply_memory_trace(v_delta, stress_delta)
        except Exception:
            pass
        trace = {"count": len(selected), "valence": round(avg_val, 3),
                 "stress_delta": round(stress_delta, 4),
                 "entry_ids": ids[:8], "ts": round(time.time(), 3)}
        self._last_memory_trace = trace
        try:
            core._last_memory_trace = trace
        except Exception:
            pass
        return trace

    async def _memory_recall(self, event, text: str, core=None, extra: str = "", vec=None, voice: str = "", user_data=None,
                             turn=None) -> str:
        """Recall for this turn. ams-life: what the recall found (meta, cause trace,
        entry ids, memory trace) goes into `turn`, a dict of this request only, so a
        request in another window waiting meanwhile cannot swap it. The self._last_*
        copies are only for the status page."""
        turn = turn if isinstance(turn, dict) else {}
        self._last_memory_meta = turn["memory_meta"] = {
            "count": 0, "confidence": 0.0, "source": "unknown",
            "abstain": False, "tiers": {}, "answer_confidence": 0.0,
            "gate": "none", "conflicts": 0}
        turn.setdefault("cause_trace", [])
        turn.setdefault("memory_entries", [])
        try:
            _partner_trust = float((self._relationship_of(user_data).get("state") or {}).get("trust", 0.5) or 0.5)
        except Exception:
            _partner_trust = None
        if not self.memory_dedup_embedding or not self._usable_memory_text(text):
            return ""
        doc = self._load_memory(event)
        entries = doc.get("entries")
        if not isinstance(entries, list):
            entries = []
            doc["entries"] = entries
        # ams-life: no one changes her memory by what they say in a chat (the owner's
        # decision): BioCore's "删除记忆 / 恢复记忆 / 撤销修改 / 确认" commands are gone. Only
        # the owner deletes, in the panel.
        if vec is None:
            vec = await self._embed_text(text)
        if not vec:
            return ""
        scored = []
        retrieval_pairs = []
        duplicate = None
        now = time.time()
        _just_restabilized = set()
        _working_set = doc.get("working_set") if isinstance(doc.get("working_set"), list) else []
        for e in entries:
            if e.get("summarized") or e.get("deleted"):
                continue
            if getattr(self, "safety_enabled", False) and e.get("poison_risk"):
                continue
            if self._restabilize_if_expired(e, now):
                _just_restabilized.add(id(e))
            cosine = self._cosine(vec, e.get("vector") or [])
            score = self._memory_score(
                core, e, cosine, query_text=text,
                hybrid=bool(getattr(self, "hybrid_retrieval", True)),
                sensitive_protect=bool(getattr(self, "sensitive_memory_protection", True)))
            try:
                score *= memory_meta.working_set_boost(
                e, _working_set, ttl_seconds=memory_meta.WORKING_SET_TTL_SECONDS)
            except Exception:
                pass
            retrieval_pairs.append((e, cosine))
            if cosine >= 0.93:
                duplicate = e
            # ACT-R partial matching + retrieval threshold (named constants).
            if cosine >= PARTIAL_MATCH_THRESHOLD:
                _admit = score >= RETRIEVAL_THRESHOLD
                if getattr(self, "attention_gate_enabled", False):
                    _admit = self._attention_gate_admit(score, str(e.get("id") or ""))
                if _admit:
                    scored.append((score, e))
        _sid, _sname = self._speaker(event)
        _here = self._here(event)
        _source = memory_meta.source_for_input(text=text, extra=extra, voice=voice)
        # Mem0 UPDATE path: an explicit correction is an update request even
        # when embedding similarity is below the exact-duplicate threshold.
        # Only the conservative correction detector can nominate this target.
        _update_target = None
        _explicit_update = False
        # ams-life: "其实是… / 不是这样" no longer picks an older memory to overwrite;
        # what was said is kept as said, and the older memory stays as it was.
        if False:
            try:
                _scored_ids = {id(_entry) for _score, _entry in scored}
                _best = None
                for _pair in retrieval_pairs:
                    _cand, _cos = _pair
                    if id(_cand) not in _scored_ids:
                        continue
                    if _cos < MEMORY_UPDATE_MATCH_THRESHOLD:
                        continue
                    if not memory_meta.detect_conflict(_cand.get("text", ""), text):
                        continue
                    if _best is None or _cos > _best[1]:
                        _best = (_cand, _cos)
                if _best is not None:
                    _update_target = _best[0]
            except Exception:
                _update_target = None
        if duplicate is None and _update_target is not None:
            duplicate = _update_target
            _explicit_update = True
        _this_turn_id = ""   # ams-life: the memory this turn's message just became, if new
        if duplicate is not None:
            _entry_age = max(0.0, (now - float(duplicate.get("ts", now) or now)) / 86400.0)
            duplicate["ts"] = now
            duplicate["last_used"] = now
            duplicate["hits"] = int(duplicate.get("hits", 0)) + 1
            if _sid:
                duplicate["sender_id"] = _sid
            if _sname:
                duplicate["sender_name"] = _sname
            if extra:
                duplicate["image_caption"] = str(extra).strip()[:1600]
            if voice:
                duplicate["voice_text"] = str(voice).strip()[:1200]
            duplicate["memory_source"] = memory_meta.merge_sources(duplicate.get("memory_source"), _source)
            duplicate["memory_confidence"] = memory_meta.update_confidence(
                duplicate.get("memory_confidence"),
                duplicate["memory_source"],
                hits=int(duplicate.get("hits", 0) or 0),
                review_count=int(duplicate.get("review_count", 0) or 0),
                age_days=_entry_age,
            )
            if not isinstance(duplicate.get("destination"), dict):
                duplicate["destination"] = memory_meta.build_destination(_sid, _sname)
            _conflict = (memory_meta.detect_conflict(duplicate.get("text", ""), text)
                         or _explicit_update)
            if _conflict:
                # ams-life: the stored text is not rewritten by what someone says now
                duplicate["conflict"] = True
                duplicate["conflict_resolved"] = bool(_explicit_update)
                try:
                    # G1/L12: key the sample by memory provenance so the
                    # bounded confidence consumer can match entries later.
                    self._record_calibration(
                        event,
                        memory_meta.normalize_source(duplicate.get("memory_source")),
                        duplicate.get("memory_confidence", 0.5),
                        0.0,
                    )
                except Exception:
                    pass
                if _explicit_update:
                    # The user explicitly corrected the fact: trust the newer
                    # direct statement, but keep the old version for rollback.
                    try:
                        _base_conf = float(duplicate.get("memory_confidence", 0.5) or 0.5)
                    except Exception:
                        _base_conf = 0.5
                    duplicate["memory_confidence"] = round(max(_base_conf, 0.78), 4)
                else:
                    try:
                        duplicate["memory_confidence"] = min(float(duplicate.get("memory_confidence", 0.5) or 0.5), 0.55)
                    except Exception:
                        duplicate["memory_confidence"] = 0.55
            if not duplicate.get("id"):
                duplicate["id"] = self._new_memory_id(
                    _here, duplicate.get("ts"), duplicate.get("text"),
                    taken=[str(x.get("id") or "") for x in entries if isinstance(x, dict)])
            duplicate["memory_tier"] = memory_meta.memory_tier(duplicate, now)
            _write_op = memory_meta.classify_write_op(
                duplicate, {"text": text[:1200]}, 1.0, conflict=_conflict or bool(duplicate.get("conflict"))
            )
            duplicate["last_write_op"] = _write_op
            _ops = duplicate.get("write_ops") if isinstance(duplicate.get("write_ops"), dict) else {}
            _ops[_write_op] = int(_ops.get(_write_op, 0) or 0) + 1
            duplicate["write_ops"] = _ops
            duplicate["provenance"] = self._memory_provenance(event, now)
            _old_origin = discretion.origin_of(duplicate, _here)
            duplicate["origin"] = discretion.merge([
                _old_origin,
                discretion.make_origin(_here, [_sid], duplicate["provenance"].get("message_refs") or [],
                                       self._event_origin(event)["visibility"]),
            ])
            duplicate["last_write_ts"] = now
            self._apply_memory_encoding(duplicate, core, now, text)
            if _write_op != "NOOP":
                memory_meta.append_write_log(doc, op=_write_op, entry_id=duplicate.get("id", ""),
                                             reason="conflict" if _conflict else "duplicate", ts=now)
        else:
            _importance = self._memory_importance(core, "user")
            _new_entry = {"id": self._new_memory_id(
                              _here, now, text, taken=[str(x.get("id") or "") for x in entries if isinstance(x, dict)]),
                          "text": text[:1200],
                          "role": "user", "vector": vec, "ts": now, "hits": 1,
                          "sender_id": _sid, "sender_name": _sname,
                          "attachments": self._attachments_from_messages(event),
                          "image_caption": str(extra or "").strip()[:1600],
                          "voice_text": str(voice or "").strip()[:1200],
                          "provenance": self._memory_provenance(event, now),
                          "origin": self._event_origin(event),
                          "importance": _importance,
                          "memory_source": _source,
                          "memory_confidence": memory_meta.initial_confidence(_source, _importance),
                          "destination": memory_meta.build_destination(_sid, _sname),
                          "conflict": False,
                          "last_write_op": "ADD",
                          "last_write_ts": now,
                          "write_ops": {"ADD": 1},
                          "memory_tier": "hot",
                          "schema_congruence": 0.0,
                          "self_defining": False,
                          "inhibition": 0.0,
                          "suppression_count": 0,
                          "last_used": now, "next_review_ts": now + 86400, "review_count": 0}
            self._apply_memory_encoding(_new_entry, core, now, text)
            entries.append(_new_entry)
            _this_turn_id = str(_new_entry["id"])
            memory_meta.append_write_log(doc, op="ADD", entry_id=_new_entry["id"],
                                         reason="new", ts=now)
            self._trim_memory(doc, core)
        # Task-15: memory write fill feeds L1 energy/social noise.
        if core is not None:
            try:
                core.integrate_noise("memory_write", energy=0.003, social=0.002)
            except Exception:
                pass
        self._save_memory(event, doc)
        try:
            _recent_ids = [str(_e.get("id") or "") for _e in entries[-3:]
                           if isinstance(_e, dict)]
            doc["working_set"] = memory_meta.update_working_set(
                doc.get("working_set") if isinstance(doc.get("working_set"), list) else [],
                _recent_ids, capacity=self._working_set_capacity(core),
                priorities={str(_e.get("id") or ""): float(_e.get("importance", 0.5) or 0.5)
                            for _e in entries
                            if isinstance(_e, dict) and str(_e.get("id") or "")})
            self._save_memory(event, doc)
        except Exception:
            pass
        self._schedule_consolidation(event, core)
        scored = [(score, entry) for score, entry in scored
                  if recall_permission(self, entry, event) != discretion.DROP]
        scored.sort(key=lambda x: x[0], reverse=True)
        top = memory_meta.select_top(
            scored, self._memory_top_k(core, _partner_trust),
            lambda_=(0.72 if getattr(self, "hybrid_retrieval", True) else 1.0))
        try:
            turn["memory_trace"] = self._apply_memory_trace(core, [e for _s, e in top])
        except Exception as exc:
            logger.warning("[biocore] memory trace apply failed: %s", exc)
        # L-T02 / C-T01: auditable retrieval-contribution trace (deterministic,
        # bounded to 8 rows, no text beyond the entry id). This is a trace of
        # ranking factors, not a claim of psychological causation, and it is
        # never produced by the LLM.
        try:
            _cos_by_id = {id(_e): _cos for _e, _cos in retrieval_pairs}
            _trace = []
            for _rank, (_score, _entry) in enumerate(top[:8], start=1):
                _eid = str(_entry.get("id") or "").strip()[:20]
                if not _eid:
                    continue
                _parts = self._memory_score_parts(
                    core, _entry, _cos_by_id.get(id(_entry), 0.0),
                    query_text=text,
                    hybrid=bool(getattr(self, "hybrid_retrieval", True)),
                    sensitive_protect=bool(getattr(self, "sensitive_memory_protection", False)))
                _trace.append({
                    "entry_id": _eid,
                    "rank": _rank,
                    "score": round(float(_score), 4),
                    "cosine": _parts["cosine"],
                    "importance": _parts["importance"],
                    "source": str(_entry.get("memory_source") or "direct")[:12],
                    "tier": str(_entry.get("memory_tier") or "warm")[:8],
                    "conflict": bool(_entry.get("conflict")),
                    "components": self._memory_trace_components(_parts),
                })
            self._last_cause_trace = turn["cause_trace"] = _trace
            self._last_memory_entries = turn["memory_entries"] = [
                str(e.get("id") or "") for _s, e in top if str(e.get("id") or "")][:8]
            doc["last_recall_trace"] = _trace
            self._save_memory(event, doc)
        except Exception as _trace_exc:
            logger.warning("[biocore] recall trace failed: %s", _trace_exc)
        # Nader reconsolidation + Ebbinghaus review: recalling an item makes
        # it labile, strengthens it slightly, and schedules the next review.
        _intervals = [1, 2, 4, 7, 15, 30, 60]
        _ids = []
        for _score, e in top:
            if id(e) in _just_restabilized:
                # The expired labile window was just closed in this pass; do
                # not re-open it on the same recall.
                continue
            try:
                e["recall_count"] = int(e.get("recall_count", 0) or 0) + 1
                e["last_recall"] = now
                e["reconsolidated_ts"] = now
                e["destabilized_until"] = now + float(getattr(self, "reconsolidation_seconds", 600.0))
                e["reconsolidation_state"] = "destabilized"
                _imp = float(e.get("importance", 0.5) or 0.5)
                e["importance"] = max(0.0, min(1.0, _imp + 0.015))
                _rc = int(e.get("review_count", 0) or 0) + 1
                e["review_count"] = _rc
                _st = max(1.0, min(365.0, float(e.get("stability_days", 1.0) or 1.0) * 1.8))
                e["stability_days"] = round(_st, 3)
                _days = max(_intervals[min(_rc - 1, len(_intervals) - 1)], _st)
                e["next_review_ts"] = now + _days * 86400
                # Keep the persisted id stable: dashboard delete/rollback and
                # write_log reference it; only assign one for legacy entries.
                _eid = str(e.get("id") or "").strip()
                if not _eid:
                    _eid = self._new_memory_id(
                        self._here(event), e.get("ts"), e.get("text"),
                        taken=[str(x.get("id") or "") for x in entries if isinstance(x, dict)])
                    e["id"] = _eid
                e["last_recall_regulation"] = str(getattr(core, "regulation", "none") or "none")
                _ids.append(e)
            except Exception:
                pass
        # ACT-R-style spreading activation: co-recalled items become associated.
        for _i in range(len(_ids)):
            for _j in range(_i + 1, len(_ids)):
                try:
                    _a = _ids[_i].setdefault("assoc", {})
                    _b = _ids[_j].setdefault("assoc", {})
                    _aid = _ids[_i].get("id") or str(_i)
                    _bid = _ids[_j].get("id") or str(_j)
                    _a[_bid] = int(_a.get(_bid, 0)) + 1
                    _b[_aid] = int(_b.get(_aid, 0)) + 1
                except Exception:
                    pass
        # Memory graph links (A-MEM-like): co-recalled memories get weighted
        # directed links; the working set keeps a bounded read set per session.
        _link_lines = []
        _link_pairs = []   # ams-life: (recalled, its linked memory) for the brain map
        _consistency = memory_meta.answer_consistency(top)
        try:
            for _i in range(len(_ids)):
                for _j in range(_i + 1, len(_ids)):
                    _aid = str(_ids[_i].get("id") or "").strip()
                    _bid = str(_ids[_j].get("id") or "").strip()
                    if _aid and _bid:
                        memory_meta.add_link(_ids[_i], _bid, now=now)
                        memory_meta.add_link(_ids[_j], _aid, now=now)
            _ws_current = doc.get("working_set") if isinstance(doc.get("working_set"), list) else _working_set
            doc["working_set"] = memory_meta.update_working_set(
                _ws_current, [str(e.get("id") or "") for _score, e in top],
                capacity=self._working_set_capacity(core),
                priorities={str(_e.get("id") or ""): float(_e.get("importance", 0.5) or 0.5)
                            for _e in entries
                            if isinstance(_e, dict) and str(_e.get("id") or "")})
            _top_ids = {id(e) for _score, e in top}
            _by_id = {str(e.get("id") or ""): e for e in entries
                      if isinstance(e, dict) and str(e.get("id") or "")}
            for _score, e in top:
                _chain_budget = bool(getattr(self, "chain_budget_enabled", False))
                for _lid in memory_meta.linked_ids(
                        e, limit=2, now=now,
                        min_weight=(0.5 if _chain_budget else 1.0)):
                    _nb = _by_id.get(_lid)
                    if _nb is None or id(_nb) in _top_ids:
                        continue
                    if _nb.get("deleted") or _nb.get("summarized"):
                        continue
                    _permission = recall_permission(self, _nb, event)
                    if _permission == discretion.DROP:
                        continue
                    if getattr(self, "safety_enabled", False) and _nb.get("poison_risk"):
                        continue
                    _nb_text = str(_nb.get("text") or "").strip().replace("\n", " ")
                    if _permission == discretion.ANON:
                        _nb_text = recall_anonymize(self, _nb_text, _nb)
                    if not _nb_text:
                        continue
                    if getattr(self, "safety_enabled", False) and _nb.get("sensitive"):
                        _nb_text = memory_meta.mask_sensitive(_nb_text)
                    _link_lines.append("- 关联记忆：%s" % _nb_text[:200])
                    _link_pairs.append((str(e.get("id") or ""), str(_lid)))
            try:
                _chain_lines = self._chain_event_lines(self._here(event), text, limit=2)
                if _chain_lines:
                    _link_lines.extend(_chain_lines)
            except Exception:
                pass
            self._save_memory(event, doc)
        except Exception:
            _link_lines = []
            _link_pairs = []
            _consistency = 1.0
        # Retrieval-induced forgetting: similar memories that lost this
        # competition become temporarily inhibited (they are not deleted and
        # the inhibition decays over days).
        try:
            memory_meta.apply_retrieval_inhibition(
                retrieval_pairs, [str(e.get("id") or "") for _score, e in top], now)
        except Exception:
            pass
        try:
            self._save_memory(event, doc)
        except Exception:
            pass
        # ams-life: recall from every other group and private chat in the one
        # library, but only what the discretion table allows here. Things said
        # openly elsewhere come back without naming who said them; things told
        # in private never leave that private chat. Nothing is copied into this place.
        _foreign_lines = []
        _foreign_ids, _held = [], []   # ams-life: for the brain map (ids only)
        _global = bool(getattr(self, "global_memory", False))
        try:
            # what this place already knew -- not the message of this turn, just kept above:
            # the same words said elsewhere (his own, in a group) must still come back here
            _known_texts = {str(e.get("text") or "") for e in entries
                            if isinstance(e, dict) and not e.get("deleted")
                            and not (_this_turn_id and str(e.get("id") or "") == _this_turn_id)}
            _foreign = []
            for _where, _entry in ([] if _global else self._cross_session_memory_entries(event)):
                _etext = str(_entry.get("text") or "").strip()
                if not _etext or _etext in _known_texts:
                    continue
                if getattr(self, "safety_enabled", False) and (
                        _entry.get("sensitive") or _entry.get("poison_risk")):
                    continue
                _verdict = recall_permission(self, _entry, event)
                _evec = _entry.get("vector") or []
                _ecos = self._cosine(vec, _evec) if _evec else 0.0
                if _ecos < PARTIAL_MATCH_THRESHOLD:
                    continue
                _escore = self._memory_score(core, _entry, _ecos)
                if _escore < RETRIEVAL_THRESHOLD:
                    continue
                if _verdict == discretion.DROP:
                    # it would have come up, but it was told in private elsewhere: held back
                    # here (only its id is noted, for the brain map)
                    _held.append((_escore, str(_entry.get("id") or "")))
                    continue
                _foreign.append((_escore, _verdict, _entry))
            _foreign.sort(key=lambda item: item[0], reverse=True)
            _numbers = None   # the numbers she knows, looked up once for these lines
            for _escore, _verdict, _entry in _foreign[:2]:
                # said elsewhere: never "对方" (that would tell who), and without names when anon
                _who = self._recall_who(_entry, "", anon=_verdict == discretion.ANON)
                _line = "%s：%s" % (_who, str(_entry.get("text") or "").strip().replace("\n", " ")[:200])
                if _verdict == discretion.ANON:
                    _numbers = self._known_numbers() if _numbers is None else _numbers
                    _line = recall_anonymize(self, _line, _entry)
                _foreign_lines.append("- （别处）" + _line)
                _known_texts.add(str(_entry.get("text") or "").strip())
                _foreign_ids.append(str(_entry.get("id") or ""))
        except Exception:
            _foreign_lines = []
            _foreign_ids, _held = [], []
        if _global:
            # step 2: everything from elsewhere, each with what she may say of it here
            _foreign_lines, _foreign_ids, _held = self._labeled_elsewhere(
                event, vec, core, entries, _this_turn_id)
        # G1/L12: bounded calibration -> confidence consumer. The recalled
        # top entries get a <=0.05 per-source adjustment (relationship.
        # calibration EWMA matched on memory_source) on a transient copy; the
        # stored entries and ranking are untouched, so hit@k cannot regress.
        _calibration_meta = {}
        _meta_top = top
        try:
            _calibration = self._relationship_of(user_data).get("calibration")
            if isinstance(_calibration, dict) and _calibration.get("sources") and top:
                _adjusted_top = []
                _deltas = []
                for _score, _entry in top:
                    _delta = memory_meta.calibration_confidence_delta(
                        _calibration, _entry.get("memory_source"))
                    if _delta:
                        _copy = dict(_entry)
                        try:
                            _base_conf = float(_copy.get("memory_confidence", 0.5) or 0.5)
                        except Exception:
                            _base_conf = 0.5
                        _copy["memory_confidence"] = round(
                            max(0.0, min(1.0, _base_conf + _delta)), 4)
                        _adjusted_top.append((_score, _copy))
                        _deltas.append(_delta)
                    else:
                        _adjusted_top.append((_score, _entry))
                if _deltas:
                    _meta_top = _adjusted_top
                    _calibration_meta = {
                        "calibration_delta": round(sum(_deltas) / len(_deltas), 4),
                        "calibration_entries": len(_deltas),
                    }
        except Exception:
            _meta_top = top
            _calibration_meta = {}
        _meta = self._last_memory_meta = turn["memory_meta"] = memory_meta.summarize_recall(
            _meta_top, now, consistency=_consistency)
        if _calibration_meta:
            _meta.update(_calibration_meta)
        # Task-15: recall hit/confidence feeds L1 noise (no-op when off).
        if core is not None:
            try:
                _cnt = int(_meta.get("count", 0) or 0)
                _conf = float(_meta.get("confidence", 0.0) or 0.0)
                core.integrate_noise(
                    "memory_recall",
                    attention=0.006 * min(1.0, _cnt / 3.0),
                    valence=0.004 * (_conf - 0.5))
            except Exception:
                pass
        _gate = str(_meta.get("gate") or "none")
        lines = []
        _speaker_id = str(self._speaker(event)[0] or "")
        for score, e in top:
            _permission = recall_permission(self, e, event)
            role = self._recall_who(e, _speaker_id, anon=_permission == discretion.ANON)
            snippet = str(e.get("text", "")).strip().replace("\n", " ")
            if _permission == discretion.ANON:
                snippet = recall_anonymize(self, snippet, e)
            if getattr(self, "sentence_dedup_enabled", False):
                snippet = self._dedupe_sentences(snippet)
            if getattr(self, "safety_enabled", False) and snippet and e.get("sensitive"):
                snippet = memory_meta.mask_sensitive(snippet)
            if snippet and _global:
                # step 2: said here, labelled like everything else (who by number, not name)
                lab = discretion.label(discretion.origin_of(e), _here, _speaker_id,
                                       said_by=self._said_by(e))
                if _permission == discretion.ANON:
                    lab.update(may=discretion.ANON, where_ok=False, yours=False)
                elif _permission == discretion.SAY and lab["may"] in (discretion.HIDE, discretion.NO, discretion.ANON):
                    lab.update(may=discretion.SAY, where_ok=True)
                lines.append("- %s%s" % (discretion.tag(lab, "memory", self._recall_role(e),
                                                        self._sayer_name(e)), snippet[:240]))
            elif snippet:
                lines.append("- %s：%s" % (role, snippet[:240]))
        lines.extend(_link_lines)
        lines.extend(_foreign_lines)
        memory_text = "\n".join(lines)
        if getattr(self, "safety_enabled", False) and _gate == "force":
            _meta["withheld"] = True
            _meta["abstain"] = True
            return ""
        # ams-life: what this turn recalled, in order (the best match first, then what it
        # called up along its links, then what came from elsewhere), the lines it went along,
        # and what the discretion table held back here. Ids only (BrainMixin._note_turn).
        _top_ids = [str(e.get("id") or "") for _s, e in top if str(e.get("id") or "")]
        # (step 2: what was shown but may not be said here is "held", not "recalled", on the map)
        _held_ids = {i for _s, i in _held}
        turn["recall_order"] = list(dict.fromkeys(
            _top_ids + [b for _a, b in _link_pairs if b] + [x for x in _foreign_ids if x and x not in _held_ids]))
        turn["recall_path"] = [[a, b] for a, b in zip(_top_ids, _top_ids[1:])] + [
            [a, b] for a, b in _link_pairs if a and b]
        turn["recall_held"] = [i for _s, i in sorted(_held, key=lambda x: -x[0]) if i][:8]
        return memory_text

    @staticmethod
    def _recall_role(entry) -> str:
        return "assistant" if str(entry.get("role") or "user") in ("assistant", "summary") else "user"

    def _said_by(self, entry) -> str:
        """Whose words a memory is, by number: the sender's; "" for hers or a summary."""
        if self._recall_role(entry) != "user":
            return ""
        return str(entry.get("sender_id") or "")

    def _sayer_name(self, entry) -> str:
        name = str(entry.get("sender_name") or "").strip()
        if name and not name.isdigit():
            return name
        return self._display_name(entry.get("sender_id"))

    def _labeled_elsewhere(self, event, vec, core, entries, this_turn_id="") -> tuple:
        """Step 2 (global_memory): what comes up from every other place, each line with what
        she may say of it here (discretion.label / tag). The one talking to her is told by
        his number. At most ELSEWHERE_MAX lines, of which at most ELSEWHERE_PRIVATE_MAX may
        not be said here; his own come first. Returns (lines, ids shown, (score, id) of the
        ones shown that may not be said here -- the brain map's "knew, did not say")."""
        here = self._here(event)
        speaker = str(self._speaker(event)[0] or "")
        present = self._present_people(event)
        known = {str(e.get("text") or "").strip() for e in entries
                 if isinstance(e, dict) and not e.get("deleted")
                 and not (this_turn_id and str(e.get("id") or "") == this_turn_id)}
        found = []
        try:
            for _where, entry in self._cross_session_memory_entries(event):
                text = str(entry.get("text") or "").strip()
                if not text or text in known:
                    continue
                if getattr(self, "safety_enabled", False) and (entry.get("sensitive") or entry.get("poison_risk")):
                    continue
                permission = recall_permission(self, entry, event)
                lab = discretion.label(discretion.origin_of(entry), here, speaker, present,
                                       said_by=self._said_by(entry),
                                       asked_in=entry.get("asked_in") if isinstance(entry.get("asked_in"), dict)
                                       else None)
                was_own = lab["may"] == discretion.OWN
                if permission == discretion.DROP and lab["may"] != discretion.NO:
                    continue
                if permission == discretion.ANON:
                    lab.update(may=discretion.ANON, where_ok=False, yours=False)
                elif permission == discretion.SAY and lab["may"] in (discretion.HIDE, discretion.NO, discretion.ANON):
                    lab.update(may=discretion.SAY, where_ok=True)
                evec = entry.get("vector") or []
                cos = self._cosine(vec, evec) if evec else 0.0
                if cos < PARTIAL_MATCH_THRESHOLD:
                    continue
                score = self._memory_score(core, entry, cos)
                if score < RETRIEVAL_THRESHOLD:
                    continue
                found.append((was_own, score, lab, entry, permission))
        except Exception as exc:
            logger.warning("[ams-life] recall from elsewhere failed: %s", exc)
            return [], [], []
        found.sort(key=lambda x: (x[0], x[1]), reverse=True)
        old_count, old_no = 0, 0
        for _own, _score, lab, entry, permission in found:
            if old_count >= ELSEWHERE_MAX:
                break
            if lab["may"] == discretion.NO:
                if old_no >= ELSEWHERE_PRIVATE_MAX:
                    continue
                old_no += 1
                if permission == discretion.DROP:
                    origin = discretion.origin_of(entry)
                    group_private = origin["where"].startswith("group:") and origin["visibility"] == discretion.PRIVATE
                    people = list(origin["people"]) + [str(entry.get("sender_id") or "")]
                    self._forbid(event, "memory:" + str(entry.get("id") or ""),
                                 str(entry.get("text") or "").strip(),
                                 [] if group_private else people, entry.get("vector"))
            old_count += 1
        lines, ids, held, n_no = [], [], [], 0
        for _own, score, lab, entry, permission in found:
            if permission == discretion.DROP:
                continue
            if len(lines) >= ELSEWHERE_MAX:
                break
            text = str(entry.get("text") or "").strip()
            if lab["may"] == discretion.ANON:
                text = recall_anonymize(self, text, entry)
            if text in known:
                continue
            origin = discretion.origin_of(entry)
            people = list(origin["people"]) + [str(entry.get("sender_id") or "")]
            if lab["may"] == discretion.NO:
                if n_no >= ELSEWHERE_PRIVATE_MAX:
                    continue
                n_no += 1
                held.append((score, str(entry.get("id") or "")))
                # the last look before sending (send_check): its words and who it is about
                group_private = origin["where"].startswith("group:") and origin["visibility"] == discretion.PRIVATE
                self._forbid(event, "memory:" + str(entry.get("id") or ""), text,
                             [] if group_private else people, entry.get("vector"))
            elif lab["may"] == discretion.ANON:
                self._forbid_names(event, "memory:" + str(entry.get("id") or ""), people)
            if lab.get("asked") == discretion.NO and isinstance(entry.get("asked_in"), dict):
                self._forbid_names(event, "asked:" + str(entry.get("id") or ""), entry["asked_in"].get("people") or [])
            tag = discretion.tag(lab, "memory", self._recall_role(entry), self._sayer_name(entry),
                                 self._partner_name(discretion.origin_of(entry)))
            lines.append("- %s%s" % (tag, text.replace("\n", " ")[:200]))
            known.add(text)
            ids.append(str(entry.get("id") or ""))
        return lines, ids, held

    @staticmethod
    def _recall_who(entry, speaker_id="", anon=False) -> str:
        """ams-life: who a recalled memory came from, as the reply model sees it (the owner,
        step 1-2). Never a QQ number. What was said here (the same group, or his own private
        chat) keeps the nickname; what was said openly elsewhere is anonymous (有人)."""
        role = str(entry.get("role") or "user")
        if role == "summary":
            return "她总结过"
        if role == "assistant":
            return "她自己说过"
        if anon:
            return "有人说过"
        name = str(entry.get("sender_name") or "").strip()
        if name and not name.isdigit():
            return name + "说过"
        sid = str(entry.get("sender_id") or "")
        return "对方说过" if speaker_id and sid == str(speaker_id) else "有人说过"

    async def _remember(self, event, text: str, role: str = "user", core=None):
        if not self.memory_dedup_embedding or not self._usable_memory_text(text):
            return
        text = str(text).strip()
        if len(text) < 4:
            return
        vec = await self._embed_text(text)
        if not vec:
            return
        doc = self._load_memory(event)
        entries = doc.get("entries")
        if not isinstance(entries, list):
            entries = []
            doc["entries"] = entries
        now = time.time()
        for e in entries:
            if e.get("summarized") or e.get("deleted"):
                continue
            self._restabilize_if_expired(e, now)
            _cos = self._cosine(vec, e.get("vector") or [])
            # Nader reconsolidation: a recalled memory is labile for a window;
            # new related information can update it before restabilization.
            try:
                _window = float(e.get("destabilized_until", 0) or 0)
            except Exception:
                _window = 0.0
            if _window > now and _cos >= 0.80:
                _origin = self._event_origin(event)
                if _origin["where"].startswith("group:") and _origin["visibility"] == discretion.PRIVATE:
                    e["origin"] = discretion.merge([discretion.origin_of(e, self._here(event)), _origin])
                _old_text = str(e.get("text", ""))
                e["text"] = (_old_text + "\n[再巩固] " + text)[:1200]
                try:
                    _ov = [float(x) for x in (e.get("vector") or [])]
                    e["vector"] = [0.8 * a + 0.2 * b for a, b in zip(_ov, vec)]
                except Exception:
                    pass
                e["reconsolidated_ts"] = now
                e["reconsolidation_count"] = int(e.get("reconsolidation_count", 0) or 0) + 1
                e["reconsolidation_state"] = "rewritten"
                e["destabilized_until"] = 0
                self._save_memory(event, doc)
                return
            if _cos >= 0.93:
                _origin = self._event_origin(event)
                if _origin["where"].startswith("group:") and _origin["visibility"] == discretion.PRIVATE:
                    e["origin"] = discretion.merge([discretion.origin_of(e, self._here(event)), _origin])
                e["ts"] = now
                e["last_used"] = now
                e["hits"] = int(e.get("hits", 0)) + 1
                self._save_memory(event, doc)
                return
        _sid, _sname = self._speaker(event)
        if role == "assistant":
            _prov = {"sender_id": "self", "sender_name": "她",
                     "session": self._here(event),
                     "ts": now, "message_refs": []}
        else:
            _prov = self._memory_provenance(event, now)
        entries.append({"id": self._new_memory_id(
                            self._here(event), now, role, text,
                            taken=[str(x.get("id") or "") for x in entries if isinstance(x, dict)]),
                        "text": text[:1200], "role": role, "vector": vec,
                        "ts": now, "hits": 1,
                        "sender_id": _sid if role == "user" else "",
                        "sender_name": _sname if role == "user" else "",
                        "attachments": self._attachments_from_messages(event) if role == "user" else [],
                        "provenance": _prov,
                        # her reply belongs to the place, to the person she answered and to
                        # the message she answered: deleting that message deletes her reply too
                        "origin": self._event_origin(event),
                        "importance": self._memory_importance(core, role),
                        "last_used": now, "next_review_ts": now + 86400, "review_count": 0})
        self._apply_memory_encoding(entries[-1], core, now, text)
        memory_meta.append_write_log(doc, op="ADD", entry_id=str(entries[-1].get("id") or ""),
                                     reason=role, ts=now)
        self._trim_memory(doc, core)
        self._save_memory(event, doc)
        self._schedule_consolidation(event, core)

    # ------------------------------------------------------------------
    # A4 continuity opener ("上次聊到").
    #
    # Deterministic only: no LLM call, no new line, no reply generation. The
    # three data sources are already persisted bio data:
    #   1) the latest consolidated memory summary / last archived session event;
    #   2) unfinished open loops captured *before* the current turn;
    #   3) relationship state (closeness/conflict/repair/phase/absence).
    # It is injected only when the user returns after A4_CONTINUITY_GAP_SECONDS
    # and at least one of the three sources is non-empty.
    # ------------------------------------------------------------------
    def _record_continuity_feedback(self, event, continuity) -> None:
        """Persist A4 continuity usage/feedback into the memory doc (bounded)."""
        if not isinstance(continuity, dict) or not continuity:
            return
        try:
            doc = self._load_memory(event)
            loops = continuity.get("open_loops") if isinstance(continuity.get("open_loops"), list) else []
            doc["last_continuity"] = {
                "ts": round(time.time(), 3),
                "summary": str(continuity.get("summary") or "")[:80],
                "open_loops": [str(x.get("text") or "")[:60] for x in loops[:3] if isinstance(x, dict)],
                "relationship_used": bool(continuity.get("relationship")),
            }
            doc["continuity_feedback_count"] = int(doc.get("continuity_feedback_count", 0) or 0) + 1
            self._save_memory(event, doc)
            try:
                for loop in (getattr(self, "_continuity_last_loops", None) or [])[:3]:
                    if isinstance(loop, dict):
                        loop["last_mentioned_ts"] = time.time()
            except Exception:
                pass
        except Exception as exc:
            logger.warning("[biocore] continuity feedback write failed: %s", exc)

    def _continuity_summary(self, event, core):
        """Return a bounded last-session summary text, or "" when none exists."""
        try:
            doc = self._load_memory(event)
            entries = doc.get("entries") if isinstance(doc, dict) else []
            summaries = [e for e in (entries or [])
                         if isinstance(e, dict)
                         and str(e.get("role") or "") == "summary"
                         and str(e.get("text") or "").strip()]
            if summaries:
                summaries.sort(key=lambda e: float(e.get("ts", 0) or 0), reverse=True)
                text = str(summaries[0].get("text") or "")
                text = text.split("\n[再巩固]")[0]
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    return text[:80]
        except Exception:
            pass
        try:
            last = self._last_session_event(self._here(event))
            if isinstance(last, dict):
                title = str(last.get("title") or "").strip()
                detail = str(last.get("meaning_to_her")
                             or last.get("reflection")
                             or last.get("event") or "").strip()
                text = (title + ("：" + detail if detail else "")).strip()
                text = re.sub(r"\s+", " ", text)
                if text:
                    return text[:80]
        except Exception:
            pass
        return ""

    def _continuity_context(self, event, core, user_data, prior_loops=None):
        """Build raw A4 continuity data; returns {} when there is no history."""
        data = user_data if isinstance(user_data, dict) else {}
        absence = data.get("absence") if isinstance(data.get("absence"), dict) else {}
        try:
            gap_days = float(absence.get("gap_days", 0.0) or 0.0)
        except Exception:
            gap_days = 0.0
        if gap_days * 86400.0 < A4_CONTINUITY_GAP_SECONDS:
            return {}
        summary = self._continuity_summary(event, core)
        loops = []
        try:
            source = prior_loops if isinstance(prior_loops, list) else self._window_loops(event)
            open_loops = []
            for item in (source or []):
                if not isinstance(item, dict):
                    continue
                if str(item.get("status") or "open") != "open":
                    continue
                text = str(item.get("text") or "").strip()
                if not text:
                    continue
                due = str(item.get("due_hint") or "")
                try:
                    seen = float(item.get("last_mentioned_ts")
                                 or item.get("created_ts") or 0.0)
                except Exception:
                    seen = 0.0
                open_loops.append((0 if due in ("soon", "tomorrow") else 1,
                                   -seen, text[:60], due))
            open_loops.sort(key=lambda row: (row[0], row[1]))
            for _rank, _neg_ts, text, due in open_loops[:A4_CONTINUITY_MAX_LOOPS]:
                loops.append({"text": text, "due_hint": due})
        except Exception:
            loops = []
        relationship = data.get("relationship") if isinstance(data.get("relationship"), dict) else {}
        state = relationship.get("state") if isinstance(relationship.get("state"), dict) else {}
        rel = {}
        if state:
            for key in ("closeness", "conflict", "repair"):
                try:
                    rel[key] = round(max(0.0, min(1.0, float(state.get(key, 0.0) or 0.0))), 3)
                except Exception:
                    pass
            repair_state = relationship.get("repair_state")
            if isinstance(repair_state, dict):
                phase = str(repair_state.get("phase") or "stable")
                if phase and phase != "stable":
                    rel["phase"] = phase
            bucket = str(absence.get("bucket") or "")
            if bucket and bucket != "same_day":
                rel["absence"] = bucket
        if not summary and not loops and not rel:
            return {}
        return {"summary": summary, "loops": loops, "relationship": rel}
