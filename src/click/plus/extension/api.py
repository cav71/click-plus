from .base import (  # noqa: F401
    ExtensionError,
    ExtensionNotFound,
    ExtensionDevelopmentError,
    ExtensionBase
)

#try:
#    import click
#    click.command  # type: ignore
#except AttributeError:
#    # The reason for this workaround is click package __init__
#    # contains code, so once click.__init__ is imported this
#    # blocks other namespace packages.
#    # With the current setup.py in the click-plus this is not an issue
#    # but when running out of source code cannot just import
#    # click and using for example click.command.
#    import click.decorators as click  # type: ignore
