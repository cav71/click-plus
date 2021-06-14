from click.decorators import command, argument, option
import click.plus.extension
from click.plus.extension import api


class MyArguments(api.ExtensionBase):
    def setup(self, fn, arguments):
        pass
    def process(self, kwargs, arguments):
        pass


class MyArguments2(api.ExtensionBase):
    def setup(self, fn, arguments):
        pass
    def process(self, kwargs, arguments):
        pass
    


@command()
@argument("value", type=int)
@click.plus.extension.configure(["myarguments", "blah"], factor=2)
def main(value):
    pass


if __name__ == "__main__":
    main()
