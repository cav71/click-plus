import inspect
import functools

from .base import (  # noqa: F401
    ExtensionError,
    ExtensionNotFound,
    ExtensionDevelopmentError
)
from .base import ExtensionBase

try:
    import click
    click.command  # type: ignore
except AttributeError:
    # The reason for this workaround is click package __init__
    # contains code, so once click.__init__ is imported this
    # blocks other namespace packages.
    # With the current setup.py in the click-plus this is not an issue
    # but when running out of source code cannot just import
    # click and using for example click.command.
    import click.decorators as click  # type: ignore


def configure(extensions=None, **arguments):
    extensions = [ExtensionBase.get(e)(e) for e in (extensions or [])]

    def _fn(fn):
        @functools.wraps(fn)
        def _fn1(**kwargs):
            for e in extensions:
                kwargs = e.process(kwargs, arguments) or kwargs
            return fn(**kwargs)

        mod = inspect.getmodule(fn)
        _fn1.__doc__ = mod.__doc__
        for e in extensions:
            ret = e.setup(_fn1, arguments)
            if isinstance(ret, (list, tuple)):
                for w in ret:
                    _fn1 = w(_fn1)
            else:
                _fn1 = ret
            if not callable(_fn1):
                name = e.__class__.__name__
                raise ExtensionDevelopmentError(
                            f"{name}.setup returned non callable",
                            name, inspect.getfile(e.__class__))
        return _fn1
    return _fn
