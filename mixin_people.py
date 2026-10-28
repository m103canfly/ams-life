# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: self model, per-user files and relationship bookkeeping."""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403


class PeopleMixin:
    def _load_self_model(self) -> dict:
        # ams-life step 1-2: her heart is only what she writes herself. Nothing is
        # preset; her notebook entries each carry an origin (see _notebook_for).
        d = {
            "who_am_i": "",
            "boundaries": [],
            "consistency": [],
            "narrative": "",
            "narrative_items": [],
            "notebook": [],
            "notebook_night": {},       # tonight's sittings tried (a failed try counts) and changes made
            "digest_night": {},         # tonight's windows gone over (by a hash of each; a failed try counts)
            "heart": 1,
            "version": 0,
            "_history": [],
        }
        try:
            if SELF_MODEL_PATH.exists():
                raw = json.loads(SELF_MODEL_PATH.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    cleared = raw.get("heart") != 1
                    if cleared:
                        raw = self._clear_written_for_her(raw)
                    for k in d:
                        if k in raw:
                            d[k] = raw[k]
                    d["heart"] = 1
                    if cleared:
                        self.self_model = d
                        self._save_self_model()
        except Exception as exc:
            logger.warning("[ams-life] self model load failed: %s", exc)
        try:
            if not SELF_MODEL_PATH.exists():
                self.self_model = d
                self._save_self_model()
        except Exception:
            pass
        return d

    @staticmethod
    def _clear_written_for_her(raw: dict) -> dict:
        """Once (step 1-2): the old file is kept as self_model.before_heart.json; the
        preset sentences (word for word), the narrative the event summaries wrote, the
        diary and the edit history are cleared. What anyone else wrote stays."""
        try:
            kept = SELF_MODEL_PATH.with_name("self_model.before_heart.json")
            if not kept.exists():
                shutil.copy2(str(SELF_MODEL_PATH), str(kept))
        except Exception as exc:
            logger.warning("[ams-life] self model archive failed: %s", exc)
            raise
        out = dict(raw)
        if str(out.get("who_am_i") or "") == PRESET_SELF["who_am_i"]:
            out["who_am_i"] = ""
        for key in ("boundaries", "consistency"):
            out[key] = [x for x in (out.get(key) or []) if x not in PRESET_SELF[key]]
        out["narrative"] = ""
        out["narrative_items"] = []
        out["diary"] = []
        out["_history"] = []
        return out

    def _save_night_marks(self) -> None:
        """Only tonight's marks (windows gone over, notebook sittings tried), into the file as it
        is: written even when the registry cannot be read, so a restart does not call again."""
        try:
            raw = json.loads(SELF_MODEL_PATH.read_text(encoding="utf-8")) if SELF_MODEL_PATH.exists() else {}
            if not isinstance(raw, dict):
                return
            for key in ("digest_night", "notebook_night"):
                if key in (self.self_model or {}):
                    raw[key] = self.self_model[key]
            SELF_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            tmp = SELF_MODEL_PATH.with_suffix(".tmp")
            tmp.write_text(json.dumps(raw, ensure_ascii=False, indent=1), encoding="utf-8")
            atomic_file.replace(tmp, SELF_MODEL_PATH)
        except Exception as exc:
            logger.warning("[ams-life] night marks not written: %s", exc)

    def _save_self_model(self) -> None:
        try:
            # ams-life: nothing the forget registry rules out stays in her notes; when the
            # registry cannot be read, nothing is written this time (nothing is dropped)
            try:
                _kept = {_key: [x for x in self.self_model[_key] if self._origin_kept(x) and not (
                                     isinstance(x, dict) and self._red_line(x.get("text"), "notes"))]
                         for _key in ("notebook", "narrative_items", "diary", "relationship_narratives")
                         if isinstance(self.self_model.get(_key), list)}
            except forget_registry.Unreadable as exc:
                logger.warning("[ams-life] forget registry unreadable, self model not written: %s", exc)
                self._save_night_marks()
                return
            SELF_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            self.self_model["version"] = int(self.self_model.get("version", 0) or 0) + 1
            _h = list(self.self_model.get("_history") or [])[-20:]
            _h.append({"ts": __import__("time").time(),
                       "who_am_i": self.self_model.get("who_am_i", ""),
                       "notebook": len(self.self_model.get("notebook") or [])})
            self.self_model["_history"] = _h[-20:]
            self.self_model.update(_kept)
            SELF_MODEL_PATH.write_text(json.dumps(self.self_model, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception:
            pass

    def _user_path(self, event) -> Path:
        sid, _ = self._speaker(event)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in (sid or "unknown"))[:60]
        return USER_DIR / (safe + ".json")

    def _we_memory_candidates(self, entries) -> list:
        """Deterministic, evidence-gated we-memory proposals (default off)."""
        out = []
        patterns = (
            ("nickname", ("叫你", "喊你", "外号", "昵称")),
            ("ritual", ("每天", "每次", "习惯", "约好", "固定")),
            ("anniversary", ("纪念日", "周年", "第一次")),
            ("inside_joke", ("梗", "暗号", "约定")),
            ("shared_object", ("我们的", "一起买", "一起做", "送给")),
        )
        for entry in (entries if isinstance(entries, list) else [])[-100:]:
            if not isinstance(entry, dict):
                continue
            text = str(entry.get("text") or "").strip()
            if not text:
                continue
            for mtype, words in patterns:
                if not any(w in text for w in words):
                    continue
                snippet = text[:40]
                out.append({"type": mtype, "text": snippet, "confidence": 0.6,
                            "evidence_refs": [str(entry.get("id") or entry.get("ts") or "m")[:80]]})
                break
        return relationship_meta.merge_we_memory([], out)

    def _touch_user(self, event, core=None) -> dict:
        try:
            sid, name = self._speaker(event)
            USER_DIR.mkdir(parents=True, exist_ok=True)
            path = self._user_path(event)
            d = {}
            if path.exists():
                try:
                    d = json.loads(path.read_text(encoding="utf-8"))
                except Exception:
                    d = {}
            d["sender_id"] = sid
            d["sender_name"] = name or d.get("sender_name", "")
            # ams-life: every name he has gone by (group cards differ), for anonymizing
            _names = [str(x) for x in (d.get("names") or []) if str(x or "").strip()]
            if name and name not in _names:
                _names.append(name)
            d["names"] = _names[-20:]
            try:
                _prev_last_seen = float(d.get("last_seen", 0) or 0)
            except Exception:
                _prev_last_seen = 0.0
            d["interactions"] = int(d.get("interactions", 0) or 0) + 1
            _now_seen = time.time()
            d["absence"] = relationship_meta.absence_state(_prev_last_seen, _now_seen)
            d["last_seen"] = _now_seen
            d.setdefault("first_seen", time.time())
            _session_key = str(getattr(event, "unified_msg_origin", "") or "").strip()
            if _session_key:
                _sessions = d.get("sessions") if isinstance(d.get("sessions"), list) else []
                _sessions = [str(x) for x in _sessions if str(x) and str(x) != _session_key]
                d["sessions"] = (_sessions[-19:] + [_session_key])[-20:]
            try:
                _ct = float(getattr(core, "trust", 0.5)) if core is not None else 0.5
                _old_trust = float(d.get("trust", 0.5) or 0.5)
                if core is not None and getattr(core, "bio_learning", False):
                    # Nassar 2010 adaptive alpha for the trust EMA.
                    _alpha = memory_meta.nassar_alpha(_ct - _old_trust)
                else:
                    _alpha = 0.30
                d["trust"] = round(_old_trust + _alpha * (_ct - _old_trust), 3)
            except Exception:
                d["trust"] = d.get("trust", 0.5)
            try:
                _prev_rel = d.get("relationship") if isinstance(d.get("relationship"), dict) else {}
                _prev_state = _prev_rel.get("state") if isinstance(_prev_rel.get("state"), dict) else None
                _opp = getattr(core, "opponent", {}) if core is not None else {}
                _opp_v = _opp.get("v", 0.0) if isinstance(_opp, dict) else 0.0
                _rel_state = relationship_meta.relationship_state(
                    trust=d.get("trust", 0.5),
                    social=getattr(core, "social", 0.5) if core is not None else 0.5,
                    stress=getattr(core, "stress", 0.5) if core is not None else 0.5,
                    opponent=_opp_v,
                    previous=_prev_state,
                )
                _mem_doc = self._load_memory(event)
                _entries = _mem_doc.get("entries") if isinstance(_mem_doc, dict) else []
                try:
                    _social_world = relationship_meta.build_social_world(_entries)
                except Exception:
                    _social_world = []
                _we_memory = []
                try:
                    if getattr(self, "we_memory_enabled", False):
                        _we_memory = self._we_memory_candidates(_entries)
                except Exception:
                    _we_memory = []
                _milestones = []
                try:
                    for _ev in self._visible_events(event, self._event_archive(20)):
                        _mk = relationship_meta.milestone_from_text(
                            str(_ev.get("title") or "") + " " + str(_ev.get("event") or ""))
                        if _mk:
                            _mk["ts"] = float(_ev.get("ts", 0) or 0)
                            # the messages it came from: deleting one of them deletes it
                            _mk["source_ids"] = discretion.origin_of(_ev)["source_ids"]
                            _milestones.append(_mk)
                except Exception:
                    _milestones = []
                d["relationship"] = relationship_meta.update_relationship_record(
                    _prev_rel,
                    state=_rel_state,
                    ts=d.get("last_seen", time.time()),
                    transactive_map=relationship_meta.build_transactive_map(_entries),
                    destination_map=relationship_meta.build_destination_map(_entries),
                    absence=d.get("absence"),
                    social_world=_social_world,
                    milestones=_milestones,
                    we_memory=_we_memory,
                    interactions=d.get("interactions", 0),
                    repair_success=int((_prev_rel.get("repair_state") or {}).get("repair_attempts", 0) or 0),
                    promises_kept=len([x for x in _milestones if x.get("type") == "promise_kept"]),
                    annotations=(_prev_rel.get("annotations")
                                 if isinstance(_prev_rel.get("annotations"), list) else None),
                )
                if core is not None:
                    # Task-15: relationship delta feeds L1 social/valence noise.
                    try:
                        _rel_now = d.get("relationship") if isinstance(d.get("relationship"), dict) else {}
                        _rel_st = _rel_now.get("state") if isinstance(_rel_now.get("state"), dict) else {}
                        core.integrate_noise(
                            "relationship",
                            social=0.004 * (float(_rel_st.get("closeness", 0.5) or 0.5) - 0.5),
                            valence=0.004 * (float(_rel_st.get("trust", 0.5) or 0.5) - 0.5))
                    except Exception:
                        pass
            except Exception:
                pass
            if not self._job_stale():
                path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            return d
        except Exception:
            return {}
