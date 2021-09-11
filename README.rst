==========
click-plus
==========
This package helps creating re-usable flags for click scripts.

.. image:: https://img.shields.io/pypi/v/click-plus.svg
    :target: https://pypi.org/project/click-plus
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/click-plus.svg
    :target: https://pypi.org/project/click-plus
    :alt: Python versions

.. image:: https://github.com/pytest-dev/pytest-subtests/workflows/build/badge.svg
    :target: https://github.com/pytest-dev/pytest-subtests/actions
    :alt: Build

Features
--------

[![PyPI version](https://badge.fury.io/py/click-plus.svg)](https://badge.fury.io/py/click-plus)
![Build](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)

### Introduction

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
