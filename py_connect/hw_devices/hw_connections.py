"""behaviours.py

Add behaviours to hardware inteface connections.
"""

from hw_devices import USB, ADC, I2C, SPI, UART, PWM, GPIO, HwInt2HwInt


def connect(self):
    """Connect two hardware interfaces.

    They must be of the same type.
    """

    # Handle USB connection
    if isinstance(self.board_hw, USB):
        self.usb_connect()

    # Handle ADC connection
    if isinstance(self.board_hw, ADC):
        self.adc_connect()

    # Handle I2C connection
    if isinstance(self.board_hw, I2C):
        self.i2c_connect()

    # Handle SPI connection
    if isinstance(self.board_hw, SPI):
        self.spi_connect()

    # Handle UART connection
    if isinstance(self.board_hw, UART):
        self.uart_connect()

    # Handle PWM connection
    if isinstance(self.board_hw, PWM):
        self.pwm_connect()

    # Handle GPIO connection
    if isinstance(self.board_hw, GPIO):
        self.gpio_connect()


def usb_connect(self):
    """Adc connections."""
    pass


def adc_connect(self):
    """Adc connections."""
    pass


def i2c_connect(self):
    """I2c connections."""
    self.board_hw.master_cons = self.peripheral_hw

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
    self.board_hw.master_cons = self.peripheral_hw

    # TODO: Connectivity check. Same as i2c.

    # Change connected flag for individual pins
    self.board_hw.miso.connected = True
    self.board_hw.mosi.connected = True
    self.board_hw.sclk.connected = True
    ce_index = 0
    while self.board_hw.ce[ce_index]:
        ce_index += 1
    self.board_hw.ce[ce_index] = True
    self.peripheral_hw.miso.connected = True
    self.peripheral_hw.mosi.connected = True
    self.peripheral_hw.sclk.connected = True
    self.peripheral_hw.ce[0] = True


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
HwInt2HwInt.connect = connect
HwInt2HwInt.i2c_connect = i2c_connect
HwInt2HwInt.spi_connect = spi_connect
HwInt2HwInt.uart_connect = uart_connect
HwInt2HwInt.pwm_connect = pwm_connect
HwInt2HwInt.gpio_connect = gpio_connect
