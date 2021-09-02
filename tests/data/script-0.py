from click.decorators import command, argument, option
import click.plus
from click.plus import api


class MyArguments(api.ExtensionBase):
    NAME = "myarguments"

    # here you can add as many click arguments/options
    def setup(self, fn, arguments):
        fn = option("--boost", type=int, default=1)(fn)
        return fn

    # kwargs contains the main **kwargs, you can modify in place
    # or return a new dict here. arguments is a dict to the
    # decorator arguments
    def process(self, kwargs, arguments):
        value = kwargs["value"]
        boost = kwargs.pop("boost")
        factor = arguments["factor"]
        kwargs["value"] = value * boost * factor


@command()
@argument("value", type=int)
@click.plus.configure(["myarguments"], factor=2)
def main(value):
    print("Got", value)


if __name__ == "__main__":
    main()
