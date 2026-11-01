# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""The BioCore state machine (L1): moved out of main.py unchanged."""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
import zlib
import copy
from datetime import datetime, timedelta
try:
    from . import daily
except ImportError:
    import daily


def ate(core, now):
    core.hunger = 0.1
    core.last_meal = float(now)


def slept(core, start, end):
    hours = max(0.0, (float(end) - float(start)) / 3600.0)
    core.sleepiness = _clip(core.sleepiness - 0.25 * hours, 0, 1)
    core.physical_fatigue = _clip(core.physical_fatigue - 0.10 * hours, 0, 1)
    core.last_sleep_end = float(end)


def rested(core, minutes, now):
    core.physical_fatigue = _clip(core.physical_fatigue - 0.10 * max(0.0, float(minutes)) / 60.0, 0, 1)
    core.last_rest = float(now)


def exerted(core, amount, now):
    core.physical_fatigue = _clip(core.physical_fatigue + max(0.0, float(amount)), 0, 1)


def _advance_needs(core, start, end):
    cursor = datetime.fromtimestamp(start)
    finish = datetime.fromtimestamp(end)
    while cursor < finish:
        boundary = daily.next_period(cursor)
        # Split at 06:00 and 23:00 for the night waking rate.
        for hour in (6, 23):
            candidate = cursor.replace(hour=hour, minute=0, second=0, microsecond=0)
            if cursor < candidate < boundary:
                boundary = candidate
        period_end = daily.next_period(cursor)
        midpoint = daily.period_start(cursor) + (period_end - daily.period_start(cursor)) / 2
        _, doing, _ = daily.schedule(cursor, core.energy, core.v, core.stress)
        if '吃' in doing and cursor < midpoint < boundary:
            boundary = midpoint
        stop = min(boundary, finish)
        hours = (stop - cursor).total_seconds() / 3600.0
        sleeping = daily.period_start(cursor).hour == 0 or doing == '睡觉'
        if sleeping:
            core.sleepiness = _clip(core.sleepiness - 0.25 * hours, 0, 1)
            core.physical_fatigue = _clip(core.physical_fatigue - 0.10 * hours, 0, 1)
            if stop == period_end:
                core.last_sleep_end = stop.timestamp()
        else:
            rate = 0.10 if cursor.hour >= 23 or cursor.hour < 6 else 0.06
            core.sleepiness = _clip(core.sleepiness + rate * hours, 0, 1)
            core.physical_fatigue = _clip(core.physical_fatigue + 0.02 * hours, 0, 1)
        core.hunger = _clip(core.hunger + 0.08 * hours, 0, 1)
        if '吃' in doing and stop == midpoint and core.last_meal < midpoint.timestamp():
            ate(core, midpoint.timestamp())
        cursor = stop


# ams-life: habituation compares what was just heard with what was heard a few minutes
# ago. It keeps a MinHash fingerprint of the character pairs instead of the words: the
# words cannot be read back from it, and the share of equal positions estimates the
# same pair-overlap (Jaccard) that _text_similarity measures on the words.
_FINGERPRINT_SIZE = 32

# Bounded changes, in body units; repeat hits within ten minutes are discounted.
MOOD_EVENT_CHANGES = {
    "praise": {"v": .06},
    "criticism": {"v": -.06, "stress": .05},
    "woken": {"v": -.06, "stress": .08, "energy": -.08},
    "answered": {"v": .04, "seen_need": -.12},
    "ignored": {"v": -.06, "seen_need": .08},
    "unanswered_share": {"v": -.06, "seen_need": .08},
    "quarrel": {"stress": .05},
    "liked_topic": {"v": .04, "social": .05},
    "fun_page": {"v": .04, "novelty_need": -.05},
    "wrong_name": {"v": -.04},
    "robot": {"v": -.04},
    "sleep": {},
}
MOOD_EVENT_LABELS = {
    "praise": "被夸了", "criticism": "被说了", "woken": "被吵醒了",
    "answered": "有人接话", "ignored": "没被接话", "unanswered_share": "分享没人回应",
    "quarrel": "群里有争执", "liked_topic": "聊到喜欢的事", "fun_page": "看到有趣的网页",
    "wrong_name": "被叫错名字", "robot": "被当成机器人", "sleep": "睡了一觉",
}
MOOD_EVENT_LIMIT = .08
MOOD_REPEAT_SECONDS = 600.0
MOOD_REPEAT_FACTOR = .5
MOOD_EVENT_HALF_LIFE_MINUTES = 120.0
MOOD_BYSTANDER_WEIGHT = 1.0 / 3.0
MOOD_PRAISE_WORDS = ("谢谢", "感谢", "真棒", "厉害", "可爱", "夸你")
MOOD_CRITICISM_WORDS = ("讨厌你", "闭嘴", "笨蛋", "蠢", "烦死了", "骂你")
MOOD_WRONG_NAME_WORDS = ("叫错名字", "不是你的名字")
MOOD_ROBOT_WORDS = ("你是机器人", "只是机器人", "不过是机器人")
MOOD_QUARREL_WORDS = ("吵架", "吵起来", "互相骂")
MOOD_LIKED_WORDS = ("喜欢的东西", "你喜欢的", "你最喜欢")


def mood_kinds(text, addressed=False):
    """Conservative word cues; ambiguous emotional speech is ordinary conversation."""
    text = str(text or "")
    kinds = []
    if addressed:
        for kind, words in (("praise", MOOD_PRAISE_WORDS), ("criticism", MOOD_CRITICISM_WORDS),
                            ("wrong_name", MOOD_WRONG_NAME_WORDS), ("robot", MOOD_ROBOT_WORDS),
                            ("liked_topic", MOOD_LIKED_WORDS)):
            if any(BioCore._word_hit(text, word) for word in words):
                kinds.append(kind)
    if any(BioCore._word_hit(text, word) for word in MOOD_QUARREL_WORDS):
        kinds.append("quarrel")
    return kinds


def _fingerprint(text) -> tuple:
    text = str(text or "")
    pairs = {text[i:i + 2] for i in range(max(0, len(text) - 1))}
    if not pairs:
        return ()
    encoded = [x.encode("utf-8") for x in pairs]
    return tuple(min(zlib.crc32(b"%d|" % k + x) for x in encoded) for k in range(_FINGERPRINT_SIZE))


def _fingerprint_similarity(a, b) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    return sum(1 for x, y in zip(a, b) if x == y) / float(len(a))


