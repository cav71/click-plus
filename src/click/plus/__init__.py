__version__ = "0.0.1"
__hash__ = ""


def configure(extensions=None, **arguments):
    from contextlib import ExitStack
    from functools import wraps
    from inspect import getfile
    from .base import ExtensionBase, ExtensionDevelopmentError  # noqa: F401

    extensions = [ExtensionBase.get(e)(e) for e in (extensions or [])]

    def _fn(fn):
        @wraps(fn)
        def _fn1(**kwargs):
            with ExitStack() as stack:
                for e in extensions:
                    kwargs = e.process(kwargs, arguments) or kwargs
                    e.atexit(stack)
                return fn(**kwargs)

        for e in extensions:
            ret = e.setup(_fn1, arguments)
            if isinstance(ret, (list, tuple)):
                for w in ret:
                    _fn1 = wraps(fn)(w(_fn1))
            else:
                _fn1 = wraps(fn)(ret)
            if not callable(_fn1):
                name = e.__class__.__name__
                raise ExtensionDevelopmentError(
                    f"{name}.setup returned non callable", name, getfile(e.__class__)
                )
        return _fn1

    return _fn
