import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/vl53l1x.xmi"  # Name of the xmi


dev = Peripheral(vcc=3.3,
                 name="vl53l1x",
                 type=PeripheralType.SENSOR,
                 operating_voltage=3.3,
                 i2cs=1)
pin_1 = Power3V3(number=1)
pin_2 = Gnd(number=2)
pin_3 = DigitalPin(name="sda", number=3)
pin_4 = DigitalPin(name="scl", number=4)

i2c = I2C(sda=pin_3, scl=pin_4)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])
dev.hw_interfaces.extend([i2c])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
