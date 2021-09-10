from click.decorators import option
from click.plus import api


class MyBoost(api.ExtensionBase):
    # if NAME is not defined if will fall back to the class name
    NAME = "booster"

    def setup(self, fn, arguments):
        # here one can add as many click.option/click.argument
        # the argments is a dict taken from the decorator (see below)
        # (remember to wrap the (fn) for each line)

        # we define a --boost option taking an int
        fn = option("--boost", type=int, default=1)(fn)
        return fn

    def process(self, kwargs, arguments):
        # before entering the main we modify
        # the kwargs passed to the main. arguments is the same dict as in setup

        # the factor is provided by the decorator (see below)
        factor = arguments["factor"]

        # kwargs is the dict arguments main will receive (you can modify it in place)
        value = kwargs["value"]
        # we remove the boost argument so main won't be aware of it
        boost = kwargs.pop("boost")
        kwargs["value"] = value * boost * factor
