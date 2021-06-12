# PYTHONPATH=src python example.py --boost 3 2

import os
import sys
import time
import click.decorators
import click.plus.extension
from   click.plus.extension import api
import click.plus.extension.goodies


class MyArguments(api.ExtensionBase):
    def setup(self, fn, arguments):
        fn = click.decorators.option("--boost", type=int, default=1)(fn)
        return fn

    def process(self, kwargs, arguments):
        boost = kwargs.pop("boost")
        kwargs["value"] *= boost
        kwargs["value"] *= arguments["factor"]
        return
        return super(MyArguments, self).process(kwargs, arguments)

import logging
log = logging.getLogger()


@click.decorators.command()
@click.decorators.option("--error", type=int, default=0)
@click.decorators.argument("value", type=int)
@click.plus.extension.configure(["myarguments", "g-logging", "g-report"], factor=2)
def main(value, error):
    print("Got", value)
    log.debug("Wow")
    log.info("Hello", extra={ "data" : "a whole\n lotta\n ... love" })
    log.warning("World")
    log.info("a very long message",
        extra={ "data": {
                    "cmdline": sys.argv,
                }
        })

    time.sleep(1.4)
    if error:
        raise RuntimeError("x")


if __name__ == "__main__":
    main()
