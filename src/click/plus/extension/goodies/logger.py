import os
import sys
import logging

from click.plus.extension.api import ExtensionBase


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


class Logger(ExtensionBase):
    # the logging extra variable eg.
    # logging.info("msg", extra={ "application" : <some-data> })
    LOGGING_VAR = "application"

    def setup(self, fn, arguments):
        # this is a workaround needed
        # only when developing click.plus
        from click.decorators import option

        fn = option("-v", "--verbose", count=True)(fn)
        fn = option("-q", "--quiet", count=True)(fn)
        return fn

    def process(self, kwargs, arguments):
        level = kwargs.pop("verbose") - kwargs.pop("quiet")

        if arguments.get("logger", False):
            level -= 1

        if level == 0:
            level = logging.INFO
        elif level > 0:
            level = logging.DEBUG
        else:
            level = logging.WARN

        fmt = f"%(levelname)s:%(name)s:%(message)s%({self.LOGGING_VAR})s"
        logging.basicConfig(level=level,
                            handlers=[_MyHandler(self.LOGGING_VAR)],
                            format=fmt)
        return kwargs


def example():
    # this is a workaround needed
    # only when developing click.plus
    from click.decorators import command, argument

    from click.plus.extension import configure

    @command()
    @configure(["logger",], logger="quiet")
    def main():
        logging.getLogger("x").debug("A debug message")
        logging.getLogger("x").info("An info message")
        logging.getLogger("x").warning("A warning message")
    main()


if __name__ == "__main__":
    example()
