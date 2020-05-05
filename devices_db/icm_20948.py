import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/icm_20948.xmi"  # Name of the xmi


dev = Peripheral(vcc=3.3,
                 name="icm_20948",
                 type=PeripheralType.SENSOR,
                 operating_voltage=3.3,)
pin_1 = PowerPin(type=PowerType.GND, number=1)
pin_2 = PowerPin(type=PowerType.Power3V3, number=2)
pin_3 = DigitalPin(name="sda_mosi", number=3)
pin_4 = DigitalPin(name="scl", number=4)
pin_5 = DigitalPin(name="ad0_miso", number=5)
pin_6 = DigitalPin(name="nc_ce", number=6)

spi = SPI(mosi=pin_3, miso=pin_5, sclk=pin_4, ce=[pin_6])
gpio = GPIO(pin=pin_5, type=GPIOType.INPUT)
i2c = I2C(sda=pin_3, scl=pin_4)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4, pin_5, pin_6])
dev.hw_interfaces.extend([spi, gpio, i2c])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
