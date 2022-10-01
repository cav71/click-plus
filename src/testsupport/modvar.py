"""modvar pytest fixture to store and restore variables

modvar is a pytest fixture helping with the task of preserving variables
in a test.

How to use it:

def testme(modvar):
    with modvar(os.environ):
        os.environ["HELLO"] = "World"
        -> so the environ variable stores "World"
    -> here HELLO is deleted (if didn't exist)
"""
from __future__ import annotations
from typing import Dict, Any

import pytest


class VarManager:
    class NA:  # pylint: disable=too-few-public-methods
        pass

    def __init__(self, source: Dict[str, Any], **kwars):
        self.source = source
        self.mods = {}
        self.mods.update(kwars)
        self.values: dict[Any, Any] = {}

    def __enter__(self):
        for name, value in self.mods.items():
            self.set(name, value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name, value in self.values.items():
            self.set(name, value)

    def set(self, name, value):
        self.values[name] = self.source.get(name, self.NA)
        if value is not self.NA:
            self.source[name] = value
        elif name in self.source:
            del self.source[name]
        return self.values[name]

    def delete(self, name):
        if name not in self.source:
            self.values[name] = self.NA
            return self.NA
        return self.set(name, self.NA)


@pytest.fixture(scope="function")
def modvar():
    yield VarManager
