import click.decorators
import click.plus


def test_import():
    "test import the api"
    from click.plus import api  # noqa: F401

    assert click.decorators.command()
