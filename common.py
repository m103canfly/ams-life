# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""Shared module-level code split out of main.py unchanged: imports, data paths, constants,
helper functions and the autonomy send target. Other modules do `from .common import *`."""
from __future__ import annotations

import json
import math
import re
import os
import shutil
import asyncio
import base64
import io
import http.client
import socket
import ssl
import subprocess
import time
import types
import urllib.request
import zipfile
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urlparse

from astrbot.api import logger
from astrbot.api.event import filter, AstrMessageEvent, MessageChain, MessageEventResult
from astrbot.api.message_components import Image, Plain, Reply, Record
from astrbot.api.provider import ProviderRequest, LLMResponse
from astrbot.api.star import Context, Star, register

try:
    from . import interpretation
except Exception:
    import interpretation

try:
    from . import memory_meta
except Exception:
    import memory_meta

try:
    from . import relationship_meta
except Exception:
    import relationship_meta
try:
    from . import discretion
except Exception:
    import discretion
try:
    from . import homeostasis
except Exception:
    import homeostasis
try:
    from . import forget_registry
except Exception:
    import forget_registry
try:
    from . import vector_store
except Exception:
    import vector_store
try:
    from . import redline
except Exception:
    import redline

HER_NAME = "小爱"   # what an @ of her becomes in what she keeps

PLUGIN_DIR = Path(__file__).resolve().parent
_LEGACY_DATA_DIR = PLUGIN_DIR / "data"
_BASE_DATA_DIR = PLUGIN_DIR.parents[1] if len(PLUGIN_DIR.parents) > 1 else PLUGIN_DIR
_PERSIST_DATA_DIR = _BASE_DATA_DIR / "plugin_data" / "astrbot_plugin_ams_life"


def _init_data_dir() -> Path:
    target = Path(os.getenv("AMS_LIFE_DATA_DIR") or os.getenv("BIOCORE_DATA_DIR") or str(_PERSIST_DATA_DIR))
    target.mkdir(parents=True, exist_ok=True)
    try:
        if _LEGACY_DATA_DIR.exists() and target.resolve() != _LEGACY_DATA_DIR.resolve():
            for src in _LEGACY_DATA_DIR.rglob("*"):
                if not src.is_file():
                    continue
                rel = src.relative_to(_LEGACY_DATA_DIR)
                dst = target / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists():
                    shutil.copy2(src, dst)
    except Exception:
        pass
    return target


DATA_DIR = _init_data_dir()
PROFILE_PATH = DATA_DIR / "persona_profile.json"
API_CONFIG_PATH = DATA_DIR / "api_config.json"
STATE_DIR = DATA_DIR / "states"
MEMORY_DIR = DATA_DIR / "memory"
# ams-life: one her. One body state and one memory library for every group and
# private chat; the per-session files of BioCore are moved aside on first start.
HER_STATE_PATH = STATE_DIR / "her.json"
STATE_ARCHIVE_DIR = STATE_DIR / "per_session_archive"
MEMORY_LIBRARY_PATH = MEMORY_DIR / "library.json"
MEMORY_LEGACY_DIR = MEMORY_DIR / "per_session_legacy"
# ams-life step 1-3: vectors live next to the library, one row per memory id; the
# library as it was before a migration is copied into MEMORY_ARCHIVE_DIR (never deleted).
MEMORY_VECTOR_PATH = MEMORY_DIR / vector_store.FILE_NAME
MEMORY_ARCHIVE_DIR = MEMORY_DIR / "archive"
# who and what she must not keep: the old companion's forget list, and the owner's
# deletions from the panel (no one can make her forget by a chat command)
FORGET_REGISTRY_PATH = DATA_DIR / forget_registry.FILE_NAME
REDLINE_COUNTS_PATH = DATA_DIR / "redline_counts.json"   # red-line hits by line: numbers only, never text
# ams-life: her phone. Every group and private chat is one window; what was
# said there (her recent replies, open loops) is kept only in that window.
# The body keeps no text at all.
PHONE_DIR = DATA_DIR / "phone"
# Local image service paths/port are configured through _conf_schema.json.
# There are no machine-specific fallback paths baked into the plugin.
IMAGE_CACHE_PATH = DATA_DIR / "image_cache.json"
EVENT_ARCHIVE_DIR = DATA_DIR / "archives"
EVENT_SESSION_DIR = EVENT_ARCHIVE_DIR / "sessions"
EVENT_ARCHIVE_PATH = EVENT_ARCHIVE_DIR / "events.jsonl"
def canonical_session_key(raw) -> str:
    """Canonical session identity: platform:Type:id (colon form).

    Event archive keys use colons ("default:FriendMessage:123"), memory file
    stems use underscores ("default_FriendMessage_123"); both must compare
    equal for dedupe/dropdown unions (task-55/task-56). Mixed separators
    ("default:GroupMessage_664") and platform prefixes with underscores are
    accepted; ids are kept verbatim.
    """
    text = str(raw or "").strip()
    if not text:
        return ""
    match = re.search(
        r"(FriendMessage|GroupMessage|GuildMessage|TempMessage|OtherMessage)",
        text)
    if match:
        platform = text[:match.start()].strip(":_") or "default"
        ident = text[match.end():].strip(":_")
        return platform + ":" + match.group(1) + ":" + ident
    return text.replace("_", ":")


def event_effective_time(record) -> float:
    """Best-effort real event time for duplicate detection (task-56).

    A re-archived event may carry the archive time in ``ts`` while its
    ``time_span`` still points at the original conversation. Dedupe must
    compare the real event time, not the archival moment, or a re-archive
    days later looks like a different event.
    """
    if not isinstance(record, dict):
        return 0.0
    try:
        span = record.get("time_span")
        if isinstance(span, dict):
            for key in ("end_ts", "start_ts"):
                try:
                    value = float(span.get(key) or 0)
                except Exception:
                    value = 0.0
                if value > 0:
                    return value
        return float(record.get("ts", 0) or 0)
    except Exception:
        return 0.0


EVENT_SUMMARY_ACTIONS = ("regenerate", "update")
MEMORY_POINT_FEEDBACK_ACTIONS = ("important", "unimportant", "edit_label", "restore")
EVENT_SUMMARY_HARD_MAX = 20000
EVENT_SUMMARY_SMALL_MAX = 80
EVENT_SUMMARY_HISTORY_MAX = 20
USER_DIR = DATA_DIR / "users"
SELF_MODEL_PATH = DATA_DIR / "self_model.json"
OWNER_RULES_PATH = DATA_DIR / "owner_rules.json"
INSIGHT_ARCHIVE_PATH = EVENT_ARCHIVE_DIR / "insights.jsonl"
# M3/M4 embedding infrastructure (registered in
# docs/BIOCORE-ENGINEERING-APPROX-v1.md, "C-S1/C-S2" table): the cache key and
# the request payload share ONE truncation, the cache is a bounded process-local
# LRU, and a slow provider degrades to "no embedding" at a configurable timeout
# (embedding_timeout_ms, default 1500 ms) instead of blocking the reply loop.
# 300 ms is only appropriate once caller-side latency p95 is measured <200 ms.
EMBED_TEXT_MAX_CHARS = 2000
EMBED_CACHE_MAX = 512
EMBED_TIMEOUT_MS_DEFAULT = 1500
EMBED_TIMEOUT_S = EMBED_TIMEOUT_MS_DEFAULT / 1000.0  # seconds, legacy convenience
EMBED_CACHE = OrderedDict()
# C-S1 sentence dedup: deterministic char-bigram Jaccard threshold. The LIT's
# embedding-0.90 path and quote/code-block whitelist are NOT implemented (M5);
# this constant is the only live dedup threshold.
SENTENCE_DEDUP_THRESHOLD = 0.92

# Memory doc schema version: bumped when entry fields/migrations change.
# Old docs are upgraded lazily on load (additive defaults only).
MEMORY_SCHEMA_VERSION = 2

DEFAULT_PROFILE = {
    "O": 0.62, "C": 0.55, "E": 0.44, "A": 0.42, "N": 0.40,
    "stress_reactivity": 0.45, "recovery_rate": 0.62,
    "social_baseline": 0.44, "energy_baseline": 0.55,
    "curiosity_baseline": 0.60, "safety_baseline": 0.55,
    "da_baseline": 0.55, "oa_baseline": 0.40, "ht_baseline": 0.35,
    "autonomy_gain": 1.0, "contagion_gain": 0.10, "baseline_v": 0.05, "baseline_a": 0.40,
}

# ams-life: her own urges (numbers only; see BioCore.record_talk / be_seen).
TALKED_HALF_LIFE_MIN = 240.0   # having talked a lot fades by half in 4 hours
SEEN_HALF_LIFE_MIN = 360.0     # wanting to be seen grows halfway back to 1 in 6 hours
SEEN_RELIEF = 0.4              # someone answering her keeps 40% of it
AMBIENT_WINDOW_SECONDS = 1800  # how lively the chats are: others' messages in the last 30 minutes
AMBIENT_BUSY_COUNT = 30        # ... this many or more is as lively as it gets
# Her heart (step 1-2): only what she writes herself, in her notebook.
NOTEBOOK_MAX = 20              # entries
NOTEBOOK_CHARS = 40            # characters per entry
NOTEBOOK_EDITS = 3             # changes per night in all sittings (add / edit / delete)
NOTEBOOK_PRIVATE_MAX = 3       # private chats she writes about a night (the busiest)
OWNER_RULES_MAX = 10           # the owner's rules (written in the panel, shown everywhere)
OWNER_RULES_CHARS = 100
# The sentences BioCore wrote for her; cleared, her heart is not written for her.
PRESET_SELF = {"who_am_i": "一个会持续受聊天影响、但不会被单条消息完全定义的角色。",
               "boundaries": ["不接受被当作没有感受的工具", "不会被一次互动改写全部立场"],
               "consistency": ["情绪会变，但核心立场不因单次互动翻转"]}

# D5: stable default shape for the page-status memory-trace projection.
DEFAULT_MEMORY_TRACE = {"count": 0, "valence": 0.0, "stress_delta": 0.0, "entry_ids": []}


# Task-15: noise -> autonomy (L1 computes; default OFF, private chat only).
NOISE_CLAMP = 0.30
AUTONOMY_ENTER = 0.72  # hysteresis: enter ready
AUTONOMY_EXIT = 0.60  # hysteresis: stay ready until below this
AUTONOMY_WEIGHTS = {
    "chaos": 0.22, "echo": 0.16, "stress_load": 0.18,
    "drive_dev": 0.16, "distrust": 0.14, "distance": 0.14,
}
AUTONOMY_THRESHOLD_MIN = 0.55
AUTONOMY_THRESHOLD_MAX = 0.90
AUTONOMY_MAX_CHARS_MIN = 60
AUTONOMY_MAX_CHARS_MAX = 240
AUTONOMY_COOLDOWN_SECONDS = 30 * 60
AUTONOMY_DAILY_CAP = 3
AUTONOMY_QUIET_START_HOUR = 0
AUTONOMY_QUIET_END_HOUR = 8
AUTONOMY_TICK_SECONDS = 300  # P0-1: autonomous generator interval (>=5min)

# Task-28: minimal autonomy loop (default OFF, private-only, token-only).
# Deterministic arbiter INSPIRED BY (not an implementation of) the papers below;
# it is NOT a global-workspace/consciousness implementation.
#   competition: Desimone & Duncan 1995 10.1146/annurev.ne.18.030195.001205;
#                Itti & Koch 2001 10.1038/35058500; Itti et al. 1998 10.1109/34.730558 (WTA+IOR)
#   goal gradient: Hull 1932 10.1037/h0072640; Kivetz 2006 10.1509/jmkr.43.1.39;
#                Koo & Fishbach 2010 10.1037/a0019443
#   delay discount: Mazur 1987 (book chapter, no DOI) + Green & Myerson 2004
#                10.1037/0033-2909.130.5.769
#   effort cost: Shenhav 2013 10.1016/j.neuron.2013.07.007; Kool & Botvinick 2014
#                10.1037/a0031048; Westbrook & Braver 2013 10.1017/s0140525x13001179
#   broadcast: Baars 1988 (book, no DOI); Dehaene & Naccache 2001
#                10.1016/S0010-0277(00)00123-2; Dehaene et al. 1998 10.1073/pnas.95.24.14529;
#                Mashour et al. 2020 10.1016/j.neuron.2020.01.026
AUTONOMY_LOOP_MODES = ("reach_out", "explore", "engage", "wait", "share", "withdraw")
AUTONOMY_LOOP_WEIGHTS = {"novelty": 0.20, "goal": 0.25, "relation": 0.20,
                         "affect": 0.20, "noise": 0.15}
AUTONOMY_LOOP_CANDIDATE_MAX = 6
AUTONOMY_LOOP_THETA_MIN = 0.35
AUTONOMY_LOOP_THETA_MAX = 0.55
AUTONOMY_LOOP_THETA_IG = 0.45
AUTONOMY_LOOP_MARGIN_MIN = 0.05
AUTONOMY_LOOP_MARGIN_MAX = 0.15
AUTONOMY_LOOP_MARGIN = 0.08
AUTONOMY_LOOP_K_MIN = 0.001
AUTONOMY_LOOP_K_MAX = 0.10
AUTONOMY_LOOP_K_DELAY = 0.02       # hyperbolic discount k per minute
AUTONOMY_LOOP_IOR_MIN = 300.0
AUTONOMY_LOOP_IOR_MAX = 1800.0
AUTONOMY_LOOP_IOR_SECONDS = 600.0  # return-inhibition recovery tau
AUTONOMY_LOOP_REFRACTORY_SECONDS = 60.0
AUTONOMY_LOOP_C0 = 0.05
AUTONOMY_LOOP_C1 = 0.20
AUTONOMY_LOOP_C2 = 0.15
AUTONOMY_LOOP_DEBT_STEP = 0.15
AUTONOMY_LOOP_DEBT_RECOVERY = 0.02
AUTONOMY_LOOP_DEBT_MAX = 0.60
AUTONOMY_LOOP_VALUE_MIN = -0.5
AUTONOMY_LOOP_VALUE_MAX = 1.0
AUTONOMY_LOOP_EMA_KEEP = 0.7
AUTONOMY_LOOP_WORKSPACE_MAX = 16
AUTONOMY_LOOP_EFFORT = {"reach_out": 0.5, "explore": 0.4, "engage": 0.6,
                        "share": 0.3, "withdraw": 0.3, "wait": 0.05}

# Task-20 batch3 L1 learning (Daw 2011 10.1016/j.neuron.2011.02.027;
# Nassar 2010 10.1523/JNEUROSCI.0822-10.2010; Wixted 1991).
LEARNING_Q_ALPHA = 0.20
LEARNING_Q_WEIGHT = 0.05
LEARNING_RETENTION_MODELS = ("power_law", "multi_scale", "single")

# Per-function LLM routing: each feature has its own enabled switch and a
# provider choice ("follow_llm" = AstrBot main chat model, or a provider_id).
# Defaults: only the two summary functions are enabled; everything else is
# opt-in. This replaces the single llm_only_reply_summary master switch while
# keeping it readable for legacy migration.
LLM_FUNCTIONS = (
    "persona_compile",
    "event_summary",
    "event_ranking",
    "insight",
    "memory_summary",
    "image_caption",
    # L-T01..L-T12: proposal-only LLM functions, all OFF by default. Each one
    # is routed through _provider_for and its prompt/parser lives in
    # interpretation.py; model output never writes biological state directly.
    "relationship_impression",
    "repair_hint",
    "empathy_hint",
    "pragmatics_hint",
    "tom_probe",
    "notebook",
    "relationship_narrative",
    "humor_hint",
    # ams-life step 1-3: the group members she knows, once a night per group
    "group_impressions",
)
LLM_FUNCTION_DEFAULTS = {
    "persona_compile": False,
    "event_summary": True,
    "event_ranking": True,
    "insight": False,
    "memory_summary": True,
    "image_caption": False,
    "relationship_impression": False,
    "repair_hint": False,
    "empathy_hint": False,
    "pragmatics_hint": False,
    "tom_probe": False,
    "notebook": False,
    "relationship_narrative": False,
    "humor_hint": False,
    "group_impressions": False,
}
INSIGHT_MIN_NEW_EVENTS = 3
INSIGHT_COOLDOWN_SECONDS = 60 * 60
INSIGHT_FALLBACK_HOURS = 24

LLM_FUNCTION_ALIASES = {
    "persona": "persona_compile",
    "ranking": "event_ranking",
    "caption": "image_caption",
    "summary": "event_summary",
    "impression": "relationship_impression",
    "repair": "repair_hint",
    "empathy": "empathy_hint",
    "pragmatics": "pragmatics_hint",
    "tom": "tom_probe",
    "diary": "notebook",
    "narrative": "relationship_narrative",
    "humor": "humor_hint",
}

# L-T01..L-T12 cooldowns (seconds); all functions stay OFF by default.
LLM_V2_COOLDOWNS = {
    "relationship_impression": 3600,
    "repair_hint": 900,
    "empathy_hint": 900,
    "pragmatics_hint": 900,
    "tom_probe": 600,
    "relationship_narrative": 86400,
    "humor_hint": 900,
}

# ACT-R retrieval constants (Anderson & Reder 1999; partial matching per
# Anderson 1994). Keeping them in one named place makes scoring tunable.
ACT_R_DECAY = 0.5
RETRIEVAL_THRESHOLD = 0.25
PARTIAL_MATCH_THRESHOLD = 0.35

# A4 continuity opener: inject "last talk" only when the user returns after a
# break, so the same-session turns and first-ever turns stay untouched.
A4_CONTINUITY_GAP_SECONDS = 600.0
A4_CONTINUITY_MAX_LOOPS = 2

# Zacks et al. (2007) event segmentation: a boundary is predicted by elapsed
# time and by the content change since the previous event in the same session.
EVENT_BOUNDARY_WINDOW_SECONDS = 1800.0
EVENT_BOUNDARY_TIME_WEIGHT = 0.62
EVENT_BOUNDARY_TEXT_WEIGHT = 0.38
EVENT_BOUNDARY_PARENT_THRESHOLD = 0.5

# Gross process model: cost paid by each regulation strategy (0..1 scale,
# distraction pays the highest bill because it leaves the concern unaddressed).
REGULATION_COST = {
    "seek_comfort": 0.003,
    "reappraise": 0.002,
    "suppress": 0.010,
    "avoid": 0.004,
    "express": 0.002,
    "distraction": 0.006,
    # Batch4 B2: affect labeling is the 7th, lowest-cost strategy.
    "label_emotion": 0.001,
}

# Batch4 A1: sensitization (dual of habituation): strong negative stimuli
# repeated within the decay window give a bounded gain, half-life 24h.
SENSITIZATION_STRONG_NEG_DV = -0.12
SENSITIZATION_STEP = 0.15
SENSITIZATION_MAX = 1.25
SENSITIZATION_HALF_LIFE_HOURS = 24.0
SENSITIZATION_HISTORY_MAX = 12
SENSITIZATION_HISTORY_MAX_AGE = 2 * 86400.0

# Batch4 B2: affect-labeling trigger thresholds (deterministic).
AFFECT_LABEL_MIN_TOP_P = 0.60
AFFECT_LABEL_MIN_AROUSAL = 0.60
# Low-cost strategy should not be picked every tick; deterministic cooldown.
AFFECT_LABEL_COOLDOWN_SECONDS = 600

# Batch4 B4: contextual recovery-speed multiplier bounds.
RECOVERY_CONTEXT_MIN = 0.8
RECOVERY_CONTEXT_MAX = 1.2

# G4: regulation-strategy statistics carry a recency weight so evidence from a
# strategy that has not been used for a long time counts less when choosing.
REGULATION_STATS_HALF_LIFE_DAYS = 10.0

# Mem0 UPDATE matching: an explicit correction ("改成/改为/其实是/更正")
# only updates a memory whose semantic similarity passes this floor; the
# exact-duplicate threshold (0.93) alone is too strict for corrections.
MEMORY_UPDATE_MATCH_THRESHOLD = 0.55

# Event-key identity: normalized keys within this window and above this
# similarity are treated as the same archived event (duplicates are merged).
EVENT_KEY_SIM_THRESHOLD = 0.82
EVENT_DUP_WINDOW_SECONDS = 21600.0
# One-time canonical cleanup compares the *real* event time (time_span) and may
# need to span the archival gap between ":"/"_" key generations (task-56).
EVENT_DEDUPE_CLEANUP_WINDOW = 7 * 86400.0

# Cowen & Keltner (2017) prototype space: which EMOTION_SPECTRUM anchors a
# basic emotion label may calibrate from this core's own state history.
SPECTRUM_FAMILY = {
    "joy": ("joy", "amusement", "contentment", "excitement", "pride", "adoration", "admiration"),
    "sadness": ("disappointment", "empathic_pain", "nostalgia", "guilt"),
    "anger": ("anger", "contempt", "disgust"),
    "fear": ("fear", "anxiety", "horror"),
    "loneliness": ("empathic_pain", "disappointment", "nostalgia"),
}

LEX = {
    "sadness": ("难过", "伤心", "委屈", "哭", "失望", "累", "撑不住"),
    "anger": ("生气", "烦", "气死", "骂", "傻逼", "滚", "恶心", "废物", "垃圾", "讨厌", "闭嘴", "没用", "蠢", "去死"),
    "fear": ("怕", "焦虑", "紧张", "担心", "失眠", "慌"),
    "joy": ("开心", "高兴", "喜欢", "好耶", "笑死", "可爱", "谢谢"),
    "loneliness": ("孤独", "一个人", "没人", "空虚"),
}


LEX["sadness"] += ("难受", "委屈", "失落", "低落")
LEX["anger"] += ("烦", "别烦", "闭嘴", "滚", "讨厌", "气人")
LEX["fear"] += ("慌", "不安", "怕", "紧张")
LEX["loneliness"] += ("丢下", "被丢下", "冷落", "忽视", "没人理", "不理我", "抛弃", "一个人", "孤单")


def _sha256(text: str) -> str:
    import hashlib
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()[:32]


def _clip(x, lo=-1.0, hi=1.0):
    try:
        return max(lo, min(hi, float(x)))
    except Exception:
        return lo


def _memory_entry_id_of(entry) -> str:
    """Stable per-entry id shared by the memory API and the dashboard index."""
    if not isinstance(entry, dict):
        return ""
    eid = str(entry.get("id") or "").strip()
    if eid:
        return eid
    text = str(entry.get("text") or "").strip()
    return _sha256(text[:300])[:12] if text else ""


def _memory_index_rows(memory_dir: Path, *, max_sessions: int = 50,
                       max_entries: int = 200, max_tombstones: int = 20) -> list:
    """Read-only, bounded memory index consumed by the dashboard.

    Only contract fields are exposed. Deleted entries are omitted from the
    entries list and surfaced through tombstones (soft deletes keep a
    tombstone matching the hard-delete shape). Old entries without the new
    metadata keep neutral values instead of failing.
    """
    sessions = []
    try:
        files = sorted(Path(memory_dir).glob("*.json"),
                       key=lambda p: p.stat().st_mtime, reverse=True)
    except Exception:
        files = []
    for path in files[:max(1, int(max_sessions))]:
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        entries = doc.get("entries") if isinstance(doc.get("entries"), list) else []
        rows = []
        soft_deleted = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("deleted"):
                soft_deleted.append(entry)
                continue
            if len(rows) >= max_entries:
                continue
            try:
                ts = round(float(entry.get("ts", 0) or 0), 3)
            except Exception:
                ts = 0.0
            try:
                importance = round(float(entry.get("importance", 0.5) or 0.5), 3)
            except Exception:
                importance = 0.5
            confidence = entry.get("memory_confidence")
            try:
                confidence = round(float(confidence), 4) if confidence is not None else None
            except Exception:
                confidence = None
            destination = entry.get("destination")
            provenance = entry.get("provenance")
            rows.append({
                "id": _memory_entry_id_of(entry),
                "text": str(entry.get("text") or "")[:400],
                "role": str(entry.get("role") or ""),
                "ts": ts,
                "importance": importance,
                # S1: read-only effective values (G7/G8) for the dashboard.
                "effective_importance": memory_meta.effective_importance(entry),
                "effective_assoc": memory_meta.decayed_assoc(entry),
                "last_recall": round(float(entry.get("last_recall", 0) or 0), 3),
                "hits": int(entry.get("hits", 0) or 0),
                "memory_source": str(entry.get("memory_source") or "direct"),
                "memory_confidence": confidence,
                "legacy": not bool(entry.get("memory_source")),
                "memory_tier": str(entry.get("memory_tier") or ""),
                "conflict": bool(entry.get("conflict")),
                "last_write_op": str(entry.get("last_write_op") or ""),
                "previous_versions": [str(v)[:400] for v in (entry.get("previous_versions") or [])][-8:],
                "summarized": bool(entry.get("summarized")),
                "destination": dict(destination) if isinstance(destination, dict) else None,
                "provenance": dict(provenance) if isinstance(provenance, dict) else None,
                # Read-only extras for the orb memory-ball layer.
                "encoding_emotion": str(entry.get("encoding_emotion") or ""),
                "encoding_emotion_secondary": str(entry.get("encoding_emotion_secondary") or ""),
                "last_used": round(float(entry.get("last_used", 0) or 0), 3),
                "scope": str(entry.get("scope") or ""),
                "poison_risk": bool(entry.get("poison_risk")),
                "links": len(entry.get("links") or []),
                "self_defining": bool(entry.get("self_defining")),
                "verification": str((entry.get("verification") or {}).get("status")
                                    or memory_meta.verify_entry(entry).get("status") or "")
            })
        tombstones = []
        for item in (doc.get("tombstones") or [])[-max_tombstones:]:
            if not isinstance(item, dict):
                continue
            try:
                tomb_ts = round(float(item.get("ts", 0) or 0), 3)
            except Exception:
                tomb_ts = 0.0
            tombstones.append({
                "id": str(item.get("id") or ""),
                "ts": tomb_ts,
                "text": str(item.get("text") or "")[:200],
            })
        for entry in soft_deleted[-max_tombstones:]:
            try:
                tomb_ts = round(float(entry.get("deleted_ts") or entry.get("ts", 0) or 0), 3)
            except Exception:
                tomb_ts = 0.0
            tombstones.append({
                "id": _memory_entry_id_of(entry),
                "ts": tomb_ts,
                "text": str(entry.get("text") or "")[:200],
            })
        sessions.append({
            "session": str(path.stem),
            "entries": rows,
            "tombstones": tombstones[-max_tombstones:],
        })
    return sessions


def _relationship_rows(user_dir: Path, *, max_users: int = 50,
                       max_trajectory: int = 40) -> list:
    """Read-only, bounded relationship index consumed by the dashboard."""
    rows = []
    try:
        files = sorted(Path(user_dir).glob("*.json"),
                       key=lambda p: p.stat().st_mtime, reverse=True)
    except Exception:
        files = []
    for path in files[:max(1, int(max_users))]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        try:
            trust = float(data.get("trust", 0.5) or 0.5)
            if not math.isfinite(trust):
                raise ValueError("non-finite trust")
            trust = round(max(0.0, min(1.0, trust)), 4)
        except Exception:
            trust = 0.5
        try:
            interactions = int(data.get("interactions", 0) or 0)
        except Exception:
            interactions = 0
        try:
            last_seen = round(float(data.get("last_seen", 0) or 0), 3)
        except Exception:
            last_seen = 0.0
        rel = data.get("relationship") if isinstance(data.get("relationship"), dict) else {}
        state = rel.get("state") if isinstance(rel.get("state"), dict) else None
        if isinstance(state, dict):
            safe_state = {}
            for _key in ("trust", "closeness", "conflict", "repair", "predictability"):
                try:
                    _value = float(state.get(_key))
                    if not math.isfinite(_value):
                        raise ValueError("non-finite")
                    safe_state[_key] = round(max(0.0, min(1.0, _value)), 4)
                except Exception:
                    safe_state = {}
                    break
            state = safe_state or None
        if not isinstance(state, dict):
            try:
                state = relationship_meta.relationship_state(trust=trust)
            except Exception:
                state = {"trust": trust, "closeness": 0.5, "conflict": 0.5,
                         "repair": 0.0, "predictability": 0.5}
        trajectory = rel.get("trajectory") if isinstance(rel.get("trajectory"), list) else []
        belief = data.get("belief_state") if isinstance(data.get("belief_state"), dict) else {}
        rows.append({
            "sender_id": str(data.get("sender_id") or ""),
            "sender_name": str(data.get("sender_name") or ""),
            "interactions": interactions,
            "trust": trust,
            "last_seen": last_seen,
            # task-55: session keys from the user file feed the dashboard
            # session dropdown union (memory + events + relations + live).
            "sessions": [str(x) for x in (data.get("sessions") or [])][:20],
            "relationship": {
                "state": {key: state.get(key) for key in
                          ("trust", "closeness", "conflict", "repair", "predictability")},
                "trajectory": [dict(x) for x in trajectory[-max_trajectory:] if isinstance(x, dict)],
                "transactive_map": rel.get("transactive_map") if isinstance(rel.get("transactive_map"), dict) else {},
                "destination_map": rel.get("destination_map") if isinstance(rel.get("destination_map"), dict) else {},
                "repair_state": rel.get("repair_state") if isinstance(rel.get("repair_state"), dict) else {},
                "absence": rel.get("absence") if isinstance(rel.get("absence"), dict) else {},
                "calibration": rel.get("calibration") if isinstance(rel.get("calibration"), dict) else {},
                "social_world": [dict(x) for x in (rel.get("social_world") or [])[:20] if isinstance(x, dict)],
                "attachment": rel.get("attachment") if isinstance(rel.get("attachment"), dict) else {},
                "milestones": [dict(x) for x in (rel.get("milestones") or [])[:10] if isinstance(x, dict)],
                "we_memory": [dict(x) for x in (rel.get("we_memory") or [])[:20] if isinstance(x, dict)],
                "commitment": round(float(rel.get("commitment", 0.0) or 0.0), 4),
                "investment": round(float(rel.get("investment", 0.0) or 0.0), 4),
                "annotations": [dict(x) for x in (rel.get("annotations") or [])[:10]
                                if isinstance(x, dict)],
            },
            "belief_state": {
                "beliefs": [str(x)[:60] for x in (belief.get("beliefs") or [])[:3] if str(x)],
                "desires": [str(x)[:60] for x in (belief.get("desires") or [])[:3] if str(x)],
                "intentions": [str(x)[:60] for x in (belief.get("intentions") or [])[:3] if str(x)],
                "confidence": round(float(belief.get("confidence", 0.0) or 0.0), 3),
            },
        })
    return rows


PLUTCHIK_WHEEL = {
    "joy": ("joy", "trust", "anticipation", "surprise"),
    "trust": ("trust", "joy", "acceptance", "admiration"),
    "fear": ("fear", "surprise", "apprehension", "awe"),
    "surprise": ("surprise", "fear", "distraction", "amazement"),
    "sadness": ("sadness", "disgust", "pensiveness", "remorse"),
    "disgust": ("disgust", "sadness", "boredom", "loathing"),
    "anger": ("anger", "anticipation", "annoyance", "rage"),
    "anticipation": ("anticipation", "anger", "interest", "vigilance"),
}

EMOTION_SPECTRUM = [
    ("admiration", "钦佩", 0.40, 0.25, 0.45, 0.55),
    ("adoration", "爱慕", 0.80, 0.45, 0.40, 0.90),
    ("aesthetic", "审美欣赏", 0.50, 0.30, 0.45, 0.60),
    ("amusement", "好笑", 0.80, 0.60, 0.55, 0.60),
    ("anger", "生气", -0.60, 0.80, 0.85, 0.30),
    ("anxiety", "焦虑", -0.40, 0.80, 0.20, 0.30),
    ("awe", "敬畏", 0.60, 0.70, 0.20, 0.60),
    ("awkwardness", "尴尬", -0.20, 0.50, 0.10, 0.40),
    ("boredom", "无聊", -0.40, 0.10, 0.40, 0.40),
    ("calmness", "平静", 0.10, 0.20, 0.50, 0.50),
    ("confusion", "困惑", -0.10, 0.50, 0.40, 0.50),
    ("contempt", "轻蔑", -0.50, 0.40, 0.90, 0.30),
    ("contentment", "满足", 0.60, 0.20, 0.60, 0.70),
    ("desire", "欲望", 0.60, 0.70, 0.60, 0.60),
    ("disappointment", "失望", -0.50, 0.30, 0.40, 0.50),
    ("disgust", "厌恶", -0.60, 0.40, 0.70, 0.40),
    ("empathic_pain", "共情痛苦", -0.40, 0.40, 0.20, 0.70),
    ("entrancement", "入迷", 0.50, 0.50, 0.40, 0.60),
    ("envy", "嫉妒", -0.40, 0.60, 0.30, 0.40),
    ("excitement", "兴奋", 0.70, 0.90, 0.50, 0.60),
    ("fear", "害怕", -0.50, 0.80, 0.20, 0.40),
    ("guilt", "内疚", -0.50, 0.40, 0.30, 0.50),
    ("horror", "恐惧", -0.80, 0.90, 0.20, 0.40),
    ("interest", "兴趣", 0.40, 0.50, 0.50, 0.60),
    ("joy", "快乐", 0.80, 0.60, 0.60, 0.70),
    ("nostalgia", "怀念", 0.30, 0.30, 0.40, 0.60),
    ("pride", "自豪", 0.60, 0.50, 0.90, 0.60),
]


class _AutonomySendTarget:
    """Minimal event-like send target for the P0-1 background generator."""

    def __init__(self, plugin, umo, sender_id="", sender_name="", private=True):
        self._plugin = plugin
        self.unified_msg_origin = str(umo or "")
        self._sender_id = str(sender_id or "")
        self._sender_name = str(sender_name or "")
        self._private = bool(private)

    def is_private_chat(self):
        return self._private

    def get_sender_id(self):
        return self._sender_id

    def get_sender_name(self):
        return self._sender_name

    async def send(self, chain):
        return await self._plugin.context.send_message(self.unified_msg_origin, chain)


# every name above, imported modules and private helpers included, for `from .common import *`
__all__ = [_n for _n in dir() if not _n.startswith('__')]
