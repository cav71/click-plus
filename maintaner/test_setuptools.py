import itertools
import re


def hubversion(gdata, fallback):
    "extracts a (version, shasum) from a GITHUB_DUMP variable"

    def getversion(txt):
        return ".".join(str(int(v)) for v in txt.split("."))

    ref = gdata["ref"]  # eg. "refs/tags/release/0.0.3"
    number = gdata["run_number"]  # eg. 3
    shasum = gdata["sha"]  # eg. "2169f90c"

    if ref == "refs/heads/master":
        return (fallback, shasum)

    if ref.startswith("refs/heads/beta/"):
        version = getversion(ref.rpartition("/")[2])
        return (f"{version}b{number}", shasum)

    if ref.startswith("refs/tags/release/"):
        version = getversion(ref.rpartition("/")[2])
        return (f"{version}", shasum)

    raise RuntimeError("unhandled github ref", gdata)


def test_hubversion():
    testdata = [
        # test 1
        {
            "ref": "refs/heads/beta/0.0.4",
            "sha": "2169f90c22e",
            "run_number": "8",
        },
        {
            "ref": "refs/tags/release/0.0.3",
            "sha": "5547365c82",
            "run_number": "3",
        },
        {
            "ref": "refs/heads/master",
            "sha": "2169f90c",
            "run_number": "20",
        },
    ]

    fallbacks = [
        "123",
        "",
    ]

    expects = [
        ("0.0.4b8", "2169f90c22e"),
        ("0.0.4b8", "2169f90c22e"),
        ("0.0.3", "5547365c82"),
        ("0.0.3", "5547365c82"),
        ("123", "2169f90c"),
        ("", "2169f90c"),
    ]

    itrange = itertools.product(testdata, fallbacks)
    for index, (gdata, fallback) in enumerate(itrange):
        expected = expects[index]
        assert expected == hubversion(gdata, fallback)


def initversion(initfile, var, value, inplace=None):
    from os import linesep

    # module level var
    expr = re.compile(f"^{var}\\s*=\\s*['\\\"](?P<value>[^\\\"']+)['\\\"]")
    fixed = None
    lines = []
    input_lines = initfile.read_text().split(linesep)
    for line in reversed(input_lines):
        if fixed:
            lines.append(line)
            continue
        match = expr.search(line)
        if match:
            fixed = match.group("value")
            if value is not None:
                x, y = match.span(1)
                line = line[:x] + value + line[y:]
        lines.append(line)
    txt = linesep.join(reversed(lines))
    if inplace:
        with initfile.open("w") as fp:
            fp.write(txt)
    return fixed, txt


def test_initversion(tmp_path):
    with open(tmp_path / "in.txt", "w") as fp:
        fp.write(
            """
# a test file
__version__ = "1.2.3"
__hash__ = "4.5.6"

# end of test
"""
        )
    version, txt = initversion(tmp_path / "in.txt", "__version__", "6.7.8")
    assert version == "1.2.3"
    assert (
        txt
        == """
# a test file
__version__ = "6.7.8"
__hash__ = "4.5.6"

# end of test
"""
    )
    version, txt = initversion(tmp_path / "in.txt", "__hash__", "6.7.8")
    assert version == "4.5.6"
    assert (
        txt
        == """
# a test file
__version__ = "1.2.3"
__hash__ = "6.7.8"

# end of test
"""
    )

    initversion(tmp_path / "in.txt", "__version__", "6.7.8", inplace=True)
    initversion(tmp_path / "in.txt", "__hash__", "8.9.10", inplace=True)

    assert (
        (tmp_path / "in.txt").read_text()
        == """
# a test file
__version__ = "6.7.8"
__hash__ = "8.9.10"

# end of test
"""
    )
