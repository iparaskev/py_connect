"""behaviours.py

Add behaviours to power connections.
"""


def connect(self):
    """Connect two power pins.

    They must be of the same type.
    """
    self.board_power.outbound = self.peripheral_power
