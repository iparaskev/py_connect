"""behaviours.py

Add behaviours to power connections.
"""

from .hw_devices import Power2Power


def connect(self):
    """Connect two power pins.

    They must be of the same type.
    """
    self.board_power.outbound.append(self.peripheral_power)


Power2Power.connect = connect
