# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Standalone stand-in; use AstrBot itself when installed."""


class _Comp:
    def __init__(self, *args, **kwargs):
        self.args = args
        for key, value in kwargs.items():
            setattr(self, key, value)


class Plain(_Comp):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text


class Image(_Comp):
    @classmethod
    def fromFileSystem(cls, path):
        return cls(file=str(path))

    @classmethod
    def fromURL(cls, url):
        return cls(url=str(url))

    @classmethod
    def fromBase64(cls, b64):
        return cls(file='base64://' + str(b64))


class Reply(_Comp):
    pass


class Record(_Comp):
    @classmethod
    def fromFileSystem(cls, path):
        return cls(file=str(path))


class At(_Comp):
    pass


class Face(_Comp):
    pass
