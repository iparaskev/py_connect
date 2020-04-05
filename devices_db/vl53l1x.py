import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/vl53l1x.xmi"  # Name of the xmi


dev = NonComputational(vcc=3.3, name="vl53l1x", type=DeviceType.SENSOR)
pin_1 = PowerPin(function=PowerType.POWER_3V3, number=1)
pin_2 = PowerPin(function=PowerType.GND, number=2)
pin_3 = DigitalPin(name="sda", number=3,
                   functions=[IOPinFunction(type=IOType.I2C_SDA, hw_port=0)])
pin_4 = DigitalPin(name="scl", number=4,
                   functions=[IOPinFunction(type=IOType.I2C_SCL, hw_port=0)])

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
