"""astrbot.api.star stand-in."""


class Context:
    pass


class Star:
    def __init__(self, context):
        self.context = context


def register(*args, **kwargs):
    def deco(cls):
        return cls
    return deco
