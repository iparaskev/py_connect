import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/tfmini.xmi"  # Name of the xmi


dev = Peripheral(vcc=5.0,
                 name="tfmini",
                 type=PeripheralType.SENSOR,
                 operating_voltage=3.3)
pin_1 = PowerPin(type=PowerType.Power5V, number=1)
pin_2 = PowerPin(type=PowerType.GND, number=2)
pin_3 = DigitalPin(name="tx", number=3)
pin_4 = DigitalPin(name="rx", number=4)

uart = UART(rx=pin_4, tx=pin_3)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])
dev.hw_interfaces.extend([uart])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
