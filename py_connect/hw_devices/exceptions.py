"""Exceptions of the library"""


class PyConnectError(Exception):
    """Base class for all exceptions in py_connect."""


class InvalidPowerCombination(PyConnectError):
    """Connection of different power pins."""
