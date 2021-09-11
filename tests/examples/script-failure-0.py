from click.decorators import command, argument
import click.plus
from click.plus import api


class MyArguments(api.ExtensionBase):
    def setup(self, fn, arguments):
        pass

    def process(self, kwargs, arguments):
        pass


class MyArguments2(api.ExtensionBase):
    NAME = "myarguments"

    def setup(self, fn, arguments):
        pass

    def process(self, kwargs, arguments):
        pass


@command()
@argument("value", type=int)
@click.plus.configure(["myarguments"], factor=2)
def main(value):
    pass


if __name__ == "__main__":
    main()
