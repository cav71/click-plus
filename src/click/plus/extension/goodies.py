# use the internal click (see comment in api.click) is only for click-plus code
# external code can simply import click
import os
import sys
import logging

from .api import ExtensionBase, click


logger = logging.getLogger(__name__)


class _MyHandler(logging.StreamHandler):
    INDENT = 2

    def __init__(self, logging_var, *args, **kwargs):
        self.logging_var = logging_var
        super(_MyHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        from json import dumps
        data = ""
        if hasattr(record, self.logging_var):
            data = getattr(record, self.logging_var)
            if not isinstance(data, str):
                data = dumps(data, indent=self.INDENT, sort_keys=True)
            data = data.strip()
            if data:
                pre = " "*self.INDENT
                data = f"\n{pre}" + f"\n{pre}".join(data.split("\n"))
        setattr(record, self.logging_var, data)
        return super(_MyHandler, self).emit(record)


class Logging(ExtensionBase):
    NAME = "g-logging"
    # the logging extra variable eg.
    # logging.info("msg", extra={ "data" : <some-data> })
    LOGGING_VAR = "data"

    def setup(self, fn, arguments):
        fn = click.option("-v", "--verbose", count=True)(fn)
        fn = click.option("-q", "--quiet", count=True)(fn)
        return fn

    def process(self, kwargs, arguments):
        level = kwargs.pop("verbose") - kwargs.pop("quiet")

        if arguments.get("quiet", False):
            level -= 1

        level = logging.WARN
        if level == 0:
            level = logging.INFO
        elif level > 0:
            level = logging.DEBUG

        fmt = f"%(levelname)s:%(name)s:%(message)s%({self.LOGGING_VAR})s"
        logging.basicConfig(level=level,
                            handlers=[_MyHandler(self.LOGGING_VAR)],
                            format=fmt)
        return kwargs


class Report(ExtensionBase):
    NAME = "g-report"

    def setup(self, fn, arguments):
        from time import monotonic
        from functools import wraps

        self.log = log = (arguments.get(f"{self.NAME}.log", {})
                          .get("log", logger))

        @click.pass_context
        @wraps(fn)
        def inner(ctx, *args, **kwargs):
            t0 = monotonic()
            failed = False
            try:
                return ctx.invoke(fn, *args, **kwargs)
            except KeyboardInterrupt:
                log.info("Script aborted in %.2fs", monotonic()-t0)
                failed = True
            except Exception:
                envdict = {
                    str(k): str(v)
                    for k, v in
                    sorted(os.environ.items(), key=lambda x: str(x[0]).upper())
                }
                log.info("Script run with errors in %.2fs", monotonic()-t0,
                         extra={
                            Logging.LOGGING_VAR: {
                                        "arguments": sys.argv,
                                        "environment": envdict,
                            },
                         }, exc_info=True)
                failed = True
            finally:
                if not failed:
                    log.info("Script completed in %.2fs", monotonic()-t0)
        return inner

    def process(self, kwargs, arguments):
        self.log.info("started script", extra={
            Logging.LOGGING_VAR: {
                "arguments": sys.argv,
            }
        })
