import os
import sys
import json
import collections


from setuptools import setup, find_namespace_packages

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import click.plus


def hubversion(gdata):
    txt = gdata["ref"]
    number = gdata['run_number']
    shasum = gdata["sha"]
    head, _, rest = txt.partition("/")

    cases = [
        ("refs/heads/master", click.plus.__version__),
        ("refs/heads/beta/", f"b{number}"),
        ("refs/tags/release/", ""),
    ]
    for pat, out in cases:
        if not txt.startswith(pat):
            continue
        return txt[len(pat):] + out, shasum
    raise RuntimeError("unhandled github ref", txt)


version = click.plus.__version__
if os.getenv("GITHUB_DUMP"):
    gdata = json.loads(os.getenv("GITHUB_DUMP"))   
    version, thehash = hubversion(gdata)
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
