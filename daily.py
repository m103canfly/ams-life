# -*- coding: utf-8 -*-
"""A deterministic daily schedule, independent of chat windows."""
from datetime import timedelta
import random

# Boundaries are local hours; the final period continues until midnight.
PERIODS = (
    (0, (("家", "睡觉"), ("家", "准备睡觉"))),
    (7, (("家", "刚起床"),)),
    (8, (("家", "吃早饭"),)),
    (9, (("学院", "上课"), ("家", "看书"), ("外面", "办事"), ("街上", "逛街"))),
    (12, (("家", "吃午饭"), ("外面", "吃午饭"))),
    (14, (("学院", "上课"), ("家", "休息"), ("外面", "办事"), ("街上", "和朋友逛街"))),
    (18, (("家", "吃晚饭"), ("外面", "吃晚饭"))),
    (20, (("家", "休息"), ("家", "看书"), ("家", "准备睡觉"))),
)
# Match render_compact's low energy and high stress; negative mood is its low-mood threshold.
LOW_ENERGY = 0.25
LOW_MOOD = -0.35
HIGH_STRESS = 0.60
HER_MAX_HOURS = 3


def period_start(now):
    hour = max(hour for hour, _ in PERIODS if hour <= now.hour)
    return now.replace(hour=hour, minute=0, second=0, microsecond=0)


def next_period(now):
    hours = [hour for hour, _ in PERIODS if hour > now.hour]
    if hours:
        return now.replace(hour=min(hours), minute=0, second=0, microsecond=0)
    return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


def schedule(now, energy, v, stress):
    start = period_start(now)
    options = next(options for hour, options in PERIODS if hour == start.hour)
    rng = random.Random(now.date().isoformat() + ":" + str(start.hour))
    # Keep meals and sleep intact; in daytime, a low state favors staying home.
    if start.hour in (9, 14) and (energy <= LOW_ENERGY or v <= LOW_MOOD or stress >= HIGH_STRESS):
        options = options + (("家", "休息"),) * 6
    where, doing = rng.choice(options)
    return where, doing, start
