# PYTHONPATH=src python example  xx

import click.decorators
import click.plus.extension
from   click.plus.extension import api


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


@click.decorators.command()
@click.decorators.argument("value", type=int)
@click.plus.extension.configure(["myarguments"], factor=2)
def main(value):
    print("Got", value)


if __name__ == "__main__":
    main()
