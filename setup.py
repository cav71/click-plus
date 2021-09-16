import os
import pathlib


from setuptools import setup, find_namespace_packages

from setuptools.github import tools

initfile = pathlib.Path(__file__).parent / "src/click/plus/__init__.py"
version = tools.update_version(initfile, os.getenv("GITHUB_DUMP"))

packages = find_namespace_packages(where="src")
packages.remove("click")

setup(
    name="click-plus",
    version=version,
    url="https://github.com/cav71/click-plus",
    packages=packages,
    package_dir={"click.plus": "src/click/plus"},
    install_requires=["click"],
    description="collection of click extensions",
    long_description=pathlib.Path("README.rst").read_text(),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
