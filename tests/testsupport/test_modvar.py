"""Test the pytest modvar plugin
"""

import pytest

MYVAR = "xyz"


def test_modvar(modvar):
    "test modvar usage"

    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        # NEWVAR doesn't exist
        NEWVAR  # pylint: disable=undefined-variable,pointless-statement

    with modvar(globals(), MYVAR=123) as mod:
        assert MYVAR == 123
        # injecting NEWVAR into the global namespace
        mod.set("NEWVAR", [4, 5, 6])
        assert NEWVAR == [4, 5, 6]  # pylint: disable=undefined-variable

    # restoring the original values
    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        NEWVAR  # pylint: disable=undefined-variable,pointless-statement


def test_modvar_operations(modvar):
    "test modvar operations"

    # starting point
    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        NEWVAR  # pylint: disable=undefined-variable,pointless-statement

    with modvar(globals()) as mod:
        mod.delete("MYVAR")
        with pytest.raises(NameError):
            MYVAR  # pylint: disable=undefined-variable,pointless-statement

        mod.set("NEWVAR", 12)
        assert NEWVAR == 12  # pylint: disable=undefined-variable

    assert MYVAR == "xyz"
    with pytest.raises(NameError):
        NEWVAR  # pylint: disable=undefined-variable,pointless-statement
