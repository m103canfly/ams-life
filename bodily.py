# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Describe bodily needs without directing behavior."""


def feel_lines(snapshot):
    lines = []
    for key, feeling in (("sleepiness", "困"), ("hunger", "饿"),
                         ("physical_fatigue", "身体累")):
        value = float(snapshot.get(key, 0.0))
        if value >= 0.35:
            lines.append(("很" if value > 0.7 else "有点") + feeling + "。")
    return lines[:2]
