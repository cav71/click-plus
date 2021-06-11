import inspect
import functools

from .base import ExtensionError, ExtensionNotFound
from .base import ExtensionBase


def configure(extensions=None, **arguments):
    extensions = [ ExtensionBase.get(e)(e) for e in (extensions or []) ]

    def _fn(fn):
        @functools.wraps(fn)
        def _fn1(**kwargs):
            for e in extensions:
                kwargs = e.process(kwargs, arguments) or kwargs
            return fn(**kwargs)

        mod = inspect.getmodule(fn)
        _fn1.__doc__ = mod.__doc__
        for e in extensions:
            _fn1 = e.setup(_fn1, arguments)
        return _fn1
    return _fn

