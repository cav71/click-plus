from click.decorators import group, argument
import click.plus

# That's the module containing the MyBoost api.ExtensionBase derived class
import my_common_args  # noqa: F401


@group()
def main():
    pass


@main.command()
@click.plus.configure(["booster"], factor=10)
@argument("value", type=int)
def per10(value):
    print("Got", value)


@main.command()
@click.plus.configure(["booster"], factor=20)
@argument("value", type=int)
def per20(value):
    print("Got", value)


if __name__ == "__main__":
    main()
