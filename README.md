# click-plus
[![PyPI version](https://badge.fury.io/py/click-plus.svg)](https://badge.fury.io/py/click-plus)
### Introduction
This package helps creating re-usable flags for click scripts.

Example:
```python

import click
import click.plus

@click.command()
.. normal click options/arguments
@click.plus.configure(["my-custon-set"])
def main():
    ...
```

For a full example [here..](README.EXTENSION.MD)
