def configure(extensions=None, **arguments):
    from .base import ExtensionBase
    extensions = [ ExtensionBase.get(e)(e) for e in (extensions or []) ]

    def _fn(fn):
        @functools.wraps(fn)
        def _fn1(**kwargs):
            for e in extensions:
                kwargs = e.process(kwargs, arguments)
            return fn(**kwargs)

        mod = inspect.getmodule(fn)
        _fn1.__doc__ = mod.__doc__
        for e in extensions:
            _fn1 = e.setup(_fn1, arguments)
        return _fn1
    return _fn

