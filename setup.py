import os

from setuptools import setup, find_namespace_packages

setup(
    name="click-plus",
    version="0.0.0",
    url="https://github.com/cav71/click-plus",
    #packages=find_namespace_packages(where="src"),
    packages=["click.plus",],
    package_dir={"click.plus": "src/click"}
)
