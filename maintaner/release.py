#!/usr/bin/env python
import pathlib
import logging
import re

import click
import pygit2

log = logging.getLogger(__name__)


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
    if not dryrun:
        refname = repo.head.name
        author = repo.default_signature
        commiter = repo.default_signature
        parent = repo.revparse_single(repo.head.shorthand).hex
        repo.index.add(initfile)
        repo.index.write()
        tree = repo.index.write_tree()
        oid = repo.create_commit(refname, author, commiter, msg, tree, [parent])
        log.info("created oid %s", oid)

    log.info("switching to new branch '%s'%s", branch, " (skip)" if dryrun else "")
    if not dryrun:
        commit = repo.revparse_single(repo.head.shorthand)
        repo.branches.local.create(branch, commit)
        ref = repo.lookup_reference(repo.lookup_branch(branch).name)
        repo.checkout(ref)


if __name__ == "__main__":
    main()
