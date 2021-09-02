from click.decorators import command, argument
import click.plus
from click.plus import api


class MyArguments(api.ExtensionBase):
    NAME = "myarguments"

    def setup(self, fn, arguments):
        return super(MyArguments, self).setup(fn, arguments)

    def process(self, kwargs, arguments):
        return super(MyArguments, self).process(kwargs, arguments)


@command()
@argument("value", type=int)
@click.plus.configure(["myarguments"], factor=2)
def main(value):
    print("Got", value)


if __name__ == "__main__":
    main()
