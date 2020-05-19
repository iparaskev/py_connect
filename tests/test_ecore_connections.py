"""test_device_m2m.py"""

import unittest
import sys
sys.path.append(".")

from py_connect.hw_devices.power_connections import *  # noqa E402
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
        with self.assertRaises(RuntimeError):
            con.pin_2 = self.sonar.power_pins["vcc"]
            con.connect()
        with self.assertRaises(RuntimeError):
            con.pin_1 = self.pi.power_pins["power_3v3_1"]
            con.connect()
        with self.assertRaises(RuntimeError):
            con.pin_1 = self.pi.power_pins["power_3v3_1"]
            con.pin_2 = self.sonar.power_pins["vcc"]
            con.connect()


if __name__ == "__main__":
    unittest.main()
