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
            cmd = [ str(a) for a in [self.exe, self.script, *args] ]
            self.p = subprocess.Popen(cmd,
                        cwd=self.tmpdir if cwd is True else cwd,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = self.p.communicate()
            return R(
                out if isinstance(out, str) else str(out, encoding="utf-8"), 
                err if isinstance(err, str) else str(err, encoding="utf-8"), 
                self.p.returncode)

    class Scripter:
        def __init__(self):
            self.src = pathlib.Path(__file__).resolve().parent / "data"
            self.exe = sys.executable
        def __truediv__(self, path):
            tmpdir = tmp_path_factory.mktemp(pathlib.Path(path).with_suffix("").name)
            return E(self.src / path, tmpdir)

    return Scripter()
