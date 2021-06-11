# use the internal click (only for click.plus in-source code)
from .api import ExtensionBase, click


class Logging(ExtensionBase):
    def setup(self, fn, arguments):
        fn = click.option("-v", "--verbose", count=True)(fn)
        fn = click.option("-q", "--quiet", count=True)(fn)
        return fn

    def process(self, kwargs, arguments):
        from logging import DEBUG, INFO, WARN, basicConfig
        level = kwargs.pop("verbose") - kwargs.pop("quiet")

        if arguments.get("quiet", False): level -= 1
        level = INFO if level == 0 else (DEBUG if level > 0 else WARN)
        basicConfig(level=level)
        return kwargs