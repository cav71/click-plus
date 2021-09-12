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

.. image:: https://github.com/cav71/click-plus/actions/workflows/master.yml/badge.svg
   :target: https://github.com/cav71/click-plus/actions
   :alt: Build

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------
The flags (defined elsewhere) can be used as::

    import click
    import click.plus

    @click.command()
    .. normal click options/arguments
    @click.plus.configure(["boost"])
    def main():
        ...

There's a commented example with a `main`_ script and the arguments
group `args`_.


Requirements
------------

* ``Python`` >= 3.5.
* ``click``

Installation
------------

You can install ``click-plus`` via `pip`_ from `PyPI`_::

    $ pip install click-plus


.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`main`: https://raw.githubusercontent.com/cav71/click-plus/master/tests/examples/example.py
.. _`args`: https://raw.githubusercontent.com/cav71/click-plus/master/tests/examples/boost.py
