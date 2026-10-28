# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: event archive: summaries, worthiness, duplicates, insights, event pages."""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403


def _merged_origin(item, other) -> dict:
    """ams-life: the origin of `item` once `other` has been merged into it: every person and
    every source id of both, the stricter visibility; it stays where `item` was."""
    mine = discretion.origin_of(item)
    both = discretion.merge([mine, other])
    return discretion.make_origin(mine["where"] or both["where"], both["people"],
                                  both["source_ids"], both["visibility"])


class EventsMixin:
    def _summary_cap(self, text) -> str:
        value = str(text or "")
        try:
            cap = int(getattr(self, "summary_max_chars", 0) or 0)
        except Exception:
            cap = 0
        return value[:cap] if cap > 0 else value

    def _event_excerpt(self, text, limit: int = 220) -> str:
        """Compact deterministic-event display text; raw evidence stays in source_texts."""
        value = re.sub(r"\s+", " ", str(text or "").replace("\n", " ")).strip()
        if len(value) <= limit:
            return value
        cut = value[:limit]
        pos = max(cut.rfind("。"), cut.rfind("！"), cut.rfind("？"), cut.rfind("；"))
        if pos >= int(limit * 0.5):
            return cut[:pos + 1].strip()
        return cut.rstrip() + "…"

    @staticmethod
    def _first_sentence(text) -> str:
        """First sentence of a raw event excerpt (used for <=80 summaries)."""
        value = re.sub(r"\s+", " ", str(text or "")).strip()
        if not value:
            return ""
        match = re.search(r"[。！？；!?;]", value)
        return value[:match.end()] if match else value

    def _dual_event_summary_fallback(self, text, title: str = ""):
        """Deterministic bounded big/small summary fallback for event records.

        No LLM is used here: big_summary is a bounded excerpt (<=220 chars) and
        small_summary is the first sentence (or the title) bounded to 80 chars.
        These records are marked summary_status="fallback" by the writers.
        """
        big = self._mask_if_safety(self._event_excerpt(text, 220))[:220]
        small = self._mask_if_safety(
            self._first_sentence(text) or str(title or "").strip())[:80]
        if not big:
            big = small
        if not small:
            small = big[:80]
        return big, small

    def _secondary_emotion(self, core) -> str:
        """Second-highest spectrum emotion excluding the current primary label."""
        if core is None:
            return ""
        try:
            primary = str((getattr(core, "labels", {}) or {}).get("emotion") or "neutral")
            probs = core._spectrum_probs() if callable(getattr(core, "_spectrum_probs", None)) else []
            for item in (probs or []):
                if not isinstance(item, dict):
                    continue
                key = str(item.get("key") or "").strip()[:32]
                if key and key != primary:
                    return key
        except Exception:
            pass
        return ""

    def _event_emotion_layers(self, core) -> list:
        """Emotion layers snapshot for the memory-ball rings (task-65).

        Top-4 EMOTION_SPECTRUM probabilities including the primary emotion,
        normalized to sum 1: [{"emotion": key, "p": weight}, ...]. The field
        is stored once with the archive record, so a later regenerate does not
        rewrite the historical layers. No spectrum data -> [] (rings then use
        the old secondary/inferred fallback; nothing is fabricated).
        """
        try:
            if core is None:
                return []
            probs = core._spectrum_probs() if callable(getattr(core, "_spectrum_probs", None)) else []
            rows = []
            for item in (probs or []):
                if not isinstance(item, dict):
                    continue
                key = str(item.get("key") or "").strip().lower()[:32]
                if not key:
                    continue
                try:
                    weight = float(item.get("p", 0) or 0)
                except Exception:
                    weight = 0.0
                if weight <= 0:
                    continue
                rows.append((key, weight))
            primary = str((getattr(core, "labels", {}) or {}).get("emotion") or "").strip().lower()
            if not rows:
                return [{"emotion": primary, "p": 1.0}] if primary else []
            merged = {}
            for key, weight in rows:
                merged[key] = merged.get(key, 0.0) + weight
            ordered = sorted(merged.items(), key=lambda pair: pair[1], reverse=True)[:4]
            picked = [{"emotion": key, "p": weight} for key, weight in ordered]
            if primary and primary not in [x["emotion"] for x in picked]:
                # The primary emotion must be part of the snapshot even when its
                # spectrum probability is missing/zero; give it a minimal weight
                # so normalization keeps it at the tail.
                picked = picked[:3] + [{"emotion": primary,
                                       "p": max(0.01, merged.get(primary, 0.0))}]
            total = sum(x["p"] for x in picked)
            if total <= 0:
                return []
            out = [{"emotion": x["emotion"], "p": round(x["p"] / total, 4)}
                   for x in picked if x["p"] > 0]
            out.sort(key=lambda x: x["p"], reverse=True)
            return out
        except Exception:
            return []

    def _event_emotion_intensity(self, core) -> float:
        """Emotion-intensity snapshot for ring speed (task-66).

        Prefers the core's own intensity(); otherwise arousal + |valence|.
        None / no core -> 0.0; the orb then falls back to importance or
        emotion_layers[0].p instead of fabricating a value.
        """
        try:
            if core is None:
                return 0.0
            fn = getattr(core, "_intensity", None)
            if callable(fn):
                raw = float(fn())
                if math.isfinite(raw):
                    return round(max(0.0, min(1.0, raw)), 4)
            arousal = float(getattr(core, "a", 0.4) or 0.4)
            valence = abs(float(getattr(core, "v", 0.0) or 0.0))
            return round(max(0.0, min(1.0, 0.5 * arousal + 0.5 * valence)), 4)
        except Exception:
            return 0.0

    def _event_secondary_for_record(self, record) -> str:
        """Secondary emotion for an archived event, from its session core.

        Only used to fill a MISSING emotion_secondary on regenerate: the
        highest spectrum probability is excluded (the primary emotion) and the
        next one wins. No core / no spectrum data -> "" (never fabricated).
        """
        try:
            rec = record if isinstance(record, dict) else {}
            session = str(rec.get("session") or "").strip()
            if not session:
                return ""
            core = None
            cores = getattr(self, "cores", None)
            if isinstance(cores, dict):
                core = cores.get(session)
            if core is None:
                try:
                    core = self._core(types.SimpleNamespace(unified_msg_origin=session))
                except Exception:
                    core = None
            if core is None:
                return ""
            primary = str((getattr(core, "labels", {}) or {}).get("emotion") or "neutral")
            probs = core._spectrum_probs() if callable(getattr(core, "_spectrum_probs", None)) else []
            ordered = []
            for item in (probs or []):
                if not isinstance(item, dict):
                    continue
                key = str(item.get("key") or "").strip()[:32]
                if not key:
                    continue
                try:
                    weight = float(item.get("p", 0) or 0)
                except Exception:
                    weight = 0.0
                ordered.append((weight, key))
            ordered.sort(key=lambda pair: pair[0], reverse=True)
            for _weight, key in ordered:
                if key != primary:
                    return key
        except Exception as exc:
            logger.warning("[biocore] event secondary lookup failed: %s", exc)
        return ""

    @staticmethod
    def _normalize_emotion_nuance(value) -> list:
        """Hidden/composite emotion layer from event_summary (task-64).

        Delegates to the interpretation-layer cleaner: max 3 short Chinese
        labels, deduped, empties dropped. Unknown/garbage input returns [] so
        the deterministic fallback never fabricates a nuance layer.
        """
        try:
            return interpretation.clean_emotion_nuance(value, 3)
        except Exception:
            return []

    def _mask_if_safety(self, text) -> str:
        value = str(text or "")
        try:
            if getattr(self, "safety_enabled", False):
                return memory_meta.mask_sensitive(value)
        except Exception:
            pass
        return value

    def _event_archive(self, limit: int = 5, read_only: bool = False) -> list:
        try:
            if not EVENT_ARCHIVE_PATH.exists():
                return []
            lines = EVENT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines()
            out = []
            forgotten = []
            for line in lines[-max(1, limit * 3):]:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if not isinstance(d, dict):
                    continue
                if not d.get("peripheral_forgotten"):
                    try:
                        _age_days = (time.time() - float(d.get("ts", 0) or 0)) / 86400.0
                        _central = float(d.get("centrality", 0.5) or 0.5)
                        if _age_days > (14.0 - 10.0 * _central):
                            d["peripheral_details"] = ""
                            d["peripheral_retention"] = min(float(d.get("peripheral_retention", 1.0) or 1.0), 0.05)
                            d["peripheral_forgotten"] = True
                            forgotten.append(dict(d))
                    except Exception:
                        pass
                # task-46: old records never carried summary_status. Mark them
                # legacy on read only (no rewrite of the stored full text).
                if not str(d.get("summary_status") or "").strip():
                    d["summary_status"] = "legacy"
                out.append(d)
            if forgotten and not read_only:
                self._persist_peripheral_forgetting(forgotten)
            # Recall/event_context are de-duplicated by normalized event_key,
            # newest first; appended duplicates from older versions collapse here.
            dedup = []
            seen = set()
            for d in out[-max(1, limit) * 3:][::-1]:
                key = self._normalize_event_key(
                    str(d.get("event_key") or d.get("title") or ""),
                    str(d.get("title") or ""))
                if key in seen:
                    continue
                seen.add(key)
                dedup.append(d)
                if len(dedup) >= limit:
                    break
            return dedup
        except Exception:
            return []

    @staticmethod
    def _same_archive_event(obj: dict, target: dict) -> bool:
        try:
            if not isinstance(obj, dict) or not isinstance(target, dict):
                return False
            tid = str(target.get("id") or "").strip()
            did = str(obj.get("id") or "").strip()
            if tid and did:
                return tid == did
            if str(obj.get("title") or "") != str(target.get("title") or ""):
                return False
            return abs(float(obj.get("ts", 0) or 0) - float(target.get("ts", 0) or 0)) <= 1.0
        except Exception:
            return False

    def _rewrite_jsonl_atomic(self, path, mutate) -> int:
        """Rewrite a JSONL archive through a sibling temp file + os.replace.

        mutate(obj) returns True when it changed the row. Unparsable lines are
        preserved verbatim and nothing is written unless a row changed.
        """
        tmp = None
        try:
            path = Path(path)
            if not path.exists():
                return 0
            rows = []
            changed = 0
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    rows.append(("raw", line))
                    continue
                try:
                    _changed = bool(mutate(obj))
                except Exception:
                    _changed = False
                if _changed:
                    changed += 1
                rows.append(("obj", obj))
            if not changed:
                return 0
            tmp = path.with_name(path.name + ".tmp_%s_%s" % (os.getpid(), int(time.time() * 1000)))
            with open(tmp, "w", encoding="utf-8") as f:
                for kind, value in rows:
                    if kind == "raw":
                        f.write(str(value) + "\n")
                    else:
                        f.write(json.dumps(value, ensure_ascii=False) + "\n")
            atomic_file.replace(tmp, path)
            tmp = None
            return changed
        except Exception as exc:
            logger.warning("[biocore] archive rewrite failed %s: %s", path, exc)
            return 0
        finally:
            try:
                if tmp is not None and Path(tmp).exists():
                    Path(tmp).unlink()
            except Exception:
                pass

    # ---- task-33: deterministic memory-point worthiness + feedback ----
    @staticmethod
    def _worth_num(value, default: float = 0.0, lo: float = 0.0,
                   hi: float = 1.0) -> float:
        """Finite bounded float for worthiness inputs (NaN/Inf -> default)."""
        try:
            number = float(value)
        except Exception:
            return default
        if number != number or number in (float("inf"), float("-inf")):
            return default
        return max(lo, min(hi, number))

    def _event_worthiness_for(self, record, core, relationship=None, *,
                              text: str = "", title: str = "",
                              schema=None):
        """task-33: deterministic W/W_her/K for one event record (no LLM).

        Returns None when memory_worthiness_enabled is OFF: the caller then
        archives exactly like 1.2.98 (no worthiness field, no gate). All inputs
        are existing fields/proxies; the gate never writes biological state.
        """
        if not getattr(self, "memory_worthiness_enabled", True):
            return None
        rec = record if isinstance(record, dict) else {}
        body = str(text or rec.get("event") or rec.get("title") or "")
        heading = str(title or rec.get("title") or "")
        if schema is None:
            try:
                schema = memory_meta.schema_congruence(
                    body or heading, self._self_schema_texts(core))
            except Exception:
                schema = 0.0
        try:
            intensity = float(core._intensity()) if core is not None else 0.0
        except Exception:
            intensity = 0.0
        appraisal = (getattr(core, "appraisal", None)
                     if core is not None else None)
        appraisal = appraisal if isinstance(appraisal, dict) else {}
        importance = self._worth_num(rec.get("importance"), 0.5)
        schema_v = self._worth_num(schema, 0.0)
        self_defining = memory_meta.event_self_defining(schema_v, importance)
        try:
            milestone = 1.0 if relationship_meta.milestone_from_text(
                heading + " " + body) else 0.0
        except Exception:
            milestone = 0.0
        rel = relationship if isinstance(relationship, dict) else {}
        rel_state = rel.get("state") if isinstance(rel.get("state"), dict) else {}
        trust = self._worth_num(rel_state.get("trust"), 0.5)
        closeness = self._worth_num(rel_state.get("closeness"), 0.5)
        conflict = self._worth_num(rel_state.get("conflict"), 0.0)
        repair = self._worth_num(rel_state.get("repair"), 0.0)
        novelty = self._worth_num(appraisal.get("novelty"), 0.0)
        routine = False
        try:
            routine = bool(memory_meta.is_routine_event(
                body or heading, intensity=intensity, novelty=novelty,
                schema=schema_v))
        except Exception:
            routine = False
        # K (core-impact) proxies from existing L1 state.
        momentum = getattr(core, "momentum", None) if core is not None else None
        momentum = momentum if isinstance(momentum, dict) else {}
        pad_delta = self._worth_num(
            2.0 * (abs(self._worth_num(momentum.get("v"), 0.0, -1.0, 1.0))
                   + abs(self._worth_num(momentum.get("a"), 0.0, -1.0, 1.0))
                   + abs(self._worth_num(momentum.get("d"), 0.0, -1.0, 1.0))),
            0.0)
        self_delta = self._worth_num(
            abs(self._worth_num(getattr(core, "boundary_pressure", 0.0), 0.0))
            + abs(self._worth_num(getattr(core, "refusal_readiness", 0.0), 0.0)))
        homeo = getattr(core, "homeostasis", None) if core is not None else None
        homeo = homeo if isinstance(homeo, dict) else {}
        drives_delta = self._worth_num(homeo.get("L_int"), 0.0)
        trust_dev = abs(trust - 0.5) * 2.0
        close_dev = abs(closeness - 0.5) * 2.0
        rel_delta = self._worth_num(
            0.50 * (trust_dev + close_dev) / 2.0
            + 0.30 * conflict + 0.20 * repair)
        persistence = self._worth_num(
            0.40 + 0.60 * max(intensity, drives_delta, self_delta, rel_delta))
        return memory_meta.compute_worthiness(
            intensity=intensity, schema_congruence=schema_v,
            self_defining=self_defining, milestone=milestone,
            boundary_score=rec.get("boundary_score", 0.0),
            recall_count=rec.get("recall_count", 0),
            merge_count=rec.get("merge_count", 0),
            goal_relevance=appraisal.get("goal_relevance", 0.0),
            novelty=novelty, rel_trust=trust, rel_closeness=closeness,
            rel_conflict=conflict, rel_repair=repair, routine=routine,
            pad_delta=pad_delta, self_delta=self_delta,
            rel_delta=rel_delta, drives_delta=drives_delta,
            persistence=persistence)

    def _event_worthiness_decision(self, record, core, relationship=None, **kw):
        """Gate wrapper -> (worthiness|None, decision); OFF => legacy memory_point."""
        worth = self._event_worthiness_for(record, core, relationship, **kw)
        if worth is None:
            return None, "memory_point"
        return worth, str(worth.get("decision") or "archive_only")

    @staticmethod
    def _memory_point_snapshot(record) -> dict:
        rec = record if isinstance(record, dict) else {}
        return {"importance": rec.get("importance", 0.5),
                "user_marked": bool(rec.get("user_marked", False)),
                "title": str(rec.get("title") or "")[:80],
                "small_summary": str(rec.get("small_summary") or "")[:80]}

    def _apply_memory_point_feedback(self, record, event_id: str,
                                     action: str, body=None) -> bool:
        """Atomic-mutation helper for the feedback API (audit/snapshot kept)."""
        if not isinstance(record, dict):
            return False
        if str(record.get("id") or "") != str(event_id or ""):
            return False
        action = str(action or "").strip().lower()
        data = body if isinstance(body, dict) else {}
        if action not in MEMORY_POINT_FEEDBACK_ACTIONS:
            return False
        if action == "restore":
            prev = record.get("feedback_prev")
            if not isinstance(prev, dict):
                return False
            for key in ("importance", "user_marked", "title", "small_summary"):
                if key in prev:
                    record[key] = prev[key]
            record["last_feedback_action"] = "restore"
            record["feedback_ts"] = round(time.time(), 3)
            return True
        before = self._memory_point_snapshot(record)
        record["feedback_prev"] = before
        if action == "important":
            base = self._worth_num(record.get("importance"), 0.5)
            record["importance"] = round(min(1.0, base + 0.15), 4)
            record["user_marked"] = True
            record["memory_point"] = True
        elif action == "unimportant":
            record["importance"] = 0.15
            record["user_marked"] = False
        elif action == "edit_label":
            title = re.sub(r"\s+", " ", str(data.get("title") or "")).strip()
            small = str(data.get("small_summary") or "").strip()
            if not title and not small:
                return False
            if title:
                record["title"] = self._mask_if_safety(title)[:80]
            if small:
                record["small_summary"] = self._mask_if_safety(small)[:80]
            elif data.get("small_summary") is not None:
                record["small_summary"] = ""
            record["label_edited"] = True
            record["user_marked"] = True
        history = record.get("feedback_history")
        history = history if isinstance(history, list) else []
        record["feedback_history"] = ([{"action": action,
                                        "ts": round(time.time(), 3),
                                        "before": before}]
                                      + [h for h in history if isinstance(h, dict)])[:20]
        record["last_feedback_action"] = action
        record["feedback_ts"] = round(time.time(), 3)
        return True

    @staticmethod
    def _parse_memory_point_feedback_request(body):
        data = body if isinstance(body, dict) else {}
        event_id = str(data.get("event_id") or "").strip()
        action = str(data.get("action") or "").strip().lower()
        if not event_id:
            return "", "", "缺少 event_id"
        if action not in MEMORY_POINT_FEEDBACK_ACTIONS:
            return event_id, action, "未知操作"
        return event_id, action, ""

    def _memory_point_public(self, record) -> dict:
        rec = record if isinstance(record, dict) else {}
        worth = rec.get("worthiness") if isinstance(rec.get("worthiness"), dict) else None
        return {"event_id": str(rec.get("id") or ""),
                "title": str(rec.get("title") or "")[:80],
                "small_summary": str(rec.get("small_summary") or "")[:80],
                "big_summary": str(rec.get("big_summary") or "")[:EVENT_SUMMARY_HARD_MAX],
                "importance": round(self._worth_num(rec.get("importance"), 0.5), 4),
                "user_marked": bool(rec.get("user_marked", False)),
                "memory_point": bool(rec.get("memory_point", True)),
                "label_edited": bool(rec.get("label_edited", False)),
                "last_feedback_action": str(rec.get("last_feedback_action") or "")[:20],
                "worthiness": dict(worth) if worth is not None else None,
                "summary_status": str(rec.get("summary_status") or "legacy"),
                "summary_edited": bool(rec.get("summary_edited", False)),
                "summary_updated_ts": round(self._worth_num(
                    rec.get("summary_updated_ts"), 0.0, 0.0, 10 ** 12), 3)}

    async def page_memory_point_feedback(self):
        """POST memory-point feedback: important/unimportant/edit_label/restore."""
        from quart import request
        try:
            body = await request.get_json(silent=True) or {}
        except Exception:
            body = {}
        event_id, action, error = self._parse_memory_point_feedback_request(body)
        if error:
            return {"status": "error", "message": error}
        record = self._find_event_summary_record(event_id)
        if record is None:
            return {"status": "error", "message": "事件不存在"}
        if action == "edit_label":
            title = str(body.get("title") or "").strip()
            small = str(body.get("small_summary") or "").strip()
            if not title and not small:
                return {"status": "error", "message": "至少提供标题或小标签"}
            if len(title) > 80:
                return {"status": "error", "message": "标题不能超过 80 字"}
            if len(small) > 80:
                return {"status": "error", "message": "小标签不能超过 80 字"}
        if action == "restore" and not isinstance(record.get("feedback_prev"), dict):
            return {"status": "error", "message": "没有可恢复的反馈前版本"}
        try:
            changed = self._rewrite_jsonl_atomic(
                EVENT_ARCHIVE_PATH,
                lambda obj: self._apply_memory_point_feedback(obj, event_id, action, body))
        except Exception as exc:
            logger.warning("[biocore] memory point feedback rewrite failed: %s", exc)
            changed = 0
        if changed <= 0:
            return {"status": "error", "message": "事件不存在或写入失败"}
        # Per-session copy stays in sync (best effort; same atomic rewrite).
        try:
            session = str(record.get("session") or "")
            if session:
                self._rewrite_jsonl_atomic(
                    self._event_session_file(session),
                    lambda obj: self._apply_memory_point_feedback(
                        obj, event_id, action, body))
        except Exception:
            pass
        saved = self._find_event_summary_record(event_id) or {}
        return {"status": "ok", "data": self._memory_point_public(saved)}

    # ---- task-47: regenerate / edit one archived event summary ----
    @staticmethod
    def _parse_event_summary_request(body):
        """Validate an event_summary POST body -> (event_id, action, error)."""
        data = body if isinstance(body, dict) else {}
        event_id = str(data.get("event_id") or "").strip()
        action = str(data.get("action") or "").strip().lower()
        if not event_id:
            return "", "", "缺少 event_id"
        if action not in EVENT_SUMMARY_ACTIONS:
            return event_id, action, "未知操作"
        return event_id, action, ""

    @staticmethod
    def _validate_edited_event_summary(big, small, max_chars: int = 0):
        """Validate a manual summary edit -> (big, small, error)."""
        big_text = str(big or "").strip()
        small_text = str(small or "").strip()
        if not big_text:
            return "", "", "大总结不能为空"
        if len(small_text) > EVENT_SUMMARY_SMALL_MAX:
            return "", "", "小总结不能超过 %d 字" % EVENT_SUMMARY_SMALL_MAX
        try:
            cap = int(max_chars or 0)
        except Exception:
            cap = 0
        limit = EVENT_SUMMARY_HARD_MAX
        if cap > 0:
            limit = min(cap, EVENT_SUMMARY_HARD_MAX)
        return big_text[:limit], small_text, ""

    @staticmethod
    def _validate_edited_event_title(title):
        """Validate a manual event title -> (title, error); 1-80 chars."""
        text = re.sub(r"\s+", " ", str(title or "")).strip()
        if not text:
            return "", "标题不能为空"
        if len(text) > 80:
            return "", "标题不能超过 80 字"
        return text[:80], ""

    @staticmethod
    def _apply_event_summary_fields(record, event_id: str, updates: dict) -> bool:
        """Mutation for _rewrite_jsonl_atomic: touch only the target row."""
        if not isinstance(record, dict) or not isinstance(updates, dict):
            return False
        if str(record.get("id") or "") != str(event_id or ""):
            return False
        record.update(updates)
        return True

    @staticmethod
    def _event_summary_history_source(record) -> str:
        """Where the OLD summary came from: edit / regenerate / legacy."""
        if not isinstance(record, dict):
            return "legacy"
        status = str(record.get("summary_status") or "legacy").strip().lower()
        if record.get("summary_edited") is True or status == "edited":
            return "edit"
        if not status or status == "legacy":
            return "legacy"
        return "regenerate"

    def _event_summary_history_entry(self, record) -> dict:
        rec = record if isinstance(record, dict) else {}
        try:
            ts = float(rec.get("summary_updated_ts") or rec.get("ts") or time.time())
        except Exception:
            ts = time.time()
        status = str(rec.get("summary_status") or "legacy").strip().lower() or "legacy"
        return {"ts": ts,
                "title": str(rec.get("title") or "")[:80],
                "summary_status": status,
                "big_summary": str(rec.get("big_summary") or "")[:EVENT_SUMMARY_HARD_MAX],
                "small_summary": str(rec.get("small_summary") or "")[:EVENT_SUMMARY_SMALL_MAX],
                "source": self._event_summary_history_source(rec)}

    def _apply_event_summary_with_history(self, record, event_id: str, updates: dict) -> bool:
        """Mutation for the atomic rewrite: archive the old summary, then update.

        Keeps the newest 20 versions (newest first) so regenerating/editing never
        loses what the panel used to show.
        """
        if not isinstance(record, dict) or not isinstance(updates, dict):
            return False
        if str(record.get("id") or "") != str(event_id or ""):
            return False
        old_big = str(record.get("big_summary") or "").strip()
        old_small = str(record.get("small_summary") or "").strip()
        if old_big or old_small:
            entry = self._event_summary_history_entry(record)
            history = record.get("summary_history")
            if not isinstance(history, list):
                history = []
            kept = [h for h in history if isinstance(h, dict)]
            record["summary_history"] = [entry] + kept
            record["summary_history"] = record["summary_history"][:EVENT_SUMMARY_HISTORY_MAX]
        elif "summary_history" in record and not isinstance(record.get("summary_history"), list):
            record["summary_history"] = []
        record.update(updates)
        return True

    def _find_event_summary_record(self, event_id: str):
        try:
            target = str(event_id or "").strip()
            if not target or not EVENT_ARCHIVE_PATH.exists():
                return None
            for line in EVENT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                if isinstance(row, dict) and str(row.get("id") or "") == target:
                    return row
        except Exception as exc:
            logger.warning("[biocore] event summary lookup failed: %s", exc)
        return None

    @staticmethod
    def _event_summary_source_texts(record) -> list:
        try:
            source = [str(t or "").strip() for t in (record.get("source_texts") or [])
                      if str(t or "").strip()]
            if source:
                return source[:12]
        except Exception:
            pass
        out = []
        for value in (record.get("event"), record.get("central_details"),
                      record.get("title")):
            text = str(value or "").strip()
            if text:
                out.append(text)
        return out[:12]

    async def _regenerate_event_summary_fields(self, record) -> dict:
        """Regenerate big/small: LLM when enabled+available, else bounded fallback."""
        record = record if isinstance(record, dict) else {}
        title = str(record.get("title") or "").strip()
        texts = self._event_summary_source_texts(record)
        source_text = "\n".join(texts) if texts else str(record.get("event") or "")
        now = time.time()
        big = small = ""
        new_title = ""
        nuance = []
        summary_layers = []
        status = "fallback"
        llm_ok = False
        try:
            if self._llm_allowed("event_summary"):
                provider = await self._provider_for("event_summary", None)
                if provider is not None:
                    prompt = interpretation.event_summary_prompt(texts or [source_text])
                    resp = await provider.text_chat(prompt=prompt)
                    raw = str(getattr(resp, "completion_text", "") or "").strip()
                    data = interpretation.parse_event_summary(
                        raw, getattr(self, "summary_max_chars", 0))
                    llm_big = str(data.get("big_summary") or "").strip()
                    llm_small = str(data.get("small_summary") or "").strip()
                    llm_title = interpretation.clean_event_title(
                        data.get("title"), 80)
                    if llm_big or llm_small:
                        try:
                            cap = int(getattr(self, "summary_max_chars", 0) or 0)
                        except Exception:
                            cap = 0
                        limit = EVENT_SUMMARY_HARD_MAX
                        if cap > 0:
                            limit = min(cap, EVENT_SUMMARY_HARD_MAX)
                        big = self._mask_if_safety(str(llm_big or llm_small))[:limit]
                        small = self._mask_if_safety(
                            str(llm_small or llm_big))[:EVENT_SUMMARY_SMALL_MAX]
                        if llm_title:
                            new_title = llm_title[:80]
                        nuance = interpretation.clean_emotion_nuance(
                            data.get("emotion_nuance"))
                        summary_layers = interpretation.clean_emotion_layers(
                            data.get("emotion_layers"))
                        llm_ok = True
        except Exception as exc:
            logger.warning("[biocore] event summary regenerate via LLM failed: %s", exc)
            llm_ok = False
        if not llm_ok:
            big, small = self._dual_event_summary_fallback(source_text, title)
            status = "fallback"
            nuance = []   # deterministic fallback never fabricates a nuance layer
            summary_layers = []
        else:
            status = "llm"
        if not new_title:
            # deterministic title: cleaned first sentence -> meaning -> old title
            new_title = (interpretation.clean_event_title(source_text)
                         or interpretation.clean_event_title(record.get("meaning_to_her"))
                         or interpretation.clean_event_title(title)
                         or "对话事件")
        updates = {"title": str(new_title or "对话事件")[:80],
                   "big_summary": str(big or "")[:EVENT_SUMMARY_HARD_MAX],
                   "small_summary": str(small or "")[:EVENT_SUMMARY_SMALL_MAX],
                   "emotion_nuance": interpretation.clean_emotion_nuance(nuance),
                   "summary_status": status,
                   "summary_edited": False,
                   "summary_updated_ts": now}
        # task-68 correction: emotion proportions come from the summary itself
        # (normalized p, including the primary emotion). No fixed 50/30/20
        # weights and no fabrication: no layers in the output -> keep the old
        # value (possibly null) untouched.
        if summary_layers:
            updates["emotion_layers"] = summary_layers
            updates["emotion_layers_source"] = "summary"
        return updates

    async def page_event_summary(self):
        """Regenerate (LLM/fallback) or manually edit one archived event summary."""
        from quart import request
        try:
            body = await request.get_json(silent=True) or {}
        except Exception:
            body = {}
        event_id, action, error = self._parse_event_summary_request(body)
        if error:
            return {"status": "error", "message": error}
        record = self._find_event_summary_record(event_id)
        if record is None:
            return {"status": "error", "message": "事件不存在"}
        try:
            if action == "regenerate":
                updates = await self._regenerate_event_summary_fields(record)
            else:
                big, small, error = self._validate_edited_event_summary(
                    body.get("big_summary"), body.get("small_summary"),
                    getattr(self, "summary_max_chars", 0))
                if error:
                    return {"status": "error", "message": error}
                updates = {"big_summary": big, "small_summary": small,
                           "summary_status": "edited", "summary_edited": True,
                           "summary_updated_ts": time.time()}
                if body.get("title") is not None:
                    checked_title, title_error = self._validate_edited_event_title(
                        body.get("title"))
                    if title_error:
                        return {"status": "error", "message": title_error}
                    updates["title"] = checked_title
        except Exception as exc:
            logger.warning("[biocore] event summary %s failed: %s", action, exc)
            return {"status": "error", "message": "处理失败"}
        # task-51: a regenerate fills a missing secondary emotion from the live
        # core spectrum (primary excluded). update never rewrites it; no core
        # data keeps the field empty instead of fabricating one.
        if action == "regenerate" and not str(record.get("emotion_secondary") or "").strip():
            _secondary = self._event_secondary_for_record(record)
            if _secondary:
                updates["emotion_secondary"] = _secondary
        try:
            changed = self._rewrite_jsonl_atomic(
                EVENT_ARCHIVE_PATH,
                lambda obj: self._apply_event_summary_with_history(obj, event_id, updates))
        except Exception as exc:
            logger.warning("[biocore] event summary rewrite failed: %s", exc)
            changed = 0
        if changed <= 0:
            return {"status": "error", "message": "事件不存在或写入失败"}
        saved = self._find_event_summary_record(event_id) or {}
        history = saved.get("summary_history")
        payload = dict({"event_id": event_id, "action": action}, **updates)
        if "emotion_secondary" not in payload and str(saved.get("emotion_secondary") or "").strip():
            payload["emotion_secondary"] = str(saved.get("emotion_secondary") or "").strip()
        if isinstance(saved.get("emotion_nuance"), list):
            payload["emotion_nuance"] = list(saved.get("emotion_nuance") or [])[:3]
        if isinstance(saved.get("emotion_layers"), list):
            payload["emotion_layers"] = [dict(x) for x in (saved.get("emotion_layers") or [])[:4]
                                         if isinstance(x, dict)]
        try:
            payload["emotion_intensity"] = round(
                float(saved.get("emotion_intensity", 0.0) or 0.0), 4)
        except Exception:
            pass
        if str(saved.get("emotion_layers_source") or "").strip():
            payload["emotion_layers_source"] = str(
                saved.get("emotion_layers_source") or "").strip()
        payload["summary_history"] = history if isinstance(history, list) else []
        return {"status": "ok", "data": payload}

    def _event_pair_duplicate(self, row, prev,
                              window: float = EVENT_DEDUPE_CLEANUP_WINDOW) -> bool:
        """Multi-signal duplicate test for two rows of one canonical session.

        The two real rows from the ":"/"_" key generations share the same
        original conversation but their archive timestamps can be days apart,
        so the comparison uses the real event time (time_span) and accepts a
        merge when source texts overlap strongly or the summaries/titles are
        near-identical. False positives are limited by requiring the text
        signals, not just the canonical session.
        """
        try:
            gap = abs(event_effective_time(row) - event_effective_time(prev))
        except Exception:
            gap = 0.0
        if gap > window:
            return False
        try:
            title_sim = self._text_similarity(str(row.get("title") or ""),
                                              str(prev.get("title") or ""))
            body_sim = self._text_similarity(str(row.get("event") or ""),
                                             str(prev.get("event") or ""))
            summary_sim = max(
                self._text_similarity(str(row.get("big_summary") or ""),
                                      str(prev.get("big_summary") or "")),
                self._text_similarity(str(row.get("small_summary") or ""),
                                      str(prev.get("small_summary") or "")))
            left = {str(x) for x in (row.get("source_texts") or []) if str(x)}
            right = {str(x) for x in (prev.get("source_texts") or []) if str(x)}
            source_overlap = (len(left & right) / float(len(left | right))
                              if (left and right) else 0.0)
        except Exception:
            return False
        if source_overlap >= 0.5:
            return True
        if body_sim >= 0.6:
            return True
        if summary_sim >= 0.5 and (source_overlap >= 0.2 or title_sim >= 0.25
                                   or body_sim >= 0.3):
            return True
        if title_sim >= 0.5 and body_sim >= 0.2:
            return True
        return False

    @staticmethod
    def _drop_ids_from_jsonl(path, ids) -> int:
        """Remove rows with the given ids from a JSONL file atomically."""
        try:
            target = Path(path)
            drop = {str(x) for x in (ids or []) if str(x)}
            if not drop or not target.exists():
                return 0
            kept = []
            dropped = 0
            for line in target.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    kept.append(line)
                    continue
                if isinstance(obj, dict) and str(obj.get("id") or "") in drop:
                    dropped += 1
                    continue
                kept.append(json.dumps(obj, ensure_ascii=False))
            if not dropped:
                return 0
            tmp = target.with_name(target.name + ".tmp_%s_%s" % (
                os.getpid(), int(time.time() * 1000)))
            tmp.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
            atomic_file.replace(tmp, target)
            return dropped
        except Exception:
            return 0

    def _cleanup_duplicate_events(self, force: bool = False) -> int:
        """One-time cross-key duplicate cleanup for events.jsonl (task-56).

        Canonical sessions unify ":"/"_" key generations. Rows of one real
        conversation are grouped by canonical session + real event time
        (time_span) + text signals (source_texts/title/summary/body); the
        richer/newer row is kept and the poorer row is merged into it
        (source_texts union, importance/centrality/recall maxima, provenance,
        summary_history). Group sessions -- including the test group
        -- and unrelated rows are never touched. The global archive and every
        affected per-session archive are rewritten atomically; each merge is
        appended to dedupe_log.jsonl and a marker keeps the migration
        idempotent.
        """
        try:
            EVENT_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            marker = EVENT_ARCHIVE_DIR / "dedupe_v1.done"
            if not force and marker.exists():
                return 0
            if not EVENT_ARCHIVE_PATH.exists():
                return 0
            rows, raw_keep = [], []
            for line in EVENT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    raw_keep.append(line)
                    continue
                (rows if isinstance(obj, dict) else raw_keep).append(obj)
        except Exception:
            return 0

        def _score(row):
            status = str(row.get("summary_status") or "").lower()
            score = {"llm": 2.0, "edited": 1.5, "fallback": 0.5}.get(status, 0.0)
            try:
                score += float(row.get("importance", 0) or 0) * 0.5
            except Exception:
                pass
            if isinstance(row.get("summary_history"), list) and row.get("summary_history"):
                score += 0.20
            if row.get("event_embedding"):
                score += 0.10
            if isinstance(row.get("time_span"), dict):
                score += 0.10
            try:
                score += float(row.get("summary_updated_ts", 0) or 0) * 1e-9
            except Exception:
                pass
            try:
                score += float(row.get("ts", 0) or 0) * 1e-10
            except Exception:
                pass
            return score

        def _merge_into(rich, poor):
            try:
                src = [str(x) for x in (rich.get("source_texts") or []) if str(x)]
                for text in [str(x) for x in (poor.get("source_texts") or []) if str(x)]:
                    if text not in src:
                        src.append(text)
                rich["source_texts"] = src[-24:]
            except Exception:
                pass
            for key in ("importance", "centrality", "recall_count", "strength",
                        "confidence", "source_count", "last_recall"):
                try:
                    rich[key] = max(float(rich.get(key, 0) or 0),
                                    float(poor.get(key, 0) or 0))
                except Exception:
                    continue
            try:
                hist = []
                for item in (list(poor.get("summary_history") or [])
                             + list(rich.get("summary_history") or [])):
                    if isinstance(item, dict) and item not in hist:
                        hist.append(item)
                if hist:
                    rich["summary_history"] = hist[:EVENT_SUMMARY_HISTORY_MAX]
            except Exception:
                pass
            try:
                merged = [str(x) for x in (rich.get("merged_event_keys") or [])]
                for item in (poor.get("merged_event_keys") or []):
                    if str(item) and str(item) not in merged:
                        merged.append(str(item))
                poor_key = str(poor.get("event_key") or "")
                if poor_key and poor_key not in merged:
                    merged.append(poor_key)
                if merged:
                    rich["merged_event_keys"] = merged[:12]
            except Exception:
                pass
            try:
                prov = dict(rich.get("provenance") or {})
                sources = [x for x in (prov.get("sources") or [])
                           if isinstance(x, dict)][-24:]
                for item in ((poor.get("provenance") or {}).get("sources") or []):
                    if isinstance(item, dict) and item not in sources:
                        sources.append(item)
                prov["sources"] = sources[-24:]
                refs = [str(x) for x in (prov.get("message_refs") or []) if str(x)]
                for ref in ((poor.get("provenance") or {}).get("message_refs") or []):
                    ref = str(ref or "")
                    if ref and ref not in refs:
                        refs.append(ref)
                if refs:
                    prov["message_refs"] = refs[:12]
                rich["provenance"] = prov
            except Exception:
                pass
            try:
                rich["origin"] = _merged_origin(rich, discretion.origin_of(poor))  # ams-life
            except Exception:
                pass
            try:
                rich["merge_count"] = int(rich.get("merge_count", 0) or 0) + 1
                merged_from = [str(x) for x in (rich.get("merged_from") or [])]
                poor_id = str(poor.get("id") or "")
                if poor_id and poor_id not in merged_from:
                    merged_from.append(poor_id)
                if merged_from:
                    rich["merged_from"] = merged_from[-8:]
            except Exception:
                pass

        kept, dropped_ids, dropped_sessions, log_rows = [], set(), set(), []
        for row in rows:
            session = canonical_session_key(row.get("session"))
            row_id = str(row.get("id") or "")
            if not session or not row_id:
                kept.append(row)
                continue
            # Requirement: group events (the test group and other
            # group chats) are out of scope for this private-session migration.
            if ":GroupMessage:" in session or ":GuildMessage:" in session:
                kept.append(row)
                continue
            current = None
            for prev in kept:
                if canonical_session_key(prev.get("session")) != session:
                    continue
                if self._event_pair_duplicate(row, prev):
                    current = prev
                    break
            if current is None:
                kept.append(row)
                continue
            keep_new = _score(row) > _score(current)
            rich = row if keep_new else current
            poor = current if keep_new else row
            rich_id = str(rich.get("id") or "")
            poor_id = str(poor.get("id") or "")
            if not rich_id or not poor_id:
                kept.append(row)
                continue
            try:
                gap_seconds = round(abs(event_effective_time(rich)
                                        - event_effective_time(poor)), 3)
            except Exception:
                gap_seconds = 0.0
            _merge_into(rich, poor)
            if keep_new:
                try:
                    kept[kept.index(current)] = row
                except Exception:
                    kept.append(row)
            dropped_ids.add(poor_id)
            dropped_sessions.add(canonical_session_key(poor.get("session")))
            log_rows.append({
                "ts": round(time.time(), 3),
                "action": "dedupe_merge",
                "reason": "canonical_cross_key_duplicate",
                "session": session,
                "kept_id": rich_id,
                "kept_title": str(rich.get("title") or "")[:80],
                "dropped_id": poor_id,
                "dropped_title": str(poor.get("title") or "")[:80],
                "dropped_sessions": sorted({str(poor.get("session") or ""),
                                            str(rich.get("session") or "")}),
                "gap_seconds": gap_seconds,
                "merged_importance": rich.get("importance"),
                "merged_source_texts": len(rich.get("source_texts") or []),
            })
        if not dropped_ids:
            try:
                marker.write_text(str(time.time()), encoding="utf-8")
            except Exception:
                pass
            return 0
        removed = 0
        try:
            out = [json.dumps(r, ensure_ascii=False) for r in rows
                   if str(r.get("id") or "") not in dropped_ids]
            out += raw_keep
            tmp = EVENT_ARCHIVE_PATH.with_name(
                EVENT_ARCHIVE_PATH.name + ".tmp_%s_%s" % (
                    os.getpid(), int(time.time() * 1000)))
            tmp.write_text("\n".join(out) + ("\n" if out else ""), encoding="utf-8")
            atomic_file.replace(tmp, EVENT_ARCHIVE_PATH)
            removed = len(dropped_ids)
        except Exception as exc:
            logger.warning("[biocore] dedupe global rewrite failed: %s", exc)
            return 0
        # ":" and "_" variants sanitize to the same per-session file name.
        for session in dropped_sessions:
            if not session:
                continue
            try:
                safe = "".join(c if c.isalnum() or c in "-_" else "_"
                               for c in session)[:80]
                self._drop_ids_from_jsonl(EVENT_SESSION_DIR / safe / "events.jsonl",
                                          dropped_ids)
            except Exception:
                continue
        try:
            with open(EVENT_ARCHIVE_DIR / "dedupe_log.jsonl", "a",
                      encoding="utf-8") as log:
                for entry in log_rows:
                    log.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass
        try:
            marker.write_text(str(time.time()), encoding="utf-8")
        except Exception:
            pass
        logger.info("[biocore] canonical duplicate cleanup removed %s event(s)",
                    removed)
        return removed

    def _decayed_merge_count(self, event) -> int:
        """G11: merge_count decays on the same schedule as peripheral forgetting."""
        try:
            count = int(event.get("merge_count", 0) or 0)
            if count <= 0:
                return 0
            ts = float(event.get("ts", 0) or 0)
            if ts <= 0:
                return count
            age_days = max(0.0, (time.time() - ts) / 86400.0)
            decay = memory_meta.time_decay(age_days)
            return max(0, int(round(count * decay)))
        except Exception:
            return 0

    def _persist_peripheral_forgetting(self, events) -> None:
        """Persist periphery forgetting to both archive layers.

        The returned view already hides forgotten details; this keeps the
        global events.jsonl and archives/sessions/<session>/events.jsonl in
        sync through atomic rewrites instead of append-only drift. G11: the
        event merge_count is decayed (30-day half-life) in the same rewrite.
        """
        try:
            targets = [d for d in (events or []) if isinstance(d, dict)]
            if not targets:
                return

            def _mutate(obj):
                for target in targets:
                    if not self._same_archive_event(obj, target):
                        continue
                    obj["merge_count"] = self._decayed_merge_count(obj)
                    obj["peripheral_details"] = ""
                    obj["peripheral_retention"] = min(
                        float(obj.get("peripheral_retention", 1.0) or 1.0), 0.05)
                    obj["peripheral_forgotten"] = True
                    return True
                return False

            self._rewrite_jsonl_atomic(EVENT_ARCHIVE_PATH, _mutate)
            seen = set()
            for target in targets:
                _sess = str(target.get("session") or "default")
                _safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in _sess)[:80]
                if _safe in seen:
                    continue
                seen.add(_safe)
                self._rewrite_jsonl_atomic(EVENT_SESSION_DIR / _safe / "events.jsonl", _mutate)
        except Exception as exc:
            logger.warning("[biocore] peripheral forgetting persist failed: %s", exc)

    def _bump_event_recall(self, ids) -> None:
        try:
            if not EVENT_ARCHIVE_PATH.exists() or not ids:
                return
            wanted = set(ids)
            rows = []
            for line in EVENT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines():
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if isinstance(d, dict) and d.get("id") in wanted:
                    d["recall_count"] = int(d.get("recall_count", 0) or 0) + 1
                    d["last_recall"] = time.time()
                rows.append(d)
            EVENT_ARCHIVE_PATH.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                encoding="utf-8")
        except Exception:
            pass

    def _event_context(self, event) -> str:
        events = self._visible_events(event, self._event_archive(9))
        if not events:
            return ""
        events = sorted(events, key=lambda e: float(e.get("importance", 0.0) or 0.0) *
                        (0.5 + 0.5 * float(e.get("centrality", 0.5) or 0.5)), reverse=True)[:3]
        lines = []
        for ev in events:
            title = str(ev.get("title") or "").strip()
            body = str(ev.get("central_details") or ev.get("event") or "").strip()
            meaning = str(ev.get("meaning_to_her") or "").strip()
            reflection = str(ev.get("reflection") or "").strip()
            if body:
                lines.append("- %s：%s%s%s" % (
                    title or "事件", body,
                    ("；意义：" + meaning) if meaning else "",
                    ("；反思：" + reflection) if reflection else ""))
        if not lines:
            return ""
        self._bump_event_recall([str(e.get("id") or "") for e in events])
        return "\n".join(lines)

    def _insights(self, limit: int = 5) -> list:
        try:
            if not INSIGHT_ARCHIVE_PATH.exists():
                return []
            out = []
            for line in INSIGHT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines()[-limit * 2:]:
                try:
                    d = json.loads(line)
                    if isinstance(d, dict):
                        try:
                            _age_days = (time.time() - float(d.get("ts", 0) or 0)) / 86400.0
                            _central = float(d.get("centrality", 0.5) or 0.5)
                            if _age_days > (14.0 - 10.0 * _central):
                                d["peripheral_details"] = ""
                                d["peripheral_retention"] = min(float(d.get("peripheral_retention", 1.0) or 1.0), 0.05)
                                d["peripheral_forgotten"] = True
                        except Exception:
                            pass
                        out.append(d)
                except Exception:
                    continue
            return out[-limit:][::-1]
        except Exception:
            return []

    _KEPT_TEXT_KEYS = ("text", "event", "title", "small_summary", "big_summary", "meaning_to_her", "reflection",
                       "summary", "insight", "lesson")

    def _keep_record_text(self, record, what) -> bool:
        """Before an event or an insight is written: numbers out of its text; False when it
        crosses a red line (then it is not written)."""
        if not isinstance(record, dict):
            return True
        for k in self._KEPT_TEXT_KEYS:
            if isinstance(record.get(k), str):
                record[k] = self._scrub(record[k])
        if isinstance(record.get("source_texts"), list):
            record["source_texts"] = [self._scrub(x) if isinstance(x, str) else x for x in record["source_texts"]]
        return not self._red_line(" ".join(str(record.get(k) or "") for k in self._KEPT_TEXT_KEYS), what)

    def _append_insight(self, record: dict) -> None:
        if self._job_stale() or not self._new_item_kept(record) or not self._keep_record_text(record, "insight"):
            return
        try:
            EVENT_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            with open(INSIGHT_ARCHIVE_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def _insight_state_path(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        return DATA_DIR / "insight_trigger.json"

    def _load_insight_state(self) -> dict:
        try:
            path = self._insight_state_path()
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {"last_run_ts": 0.0, "last_event_ts": 0.0, "seen_ids": []}

    def _save_insight_state(self, state: dict) -> None:
        try:
            self._insight_state_path().write_text(
                json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as exc:
            logger.warning("[biocore] insight trigger state save failed: %s", exc)

    def _insight_trigger_decision(self, state: dict, events: list, now: float | None = None) -> dict:
        """Decide whether the unified insight entry should fire.

        Rules:
        - dedupe by event id + event ts (only events newer than last_event_ts count);
        - >= insight_min_new_events (default 3) new important events
          (importance >= 0.6) AND cooldown >= insight_cooldown_minutes (default 60);
        - 24h ultra-long fallback can fire with at least 1 new important event.
        """
        current = time.time() if now is None else float(now)
        st = state if isinstance(state, dict) else {}
        try:
            last_run = float(st.get("last_run_ts", 0.0) or 0.0)
        except Exception:
            last_run = 0.0
        try:
            last_event_ts = float(st.get("last_event_ts", 0.0) or 0.0)
        except Exception:
            last_event_ts = 0.0
        seen = st.get("seen_ids") if isinstance(st.get("seen_ids"), list) else []
        seen_set = {str(x) for x in seen}
        new_events = []
        for ev in (events or []):
            if not isinstance(ev, dict):
                continue
            try:
                imp = float(ev.get("importance", 0) or 0)
            except Exception:
                imp = 0.0
            if imp < 0.6:
                continue
            eid = str(ev.get("id") or "")
            try:
                ets = float(ev.get("ts", 0) or 0)
            except Exception:
                ets = 0.0
            if eid and eid in seen_set:
                continue
            if ets and ets <= last_event_ts:
                continue
            new_events.append(ev)
        count = len(new_events)
        elapsed = current - last_run if last_run > 0 else None
        _min_new = max(1, int(getattr(self, "_insight_min_new_events",
                                      INSIGHT_MIN_NEW_EVENTS) or INSIGHT_MIN_NEW_EVENTS))
        _cooldown_s = max(60, int(getattr(self, "_insight_cooldown_minutes",
                                          INSIGHT_COOLDOWN_SECONDS // 60)
                                  or (INSIGHT_COOLDOWN_SECONDS // 60)) * 60)
        cooldown_ok = (last_run <= 0) or (elapsed is not None and elapsed >= _cooldown_s)
        fallback_ok = (last_run > 0 and elapsed is not None and
                       elapsed >= self._insight_fallback_hours * 3600)
        ready = (count >= _min_new and cooldown_ok) or (count >= 1 and fallback_ok)
        return {"ready": bool(ready), "new_count": count,
                "new_events": new_events,
                "last_run_ts": last_run, "last_event_ts": last_event_ts}

    async def _maybe_archive_insight(self, event, core, trigger: str = "event_archive"):
        """Automatic long-term insight entry (compression / event archive).

        Only runs when the opt-in auto switch is ON *and* the insight LLM
        switch is ON. There is no silent deterministic fallback: with either
        switch off nothing is written in the background.
        """
        if not bool(getattr(self, "insight_auto_enabled", False)):
            return False
        if not self._llm_allowed("insight"):
            return False
        try:
            state = self._load_insight_state()
            events = self._event_archive(50)
            decision = self._insight_trigger_decision(state, events)
            if not decision["ready"]:
                logger.info("[biocore] insight trigger skipped (%s): new=%s cooldown/fallback not met",
                            trigger, decision["new_count"])
                return False
            new_events = decision["new_events"]
            # BUG-05: _event_archive returns newest-first; use [:6], not [-6:].
            recent = (events[:6] if len(events) >= 3 else new_events[:6])
            ok = await self._generate_insight(event, core, recent)
            if not ok:
                logger.info("[biocore] insight trigger produced nothing (%s); state not advanced", trigger)
                return False
            now = time.time()
            latest_ts = max([decision["last_event_ts"]] +
                            [float(e.get("ts", 0) or 0) for e in events] or [0.0])
            seen = [str(e.get("id") or "") for e in events if str(e.get("id") or "")]
            self._save_insight_state({
                "last_run_ts": now,
                "last_event_ts": latest_ts,
                "seen_ids": seen[-100:],
            })
            logger.info("[biocore] insight triggered (%s): new=%s events=%s",
                        trigger, decision["new_count"], len(recent))
            return True
        except Exception as exc:
            logger.warning("[biocore] insight trigger failed: %s", exc)
            return False

    async def _generate_insight(self, event, core, events):
        """Generate one long-term pattern insight from the given events.

        LLM-only: when the insight switch is off this returns False and writes
        nothing (no silent deterministic note in the background).
        """
        try:
            events = [e for e in (events or []) if isinstance(e, dict)]
            if not events:
                return False
            if not self._llm_allowed("insight"):
                return False
            provider = await self._provider_for("insight", event)
            if provider is None:
                return False
            prompt = interpretation.insight_prompt(events[:6])
            resp = await provider.text_chat(prompt=prompt)
            raw = str(getattr(resp, "completion_text", "") or "").strip()
            insight = interpretation.parse_insight(raw)
            if not insight:
                return False
            # ams-life step 1-2: an insight lives with the events (memory), not in her
            # body; its origin is that of the events it was drawn from, so forgetting
            # finds it and it is never shown where those events could not be.
            self._append_insight({
                "ts": time.time(), "insight": insight,
                "emotion": str(getattr(core, "labels", {}).get("emotion") or "neutral") if core else "neutral",
                "event_ids": [str(e.get("id") or "") for e in events[:6]],
                "origin": discretion.merge([discretion.origin_of(e) for e in events[:6]]),
            })
            try:
                if core is not None:
                    core.integrate_noise("reflection", attention=0.006, valence=0.003)
            except Exception:
                pass
            logger.info("[biocore] long-term insight archived")
            return True
        except Exception as exc:
            logger.warning("[biocore] insight generation failed: %s", exc)
            return False

    async def _archive_cross_event_insight(self, event, core):
        """Compatibility wrapper for direct callers: uses the last 6 events."""
        events = self._event_archive(6)
        if len(events) < 3:
            return
        await self._generate_insight(event, core, events[:6])

    def _segment_event_rows(self, entries) -> list:
        """The last three stretches of conversation, each a list of (text, entry).
        ams-life: the entries come along, so nothing has to find them again by text
        (a picture's caption is added to its text here, so that would miss them)."""
        try:
            rows = []
            for e in entries:
                txt = str(e.get("text", "")).strip()
                cap = str(e.get("image_caption", "") or "").strip()
                if cap:
                    txt = (txt + "\n[图片内容] " + cap).strip() if txt else ("[图片内容] " + cap)
                if txt:
                    rows.append((float(e.get("ts", 0) or 0), txt, e))
            rows.sort(key=lambda x: x[0])
        except Exception:
            return []
        segments = []
        current = []
        last = None
        for ts, txt, e in rows:
            _changed = False
            if current:
                try:
                    _changed = self._text_similarity(str(current[-1][0]), str(txt)) < 0.045 and len(str(txt)) > 8
                except Exception:
                    _changed = False
            if last is not None and ((ts - last > 1800) or _changed) and current:
                segments.append(current)
                current = []
            current.append((txt, e))
            last = ts
        if current:
            segments.append(current)
        return [list(seg) for seg in segments[-3:]]

    def _append_event_archive(self, record: dict) -> None:
        if self._job_stale() or not self._new_item_kept(record) or not self._keep_record_text(record, "event"):
            return
        try:
            EVENT_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            if isinstance(record, dict):
                _raw_key = str(record.get("event_key") or record.get("title") or "")
                _norm_key = self._normalize_event_key(_raw_key, str(record.get("title") or ""))
                if _norm_key:
                    record["event_key"] = _norm_key
                # Batch5 H2-1: <=3 event-event edges (time proximity 1800s +
                # causal words), Radvansky & Zacks 2014; Trabasso 1985.
                if getattr(self, "memory_chain_enabled", False):
                    try:
                        _sess = str(record.get("session") or "default")
                        _recent = self._recent_session_events(_sess, 3)
                        _text = " ".join(str(record.get(k) or "") for k in
                                         ("title", "event", "big_summary"))
                        _causal = any(w in _text for w in
                                      ("因为", "所以", "导致", "于是", "结果", "因此", "然后", "后来"))
                        _rts = float(record.get("ts", 0) or 0)
                        _links = []
                        for _prev in _recent[-3:]:
                            if not isinstance(_prev, dict) or not _prev.get("id"):
                                continue
                            _gap = abs(_rts - float(_prev.get("ts", 0) or 0))
                            if _gap > 1800.0:
                                continue
                            _w = 1.0 if _causal else max(0.5, 1.0 - 0.5 * _gap / 1800.0)
                            _links.append({"id": str(_prev["id"]), "weight": round(_w, 3),
                                           "ts": _rts, "kind": "causal" if _causal else "temporal"})
                            if len(_links) >= 3:
                                break
                        if _links:
                            record["chain_links"] = _links
                    except Exception:
                        pass
                # ams-life: where it happened, who it is about, which messages it came from.
                if not isinstance(record.get("origin"), dict):
                    record["origin"] = discretion.origin_of(record)
            line = json.dumps(record, ensure_ascii=False)
            with open(EVENT_ARCHIVE_PATH, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            _sess = str(record.get("session") or "default")
            _safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in _sess)[:80]
            _dir = EVENT_SESSION_DIR / _safe
            _dir.mkdir(parents=True, exist_ok=True)
            with open(_dir / "events.jsonl", "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception as exc:
            logger.warning("[biocore] event archive failed: %s", exc)

    def _chain_event_lines(self, session: str, query: str, limit: int = 2) -> list:
        """H2-1 read path: decayed event-chain expansion (default OFF).

        Only called when memory_chain_enabled. Seeds = same-session event with
        the highest character overlap with the query; follows its chain_links
        (hop<=1), applies 30-day decay, returns <=limit lines (no avalanche).
        """
        if not getattr(self, "memory_chain_enabled", False):
            return []
        try:
            events = [e for e in self._event_archive(100) if isinstance(e, dict)]
            sess = str(session or "")
            same = [e for e in events if str(e.get("session") or "default") == sess]
            if not same:
                return []
            q = set(str(query or ""))
            def _overlap(e):
                txt = str(e.get("title") or "") + " " + str(e.get("big_summary") or "")
                return len(q & set(txt))
            same.sort(key=lambda e: (-_overlap(e), -float(e.get("ts", 0) or 0)))
            seed = same[0]
            out = []
            for link in (seed.get("chain_links") or [])[:3]:
                if not isinstance(link, dict):
                    continue
                lid = str(link.get("id") or "")
                target = next((e for e in same if str(e.get("id") or "") == lid), None)
                if not target:
                    continue
                w = memory_meta.decayed_chain_weight(link.get("weight", 1.0), link.get("ts", 0))
                if w < 0.1:
                    continue
                text = str(target.get("title") or target.get("big_summary") or "").strip().replace("\n", " ")
                if text:
                    out.append("- 关联事件(链 %.2f)：%s" % (w, text[:160]))
                if len(out) >= limit:
                    break
            return out
        except Exception:
            return []

    def _attachments_from_messages(self, event) -> list:
        out = []
        try:
            for m in event.get_messages() or []:
                if isinstance(m, Image):
                    ref = str(getattr(m, "url", "") or getattr(m, "file", "") or getattr(m, "path", "") or "").strip()
                    if ref:
                        out.append({"type": "image", "ref": ref[:500]})
                elif isinstance(m, Record):
                    ref = str(getattr(m, "url", "") or getattr(m, "file", "") or "").strip()
                    if ref:
                        out.append({"type": "voice", "ref": ref[:500]})
        except Exception:
            pass
        return out

    def _memory_provenance(self, event, ts=None) -> dict:
        try:
            _sid, _sname = self._speaker(event)
        except Exception:
            _sid, _sname = "", ""
        # ams-life: message_refs is this message's own id (what forgetting by message
        # looks for); the id of a message it quotes goes in reply_to, never in the refs.
        prov = {"sender_id": _sid, "sender_name": _sname,
                "session": str(getattr(event, "unified_msg_origin", "") or ""),
                "ts": float(ts if ts is not None else time.time()),
                "message_refs": self._source_ids(event)}
        quoted = self._reply_to(event)
        if quoted:
            prov["reply_to"] = quoted
        return prov

    def _event_provenance(self, event, entries=None, ts=None) -> dict:
        prov = self._memory_provenance(event, ts)
        sources = []
        refs = list(prov.get("message_refs") or [])
        senders = {str(prov.get("sender_id") or "")}
        if entries:
            for e in entries[-24:]:
                p = e.get("provenance") if isinstance(e, dict) else None
                if not isinstance(p, dict):
                    continue
                item = {"sender_id": str(p.get("sender_id") or ""),
                        "sender_name": str(p.get("sender_name") or ""),
                        "session": str(p.get("session") or ""),
                        "ts": float(p.get("ts", 0) or 0),
                        "message_refs": list(p.get("message_refs") or [])[:6]}
                sources.append(item)
                senders.add(item["sender_id"])
                refs.extend(item["message_refs"])
        prov["sources"] = sources[-24:]
        prov["message_refs"] = list(dict.fromkeys([str(x) for x in refs if x]))[:12]
        prov["senders"] = sorted([x for x in senders if x])
        return prov

    @staticmethod
    def _source_check(text: str, texts, provenance=None, record_ts=None) -> dict:
        try:
            src = "".join(str(t) for t in texts)
            src_chars = {c for c in src if not c.isspace() and c not in "，。！？、；：,.!?;:"}
            body = {c for c in str(text or "") if not c.isspace() and c not in "，。！？、；：,.!?;:"}
            if not body:
                return {"overlap": 0.0, "coverage": 0.0, "novelty": 0.0,
                        "length_ratio": 0.0, "status": "empty",
                        "source_items": [], "time_ok": True, "speaker_ok": True,
                        "cross_ref": 0}
            overlap = sum(1 for c in body if c in src_chars) / max(1, len(body))
            covered = sum(1 for c in src_chars if c in body) / max(1, len(src_chars))
            novelty = max(0.0, len(body - src_chars) / max(1, len(body)))
            ratio = len(str(text or "")) / max(1, len(src))
            source_items = []
            try:
                prov = provenance if isinstance(provenance, dict) else {}
                _srcs = prov.get("sources") if isinstance(prov.get("sources"), list) else []
                if _srcs:
                    source_items = [dict(x) for x in _srcs if isinstance(x, dict)][:24]
                elif prov:
                    source_items = [{
                        "sender_id": str(prov.get("sender_id") or ""),
                        "sender_name": str(prov.get("sender_name") or ""),
                        "session": str(prov.get("session") or ""),
                        "ts": float(prov.get("ts", 0) or 0),
                        "message_refs": list(prov.get("message_refs") or []),
                    }]
            except Exception:
                source_items = []
            # time_ok: evidence cannot postdate the record and must be near it.
            time_ok = True
            try:
                _rts = float(record_ts if record_ts is not None else 0.0)
                _ts = [float(x.get("ts", 0) or 0) for x in source_items
                       if float(x.get("ts", 0) or 0) > 0]
                if _rts > 0 and _ts:
                    time_ok = (max(_ts) <= _rts + 300.0) and ((_rts - min(_ts)) <= 7 * 86400.0)
            except Exception:
                time_ok = True
            # speaker_ok: the claimed speaker must appear among the sources.
            speaker_ok = True
            try:
                _claim_sid = str((provenance or {}).get("sender_id") or "") if isinstance(provenance, dict) else ""
                _sids = {str(x.get("sender_id") or "") for x in source_items if str(x.get("sender_id") or "")}
                if _claim_sid and _sids:
                    speaker_ok = _claim_sid in _sids
            except Exception:
                speaker_ok = True
            # cross_ref: count independent evidence items / message refs.
            cross_ref = 0
            try:
                _refs = set()
                for x in source_items:
                    for r in (x.get("message_refs") or []):
                        _refs.add(str(r))
                cross_ref = max(len(source_items), len(_refs))
            except Exception:
                cross_ref = len(source_items)
            if overlap >= 0.55 and novelty <= 0.25 and ratio <= 1.6:
                status = "ok"
            elif overlap >= 0.35 and novelty <= 0.45:
                status = "weak"
            else:
                status = "suspect"
            if not time_ok or not speaker_ok:
                if status == "ok":
                    status = "weak"
            return {"overlap": round(overlap, 3), "coverage": round(covered, 3),
                    "novelty": round(novelty, 3), "length_ratio": round(ratio, 3),
                    "status": status, "source_items": source_items[:24],
                    "time_ok": bool(time_ok), "speaker_ok": bool(speaker_ok),
                    "cross_ref": int(cross_ref)}
        except Exception:
            return {"overlap": 0.0, "status": "unknown"}

    @staticmethod
    def _event_session_file(session: str) -> Path:
        _safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(session or "default"))[:80]
        return EVENT_SESSION_DIR / _safe / "events.jsonl"

    def _last_session_event(self, session: str):
        try:
            path = self._event_session_file(session)
            if not path.exists():
                return None
            for line in reversed(path.read_text(encoding="utf-8").splitlines()):
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if isinstance(d, dict):
                    return d
        except Exception:
            pass
        return None

    def _event_boundary(self, session: str, body: str, ts: float) -> dict:
        """Zacks et al. (2007) event segmentation for the event archive.

        Boundary = weighted elapsed-time gap + content dissimilarity against
        the previous event in the same session. A boundary below the split
        threshold continues the previous episode and inherits its id as
        parent_event_id; a strong boundary starts a new root event.
        """
        prev = self._last_session_event(session)
        if not isinstance(prev, dict):
            return {"boundary_score": 0.0, "parent_event_id": "",
                    "gap_seconds": 0.0, "similarity": 0.0}
        try:
            gap = max(0.0, float(ts) - float(prev.get("ts", 0) or 0))
        except Exception:
            gap = 0.0
        try:
            sim = float(self._text_similarity(str(body or ""), str(prev.get("event") or prev.get("title") or "")))
        except Exception:
            sim = 0.0
        gap_norm = max(0.0, min(1.0, gap / EVENT_BOUNDARY_WINDOW_SECONDS))
        score = max(0.0, min(1.0, EVENT_BOUNDARY_TIME_WEIGHT * gap_norm
                            + EVENT_BOUNDARY_TEXT_WEIGHT * (1.0 - sim)))
        parent = ""
        if score < EVENT_BOUNDARY_PARENT_THRESHOLD:
            parent = str(prev.get("id") or "")
        return {"boundary_score": round(score, 3), "parent_event_id": parent,
                "gap_seconds": round(gap, 3), "similarity": round(sim, 3)}

    @staticmethod
    def _text_similarity(a: str, b: str) -> float:
        """Bigram Jaccard similarity shared by archive/dedupe paths (task-56).

        BioCore keeps its own copy for the state machine; the plugin-level
        archive code calls this through ``self`` so duplicate detection and
        event boundary scoring actually run instead of raising AttributeError
        inside the surrounding try/except.
        """
        return BioCore._text_similarity(a, b)

    @staticmethod
    def _normalize_event_key(key: str, title: str = "") -> str:
        """Normalize event identity: NFKC, lowercase, punctuation/joiners removed."""
        import unicodedata

        def _norm(value) -> str:
            s = unicodedata.normalize("NFKC", str(value or "")).strip().lower()
            s = s.replace("／", "/").replace("·", "")
            s = re.sub(r"[\s\-_/\\|｜&＆+＋~～,，.。、;；:：!！?？'\"“”‘’()（）\[\]【】<>《》]+", "", s)
            return s[:120]

        out = _norm(key)
        if not out:
            out = _norm(title)
        if not out:
            out = "evt_" + _sha256(str(key) + "|" + str(title))[:12]
        return out

    def _recent_session_events(self, session: str, limit: int = 20) -> list:
        try:
            path = self._event_session_file(session)
            if not path.exists():
                return []
            rows = []
            for line in reversed(path.read_text(encoding="utf-8").splitlines()):
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if isinstance(d, dict):
                    rows.append(d)
                if len(rows) >= limit:
                    break
            return rows
        except Exception:
            return []

    def _find_duplicate_event(self, session: str, event_key: str, body: str, ts: float):
        """Return the same-session archived event this record duplicates."""
        try:
            for prev in self._recent_session_events(session, 20):
                prev_key = self._normalize_event_key(
                    str(prev.get("event_key") or prev.get("title") or ""),
                    str(prev.get("title") or ""))
                if not prev_key:
                    continue
                try:
                    # task-56: compare against the real event time so a
                    # re-archived row is not treated as a new event.
                    gap = abs(float(ts) - event_effective_time(prev))
                except Exception:
                    gap = 0.0
                if gap > EVENT_DUP_WINDOW_SECONDS:
                    continue
                if prev_key == event_key:
                    return prev
                if self._text_similarity(prev_key, event_key) >= EVENT_KEY_SIM_THRESHOLD:
                    body_sim = self._text_similarity(str(body or ""), str(prev.get("event") or ""))
                    if body_sim >= 0.45:
                        return prev
            # task-57: the same real session may be archived under ":" and "_"
            # variants; compare canonical keys across the archive too.
            target_session = canonical_session_key(session)
            try:
                _event_key = self._normalize_event_key(str(event_key or ""), "")
            except Exception:
                _event_key = str(event_key or "")
            for prev in self._event_archive(200):
                if canonical_session_key(prev.get("session")) != target_session:
                    continue
                try:
                    gap = abs(float(ts) - event_effective_time(prev))
                except Exception:
                    gap = 0.0
                if gap > EVENT_DUP_WINDOW_SECONDS:
                    continue
                prev_key = self._normalize_event_key(
                    str(prev.get("event_key") or prev.get("title") or ""),
                    str(prev.get("title") or ""))
                if prev_key and prev_key == _event_key:
                    return prev
                if prev_key and self._text_similarity(prev_key, _event_key) >= EVENT_KEY_SIM_THRESHOLD:
                    if self._text_similarity(str(body or ""), str(prev.get("event") or "")) >= 0.45:
                        return prev
                if self._text_similarity(str(body or ""), str(prev.get("event") or "")) >= 0.60:
                    return prev
        except Exception:
            pass
        return None

    def _find_global_duplicate_event(self, event_key: str, body: str, ts: float):
        """Cross-session event identity: same normalized key + body within window."""
        try:
            if not EVENT_ARCHIVE_PATH.exists():
                return None
            event_key = self._normalize_event_key(str(event_key or ""), "")
            lines = EVENT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines()
            for line in reversed(lines[-200:]):
                try:
                    prev = json.loads(line)
                except Exception:
                    continue
                if not isinstance(prev, dict):
                    continue
                prev_key = self._normalize_event_key(
                    str(prev.get("event_key") or prev.get("title") or ""),
                    str(prev.get("title") or ""))
                if not prev_key:
                    continue
                try:
                    gap = abs(float(ts) - event_effective_time(prev))
                except Exception:
                    gap = 0.0
                if gap > EVENT_DUP_WINDOW_SECONDS:
                    continue
                if prev_key == event_key:
                    return prev
                if self._text_similarity(prev_key, event_key) >= EVENT_KEY_SIM_THRESHOLD:
                    if self._text_similarity(str(body or ""),
                                             str(prev.get("event") or "")) >= 0.45:
                        return prev
        except Exception:
            pass
        return None

    def _find_any_duplicate_event(self, session: str, event_key: str, body: str, ts: float):
        """Same-session duplicate first, then cross-session global duplicate.

        ams-life: a duplicate from another chat window is not merged; merging
        would carry this window's source texts into an event of another place.
        """
        prev = self._find_duplicate_event(session, event_key, body, ts)
        if prev is not None:
            return prev
        prev = self._find_global_duplicate_event(event_key, body, ts)
        if prev is not None and discretion.origin_of(prev)["where"] != discretion.place_of(session):
            return None
        return prev

    def _merge_archive_duplicate(self, prev: dict, record: dict) -> None:
        """Merge a duplicate event into the existing archive row atomically."""
        if self._job_stale():
            return
        try:
            prev_id = str(prev.get("id") or "")
            if not prev_id:
                return
            _new_key = str(record.get("event_key") or "")
            _new_ts = float(record.get("ts", 0) or 0)
            _new_sources = list((record.get("provenance") or {}).get("sources") or [])[:12]
            _new_texts = list(record.get("source_texts") or [])[:12]
            _new_origin = discretion.origin_of(record)

            def _mutate(obj):
                if str(obj.get("id") or "") != prev_id:
                    return False
                merged = [str(x) for x in (obj.get("merged_event_keys") or [])]
                if _new_key and _new_key not in merged:
                    merged.append(_new_key)
                obj["merged_event_keys"] = merged[:12]
                try:
                    obj["ts"] = max(float(obj.get("ts", 0) or 0), _new_ts)
                except Exception:
                    obj["ts"] = _new_ts
                obj["importance"] = round(max(float(obj.get("importance", 0) or 0),
                                              float(record.get("importance", 0) or 0)), 3)
                obj["centrality"] = round(max(float(obj.get("centrality", 0) or 0),
                                              float(record.get("centrality", 0) or 0)), 3)
                obj["merge_count"] = int(obj.get("merge_count", 0) or 0) + 1
                src = [str(x) for x in (obj.get("source_texts") or [])[-24:]]
                for _t in _new_texts:
                    if _t and _t not in src:
                        src.append(str(_t))
                obj["source_texts"] = src[-24:]
                prov = dict(obj.get("provenance") or {})
                sources = [x for x in (prov.get("sources") or []) if isinstance(x, dict)][-24:]
                for _item in _new_sources:
                    if isinstance(_item, dict) and _item not in sources:
                        sources.append(_item)
                prov["sources"] = sources[-24:]
                obj["provenance"] = prov
                # ams-life: whoever said the merged lines is in the origin too
                obj["origin"] = _merged_origin(obj, _new_origin)
                return True

            session = str(prev.get("session") or record.get("session") or "default")
            self._rewrite_jsonl_atomic(EVENT_ARCHIVE_PATH, _mutate)
            self._rewrite_jsonl_atomic(self._event_session_file(session), _mutate)
            logger.info("[biocore] duplicate event merged: %s key=%s", prev.get("title"), _new_key)
        except Exception as exc:
            logger.warning("[biocore] duplicate merge failed: %s", exc)

    async def _archive_ranked_events_deterministic(self, event, core, entries):
        """Deterministic event candidate generation + embedding ranking.

        Used when the LLM event_ranking function is off (the default): split
        recent messages into event segments, score them with importance /
        self-schema congruence / embedding novelty / commitment cues, and
        archive the top candidates. The LLM is still optional via event_summary.
        """
        try:
            segments = self._segment_event_rows(entries)
            if not segments:
                return
            now = time.time()
            recent_events = self._event_archive(10)
            candidates = []
            for seg in segments:
                seg_texts = [txt for txt, _e in seg]
                seg_text = "\n".join(str(t) for t in seg_texts if str(t).strip()).strip()
                if len(seg_text) < 8:
                    continue
                # ams-life: the segment's own entries (BioCore looked them up again by text,
                # which misses a picture's message: its text carries the caption here)
                seg_entries = [e for _t, e in seg]
                imp = 0.5
                vecs = []
                for e in seg_entries:
                    try:
                        imp = max(imp, float(e.get("importance", 0.5) or 0.5))
                    except Exception:
                        pass
                    _v = e.get("vector") if isinstance(e.get("vector"), list) else []
                    if _v:
                        vecs.append(_v)
                try:
                    schema = memory_meta.schema_congruence(
                        seg_text, self._self_schema_texts(core))
                except Exception:
                    schema = 0.0
                try:
                    # M1: an event segment that contains an already-tagged
                    # sensitive memory is withheld from the provider when safety
                    # is on (default off => identical to 1.2.98).
                    _seg_sensitive = any(bool(e.get("sensitive")) for e in seg_entries)
                    vec = await self._embedding_for(
                        "event_ranking", seg_text[:600],
                        sensitive=self._embed_skip_sensitive(_seg_sensitive))
                except Exception:
                    vec = []
                if not vec and vecs:
                    try:
                        dim = len(vecs[0])
                        vec = [sum(float(v[i]) for v in vecs if i < len(v)) / len(vecs)
                               for i in range(dim)]
                    except Exception:
                        vec = []
                novelty = 0.6
                max_cos = 0.0
                for ev in recent_events:
                    _ev = ev.get("event_embedding") if isinstance(ev, dict) else None
                    if isinstance(_ev, list) and _ev:
                        max_cos = max(max_cos, self._cosine(vec, _ev))
                if vec and max_cos > 0:
                    novelty = max(0.0, min(1.0, 1.0 - max_cos))
                cues = sum(1 for w in ("承诺", "答应", "喜欢", "讨厌", "对不起", "谢谢",
                                        "以后", "永远", "骗", "害怕", "难过", "别")
                           if w in seg_text)
                cue_score = min(1.0, cues / 3.0)
                score = 0.35 * imp + 0.25 * schema + 0.20 * novelty + 0.20 * cue_score
                if imp < 0.55 or score < 0.40:
                    continue
                candidates.append((score, seg_text, seg_entries, vec, schema, imp, list(seg_texts)))
            if len(candidates) > 1 and getattr(self, "event_ranking_llm", False):
                _docs = [c[1] for c in candidates]
                _rs = await self._rerank_scores(
                    "event_ranking", "最近对话中值得记住的重要事件", _docs)
                if _rs:
                    candidates = [
                        (round(0.6 * c[0] + 0.4 * float(_rs.get(i, 0.0)), 4),
                         c[1], c[2], c[3], c[4], c[5], c[6])
                        for i, c in enumerate(candidates)
                    ]
            candidates.sort(key=lambda x: x[0], reverse=True)
            _digest_event_ids = []
            for score, body, seg_entries, vec, schema, imp, seg_texts in candidates[:2]:
                # ams-life: seg_texts is this candidate's own (BioCore read the variable the
                # segment loop above left behind: the last segment's texts)
                title = interpretation.clean_event_title(body) or "对话事件"
                _ekey = self._normalize_event_key(title, title)
                # ams-life: the sources are the entries this event was made of (BioCore took
                # the last 24 of all), and the origin takes in each one's origin
                prov = self._event_provenance(event, seg_entries, ts=now)
                check = self._source_check(body, [str(t) for t in seg_entries],
                                           provenance=prov, record_ts=now)
                # task-56: duplicate detection compares the real message time
                # (time_span end), not the archival moment, so a delayed
                # re-archive of the same conversation still dedupes.
                try:
                    _real_ts = max(float(e.get("ts", 0) or 0) for e in seg_entries
                                   if float(e.get("ts", 0) or 0) > 0)
                except Exception:
                    _real_ts = now
                dup = self._find_any_duplicate_event(
                    str(getattr(event, "unified_msg_origin", "") or ""), _ekey, body, _real_ts)
                if dup is not None:
                    continue
                _imp = round(max(0.55, min(1.0, imp * 0.7 + score * 0.3)), 3)
                _safe_title = self._mask_if_safety(title)
                _safe_body = self._mask_if_safety(self._event_excerpt(body, 220))
                _safe_big, _safe_small = self._dual_event_summary_fallback(body, title)
                record = {
                    "id": "evt_" + str(int(now)) + "_" + str(abs(hash(title + body)) % 100000),
                    "ts": now,
                    "session": str(getattr(event, "unified_msg_origin", "") or ""),
                    "title": _safe_title,
                    "event": _safe_body[:600],
                    "big_summary": _safe_big,
                    "small_summary": _safe_small,
                    "summary_status": "fallback",
                    "event_key": _ekey,
                    "centrality": round(max(0.0, min(1.0, schema)), 3),
                    "central_details": _safe_body[:180],
                    "peripheral_details": "",
                    "meaning_to_her": "",
                    "reflection": "",
                    "emotion": str((getattr(core, "labels", {}) or {}).get("emotion") or "neutral") if core else "neutral",
                    "emotion_secondary": self._secondary_emotion(core),
                    "emotion_nuance": [],
                    "emotion_layers": self._event_emotion_layers(core),
                    "emotion_layers_source": "core",
                    "emotion_intensity": self._event_emotion_intensity(core),
                    "importance": _imp,
                    "appraisal": dict(core.appraisal) if core is not None else {},
                    "confidence": round(max(0.2, min(1.0, 0.55 + 0.45 * float(check.get("overlap", 0)))), 3),
                    "source_count": len(seg_entries),
                    "source_check": check,
                    "provenance": prov,
                    "attachments": [],
                    "modalities": [],
                    "recall_count": 0,
                    "last_recall": now,
                    "strength": _imp,
                    "source_texts": [self._mask_if_safety(t) for t in seg_texts[:12]],
                    "ranking_mode": "deterministic_embedding",
                    "milestone": relationship_meta.milestone_from_text(title + " " + body),
                }
                _o = discretion.merge([discretion.origin_of(e) for e in seg_entries]
                                      + [discretion.origin_of({"provenance": prov})])
                record["origin"] = discretion.make_origin(self._here(event), _o["people"],
                                                          _o["source_ids"], _o["visibility"])
                if vec:
                    record["event_embedding"] = [round(float(x), 5) for x in vec]
                try:
                    times = [float(e.get("ts", 0) or 0) for e in seg_entries]
                    times = [t for t in times if t > 0]
                    if times:
                        record["time_span"] = {"start_ts": round(min(times), 3),
                                               "end_ts": round(max(times), 3),
                                               "span_seconds": round(max(times) - min(times), 3)}
                except Exception:
                    pass
                # task-33: worthiness gate (OFF => legacy: archive everything).
                _memory_point = True
                try:
                    _rel = self._relationship_of(self._user_record(event))
                except Exception:
                    _rel = {}
                try:
                    _worth = self._event_worthiness_for(
                        record, core, _rel, text=body, title=title, schema=schema)
                except Exception as exc:
                    logger.warning("[biocore] worthiness failed: %s", exc)
                    _worth = None
                if _worth is not None:
                    record["worthiness"] = _worth
                    _memory_point = _worth.get("decision") == "memory_point"
                    record["memory_point"] = bool(_memory_point)
                    if _worth.get("decision") == "skip":
                        logger.info("[biocore] event below worthiness floor: %s W=%.3f reason=%s",
                                    title, _worth.get("W", 0.0), _worth.get("reason", ""))
                        continue
                self._append_event_archive(record)
                if _memory_point:
                    _digest_event_ids.append(record.get("id"))
                    if core is not None:
                        try:
                            core.integrate_noise("event_summary", attention=0.005)
                        except Exception:
                            pass
                logger.info("[biocore] deterministic event archived: %s score=%.2f mp=%s",
                            title, score, _memory_point)
        except Exception as exc:
            logger.warning("[biocore] deterministic event ranking failed: %s", exc)
        try:
            if core is not None:
                core.update_daily_digest(event_ids=_digest_event_ids)
        except Exception:
            pass
        await self._maybe_archive_insight(event, core, "event_archive")

    async def _archive_ranked_events(self, event, core, entries):
        """Deterministic embedding/rule event extraction (LLM is never used here).

        The event_ranking switch merely enables/disables this local pipeline;
        event summarization stays a separate optional function (event_summary).
        """
        if not entries:
            return
        if not self._llm_allowed("event_ranking"):
            return
        await self._archive_ranked_events_deterministic(event, core, entries)

    async def _archive_strong_event(self, event, core, texts, summary, attachments=None, origin=None):
        if core is None:
            return
        intensity = float(core._intensity())
        strong = (intensity >= 0.35 or abs(float(core.v)) >= 0.40 or
                  float(core.a) >= 0.75 or float(core.stress) >= 0.65 or
                  (abs(float(core.v)) >= 0.28 and float(core.a) >= 0.60))
        if not strong or not texts:
            return
        if not self._llm_allowed("event_summary"):
            return
        texts = [self._mask_if_safety(t) for t in texts if str(t).strip()]
        try:
            provider = await self._provider_for("event_summary", event)
            if provider is None:
                return
            prompt = interpretation.event_summary_prompt(texts)
            resp = await provider.text_chat(prompt=prompt)
            raw = str(getattr(resp, "completion_text", "") or "").strip()
            data = interpretation.parse_event_summary(raw, getattr(self, "summary_max_chars", 0))
            _llm_big = str(data.get("big_summary") or "").strip()
            _llm_small = str(data.get("small_summary") or "").strip()
            title = str(data.get("title") or summary or "重要事件").strip()[:80]
            title = self._mask_if_safety(title)
            ev = self._mask_if_safety(self._summary_cap(str(data.get("event") or summary or "").strip()))
            big_summary = self._mask_if_safety(self._summary_cap(
                str(_llm_big or ev or summary or "").strip()))
            small_summary = self._mask_if_safety(
                str(_llm_small or big_summary or ev).strip())[:80]
            summary_status = "llm" if (_llm_big or _llm_small) else "fallback"
            meaning = self._mask_if_safety(self._summary_cap(str(data.get("meaning_to_her") or "").strip()))
            reflection = self._mask_if_safety(self._summary_cap(str(data.get("reflection") or "").strip()))
            if not ev:
                return
            _prov = self._event_provenance(event, None, ts=time.time())
            _check = self._source_check(ev, texts, provenance=_prov, record_ts=_prov.get("ts"))
            _ekey = self._normalize_event_key(title, title)
            _conf = round(max(0.2, min(1.0, 0.55 + 0.45 * float(_check.get("overlap", 0)))), 3)
            record = {
                "id": "evt_" + str(int(time.time())) + "_" + str(abs(hash(summary)) % 100000),
                "ts": time.time(),
                "session": str(getattr(event, "unified_msg_origin", "") or ""),
                "title": title,
                "event": ev,
                "big_summary": big_summary,
                "small_summary": small_summary,
                "summary_status": summary_status,
                "event_key": _ekey,
                "meaning_to_her": meaning,
                "reflection": reflection,
                "emotion": str(core.labels.get("emotion") or "neutral"),
                "emotion_secondary": self._secondary_emotion(core),
                "emotion_nuance": self._normalize_emotion_nuance(
                    data.get("emotion_nuance")),
                "emotion_layers": (interpretation.clean_emotion_layers(
                    data.get("emotion_layers")) or None),
                "emotion_layers_source": ("summary"
                    if interpretation.clean_emotion_layers(
                        data.get("emotion_layers")) else ""),
                "emotion_intensity": self._event_emotion_intensity(core),
                "importance": round(max(0.5, min(1.0, intensity)), 3),
                "appraisal": dict(core.appraisal),
                "confidence": _conf,
                "source_count": len(texts),
                "source_check": _check,
                "provenance": _prov,
                "attachments": (attachments or [])[:20],
                "modalities": sorted(set(["图片"] if any(a.get("type") == "image" for a in (attachments or [])) else []) | set(["语音"] if any(a.get("type") == "voice" for a in (attachments or [])) else [])),
                "recall_count": 0,
                "last_recall": time.time(),
                "strength": round(max(0.5, min(1.0, intensity)), 3),
                "source_texts": [self._mask_if_safety(t) for t in texts[:12]],
            }
            # ams-life: this window, the people of the lines it was made from, their message ids.
            if isinstance(origin, dict):
                record["origin"] = origin
            # task-33: same worthiness gate as the deterministic path.
            _memory_point = True
            try:
                _rel = self._relationship_of(self._user_record(event))
            except Exception:
                _rel = {}
            try:
                _worth = self._event_worthiness_for(
                    record, core, _rel, text=ev, title=title)
            except Exception as exc:
                logger.warning("[biocore] worthiness failed: %s", exc)
                _worth = None
            if _worth is not None:
                record["worthiness"] = _worth
                _memory_point = _worth.get("decision") == "memory_point"
                record["memory_point"] = bool(_memory_point)
                if _worth.get("decision") == "skip":
                    logger.info("[biocore] strong event below worthiness floor: %s W=%.3f",
                                title, _worth.get("W", 0.0))
                    return
            _dup = self._find_any_duplicate_event(record.get("session") or "", _ekey, ev,
                                                 record.get("ts") or time.time())
            if _dup is not None:
                record["duplicate_of"] = str(_dup.get("id") or "")
                self._merge_archive_duplicate(_dup, record)
                return
            _bnd = self._event_boundary(record.get("session") or "", ev, record.get("ts") or time.time())
            record["boundary_score"] = _bnd.get("boundary_score", 0.0)
            record["parent_event_id"] = _bnd.get("parent_event_id", "")
            self._append_event_archive(record)
            if core is not None:
                try:
                    core.integrate_noise("event_summary", attention=0.005)
                except Exception:
                    pass
            await self._maybe_archive_insight(event, core, "event_archive")
            try:
                if core is not None:
                    core.update_daily_digest(event_ids=[record.get("id")])
            except Exception:
                pass
            # ams-life step 1-2: the meaning and reflection stay in the event record as
            # material; whether they go into her notebook is hers to decide at night.
            logger.info("[biocore] strong event archived: %s mp=%s", title, _memory_point)
        except Exception as exc:
            logger.warning("[biocore] strong event summary failed: %s", exc)

    async def _maybe_archive_events(self, event, core=None):
        """Request-path hook: make deterministic event archive reachable."""
        if not self._llm_allowed("event_ranking"):
            return
        now = time.time()
        if now - float(getattr(self, "_last_event_archive", 0.0)) < 300:
            return
        try:
            doc = self._load_memory(event)
            entries = doc.get("entries") if isinstance(doc, dict) else []
            if not isinstance(entries, list) or not entries:
                return
            self._last_event_archive = now
            await self._archive_ranked_events(event, core, entries)
        except Exception as exc:
            logger.warning("[biocore] request-path event archive failed: %s", exc)

    async def _maybe_archive_strong_event(self, event, core, text=""):
        """Request-path hook: wire the single-event summary path (BUG-01)."""
        if not self._llm_allowed("event_summary"):
            return
        key = str(getattr(event, "unified_msg_origin", "") or "")
        now = time.time()
        try:
            last_map = getattr(self, "_last_strong_event_summary", None)
            if not isinstance(last_map, dict):
                last_map = {}
                self._last_strong_event_summary = last_map
            if now - float(last_map.get(key, 0.0) or 0.0) < 600:
                return
            # ams-life: the latest lines of this window only (anyone's), never another chat's.
            lines = self._window_lines(event, 6)
            texts = [str(h.get("text") or "").strip() for h in lines]
            origins = [discretion.origin_of(h) for h in lines]
            if str(text or "").strip():
                texts.append(str(text).strip())
                origins.append(self._event_origin(event))
            if not texts:
                return
            last_map[key] = now
            origin = discretion.merge(origins)
            origin = discretion.make_origin(self._here(event), origin["people"], origin["source_ids"])
            await self._archive_strong_event(event, core, texts, str(text or texts[-1])[:160], origin=origin)
        except Exception as exc:
            logger.warning("[biocore] request-path strong event failed: %s", exc)