class BioCore:
    @staticmethod
    def _word_hit(text: str, word: str) -> bool:
        idx = text.find(word)
        while idx >= 0:
            prefix = text[max(0, idx - 2):idx]
            if not prefix.endswith(("不", "没", "别", "无")):
                return True
            idx = text.find(word, idx + len(word))
        return False

    def feedback_user(self, text: str) -> None:
        t = str(text or "")
        cold_words = ("废物", "垃圾", "讨厌", "滚", "闭嘴", "没用", "蠢", "去死", "别烦", "傻子")
        warm_words = ("谢谢", "喜欢", "陪", "辛苦", "厉害", "可爱", "抱")
        cold = sum(1 for w in cold_words if self._word_hit(t, w))
        warm = sum(1 for w in warm_words if self._word_hit(t, w))
        if cold:
            self.v = _clip(self.v - 0.035 * cold, -1, 1)
            self.stress = _clip(self.stress + 0.035 * cold, 0, 1)
            self.echo_trace = _clip(self.echo_trace - 0.03 * cold, -1, 1)
        if warm:
            self.v = _clip(self.v + 0.02 * warm, -1, 1)
            self.stress = _clip(self.stress - 0.01 * warm, 0, 1)

    def __init__(self, profile=None):
        self.profile = dict(profile or DEFAULT_PROFILE)
        self.v = _clip(self.profile.get("baseline_v", 0.05), -1, 1)
        self.a = _clip(self.profile.get("baseline_a", 0.4), 0, 1)
        # Compiled persona profiles use PAD-baseline names (da_baseline /
        # social_baseline); legacy profiles may use baseline_d / baseline_social.
        self.d = _clip(self.profile.get("baseline_d", self.profile.get("da_baseline", 0.55)), -1, 1)
        self.social = _clip(self.profile.get("baseline_social", self.profile.get("social_baseline", 0.55)), 0, 1)
        self.stress = 0.1
        self.energy = _clip(self.profile.get("energy_baseline", 0.55), 0, 1)
        # ams-life: an electronic ghost's own urges, numbers only. There is no
        # global trust: trust lives in each person's relationship record.
        self.seen_need = 0.3        # wanting to be seen: rises while nobody answers her
        self.talked = 0.0           # having talked a lot: every reply adds, it fades over hours
        self.ambient = 0.0          # how lively the chats around her are (message times only)
        self._partner_trust = None  # trust in the person she is answering, during one observe()
        self._derive()
        self.ticks = 0
        self.labels = {"emotion": "neutral", "intent": "hold", "expression": "normal",
                       "need": "talk", "energy": "normal", "stress": "calm"}
        self.noise = {"stress": 0.0, "energy": 0.0, "social": 0.0, "attention": 0.0, "valence": 0.0}
        # Task-15: autonomy is opt-in; default OFF is a pure no-op.
        self.autonomy_enabled = False
        self._proactive_autonomy = {"enabled": False}
        # Task-28: minimal autonomy loop. Config owns "enabled"; the loop state
        # dict is created lazily and only persisted while enabled (default OFF
        # leaves the state file byte-identical to 1.2.98).
        self.autonomy_loop_enabled = False
        self.autonomy_loop = None
        self.autonomy_loop_theta_ig = AUTONOMY_LOOP_THETA_IG
        self.autonomy_loop_margin = AUTONOMY_LOOP_MARGIN
        self.autonomy_loop_k_delay = AUTONOMY_LOOP_K_DELAY
        self.autonomy_loop_ior_seconds = AUTONOMY_LOOP_IOR_SECONDS
        self.autonomy_loop_c0 = AUTONOMY_LOOP_C0
        self.autonomy_loop_c1 = AUTONOMY_LOOP_C1
        self.autonomy_loop_c2 = AUTONOMY_LOOP_C2
        self.autonomy_loop_token_only = True
        self._noise_seed = 0
        self._noise_accum = {}
        # Task-20: L1 learning state (deterministic, bounded, auditable).
        self.bio_learning = True
        self.retention_model = "single"
        self._learning = {
            "version": 1,
            "params": {"regulation_q": {}, "trust_alpha": 0.30,
                       "learning_rate": LEARNING_Q_ALPHA},
            "last_update": 0.0, "updates_count": 0, "log": [],
        }
        self.echo = 0.0
        self.echo_trace = 0.0
        self.reflection = {"v": 0.0, "a": 0.0, "d": 0.0, "social": 0.0}
        self.momentum = {"v": 0.0, "a": 0.0, "d": 0.0, "social": 0.0}
        self.appraisal = {"novelty": 0.0, "goal_relevance": 0.0, "coping": 0.5, "agency": 0.5}
        self.compound = ""
        self.regulation = "none"
        self.history = []
        # B-T06: exploration/boredom drive (bounded state; not a claim about feelings).
        self.novelty_need = 0.5
        self.boredom = 0.0
        # Batch4: transient bounded states (not persisted): information-gap
        # curiosity proxy and strong-negative sensitization history.
        self.info_gap = 0.0
        self._sensitization_history = []
        # B-T07: autonomy/refusal readiness (bounded state; strategy stays outside).
        self.boundary_pressure = 0.0
        self.refusal_readiness = 0.0
        # B-T09: interpersonal coupling (co-regulation proxy, not "being dragged").
        self.interpersonal = {"other_valence_est": 0.0, "coupling": 0.0, "dampening": 1.0}
        # Allostatic paper mechanism (bounded, no prompt). ams-life: no circadian
        # rhythm; how lively the chats are (self.ambient) takes its place.
        self.allostatic_load = 0.0
        # B-T12: deterministic daily digest base (no narrative text).
        self.daily_digests = []
        self._daily_accum = {"date": "", "n": 0, "v": 0.0, "a": 0.0, "stress": 0.0,
                             "emotions": {}, "ticks": 0}
        # ams-life: open loops live in her phone (one list per chat window);
        # the body only knows how many are due, as a number.
        self.loop_pressure = {"due": 0, "delay_min": 0.0}
        self.stimuli = []
        self.goals = [
            {"key": "relationship", "name": "和重要的人保持亲近", "keywords": ("喜欢", "爱", "陪", "关系", "信任", "靠近", "一起"),
             "horizon": "long", "progress": 0.0, "priority": 0.90, "last_update": 0.0},
            {"key": "autonomy", "name": "不被当成工具", "keywords": ("废物", "命令", "必须", "听话", "工具", "滚", "闭嘴"),
             "horizon": "long", "progress": 0.0, "priority": 0.85, "last_update": 0.0},
            {"key": "competence", "name": "证明自己能做好", "keywords": ("没用", "做不好", "失败", "厉害", "做得好", "能干"),
             "horizon": "long", "progress": 0.0, "priority": 0.60, "last_update": 0.0},
            {"key": "stability", "name": "保持情绪稳定", "keywords": ("平静", "冷静", "慢慢", "不急", "休息"),
             "horizon": "short", "progress": 0.0, "priority": 0.55, "last_update": 0.0},
        ]
        self.goal_focus = ""
        self.goal_scores = {}
        self.goal_context_terms = {
            "relationship": ("喜欢", "陪", "亲近", "信任", "关系", "一起", "在乎", "记得", "承诺", "重要", "对方"),
            "autonomy": ("自由", "命令", "被迫", "工具", "听话", "安排", "关起来", "憋", "自主"),
            "competence": ("做不好", "失败", "没用", "厉害", "能干", "任务", "做好", "证明", "靠谱"),
            "stability": ("平静", "冷静", "休息", "不急", "慢慢", "稳住", "安心", "别怕"),
        }
        self.coping_history = []
        self.opponent = {"v": 0.0, "a": 0.0, "d": 0.0, "social": 0.0}
        self.opponent_gain = 0.10
        self.reconsolidation_seconds = 600.0
        self.regulation_stats = {}
        self.attention = 0.5
        self.meta_emotion = ""
        self.goal_conflict = []
        self.self_timeline = {"past": [], "present": "", "future": []}
        self.sec = {}
        self.core_self = ""
        self.narrative_self = ""
        self._query_embedding = None
        self.emotion_decay_factors = {"anger": 0.55, "fear": 0.70, "joy": 1.15,
                                      "sadness": 1.50, "loneliness": 1.80, "neutral": 1.0}
        self.valence_decay_minutes = 120.0
        self.arousal_decay_minutes = 30.0
        self.social_decay_minutes = 180.0
        self.last_tick = __import__("time").time()
        self.sleepiness, self.hunger, self.physical_fatigue = 0.2, 0.3, 0.1
        self.last_sleep_end = self.last_meal = self.last_rest = self.last_tick
        self.ripple = {"upper": 0.0, "lower": 0.0, "overlap": 0.0, "energy": 0.0}
        self.spiking = {"rate": 0.0, "variance": 0.0, "ei": 0.0}
        self._rng = __import__("random").Random()

    def load_state(self, d: dict) -> None:
        if not isinstance(d, dict):
            return
        now = __import__("time").time()
        for key, default in (("sleepiness", 0.2), ("hunger", 0.3), ("physical_fatigue", 0.1)):
            try:
                value = float(d.get(key, default))
                setattr(self, key, _clip(value, 0, 1) if math.isfinite(value) else default)
            except (TypeError, ValueError):
                setattr(self, key, default)
        for key in ("last_sleep_end", "last_meal", "last_rest"):
            try:
                value = float(d.get(key, now))
                setattr(self, key, value if math.isfinite(value) and value >= 0 else now)
            except (TypeError, ValueError):
                setattr(self, key, now)
        for key in ("v", "a", "d", "stress", "energy", "social"):
            if key in d:
                try:
                    lo = -1 if key in ("v", "d") else 0
                    hi = 1.0
                    setattr(self, key, _clip(d[key], lo, hi))
                except Exception:
                    pass
        self._derive()
        try:
            self.ticks = max(0, int(d.get("ticks", self.ticks) or 0))
        except Exception:
            pass
        def _num_map(raw, defaults, lo=-1.0, hi=1.0):
            out = dict(defaults)
            if not isinstance(raw, dict):
                return out
            for key, default in defaults.items():
                if key not in raw:
                    continue
                try:
                    value = float(raw.get(key))
                    if not math.isfinite(value):
                        continue
                    out[key] = max(lo, min(hi, value))
                except Exception:
                    continue
            return out

        self.noise = _num_map(d.get("noise"),
                              {"stress": 0.0, "energy": 0.0, "social": 0.0,
                               "attention": 0.0, "valence": 0.0}, -0.3, 0.3)
        self.reflection = _num_map(d.get("reflection"),
                                   {"v": 0.0, "a": 0.0, "d": 0.0, "social": 0.0}, -1.0, 1.0)
        self.momentum = _num_map(d.get("momentum"),
                                 {"v": 0.0, "a": 0.0, "d": 0.0, "social": 0.0}, -1.0, 1.0)
        self.appraisal = _num_map(d.get("appraisal"),
                                  {"novelty": 0.0, "goal_relevance": 0.0,
                                   "coping": 0.5, "agency": 0.5}, 0.0, 1.0)
        self.opponent = _num_map(d.get("opponent"),
                                 {"v": 0.0, "a": 0.0, "d": 0.0, "social": 0.0}, -1.0, 1.0)
        # Labels are display/decision proxies: whitelist known values only.
        _allowed_labels = {
            "emotion": {"joy", "sadness", "anger", "fear", "loneliness", "neutral"},
            "intent": {"approach", "hold", "withdraw"},
            "expression": {"open", "normal", "short"},
            "need": {"share", "space", "vent", "be_heard", "talk"},
            "energy": {"low", "normal", "high"},
            "stress": {"calm", "tense", "overloaded"},
        }
        safe_labels = {}
        raw_labels = d.get("labels") if isinstance(d.get("labels"), dict) else {}
        for key, allowed in _allowed_labels.items():
            value = str(raw_labels.get(key) or "").strip()
            if value in allowed:
                safe_labels[key] = value
        self.labels = {**{"emotion": "neutral", "intent": "hold",
                          "expression": "normal", "need": "talk",
                          "energy": "normal", "stress": "calm"}, **safe_labels}
        if isinstance(d.get("ripple"), dict):
            self.ripple = _num_map(d["ripple"], self.ripple, 0.0, 1.0)
        if isinstance(d.get("spiking"), dict):
            self.spiking = _num_map(d["spiking"], self.spiking, 0.0, 10.0)
        # ams-life: the body keeps no text. Older state files may still carry
        # what was said (stimulus text, reply text); it is left behind here.
        if isinstance(d.get("stimuli"), list):
            self.stimuli = [{k: v for k, v in x.items() if k not in ("text", "fp")}
                            for x in d["stimuli"] if isinstance(x, dict)][-40:]
        if isinstance(d.get("history"), list):
            self.history = [{k: v for k, v in x.items() if k != "text"}
                            for x in d["history"] if isinstance(x, dict)][-80:]
        if isinstance(d.get("coping_history"), list):
            self.coping_history = [float(x) for x in d["coping_history"] if isinstance(x, (int, float))][-40:]
        if isinstance(d.get("regulation_stats"), dict):
            self.regulation_stats = {str(k): dict(v) for k, v in d["regulation_stats"].items() if isinstance(v, dict)}
        try:
            self.attention = _clip(d.get("attention", 0.5), 0, 1)
        except Exception:
            self.attention = 0.5
        for _key in ("allostatic_load",):
            if _key in d:
                try:
                    setattr(self, _key, _clip(d[_key], 0, 1))
                except Exception:
                    pass
        try:
            self.homeostasis = homeostasis.normalize_state(d.get("homeostasis"))
        except Exception:
            self.homeostasis = homeostasis.default_state()
        # BUG-01: restore the remaining bounded biological fields.
        for _key in ("novelty_need", "boredom", "boundary_pressure", "refusal_readiness",
                     "seen_need", "talked", "ambient"):
            if _key in d:
                try:
                    setattr(self, _key, _clip(d[_key], 0.0, 1.0))
                except Exception:
                    pass
        raw_inter = d.get("interpersonal") if isinstance(d.get("interpersonal"), dict) else {}
        self.interpersonal = {
            "other_valence_est": round(_clip(raw_inter.get("other_valence_est", 0.0), -1.0, 1.0), 6),
            "coupling": round(_clip(raw_inter.get("coupling", 0.0), 0.0, 1.0), 6),
            "dampening": round(_clip(raw_inter.get("dampening", 1.0), 0.0, 1.0), 6),
        }
        digests = d.get("daily_digests")
        if isinstance(digests, list):
            safe_digests = []
            for item in digests[-30:]:
                if not isinstance(item, dict):
                    continue
                try:
                    safe_digests.append({
                        "date": str(item.get("date") or "")[:10],
                        "event_ids": [str(x)[:80] for x in (item.get("event_ids") or [])[:50] if str(x)],
                        "mean_v": round(_clip(item.get("mean_v", 0.0), -1.0, 1.0), 4),
                        "mean_a": round(_clip(item.get("mean_a", 0.0), 0.0, 1.0), 4),
                        "mean_stress": round(_clip(item.get("mean_stress", 0.0), 0.0, 1.0), 4),
                        "dominant_emotion": str(item.get("dominant_emotion") or "neutral")[:20],
                        "interaction_count": max(0, int(item.get("interaction_count", 0) or 0)),
                    })
                except Exception:
                    continue
            self.daily_digests = safe_digests[-30:]
        self.goal_focus = str(d.get("goal_focus") or "")[:40]
        if isinstance(d.get("meta_emotion"), str):
            self.meta_emotion = d["meta_emotion"]
        if isinstance(d.get("goals"), list):
            self.goals = [dict(g) for g in d["goals"] if isinstance(g, dict)][:8]
        if isinstance(d.get("goal_conflict"), list):
            self.goal_conflict = [str(x) for x in d["goal_conflict"]][:6]
        if isinstance(d.get("goal_scores"), dict):
            self.goal_scores = {str(k): _clip(v, 0, 1) for k, v in d["goal_scores"].items()
                                if isinstance(v, (int, float))}
        for _g in self.goals:
            if not isinstance(_g, dict):
                continue
            _g.setdefault("priority", 0.5)
            _g.setdefault("last_update", 0.0)
        if isinstance(d.get("sec"), dict):
            self.sec = dict(d["sec"])
        self.last_tick = __import__("time").time()
        for key in ("echo", "echo_trace"):
            if key in d:
                try:
                    setattr(self, key, _clip(d[key]))
                except Exception:
                    pass
        # Task-15: restore autonomy counters/history only; enabled is owned by
        # plugin config. Old states without the key keep {"enabled": False}.
        _raw_auto = d.get("proactive_autonomy")
        if isinstance(_raw_auto, dict):
            _safe_auto = {"enabled": bool(_raw_auto.get("enabled", False))}
            for _k in ("threshold", "max_chars", "impulse", "chaos",
                       "impulse_ema", "ready", "gain", "noise_seed",
                       "last_sent_ts", "sent_count", "sent_day", "updated_ts"):
                if _k in _raw_auto:
                    _safe_auto[_k] = _raw_auto[_k]
            self._proactive_autonomy = _safe_auto
            try:
                self._noise_seed = max(0, int(_raw_auto.get("noise_seed", 0) or 0))
            except Exception:
                self._noise_seed = 0
        # Task-28: restore the autonomy-loop state if present; "enabled" is
        # owned by plugin config and unknown/extra keys are ignored.
        _raw_loop = d.get("autonomy_loop")
        if isinstance(_raw_loop, dict):
            self.autonomy_loop = self._autonomy_loop_restore(_raw_loop)

    def _derive(self) -> None:
        """Derive stress/energy from v, a, dominance, social (they are not independent)."""
        v = float(getattr(self, "v", 0.0))
        a = float(getattr(self, "a", 0.5))
        d = float(getattr(self, "d", 0.55))
        soc = float(getattr(self, "social", 0.55))
        self.stress = _clip(0.45 * max(0.0, -v) * a + 0.35 * (1.0 - d) + 0.20 * (1.0 - soc), 0, 1)
        self.energy = _clip(0.45 * a + 0.25 * max(0.0, v) + 0.20 * d + 0.10 * soc, 0, 1)
        if hasattr(self, "_mood_stress"):
            self.stress = _clip(self.stress + self._mood_stress, 0, 1)
        if hasattr(self, "_mood_energy"):
            self.energy = _clip(self.energy + self._mood_energy, 0, 1)

    def mood_event(self, kind, weight=1.0, now=None) -> None:
        """Apply one known event; retain only its kind and time, never its source."""
        if kind not in MOOD_EVENT_CHANGES:
            return
        now = time.time() if now is None else float(now)
        self._decay_to_now()
        recent = getattr(self, "mood_events", [])
        previous = next((x for x in reversed(recent) if x["kind"] == kind), None)
        repeat = MOOD_REPEAT_FACTOR if previous and 0 <= now - previous["ts"] < MOOD_REPEAT_SECONDS else 1.0
        weight = _clip(float(weight), 0, 1) * repeat
        if kind == "sleep":
            self._mood_stress = float(getattr(self, "_mood_stress", 0.0)) * .25
            self._mood_energy = float(getattr(self, "_mood_energy", 0.0)) * .25
            self.v = min(0.0, self.v) * .25 + max(0.0, self.v)
            self.seen_need = .3 + (self.seen_need - .3) * .25
        else:
            for field, change in MOOD_EVENT_CHANGES[kind].items():
                delta = max(-MOOD_EVENT_LIMIT, min(MOOD_EVENT_LIMIT, change * weight))
                name = "_mood_" + field if field in ("stress", "energy") else field
                low = -1.0 if field in ("v", "stress", "energy") else 0.0
                before = float(getattr(self, name, 0.0))
                setattr(self, name, _clip(before + delta, low, 1.0))
                if field == "novelty_need":
                    self._mood_novelty = float(getattr(self, "_mood_novelty", 0.0)) + self.novelty_need - before
        self.mood_events = (recent + [{"kind": kind, "ts": now}])[-8:]
        self._derive()

    def mood_hear(self, text, familiar=False) -> None:
        """Observe on a copy, then apply a bounded share of its emotional movement."""
        text = str(text or "").strip()
        if not text:
            return
        self._decay_to_now()
        probe = copy.deepcopy(self)
        probe._rng = __import__("random").Random(0)
        probe.observe(text)
        weight = 1.0 if familiar else MOOD_BYSTANDER_WEIGHT
        fingerprint = _fingerprint(re.sub(r"\s+", "", text)[:120])
        now = time.time()
        previous = getattr(self, "_mood_heard", None)
        if (previous and now - previous[0] < MOOD_REPEAT_SECONDS
                and _fingerprint_similarity(previous[1], fingerprint) >= .65):
            weight *= MOOD_REPEAT_FACTOR
        self._mood_heard = (now, fingerprint)
        for name in ("v", "a", "d", "social"):
            delta = (float(getattr(probe, name)) - float(getattr(self, name))) * weight
            delta = max(-MOOD_EVENT_LIMIT * weight, min(MOOD_EVENT_LIMIT * weight, delta))
            low = -1.0 if name in ("v", "d") else 0.0
            setattr(self, name, _clip(getattr(self, name) + delta, low, 1.0))
        self._derive()

    def _trust(self) -> float:
        """ams-life: no global trust. The trust in the person she is answering, while
        one observe() runs (it is passed in, never kept), else neutral."""
        t = getattr(self, "_partner_trust", None)
        return 0.5 if t is None else float(t)

    def _lexicon_deltas(self, t: str):
        """Mood deltas from the emotion word lists (negation-aware), and the labels hit."""
        v_delta, a_delta, d_delta, social_delta = 0.0, 0.0, 0.0, 0.0
        _hits = []
        for label, words in LEX.items():
            if not any(self._word_hit(t, w) for w in words):
                continue
            _hits.append(label)
            if label == "joy":
                v_delta += 0.12
                a_delta += 0.05
                d_delta += 0.04
                social_delta += 0.03
            elif label == "sadness":
                v_delta -= 0.14
                a_delta -= 0.03
                d_delta -= 0.05
            elif label == "loneliness":
                v_delta -= 0.12
                a_delta -= 0.03
                d_delta -= 0.04
                social_delta -= 0.16
            elif label == "anger":
                v_delta -= 0.12
                a_delta += 0.15
                d_delta += 0.10
                social_delta -= 0.05
            elif label == "fear":
                v_delta -= 0.16
                a_delta += 0.14
                d_delta -= 0.12
                social_delta -= 0.03
        return v_delta, a_delta, d_delta, social_delta, _hits

    def _intensity(self) -> float:
        """Normalized current emotional intensity (0..1)."""
        v = abs(float(getattr(self, "v", 0.0)))
        a = float(getattr(self, "a", 0.5))
        d = abs(float(getattr(self, "d", 0.5)) - 0.5) * 2.0
        soc = abs(float(getattr(self, "social", 0.5)) - 0.5) * 2.0
        stress = float(getattr(self, "stress", 0.0))
        return max(0.0, min(1.0, 0.30 * v + 0.30 * a + 0.20 * stress + 0.10 * d + 0.10 * soc))

    def _goal_signature(self, g: dict) -> str:
        try:
            return "、".join([str(g.get("name") or "")] + [str(x) for x in (g.get("keywords") or ())[:6]])
        except Exception:
            return str(g.get("name") or "")

    def _goal_evidence(self, g: dict, local_text: str, context_text: str, own_lines=()) -> float:
        """Evidence that a goal is active, from this turn plus retrieved context.

        Local keyword hits are only one channel; memory / self-narrative text is
        compared against the goal signature so relevance is not keyword-only.
        """
        try:
            t = str(local_text or "")
            ctx = str(context_text or "")
            sig = self._goal_signature(g)
            terms = tuple(g.get("keywords") or ())
            terms += tuple((getattr(self, "goal_context_terms", {}) or {}).get(str(g.get("key") or ""), ()))
            hits = sum(1 for w in terms if w and str(w) in t)
            local = min(1.0, 0.35 + 0.18 * hits) if hits else 0.0
            local = max(local, self._text_similarity(t, sig) * 0.75)
            learned = 0.0
            if ctx:
                term_hits = [w for w in terms if w and str(w) in ctx]
                coverage = len(term_hits) / max(1, len(terms))
                density = min(1.0, len(term_hits) / 5.0)
                learned = max(self._text_similarity(ctx[:900], sig) * 1.6,
                              min(1.0, 0.5 * density + 0.9 * coverage))
                for _txt in list(own_lines or ())[-12:]:
                    _txt = str(_txt or "")
                    if _txt and _txt in ctx:
                        learned = max(learned, self._text_similarity(_txt, sig) * 0.8)
            return max(0.0, min(1.0, max(local, 0.75 * learned)))
        except Exception:
            return 0.0

    def _resolve_goal_conflict(self, scores=None) -> None:
        """Pick a focus among active goals: high priority and low progress win."""
        scores = scores if isinstance(scores, dict) else dict(getattr(self, "goal_scores", {}) or {})
        cand = []
        for g in getattr(self, "goals", []) or []:
            if not isinstance(g, dict):
                continue
            key = str(g.get("key") or "")
            rel = float(scores.get(key, 0.0) or 0.0)
            if rel < 0.25:
                continue
            try:
                pri = float(g.get("priority", 0.5) or 0.5)
                prog = max(0.0, min(1.0, float(g.get("progress", 0.0) or 0.0)))
            except Exception:
                pri, prog = 0.5, 0.0
            cand.append((pri * (1.0 - prog), rel, g))
        if not cand:
            self.goal_focus = ""
            self.goal_conflict = []
            return
        cand.sort(key=lambda x: (x[0], x[1]), reverse=True)
        self.goal_focus = str(cand[0][2].get("name") or "")
        self.goal_conflict = [str(x[2].get("name") or "") for x in cand[1:]][:4]

    def _update_goals(self, text: str, context: str = "") -> None:
        t = str(text or "")
        ctx = str(context or "")
        scores = {}
        for g in getattr(self, "goals", []) or []:
            if not isinstance(g, dict):
                continue
            key = str(g.get("key") or "")
            scores[key] = round(self._goal_evidence(g, t, ctx), 3)
        self.goal_scores = scores
        # Deterministic priority learning: repeated evidence raises a goal,
        # neglect decays it slowly (bounded EMA; no LLM involved).
        try:
            for g in getattr(self, "goals", []) or []:
                if not isinstance(g, dict):
                    continue
                _key = str(g.get("key") or "")
                _rel = float(scores.get(_key, 0.0) or 0.0)
                memory_meta.update_goal_priority(
                    g, hit=(_rel > 0.05), relevance=_rel)
        except Exception:
            pass
        best = max(scores.values()) if scores else 0.0
        self.appraisal["goal_relevance"] = round(best, 3)
        self._resolve_goal_conflict(scores)
        _pos = sum(1 for w in ("谢谢", "喜欢", "陪", "开心", "信任", "爱") if w in t)
        _neg = sum(1 for w in ("废物", "滚", "闭嘴", "讨厌", "没用", "难受") if w in t)
        self.appraisal["norm_compatibility"] = round(max(0.0, min(1.0, 0.5 + 0.12 * _pos - 0.18 * _neg)), 3)
        self.appraisal["expectedness"] = round(1.0 - float(self.appraisal.get("novelty", 0.0) or 0.0), 3)
        self.appraisal["urgency"] = round(float(getattr(self, "a", 0.5)), 3)

    def _advance_goals(self, v_delta: float = 0.0, social_delta: float = 0.0) -> None:
        """Goal progress follows the interaction outcome, not a fixed step."""
        focus_key = ""
        focus_name = str(getattr(self, "goal_focus", "") or "")
        if not focus_name:
            return
        for g in getattr(self, "goals", []) or []:
            if str(g.get("name") or "") == focus_name:
                focus_key = str(g.get("key") or "")
                break
        if not focus_key:
            return
        try:
            rel = float((getattr(self, "goal_scores", {}) or {}).get(focus_key, 0.0) or 0.0)
            if rel <= 0.0:
                return
            gain = (0.004 * rel
                    + 0.060 * max(0.0, float(v_delta))
                    + 0.040 * max(0.0, float(social_delta))
                    - 0.060 * max(0.0, -float(v_delta)))
            # Stage-2 C9: appraisal/emotion now feeds goal progress (real loop),
            # gated by bio_feedback_loops; default OFF keeps 1.2.98 unchanged.
            if getattr(self, "bio_feedback_loops", False):
                try:
                    _coping = float((getattr(self, "appraisal", {}) or {}).get("coping", 0.5) or 0.5)
                    _goal_rel = float((getattr(self, "appraisal", {}) or {}).get("goal_relevance", 0.5) or 0.5)
                    gain += 0.02 * ((_coping - 0.5) + (_goal_rel - 0.5))
                except Exception:
                    pass
            gain = max(-0.06, min(0.08, gain))
            for g in self.goals:
                if str(g.get("key") or "") != focus_key:
                    continue
                g["progress"] = round(max(0.0, min(1.0, float(g.get("progress", 0.0) or 0.0) + gain)), 4)
                g["last_update"] = round(__import__("time").time(), 3)
                try:
                    memory_meta.update_goal_priority(
                        g, hit=(gain >= 0.0), relevance=min(1.0, rel + max(0.0, gain)))
                except Exception:
                    pass
                break
        except Exception:
            pass

    def bind_goal_context(self, memory_text: str = "", self_model=None, recent=None, text: str = "",
                          own_lines=None) -> None:
        """Fuse retrieved memory / self narrative / recent turns into goal relevance.

        ams-life: `recent` and `own_lines` (her latest replies) come from the
        chat window she is in; the body itself keeps no text.
        """
        try:
            ctx_parts = [str(memory_text or "")]
            if isinstance(self_model, dict):
                ctx_parts.append(str(self_model.get("narrative") or ""))
                ctx_parts.append("、".join(str(x) for x in (self_model.get("consistency") or [])[:5]))
            if isinstance(recent, (list, tuple)):
                ctx_parts.extend(str(x)[:200] for x in recent[:8])
            ctx = "\n".join([p for p in ctx_parts if p])
            if not ctx.strip():
                return
            base = dict(getattr(self, "goal_scores", {}) or {})
            for g in getattr(self, "goals", []) or []:
                if not isinstance(g, dict):
                    continue
                key = str(g.get("key") or "")
                rel = self._goal_evidence(g, str(text or ""), ctx, own_lines or ())
                base[key] = round(max(float(base.get(key, 0.0) or 0.0), rel), 3)
            self.goal_scores = base
            if base:
                self.appraisal["goal_relevance"] = round(min(1.0, max(base.values())), 3)
            self._resolve_goal_conflict(base)
        except Exception:
            pass

    def _update_coping(self, pre_stress: float) -> None:
        delta = float(getattr(self, "stress", 0.2)) - float(pre_stress)
        success = 0.5 - 0.8 * delta + 0.15 * (float(getattr(self, "social", 0.5)) - 0.5)
        success = max(0.0, min(1.0, success))
        self.coping_history = (list(getattr(self, "coping_history", [])) + [success])[-40:]
        if self.coping_history:
            self.appraisal["coping"] = round(sum(self.coping_history) / len(self.coping_history), 3)

    @staticmethod
    def _cosine_static(a, b) -> float:
        try:
            aa = [float(x) for x in (a or [])]
            bb = [float(x) for x in (b or [])]
            if not aa or not bb:
                return 0.0
            return sum(x * y for x, y in zip(aa, bb))
        except Exception:
            return 0.0

    @staticmethod
    def _text_similarity(a: str, b: str) -> float:
        a = str(a or "")
        b = str(b or "")
        if not a or not b:
            return 0.0
        def grams(x):
            x = re.sub(r"\s+", "", x)
            return {x[i:i + 2] for i in range(max(0, len(x) - 1))}
        ga, gb = grams(a), grams(b)
        if not ga or not gb:
            return 0.0
        return len(ga & gb) / float(len(ga | gb))

    def _update_sec(self, v_delta: float, a_delta: float) -> None:
        self.sec = {
            "relevance": round(max(0.0, min(1.0, float(self.appraisal.get("goal_relevance", 0.0) or 0.0) * 0.7 + float(self.appraisal.get("novelty", 0.0) or 0.0) * 0.3)), 3),
            "implication": round(max(0.0, min(1.0, abs(float(v_delta)) * 2.0 + float(self.stress))), 3),
            "coping_potential": round(max(0.0, min(1.0, float(self.appraisal.get("coping", 0.5) or 0.5))), 3),
            "normative": round(max(0.0, min(1.0, float(self.appraisal.get("norm_compatibility", 0.5) or 0.5))), 3),
        }

    def _update_attention(self, v_delta: float, a_delta: float) -> None:
        novelty = float(self.appraisal.get("novelty", 0.0) or 0.0)
        goal = float(self.appraisal.get("goal_relevance", 0.0) or 0.0)
        salience = abs(float(v_delta)) * 1.8 + abs(float(a_delta)) * 1.2 + novelty * 0.4 + goal * 0.5
        self.attention = _clip(0.82 * float(self.attention) + 0.18 * _clip(salience, 0, 1), 0, 1)

    def _update_meta_emotion(self) -> None:
        e = str((self.labels or {}).get("emotion") or "neutral")
        t = self._trust()
        soc = float(self.social)
        if e == "sadness" and t < 0.55:
            self.meta_emotion = "对难过的羞耻"
        elif e == "anger" and soc < 0.50:
            self.meta_emotion = "对生气的羞耻"
        elif e == "fear" and float(self.appraisal.get("coping", 0.5)) < 0.45:
            self.meta_emotion = "对害怕的焦虑"
        elif e == "loneliness" and t >= 0.55:
            self.meta_emotion = "对孤独的承认"
        else:
            self.meta_emotion = ""

    def observe(self, text: str, embedding=None, relationship=None) -> None:
        """A message that woke her. ams-life: `relationship` is the record of the person
        she is answering; its trust is used during this call and not kept."""
        try:
            state = (relationship or {}).get("state") if isinstance(relationship, dict) else None
            self._partner_trust = _clip(float((state or {}).get("trust", 0.5) or 0.5), 0, 1)
        except Exception:
            self._partner_trust = None
        try:
            self._observe(text, embedding, relationship)
        finally:
            self._partner_trust = None

    def _observe(self, text: str, embedding=None, relationship=None) -> None:
        self._decay_to_now()
        self._query_embedding = embedding
        _pre_stress = float(self.stress)
        t = str(text or "")
        self._update_goals(t)
        _event_key = ""
        v_delta, a_delta, d_delta, social_delta, _hits = self._lexicon_deltas(t)
        # Short-term habituation: repeated equivalent emotional stimuli decay.
        _now = time.time()
        # B-T06: generic novelty history (also covers non-emotional repeated text).
        try:
            # ams-life: a fingerprint of what was said, never the words (see _fingerprint)
            _novelty_text = _fingerprint(re.sub(r"\s+", "", t)[:160])
            if _novelty_text:
                _hist = getattr(self, "_novelty_history", [])
                _seen_before = any(
                    _fingerprint_similarity(_novelty_text, x) >= 0.65
                    for x in _hist[-12:])
                if _seen_before:
                    self.boredom = _clip(self.boredom + 0.06 * (1.0 - self.boredom), 0.0, 1.0)
                    self.novelty_need = _clip(self.novelty_need + 0.03 * (1.0 - self.novelty_need), 0.0, 1.0)
                else:
                    self.boredom = _clip(self.boredom - 0.08, 0.0, 1.0)
                    self.novelty_need = _clip(0.94 * self.novelty_need + 0.06 * 0.5, 0.0, 1.0)
                self._novelty_history = (_hist + [_novelty_text])[-20:]
        except Exception:
            pass
        # Batch4 B5: information-gap curiosity proxy. Question/unknown cues raise
        # a bounded EMA that the homeostasis layer reads as extra curiosity.
        try:
            _question_cue = ("?" in t or "？" in t or any(
                w in t for w in ("什么", "谁", "为什么", "怎么", "哪", "多少", "吗", "如何")))
            self.info_gap = _clip(
                0.85 * float(getattr(self, "info_gap", 0.0))
                + 0.15 * (1.0 if _question_cue else 0.0), 0.0, 1.0)
        except Exception:
            self.info_gap = 0.0
        self.stimuli = [x for x in (getattr(self, "stimuli", []) or [])
                        if _now - float(x.get("ts", 0) or 0) <= float(getattr(self, "stimulus_decay_seconds", 300))]
        if _hits:
            _labels = tuple(sorted(set(_hits)))
            _norm = _fingerprint(re.sub(r"\s+", "", t)[:120])
            _item = None
            for _cand in self.stimuli:
                if _event_key:
                    if str(_cand.get("event_key", "")) != _event_key:
                        continue
                    _item = _cand
                    break
                if tuple(_cand.get("labels") or ()) != _labels:
                    continue
                if _fingerprint_similarity(_norm, _cand.get("fp")) >= 0.55:
                    _item = _cand
                    break
            if _item:
                _gap = max(0.0, _now - float(_item.get("ts", _now)))
                try:
                    _count = float(_item.get("n", 0) or 0) * math.exp(-_gap / max(30.0, float(getattr(self, "stimulus_decay_seconds", 300))))
                except Exception:
                    _count = 0.0
            else:
                _count = 0.0
            _hab = 1.0 / (1.0 + float(getattr(self, "stimulus_habituation", 0.75)) * _count)
            _novelty = float((getattr(self, "appraisal", {}) or {}).get("novelty", 0.0) or 0.0)
            _hab *= max(0.25, 1.0 - 0.6 * _novelty)
            # Batch4 B1: sensitization is the dual of habituation. Only strong
            # negative impulses (v_delta <= -0.12) repeated with >=0.55 text
            # similarity get a gain: 1 + 0.15 * sum(0.5 ** (age_h / 24h)),
            # capped at 1.25. Weak/neutral stimuli keep _sens = 1.0; the final
            # impulse is base * _hab * _sens (habituation still applies).
            _sens = 1.0
            try:
                _prior_sens = [x for x in (getattr(self, "_sensitization_history", []) or [])
                               if isinstance(x, dict)
                               and _now - float(x.get("ts", 0) or 0) <= SENSITIZATION_HISTORY_MAX_AGE]
                if v_delta <= SENSITIZATION_STRONG_NEG_DV:
                    _rep = 0.0
                    for _old in _prior_sens:
                        if _fingerprint_similarity(_norm, _old.get("fp")) < 0.55:
                            continue
                        _age_h = max(0.0, _now - float(_old.get("ts", 0) or 0)) / 3600.0
                        _rep += 0.5 ** (_age_h / SENSITIZATION_HALF_LIFE_HOURS)
                    _sens = min(SENSITIZATION_MAX, 1.0 + SENSITIZATION_STEP * _rep)
                    _prior_sens.append({"fp": _norm, "ts": _now})
                self._sensitization_history = _prior_sens[-SENSITIZATION_HISTORY_MAX:]
            except Exception:
                _sens = 1.0
            if _item:
                _item["n"] = _count + 1
                _item["ts"] = _now
            else:
                self.stimuli.append({"labels": _labels, "fp": _norm, "n": 1, "ts": _now, "event_key": _event_key})
            v_delta *= _hab * _sens
            a_delta *= _hab * _sens
            d_delta *= _hab * _sens
            social_delta *= _hab * _sens
            if _item:
                # Repeated equivalent stimulus: boredom rises, novelty need rises.
                self.boredom = _clip(self.boredom + (0.05 + 0.03 * min(3.0, _count)) * (1.0 - self.boredom), 0.0, 1.0)
                self.novelty_need = _clip(self.novelty_need + 0.04 * (1.0 - self.novelty_need), 0.0, 1.0)
            else:
                # New stimulus: boredom falls, novelty need eases toward baseline.
                self.boredom = _clip(self.boredom - 0.08, 0.0, 1.0)
                self.novelty_need = _clip(0.92 * self.novelty_need + 0.08 * 0.5, 0.0, 1.0)
        # B-T07: boundary pressure/refusal readiness from explicit command cues.
        _text_b = str(t or "")
        _commands = sum(1 for w in ("必须", "立刻", "马上", "服从", "不许", "闭嘴", "滚", "废物", "没用", "就该") if w in _text_b)
        _polite = sum(1 for w in ("请", "可以", "愿意", "谢谢", "麻烦") if w in _text_b)
        self.boundary_pressure = _clip(0.86 * self.boundary_pressure + 0.14 * min(1.0, _commands) - 0.04 * min(1.0, _polite), 0.0, 1.0)
        self.refusal_readiness = _clip(
            0.78 * self.refusal_readiness + 0.30 * self.boundary_pressure * min(1.0, _commands)
            + 0.08 * self.stress - 0.05 * min(1.0, _polite), 0.0, 1.0)
        # B-T09: estimate other's valence from the stimulus response, couple with dampening.
        _other_v = _clip(v_delta * 2.5, -1.0, 1.0)
        _gain = _clip(float(getattr(self, "profile", {}).get("contagion_gain", 0.10) or 0.10), 0.0, 0.6)
        _reg = str(getattr(self, "regulation", "none") or "none").lower()
        _damp = 0.55 if _reg in ("reappraise", "reframe") else (0.75 if _reg in ("suppress", "suppression") else 1.0)
        _coupling = _clip(_gain * _damp * abs(_other_v), 0.0, 1.0)
        self.interpersonal = {"other_valence_est": round(_other_v, 4),
                              "coupling": round(_coupling, 4), "dampening": round(_damp, 3)}
        self.v = _clip(self.v + 0.05 * _coupling * _other_v, -1, 1)
        self.a = _clip(self.a + 0.02 * _coupling * abs(_other_v), 0, 1)
        self.v = _clip(0.7 * self.v + 0.3 * v_delta, -1, 1)
        self.a = _clip(0.8 * self.a + 0.2 * (0.4 + a_delta), 0, 1)
        self.d = _clip(0.8 * self.d + 0.2 * (0.55 + d_delta), -1, 1)
        self.social = _clip(0.8 * self.social + 0.2 * (0.55 + social_delta), 0, 1)
        # Affective inertia: recent impulses keep pushing in their direction.
        self.momentum["v"] = _clip(0.75 * float(self.momentum.get("v", 0.0)) + 0.25 * v_delta, -1, 1)
        self.momentum["a"] = _clip(0.75 * float(self.momentum.get("a", 0.0)) + 0.25 * a_delta, -1, 1)
        self.momentum["d"] = _clip(0.75 * float(self.momentum.get("d", 0.0)) + 0.25 * d_delta, -1, 1)
        self.momentum["social"] = _clip(0.75 * float(self.momentum.get("social", 0.0)) + 0.25 * social_delta, -1, 1)
        self.v = _clip(self.v + 0.16 * self.momentum["v"], -1, 1)
        self.a = _clip(self.a + 0.16 * self.momentum["a"], 0, 1)
        self.d = _clip(self.d + 0.16 * self.momentum["d"], -1, 1)
        self.social = _clip(self.social + 0.16 * self.momentum["social"], 0, 1)
        # Intensity raises noise amplitude, but a dimension already near its
        # ceiling receives less effective noise (saturation).
        _int = self._intensity()
        _amp = 0.010 + 0.055 * _int
        self.v = _clip(self.v + self._rng.gauss(0, _amp * (1.0 - 0.75 * abs(self.v))), -1, 1)
        self.a = _clip(self.a + self._rng.gauss(0, _amp * (1.0 - 0.55 * self.a)), 0, 1)
        self.d = _clip(self.d + self._rng.gauss(0, _amp * 0.6 * (1.0 - 0.65 * abs(self.d))), -1, 1)
        self.social = _clip(self.social + self._rng.gauss(0, _amp * 0.5 * (1.0 - 0.65 * self.social)), 0, 1)
        # Reflection buffer: impulse proportional to intensity, then decays;
        # feedback is attenuated when the destination is already high.
        _ref_gain = 0.10 + 0.25 * _int
        self.reflection["v"] = _clip(0.90 * float(self.reflection.get("v", 0.0)) + _ref_gain * v_delta, -1, 1)
        self.reflection["a"] = _clip(0.88 * float(self.reflection.get("a", 0.0)) + _ref_gain * a_delta, -1, 1)
        self.reflection["d"] = _clip(0.92 * float(self.reflection.get("d", 0.0)) + _ref_gain * 0.6 * d_delta, -1, 1)
        self.reflection["social"] = _clip(0.92 * float(self.reflection.get("social", 0.0)) + _ref_gain * 0.6 * social_delta, 0, 1)
        self.v = _clip(self.v + self.reflection["v"] * (1.0 - 0.7 * abs(self.v)), -1, 1)
        self.a = _clip(self.a + self.reflection["a"] * (1.0 - 0.5 * self.a), 0, 1)
        self.d = _clip(self.d + self.reflection["d"] * (1.0 - 0.6 * abs(self.d)), -1, 1)
        self.social = _clip(self.social + self.reflection["social"] * (1.0 - 0.6 * self.social), 0, 1)
        # Opponent process (Solomon & Corbit): the after-reaction builds in the
        # opposite direction and decays slowly, producing an affective rebound.
        _deltas = {"v": v_delta, "a": a_delta, "d": d_delta, "social": social_delta}
        for _k in ("v", "a", "d", "social"):
            _old = float(self.opponent.get(_k, 0.0))
            self.opponent[_k] = _clip(0.86 * _old - 0.22 * _deltas[_k], -1, 1)
        self.v = _clip(self.v + float(getattr(self, "opponent_gain", 0.10)) * self.opponent["v"], -1, 1)
        self.a = _clip(self.a + float(getattr(self, "opponent_gain", 0.10)) * self.opponent["a"], 0, 1)
        self.d = _clip(self.d + float(getattr(self, "opponent_gain", 0.10)) * self.opponent["d"], -1, 1)
        self.social = _clip(self.social + float(getattr(self, "opponent_gain", 0.10)) * self.opponent["social"], 0, 1)
        self._derive()
        self._update_coping(_pre_stress)
        # Stage-2 C8: goal progress writes back to appraisal/affect (real loop),
        # gated by bio_feedback_loops; default OFF is a pure 1.2.98 no-op.
        _progress_before = 0.0
        if getattr(self, "bio_feedback_loops", False):
            try:
                _focus = str(getattr(self, "goal_focus", "") or "")
                for _g in (getattr(self, "goals", []) or []):
                    if isinstance(_g, dict) and str(_g.get("name") or "") == _focus:
                        _progress_before = float(_g.get("progress", 0.0) or 0.0)
                        break
            except Exception:
                _progress_before = 0.0
        self._advance_goals(v_delta, social_delta)
        if getattr(self, "bio_feedback_loops", False):
            try:
                _focus = str(getattr(self, "goal_focus", "") or "")
                _progress_after = _progress_before
                for _g in (getattr(self, "goals", []) or []):
                    if isinstance(_g, dict) and str(_g.get("name") or "") == _focus:
                        _progress_after = float(_g.get("progress", 0.0) or 0.0)
                        break
                _pdelta = _progress_after - _progress_before
                if abs(_pdelta) > 1e-9:
                    _apr = self.appraisal if isinstance(self.appraisal, dict) else {}
                    _apr["coping"] = round(_clip(
                        float(_apr.get("coping", 0.5) or 0.5) + 0.30 * _pdelta,
                        0.0, 1.0), 3)
                    _apr["goal_relevance"] = round(_clip(
                        float(_apr.get("goal_relevance", 0.5) or 0.5)
                        + 0.20 * max(0.0, _pdelta), 0.0, 1.0), 3)
                    self.v = _clip(self.v + 0.20 * _pdelta, -1.0, 1.0)
                    self.stress = _clip(self.stress - 0.10 * max(0.0, _pdelta), 0.0, 1.0)
                    self.appraisal = _apr
            except Exception:
                pass
        self._update_attention(v_delta, a_delta)
        self._update_sec(v_delta, a_delta)
        self._update_meta_emotion()
        if not getattr(self, "autonomy_enabled", False):
            # Legacy noise update (1.2.98). When autonomy is enabled, the only
            # noise update point is noise_tick() driven by the background tick.
            for k in self.noise:
                self.noise[k] = _clip(0.82 * self.noise[k] + self._rng.gauss(0, 0.045), -0.3, 0.3)
            self.noise["valence"] = _clip(0.7 * self.noise["valence"] + 0.3 * v_delta, -0.3, 0.3)
            self.noise["stress"] = _clip(0.8 * self.noise["stress"] + 0.2 * (self.stress - 0.2), -0.3, 0.3)
        self.echo_trace = _clip(0.88 * self.echo_trace + 0.12 * (self.v - self.stress * 0.5), -1, 1)
        self.echo = _clip(0.7 * self.echo + 0.3 * self.echo_trace, -1, 1)
        upper = _clip(0.6 * max(0.0, self.v) + 0.2 * self._trust(), 0, 1)
        lower = _clip(0.6 * max(0.0, -self.v) + 0.3 * self.stress, 0, 1)
        self.ripple = {"upper": round(upper, 3), "lower": round(lower, 3),
                       "overlap": round(min(upper, lower), 3), "energy": round((upper + lower) / 2, 3)}
        self.spiking = {"rate": round(0.02 + self.energy * 0.08, 3),
                        "variance": round(0.01 + self.stress * 0.05, 4),
                        "ei": round(0.2 + self._trust() * 0.3, 3)}
        self.ticks += 1
        self.infer_labels(force=True)
        try:
            homeostasis.step(self, relationship=relationship)
        except Exception:
            pass
        # Task-15: affect tick + homeostasis drive deviation feed L1 noise.
        try:
            self.integrate_noise(
                "emotion_tick",
                stress=0.004 * float(self.stress),
                energy=0.003 * (0.5 - float(self.energy)),
                social=0.003 * (0.5 - float(self.social)),
                valence=0.004 * float(self.v))
            _homeo = self.homeostasis if isinstance(self.homeostasis, dict) else {}
            _l_int = float(_homeo.get("L_int", 0.0) or 0.0)
            _drives = _homeo.get("drives") if isinstance(_homeo.get("drives"), dict) else {}
            _points = _homeo.get("set_points") if isinstance(_homeo.get("set_points"), dict) else {}
            self.integrate_noise(
                "homeostasis",
                energy=0.004 * _l_int,
                social=0.004 * abs(float(_drives.get("social", 0.5))
                                   - float(_points.get("social", 0.55))),
                attention=0.002 * _l_int)
        except Exception:
            pass

    def _spectrum(self) -> list:
        v = (float(getattr(self, "v", 0.0)) + 1.0) / 2.0
        a = float(getattr(self, "a", 0.5))
        d = (float(getattr(self, "d", 0.5)) + 1.0) / 2.0
        soc = float(getattr(self, "social", 0.5))
        out = []
        _emo_bias = {
            "sadness": {"disappointment": 0.42, "empathic_pain": 0.36, "guilt": 0.18},
            "anger": {"anger": 0.52, "contempt": 0.30, "disgust": 0.18},
            "fear": {"fear": 0.52, "anxiety": 0.42, "horror": 0.24},
            "loneliness": {"empathic_pain": 0.42, "disappointment": 0.36, "nostalgia": 0.24},
            "joy": {"joy": 0.52, "contentment": 0.36, "amusement": 0.24},
        }.get(str((self.labels or {}).get("emotion") or ""), {})
        _protos = {}
        try:
            _protos = self._calibrate_spectrum_prototypes()
        except Exception:
            _protos = {}
        for key, cn, sv, sa, sd, ss in EMOTION_SPECTRUM:
            _p = _protos.get(key)
            if _p:
                sv, sa, sd, ss = _p
            dv = v - ((sv + 1.0) / 2.0)
            dd = d - ((sd + 1.0) / 2.0)
            dist = (dv * dv * 1.2 + (a - sa) ** 2 + dd * dd + (soc - ss) ** 2) ** 0.5
            dist = max(0.0, dist - float(_emo_bias.get(key, 0.0)))
            out.append((round(dist, 3), key, cn))
        out.sort(key=lambda x: x[0])
        return [{"key": k, "name": n, "distance": dist} for dist, k, n in out[:3]]

    def _spectrum_probs(self) -> list:
        try:
            out = []
            for it in self._spectrum():
                dist = max(0.001, float(it.get("distance", 1.0)))
                out.append({"key": it.get("key"), "name": it.get("name"), "p": round(1.0 / dist, 4)})
            total = sum(x["p"] for x in out) or 1.0
            for x in out:
                x["p"] = round(x["p"] / total, 4)
            return out
        except Exception:
            return []

    def _calibrate_spectrum_prototypes(self) -> dict:
        """Cowen & Keltner (2017) style prototype calibration.

        Each EMOTION_SPECTRUM anchor is mixed with the centroid of this core's
        own state history for the matching emotion family. Pure anchors are
        used until at least two observations exist, so a single turn cannot
        move the emotion map. Deterministic: no RNG, no LLM call.
        """
        anchors = {key: (sv, sa, sd, ss) for key, cn, sv, sa, sd, ss in EMOTION_SPECTRUM}
        sums = {}
        counts = {}
        hist = list(getattr(self, "history", []) or [])[-80:]
        cur_d = float(getattr(self, "d", 0.55))
        cur_soc = float(getattr(self, "social", 0.55))
        for h in hist:
            if not isinstance(h, dict):
                continue
            emo = str(h.get("emotion") or "").strip()
            keys = SPECTRUM_FAMILY.get(emo)
            if not keys:
                continue
            try:
                w = max(0.05, min(1.0, float(h.get("intensity", 0.5) or 0.5)))
            except Exception:
                w = 0.5
            try:
                hv = float(h.get("v", 0.0))
                ha = float(h.get("a", 0.5))
            except Exception:
                continue
            try:
                hd = float(h.get("d", cur_d))
            except Exception:
                hd = cur_d
            try:
                hs = float(h.get("social", cur_soc))
            except Exception:
                hs = cur_soc
            for key in keys:
                if key not in anchors:
                    continue
                acc = sums.setdefault(key, [0.0, 0.0, 0.0, 0.0, 0.0])
                acc[0] += hv * w
                acc[1] += ha * w
                acc[2] += hd * w
                acc[3] += hs * w
                acc[4] += w
                counts[key] = int(counts.get(key, 0) or 0) + 1
        out = {}
        for key, anchor in anchors.items():
            acc = sums.get(key)
            n = int(counts.get(key, 0) or 0)
            if acc and n >= 2 and acc[4] > 0:
                alpha = min(0.35, 0.06 * n)
                centroid = [acc[0] / acc[4], acc[1] / acc[4], acc[2] / acc[4], acc[3] / acc[4]]
                out[key] = tuple((1.0 - alpha) * anchor[i] + alpha * centroid[i] for i in range(4))
            else:
                out[key] = anchor
        self._spectrum_calibration_meta = {
            "samples": len(hist),
            "families": len({str(h.get("emotion") or "") for h in hist
                             if SPECTRUM_FAMILY.get(str(h.get("emotion") or ""))}),
            "calibrated": sum(1 for k in anchors if int(counts.get(k, 0) or 0) >= 2),
        }
        return out

    def _compound_emotion(self) -> str:
        v = float(getattr(self, "v", 0.0))
        a = float(getattr(self, "a", 0.5))
        d = float(getattr(self, "d", 0.5))
        soc = float(getattr(self, "social", 0.5))
        trust = self._trust()
        w = {
            "joy": max(0.0, v) * max(0.2, a),
            "trust": trust * max(0.0, 1.0 - abs(v)),
            "sadness": max(0.0, -v) * (1.0 - a * 0.5),
            "anger": max(0.0, -v) * a * max(0.0, d - 0.5) * 2.0,
            "fear": max(0.0, -v) * a * max(0.0, 0.5 - d) * 2.0,
            "loneliness": max(0.0, -v) * max(0.0, 0.7 - soc),
            "surprise": max(0.0, float(self.appraisal.get("novelty", 0.0) or 0.0)) * max(0.2, a),
            "anticipation": max(0.0, float(self.appraisal.get("goal_relevance", 0.0) or 0.0)) * max(0.2, a),
            "disgust": max(0.0, -v) * max(0.0, 1.0 - a) * max(0.0, 0.6 - soc),
        }
        top = sorted(w.items(), key=lambda kv: kv[1], reverse=True)[:2]
        if len(top) < 2 or top[1][1] < 0.08:
            return ""
        pair = frozenset((top[0][0], top[1][0]))
        names = {
            frozenset(("joy", "trust")): "亲近",
            frozenset(("joy", "fear")): "不安的期待",
            frozenset(("joy", "sadness")): "苦甜参半",
            frozenset(("joy", "anger")): "复杂",
            frozenset(("joy", "loneliness")): "热闹中的空",
            frozenset(("trust", "fear")): "顺从的不安",
            frozenset(("trust", "sadness")): "失落",
            frozenset(("trust", "anger")): "失望的怒",
            frozenset(("trust", "loneliness")): "想念",
            frozenset(("fear", "sadness")): "无助",
            frozenset(("fear", "anger")): "戒备",
            frozenset(("fear", "loneliness")): "被抛下",
            frozenset(("sadness", "anger")): "委屈",
            frozenset(("sadness", "loneliness")): "空落",
            frozenset(("anger", "loneliness")): "被排斥的怒",
        }
        names.update({
            frozenset(("joy", "surprise")): "惊喜",
            frozenset(("trust", "surprise")): "敬畏",
            frozenset(("fear", "surprise")): "惊骇",
            frozenset(("sadness", "surprise")): "意外失落",
            frozenset(("disgust", "surprise")): "错愕",
            frozenset(("anger", "surprise")): "暴怒",
            frozenset(("anticipation", "surprise")): "期待",
            frozenset(("joy", "anticipation")): "乐观",
            frozenset(("trust", "anticipation")): "希望",
            frozenset(("fear", "anticipation")): "焦虑",
            frozenset(("sadness", "anticipation")): "悲观",
            frozenset(("disgust", "anticipation")): "蔑视",
            frozenset(("anger", "anticipation")): "攻击性",
            frozenset(("joy", "disgust")): "幸灾乐祸",
            frozenset(("trust", "disgust")): "矛盾",
            frozenset(("fear", "disgust")): "厌恶恐惧",
            frozenset(("sadness", "disgust")): "懊悔",
            frozenset(("joy", "sadness")): "苦甜参半",
            frozenset(("trust", "anger")): "失望的怒",
            frozenset(("surprise", "anticipation")): "警觉",
            frozenset(("disgust", "anger")): "轻蔑",
            frozenset(("disgust", "sadness")): "嫌恶",
            frozenset(("disgust", "fear")): "恶心",
            frozenset(("disgust", "trust")): "勉强接受",
            frozenset(("surprise", "joy")): "惊喜",
            frozenset(("surprise", "fear")): "惊骇",
            frozenset(("anticipation", "joy")): "乐观",
            frozenset(("anticipation", "fear")): "焦虑",
        })
        return names.get(pair, "混合")

    def _regulation_rate(self, strategy: str, now: float = None) -> float:
        """G4: recency-weighted success rate for one regulation strategy.

        Raw uses/success/cost stay cumulative; the score is multiplied by an
        exponential recency weight derived from last_update (half-life
        REGULATION_STATS_HALF_LIFE_DAYS). Read-only: stats are never rewritten
        here, and legacy stats without last_update keep their old score.
        """
        try:
            st = (getattr(self, "regulation_stats", None) or {}).get(strategy) or {}
            uses = int(st.get("uses", 0) or 0)
            if uses <= 0:
                return 0.0
            success = float(st.get("success", 0) or 0)
            cost = float(st.get("cost", 0) or 0)
            score = success / uses - 0.05 * (cost / uses)
            last = st.get("last_update")
            if last is None:
                return score
            current = float(now if now is not None else time.time())
            elapsed_days = max(0.0, current - float(last)) / 86400.0
            return score * (0.5 ** (elapsed_days / REGULATION_STATS_HALF_LIFE_DAYS))
        except Exception:
            return 0.0

    def _choose_regulation(self) -> str:
        stress = float(getattr(self, "stress", 0.0))
        trust = self._trust()
        soc = float(getattr(self, "social", 0.5))
        arousal = float(getattr(self, "a", 0.5))
        attention = float(getattr(self, "attention", 0.5))
        emo = str(self.labels.get("emotion") or "neutral")
        if stress >= 0.65:
            if trust >= 0.55:
                return "seek_comfort"
            if soc <= 0.30:
                return "avoid"
            return "reappraise"
        _cands = []
        if emo in ("anger", "fear"):
            _cands = (["suppress", "reappraise", "distraction"] if soc < 0.50
                      else ["reappraise", "express", "distraction"])
            if arousal >= 0.72:
                _cands = ["distraction"] + _cands
        elif emo == "sadness":
            _cands = ["express", "reappraise", "seek_comfort", "distraction"]
        elif emo == "loneliness":
            _cands = ["seek_comfort", "avoid", "express", "distraction"]
        elif stress >= 0.45 and arousal >= 0.70 and attention < 0.55:
            _cands = ["distraction", "reappraise"]
        # Batch4 B2: affect labeling (naming the emotion) is the 7th strategy.
        # Deterministic trigger: spectrum top1 >= 0.45 and arousal >= 0.50.
        if _cands and arousal >= AFFECT_LABEL_MIN_AROUSAL:
            try:
                _top_p = max((float(x.get("p", 0.0) or 0.0)
                              for x in self._spectrum_probs() if isinstance(x, dict)),
                             default=0.0)
            except Exception:
                _top_p = 0.0
            try:
                _label_stats = (getattr(self, "regulation_stats", {}) or {}).get(
                    "label_emotion") or {}
                _last_label = _label_stats.get("last_update")
                if _last_label is None:
                    _label_ready = True
                else:
                    _label_ready = (time.time() - float(_last_label)
                                    >= AFFECT_LABEL_COOLDOWN_SECONDS)
            except Exception:
                _label_ready = True
            if _top_p >= AFFECT_LABEL_MIN_TOP_P and _label_ready:
                _cands = ["label_emotion"] + _cands
        if _cands:
            if getattr(self, "regulation_stats", None):
                _qs = (getattr(self, "_learning", {}) or {}).get("params", {}).get("regulation_q", {}) if getattr(self, "bio_learning", False) else {}
                _cands.sort(key=lambda s: self._regulation_rate(s) + (LEARNING_Q_WEIGHT * float((_qs or {}).get(s, 0.0) or 0.0)), reverse=True)
            return _cands[0]
        return "none"

    def _record_regulation(self, strategy: str, pre_stress: float) -> None:
        """Persist uses / success / cumulative stress change / cost + last_update."""
        if not strategy or strategy == "none":
            return
        try:
            stats = self.regulation_stats
            st = stats.setdefault(strategy, {"uses": 0, "success": 0, "stress_delta": 0.0, "cost": 0.0})
            uses = int(st.get("uses", 0) or 0) + 1
            delta = float(getattr(self, "stress", 0.0)) - float(pre_stress)
            st["uses"] = uses
            st["stress_delta"] = round(float(st.get("stress_delta", 0.0) or 0.0) + delta, 5)
            st["cost"] = round(float(st.get("cost", 0.0) or 0.0) + float(REGULATION_COST.get(strategy, 0.003)), 5)
            st["last_update"] = round(time.time(), 3)
            if getattr(self, "bio_learning", False):
                try:
                    # Daw 2011 Q-learning; min-sample N=5 + step cap 0.02 (review BLOCK-05).
                    r = max(-1.0, min(1.0, (-delta) * 10.0
                                      - 0.05 * float(REGULATION_COST.get(strategy, 0.003))
                                      + 0.10 * float(getattr(self, "a", 0.5))))
                    qs = self._learning.setdefault("params", {}).setdefault("regulation_q", {})
                    evidence = self._learning.setdefault("evidence", {}).setdefault("regulation_q", {})
                    ev = evidence.get(strategy) if isinstance(evidence.get(strategy), dict) else {"n": 0, "sum_pe": 0.0}
                    old_q = float(qs.get(strategy, 0.0) or 0.0)
                    ev["n"] = int(ev.get("n", 0) or 0) + 1
                    ev["sum_pe"] = float(ev.get("sum_pe", 0.0) or 0.0) + (r - old_q)
                    evidence[strategy] = ev
                    if int(ev.get("n", 0)) >= 5:
                        alpha = memory_meta.nassar_alpha(float(ev["sum_pe"]) / int(ev["n"]))
                        delta_q = max(-0.02, min(0.02, alpha * float(ev["sum_pe"]) / int(ev["n"])))
                        new_q = max(-1.0, min(1.0, old_q + delta_q))
                        qs[strategy] = round(new_q, 5)
                        evidence[strategy] = {"n": 0, "sum_pe": 0.0}
                        self._learning["updates_count"] = int(self._learning.get("updates_count", 0) or 0) + 1
                        self._learning["last_update"] = round(time.time(), 3)
                        log = self._learning.get("log") if isinstance(self._learning.get("log"), list) else []
                        log.append({"ts": round(time.time(), 3), "param": "regulation_q." + str(strategy),
                                    "old": round(old_q, 5), "new": round(new_q, 5),
                                    "reason": "delta_stress", "samples": 5})
                        self._learning["log"] = log[-20:]
                except Exception:
                    pass
            if delta <= 0.0005:
                st["success"] = int(st.get("success", 0) or 0) + 1
        except Exception:
            pass

    def _apply_regulation(self) -> None:
        r = self.regulation
        _pre_stress = float(self.stress)
        if r == "seek_comfort":
            self.social = _clip(self.social + 0.03, 0, 1)
            self.stress = _clip(self.stress - 0.02, 0, 1)
        elif r == "reappraise":
            self.stress = _clip(self.stress - 0.04, 0, 1)
            self.v = _clip(self.v + 0.015, -1, 1)
        elif r == "suppress":
            self.stress = _clip(self.stress + 0.01, 0, 1)
            self.v = _clip(self.v - 0.005, -1, 1)
        elif r == "avoid":
            self.social = _clip(self.social - 0.03, 0, 1)
        elif r == "express":
            self.v = _clip(self.v + 0.01, -1, 1)
            self.stress = _clip(self.stress - 0.01, 0, 1)
        elif r == "label_emotion":
            # Batch4 B2: name the feeling; deliberately tiny effects (not a
            # comfort button): v toward 0, arousal/stress slightly down.
            self.v = _clip(self.v + 0.005, -1, 1)
            self.a = _clip(self.a - 0.01, 0, 1)
            self.stress = _clip(self.stress - 0.005, 0, 1)
        elif r == "distraction":
            # Brief relief: lower arousal/stress now, but attention and the
            # current goal pay for it because the concern is left unaddressed.
            self.a = _clip(self.a - 0.06, 0, 1)
            self.stress = _clip(self.stress - 0.035, 0, 1)
            self.attention = _clip(self.attention - 0.05, 0, 1)
            _focus = str(getattr(self, "goal_focus", "") or "")
            for g in self.goals:
                if str(g.get("name") or "") == _focus:
                    g["progress"] = round(max(0.0, float(g.get("progress", 0) or 0) - 0.005), 5)
                    break
        self._derive()
        self._record_regulation(r, _pre_stress)

    def infer_labels(self, force: bool = False) -> None:
        """Derive labels from the biological state when the model omits them."""
        v = float(getattr(self, "v", 0.0))
        a = float(getattr(self, "a", 0.5))
        d = float(getattr(self, "d", 0.55))
        soc = float(getattr(self, "social", 0.55))
        stress = float(getattr(self, "stress", 0.0))
        energy = float(getattr(self, "energy", 0.8))
        trust = self._trust()
        inferred = {}
        if soc <= 0.47 and v <= 0.00:
            inferred["emotion"] = "loneliness"
        elif v >= 0.16 and a >= 0.40 and d >= 0.35:
            inferred["emotion"] = "joy"
        elif v <= -0.20 and a < 0.55:
            inferred["emotion"] = "sadness"
        elif v <= -0.12 and a >= 0.55 and d >= 0.50:
            inferred["emotion"] = "anger"
        elif v <= -0.08 and a >= 0.50 and d < 0.50:
            inferred["emotion"] = "fear"
        else:
            inferred["emotion"] = "neutral"
        if v >= 0.25 and soc >= 0.35:
            inferred["intent"] = "approach"
        elif v <= -0.25 or soc <= 0.30:
            inferred["intent"] = "withdraw"
        else:
            inferred["intent"] = "hold"
        if energy >= 0.68 and v >= 0.15:
            inferred["expression"] = "open"
        elif energy <= 0.35:
            inferred["expression"] = "short"
        else:
            inferred["expression"] = "normal"
        if soc <= 0.30:
            inferred["need"] = "space"
        elif stress >= 0.65:
            inferred["need"] = "vent" if trust >= 0.40 else "space"
        elif trust >= 0.60:
            inferred["need"] = "be_heard" if v <= 0.0 else "share"
        elif v <= -0.30:
            inferred["need"] = "space"
        else:
            inferred["need"] = "talk"
        inferred["energy"] = "high" if energy >= 0.70 else ("low" if energy <= 0.35 else "normal")
        inferred["stress"] = "overloaded" if stress >= 0.70 else ("tense" if stress >= 0.35 else "calm")
        for key, value in inferred.items():
            if force or not self.labels.get(key):
                self.labels[key] = value
        self.compound = self._compound_emotion()
        self.regulation = self._choose_regulation()
        self._apply_regulation()

    def intent(self) -> dict:
        labels = dict(getattr(self, "labels", {}) or {})
        return {
            "emotion": labels.get("emotion", "neutral"),
            "energy": labels.get("energy", "normal"),
            "stress": labels.get("stress", "calm"),
            "intent": labels.get("intent", "hold"),
            "expression": labels.get("expression", "normal"),
            "need": labels.get("need", "talk"),
            "dominance": round(self.d, 2),
            "social": round(self.social, 2),
            "compound": self.compound,
            "spectrum": self._spectrum(),
            "regulation": self.regulation,
        }

    def _recovery_speed(self) -> float:
        """Batch4 B4: contextual recovery-speed multiplier, bounded [0.8, 1.2].

        speed = clamp(0.85 + 0.30*recovery_rate
                      + 0.05*(2*coping_success - 1), 0.8, 1.2)
        Applied as HL/speed only to dimensions below baseline (v<0, a>0.40,
        social<0.55), so recovery is faster after rest/support and slower when
        recovery_rate is low. Deterministic, no LLM, no new stored field.
        """
        try:
            rate = _clip(float((getattr(self, "profile", {}) or {}).get(
                "recovery_rate", 0.62) or 0.62), 0.0, 1.0)
        except Exception:
            rate = 0.62
        success = 0.5
        try:
            stats = getattr(self, "regulation_stats", {}) or {}
            uses = sum(int(v.get("uses", 0) or 0) for v in stats.values()
                       if isinstance(v, dict))
            succ = sum(int(v.get("success", 0) or 0) for v in stats.values()
                       if isinstance(v, dict))
            if uses > 0:
                success = _clip(succ / uses, 0.0, 1.0)
        except Exception:
            success = 0.5
        speed = 0.85 + 0.30 * rate + 0.05 * (2.0 * success - 1.0)
        return max(RECOVERY_CONTEXT_MIN, min(RECOVERY_CONTEXT_MAX, speed))

    def _decay_to_now(self) -> None:
        now = __import__("time").time()
        try:
            dt_min = max(0.0, (now - float(getattr(self, "last_tick", now))) / 60.0)
        except Exception:
            dt_min = 0.0
        if dt_min < 0.5:
            return  # ams-life: last_tick stays, so these seconds count at the next decay
        _advance_needs(self, now - dt_min * 60.0, now)
        self.last_tick = now
        def factor(halflife):
            try:
                hl = max(1.0, float(halflife))
            except Exception:
                hl = 120.0
            return 0.5 ** (dt_min / hl)
        if hasattr(self, "_mood_stress"):
            self._mood_stress *= factor(MOOD_EVENT_HALF_LIFE_MINUTES)
        if hasattr(self, "_mood_energy"):
            self._mood_energy *= factor(MOOD_EVENT_HALF_LIFE_MINUTES)
        if hasattr(self, "_mood_novelty"):
            old = self._mood_novelty
            self._mood_novelty *= factor(MOOD_EVENT_HALF_LIFE_MINUTES)
            self.novelty_need = _clip(self.novelty_need + self._mood_novelty - old, 0, 1)
        _emo = str((getattr(self, "labels", {}) or {}).get("emotion") or "neutral")
        _ef = float((getattr(self, "emotion_decay_factors", {}) or {}).get(_emo, 1.0))
        # Batch4 B4: contextual recovery speed shortens the half-life only for
        # dimensions that are recovering toward baseline.
        _rec = self._recovery_speed()
        # ams-life: arousal settles a little higher when the chats around her are
        # lively and lower when they are quiet (instead of a day-night rhythm)
        _a_rest = 0.40 + 0.08 * (_clip(getattr(self, "ambient", 0.0), 0, 1) - 0.5)
        _v_rec = _rec if self.v < 0 else 1.0
        _a_rec = _rec if self.a > _a_rest else 1.0
        _soc_rec = _rec if self.social < 0.55 else 1.0
        self.v = _clip(self.v * factor(self.valence_decay_minutes * _ef / _v_rec), -1, 1)
        self.a = _clip(_a_rest + (self.a - _a_rest) * factor(
            self.arousal_decay_minutes * max(0.5, _ef) / _a_rec), 0, 1)
        self.d = _clip(0.55 + (self.d - 0.55) * factor(self.valence_decay_minutes * _ef), -1, 1)
        self.social = _clip(0.55 + (self.social - 0.55) * factor(
            self.social_decay_minutes * _ef / _soc_rec), 0, 1)
        self._derive()
        try:
            self._update_allostatic_load()
        except Exception:
            pass
        # ams-life: having talked fades (half in TALKED_HALF_LIFE_MIN); wanting to be
        # seen grows back toward 1 while nobody answers her (half in SEEN_HALF_LIFE_MIN)
        self.talked = _clip(float(getattr(self, "talked", 0.0)) * factor(TALKED_HALF_LIFE_MIN), 0, 1)
        self.seen_need = _clip(1.0 - (1.0 - float(getattr(self, "seen_need", 0.3)))
                               * factor(SEEN_HALF_LIFE_MIN), 0, 1)

    def record_talk(self, text: str = "") -> float:
        """ams-life: she said something (in any chat): "talked" goes up by its length."""
        self._decay_to_now()
        cost = 0.03 + 0.0004 * min(150, len(str(text or "")))
        self.talked = _clip(float(getattr(self, "talked", 0.0)) + cost, 0, 1)
        return cost

    def be_seen(self) -> None:
        """ams-life: someone answered her, called her or quoted her."""
        self._decay_to_now()
        self.seen_need = _clip(float(getattr(self, "seen_need", 0.3)) * SEEN_RELIEF, 0, 1)

    def set_ambient(self, value: float) -> None:
        """ams-life: how lively the chats around her are now (0 quiet .. 1 busy)."""
        self.ambient = _clip(value, 0, 1)

    def observe_own(self, text: str) -> None:
        """ams-life: her own reply moves her mood a little (half of hearing the same words),
        from the same word lists. No model self-report is used."""
        t = str(text or "")
        if not t:
            return
        self._decay_to_now()
        v_delta, a_delta, d_delta, social_delta, _hits = self._lexicon_deltas(t)
        if not _hits:
            return
        self.v = _clip(self.v + 0.5 * v_delta, -1, 1)
        self.a = _clip(self.a + 0.5 * a_delta, 0, 1)
        self.d = _clip(self.d + 0.5 * d_delta, -1, 1)
        self.social = _clip(self.social + 0.5 * social_delta, 0, 1)
        self._derive()
        self.infer_labels(force=True)

    def apply_memory_trace(self, v_delta: float = 0.0, stress_delta: float = 0.0) -> dict:
        """Single BioCore writer for L3 memory-trace nudges (bounded)."""
        try:
            dv = max(-0.05, min(0.05, float(v_delta or 0.0)))
        except Exception:
            dv = 0.0
        try:
            ds = max(-0.05, min(0.05, float(stress_delta or 0.0)))
        except Exception:
            ds = 0.0
        self.v = _clip(float(getattr(self, "v", 0.0)) + dv, -1.0, 1.0)
        self.stress = _clip(float(getattr(self, "stress", 0.0)) + ds, 0.0, 1.0)
        return {"v_delta": round(dv, 4), "stress_delta": round(ds, 4)}

    def record_reply(self, text: str = "", meta=None) -> None:
        try:
            emo = str((self.labels or {}).get("emotion") or "neutral")
            self.history.append({
                "ts": __import__("time").time(),
                "emotion": emo,
                "compound": str(self.compound or ""),
                "intensity": round(float(self._intensity()), 3),
                "v": round(float(self.v), 3),
                "a": round(float(self.a), 3),
                "d": round(float(self.d), 3),
                "social": round(float(self.social), 3),
            })
            if len(self.history) > 80:
                self.history = self.history[-80:]
        except Exception:
            pass

    def _update_allostatic_load(self) -> float:
        """Slow allostatic accumulation/recovery; bounded, tiny stress offset."""
        try:
            stress = _clip(self.stress, 0.0, 1.0)
            if stress > 0.55:
                self.allostatic_load = _clip(
                    self.allostatic_load + 0.01 * (stress - 0.55) * (1.0 - self.allostatic_load), 0.0, 1.0)
            else:
                self.allostatic_load = _clip(
                    self.allostatic_load - 0.004 * (0.55 - stress), 0.0, 1.0)
            if self.allostatic_load > 0:
                self.stress = _clip(self.stress + 0.005 * self.allostatic_load, 0.0, 1.0)
            return float(self.allostatic_load)
        except Exception:
            return 0.0

    def update_daily_digest(self, now=None, event_ids=None) -> dict:
        """Deterministic daily digest base; no narrative/LLM. Bounded to 30 days."""
        try:
            current = float(time.time() if now is None else now)
            date = time.strftime("%Y-%m-%d", time.localtime(current))
            accum = getattr(self, "_daily_accum", None)
            if not isinstance(accum, dict):
                accum = {"date": "", "n": 0, "v": 0.0, "a": 0.0, "stress": 0.0,
                         "emotions": {}, "ticks": 0, "event_ids": []}
            if accum.get("date") and accum.get("date") != date:
                if int(accum.get("n", 0) or 0) > 0:
                    emotions = accum.get("emotions") or {}
                    dominant = max(emotions.items(), key=lambda kv: kv[1])[0] if emotions else "neutral"
                    n = int(accum.get("n", 1) or 1)
                    self.daily_digests.append({
                        "date": str(accum.get("date")),
                        "event_ids": [str(x) for x in (accum.get("event_ids") or [])[-50:] if str(x)],
                        "mean_v": round(float(accum.get("v", 0.0) or 0.0) / n, 4),
                        "mean_a": round(float(accum.get("a", 0.0) or 0.0) / n, 4),
                        "mean_stress": round(float(accum.get("stress", 0.0) or 0.0) / n, 4),
                        "dominant_emotion": dominant,
                        "interaction_count": n,
                    })
                    self.daily_digests = self.daily_digests[-30:]
                accum = {"date": date, "n": 0, "v": 0.0, "a": 0.0, "stress": 0.0,
                         "emotions": {}, "ticks": 0, "event_ids": []}
            accum["date"] = date
            accum["n"] = int(accum.get("n", 0) or 0) + 1
            accum["v"] = float(accum.get("v", 0.0) or 0.0) + float(self.v)
            accum["a"] = float(accum.get("a", 0.0) or 0.0) + float(self.a)
            accum["stress"] = float(accum.get("stress", 0.0) or 0.0) + float(self.stress)
            _emo = str((self.labels or {}).get("emotion") or "neutral")
            emotions = accum.get("emotions") if isinstance(accum.get("emotions"), dict) else {}
            emotions[_emo] = int(emotions.get(_emo, 0) or 0) + 1
            accum["emotions"] = emotions
            accum["ticks"] = int(accum.get("ticks", 0) or 0) + 1
            if isinstance(event_ids, (list, tuple)):
                _eids = accum.get("event_ids") if isinstance(accum.get("event_ids"), list) else []
                for _eid in event_ids:
                    if str(_eid) and str(_eid) not in _eids:
                        _eids.append(str(_eid))
                accum["event_ids"] = _eids[-50:]
            self._daily_accum = accum
            return dict(accum)
        except Exception:
            return {}

    def integrate_noise(self, source: str = "", **deltas) -> dict:
        """L1 task-15: decayed addition into the 5-channel noise integrator.

        Only active when the plugin enabled proactive autonomy
        (core.autonomy_enabled). Default OFF is a pure no-op, so the legacy
        noise trajectory is unchanged. Channels decay 0.98 per integration and
        are clamped to ±NOISE_CLAMP. This is an L1 state update: callers only
        hand in module deltas; no caller reads it to bypass L1 decisions.
        """
        if not getattr(self, "autonomy_enabled", False):
            return {}
        # Accumulator only: modules add small deltas; the single tick applies
        # decay + RNG + the accumulated injections (P0-2 unified noise model).
        if not isinstance(getattr(self, "_noise_accum", None), dict):
            self._noise_accum = {}
        out = {}
        try:
            for key in ("stress", "energy", "social", "attention", "valence"):
                try:
                    add = float(deltas.get(key, 0.0) or 0.0)
                except Exception:
                    add = 0.0
                add = max(-0.02, min(0.02, add))
                current = float(self._noise_accum.get(key, 0.0) or 0.0)
                value = _clip(current + add, -NOISE_CLAMP, NOISE_CLAMP)
                self._noise_accum[key] = round(value, 4)
                out[key] = round(value, 4)
            self._last_noise_source = {"source": str(source or "")[:40],
                                       "ts": round(time.time(), 3)}
        except Exception:
            pass
        return out

    def noise_tick(self, now=None) -> dict:
        """L1 task-15 P0-2: single noise update point.

        noise = clip(0.82*noise + gauss(0,0.045) + accumulated module deltas,
                     ±NOISE_CLAMP). Only called by the autonomy tick; legacy
        per-observe noise updates are skipped while autonomy is enabled.
        """
        if not (getattr(self, "autonomy_enabled", False)
                or getattr(self, "autonomy_loop_enabled", False)):
            return {}
        out = {}
        try:
            accum = self._noise_accum if isinstance(getattr(self, "_noise_accum", None), dict) else {}
            for key in ("stress", "energy", "social", "attention", "valence"):
                old = float(self.noise.get(key, 0.0) or 0.0)
                try:
                    gauss = float(self._rng.gauss(0, 0.045))
                except Exception:
                    gauss = 0.0
                try:
                    add = float(accum.get(key, 0.0) or 0.0)
                except Exception:
                    add = 0.0
                value = _clip(0.82 * old + gauss + add, -NOISE_CLAMP, NOISE_CLAMP)
                self.noise[key] = round(value, 4)
                out[key] = round(value, 4)
            self._noise_accum = {}
        except Exception:
            pass
        return out

    # ------------------------------------------------------------------
    # Task-28: minimal autonomy loop (L1, deterministic, default OFF)
    # ------------------------------------------------------------------
    @staticmethod
    def _loop_num(value, default: float = 0.0, lo: float = 0.0,
                  hi: float = 1.0) -> float:
        """Finite, bounded float for loop inputs (NaN/Inf -> default)."""
        try:
            num = float(value)
        except Exception:
            return default
        if num != num or num in (float("inf"), float("-inf")):
            return default
        return max(lo, min(hi, num))

    @staticmethod
    def _autonomy_loop_default_state(now: float = 0.0) -> dict:
        """Bounded loop state shape (spec §7.2); created only while enabled."""
        try:
            stamp = float(now or time.time())
        except Exception:
            stamp = time.time()
        return {
            "enabled": True,
            "tick": 0,
            "candidates": [],
            "winner": None,
            "ignition": False,
            "workspace_token": "",
            "inhibition": {},
            "value_ema": {},
            "effort_debt": 0.0,
            "budget": {"day": time.strftime("%Y-%m-%d", time.localtime(stamp)),
                       "used": 0, "last_action_ts": 0.0},
            "stats": {"ticks": 0, "no_ignition": 0, "ignitions": 0, "executed": 0,
                      "blocked_group": 0, "blocked_quiet": 0,
                      "blocked_cooldown": 0, "blocked_cap": 0},
            "updated_ts": 0.0,
        }

    def _autonomy_loop_restore(self, raw: dict) -> dict:
        """Restore persisted loop state; unknown keys dropped, values bounded."""
        base = self._autonomy_loop_default_state()
        if not isinstance(raw, dict):
            return base
        try:
            base["tick"] = max(0, min(10 ** 9, int(raw.get("tick", 0) or 0)))
        except Exception:
            base["tick"] = 0
        cands = raw.get("candidates") if isinstance(raw.get("candidates"), list) else []
        safe_cands = []
        for row in cands[:AUTONOMY_LOOP_CANDIDATE_MAX]:
            if not isinstance(row, dict):
                continue
            mode = str(row.get("mode") or "")[:AUTONOMY_LOOP_WORKSPACE_MAX]
            if mode not in AUTONOMY_LOOP_MODES:
                continue
            safe_cands.append({
                "mode": mode,
                "source": str(row.get("source") or "")[:16],
                "salience": round(self._loop_num(row.get("salience"), 0.0, 0.0, 1.0), 4),
                "goal_gain": round(self._loop_num(row.get("goal_gain"), 1.0, 0.8, 1.4), 4),
                "discount": round(self._loop_num(row.get("discount"), 1.0, 0.05, 1.0), 4),
                "effort": round(self._loop_num(row.get("effort"), 0.5, 0.0, 1.0), 4),
                "cost": round(self._loop_num(row.get("cost"), 0.0, 0.0, 1.0), 4),
                "value": round(self._loop_num(row.get("value"), 0.0,
                                              AUTONOMY_LOOP_VALUE_MIN,
                                              AUTONOMY_LOOP_VALUE_MAX), 4),
            })
        base["candidates"] = safe_cands
        winner = raw.get("winner")
        if isinstance(winner, dict) and str(winner.get("mode") or "") in AUTONOMY_LOOP_MODES:
            base["winner"] = {
                "mode": str(winner.get("mode"))[:AUTONOMY_LOOP_WORKSPACE_MAX],
                "value": round(self._loop_num(winner.get("value"), 0.0,
                                              AUTONOMY_LOOP_VALUE_MIN,
                                              AUTONOMY_LOOP_VALUE_MAX), 4),
                "ts": round(self._loop_num(winner.get("ts"), 0.0, 0.0, 10 ** 12), 3),
            }
        base["ignition"] = bool(raw.get("ignition", False))
        token = str(raw.get("workspace_token") or "")[:AUTONOMY_LOOP_WORKSPACE_MAX]
        base["workspace_token"] = token if token in AUTONOMY_LOOP_MODES else ""
        inhibition = raw.get("inhibition") if isinstance(raw.get("inhibition"), dict) else {}
        safe_inh = {}
        for mode, ts in list(inhibition.items())[:AUTONOMY_LOOP_CANDIDATE_MAX]:
            mode = str(mode or "")[:AUTONOMY_LOOP_WORKSPACE_MAX]
            if mode not in AUTONOMY_LOOP_MODES:
                continue
            safe_inh[mode] = round(self._loop_num(ts, 0.0, 0.0, 10 ** 12), 3)
        base["inhibition"] = dict(sorted(safe_inh.items(),
                                         key=lambda kv: kv[1], reverse=True)
                                 [:AUTONOMY_LOOP_CANDIDATE_MAX])
        ema = raw.get("value_ema") if isinstance(raw.get("value_ema"), dict) else {}
        base["value_ema"] = {
            str(k)[:AUTONOMY_LOOP_WORKSPACE_MAX]:
                round(self._loop_num(v, 0.0, AUTONOMY_LOOP_VALUE_MIN,
                                     AUTONOMY_LOOP_VALUE_MAX), 6)
            for k, v in list(ema.items())[:AUTONOMY_LOOP_CANDIDATE_MAX]
            if str(k)[:AUTONOMY_LOOP_WORKSPACE_MAX] in AUTONOMY_LOOP_MODES}
        base["effort_debt"] = round(self._loop_num(
            raw.get("effort_debt"), 0.0, 0.0, AUTONOMY_LOOP_DEBT_MAX), 6)
        budget = raw.get("budget") if isinstance(raw.get("budget"), dict) else {}
        base["budget"] = {
            "day": str(budget.get("day") or "")[:10],
            "used": max(0, min(int(self._loop_num(budget.get("used"), 0.0, 0.0, 10 ** 6)),
                               AUTONOMY_DAILY_CAP)),
            "last_action_ts": round(self._loop_num(
                budget.get("last_action_ts"), 0.0, 0.0, 10 ** 12), 3),
        }
        stats = raw.get("stats") if isinstance(raw.get("stats"), dict) else {}
        base["stats"] = {key: max(0, min(
            int(self._loop_num(stats.get(key), 0.0, 0.0, 10 ** 9)), 10 ** 9))
            for key in base["stats"]}
        base["updated_ts"] = round(self._loop_num(
            raw.get("updated_ts"), 0.0, 0.0, 10 ** 12), 3)
        return base

    def _autonomy_loop_param(self, name: str, default: float,
                             lo: float, hi: float) -> float:
        """Read one loop tuning parameter, defensively clamped to its range."""
        try:
            value = float(getattr(self, name, default))
        except Exception:
            return float(default)
        if value != value or value in (float("inf"), float("-inf")):
            return float(default)
        return max(float(lo), min(float(hi), value))

    def _autonomy_loop_ior_factor(self, state: dict, mode: str, now: float) -> float:
        """Return-inhibition recovery factor (Itti & Koch 1998 WTA + IOR).

        A just-broadcast mode is fully suppressed (0) and recovers towards 1 as
        exp(-Δ/τ). Note: spec §2's literal exp(-Δ/τ) points the opposite way
        (no suppression right after selection); the implemented direction is the
        IOR semantics the spec's S9 scenario requires.
        """
        try:
            inhibition = state.get("inhibition") if isinstance(state.get("inhibition"), dict) else {}
            stamp = float(inhibition.get(mode, 0.0) or 0.0)
        except Exception:
            stamp = 0.0
        if stamp <= 0:
            return 1.0
        tau = self._autonomy_loop_param(
            "autonomy_loop_ior_seconds", AUTONOMY_LOOP_IOR_SECONDS,
            AUTONOMY_LOOP_IOR_MIN, AUTONOMY_LOOP_IOR_MAX)
        delta = max(0.0, float(now) - stamp)
        return _clip(1.0 - math.exp(-delta / max(1.0, tau)), 0.0, 1.0)

    def _autonomy_loop_goal_progress(self) -> float:
        """Progress proxy for the engaged goal (0 when there is no goal)."""
        try:
            goals = [g for g in (getattr(self, "goals", []) or [])
                     if isinstance(g, dict)]
            if not goals:
                return 0.0
            focus = str(getattr(self, "goal_focus", "") or "")
            chosen = next((g for g in goals
                           if str(g.get("key") or "") == focus), None)
            if chosen is None:
                chosen = max(goals, key=lambda g: self._loop_num(
                    g.get("priority"), 0.5, 0.0, 1.0))
            return self._loop_num(chosen.get("progress"), 0.0, 0.0, 1.0)
        except Exception:
            return 0.0

    def _autonomy_loop_noise_chaos(self) -> float:
        """Normalized 5-channel noise chaos (same scale as task-15)."""
        try:
            total = sum(abs(self._loop_num((getattr(self, "noise", {}) or {}).get(k),
                                           0.0, -NOISE_CLAMP, NOISE_CLAMP))
                        for k in ("stress", "energy", "social", "attention", "valence"))
            return _clip(total / (5.0 * NOISE_CLAMP), 0.0, 1.0)
        except Exception:
            return 0.0

    def _autonomy_loop_open_loops(self) -> tuple:
        """(due_count, delay_min proxy) for the open-loop candidate."""
        due = 0
        delay_min = 0.0
        try:
            # ams-life: the loops themselves are in her phone; the plugin keeps
            # this count (over every window) up to date.
            pressure = getattr(self, "loop_pressure", None) or {}
            due = int(pressure.get("due", 0) or 0)
            delay_min = float(pressure.get("delay_min", 0.0) or 0.0)
        except Exception:
            return 0, 0.0
        return due, delay_min

    def _autonomy_loop_candidates(self, relationship, now: float, state: dict) -> list:
        """Build ≤6 deterministic candidates (spec §7.3); values per §2–§6."""
        rel = relationship if isinstance(relationship, dict) else {}
        rel_state = rel.get("state") if isinstance(rel.get("state"), dict) else {}
        attachment = rel.get("attachment") if isinstance(rel.get("attachment"), dict) else {}
        absence = rel.get("absence") if isinstance(rel.get("absence"), dict) else {}
        closeness = self._loop_num(rel_state.get("closeness"), 0.5)
        conflict = self._loop_num(rel_state.get("conflict"), 0.0)
        attachment_safe = self._loop_num(attachment.get("safe"), 0.5)
        closeness_eff = _clip(0.70 * closeness + 0.30 * attachment_safe, 0.0, 1.0)
        gap_days = self._loop_num(absence.get("gap_days"), 0.0, 0.0, 365.0)
        appraisal = getattr(self, "appraisal", {}) if isinstance(getattr(self, "appraisal", None), dict) else {}
        novelty = self._loop_num(appraisal.get("novelty"), 0.0)
        goal_rel = self._loop_num(appraisal.get("goal_relevance"), 0.0)
        intensity = self._loop_num(self._intensity(), 0.0)
        stress = self._loop_num(getattr(self, "stress", 0.0), 0.0)
        boredom = self._loop_num(getattr(self, "boredom", 0.0), 0.0)
        novelty_need = self._loop_num(getattr(self, "novelty_need", 0.5), 0.5)
        chaos = self._autonomy_loop_noise_chaos()
        due_count, loop_delay = self._autonomy_loop_open_loops()
        loop_progress = 0.5 if due_count else 0.0
        goal_progress = self._autonomy_loop_goal_progress()
        debt = self._loop_num(state.get("effort_debt"), 0.0, 0.0,
                              AUTONOMY_LOOP_DEBT_MAX)
        k = self._autonomy_loop_param("autonomy_loop_k_delay", AUTONOMY_LOOP_K_DELAY,
                                      AUTONOMY_LOOP_K_MIN, AUTONOMY_LOOP_K_MAX)
        c0 = self._autonomy_loop_param("autonomy_loop_c0", AUTONOMY_LOOP_C0, 0.0, 1.0)
        c1 = self._autonomy_loop_param("autonomy_loop_c1", AUTONOMY_LOOP_C1, 0.0, 1.0)
        c2 = self._autonomy_loop_param("autonomy_loop_c2", AUTONOMY_LOOP_C2, 0.0, 1.0)
        w = AUTONOMY_LOOP_WEIGHTS
        # (mode, features, goal_progress|None, delay_min)
        rows = [
            ("reach_out",
             {"novelty": 0.0, "goal": 0.0, "relation": closeness_eff,
              "affect": intensity, "noise": chaos}, None, gap_days * 1440.0),
            ("explore",
             {"novelty": max(novelty_need, boredom), "goal": 0.0, "relation": 0.0,
              "affect": 0.5 * intensity, "noise": 0.5 * chaos}, None, 0.0),
            ("engage",
             {"novelty": novelty, "goal": goal_rel,
              "relation": 0.5 * closeness_eff, "affect": intensity,
              "noise": 0.3 * chaos}, goal_progress, 0.0),
            ("wait",
             {"novelty": 0.0, "goal": 0.0, "relation": 0.0,
              "affect": 0.0, "noise": 0.0}, None, 0.0),
            ("share",
             {"novelty": 0.0, "goal": loop_progress, "relation": closeness_eff,
              "affect": 0.3 * intensity, "noise": 0.2 * chaos},
             loop_progress, loop_delay),
            ("withdraw",
             {"novelty": 0.0, "goal": 0.0,
              "relation": _clip(max(conflict, 1.0 - closeness_eff), 0.0, 1.0),
              "affect": stress, "noise": chaos}, None, 0.0),
        ]
        out = []
        for mode, features, progress, delay_min in rows[:AUTONOMY_LOOP_CANDIDATE_MAX]:
            salience = sum(w[key] * self._loop_num(features.get(key), 0.0)
                           for key in w)
            salience = _clip(salience, 0.0, 1.0)
            ior = self._autonomy_loop_ior_factor(state, mode, now)
            salience = _clip(salience * ior, 0.0, 1.0)
            if progress is None:
                goal_gain = 1.0
            else:
                goal_gain = _clip(0.8 + 0.4 * self._loop_num(progress, 0.0),
                                  0.8, 1.4)
            discount = _clip(1.0 / (1.0 + k * max(0.0, self._loop_num(
                delay_min, 0.0, 0.0, 1440.0))), 0.05, 1.0)
            effort = AUTONOMY_LOOP_EFFORT.get(mode, 0.5)
            cost = c0 + c1 * effort + c2 * debt
            value = _clip(salience * goal_gain * discount - cost,
                          AUTONOMY_LOOP_VALUE_MIN, AUTONOMY_LOOP_VALUE_MAX)
            out.append({
                "mode": mode,
                "source": ("readiness" if mode == "reach_out" else
                           "curiosity" if mode == "explore" else
                           "context" if mode == "engage" else
                           "fallback" if mode == "wait" else
                           "open_loop" if mode == "share" else "stress"),
                "salience": round(salience, 4),
                "goal_gain": round(goal_gain, 4),
                "discount": round(discount, 4),
                "effort": round(effort, 4),
                "cost": round(cost, 4),
                "value": round(value, 4),
            })
        return out

    def autonomy_loop_tick(self, relationship=None, now=None,
                           private_chat: bool = True) -> dict:
        """One deterministic minimal-autonomy-loop tick (L1, spec §7.1).

        Deterministic arbitration inspired by biased competition / saliency
        WTA+IOR / goal gradient / hyperbolic delay discounting / effort cost /
        global-workspace-style single-token broadcast. This is an engineering
        control loop, NOT an implementation of consciousness or a GWT.

        Default OFF returns {"enabled": False} without creating state or
        touching any other field. Only one token is broadcast per tick; the
        caller decides whether anything is sent (token-only default).
        """
        if not getattr(self, "autonomy_loop_enabled", False):
            return {"enabled": False}
        try:
            current = float(now if now is not None else time.time())
        except Exception:
            current = time.time()
        state = self.autonomy_loop if isinstance(
            getattr(self, "autonomy_loop", None), dict) else None
        if state is None:
            state = self._autonomy_loop_default_state(current)
            self.autonomy_loop = state
        base = self._autonomy_loop_default_state(current)
        for key, value in base.items():
            if key not in state or not isinstance(state.get(key), type(value)):
                state[key] = value
        for key in base["stats"]:
            if key not in state["stats"]:
                state["stats"][key] = 0
        state["enabled"] = True
        try:
            state["tick"] = int(state.get("tick", 0) or 0) + 1
        except Exception:
            state["tick"] = 1
        stats = state["stats"]
        stats["ticks"] = int(stats.get("ticks", 0) or 0) + 1
        budget = state["budget"]
        day = time.strftime("%Y-%m-%d", time.localtime(current))
        if str(budget.get("day") or "") != day:
            budget["day"] = day
            budget["used"] = 0
        # --- gates (spec §7.1 order: group -> quiet -> cooldown -> daily cap)
        blocked = ""
        if not private_chat:
            blocked = "group"
            stats["blocked_group"] = int(stats.get("blocked_group", 0) or 0) + 1
        else:
            hour = time.localtime(current).tm_hour
            if AUTONOMY_QUIET_START_HOUR <= hour < AUTONOMY_QUIET_END_HOUR:
                blocked = "quiet"
                stats["blocked_quiet"] = int(stats.get("blocked_quiet", 0) or 0) + 1
            else:
                last_ts = self._loop_num(budget.get("last_action_ts"), 0.0,
                                         0.0, 10 ** 12)
                if last_ts > 0 and (current - last_ts) < AUTONOMY_COOLDOWN_SECONDS:
                    blocked = "cooldown"
                    stats["blocked_cooldown"] = int(
                        stats.get("blocked_cooldown", 0) or 0) + 1
                elif int(budget.get("used", 0) or 0) >= AUTONOMY_DAILY_CAP:
                    blocked = "cap"
                    stats["blocked_cap"] = int(stats.get("blocked_cap", 0) or 0) + 1
        if blocked:
            state["ignition"] = False
            state["winner"] = None
            state["workspace_token"] = ""
            state["candidates"] = []
            state["updated_ts"] = round(current, 3)
            return {"enabled": True, "blocked": blocked, "ignition": False,
                    "tick": state["tick"], "candidates": [], "stats": dict(stats)}
        # --- effort-debt recovery on every active tick (bounded)
        state["effort_debt"] = round(_clip(
            self._loop_num(state.get("effort_debt"), 0.0, 0.0,
                           AUTONOMY_LOOP_DEBT_MAX) - AUTONOMY_LOOP_DEBT_RECOVERY,
            0.0, AUTONOMY_LOOP_DEBT_MAX), 6)
        # --- candidates + values
        candidates = self._autonomy_loop_candidates(relationship, current, state)
        state["candidates"] = [dict(row) for row in candidates]
        if not candidates:
            stats["no_ignition"] = int(stats.get("no_ignition", 0) or 0) + 1
            state["ignition"] = False
            state["winner"] = None
            state["workspace_token"] = ""
            state["updated_ts"] = round(current, 3)
            return {"enabled": True, "blocked": "", "ignition": False,
                    "tick": state["tick"], "candidates": [], "stats": dict(stats)}
        theta = self._autonomy_loop_param(
            "autonomy_loop_theta_ig", AUTONOMY_LOOP_THETA_IG,
            AUTONOMY_LOOP_THETA_MIN, AUTONOMY_LOOP_THETA_MAX)
        margin_min = self._autonomy_loop_param(
            "autonomy_loop_margin", AUTONOMY_LOOP_MARGIN,
            AUTONOMY_LOOP_MARGIN_MIN, AUTONOMY_LOOP_MARGIN_MAX)
        inhibition = state["inhibition"] if isinstance(
            state.get("inhibition"), dict) else {}
        # Refractory: a mode broadcast within the last 60 s cannot win again.
        eligible = []
        for row in candidates:
            stamp = self._loop_num(inhibition.get(row["mode"]), 0.0, 0.0, 10 ** 12)
            if stamp > 0 and (current - stamp) < AUTONOMY_LOOP_REFRACTORY_SECONDS:
                continue
            eligible.append(row)
        margin = 0.0
        ignition = False
        winner = None
        if eligible:
            ranked = sorted(
                eligible, key=lambda row: (-float(row["value"]),
                                           AUTONOMY_LOOP_MODES.index(row["mode"])))
            winner = ranked[0]
            second = float(ranked[1]["value"]) if len(ranked) > 1 else \
                AUTONOMY_LOOP_VALUE_MIN
            margin = float(winner["value"]) - second
            ignition = bool(float(winner["value"]) >= theta
                            and margin >= margin_min)
        if not ignition:
            stats["no_ignition"] = int(stats.get("no_ignition", 0) or 0) + 1
            state["ignition"] = False
            state["winner"] = None
            state["workspace_token"] = ""
            state["updated_ts"] = round(current, 3)
            return {"enabled": True, "blocked": "", "ignition": False,
                    "tick": state["tick"], "candidates": [dict(r) for r in candidates],
                    "theta_ig": round(theta, 4), "margin": round(margin, 4),
                    "stats": dict(stats)}
        # --- broadcast exactly one workspace token (token-only; no send here)
        mode = str(winner["mode"])[:AUTONOMY_LOOP_WORKSPACE_MAX]
        state["workspace_token"] = mode
        state["winner"] = {"mode": mode, "value": round(float(winner["value"]), 4),
                           "ts": round(current, 3)}
        state["ignition"] = True
        inhibition[mode] = round(current, 3)
        state["inhibition"] = dict(sorted(
            inhibition.items(), key=lambda kv: self._loop_num(
                kv[1], 0.0, 0.0, 10 ** 12), reverse=True
        )[:AUTONOMY_LOOP_CANDIDATE_MAX])
        # --- feedback EMA (record-only; no learning gradient / no next-tick use)
        ema = state["value_ema"] if isinstance(state.get("value_ema"), dict) else {}
        prev = self._loop_num(ema.get(mode), 0.0, AUTONOMY_LOOP_VALUE_MIN,
                              AUTONOMY_LOOP_VALUE_MAX)
        outcome = _clip(float(winner["value"]), AUTONOMY_LOOP_VALUE_MIN,
                        AUTONOMY_LOOP_VALUE_MAX)
        ema[mode] = round(_clip(
            AUTONOMY_LOOP_EMA_KEEP * prev
            + (1.0 - AUTONOMY_LOOP_EMA_KEEP) * outcome,
            AUTONOMY_LOOP_VALUE_MIN, AUTONOMY_LOOP_VALUE_MAX), 6)
        state["value_ema"] = {str(k)[:AUTONOMY_LOOP_WORKSPACE_MAX]: v
                              for k, v in list(ema.items())[
                                  :AUTONOMY_LOOP_CANDIDATE_MAX]}
        state["effort_debt"] = round(_clip(
            self._loop_num(state.get("effort_debt"), 0.0, 0.0,
                           AUTONOMY_LOOP_DEBT_MAX) + AUTONOMY_LOOP_DEBT_STEP,
            0.0, AUTONOMY_LOOP_DEBT_MAX), 6)
        budget["last_action_ts"] = round(current, 3)
        budget["used"] = int(budget.get("used", 0) or 0) + 1
        stats["ignitions"] = int(stats.get("ignitions", 0) or 0) + 1
        stats["executed"] = int(stats.get("executed", 0) or 0) + 1
        state["updated_ts"] = round(current, 3)
        return {"enabled": True, "blocked": "", "ignition": True,
                "tick": state["tick"], "workspace_token": mode,
                "winner": dict(state["winner"]),
                "candidates": [dict(r) for r in candidates],
                "theta_ig": round(theta, 4), "margin": round(margin, 4),
                "effort_debt": state["effort_debt"],
                "value_ema": dict(state["value_ema"]), "stats": dict(stats)}

    def autonomy_state(self, relationship=None, now=None, persist: bool = True) -> dict:
        """L1 task-15: deterministic noise -> autonomy readiness.

        Inputs are all L1 state: 5 noise channels, echo_trace, stress_load
        (stress + allostatic), homeostasis drive deviation (L_int), persona
        autonomy_gain, and the relationship record passed in as data.
        Outputs are bounded: threshold ∈ [0.55, 0.90], max_chars ∈ [60, 240],
        impulse ∈ [0, 1]. P1-G11: threshold follows an EMA of past impulses plus
        a ready hysteresis band, not the current impulse alone. Default OFF
        returns {"enabled": False} without computing anything.
        """
        if not getattr(self, "autonomy_enabled", False):
            return {"enabled": False}
        try:
            current = float(now if now is not None else time.time())
        except Exception:
            current = time.time()
        try:
            noise = {k: float(self.noise.get(k, 0.0) or 0.0)
                     for k in ("stress", "energy", "social", "attention", "valence")}
        except Exception:
            noise = {}
        chaos = _clip(sum(abs(v) for v in noise.values()) / (5.0 * NOISE_CLAMP), 0.0, 1.0)
        # Stage-2: echo/ripple/spiking all feed the readiness input, not just
        # echo_trace. Bounded weighted mix (deterministic).
        try:
            _echo_raw = abs(float(getattr(self, "echo_trace", 0.0) or 0.0))
            _ripple = float((getattr(self, "ripple", {}) or {}).get("energy", 0.0) or 0.0)
            _spiking = float((getattr(self, "spiking", {}) or {}).get("rate", 0.0) or 0.0)
            echo = _clip(0.60 * _echo_raw + 0.20 * _ripple + 0.20 * min(1.0, _spiking), 0.0, 1.0)
        except Exception:
            echo = 0.0
        try:
            stress_load = _clip(
                0.6 * float(self.stress)
                + 0.4 * float(getattr(self, "allostatic_load", 0.0)), 0.0, 1.0)
        except Exception:
            stress_load = 0.0
        try:
            homeo = self.homeostasis if isinstance(self.homeostasis, dict) else {}
            drive_dev = _clip(float(homeo.get("L_int", 0.0) or 0.0), 0.0, 1.0)
        except Exception:
            drive_dev = 0.0
        rel = relationship if isinstance(relationship, dict) else {}
        rel_state = rel.get("state") if isinstance(rel.get("state"), dict) else {}
        try:
            trust = _clip(float(rel_state.get("trust", 0.5) or 0.5), 0.0, 1.0)
        except Exception:
            trust = 0.5
        try:
            closeness = _clip(float(rel_state.get("closeness", 0.5) or 0.5), 0.0, 1.0)
        except Exception:
            closeness = 0.5
        # Stage-2: attachment is an L1 input (not dashboard-only anymore).
        try:
            _attachment = rel.get("attachment") if isinstance(rel.get("attachment"), dict) else {}
            attachment_safe = _clip(float(_attachment.get("safe", 0.5) or 0.5), 0.0, 1.0)
        except Exception:
            attachment_safe = 0.5
        closeness_eff = _clip(0.70 * closeness + 0.30 * attachment_safe, 0.0, 1.0)
        try:
            gain = _clip(float((getattr(self, "profile", {}) or {}).get(
                "autonomy_gain", 1.0) or 0.0), 0.0, 1.5)
        except Exception:
            gain = 1.0
        w = AUTONOMY_WEIGHTS
        impulse = _clip(
            w["chaos"] * chaos + w["echo"] * echo + w["stress_load"] * stress_load
            + w["drive_dev"] * drive_dev + w["distrust"] * (1.0 - trust)
            + w["distance"] * (1.0 - closeness_eff), 0.0, 1.0)
        # P1-G10: autonomy_gain (persona profile) is now a real consumer.
        impulse = _clip(impulse * gain, 0.0, 1.0)
        prev = self._proactive_autonomy if isinstance(self._proactive_autonomy, dict) else {}
        try:
            prev_ema = float(prev.get("impulse_ema", impulse))
        except Exception:
            prev_ema = impulse
        impulse_ema = _clip(0.8 * prev_ema + 0.2 * impulse, 0.0, 1.0)
        # P1-G11: threshold uses the EMA (history), so it does not collapse to a
        # function of the current impulse; ready uses a small hysteresis band.
        target = _clip(0.82 - 0.30 * impulse_ema,
                       AUTONOMY_THRESHOLD_MIN, AUTONOMY_THRESHOLD_MAX)
        prev_ready = bool(prev.get("ready", False))
        # Explicit hysteresis: enter at 0.72, exit only below 0.60.
        if prev_ready:
            ready = impulse >= AUTONOMY_EXIT
        else:
            ready = impulse >= AUTONOMY_ENTER
        max_chars = int(round(_clip(60.0 + 180.0 * impulse,
                                    AUTONOMY_MAX_CHARS_MIN, AUTONOMY_MAX_CHARS_MAX)))
        result = {
            "enabled": True,
            "threshold": round(target, 4),
            "max_chars": max_chars,
            "impulse": round(impulse, 4),
            "impulse_ema": round(impulse_ema, 4),
            "ready": bool(ready),
            "chaos": round(chaos, 4),
            "gain": round(gain, 3),
            "noise_seed": int(getattr(self, "_noise_seed", 0) or 0),
            "sources": {
                "noise": {k: round(v, 4) for k, v in noise.items()},
                "echo_trace": round(echo, 4),
                "stress_load": round(stress_load, 4),
                "drive_dev": round(drive_dev, 4),
                "trust": round(trust, 4),
                "closeness": round(closeness, 4),
                "attachment_safe": round(attachment_safe, 4),
                "closeness_effective": round(closeness_eff, 4),
                "autonomy_gain": round(gain, 3),
            },
            "updated_ts": round(current, 3),
            "last_sent_ts": float(prev.get("last_sent_ts", 0.0) or 0.0),
            "sent_count": int(prev.get("sent_count", 0) or 0),
            "sent_day": str(prev.get("sent_day") or ""),
            "cooldown_seconds": AUTONOMY_COOLDOWN_SECONDS,
            "daily_cap": AUTONOMY_DAILY_CAP,
            "quiet_hours": [AUTONOMY_QUIET_START_HOUR, AUTONOMY_QUIET_END_HOUR],
        }
        if persist:
            self._proactive_autonomy = result
        return dict(result)

    def snapshot(self) -> dict:
        self._decay_to_now()
        out = {"v": round(self.v, 4), "a": round(self.a, 4),
                "sleepiness": round(self.sleepiness, 4), "hunger": round(self.hunger, 4),
                "physical_fatigue": round(self.physical_fatigue, 4),
                "last_sleep_end": self.last_sleep_end, "last_meal": self.last_meal,
                "last_rest": self.last_rest,
                "d": round(self.d, 4), "social": round(self.social, 4),
                "stress": round(self.stress, 4), "energy": round(self.energy, 4),
                "seen_need": round(float(getattr(self, "seen_need", 0.3)), 4),
                "talked": round(float(getattr(self, "talked", 0.0)), 4),
                "ambient": round(float(getattr(self, "ambient", 0.0)), 4),
                "ticks": self.ticks,
                "noise": {k: round(float(v), 3) for k, v in self.noise.items()},
                "echo": round(self.echo, 4), "echo_trace": round(self.echo_trace, 4),
                "ripple": dict(self.ripple), "spiking": dict(self.spiking),
                "reflection": dict(self.reflection),
                "momentum": dict(self.momentum),
                "appraisal": dict(self.appraisal),
                "stimuli": [{k: v for k, v in x.items() if k not in ("text", "fp")}
                            for x in list(self.stimuli)[-8:] if isinstance(x, dict)],
                "history": list(self.history)[-80:],
                "open_loops_due": int((getattr(self, "loop_pressure", None) or {}).get("due", 0) or 0),
                "goal_focus": self.goal_focus,
                "coping": round(float((self.appraisal or {}).get("coping", 0.5)), 3),
                "opponent": dict(self.opponent),
                "regulation_stats": dict(self.regulation_stats),
                "attention": round(float(self.attention), 3),
                "novelty_need": round(float(getattr(self, "novelty_need", 0.5)), 3),
                "boredom": round(float(getattr(self, "boredom", 0.0)), 3),
                "allostatic_load": round(float(getattr(self, "allostatic_load", 0.0)), 3),
                "homeostasis": dict(getattr(self, "homeostasis", {}) or {}),
                "boundary_pressure": round(float(getattr(self, "boundary_pressure", 0.0)), 3),
                "refusal_readiness": round(float(getattr(self, "refusal_readiness", 0.0)), 3),
                "interpersonal": {k: round(float(v), 4) for k, v in (getattr(self, "interpersonal", {}) or {}).items()},
                "daily_digests": [dict(x) for x in (getattr(self, "daily_digests", []) or [])[-30:]],
                "meta_emotion": self.meta_emotion,
                "goals": [{"key": g.get("key"), "name": g.get("name"), "horizon": g.get("horizon"),
                           "progress": round(float(g.get("progress", 0) or 0), 3),
                           "priority": round(float(g.get("priority", 0.5) or 0.5), 3),
                           "last_update": round(float(g.get("last_update", 0.0) or 0.0), 3)}
                          for g in self.goals],
                "goal_conflict": list(self.goal_conflict),
                "goal_scores": dict(getattr(self, "goal_scores", {}) or {}),
                "self_timeline": dict(self.self_timeline),
                "spectrum_probs": self._spectrum_probs(),
                "sec": dict(self.sec),
                "core_self": self.core_self,
                "narrative_self": self.narrative_self,
                "plutchik": PLUTCHIK_WHEEL,
                "compound": self.compound,
                "regulation": self.regulation,
                "spectrum": self._spectrum(),
                "spectrum_calibration": dict(getattr(self, "_spectrum_calibration_meta", {}) or {}),
                "labels": dict(getattr(self, "labels", {}) or {}),
                # Task-15: exactly one new top-level field; default OFF keeps
                # the minimal marker and computes no readiness.
                "learning": dict(self._learning),
                "proactive_autonomy": (dict(self._proactive_autonomy)
                                       if getattr(self, "autonomy_enabled", False)
                                       and isinstance(getattr(self, "_proactive_autonomy", None), dict)
                                       else {"enabled": False})}
        # Task-28: persisted ONLY while the loop is enabled. Default OFF is a
        # true no-op: the state file stays byte-identical (key absent entirely).
        if (getattr(self, "autonomy_loop_enabled", False)
                and isinstance(getattr(self, "autonomy_loop", None), dict)):
            out["autonomy_loop"] = dict(self.autonomy_loop)
        return out
