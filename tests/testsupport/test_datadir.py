from pathlib import Path

import pytest

PROJECTDIR = Path(__file__).parent.parent.parent


@pytest.fixture(scope="function")
def fixer_change_relative_datadir(modvar):
    with modvar(globals(), DATADIR="abc") as mod:
        yield mod


@pytest.fixture(scope="function")
def fixer_change_absolute_datadir(modvar):
    with modvar(globals(), DATADIR="/abc/def") as mod:
        yield mod


def test_datadir(datadir, testdir):
    assert all(isinstance(d, Path) for d in (datadir, testdir))
    assert datadir == (PROJECTDIR / "tests" / "datadir")
    assert testdir == (
        PROJECTDIR / "tests" / "datadir" / "testsupport" / "test_datadir"
    )


def test_datadir_with_relative_datadir(fixer_change_relative_datadir, datadir, testdir):
    assert all(isinstance(d, Path) for d in (datadir, testdir))
    assert datadir == (PROJECTDIR / "tests" / "datadir" / "abc")
    assert testdir == (
        PROJECTDIR / "tests" / "datadir" / "abc" / "testsupport" / "test_datadir"
    )


def test_datadir_with_absolute_datadir(fixer_change_absolute_datadir, datadir, testdir):
    assert all(isinstance(d, Path) for d in (datadir, testdir))
    assert datadir == Path(datadir.drive, "/abc/def")
    assert testdir == Path(datadir.drive, "/abc/def/testsupport/test_datadir")
