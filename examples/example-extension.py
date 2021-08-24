# PYTHONPATH=src:examples python examples/first.py factor-2 --boost 3 2


# this is a workaround for when running this script out this very source tree
# (not needed anywhere else, just import click as per usual)
from click.decorators import group, argument, option

import click.plus.extension
import my_common_args


@group()
def main():
    pass


@main.command(name="factor-2")
@argument("value", type=int)
@click.plus.extension.configure(["myarguments",], factor=2)
def factor_2(value):
    print("value", value)


@main.command(name="factor-10")
@argument("value", type=int)
@click.plus.extension.configure(["myarguments",], factor=10)
def factor_10(value):
    print("value", value)


if __name__ == "__main__":
    main()
