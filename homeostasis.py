# -*- coding: utf-8 -*-
"""Minimal homeostasis / action-control layer for BioCore.

Deterministic, bounded, no LLM and no prompt writing. It only produces
drive / set-point / L_int / readiness / action-tendency state.

ams-life: an electronic ghost has no physiology. The virtual body (energy,
hydration, warmth, fatigue), interoception and the Maslow need pyramid are
gone; the drives are her own urges: wanting to talk (social), curiosity and
wanting to be seen. Having talked a lot (core.talked) lowers readiness.

This is an engineering control loop, not a physiological or clinical model.
"""
from __future__ import annotations

import time
from typing import Any

DRIVE_KEYS = ("social", "curiosity", "seen")
# Task-15 P0-2: bounded noise jitter on action strength (only when autonomy on).
AUTONOMY_ACTION_JITTER = 0.05
SETPOINT_WARMUP_TICKS = 12
SETPOINT_ETA = 2e-6
MAX_DRIVES = len(DRIVE_KEYS)
ACTION_MODES = ("engage", "rest", "seek_social", "explore", "withdraw", "comfort")


def _clamp(value: Any, low: float = 0.0, high: float = 1.0) -> float:
    try:
        number = float(value)
        if number != number or number in (float("inf"), float("-inf")):
            return low
        return max(low, min(high, number))
    except Exception:
        return low


def default_state() -> dict[str, Any]:
    return {
        "drives": {key: 0.55 for key in DRIVE_KEYS},
        "set_points": {key: 0.55 for key in DRIVE_KEYS},
        "setpoint_ticks": 0,
        "tick": 0,
        "L_int": 0.0,
        "readiness": 0.60,
        "action": {"mode": "engage", "reason": "baseline", "strength": 0.5},
        "updated_ts": 0.0,
    }


def _ensure_state(state: Any) -> dict[str, Any]:
    base = default_state()
    if not isinstance(state, dict):
        return base
    for key, value in base.items():
        if key not in state:
            state[key] = value
    for group in ("drives", "set_points"):
        if not isinstance(state.get(group), dict):
            state[group] = dict(base[group])
    return state


def _core(core: Any, name: str, default: float = 0.5) -> float:
    try:
        return _clamp(getattr(core, name, default), 0.0, 1.0)
    except Exception:
        return default


def _drives(core: Any, relationship: Any = None) -> dict[str, float]:
    social = _core(core, "social", 0.55)
    curiosity = _clamp(0.60 * (1.0 - _core(core, "boredom", 0.0)) +
                       0.40 * _core(core, "novelty_need", 0.5) +
                       0.10 * _core(core, "info_gap", 0.0))
    seen = _core(core, "seen_need", 0.3)
    if isinstance(relationship, dict):
        state = relationship.get("state") if isinstance(relationship.get("state"), dict) else {}
        try:
            social = _clamp(social + 0.10 * _clamp(state.get("closeness", 0.5)))
        except Exception:
            pass
    return {"social": round(social, 4), "curiosity": round(curiosity, 4), "seen": round(seen, 4)}


def _update_set_points(state: dict, dt: float = 60.0) -> None:
    drive = state.get("drives") or {}
    points = state.get("set_points") or {}
    try:
        ticks = int(state.get("setpoint_ticks", 0) or 0) + 1
    except Exception:
        ticks = 1
    for key in DRIVE_KEYS:
        current = _clamp(points.get(key, 0.55))
        value = _clamp(drive.get(key, 0.55))
        if ticks <= SETPOINT_WARMUP_TICKS:
            points[key] = round(current + (value - current) / max(1, ticks), 6)
        else:
            try:
                step = SETPOINT_ETA * max(0.0, float(dt))
            except Exception:
                step = SETPOINT_ETA * 60.0
            points[key] = round(_clamp(current + step * (value - current)), 6)
    state["set_points"] = points
    state["setpoint_ticks"] = ticks


def _readiness(drives: dict, L_int: float, stress: float, talked: float) -> float:
    return round(_clamp(
        0.30 * float(drives.get("social", 0.5)) +
        0.15 * float(drives.get("curiosity", 0.5)) +
        0.15 * float(drives.get("seen", 0.3)) +
        0.40 * (1.0 - _clamp(stress)) -
        0.30 * _clamp(L_int) -
        0.40 * _clamp(talked)), 4)


