"""behaviours.py

Add behaviours to power connections.
"""

from .hw_devices import Power2Power


def connect(self):
    """Connect two power pins.

    They must be of the same type.
    """
    if self.pin_1.type == self.pin_2.type:
        self.pin_1.connected = True
        self.pin_2.connected = True
    else:
        print("Not the same types")


Power2Power.connect = connect
