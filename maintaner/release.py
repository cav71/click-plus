#!/usr/bin/env python
import pathlib
import functools
import logging
import re

import click
from dulwich import porcelain
import pygit2

log = logging.getLogger(__name__)


class Pcl:
    ENC = "utf-8"

    def __getattr__(self, name):
        fn = getattr(porcelain, name)

        @functools.wraps(fn)
        def _fn(*args, **kwargs):
            ret = fn(*args, **kwargs)
            if isinstance(ret, bytes):
                return str(ret, encoding=self.ENC)
            elif isinstance(ret, (list, tuple, set)) and all(
                isinstance(t, bytes) for t in ret
            ):
                return type(ret)([str(r, encoding=self.ENC) for r in ret])
            return ret

        return _fn

    def branches_remote(self, repo, origin):
        branches = set()
        with porcelain.open_repo_closing(repo) as r:
            for item in r.refs.keys(base=f"refs/remotes/{origin}".encode("utf-8")):
                branches.add(str(item, encoding=self.ENC))
        return branches


def handle_version(initfile, version=None):
    expr = re.compile(r"__version__\s*=\s*['\"](?P<version>[^\"']+)['\"]")
    lines = []
    with open(initfile) as fp:
        for line in fp:
            match = expr.search(line)
            if match:
                if version is None:
                    return match.group("version")
                else:
                    x, y = match.span(1)
                    line = line[:x] + version + line[y:]
            if version is not None:
                lines.append(line)
    if version is not None:
        txt = "".join(lines)
        with open(initfile, "w") as fp:
            fp.write(txt)


def newversion(version, mode):
    newver = [int(n) for n in version.split(".")]
    if mode == "major":
        newver[-3] += 1
        newver[-2] = 0
        newver[-1] = 0
    elif mode == "minor":
        newver[-2] += 1
        newver[-1] = 0
    else:
        newver[-1] += 1
    return ".".join(str(v) for v in newver)


@click.command()
@click.argument(
    "mode", type=click.Choice(["micro", "minor", "major"], case_sensitive=False)
)
@click.argument("initfile")
@click.option("-f", "--force", is_flag=True)
@click.option("-n", "--dry-run", "dryrun", is_flag=True)
@click.option(
    "-w",
    "--workdir",
    help="git working dir",
    default=pathlib.Path("."),
    type=pathlib.Path,
)
def main(mode, initfile, workdir, force, dryrun):
    logging.basicConfig(level=logging.INFO)
    workdir = workdir.resolve()
    log.info("using working dir %s", workdir)

    repo = pygit2.Repository(workdir)

    # check we are on master
    current = repo.head.shorthand
    log.info("current branch %s", current)
    if current != "master":
        raise click.UsageError(f"you must be on master branch, currently on {current}")

    # and we have no uncommitted changes
    def ignore(f):
        return (f & pygit2.GIT_STATUS_WT_NEW) or (f & pygit2.GIT_STATUS_IGNORED)

    localmods = {p for p, f in repo.status().items() if not ignore(f)}
    if (not force) and localmods:
        raise click.UsageError(
            "local modification staged for commit, use -f|--force to skip check"
        )

    # pull the current version from initfile
    curver = handle_version(initfile)
    if not curver:
        raise click.UsageError(f"cannot find __version__ in {initfile}")
    log.info("got current version '%s'", curver)

    # verify the current version has a beta/<curver> branch
    remotes = {remote.name for remote in repo.remotes}
    if len(remotes) != 1:
        raise click.UsageError(f"multiple remotes defined: {', '.join(remotes)}")
    remote = remotes.pop()
    n = len(remote)
    branche_names = {
        b[n:].lstrip("/") if b.startswith(remote) else b for b in repo.branches
    }
    if f"beta/{curver}" not in branche_names:
        raise click.UsageError(
            f"there's no 'beta/{curver}' branch in the worktree and remote"
        )

    # move into creating a new branch
    newver = newversion(curver, mode)
    log.info("releasing %s -> %s", curver, newver)

    branch = f"beta/{newver}"
    if branch in branche_names:
        raise click.UsageError(f"new branch {branch} fund in current branches")

    # modify the __init__
    log.info("updating init file %s%s", initfile, " (skip)" if dryrun else "")
    if not dryrun:
        handle_version(initfile, newver)

    msg = f"beta release {newver}"
    log.info("committing '%s'%s", msg, " (skip)" if dryrun else "")
    # if not dryrun:
    #    pcl.commit(repo, msg)

    # create and co new branch
    log.info("switching to new branch '%s'%s", branch, " (skip)" if dryrun else "")
    # if not dryrun:
    #    pcl.update_head(repo, branch, new_branch=branch)
    # merge form mastenewverr
    # push remote


if __name__ == "__main__":
    main()
