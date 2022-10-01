import os
import sys
import contextlib
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import pytest


def npath(path: Optional[Path] = None) -> Path:
    return Path(os.path.normpath(Path(path or Path.cwd()).expanduser()))


@pytest.fixture()
def scripter(request, tmp_path_factory, datadir, testdir):
    """handles script (cli) execution

    def test(scripter):
        script = scripter / "script-file.py"
        result = script.run(["--help"]) # this will execute:
                                        #   script-file.py --help
        assert result.out and result.err
    """

    class ScripterError(Exception):
        pass

    class MissingExecutableError(ScripterError):
        pass

    class Result:
        def __int__(self, **kwargs):
            self.out = kwargs.get("out")
            self.err = kwargs.get("err")
            self.code = kwargs.get("code")

    class Executable:
        def __repr__(self):
            return (
                f"<{self.__class__.__name__} script={self.script} at {hex(id(self))}>"
            )

        def __init__(self, script, workdir, datadir, exe, env=None):
            self.script = script
            self.workdir = workdir
            self.datadir = os.path.normpath(datadir)
            self.exe = exe
            self.env = env
            # if not Path(script).exists():
            #     raise MissingExecutableError(f"script file {script} not found")

        def rundir(self, subdir=None):
            return (self.workdir / subdir) if subdir else self.workdir

        def run(self, args, cwd=None, load_data=True):
            cmd = [str(a) for a in [self.exe, self.script, *args]]

            with contextlib.ExitStack() as stack:
                fpout = stack.enter_context((self.workdir / "stdout.txt").open("w"))
                fperr = stack.enter_context((self.workdir / "stderr.txt").open("w"))
                self.p = subprocess.Popen(
                    cmd,
                    cwd=self.workdir if cwd is True else cwd,
                    stdout=fpout,
                    stderr=fperr,
                )
                self.p.communicate()
            out = (self.workdir / "stdout.txt").read_text()
            err = (self.workdir / "stderr.txt").read_text()
            return Result(
                out.replace("\r\n", "\n"), err.replace("\r\n", "\n"), self.p.returncode
            )

        def compare(self, refdir, populate=False):
            src = self.datadir / refdir
            if not src.exists():
                raise MissingExecutableError(f"reference dir {src} not found")

            for name in ["stdout.txt", "stderr.txt"]:
                left = src / name
                right = self.workdir / name
                if populate:
                    if left.exists():
                        raise ScripterError(f"cannot overwrite {left} with {right}")
                    shutil.copyfile(right, left)
                assert left.read_text() == right.read_text()

    class Scripter:
        def __init__(self, datadir, testdir, pyexe=sys.executable):
            self.datadir = npath(datadir)
            self.testdir = testdir
            self.pyexe = pyexe

        def __truediv__(self, path):
            tmpdir = tmp_path_factory.mktemp(Path(path).with_suffix("").name)
            scriptdir = testdir if hasattr(request.module, "DATADIR") else self.testdir
            # script = self.testdir / path if hasattr(request.module, "DATADIR", "")
            return Executable(scriptdir / path, tmpdir, self.datadir, self.pyexe)

    return Scripter(datadir, testdir)


def pytest_configure(config):
    plugins = {"datadir", "modvar"}
    missing = {
        p for p in plugins if not config.pluginmanager.get_plugin(f"testsupport.{p}")
    }
    if missing:
        raise RuntimeError(f"testsupport.scripter needs [{', '.join(missing)}] plugins")
