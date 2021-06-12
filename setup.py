import os
import sys

from setuptools import setup, find_namespace_packages

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import click.plus

version = click.plus.__version__
if os.getenv("MYVERSION"):
    assert os.getenv("MYHASH")
    version = os.getenv("MYVERSION")
    thehash = os.getenv("MYHASH")
    with open(click.plus.__file__, "w") as fp:
        fp.write(f"""
__version__ = "{version}"
__hash__ = "{thehash}"
""".strip())


packages = find_namespace_packages(where="src")
packages.remove("click")

setup(
    name="click-plus",
    version=version,
    url="https://github.com/cav71/click-plus",
    packages=packages,
    package_dir={"click.plus": "src/click/plus"}
)
