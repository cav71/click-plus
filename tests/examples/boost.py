# This is an artifact needed only for development,
# usually you just use import click
try:
    from click import option
except ImportError:
    from click.decorators import option

from click.plus import api

# this will provide an extensio with the --boost flag


class Boost(api.ExtensionBase):
    # NAME is the visible name for this extension, it must be unique
    #      if not assigned it will default to the class name Boost (case insensitive)
    NAME = "booster"

    def setup(self, fn, arguments):
        # here one can add as many click.option/click.argument
        # the argments is a dict taken from the decorator

        # we define a --boost option taking an int
        # (remember to wrap the (fn) for each line)
        fn = option("--boost", type=int, default=1)(fn)
        return fn

    def process(self, kwargs, arguments):
        # before entering the main we intercept the kwargs
        # arguments is the same dict as in the setup method

        # we extract the factor from the arguments factor keyword
        factor = arguments["factor"]

        # kwargs is the dict arguments main will receive (you can modify it in place)
        value = kwargs["value"]

        # we remove the boost argument so main won't be aware of it
        boost = kwargs.pop("boost")

        # so we udpate the kwargs that the main will receive
        kwargs["value"] = value * boost * factor
