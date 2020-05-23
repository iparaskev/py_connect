"""test_device_m2m.py"""

import unittest
from py_connect import DeviceHandler
from py_connect import PowerType, PowerPin, DigitalPin
from py_connect import GPIOType


class TestDeviceM2M(unittest.TestCase):

    def test_board(self):
        pi = DeviceHandler("rpi_3b_plus.hwd")

        # Test attributes
        self.assertEqual(pi.dev.name, "rpi_3b_plus", "Wrong name error")
        self.assertEqual(pi.dev.vcc, 5, "Wrong voltage")
        self.assertEqual(pi.dev.timers, 1, "Wrong timers")
        self.assertEqual(pi.dev.dma, True, "Wrong dma")
        self.assertEqual(pi.dev.battery, False, "Wrong battery")
        self.assertEqual(pi.dev.memory.ram, 1*1024*1024, "Wrong ram")
        self.assertEqual(pi.dev.memory.rom, 0, "Wrong rom")
        self.assertEqual(pi.dev.network[0].name, "wlan0", "Wrong wifi name")
        self.assertEqual(pi.dev.network[1].name, "eth0", "Wrong ethernet name")

        # Check pins
        self.assertIsInstance(pi.dev.pins[0], PowerPin, "Wrong pin type.")
        self.assertEqual(pi.dev.pins[0], pi.power_pins["power_3v3_1"],
                         "Wrong mapping between power pin objects.")
        self.assertEqual(pi.dev.pins[0].name, "power_3v3_1", "Wrong pin name")
        self.assertEqual(pi.dev.pins[0].type, PowerType.Power3V3, "Wrong pin type")
        self.assertIsInstance(pi.dev.pins[2], DigitalPin, "Wrong pin type.")
        self.assertEqual(pi.dev.pins[2].name, "bcm_2", "Wrong pin name")
        self.assertEqual(pi.dev.pins[2].number, 3, "Wrong pin number")

        # Hardware interfaces
        # GPIO
        self.assertEqual(pi.dev.pins[2], pi.hw_interfaces["gpio"]["bcm_2"].pin,
                         "Wrong mapping between gpio pin objects.")
        self.assertEqual(pi.hw_interfaces["gpio"]["bcm_2"].type, GPIOType.BOTH,
                         "Wrong gpio type.")
        # I2C
        self.assertIn(pi.hw_interfaces["i2c"]["i2c_1"], pi.dev.hw_interfaces,
                      "I2c interface isn't in hw interfaces.")
        self.assertEqual(pi.hw_interfaces["i2c"]["i2c_1"].sda,
                         pi.hw_interfaces["gpio"]["bcm_2"].pin,
                         "I2c wrong sda pin.")
        self.assertEqual(pi.hw_interfaces["i2c"]["i2c_1"].scl,
                         pi.hw_interfaces["gpio"]["bcm_3"].pin,
                         "I2c wrong scl pin.")
        self.assertEqual(pi.hw_interfaces["i2c"]["i2c_1"].is_master, True,
                         "I2c should be master.")
        self.assertEqual(pi.hw_interfaces["i2c"]["i2c_1"].bus, 1,
                         "I2c bus should be 1.")
        self.assertEqual(pi.hw_interfaces["i2c"]["i2c_0"].bus, 0,
                         "I2c bus should be 0.")
        self.assertEqual(pi.hw_interfaces["i2c"]["i2c_0"].sda,
                         pi.hw_interfaces["gpio"]["bcm_0"].pin,
                         "I2c wrong sda pin.")

        # SPI
        self.assertIn(pi.hw_interfaces["spi"]["spi_1"], pi.dev.hw_interfaces,
                      "SPI interface isn't in hw interfaces.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_1"].mosi,
                         pi.hw_interfaces["gpio"]["bcm_20"].pin,
                         "SPI wrong mosi pin.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_1"].miso,
                         pi.hw_interfaces["gpio"]["bcm_19"].pin,
                         "SPI wrong miso pin.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_1"].sclk,
                         pi.hw_interfaces["gpio"]["bcm_21"].pin,
                         "SPI wrong sclk pin.")
        self.assertIn(pi.hw_interfaces["gpio"]["bcm_16"].pin,
                      pi.hw_interfaces["spi"]["spi_1"].ce,
                      "SPI wrong ce pin.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_1"].is_master, True,
                         "SPI should be master.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_1"].bus, 1,
                         "SPI bus should be 1.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_0"].bus, 0,
                         "SPI bus should be 0.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_1"].max_master_cons, 3,
                         "SPI should have 3 max_connections.")
        self.assertEqual(pi.hw_interfaces["spi"]["spi_0"].max_master_cons, 2,
                         "SPI should have 2 max_connections.")

        # PWM
        self.assertEqual(pi.hw_interfaces["pwm"]["bcm_12"].pin,
                         pi.hw_interfaces["gpio"]["bcm_12"].pin,
                         "PWM wrong pin.")
        self.assertEqual(pi.hw_interfaces["pwm"]["bcm_12"].pin.name,
                         "bcm_12", "PWM wrong pin.")

        # UART
        self.assertIn(pi.hw_interfaces["uart"]["uart_0"], pi.dev.hw_interfaces,
                      "UART interface isn't in hw interfaces.")
        self.assertEqual(pi.hw_interfaces["uart"]["uart_0"].tx,
                         pi.hw_interfaces["gpio"]["bcm_14"].pin,
                         "UART wrong tx pin.")
        self.assertEqual(pi.hw_interfaces["uart"]["uart_0"].rx,
                         pi.hw_interfaces["gpio"]["bcm_15"].pin,
                         "UART wrong rx pin.")
        self.assertEqual(pi.hw_interfaces["uart"]["uart_0"].bus, 0,
                         "UART bus should be 0.")


if __name__ == "__main__":
    unittest.main()
