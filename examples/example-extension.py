#!/usr/bin/env python
# This is an example script on how to define and use click.plus.extension
import logging

# These are usual imports
import click
from click.plus.extension import api

# goodies contain the logging and report cli pre-defined extensions
import click.plus.extension.goodies

# we define a new extension "myarguments"
# (name is either defined in the NAME attribute 
# or taken from the class name itself, case insensitive)
class MyArguments(api.ExtensionBase):
    NAME = "myarguments"
    
    # setup is called when decorating fn, arguments is a kw dict
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


@click.group()
def main():
    pass

# factor_2 will multiply the input value x 2
# the extension logging is from the goodies
@main.command(name="factor-2")
@click.argument("value", type=int)
@click.plus.extension.configure(["myarguments", "logging"], factor=2, logger="quiet")
def factor_2(value):
    logging.debug("a debug message") 
    logging.info("an info message") 
    logging.warning("a warning message") 
    print("value", value)


@main.command(name="factor-10")
@click.argument("value", type=int)
@click.plus.extension.configure(["myarguments", "report"], factor=10)
def factor_10(value):
    print("value", value)


if __name__ == "__main__":
    main()
