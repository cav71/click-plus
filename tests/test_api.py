import pathlib
import click.decorators
import click.plus


def test_import():
    "test import the api"
    from click.plus.extension import api
    assert click.decorators.command()

