"""test_device_m2m.py"""

import unittest
import sys
sys.path.append(".")

from py_connect.hw_devices.power_connections import *  # noqa E402
from py_connect.hw_devices.hw_connections import *  # noqa E402
from py_connect.hw_devices.exceptions import *  # noqa E402
from py_connect.hw_devices_language.hw_devices_parser import DeviceHandler  # noqa E402


class TestHwConnections(unittest.TestCase):

    def devices(self):
        self.pi = DeviceHandler("rpi_3b_plus.hwd")
        self.sonar = DeviceHandler("hc_sr04.hwd")

    def test_power(self):
        """Test power connection"""
        self.devices()

        con = Power2Power(pin_1=self.pi.power_pins["gnd_1"],
                          pin_2=self.sonar.power_pins["gnd"])
        con.connect()

        # Wrong power types
        with self.assertRaises(InvalidPowerCombination):
            con.pin_2 = self.sonar.power_pins["vcc"]
            con.connect()
        with self.assertRaises(InvalidPowerCombination):
            con.pin_1 = self.pi.power_pins["power_3v3_1"]
            con.connect()
        with self.assertRaises(InvalidPowerCombination):
            con.pin_1 = self.pi.power_pins["power_3v3_1"]
            con.pin_2 = self.sonar.power_pins["vcc"]
            con.connect()

    def test_gpio(self):
        """Test gpio connection."""
        self.devices()

        con = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_2"],
                        hwint_2=self.sonar.hw_interfaces["gpio"]["echo"])
        con.connect()

        # Exceed max connections
        with self.assertRaises(MaxConnectionsError):
            con.hwint_1 = self.sonar.hw_interfaces["gpio"]["trigger"]
            con.connect()

        # Connect two input pins
        with self.assertRaises(InvalidGpioError):
            con.hwint_1 = self.sonar.hw_interfaces["gpio"]["trigger"]
            con.hwint_2 = self.sonar.hw_interfaces["gpio"]["trigger"]
            con.connect()

        # Connect two output pins
        with self.assertRaises(InvalidGpioError):
            tmp = DeviceHandler("hc_sr04.hwd")
            con.hwint_1 = tmp.hw_interfaces["gpio"]["echo"]
            con.hwint_2 = tmp.hw_interfaces["gpio"]["echo"]
            con.connect()


if __name__ == "__main__":
    unittest.main()
