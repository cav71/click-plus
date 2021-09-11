"""This is an example script

It contains two commands, and leverages the extension mechanism of click-plus
to add a common --boost flag.
"""

# This is an artifact needed only for development,
# usually here you'd just import click
try:
    from click import group, argument
except ImportError:
    from click.decorators import group, argument

# from here BAU
import click.plus

# That's the module containing the MyBoost api.ExtensionBase derived class
import boost  # noqa: F401


@group()
def main():
    """a multicommand wrapper"""
    pass


@main.command()
@click.plus.configure(["booster"], factor=10)
@argument("value", type=int)
def per10(value):
    """multiplies the value x 10

    This subcommand multiply the value x 10 by default (the boost)."""
    print("Got", value)


@main.command()
@click.plus.configure(["booster"], factor=20)
@argument("value", type=int)
def per20(value):
    "multiplies the value x 20"
    print("Got", value)


if __name__ == "__main__":
    main()
