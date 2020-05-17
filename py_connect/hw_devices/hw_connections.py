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
    # TODO: Connectivity check
    # Use cases:
    #     * i2c-gpio: In gpio we have an error
    #     * gpio-i2c: Only one pin connected so erroneous connection
    #     * gpio-gpio-i2c: Both pins connected but no master conns so
    #                     erroneous connection.
    #     * i2c-i2c: Both connected and master_cons ,no problem.
    # I2C logic error
    if self.hwint_1.is_master and self.hwint_2.is_master:
        print("Can't connect two master interfaces.")

    # General hw int errors
    check_ints(self.hwint_1, self.hwint_2)

    # Update interfaces
    update_int(self.hwint_1, [self.hwint_1.sda, self.hwint_1.scl])
    update_int(self.hwint_2, [self.hwint_2.sda, self.hwint_2.scl])


def spi_connect(self):
    """spi connections."""
    # TODO: Connectivity check. Same as i2c.
    # Find proper ce index
    self.ce_index = self.hwint_1.num_connections

    # Spi logic error
    if self.hwint_1.is_master and self.hwint_2.is_master:
        print("Can't connect two master interfaces.")

    # General hw int erros
    check_ints(self.hwint_1, self.hwint_2, master_flag=True)

    # Update interfaces
    update_int(self.hwint_1,
               [self.hwint_1.mosi, self.hwint_1.miso,
                self.hwint_1.sclk, self.hwint_1.ce[self.ce_index]])
    update_int(self.hwint_2,
               [self.hwint_2.mosi, self.hwint_2.miso,
                self.hwint_2.sclk, self.hwint_2.ce[0]])


def uart_connect(self):
    """uart connections."""
    pass


def pwm_connect(self):
    """pwm connections."""
    # General hw int erros
    check_ints(self.hwint_1, self.hwint_2)

    # Update interfaces
    update_int(self.hwint_1, [self.hwint_1.pin])
    update_int(self.hwint_2, [self.hwint_2.pin])


def gpio_connect(self):
    """gpio connections."""
    # GPIO logic error
    if self.hwint_1.type == self.hwint_2.type and not self.hwint_1 == GPIOType.BOTH:
        print("Invalid connection. GPIO types should be input-output")

    # General hw int erros
    check_ints(self.hwint_1, self.hwint_2)

    # Update interfaces
    update_int(self.hwint_1, [self.hwint_1.pin])
    update_int(self.hwint_2, [self.hwint_2.pin])


def update_int(hw_int, pins):
    """Update the connections for a hw interface and the state of the pins that
    it has.

    Args:
        hw_int (HwInterface):
        pins (list): A list with Pin objects.
    """
    hw_int.num_connections += 1
    for pin in pins:
        pin.connected = True


def check_ints(hwint_1, hwint_2, master_flag=False):
    """Check if two hw interfaces have exceed the max connections before their
    connection.

    Args:
        hwint_1 (HwInterface):
        hwint_2 (HwInterface):
        master_flag (bool):

    Raises:
    """
    max_c = hwint_1.max_master_cons if master_flag else hwint_1.max_connections
    if hwint_1.num_connections == max_c:
        print(f"{hwint_1.name} can't make more than {max_c} connections.")

    max_c = hwint_2.max_connections
    if hwint_2.num_connections == max_c:
        print(f"{hwint_2.name} can't make more than {max_c} connections.")


# Add the behaviours to the meta classes
Gpio2Gpio.connect = gpio_connect
Pwm2Pwm.connect = pwm_connect
Spi2Spi.connect = spi_connect
I2c2I2c.connect = i2c_connect
