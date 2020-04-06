import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/bme680.xmi"  # Name of the xmi


dev = Peripheral(vcc=3.3, 
                 name="bme680",
                 type=PeripheralType.SENSOR,
                 operating_voltage=3.3,
                 i2cs=1)
pin_1 = PowerPin(function=PowerType.POWER_5V, number=1)
pin_2 = DigitalPin(name="sda", number=2)
pin_3 = DigitalPin(name="scl", number=3)
pin_4 = PowerPin(function=PowerType.GND, number=4)

i2c = I2C(sda=pin_2, scl=pin_3)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])
dev.hw_interfaces.extend([i2c])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
