"""test_device_m2m.py"""

import unittest
import sys
import time
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
        bme = DeviceHandler("bme680.hwd")

        con = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_2"],
                        hwint_2=self.sonar.hw_interfaces["gpio"]["echo"])
        i2c_con = I2c2I2c(hwint_1=self.pi.hw_interfaces["i2c"]["i2c_1"],
                          hwint_2=bme.hw_interfaces["i2c"]["i2c_0"])
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

        con.hwint_1 = self.pi.hw_interfaces["gpio"]["bcm_2"]
        self.pi.hw_interfaces["gpio"]["bcm_2"].pin.connected = False
        # Check already connected with other interface.
        with self.assertRaises(MaxConnectionsError):
            i2c_con.connect()
            con.connect()

    def test_pwm(self):
        """Test pwm connection."""
        pass

    def test_i2c(self):
        """Test i2c connection."""
        self.devices()
        bme = DeviceHandler("bme680.hwd")

        gpio_con = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_2"],
                             hwint_2=self.sonar.hw_interfaces["gpio"]["echo"])
        gpio_con_2 = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_3"],
                               hwint_2=self.sonar.hw_interfaces["gpio"]["trigger"])
        i2c_con = I2c2I2c(hwint_1=self.pi.hw_interfaces["i2c"]["i2c_1"],
                          hwint_2=bme.hw_interfaces["i2c"]["i2c_0"])

        # Two master error
        with self.assertRaises(TwoMasterError):
            i2c_con.hwint_2 = self.pi.hw_interfaces["i2c"]["i2c_0"]
            i2c_con.connect()
        # Two slave error
        with self.assertRaises(TwoSlaveError):
            i2c_con.hwint_1 = bme.hw_interfaces["i2c"]["i2c_0"]
            i2c_con.hwint_2 = bme.hw_interfaces["i2c"]["i2c_0"]
            i2c_con.connect()

        i2c_con.hwint_1 = self.pi.hw_interfaces["i2c"]["i2c_1"]
        # Check already connected errors.
        with self.assertRaises(AlreadyConnectedError):
            gpio_con.connect()
            i2c_con.connect()
        with self.assertRaises(AlreadyConnectedError):
            gpio_con_2.connect()
            i2c_con.connect()
        with self.assertRaises(AlreadyConnectedError):
            gpio_con.hwint_1 = self.pi.hw_interfaces["gpio"]["bcm_0"]
            gpio_con_2.hwint_1 = self.pi.hw_interfaces["gpio"]["bcm_1"]
            sonar = DeviceHandler("hc_sr04.hwd")
            gpio_con.hwint_2 = sonar.hw_interfaces["gpio"]["echo"]
            gpio_con_2.hwint_2 = sonar.hw_interfaces["gpio"]["trigger"]
            gpio_con.connect()
            gpio_con_2.connect()
            i2c_con.connect()

    def test_spi(self):
        self.devices()
        icm = DeviceHandler("icm_20948.hwd")
        sonar = DeviceHandler("hc_sr04.hwd")

        gpio_con = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_10"],
                             hwint_2=self.sonar.hw_interfaces["gpio"]["echo"])
        gpio_con_2 = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_9"],
                               hwint_2=self.sonar.hw_interfaces["gpio"]["trigger"])
        gpio_con_3 = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_11"],
                               hwint_2=sonar.hw_interfaces["gpio"]["echo"])
        gpio_con_4 = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_7"],
                               hwint_2=sonar.hw_interfaces["gpio"]["trigger"])
        gpio_con_5 = Gpio2Gpio(hwint_1=self.pi.hw_interfaces["gpio"]["bcm_8"],
                               hwint_2=self.pi.hw_interfaces["gpio"]["bcm_2"])

        spi_con = Spi2Spi(hwint_1=self.pi.hw_interfaces["spi"]["spi_0"],
                          hwint_2=icm.hw_interfaces["spi"]["spi_0"])

        # Two master error
        with self.assertRaises(TwoMasterError):
            spi_con.hwint_2 = self.pi.hw_interfaces["spi"]["spi_1"]
            spi_con.connect()
        # Two slave error
        with self.assertRaises(TwoSlaveError):
            spi_con.hwint_1 = icm.hw_interfaces["spi"]["spi_0"]
            spi_con.hwint_2 = icm.hw_interfaces["spi"]["spi_0"]
            spi_con.connect()

        spi_con.hwint_1 = self.pi.hw_interfaces["spi"]["spi_0"]

        # Check connected mosi, miso sclk
        with self.assertRaises(AlreadyConnectedError):
            gpio_con.connect()
            spi_con.connect()
        with self.assertRaises(AlreadyConnectedError):
            self.pi.hw_interfaces["gpio"]["bcm_10"].pin.connected = False
            gpio_con_2.connect()
            spi_con.connect()
        with self.assertRaises(AlreadyConnectedError):
            self.pi.hw_interfaces["gpio"]["bcm_9"].pin.connected = False
            gpio_con_3.connect()
            spi_con.connect()
        with self.assertRaises(AlreadyConnectedError):
            self.pi.hw_interfaces["gpio"]["bcm_11"].pin.connected = False
            self.sonar.hw_interfaces["gpio"]["echo"].pin.connected = False
            sonar.hw_interfaces["gpio"]["echo"].pin.connected = False
            gpio_con.connect()
            gpio_con_3.connect()
            spi_con.connect()

        self.pi.hw_interfaces["gpio"]["bcm_10"].pin.connected = False
        self.pi.hw_interfaces["gpio"]["bcm_11"].pin.connected = False

        # Check if chip enabled are in use.
        with self.assertRaises(ChipEnabledFullError):
            gpio_con_4.connect()
            gpio_con_5.connect()
            spi_con.connect()
        self.pi.hw_interfaces["gpio"]["bcm_7"].pin.connected = False

        # Check right spi index.
        spi_con.connect()
        self.assertEqual(
            self.pi.hw_interfaces["spi"]["spi_0"].ce[spi_con.ce_index].name,
            "bcm_7", "Wrong chip enable pin."
        )

        # Use one chip enable and on spi and try one more
        with self.assertRaises(ChipEnabledFullError):
            icm_2 = DeviceHandler("icm_20948.hwd")
            spi_con_2 = Spi2Spi(hwint_1=self.pi.hw_interfaces["spi"]["spi_0"],
                                hwint_2=icm_2.hw_interfaces["spi"]["spi_0"])
            spi_con_2.connect()


if __name__ == "__main__":
    unittest.main()
