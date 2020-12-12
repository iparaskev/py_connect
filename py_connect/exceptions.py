"""Exceptions of the library"""


class PyConnectError(Exception):
    """Base class for all exceptions in py_connect."""


class InvalidPowerCombination(PyConnectError):
    """Connection of different power pins."""


class MaxConnectionsError(PyConnectError):
    """Interface has exceeded it's max connections limit."""


class InvalidGpioError(PyConnectError):
    """Invalid connection of two gpio pins."""


class AlreadyConnectedError(PyConnectError):
    """One or more pins of the interface are already connected."""


class TwoMasterError(PyConnectError):
    """Error when connecting two master interfaces."""


class TwoSlaveError(PyConnectError):
    """Error when connecting two slave interfaces."""


class ChipEnabledFullError(PyConnectError):
    """All chip enable pins are in use."""


class NotImplementedDriverError(PyConnectError):
    """This peripheral doesn't have an implemented driver."""


class UnicludedDeviceError(PyConnectError):
    """Device hasn't been included in connections specification."""


class EmptyListError(PyConnectError):
    """Empty list given for an attribute."""
