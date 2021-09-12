import re
import json
import os
import pathlib
import sys


from setuptools import setup, find_namespace_packages

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import click.plus  # noqa: E402


def hubversion(gdata, fallback):
    """returns (version, shasum)
    >>> hubversion({
        'ref': 'refs/heads/beta/0.0.4',
        'sha': '2169f90c22e',
        'run_number': '8',
    }, None)
    ('0.0.4b8', '2169f90c22e')
    >>> hubversion({
        'ref': 'refs/tags/release/0.0.3',
        'sha': '5547365c82',
        'run_number': '3',
    }, None)
    ('0.0.3', '5547365c82')
    >>> hubversion({
        'ref': 'refs/heads/master',
        'sha': '2169f90c',
        'run_number': '20',
    }, '123'))
    ('123', '2169f90c')"""
    txt = gdata["ref"]
    number = gdata["run_number"]
    shasum = gdata["sha"]
    head, _, rest = txt.partition("/")

    cases = [
        (
            "refs/heads/master",
            fallback,
        ),
        ("refs/heads/beta/", f"b{number}"),
        ("refs/tags/release/", ""),
    ]
    for pat, out in cases:
        if not txt.startswith(pat):
            continue
        return txt[len(pat) :] + out, shasum
    raise RuntimeError("unhandled github ref", txt)


def update_version(data, path, fallback):
    if not data:
        return

    gdata = json.loads(data)
    version, thehash = hubversion(gdata, fallback)

    lines = pathlib.Path(path).read_text().split("\n")

    exp = re.compile(r"__version__\s*=\s*")
    exp1 = re.compile(r"__hash__\s*=\s*")
    assert len([l for l in lines if exp.search(l)]) == 1  # noqa: E741
    assert len([l for l in lines if exp1.search(l)]) == 1  # noqa: E741

    lines = [
        f'__version__ = "{version}"'
        if exp.search(l)
        else f'__hash__ = "{thehash}"'
        if exp1.search(l)
        else l
        for l in lines  # noqa: E741
    ]

    pathlib.Path(path).write_text("\n".join(lines))
    return version


version = update_version(
    os.getenv("GITHUB_DUMP"), click.plus.__file__, click.plus.__version__
)

packages = find_namespace_packages(where="src")
packages.remove("click")

setup(
    name="click-plus",
    version=version,
    url="https://github.com/cav71/click-plus",
    packages=packages,
    package_dir={"click.plus": "src/click/plus"},
    description="collection of click extensions",
    long_description=pathlib.Path("README.rst").read_text(),
    install_requires=["click"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
