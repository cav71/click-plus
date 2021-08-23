def configure(extensions=None, **arguments):
    from functools import wraps
    from inspect import getmodule, getfile
    from .base import (  # noqa: F401
        ExtensionBase,
        ExtensionDevelopmentError
    )
    extensions = [ExtensionBase.get(e)(e) for e in (extensions or [])]

    def _fn(fn):
        @wraps(fn)
        def _fn1(**kwargs):
            for e in extensions:
                kwargs = e.process(kwargs, arguments) or kwargs
            return fn(**kwargs)

        mod = getmodule(fn)
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
                            name, getfile(e.__class__))
        return _fn1
    return _fn
