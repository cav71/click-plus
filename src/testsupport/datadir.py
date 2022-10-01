import os
from pathlib import Path
from typing import Optional
import pytest


def npath(path: Optional[Path]=None) -> Path:
    return Path(os.path.normpath(Path(path or Path.cwd()).expanduser()))


@pytest.fixture(scope="function")
def datadir(request) -> Path:
    basedir = request.config.getoption("datadir")
    return npath(basedir / getattr(request.module, "DATADIR", ""))


@pytest.fixture(scope="function")
def testdir(datadir, request) -> Path:
    from conftest import __file__
    result = (
        Path(request.module.__file__)
        .relative_to(Path(__file__).parent)
        .with_suffix("")
    )
    return npath(datadir / result)


def pytest_addoption(parser):
    from conftest import __file__
    group = parser.getgroup("datadir")
    group.addoption(
        "--datadir",
        default=os.getenv("DATADIR", npath(Path(__file__).parent / "datadir")),
        type=Path,
        help="""
        source data: the datadir fixture will be a path rooted under DATADIR. resolution order is:

          1. path relative to the root conftest.py
          2. environment variable DATADIR
          3. command line argumnet --datadir
    
        additionally if a test module contains a DATADIR global variable it 
        will be appended to the datadir fixture
    """
    )
