DATADIR = "examples"


def test_script0(scripter):
    "test a simple script"

    script = scripter / "examples/script-0.py"

    # test help
    result = script.run(
        [
            "--help",
        ]
    )

    assert (
        """
Usage: script-0.py [OPTIONS] VALUE

Options:
  --boost INTEGER
  --help           Show this message and exit.
""".lstrip()
        == result.out
    )

    # test logic: factor * value * boost

    # 2 * 13 * 1
    result = script.run(
        [
            "13",
        ]
    )
    assert "Got 26" == result.out.strip()

    # 2 * 13 * 3
    result = script.run(["13", "--boost", "3"])
    assert "Got 78" == result.out.strip()


def test_script1(scripter):
    "test a script with group"

    script = scripter / "examples/script-1.py"

    # test help
    assert not script.run(
        [
            "--help",
        ]
    ).code

    # 2 * 13 * 1
    result = script.run(["factor-2", "13"])
    assert "Got 26" == result.out.strip()

    # 2 * 13 * 3
    result = script.run(["factor-2", "13", "--boost", "3"])
    assert "Got 78" == result.out.strip()

    # 10 * 13 * 1
    result = script.run(["factor-10", "13"])
    assert "Got 130" == result.out.strip()

    # 10 * 13 * 3
    result = script.run(["factor-10", "13", "--boost", "3"])
    assert "Got 390" == result.out.strip()


def test_script2(scripter):
    "test a script with group"
    script = scripter / "examples/script-2.py"

    # test help
    assert not script.run(
        [
            "--help",
        ]
    ).code

    result = script.run(["99"])
    assert "Got 99" == result.out.strip()
    assert "This is the ExtensionBase.setup" in result.err
    assert "This is the ExtensionBase.process" in result.err


def test_example(scripter):
    "tets the example script"

    script = scripter / "examples/example.py"
    script.run(["--help"])
    script.compare("example-help")
