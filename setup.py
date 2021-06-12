import os
import sys

from setuptools import setup, find_namespace_packages

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import click.plus

setup(
    name="click-plus",
    version=click.plus.__version__,
    url="https://github.com/cav71/click-plus",
    #packages=find_namespace_packages(where="src"),
    packages=["click.plus",],
    package_dir={"click.plus": "src/click"}
)
