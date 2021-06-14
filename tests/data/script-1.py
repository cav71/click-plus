from click.decorators import group, argument, option
import click.plus.extension
from click.plus.extension import api


class MyArguments(api.ExtensionBase):
    NAME = "myarguments"

    def setup(self, fn, arguments):
        return [
            option("--boost", type=int, default=1),
            argument("value", type=int)
        ]
    
    # decorator arguments
    def process(self, kwargs, arguments):
        value = kwargs["value"]
        boost = kwargs.pop("boost")
        factor = arguments["factor"]
        kwargs["value"] = value * boost * factor


@group()
def main():
    pass


@main.command(name="factor-2")
@click.plus.extension.configure(["myarguments"], factor=2)
def factor_2(value):
    print("Got", value)


@main.command(name="factor-10")
@click.plus.extension.configure(["myarguments"], factor=10)
def factor_10(value):
    print("Got", value)


if __name__ == "__main__":
    main()
