# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Standalone stand-in; use AstrBot itself when installed."""


class Context:
    pass


class Star:
    def __init__(self, context):
        self.context = context


def register(*args, **kwargs):
    def deco(cls):
        return cls
    return deco