def action_tendency(state: Any, core: Any = None) -> dict[str, Any]:
    """Deterministic drive->action tendency (state token only; no send gate)."""
    s = _ensure_state(state if isinstance(state, dict) else None)
    drives = s.get("drives") or {}
    readiness = _clamp(s.get("readiness", 0.6))
    L_int = _clamp(s.get("L_int", 0.0))
    social = _clamp(drives.get("social", 0.5))
    curiosity = _clamp(drives.get("curiosity", 0.5))
    seen = _clamp(drives.get("seen", 0.3))
    stress = _core(core, "stress", 0.1) if core is not None else 0.0
    talked = _core(core, "talked", 0.0) if core is not None else 0.0
    boredom = _core(core, "boredom", 0.0) if core is not None else 0.0
    if talked >= 0.72:
        mode, why = "rest", "talked_a_lot"
    elif stress >= 0.75:
        mode, why = "withdraw", "stress"
    elif seen >= 0.65 and social >= 0.45:
        mode, why = "seek_social", "wants_to_be_seen"
    elif boredom >= 0.60 and curiosity >= 0.45:
        mode, why = "explore", "bored_and_curious"
    elif readiness >= 0.65 and L_int <= 0.25:
        mode, why = "engage", "ready"
    elif L_int >= 0.35:
        mode, why = "comfort", "internal_load"
    else:
        mode, why = "engage", "baseline"
    strength = _clamp(0.35 + 0.40 * readiness + 0.25 * L_int)
    # Task-15 P0-2: noise is an L1 input to expression tendency, not a parallel
    # telemetry path. Bounded ±0.05 jitter on strength; disabled autonomy means
    # the exact legacy value (no change).
    try:
        if core is not None and bool(getattr(core, "autonomy_enabled", False)):
            _noise = getattr(core, "noise", {}) or {}
            _st = float(_noise.get("stress", 0.0) or 0.0)
            _so = float(_noise.get("social", 0.0) or 0.0)
            _va = float(_noise.get("valence", 0.0) or 0.0)
            _jitter = AUTONOMY_ACTION_JITTER * ((_st + _so - _va) / 0.30)
            _jitter = max(-AUTONOMY_ACTION_JITTER, min(AUTONOMY_ACTION_JITTER, _jitter))
            strength = _clamp(strength + _jitter, 0.0, 1.0)
    except Exception:
        pass
    return {"mode": mode, "reason": why, "strength": round(strength, 4)}


def normalize_state(state: Any) -> dict[str, Any]:
    """Normalize a persisted homeostasis dict; malformed input falls back safely.
    ams-life: keys of the old physiology (body, need_pyramid, interoception,
    the energy/safety drives) are dropped here."""
    base = default_state()
    if not isinstance(state, dict):
        return base
    try:
        for group in ("drives", "set_points"):
            raw = state.get(group) if isinstance(state.get(group), dict) else {}
            for key in DRIVE_KEYS:
                base[group][key] = round(_clamp(raw.get(key, base[group][key])), 6)
        for key in ("tick", "setpoint_ticks"):
            try:
                base[key] = max(0, min(10 ** 9, int(float(state.get(key, 0) or 0))))
            except Exception:
                base[key] = 0
        base["L_int"] = round(_clamp(state.get("L_int", 0.0)), 6)
        base["readiness"] = round(_clamp(state.get("readiness", 0.6)), 6)
        action = state.get("action") if isinstance(state.get("action"), dict) else {}
        mode = str(action.get("mode") or "engage")
        if mode not in ACTION_MODES:
            mode = "engage"
        base["action"] = {"mode": mode,
                          "reason": str(action.get("reason") or "baseline")[:40],
                          "strength": round(_clamp(action.get("strength", 0.5)), 6)}
        try:
            base["updated_ts"] = round(float(state.get("updated_ts", 0.0) or 0.0), 3)
        except Exception:
            base["updated_ts"] = 0.0
        return base
    except Exception:
        return default_state()


def step(core: Any, dt: float = 60.0, relationship: Any = None) -> dict[str, Any]:
    """One deterministic homeostasis update; attaches and returns the state."""
    state = _ensure_state(getattr(core, "homeostasis", None))
    drives = _drives(core, relationship)
    state["drives"] = drives
    _update_set_points(state, dt)
    points = state["set_points"]
    L_int = sum(abs(float(drives.get(key, 0.5)) - float(points.get(key, 0.5)))
                for key in DRIVE_KEYS) / MAX_DRIVES
    state["L_int"] = round(_clamp(L_int), 4)
    # Entry: internal load lightly raises stress (bounded; no runaway).
    try:
        core.stress = _clamp(float(getattr(core, "stress", 0.1)) + 0.01 * state["L_int"], 0.0, 1.0)
    except Exception:
        pass
    state["readiness"] = _readiness(drives, state["L_int"], _core(core, "stress", 0.1),
                                    _core(core, "talked", 0.0))
    state["action"] = action_tendency(state, core)
    state["tick"] = int(state.get("tick", 0) or 0) + 1
    state["updated_ts"] = round(time.time(), 3)
    try:
        core.homeostasis = state
    except Exception:
        pass
    return state


def snapshot(core: Any) -> dict[str, Any]:
    state = getattr(core, "homeostasis", None)
    return dict(state) if isinstance(state, dict) else default_state()
