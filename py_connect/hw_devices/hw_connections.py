"""behaviours.py

Add behaviours to hardware inteface connections.
"""

from .hw_devices import USB, ADC, I2C, SPI, UART, PWM, GPIO, Gpio2Gpio
from .hw_devices import Usb2Usb, Adc2Adc, I2c2I2c, Spi2Spi, Uart2Uart, Pwm2Pwm
from .hw_devices import Power2Power


def check_same(interface_1, interface_2):
    """Check if two interfaces are the same

    Args:
        interface_1 (HwInterface):
        interface_2 (HwInterface):

    Returns:
        (bool): Indicating if the two instances are of the same class.
    """
    pass


def usb_connect(self):
    """Adc connections."""
    pass


def adc_connect(self):
    """Adc connections."""
    pass


def i2c_connect(self):
    """I2c connections."""
    self.board_hw.master_conns.append(self.peripheral_hw)

    # TODO: Connectivity check
    # Use cases:
    #     * i2c-gpio: In gpio we have an error
    #     * gpio-i2c: Only one pin connected so erroneous connection
    #     * gpio-gpio-i2c: Both pins connected but no master conns so
    #                     erroneous connection.
    #     * i2c-i2c: Both connected and master_cons ,no problem.

    # Change connected flag for individual pins
    self.board_hw.sda.connected = True
    self.board_hw.scl.connected = True
    self.peripheral_hw.sda.connected = True
    self.peripheral_hw.scl.connected = True


def spi_connect(self):
    """spi connections."""
    self.board_hw.master_conns.append(self.peripheral_hw)

    # TODO: Connectivity check. Same as i2c.

    # Change connected flag for individual pins
    self.board_hw.miso.connected = True
    self.board_hw.mosi.connected = True
    self.board_hw.sclk.connected = True
    ce_index = 0
    while self.board_hw.ce[ce_index].connected:
        ce_index += 1
    self.board_hw.ce[ce_index].connected = True
    self.peripheral_hw.miso.connected = True
    self.peripheral_hw.mosi.connected = True
    self.peripheral_hw.sclk.connected = True
    self.peripheral_hw.ce[0].connected = True


def uart_connect(self):
    """uart connections."""
    self.board_hw.connection = self.peripheral_hw
    self.peripheral_hw.connection = self.board_hw


def pwm_connect(self):
    """pwm connections."""
    self.board_hw.connection = self.peripheral_hw
    self.peripheral_hw.connection = self.board_hw


def gpio_connect(self):
    """gpio connections."""
    # TODO check valid connectivity. If it is connected no connection.

    self.board_hw.connection = self.peripheral_hw
    self.peripheral_hw.connection = self.board_hw.connection


# Add the behaviours to the meta classes
#HwInt2HwInt.connect = connect
#HwInt2HwInt.i2c_connect = i2c_connect
#HwInt2HwInt.spi_connect = spi_connect
#HwInt2HwInt.uart_connect = uart_connect
#HwInt2HwInt.pwm_connect = pwm_connect
#HwInt2HwInt.gpio_connect = gpio_connect
