"""Test the pytest modvar plugin
"""

import pytest

MYVAR = "xyz"


def test_modvar(modvar):
    "test modvar usage"

    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        # NEWVAR doesn't exist
        NEWVAR  # type: ignore # noqa

    with modvar(globals(), MYVAR=123) as mod:
        assert MYVAR == 123
        # injecting NEWVAR into the global namespace
        mod.set("NEWVAR", [4, 5, 6])
        assert NEWVAR == [4, 5, 6]  # type: ignore # noqa

    # restoring the original values
    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        NEWVAR  # type: ignore # noqa


def test_modvar_operations(modvar):
    "test modvar operations"

    # starting point
    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        NEWVAR  # type: ignore # noqa

    with modvar(globals()) as mod:
        mod.delete("MYVAR")
        with pytest.raises(NameError):
            MYVAR  # type: ignore # noqa

        mod.set("NEWVAR", 12)
        assert NEWVAR == 12  # type: ignore # noqa

    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        NEWVAR  # type: ignore # noqa


def test_modvar_shadow_myvar(modvar):
    assert MYVAR == "xyz"
    with modvar(globals(), MYVAR=modvar.NA):
        with pytest.raises(NameError):
            MYVAR  # pylint: disable=undefined-variable,pointless-statement
    assert MYVAR == "xyz"
