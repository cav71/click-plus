def test_failure_duplicates(scripter):
    "test for duplicate class names"
    result = (scripter / "script-failure-0.py").run(["--help"])

    assert (
        "click.plus.base.ExtensionDevelopmentError: "
        "('duplicate name for extension myarguments'" in result.err
    )
    assert result.code
    assert not result.out


def test_failure_missing(scripter):
    "test for missing extension"

    result = (scripter / "script-failure-1.py").run(["--help"])
    assert (
        "click.plus.base.ExtensionNotFound: ('no class found for name=blah"
        in result.err
    )
    assert result.code
    assert not result.out


def test_failure_wrong_setup(scripter):
    "test for wrong setup return code"

    result = (scripter / "script-failure-2.py").run(["--help"])
    assert (
        "click.plus.base.ExtensionDevelopmentError: "
        "('MyArguments.setup returned non callable'" in result.err
    )
    assert result.code
    assert not result.out
