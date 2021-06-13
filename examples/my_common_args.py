# this is a workaround for when running this script out this very source tree
# (not needed anywhere else, just import click as per usual)
import click.decorators as click
from   click.plus.extension import api


class MyArguments(api.ExtensionBase):
    NAME = "myarguments"
    
    # here you can add as many click arguments/options
    def setup(self, fn, arguments):
        # you can return here the wrapped fn or a list of click.{option/argument}
        fn = click.option("--boost", type=int, default=1)(fn)
        return fn
    
    # kwargs contains the main **kwargs, you can modify in place
    # or return a new dict here. arguments is a dict to the
    # decorator arguments
    def process(self, kwargs, arguments):
        value = kwargs["value"]
        boost = kwargs.pop("boost")
        factor = arguments["factor"]
        kwargs["value"] = value * boost * factor
