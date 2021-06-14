import sys
import pathlib
import inspect
import collections
import subprocess
import pytest


@pytest.fixture()
def scripter(tmp_path_factory):
    R = collections.namedtuple("R", "out,err,code")
    class E:
        def __init__(self, script, tmpdir, exe=sys.executable):
            self.script = script
            self.tmpdir = tmpdir
            self.exe = exe

        def run(self, args, cwd=None):
            self.p = subprocess.Popen([self.exe, self.script, *args],
                        cwd=self.tmpdir if cwd is True else cwd,
                        text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = self.p.communicate()
            return R(out, err, self.p.returncode)

    class Scripter:
        def __init__(self):
            self.src = pathlib.Path(__file__).resolve().parent / "data"
            self.exe = sys.executable
        def __truediv__(self, path):
            tmpdir = tmp_path_factory.mktemp(pathlib.Path(path).with_suffix("").name)
            return E(self.src / path, tmpdir)

    return Scripter()
