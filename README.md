# click-plus

### Introduction
This package allows creation of re-usable flags for click scripts.

Example:
```python

import click
import click.plus
import module containing a class named MyCustomSet

@click.command()
.. normal click options/arguments
@click.plus.configure(["my-custon-set"])
def main():
    ...
```

For a full example [here..](README.EXTENSION.MD)
