"""behaviours.py

Add behaviours to power connections.
"""

from .hw_devices import Power2Power
from ..exceptions import InvalidPowerCombination


def connect(self):
    """Connect two power pins.

    They must be of the same type.
    """
    if self.pin_1.type == self.pin_2.type:
        self.pin_1.connected = True
        self.pin_2.connected = True
    else:
        raise InvalidPowerCombination("Not the same types")


Power2Power.connect = connect
