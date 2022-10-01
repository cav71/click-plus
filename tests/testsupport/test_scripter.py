import pytest
from pathlib import Path

PROJECTDIR = Path(__file__).parent.parent.parent

DATADIR = "../../examples"


@pytest.fixture(scope="function")
def fixer_change_relative_datadir(modvar):
    with modvar(globals(), DATADIR="abc") as mod:
        yield mod


@pytest.fixture(scope="function")
def fixer_change_absolute_datadir(modvar):
    with modvar(globals(), DATADIR="/abc/def") as mod:
        yield mod


@pytest.fixture(scope="function")
def fixer_change_no_datadir(modvar):
    with modvar(globals(), DATADIR=modvar.NA) as mod:
        yield mod


def test_scripter_paths(scripter, datadir, testdir):
    assert scripter.datadir == (PROJECTDIR / "examples")
    assert scripter.testdir == (
        PROJECTDIR / "examples" / "testsupport" / "test_scripter"
    )


def test_scripter_paths_no_datadir(fixer_change_no_datadir, scripter, datadir, testdir):
    assert scripter.datadir == (PROJECTDIR / "tests" / "datadir")
    assert scripter.testdir == (
        PROJECTDIR / "tests" / "datadir" / "testsupport" / "test_scripter"
    )


def test_scripter_paths_relative_datadir(
    fixer_change_relative_datadir, scripter, datadir, testdir
):
    assert scripter.datadir == (PROJECTDIR / "tests" / "datadir" / "abc")
    assert scripter.testdir == (
        PROJECTDIR / "tests" / "datadir" / "abc" / "testsupport" / "test_scripter"
    )


def test_scripter_paths_absolute_datadir(
    fixer_change_absolute_datadir, scripter, datadir, testdir
):
    assert scripter.datadir == Path(scripter.datadir.drive, "/abc/def")
    assert scripter.testdir == Path(
        scripter.datadir.drive, "/abc/def", "testsupport", "test_scripter"
    )


# def test_simplest_script(scripter):
#     assert scripter.datadir == (PROJECTDIR / "examples")
#     script = scripter / "hello-world.py"
#     print()
#     print("*** !>", script.script)
#     # /Users/antonio/Projects/github/click-plus/tests/d
#     atadir/testsupport/test_scripter/hello-world.py
#     # /Users/antonio/Projects/github/click-plus/examples/te
#     stsupport/test_scripter/hello-world.py
#     # print("*** !>", scripter.scriptsdir)
#     # print("*** !>", script.rundir())
#     # #assert (scripter / "hello-world.py" ).exe.exists()
#     # #script.run(["--help"])
#     # print(TOPDIR)
#
# def test_xxx(ignore_module_datadir, scripter):
#     assert scripter.datadir == (PROJECTDIR / "tests" / "datadir")
#     script = scripter / "hello-world.py"
#     print()
#     print("*** !>", script.script)
