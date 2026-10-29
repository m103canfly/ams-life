"""astrbot.api.message_components stand-in."""


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
